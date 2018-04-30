#
#   Dan Kirkwood (dkirkwoo@cisco.com)
#       August 2017
#
#       A collection of generic API calls to Spark
#       
#
#
#   WARNING:
#       This script is meant for educational purposes only.
#       Any use of these scripts and tools is at
#       your own risk. There is no guarantee that
#       they have been through thorough testing in a
#       comparable environment and we are not
#       responsible for any damage or data loss
#       incurred with their use.
#     

import requests
import json



from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class SparkAPI(object):

	"""
	Requires a known bot ID and Room ID for retrieving and creating messages
	"""

	def __init__(self, botID):
		self.botID = botID

	def SparkGET(self, url, headers):
		"""
		Generic Spark GET
		"""
		
		try:
			response = requests.request("GET", url, headers=headers, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				return response.text
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def SparkPOST(self, url, headers, payload):
		"""
		Generic Spark POST
		"""
		
		try:
			response = requests.request("POST", url, headers=headers, data=payload, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				return response.text
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()

	def SparkJSONPOST(self, url, headers, payload):
		try:
			response = requests.request("POST", url, headers=headers, json=payload, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				return response.text
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()		


	def GETMessage(self, messageID):
		"""
		Get a message from its unique Spark Message ID
		"""
		
		url = 'https://api.ciscospark.com/v1/messages/'+messageID
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkGET(url, headers)

	def GETPerson(self, userID):
		"""
		Get details of a Spark user
		"""

		url = 'https://api.ciscospark.com/v1/people/'+userID
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkGET(url, headers)

	def POSTMessage(self, payload):
		"""
		Create a message in Spark
		"""

		url = 'https://api.ciscospark.com/v1/messages'
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkPOST(url, headers, payload)

	def POSTMarkdownMessage(self, payload):

		url = 'https://api.ciscospark.com/v1/messages'
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkJSONPOST(url, headers, payload)
