import os
import json
import dialogflow_v2 as dialogflow
from dialogflowClientConfig import project_id
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToJson
import showStock


os.environ ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"
language_code = 'zh-HK'


session_client = dialogflow.SessionsClient()


def getDialogflowJsonResponse(session, query_input):
    dialogflowResponse = session_client.detect_intent(session=session, query_input=query_input)
    jsonObj = MessageToJson(dialogflowResponse.query_result)
    response = json.loads(jsonObj)
    return response                    #我該如何將爬蟲結果輸進response?


def getfulfillmentMessages(dialogflowModel, response):
    if ('fulfillmentText' in response):
        fulfillmentMessages = response['fulfillmentMessages']
        for fulfillmentMessage in fulfillmentMessages:
            dialogflowModel.responses.append(fulfillmentMessage['text']['text'][0])


def getResponsesByEvent(dialogflowModel):
    dialogflowParameters = Struct()
    dialogflowParameters['lineId'] = dialogflowModel.lineId   
    nowPrice = "0" 

    if (dialogflowModel.eventName == 'retrieve_responseEvent'):

        nowPrice = showStock.showStockPrice(dialogflowModel.parameters['stockId'])

        dialogflowParameters['name'] = dialogflowModel.parameters['name']
        dialogflowParameters['stockId'] = dialogflowModel.parameters['stockId']
        dialogflowParameters['price'] = dialogflowModel.parameters['price'] + float(nowPrice)
        dialogflowParameters['buyPrice'] = dialogflowModel.parameters['buyPrice']
        dialogflowParameters['spread'] = float(nowPrice) - dialogflowModel.parameters['buyPrice']
        #dialogflowParameters['lineId'] = dialogflowModel.parameters['lineId']

    session = session_client.session_path(project_id, dialogflowModel.lineId)
    event_input = dialogflow.types.EventInput(name=dialogflowModel.eventName, parameters=dialogflowParameters, language_code=language_code)
    query_input = dialogflow.types.QueryInput(event=event_input)
    response = getDialogflowJsonResponse(session, query_input)
    print(response['intent']['displayName'])
    getfulfillmentMessages(dialogflowModel, response)


def eventDispatch(dialogflowModel):
    session = session_client.session_path(project_id, dialogflowModel.lineId)
    getResponsesByEvent(dialogflowModel)
    if (dialogflowModel.eventName == 'welcomeEvent'):
        dialogflowModel.eventName = 'menuEvent'
        getResponsesByEvent(dialogflowModel)
    #if (dialogflowModel.eventName == 'todayStockEvent'):
    #    printStockInfro(dialogflowModel)
   
   
def queryDispatch(dialogflowModel):
    session = session_client.session_path(project_id, dialogflowModel.lineId)
    text_input = dialogflow.types.TextInput(text=dialogflowModel.queryInput, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = getDialogflowJsonResponse(session, query_input)
    getfulfillmentMessages(dialogflowModel, response)
    
    if (set(['action','allRequiredParamsPresent']).issubset(response)):
        dialogflowModel.actionName = response['action']
        dialogflowModel.parameters = response['parameters']
        
    elif (set(['isFallback']).issubset(response['intent'])):
        dialogflowModel.eventName = 'menuEvent'
        eventDispatch(dialogflowModel)

#def todayStockEventDispatch(dialogflowModel, output):
 #   dialogflowParameters = Struct()
#    dialogflowParameters['lineId'] = dialogflowModel.lineId       
#    session = session_client.session_path(project_id, dialogflowModel.lineId)
#    event_input = dialogflow.types.EventInput(name=dialogflowModel.eventName, parameters=dialogflowParameters, language_code=language_code)
#    query_input = dialogflow.types.QueryInput(event=event_input)
#    response = getDialogflowJsonResponse(session, query_input)
#    getfulfillmentMessages(dialogflowModel, response)