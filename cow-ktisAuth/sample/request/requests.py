import requests

url = "https://1zi1pnd5vb.execute-api.ap-northeast-2.amazonaws.com/dev/auth"

payload = "{\n\t\"user_id\": \"user_id\",\n\t\"passwd\": \"password\"\n}"
headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)