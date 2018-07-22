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
viewOnlyGroup = 'eebca7a0-4c17-11e8-a046-6616e204bb54'

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

                
                try:

                    #Do a check to see if the end date has changed
                    ServNowUrl = "https://dev59027.service-now.com/api/now/table/change_request/" + entry['sys_id']
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

                        time.sleep(10)

                        url = "https://10.67.54.85:9060/ers/config/internaluser/3f2d3c27-c403-49e5-a73c-daaa340b5bb1"

                        payloadDict = {
                            "InternalUser": {
                                "id": "3f2d3c27-c403-49e5-a73c-daaa340b5bb1",
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
                            'Authorization': "Basic RVJTQWRtaW46QyFzY28xMjM=",
                            'Cache-Control': "no-cache",
                            }

                        response = requests.request("PUT", url, data=payloadJSON, headers=headers, verify=False)

                        deviceURL = 'https://10.67.54.85:9060/ers/config/networkdevice/eab08020-4c15-11e8-a046-6616e204bb54'
                        deviceChange = {
                            "NetworkDevice": {
                                "id": "eab08020-4c15-11e8-a046-6616e204bb54",
                                "name": "4948",
                                "modelName": "4948",
                                "softwareVersion": "Unknown",
                                "tacacsSettings": {
                                    "sharedSecret": "C1sco12345",
                                    "connectModeOptions": "OFF",
                                    "previousSharedSecret": "",
                                    "previousSharedSecretExpiry": 0
                                },
                                "NetworkDeviceIPList": [
                                    {
                                        "ipaddress": "10.66.106.44",
                                        "mask": 32
                                    }
                                ],
                                "NetworkDeviceGroupList": [
                                    "Location#All Locations",
                                    "IPSEC#Is IPSEC Device#No",
                                    "Device Type#All Device Types#AccessSwitches"
                                ]
                            }
                        }

                        deviceChangeJSON = json.dumps(deviceChange)

                        response = requests.request("PUT", deviceURL, data=deviceChangeJSON, headers=headers, verify=False)



                        activeChangesTable.update_one({"number":requestID}, {"$set":{"deleted":"True"}})
                        activeChangesTable.update_one({"number":requestID}, {"$set":{"number":requestID+"d"}})



                        payload = "{\n  \"roomId\" : \""+roomId+"\",\n  \"text\" : \"Hi "+name+". Change request "+requestID+" is now closed. Please update the case notes if required.\"\n}"

                        sparkCall.POSTMessage(payload)


                except requests.exceptions.SSLError:

                    print('connection error')
                    time.sleep(10)
                    continue

    time.sleep(10)



