import json
import requests
import urllib3.response

def create_mock_response(code, content):
	content = json.dumps(content).encode('utf-8')

	response = requests.Response()
	response._content    = content
	response.raw         = urllib3.response.HTTPResponse(
		body   = content,
		status = code,
	)
	response.status_code = code

	return response

