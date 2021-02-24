from get_categories import get_categories
from requests_html import HTMLSession
from paginate import paginate
from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import time
import os

s = HTMLSession()
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
			continue
	# return cleaned link
	return(link)

def download_images(url_list, reference):
	'''
	Input:
		url       : list with all urls of images within a product
		reference : reference name to use in images filenames
	
	Output:
		img_names : names of the image filenames
	'''
	save_path = '/media/MLdata/scraped_imgs/'
	# start image count index and empty list
	idx = 1
	img_names = []
	for url in url_list:
		if idx%len(url_list)==0:
			print(f'Downloaded {idx}/{len(url_list)} images')
		filename = reference + f'_{idx}.jpg'
		img_names.append(filename)
		try:
			urllib.request.urlretrieve(url, os.path.join(save_path, filename))
		except:
			print(f'{url} is having trouble with the download of the image with filename: {filename}\nStoring details in img_url_error_log.txt and file_error_log.txt.')
			url_error = open('img_url_error_log.txt', 'a')
			url_error.write(f'{url}\n')
			url_error.close()
			file_error = open('file_error_log.txt', 'a')
			file_error.write(f'{filename}\n')
			file_error.close()
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
			continue

	img_names = download_images(imgs_urls, reference)
	return(img_names)

def request(url):
	r = s.get(url)
	r.html.render(sleep=1)
	return(r.html.xpath('/html/body/form/div[2]/div/div/div[1]/div/div[1]/div[3]/div[2]/div/div/div[3]', first=True))
                        
def parse(products, category):
	for item in products.absolute_links:
		item = check_bad_string_links(item)
		# request to product link
		try:
			r = s.get(item)
		except:
			print(f'Unable to make request to {item} logging error to productLink_error_log.txt')
			product_link_error = open('productLink_error_log.txt', 'a')
			product_link_error.write(f'{item}\n')
			product_link_error.close() 
			continue
		# get product info from product link
		try:
			string = r.html.find('div.hola', first=True).text.split('\n', maxsplit=2)
		except:
			print(f'Unable to get product info from {item} logging error to productInfo_error_log.txt')
			product_info_error = open('productInfo_error_log.txt', 'a')
			product_info_error.write(f'{item}\n')
			product_info_error.close() 
			continue
		# save the relevant features
		name = string[0]
		ref = string[1]
		description = string[-1].replace('\n', ' ')
		url = item
		img_names = get_images(url, ref)

		product = {
			'name': name,
			'category': category,
			'reference': ref,
			'description': description,
			'url': url,
			'img_names': img_names
		}
		product_list.append(product)

def output(csv_filename):
	df = pd.DataFrame(product_list)
	csv_filename += '.csv'
	df.to_csv(csv_filename, index=False)
	print(f'Saved csv file as {csv_filename}')


# get category names and respective url
cat_urls, cat_names = get_categories(base_url=base_url)
N_cats = len(cat_urls)
w = 1

start_time = time.time()

for x, y in zip(cat_urls, cat_names):
	product_list = []
	print(f'Retrieving data from category {w}/{N_cats} : {y}')
	# get the list of every page within tthe current product
	page_list = paginate(x, base_url)
	N_pages = len(page_list)
	v = 1
	for page in page_list:
		products = request(page)
		print(f'Getting items from page {v}/{N_pages}')
		parse(products, y)
		total_products = len(product_list)
		print('Total items: {}'.format(total_products))		
		v += 1
		time.sleep(1)
	print('\n')
	output(y)
	w += 1	
# consider putting time log
print('--------This process took %s seconds--------' %(time.time() - start_time))