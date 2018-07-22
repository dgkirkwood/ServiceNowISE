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

changeGroup = 'f879a2c0-4c17-11e8-a046-6616e204bb54'
viewOnlyGroup = 'eebca7a0-4c17-11e8-a046-6616e204bb54'

mongoAddr = 'database:27017'
client = MongoClient(mongoAddr)

activeChangesDB = client.activeChangesDB
activeChangesTable = activeChangesDB.activeChangesTable


#Put David into Show Only group to start




url = "https://10.67.54.85:9060/ers/config/internaluser/3f2d3c27-c403-49e5-a73c-daaa340b5bb1"

payloadDict = {
    "InternalUser": {
        "id": "3f2d3c27-c403-49e5-a73c-daaa340b5bb1",
        "name": "davidloo",
        "identityGroups": viewOnlyGroup
    }
}


payloadJSON = json.dumps(payloadDict)

ISEHeaders = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Basic RVJTQWRtaW46QyFzY28xMjM=",
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

            url = "https://10.67.54.85:9060/ers/config/internaluser/3f2d3c27-c403-49e5-a73c-daaa340b5bb1"

            payloadDict = {
                "InternalUser": {
                    "id": "3f2d3c27-c403-49e5-a73c-daaa340b5bb1",
                    "name": "davidloo",
                    "enabled": True,
                    "identityGroups": changeGroup,
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

            print (response)

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
                        "Device Type#All Device Types#AccessSwitches#WithinChangeWindow"
                    ]
                }
            }

            deviceChangeJSON = json.dumps(deviceChange)

            response = requests.request("PUT", deviceURL, data=deviceChangeJSON, headers=headers, verify=False)



            payload = "{\n  \"roomId\" : \""+roomId+"\",\n  \"text\" : \"Attention "+name+"! You are assigned to active change request "+requestID+". Please log in to "+asset+" to complete this request.\"\n}"

            sparkCall.POSTMessage(payload)


            activeChangesTable.update_one({"number":requestID}, {"$set":{"updated":"True"}})
            activeChangesTable.update_one({"number":requestID}, {"$set":{"name":name}})

    time.sleep(10)
