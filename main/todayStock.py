from bs4 import BeautifulSoup
from lxml import etree
import requests

def stock():
    res = requests.get('https://www.cnyes.com/twstock/')
    soup = BeautifulSoup(res.text, "lxml")
    '''Weighted_index = soup.find("td").find_next_sibling("td").text
    print(Weighted_index)'''
    Weighted_index = soup.find(id = 'twftr_0')
    k = 0
    outputString = ""
    outputDialog = []
    for i in Weighted_index.find_all("td"):#find_all("td")
        k = k + 1
        if k == 1:
            outputString = "加權指數 : "
        elif k == 2:
            outputString = "目前漲跌 : "
        elif k == 3:
            outputString = "漲跌%數  : "
        elif k == 4:
            outputString = "更新時間 : "

        #print(outputString + i.find_next_sibling("td").text)
        outputDialog.append(outputString + i.find_next_sibling("td").text)
        if k == 4:
            break
    #test = soup.find_all("td", class_ = "rt", limit=7)
    #print(test)
    #for i in outputDialog:
    #    print(i)
    return outputDialog