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
BYTHJUL_SEARCH_URL: str = "https://www.bythjul.com/sok/storlek/dack/0/DS"
SUMMER = "summer"
WINTER = "winter"

PROXY = "192.0.0.1:50"


def scrape_national(width, aspect_ratio, rim_size) -> list[tuple]:
    scrape_results = []
    
    search_url = NATIONAL_SEARCH_URL + f"/{width}-{aspect_ratio}-{rim_size}"

    try:
        response = requests.get(search_url)             
    except:
        return None
    
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    all_tyreresults: BeautifulSoup = soup.find_all('div',class_ = "tyreresult")
    
    for tyreresult in all_tyreresults:
        details:BeautifulSoup = tyreresult.find('div', class_ = "details")
        # the only image in details is the brand image, which has alt text of the brand name
        brand_image = details.find('img')
        brand = brand_image.get('alt')   
        # there are then 4 <p>s which are the pattern, size, load index, speed rating, then a black <p>
        pattern = details.find_next('p')
        size = pattern.find_next('p')
        
        pattern: str = pattern.text.strip()
        size:str = size.text.strip()
        
        red_text = tyreresult.find('span', class_ = "red text-24")
        price:BeautifulSoup = red_text.find('strong')
        price:str = price.text
        # replace most common currency symbols with nothing so only number left
        price = price.replace("£", "")
        price = price.replace("$", "")
        price = price.replace("€", "")
        price = price.strip()
        
        # national does not give seasonality
        seasonality = "na"
        
        if WINTER in pattern.lower():
            seasonality = WINTER
            
        if SUMMER in pattern.lower():
            seasonality = SUMMER
            
        if "4seasons" in pattern.lower() or "all season" in pattern.lower():
            seasonality = "all"
        
        scrape_results.append(("national.co.uk", brand, pattern, size, seasonality, price))
    return scrape_results


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

    print(soup.prettify())        
        
python_file, width, aspect_ratio, rim_size = sys.argv
# scrape = scrape_bythjul(width=width, aspect_ratio=aspect_ratio, rim_size=rim_size)
scrape = scrape_national(width=width, aspect_ratio=aspect_ratio, rim_size=rim_size)
if not scrape:
    print(f"No search results for Width {width} AR {aspect_ratio} Rim {rim_size}")


db_manager: databaseManager = databaseManager("database")

for line in scrape:
      db_manager.create((width, aspect_ratio, rim_size), line)