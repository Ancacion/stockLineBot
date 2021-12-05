import json
import model
import requests
import dialogflowClient
#import todayStock
from chatBotConfig import channel_secret, channel_access_token
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, TextSendMessage, MessageEvent, TextMessage
from umsConfig import umsWebApi


handler = WebhookHandler(channel_secret)
linebotApi = LineBotApi(channel_access_token)
dialogflowModel = model.DialogflowModel()
userModel = model.UserModel()
todayStockResponse = model.todayStockResponse()
todayStockModel = model.todayStockModel()


# (1) functions
def model_init_(lineId):
    global dialogflowModel, userModel, todayStockResponse
    dialogflowModel = model.DialogflowModel()
    userModel = model.UserModel()
    todayStockResponse = model.todayStockResponse()
    todayStockModel = model.todayStockModel()
    dialogflowModel.lineId = userModel.lineId = lineId


def actionDispatch():
    url = umsWebApi + dialogflowModel.actionName
    
    if (dialogflowModel.actionName in ['create', 'delete', 'update']):
        result = requests.post(url, json=userModel.__dict__)
        
    elif (dialogflowModel.actionName == 'retrieve'):
        result = requests.get(url + '?stockId=' + userModel.stockId)

    elif (dialogflowModel.actionName == 'todayStock'):
        result = requests.post(url, json=todayStockModel.__dict__)
        
    return result


def replyMessageToUser(replyToken, texts):
    replyMessages = []
    for text in texts:
        replyMessages.append(TextSendMessage(text=text))
    linebotApi.reply_message(replyToken, replyMessages)


# (2) Webhook
def lineWebhook(request):
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '200 OK'


# (3) Follow Event
@handler.add(FollowEvent)
def handle_follow(event):
    model_init_(event.source.user_id)
    dialogflowModel.lineId = event.source.user_id
    dialogflowModel.eventName = 'welcomeEvent'
    dialogflowClient.eventDispatch(dialogflowModel)
    replyMessageToUser(event.reply_token, dialogflowModel.responses)


# (4) Message Event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    model_init_(event.source.user_id)
    dialogflowModel.queryInput = event.message.text
    dialogflowClient.queryDispatch(dialogflowModel)
    output = []

    if (dialogflowModel.actionName == 'todayStock'):

        result = actionDispatch()

        if (json.loads(result.text)['result']['code'] == '1'):
            dialogflowModel.parameters = json.loads(result.text)['todayStockModel']
            dialogflowModel.eventName = dialogflowModel.actionName + '_responseEvent'

        dialogflowClient.eventDispatch(dialogflowModel)  

    #    output = todayStock.stock()                    #網路爬蟲程式
    #    dialogflowClient.todayStockEventDispatch(dialogflowModel, output)  #同時將Model與爬蟲結果扔進dialogflowClient
        #for i in output:                              #原先想透過linebotApi直接將結果印出，結果並沒有，仍只有dialogflow設定的回答
            #linebotApi.reply_message(event.replyToken, i)
    
    elif (dialogflowModel.actionName):
        
        if (dialogflowModel.actionName == 'update'):
            dialogflowModel.actionName = 'retrieve'
            userModel.stockId = dialogflowModel.parameters['stockId']
            result = actionDispatch()
            originalUserData = json.loads(result.text)['userModel']
            newUserData = json.loads(result.text)['userModel']
            
            for key in dialogflowModel.parameters:
                newUserData[key] = dialogflowModel.parameters[key]
                
            dialogflowModel.parameters = newUserData
            dialogflowModel.actionName = 'update'
        
        for key in dialogflowModel.parameters:
            setattr(userModel, key, dialogflowModel.parameters[key])
            
        result = actionDispatch()
        
        if (json.loads(result.text)['result']['code'] == '1'):
            dialogflowModel.parameters = json.loads(result.text)['userModel']
            dialogflowModel.eventName = dialogflowModel.actionName + '_responseEvent'  
            
        else:
            dialogflowModel.eventName = dialogflowModel.actionName + '_failResponseEvent'
            
        if (dialogflowModel.actionName == 'update'):
            dialogflowModel.parameters = originalUserData

        #if (dialogflowModel.actionName == 'todayStock'):
        #    output = todayStock.stock()
        #    for i in output:
        #        dialogflowModel.responses.append(i)

        dialogflowClient.eventDispatch(dialogflowModel)
    
    #if (dialogflowModel.eventName == 'todayStockEvent'):
        #dialogflowClient.eventDispatch(dialogflowModel)
    #    output = todayStock.stock()
    #    for i in output:
    #        linebotApi.reply_message(event.replyToken, i)
            #dialogflowModel.responses.append(i)
        #dialogflowClient.eventDispatch(dialogflowModel)
        #linebotApi.reply_message(event.replyToken,)

    replyMessageToUser(event.reply_token, dialogflowModel.responses)