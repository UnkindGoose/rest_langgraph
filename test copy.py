from bs4 import BeautifulSoup
import requests


base_url = 'https://guide.michelin.com'
restaurants_url = 'https://guide.michelin.com/en/restaurants'
desc_selector = '.data-sheet__description'
links_selector = 'link'
main_loader = WebBaseLoader(restaurants_url)
main_docs = main_loader.load()
soup = BeautifulSoup(main_docs[0].page_content, 'html.parser')

main_div = soup.find('div', class_='js-restaurant__list_items')
links = []
if main_div:
    link_tags = main_div.find_all('a', class_='link')
    links = [base_url + a.get('href') for a in link_tags if a.get('href')]

michelin_examples = []

for link in links:
    loader = WebBaseLoader(link)
    docs = loader.load()
    soup = BeautifulSoup(docs[0].page_content, 'html.parser')
    desc_div = soup.select_one(desc_selector)
    if desc_div:
        michelin_examples.append(desc_div.get_text().strip())
        

    
print(michelin_examples)