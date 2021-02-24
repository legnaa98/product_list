from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import time

s = HTMLSession()

def paginate(category_url, base_url):
	'''
	Inputs:
		base_url     : base web-site url to buil on top of for the pagination
		category_url : corresponds to the first page url
	
	Outputs:
		pag_list     : a list containing all the urls for each page of the current product
	'''

	# define request
	r = s.get(category_url)
	# extract html  data with lxml parser
	soup = bs(r.content, 'lxml')
	# extract info from the  bottom page regartding to the numbe of pages
	stuff = soup.find_all('span', class_='paging1Catalogo' )
	# pages are always stored in the last element of "stuff"
	# their links can be easily retrieved
	pages = stuff[-1].find_all('a', href=True)

	# pages list
	pag_list = [category_url]
	for i in range(len(pages)):
		url = base_url + pages[i]['href']
		pag_list.append(url)
	return(pag_list)

if __name__ == '__main__':
	paginate(category_url='https://www.catalogospromocionales.com/promocionales/confeccion.html',
	         base_url='https://www.catalogospromocionales.com')