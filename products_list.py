from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

#url = 'https://www.catalogospromocionales.com/promocionales/mugs.html'
#https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page=17
s = HTMLSession()
product_list = []
base_url = 'https://www.catalogospromocionales.com'

def clean_link(link, bad_character):
	# clean bad links
	bad_link_example = 'https://www.catalogospromocionales.com/p/botilito-swivel-300ml-<span>OFERTA</span>/7469/23'
	# return cleaned link
	return(link.replace(bad_character, ''))

def check_bad_string_links(link):
	# check if a link contains a bad sting that will cause a bad request
	bad_character_list = ['<span>', '</span>']
	for character in bad_character_list:
		if character in link:
			link = clean_link(link, character)
		else:
			pass
	# return cleaned link
	return(link)

def get_images(link, reference):
	'''
	Inputs:
		link      : link to be scraped
		reference : reference name to use in images filenames
	'''
	r = s.get(link)
	soup = bs(r.content, 'lxml')
	#main_img = soup.find_all('div', id='gal1') # need procesing
	imgs = soup.find_all('img', alt="")
	for item in imgs:
		img_url = item.get('src')
		# check if image is primary image with url pattern
		# check if image is alternate image with url pattern
		# discard all images that are not primary or alternate
		# complete urls of alternate images with base url
	# proceed to download images and rename them with the indicator of the reference


	


def request(url):
	r = s.get(url)
	r.html.render(sleep=1)
	return(r.html.xpath('/html/body/form/div[2]/div/div/div[1]/div/div[1]/div[3]/div[2]/div/div/div[3]', first=True))

def parse(products):
	for item in products.absolute_links:
		item = check_bad_string_links(item)
		r = s.get(item)
		string = r.html.find('div.hola', first=True).text.split('\n', maxsplit=2)
		
		# save the relevant features
		name = string[0]
		ref = string[1]
		description = string[-1].replace('\n', ' ')

		product = {
			'name': name,
			'reference': ref,
			'description': description,
			'url': item
		}
		product_list.append(product)

def output():
	df = pd.DataFrame(product_list)
	df.to_csv('products_demo.csv', index=False)
	print('Saved to csv file')



x = 1
total_products_cache = []

'''while True:
	try:
		#https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page={x}
		products = request(f'https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page={x}')
		print('Getting items from page {}'.format(x))
		parse(products)
		total_products = len(product_list)
		print('Total items: {}'.format(total_products))

		total_products_cache.append(total_products)
		if x!=1:
			if total_products_cache[-1] != total_products_cache[-2]:
				x += 1
				time.sleep(1)
			else:
				break
		else:
			x += 1
			time.sleep(1)
	except:
		print('No more items!')
		break

output()'''