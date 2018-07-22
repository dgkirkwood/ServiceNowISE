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

mongoAddr = 'database:27017'
client = MongoClient(mongoAddr)

activeChangesDB = client.activeChangesDB
activeChangesTable = activeChangesDB.activeChangesTable

#Create index to prevent duplicate entries in active table
activeChangesTable.create_index([('number', pymongo.ASCENDING)], unique=True)

sparkCall = SparkAPI(botToken)


url = "https://dev59027.service-now.com/api/now/table/change_request"

querystring = {"sysparm_query":"category=network^ORDERBYDESCnumber"}

headers = {
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }


while True:

    
    try:

        response = requests.request("GET", url, headers=headers, params=querystring)

        #print(response.text)

        responseDict = json.loads(response.text)

        first = responseDict['result'][0]

        for entry in responseDict['result']:

            #print('this entry is ' + entry['number'])

            startDate = entry['start_date']
            startObj = datetime.datetime.strptime(startDate , '%Y-%m-%d %H:%M:%S')
            #print ('start time is ' + startObj.strftime('%Y/%m/%d %X'))

            endDate = entry['end_date']
            endObj = datetime.datetime.strptime(endDate , '%Y-%m-%d %H:%M:%S')
            #print ('end time is ' + endObj.strftime('%Y/%m/%d %X'))

            timeNow = datetime.datetime.utcnow()
            #print ('current time is ' + timeNow.strftime('%Y/%m/%d %X'))

            if timeNow > startObj and timeNow < endObj:
                try:
                    activeChangesTable.insert_one(entry)
                except pymongo.errors.DuplicateKeyError:
                    print('Entry already in the table')
                    break

                payload = "{\n  \"roomId\" : \""+roomId+"\",\n  \"text\" : \"Change window has opened for request "+entry['number']+". Assigning user rights...\"\n}"

                sparkCall.POSTMessage(payload)


        time.sleep(20)

    except requests.exceptions.SSLError:

        print('connection error')
        time.sleep(10)
        continue



#userLink = first['assigned_to']['link']
#cmdbLink = first['cmdb_ci']['link']


