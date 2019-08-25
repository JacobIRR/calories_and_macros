from pprint import pprint
import  json
import requests

url = 'https://api.nal.usda.gov/ndb/search/?format=json&q={}&sort=n&max=50&offset=0&api_key=0lIAZDhVt4xweOX3fbjBwUJCd6zZedU2Gh9wEDaX'

response = requests.get(url.format('eggs'))

pprint(response.text)
# ... might as well use the web for this
