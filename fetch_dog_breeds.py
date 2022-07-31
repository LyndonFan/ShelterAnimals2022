import requests
import urllib
from bs4 import BeautifulSoup

url = 'https://www.thekennelclub.org.uk/search/breeds-a-to-z/'
response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
children = soup.find_all('strong', {'class': 'm-breed-card__title'})

breeds = [c.text for c in children]
with open('dog_breeds.txt', 'w+') as f:
    f.write('\n'.join(breeds))
