import requests
from bs4 import BeautifulSoup
from databaseManager import databaseManager


# https://www.national.co.uk/tyres-search/205-55-16?pc=S254FF
# national.co.uk uses a structure of /tyre-search/width-aspect ratio-wim size?postcode
# ?postcode is optional

# Needed information: website, brand, pattern, size, season, price

NATIONAL_BASE_URL: str = "https://www.national.co.uk/tyres-search"


def scrape_national(info: tuple):
    search_url = NATIONAL_BASE_URL + f"/{info[0]}-{info[1]}-{info[2]}"

    try:
        response = requests.get(search_url)             
    except:
        return f"GET {search_url} returned error"
    
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    all_tyreresults: BeautifulSoup = soup.find_all('div',class_ = "tyreresult")
    
    for tyreresult in all_tyreresults:
        details = tyreresult.find('div', class_ = "details")
        # the only image in details is the brand image, which has alt text of the brand name
        brand_image = details.find('img')
        brand_name = brand_image.get('alt')   
    
print(scrape_national((205, 55, 16)))