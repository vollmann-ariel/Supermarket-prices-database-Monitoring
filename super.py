def descarga_página(soup):
  all_divs = soup.find_all('div', attrs={'class':'prateleira__item'})
  productos = []
  for item in all_divs:
    producto = {}
    producto['title'] = item['title']
    producto['price'] = item.find(class_='originalBestPrice hidden').text
    producto['brand'] = item.find('div',class_='itemBrand hidden').find('p').text
    producto['link'] = item.find('a',class_='prateleira__flags')['href']
    productos.append(producto)
  return productos


import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import random
  
# Páginas de cada familia de productos
pages = ['1','499','40','47','107','26','515','137','123','414','472','775','790','459','1041','1084','1070',
         '390','396','403','411','389','359','383','351','355','172','206','212','277','259','253','591',
         '221','282','290','295','315','298','322','1028','331','335','345']
sucursal = 22

complete_list = []

for pag in pages:
  page_number = 1
  while True:
    url = f'https://www.walmart.com.ar/buscapagina?sl=63c6cac5-a4b5-4191-a52a-65582db8f8b3&PS=48&cc=50&PageNumber={page_number}&O=OrderByReviewRateDESC&sm=0&fq=C:/{pag}/&sc={sucursal}'
    sleep(2 * random())
    response = requests.get(url)
    if len(response.text) == 0: break
    print(pag)
    page = response.text
    soup = bs(page)
    complete_list += descarga_página(soup)
    page_number += 1

import pandas as pd
complete_list_df = pd.DataFrame(complete_list)
# complete_list_df

complete_list_df.to_excel('lista_completa_Walmart.xls', index= False)
# from google.colab import files
# files.download('lista_completa_Walmart.xls')