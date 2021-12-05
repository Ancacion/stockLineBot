import os
from firebase_admin import credentials, firestore, initialize_app
import requests
import json
from model import UserModel,UserResponse

userModel = UserModel()
userResponse = UserResponse()

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
users_ref = db.collection('stocks')


def retrieve(request):
    
    request_args = request.args
    if(request.args and 'stockId' in request.args):
        id = request.args.get('stockId')
        user = users_ref.document(id).get().to_dict()
        if(user != None):
            userResponse.userModel = user
            userResponse.result ={
                    "code":"1",
                    "title":"查詢完成",
                }
        else:
            userResponse.userModel = {}
            userResponse.result ={
                    "code":"-1",
                    "title":"無相關資料",
                    "description":"本檔股票("+str(id)+")尚未列入追蹤"
                }
    else:
        userResponse.userModel = [doc.to_dict() for doc in users_ref.stream()]
        userResponse.result ={
                    "code":"1",
                    "title":"追蹤股票列表",
                }
    return userResponse.__dict__
