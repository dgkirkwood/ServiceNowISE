import requests
import json
import datetime

#david loo id: e118bc02-dc0f-4f8f-99f4-1dca897598d7
#employee group a1740510-8c01-11e6-996c-525400b48521
#showonly group 0b165030-38c3-11e8-b70b-00505698c3e2

url = "https://dev50338.service-now.com/api/now/table/change_request"

querystring = {"sysparm_query":"category=network^ORDERBYDESCnumber"}

headers = {
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }

employeeGroup = '0b165030-38c3-11e8-b70b-00505698c3e2'
viewOnlyGroup = '1740510-8c01-11e6-996c-525400b48521'

response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)

responseDict = json.loads(response.text)

first = responseDict['result'][0]

startDate = first['start_date']
startObj = datetime.datetime.strptime(startDate , '%Y-%m-%d %H:%M:%S')

endDate = first['end_date']
endObj = datetime.datetime.strptime(endDate , '%Y-%m-%d %H:%M:%S')

timeNow = datetime.datetime.now()

if timeNow < startObj:
	exit()

if timeNow > endObj:
	exit()


userLink = first['assigned_to']['link']
cmdbLink = first['cmdb_ci']['link']


response = requests.request("GET", userLink, headers=headers, params=querystring)

responseDict = json.loads(response.text)

name = responseDict['result']['name']

response = requests.request("GET", cmdbLink, headers=headers, params=querystring)

responseDict = json.loads(response.text)

asset = responseDict['result']





url = "https://se-cis-ise1.nsd5.ciscolabs.com:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7"

payloadDict = {
    "InternalUser": {
        "id": "e118bc02-dc0f-4f8f-99f4-1dca897598d7",
        "name": "davidloo",
        "enabled": True,
        "email": "davelo@cisco.com",
        "firstName": "David",
        "lastName": "Loo",
        "changePassword": False,
        "identityGroups": "a1740510-8c01-11e6-996c-525400b48521",
        "expiryDateEnabled": False,
        "customAttributes": {},
        "passwordIDStore": "Internal Users",
        "link": {
            "rel": "self",
            "href": "https://se-cis-ise1.nsd5.ciscolabs.com:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7",
            "type": "application/xml"
        }
    }
}

payloadJSON = json.dumps(payloadDict)

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    }

response = requests.request("PUT", url, data=payloadJSON, headers=headers)

print(response.text)



print(name)
print(asset)
print(startDate)
print(endDate)




"""
From here - look for recent request

Look at start time
Look at end time

Look at Assigned To - returns a link to do a further call
https://dev50338.service-now.com/api/now/table/sys_user/5137153cc611227c000bbd1bd8cd2007

Look at cmdb_ci - then look at Asset
"""