import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import random
import json
import pandas as pd

prodTable = []

for department in range(268, 274):
    pageNumber = 1
    while True:
        url = f'https://www.masonline.com.ar/{department}?map=productClusterIds&page={pageNumber}'
        soup = bs(requests.get(url).text)
        prod = soup.find('template', attrs={'data-type': 'json', 'data-varname': '__STATE__'}).find('script').text
        pageNumber += 1
        if not ('productId' in prod):
            break
        prod = json.loads(prod)

        nextProd = ' '
        for each in prod:
            if not ((nextProd in each) or ('Image' in each) or ('ROOT' in each)):
                nextProd = each
                singleProd = {'productId': prod[each]['productId'], 'productReference': prod[each]['productReference'],
                              'productName': prod[each]['productName'], 'description': prod[each]['description'],
                              'brand': prod[each]['brand'], 'link': prod[each]['link'],
                              'highPrice': prod[(prod[each]['priceRange']['id'] + '.sellingPrice')]['highPrice'],
                              'lowPrice': prod[(prod[each]['priceRange']['id'] + '.sellingPrice')]['lowPrice']}
                prodTable.append(singleProd)
                print(singleProd)
        delay = random()
        print(str(pageNumber - 1) + '@' + str(department) + ' - Sleeping ' + str(delay) + ' seconds')
        sleep(delay)

prodTableDF = pd.DataFrame(prodTable)
