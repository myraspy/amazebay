import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def Amazon():
    amazon_url =(input(str('Input Amazon Product URL : ')))        
    r_amazon = requests.get(amazon_url, headers = headers)
    amazon_soup = bs(r_amazon.content,'lxml')
    Amazon.name = amazon_soup.find(id = 'productTitle').get_text().strip()
    raw_price = amazon_soup.find(id = 'priceblock_ourprice').get_text()
    Amazon.price = float(raw_price[1:])
    return (Amazon.price)
Amazon()

def Compare(): #Compare with Ebay Listings
    ebayUrl = (Amazon.name.replace(' ','+'))[0:50]
    print('Searching Ebay using search query :\n'+ ebayUrl)
    ebay_url = str('https://www.ebay.co.uk/sch/i.html?_osacat=0&_nkw=') + str(ebayUrl) + ('&_sacat=0')
    r_ebay = requests.get(ebay_url, headers= headers)
    ebay_soup = bs(r_ebay.content,'lxml')
    listings = ebay_soup.find_all('li', attrs={'class': 's-item'})
    for listing in listings:
        for name in listing.find_all('h3', attrs={'class':'s-item__title'}):
            if(str(name.find(text=True, recursive=False))!="None"):
                #prod_name=str(name.find(text=True, recursive=False))
                #print(prod_name)
                try:
                    price = listing.find('span', attrs={'class':'s-item__price'})
                    prod_price = str(price.find(text=True, recursive=False))
                    float_price = float(prod_price[1:])  
                except:
                     pass
                #df = pd.DataFrame((prod_name,float_price),index=[' ',' '], columns=[' '])
                #print(df)
                compare = format((float_price - Amazon.price),'.2f')
                print(compare)

print('-'*50)
print('AMAZON PRODUCT NAME:')
print (Amazon.name)
print ('AMAZON PRICE: £' + str(Amazon.price))
print('-'*50)
print('Comparing with Ebay Prices')
print('\nCalculating Profit per Flip')
print('-'*25)


Compare()
