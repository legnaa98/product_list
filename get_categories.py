from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import time

s = HTMLSession()

def get_categories(url='https://www.catalogospromocionales.com/seccion/subcategorias.html'):
	'''
	Inputs:
		url       : is the main product web-page from where each product category and name will be retrieved
	Output:
		cat_urls  : a list containing the url for each category
		cat_names : a list containing the name of every category 
	'''

	# make the request to the url
	r = s.get(url)
	# use beautifulsoup to extract html with lxml parser
	soup = bs(r.content, 'lxml')
	# retrieve categories
	categories = soup.find_all('div', class_='categoria')
	
	# category url and name lists
	cat_urls = []
	cat_names = []

	# for each category obtain url and name
	for category in categories:
		# get url for category
		url = category.find_all('a', href=True)[-1]['href']
		cat_urls.append(url)
		# get category name
		name = url.split('/')[-1].split('.html')[0]
		cat_names.append(name)
	
	return(cat_urls, cat_names)

if __name__ == '__main__':
	get_categories()