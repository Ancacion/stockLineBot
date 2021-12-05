import os
import requests
import json
from model import todayStockResponse
#from model import todayStockModel,todayStockResponse
from bs4 import BeautifulSoup
from lxml import etree

#todayStockModel = todayStockModel()
todayStockResponse = todayStockResponse()

def todayStock(request):
    request_args = request.args
    res = requests.get('https://www.cnyes.com/twstock/')
    soup = BeautifulSoup(res.text, "lxml")
    Weighted_index = soup.find(id = 'twftr_0')

    k = 0
    outputString = ""
    outputDialog = []

    for i in Weighted_index.find_all("td"):
        k = k + 1
        if k == 1:
            outputString = "加權指數 : "
        elif k == 2:
            outputString = "目前漲跌 : "
        elif k == 3:
            outputString = "漲跌%數  : "
        elif k == 4:
            outputString = "更新時間 : "

        outputDialog.append(i.find_next_sibling("td").text)
        if k == 4:
            break

    #todayStockResponse.todayStockModel.addStock(outputDialog[0])
    #todayStockResponse.todayStockModel.addUpAndDown(outputDialog[1])
    #todayStockResponse.todayStockModel.addPercentageOfUD(outputDialog[2])
    #todayStockResponse.todayStockModel.addUpdateTime(outputDialog[3])
    #todayStockResponse.todayStockModel(outputDialog[0], outputDialog[1], outputDialog[2], outputDialog[3])
    todayStockResponse.todayStockModel ={
                    "stock":outputDialog[0],
                    "upAndDown":outputDialog[1],
                    "percentageOfUD":outputDialog[2],
                    "updateTime":outputDialog[3],
                }

    todayStockResponse.result ={
                    "code":"1",
                    "title":"今日大盤",
                }
                
    return todayStockResponse.__dict__
