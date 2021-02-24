from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import time
import os

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

def download_images(url_list, reference):
	'''
	Input:
		reference : reference name to use in images filenames
	Output:
		img_names : names of the image filenames
	'''
	save_path = '/media/MLdata/scraped_imgs/'
	# start image count index and empty list
	idx = 1
	img_names = []
	for url in url_list:
		filename = reference + f'_{idx}.jpg'
		img_names.append(filename)
		urllib.request.urlretrieve(url, os.path.join(save_path, filename))
		idx += 1

	return(img_names)



def get_images(link, reference):
	'''
	Inputs:
		link      : link to be scraped
	Output:
		img_names : names of the image filenames
	'''
	r = s.get(link)
	soup = bs(r.content, 'lxml')
	imgs_urls = []

	# find all images in link
	imgs = soup.find_all('img', alt="")
	for item in imgs:
		img_url = item.get('src')
		# check if image is primary or alternate image with url pattern
		if 'https://' in img_url:
			imgs_urls.append(img_url)
		elif '/images' in img_url[0:7]:
			imgs_urls.append(base_url + img_url)
		else:
			pass

	img_names = download_images(imgs_urls, reference)
	return(img_names)

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
		url = item
		img_names = get_images(url, ref)

		product = {
			'name': name,
			'reference': ref,
			'description': description,
			'url': url,
			'img_names': img_names
		}
		product_list.append(product)

def output():
	df = pd.DataFrame(product_list)
	df.to_csv('products_demo.csv', index=False)
	print('Saved to csv file')



x = 1
total_products_cache = []

while True:
	try:
		#https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page={x}
		products = request(f'https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=292&Page={x}')
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

output()