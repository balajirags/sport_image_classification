import requests

url = 'http://localhost:9696/predict'

data = {'url': 'https://wallpaperheart.com/wp-content/uploads/2018/03/Cricket-wallpapers.jpg'}

result = requests.post(url, json=data).json()

print(result)