import requests
import json
import datetime
import pymongo
from pymongo import MongoClient
import time
from SPARKAPI import SparkAPI


#david loo id: e118bc02-dc0f-4f8f-99f4-1dca897598d7
#employee group a1740510-8c01-11e6-996c-525400b48521
#showonly group 0b165030-38c3-11e8-b70b-00505698c3e2
#within change group c735f800-46e8-11e8-b70b-00505698c3e2
#Admin group 71c5ce00-07a0-11e7-86dd-024207e6c1ff

botToken = 'MzVlYjI2Y2UtZTg3NS00YWEwLWE3MjgtY2JlYWE1NjJlNWZkMWRkZGVkOTMtMDgx'
botId = 'Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2E2ZjcwNjJjLTA0NmQtNDUwZS1hMjRhLWExMWViOTY5ZTdhZA'
roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vNzVkN2FiZTAtNGFkOC0xMWU4LWFiYTMtNDc4YzY1MGUyYjVl'

sparkCall = SparkAPI(botToken)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

changeGroup = 'c735f800-46e8-11e8-b70b-00505698c3e2'
viewOnlyGroup = '0b165030-38c3-11e8-b70b-00505698c3e2'

mongoAddr = 'database:27017'
client = MongoClient(mongoAddr)

activeChangesDB = client.activeChangesDB
activeChangesTable = activeChangesDB.activeChangesTable


#Put David into Show Only group to start




url = "https://10.66.113.102:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7"

payloadDict = {
    "InternalUser": {
        "id": "e118bc02-dc0f-4f8f-99f4-1dca897598d7",
        "name": "davidloo",
        "identityGroups": "0b165030-38c3-11e8-b70b-00505698c3e2"
    }
}


payloadJSON = json.dumps(payloadDict)

ISEHeaders = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }

response = requests.request("PUT", url, data=payloadJSON, headers=ISEHeaders, verify=False)
print(response)


headers = {
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }

while True:

    for entry in activeChangesTable.find():

        if 'updated' not in entry:

            userLink = entry['assigned_to']['link']
            cmdbLink = entry['cmdb_ci']['link']
            requestID = entry['number']


            response = requests.request("GET", userLink, headers=headers)

            responseDict = json.loads(response.text)

            name = responseDict['result']['name']

            response = requests.request("GET", cmdbLink, headers=headers)

            responseDict = json.loads(response.text)

            asset = responseDict['result']['name']

            url = "https://10.66.113.102:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7"

            payloadDict = {
                "InternalUser": {
                    "id": "e118bc02-dc0f-4f8f-99f4-1dca897598d7",
                    "name": "davidloo",
                    "enabled": True,
                    "identityGroups": changeGroup,
                }
            }
            

            payloadJSON = json.dumps(payloadDict)

            headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
                'Cache-Control': "no-cache",
                }

            response = requests.request("PUT", url, data=payloadJSON, headers=headers, verify=False)

            print (response)

            payload = "{\n  \"roomId\" : \""+roomId+"\",\n  \"text\" : \"Attention "+name+"! You are assigned to active change request "+requestID+". Please log in to "+asset+" to complete this request.\"\n}"

            sparkCall.POSTMessage(payload)


            activeChangesTable.update_one({"number":requestID}, {"$set":{"updated":"True"}})
            activeChangesTable.update_one({"number":requestID}, {"$set":{"name":name}})

    time.sleep(10)
