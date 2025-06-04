from bs4 import BeautifulSoup
import requests
from langchain_community.document_loaders import WebBaseLoader

base_url = 'https://guide.michelin.com'
restaurants_url = 'https://guide.michelin.com/en/restaurants'
desc_selector = '.data-sheet__description'
links_selector = ['link']

def fetch_page(url):
    
    response = requests.get(url)
    response.raise_for_status()
    return response.text
    
    
def parse_page(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    desc_div = soup.select_one(desc_selector)
    
    if not desc_div:
        return None

    return desc_div.get_text()
    
test = fetch_page(restaurants_url)
soup = BeautifulSoup(test, 'html.parser')

main_div = soup.find('div', class_='js-restaurant__list_items')

links = []
if main_div:
    link_tags = main_div.find_all('a', class_='link')
    links = [base_url + a.get('href') for a in link_tags if a.get('href')]


michelin_examples = []
for link in links:
        
        page_html = fetch_page(link)
            
        page_data = parse_page(page_html)
        michelin_examples.append(page_data)
    
    
print(michelin_examples)