import requests

url = 'http://localhost:5000/gestureDrive'
data = {'command': 'Scan'}

response = requests.post(url, json=data)

print(response.json())
