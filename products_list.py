from requests_html import HTMLSession
import pandas as pd
import time

#url = 'https://www.catalogospromocionales.com/promocionales/mugs.html'
#https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page=17
s = HTMLSession()
product_list = []

def request(url):
	r = s.get(url)
	r.html.render(sleep=1)
	return(r.html.xpath('/html/body/form/div[2]/div/div/div[1]/div/div[1]/div[3]/div[2]/div/div/div[3]', first=True))

def parse(products):
	for item in products.absolute_links:
		r = s.get(item)
		string = r.html.find('div.hola', first=True).text.split('Unidades por Caja')
		string = string[:-1]
		string = string[0].split('\n', maxsplit=2)
		
		# save the relevant features
		name = string[0]
		ref = string[1]
		description = string[-1].replace('\n', ' ')

		product = {
			'name': name,
			'reference': ref,
			'description': description
		}
		product_list.append(product)

def output():
	df = pd.DataFrame(product_list)
	df.to_csv('products_demo.csv', index=False)
	print('Saved to csv file')

x = 1
'''
while True:
	try:
		#https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=23&Page={x}
		products = request(f'https://www.catalogospromocionales.com/Catalogo/Default.aspx?id=253&Page={x}')
		print('Getting items from page {}'.format(x))
		parse(products)
		print('Total items: {}'.format(len(product_list)))
		x += 1
		time.sleep(3)
	except:
		print('No more items!')
		break

output()'''