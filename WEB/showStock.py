import os
import requests
import json
#from model import todayStockModel,todayStockResponse,AdvancedJSONEncoder
from model import todayStockResponse
from bs4 import BeautifulSoup
from lxml import etree
import datetime

def showStockPrice(stock_id):
    url = 'https://tw.stock.yahoo.com/q/q?s='+stock_id
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all(text='成交')[0].parent.parent.parent
    price = table.select('tr')[1].select('td')[2].text
    return price
