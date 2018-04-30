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

botToken = 'MzVlYjI2Y2UtZTg3NS00YWEwLWE3MjgtY2JlYWE1NjJlNWZkMWRkZGVkOTMtMDgx'
botId = 'Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2E2ZjcwNjJjLTA0NmQtNDUwZS1hMjRhLWExMWViOTY5ZTdhZA'
roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vNzVkN2FiZTAtNGFkOC0xMWU4LWFiYTMtNDc4YzY1MGUyYjVl'

sparkCall = SparkAPI(botToken)

employeeGroup = 'a1740510-8c01-11e6-996c-525400b48521'
viewOnlyGroup = '0b165030-38c3-11e8-b70b-00505698c3e2'

mongoAddr = 'database:27017'
client = MongoClient(mongoAddr)

activeChangesDB = client.activeChangesDB
activeChangesTable = activeChangesDB.activeChangesTable


headers = {
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }



while True:

    for entry in activeChangesTable.find():

        if 'updated' in entry:

            if 'deleted' not in entry:

                #Do a check to see if the end date has changed
                ServNowUrl = "https://dev50338.service-now.com/api/now/table/change_request/" + entry['sys_id']
                ServNowHeaders = {'Authorization': "Basic YWRtaW46QyFzY28xMjM=", 'Cache-Control': "no-cache",}

                entryCheck = requests.request("GET", ServNowUrl, headers=ServNowHeaders)

                entryDict = json.loads(entryCheck.text)


                startDate = entryDict['result']['start_date']
                startObj = datetime.datetime.strptime(startDate , '%Y-%m-%d %H:%M:%S')

                endDate = entryDict['result']['end_date']
                endObj = datetime.datetime.strptime(endDate , '%Y-%m-%d %H:%M:%S')

                timeNow = datetime.datetime.utcnow()

                if timeNow > endObj:

                    requestID = entry['number']
                    name = entry['name']

                    payload = "{\n  \"roomId\" : \""+roomId+"\",\n  \"text\" : \"Hi "+name+". Please note the change window for change request "+requestID+" is about to close. Please ensure you have completed the assigned task.\"\n}"

                    sparkCall.POSTMessage(payload)


                    url = "https://10.66.113.102:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7"

                    payloadDict = {
                        "InternalUser": {
                            "id": "e118bc02-dc0f-4f8f-99f4-1dca897598d7",
                            "name": 'davidloo',
                            "enabled": True,
                            "identityGroups": viewOnlyGroup,
                            "expiryDateEnabled": False,
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



                    activeChangesTable.update_one({"number":requestID}, {"$set":{"deleted":"True"}})
                    activeChangesTable.update_one({"number":requestID}, {"$set":{"number":requestID+"d"}})


    time.sleep(10)



