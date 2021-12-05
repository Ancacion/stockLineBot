class UserModel():
    def __init__(self, name=None, stockId=None, lineId="1", role="favorite", price=0, buyPrice=0, spread=0):
        self.name = name
        self.stockId = stockId
        self.lineId = lineId
        self.role = role
        self.price = price
        self.buyPrice = buyPrice
        self.spread = spread
        

class UserResponse():
    def __init__(self, userModel=None, result=None):
        self.userModel = userModel
        self.result = result