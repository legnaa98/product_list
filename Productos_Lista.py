import requests
from bs4 import BeautifulSoup

# the base url to be scraped
baseurl = 'https://www.catalogospromocionales.com/seccion/subcategorias.html'

# change the user agent to make requests without getting blocked
headers = {
	'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

}

r = requests.get('https://www.catalogospromocionales.com/promocionales/mugs.html')
soup = BeautifulSoup(r.content, 'lxml')


productlist = soup.find_all('div', class_='itemProducto- newD2018 col-lg-4 col-md-4 col-sm-4 col-xs-6 ')

print(productlist)