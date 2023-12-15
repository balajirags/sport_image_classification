import requests

url = 'http://localhost:9696/predict'
#url = 'http://a4e21e7898c7b48daace6ac39c2e813c-912773252.us-east-2.elb.amazonaws.com:9696/predict'
data = {'url': 'https://www.athletico.com/blog2/wp-content/uploads/2012/07/Istock-swimmer-032410.jpg'}

result = requests.post(url, json=data).json()

print(result)