class DialogflowModel():
    def __init__(self):
        self.eventName = None
        self.actionName = None
        self.queryInput = None
        self.parameters = {}
        self.responses = []
        self.lineId: None

class UserModel():
    def __init__(self):
        self.name = None
        self.stockId = None
        self.lineId = None
        self.role = "favorite"
        self.price = 0
        self.buyPrice = None
        self.spread = 0

class todayStockResponse():
    def __init__(self, todayStockModel=None, result=None):
        self.todayStockModel = todayStockModel
        self.result = result

class todayStockModel():
    def __init__(self):
        self.stock = None
        self.upAndDown = None
        self.percentageOfUD = None
        self.updateTime = None