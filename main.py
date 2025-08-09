import requests
from bs4 import BeautifulSoup
from databaseManager import databaseManager


# https://www.national.co.uk/tyres-search/205-55-16?pc=S254FF
# national.co.uk uses a structure of /tyre-search/width-aspect ratio-wim size?postcode
# ?postcode is optional

# Needed information: website, brand, pattern, size, season, price

NATIONAL_BASE_URL: str = "https://www.national.co.uk/tyres-search"
SUMMER = "summer"
WINTER = "winter"


def scrape_national(info: tuple) -> list[tuple]:
    scrape_results = []
    
    search_url = NATIONAL_BASE_URL + f"/{info[0]}-{info[1]}-{info[2]}"

    try:
        response = requests.get(search_url)             
    except:
        return f"GET {search_url} returned error"
    
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
            
scrape = scrape_national((205, 55, 16))
for scar in scrape:
    print(scar[2], scar[4])