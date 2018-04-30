import requests

url = "https://10.66.113.102:9060/ers/config/internaluser/e118bc02-dc0f-4f8f-99f4-1dca897598d7"

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Basic YWRtaW46QyFzY28xMjM=",
    'Cache-Control': "no-cache",
    'Postman-Token': "3efe7d99-029d-4463-8e89-bfd53765635d"
    }

response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)