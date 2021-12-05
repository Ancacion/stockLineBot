class todayStockModel():
    def __init__(self, stock=None, upAndDown=None, percentageOfUD=None, updateTime=None):
        self.stock = stock
        self.upAndDown = upAndDown
        self.percentageOfUD = percentageOfUD
        self.updateTime = updateTime

    #def addStock(self ,stock):
    #    self.stock = stock

    #def addUpAndDown(self ,upAndDown):
    #    self.upAndDown = upAndDown

    #def addPercentageOfUD(self, percentageOfUD):
    #    self.percentageOfUD = percentageOfUD

    #def addUpdateTime(self, updateTime):
    #    self.updateTime = updateTime

class todayStockResponse():
    def __init__(self, todayStockModel=None, result=None):
        self.todayStockModel = todayStockModel
        self.result = result