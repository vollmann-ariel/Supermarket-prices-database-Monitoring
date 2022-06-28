import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import random
import json
import pandas as pd
import function.py

prodTable = []

for department in range(268, 274):
    pageNumber = 50
    while True:
        url = f'https://www.masonline.com.ar/{department}?map=productClusterIds&page={pageNumber}'
        soup = bs(requests.get(url).text)
        productsData = soup.find('template', attrs={'data-type': 'json', 'data-varname': '__STATE__'}).find('script').text
        pageNumber += 1
        if not ('productId' in productsData):
            break
        productsJsonData = json.loads(productsData)

        nextProd = ' '
        for each in productsData:
            if not ((nextProd in each) or ('Image' in each) or ('ROOT' in each)):
                nextProd = each
                singleProd = {'productId': productsJsonData[each]['productId'], 'productReference': productsJsonData[each]['productReference'],
                              'productName': productsJsonData[each]['productName'], 'description': productsJsonData[each]['description'],
                              'brand': productsJsonData[each]['brand'], 'link': productsJsonData[each]['link'],
                              'highPrice': productsJsonData[(productsJsonData[each]['priceRange']['id'] + '.sellingPrice')]['highPrice'],
                              'lowPrice': productsJsonData[(productsJsonData[each]['priceRange']['id'] + '.sellingPrice')]['lowPrice']}
                prodTable.append(singleProd)
                print(singleProd)
        delay = random()
        print(str(pageNumber - 1) + '@' + str(department) + ' - Sleeping ' + str(delay) + ' seconds')
        sleep(delay)

prodTableDF = pd.DataFrame(prodTable)

prodTableDF.to_excel('excel file.xls', index=False)
'''
from google.colab import files
files.download('excel file.xls')
'''