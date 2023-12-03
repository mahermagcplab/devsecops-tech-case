import os
import requests

# Get environment variables
OWM_CITY = os.environ.get('OWM_CITY')
OWM_API_KEY = os.environ.get('OWM_API_KEY')

# Define API URL
url = f'http://api.openweathermap.org/data/2.5/forecast?q={OWM_CITY}&appid={OWM_API_KEY}'

# Get data from API and format data
response = requests.get(url)
jsondata = response.json()

city = ("city="+'"'+jsondata["city"]["name"]+'"')
description = ("description="+'"'+jsondata["list"][0]["weather"][0]["description"]+'"')
temp = ("temp="+str(jsondata["list"][0]["main"]["temp"]))
humidity = ("humidity="+str(jsondata["list"][0]["main"]["humidity"]))

# Print data
print(city+',',description+',',temp+',',humidity)
