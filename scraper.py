import requests
from bs4 import BeautifulSoup
from databaseManager import databaseManager
import sys
from selenium import webdriver



# https://www.national.co.uk/tyres-search/205-55-16?pc=S254FF
# national.co.uk uses a structure of /tyre-search/width-aspect ratio-wim size?postcode
# ?postcode is optional

# Needed information: website, brand, pattern, size, season, price

NATIONAL_SEARCH_URL: str = "https://www.national.co.uk/tyres-search"
BASE_BLACKCIRCLES_URL: str = "https://www.blackcircles.com/tyres"
BYTHJUL_SEARCH_URL: str = "https://www.bythjul.com/sok/storlek/dack/0/DS"
SUMMER = "summer"
WINTER = "winter"

PROXY = "192.0.0.1:50"

def find_seasonality(pattern: str):
    if WINTER in pattern.lower():
        return WINTER
            
    if SUMMER in pattern.lower():
        return SUMMER
            
    if "4seasons" in pattern.lower() or "all season" in pattern.lower():
        return "all"
    
    return "na"


def scrape_national(width, aspect_ratio, rim_size) -> list[tuple]:
    scrape_results = []
    
    
    search_url = NATIONAL_SEARCH_URL + f"/{width}-{aspect_ratio}-{rim_size}"

    try:
        # This is the only request made to the server, fufilling the ethical component of the task as 1 request is the minimum possible
        response = requests.get(search_url)             
    except:
        return None
    
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    # This element is the wrapper of all the tyres on the page
    all_tyreresults: BeautifulSoup = soup.find_all('div',class_ = "tyreresult")
    
    for tyreresult in all_tyreresults:
        # This is the element containing the detials of the individual tyre
        details:BeautifulSoup = tyreresult.find('div', class_ = "details")
        # the only image in details is the brand image, which has alt text of the brand name
        brand_image = details.find('img')
        brand = brand_image.get('alt')   
        # there are then 4 <p>s which are the pattern, size, load index, speed rating, then a black <p>
        pattern = details.find_next('p')
        # the <p> after the tyre pattern is the tyre size
        size = pattern.find_next('p')
        
        # Extracts the pattern and size text from the <p> tags containing them
        pattern: str = pattern.text.strip()
        size:str = size.text.strip()
        
        # The red text is the price text object on the page
        red_text = tyreresult.find('span', class_ = "red text-24")
        price:BeautifulSoup = red_text.find('strong')
        price:str = price.text
        # replace most common currency symbols with nothing so only number left
        price = price.replace("£", "")
        price = price.replace("$", "")
        price = price.replace("€", "")
        price = price.strip()
        
        seasonality = find_seasonality(pattern = pattern)
        
        scrape_results.append(("national.co.uk", brand, pattern, size, seasonality, price))
    return scrape_results

def scrape_blackcircles(width, aspect_ratio, rim_size) -> list[tuple]:
    scrape_results = []
    
    
    search_url = BASE_BLACKCIRCLES_URL + f"/{width}-{aspect_ratio}-{rim_size}"

    try:
        response = requests.get(search_url)             
        # This is the only request made to the server, fufilling the ethical component of the task as 1 request is the minimum possible
    except:
        return None
    
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    # This element is the wrapper of all the tyres on the page
    deal_results_wrap: BeautifulSoup = soup.find('div',class_ = "deal-results-wrap")
    res_boxes = deal_results_wrap.find_all("div", class_=["resBox", "featured"])

    
    for i, res_box in enumerate(res_boxes):
        brand_spec_wrap:BeautifulSoup = res_box.find('div', class_ = "brandSpecWrap")
        
        # This anchor and header contain the brand, pattern, and size of the tyre
        mode_size_wrap:BeautifulSoup = brand_spec_wrap.find('a', class_ = "modelSizeWrap")
        infomation_header:BeautifulSoup = mode_size_wrap.find('h3')
        
        # This element contains the brand then the pattern of the tyre
        tyre_name_wrap:BeautifulSoup = infomation_header.find('span', class_ = "tyreNameWrap")
        model_size:BeautifulSoup = infomation_header.find('p', class_ = "model-size")
        
        tyre_brand_and_name:str = tyre_name_wrap.text
        
        # The brand is the first element of the string so this gets that out
        brand = tyre_brand_and_name.split(' ')[0]
        
        # Cleanly removes the brand to isolate the name
        pattern = tyre_brand_and_name.replace(brand, "").strip()

        size = model_size.text.strip()
        
        # The red text is the price text object on the page
        tyre_price:BeautifulSoup = res_box.find('div', class_ = "tyrePrice")
        # The pounds of the price is the text of the <div>
        price = tyre_price.text.strip()

        price = price.replace("£", "")
        price = price.replace("$", "")
        price = price.replace("€", "")
        price = price.strip()
        
        seasonality = find_seasonality(pattern = pattern)
        
        scrape_results.append(("blackcircles.com", brand, pattern, size, seasonality, price))
    return scrape_results


# Dexel used html selected tags to load the selected tyres which cannot be loaded by a conventional url search
# A branch (shop) must be selected so scrappign the entire stock seems undoable
# My guess is the dexel uses URL masking as every webpage has the url https://www.dexel.co.uk/tyres#tyres
# Using the network panel on inspect it seems there is only 1 tyres web page but javascript is used to hot load content to the page
# This means a more sophisticaed approach would be nessasary to scrape data from Dexel, as dialouge needs to be populated, then scripts run, then data scraped.

# bythjul is protected by cloudflare therefore this either need be bypassed, however "you must attempt to be ethical while scraping a website" is a specification of the task.
# Therefore the better approch would be to find an API route, which falls outside of the scope of this task
def scrape_bythjul(width, aspect_ratio, rim_size) -> list[tuple]:
    scrape_results = []
    
    search_url = BYTHJUL_SEARCH_URL + f"/{width}-{aspect_ratio}-{rim_size}"#!price=520.35,1653.25&special=hideCtyre"
    print(f"I AM SEARCHING {search_url}")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--proxy-server={PROXY}")
    driver = webdriver.Chrome(options=options)
    
    try:
        # response = requests.get(search_url)  
        response = driver.get(search_url)           
    except:
        driver.close()
        return None    
    
    soup = BeautifulSoup(driver.page_source, "html")
    driver.close()

  

        
        
python_file, width, aspect_ratio, rim_size = sys.argv
# scrape = scrape_bythjul(width=width, aspect_ratio=aspect_ratio, rim_size=rim_size)
scrape = scrape_national(width=width, aspect_ratio=aspect_ratio, rim_size=rim_size)
scrape += scrape_blackcircles(width=width, aspect_ratio=aspect_ratio, rim_size=rim_size)

# If the scrape function has returned none it means no search results were found
# Tested with W 185 AR 16 RS 14
# if not scrape:
#     print(f"No search results for Width {width} AR {aspect_ratio} Rim {rim_size}")


db_manager: databaseManager = databaseManager("database")

for line in scrape:
      db_manager.create((width, aspect_ratio, rim_size), line)
      