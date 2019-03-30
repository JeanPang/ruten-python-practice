import requests
from bs4 import BeautifulSoup
from builtins import str
import json
import re
url = 'https://class.ruten.com.tw/user/index00.php?s=hambergurs'

def Runten_Spider(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    resp = requests.get(url,headers = headers) 
    resp.encoding = 'utf-8'

    soup = BeautifulSoup(resp.text)
    
    itemTitle = getItemTitle(soup)
    itemImg = getItemImg(soup)  
        
    item_title = soup.find_all('h3', 'item-name')
     
    itemCost = []
    for index, item in enumerate(item_title[:30]):
        url = item.find('a').get('href')
        itemCost.append(getCost(url))

#     print (itemTitle)
#     print (itemImg)
#     print (itemCost)

    item = list(zip(itemTitle, itemImg, itemCost))

    dictionaryArray = []
    for index in range(len(item)):
        keys = ['標題', '圖片', '運費']
        dictionary = dict(zip(keys, item[index]))
        dictionaryArray.append(dictionary)
    return (dictionaryArray)
        
    
def getItemTitle(soup):
    item_title = soup.find_all('h3', 'item-name')
    item_title_list = []
    
    for index, item in enumerate(item_title[:30]):
        title = item.text.strip()
        item_title_list.append(title)
        
    return (item_title_list)
    
    
def getItemImg(soup):
    item_img = soup.find_all('div', 'rt-store-goods-disp-mix')
    item_img_list = []
    
    for index, item in enumerate(item_img[:30]):
        img = item.find('div', 'item-img').find('a').find('img')['src']
        item_img_list.append(img)
    
    return (item_img_list)
        
    
def getCost(itemUrl):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    resp = requests.get(itemUrl,headers = headers) 
    resp.encoding = 'utf-8'
    
    soup = BeautifulSoup(resp.text)
    js = soup.find_all('script', type='text/javascript')[15].text
    
    pattern = re.compile('RT.context = (.*?);')
    script = soup.find(text=pattern)
    isProductPage = pattern.search(script).group(1)
    
    jsonProduct = json.loads(isProductPage)
    cost = jsonProduct['item']['shipment']

    costArray = []
    costArray.append(cost)
    
    return (costArray)

# Runten_Spider(url)


def multiplePage(url):
    data = []

    for i in range(1,4):
        finalURL = url + '&p='+str(i)
#         print('loading page' + str(i))
        threePagesItem = Runten_Spider(finalURL)
        data.append(threePagesItem)
    return (data)

multiplePage(url)

# testing
# multiplePage(url)[0][0]['運費']
