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

def delete(request):
    
    request_json = request.get_json()
    id = str(request_json['stockId'])
    
    userResponse.userModel = {}
    
    user = users_ref.document(id).get().to_dict()
    
    if(user != None):
        users_ref.document(id).delete()
        userResponse.result ={
                "code":"1",
                "title":"退出追蹤成功",
            }
    else:
        userResponse.result ={
                "code":"-1",
                "title":"無此追蹤，請確認後再試",
            }
    return userResponse.__dict__
