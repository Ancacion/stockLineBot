import os
from flask import Flask, request, render_template
import requests
import json
from model import UserModel, todayStockModel
import umsConfig
import showStock

app = Flask(__name__)

userModel = UserModel()
todayStockModel = todayStockModel()

@app.route("/ums/index", methods=['GET'])
def index():
    global userModel
    try:
        userModel.lineId = request.values['lineId']
    except:
        pass
    return render_template("index.html", userModel=userModel)


@app.route("/ums/create", methods=['GET', 'POST'])
def create():
    global userModel
    if request.method == "GET":

        return render_template("createUserRequest.html", userModel=userModel)
    if request.method == 'POST':

        userModel = UserModel(request.values['name'], request.values['stockId'], userModel.lineId,  userModel.role, userModel.price, request.values['buyPrice'], userModel.spread)

        apiResponse = requests.post(
            umsConfig.createApi, json=userModel.__dict__)

        userResponse = apiResponse.json()

        if userResponse['result']['code'] == "1":
            return render_template("createUserResponse.html", userModel=userResponse)
        else:
            return render_template("createUserFail.html", result=userResponse)


'''@app.route('/ums/update', methods=['GET', 'POST'])
def update():
    global userModel
    if request.method == "GET":
        return render_template("queryUserRequest.html")
    if request.method == "POST":
        try:
            userModel = UserModel(request.values['name'], request.values['phone'],
                              request.values['email'], userModel.role, userModel.lineId)
            apiResponse = requests.put(umsConfig.updateApi, json=userModel.__dict__)
            userResponse = apiResponse.json()
            if userResponse['userModel']!={}:
                return render_template('updateUserResponse.html', userModel=userResponse)
        except:
            apiResponse = requests.get(umsConfig.queryApi+'?phone='+request.values['phone'])
            userResponse = apiResponse.json()
            if userResponse['userModel']!={}:
                return render_template('updateUserRequest.html', userModel=userResponse)
            else:
                return render_template('queryUserFail.html', userModel=userResponse)'''

@app.route('/ums/query', methods=['GET', 'POST'])
def query():
    #global userModel
    if request.method == "GET":
        return render_template("queryUserRequest.html")
    if request.method == "POST":
        apiResponse = requests.get(umsConfig.queryApi+'?stockId='+request.values['stockId'])
        nowPrice = showStock.showStockPrice(request.values['stockId'])

        userResponse = apiResponse.json()

        if userResponse['userModel']!={}:
            nowSpread = float(nowPrice) - float(userResponse['userModel']['buyPrice'])
            return render_template('queryUserResponse.html', userModel=userResponse, stockPrice=nowPrice, spread = nowSpread)
        else:
            return render_template('queryUserFail.html', userModel=userResponse)

@app.route('/ums/list', methods=['GET', 'POST'])
def list():
    apiResponse = requests.get(umsConfig.listApi)

    userResponse = apiResponse.json()
    usersLength = len(userResponse['userModel'])

    return render_template('listUserResponse.html', userModel=userResponse, length=usersLength)


@app.route('/ums/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "GET":
        return render_template("deleteUserRequest.html")
    if request.method == 'POST':
        userModel = UserModel(stockId=request.values['stockId'])
        #userModel = UserModel(request.values['name'], request.values['stockId'], userModel.role, userModel.lineId)

        userResponse = requests.delete(
            umsConfig.deleteApi, json=userModel.__dict__)

        userResponse = userResponse.json()

        if userResponse['result']['code'] == "1":
            return render_template("deleteUserResponse.html", userModel=userResponse)
        else:
            return render_template("deleteUserFail.html", result=userResponse)

@app.route('/ums/todayStock', methods=['GET', 'POST'])
def todayStock():
    apiResponse = requests.get(umsConfig.todayStockApi)
    
    todayStockResponse = apiResponse.json()
    return render_template('todayStockUserResponse.html', todayStockModel=todayStockResponse)

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='127.0.0.1', port=port)
