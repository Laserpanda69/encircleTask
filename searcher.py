import requests
from bs4 import BeautifulSoup 

url = "https://www.dexel.co.uk/tyres#tyres"


response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())