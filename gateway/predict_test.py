import requests

server_url = 'http://localhost:9696/predict'
#server_url = 'http://localhost:9696/predict?show_probability=true'

data = {'url': 'https://www.martialtribes.com/wp-content/uploads/2017/07/karate-sparring.jpg'}

result = requests.post(server_url, json=data).json()

print(result)



### TEST IMAGES ###
#karate - https://www.martialtribes.com/wp-content/uploads/2017/07/karate-sparring.jpg

#image which is blocked - https://wallpapercave.com/wp/wp3088699.jpg
