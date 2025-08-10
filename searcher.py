import requests
from bs4 import BeautifulSoup 

scrape_results = []
    
    
search_url = "https://www.blackcircles.com/tyres/205-55-16"

try:
# This is the only request made to the server, fufilling the ethical component of the task as 1 request is the minimum possible
    response = requests.get(search_url) 
except:
    None
    
content = response.content
soup = BeautifulSoup(content, 'html.parser')
# This element is the wrapper of all the tyres on the page
deal_results_wrap: BeautifulSoup = soup.find_all('div',class_ = "deal-results-wrap")
    
for deal_result in deal_results_wrap:
    # This is the element containing the detials of the individual tyre
    brand_spec_wrap:BeautifulSoup = deal_result.find('div', class_ = "brandSpecWrap")
    
    # This anchor and header contain the brand, pattern, and size of the tyre
    mode_size_wrap:BeautifulSoup = brand_spec_wrap.find('a', class_ = "modelSizeWrap")

    infomation_header:BeautifulSoup = mode_size_wrap.find('h3')

    # This element contains the brand then the pattern of the tyre
    tyre_name_wrap:BeautifulSoup = infomation_header.find('span', class_ = "tyreNameWrap")
    model_size:BeautifulSoup = infomation_header.find('p', class_ = "model-size")
    
    break