import requests
import os
import json
from string import Template

apiKey = os.environ['ABSOLUT_API_KEY']
drinks = {}
start = 0
pageSize = 100
url = Template('http://addb.absolutdrinks.com/drinks/' +
    '?apiKey=$apiKey&start=$start&pageSize=$pageSize')
next = url.substitute(
    apiKey = apiKey,
    start = str(start),
    pageSize = str(pageSize))
print('Fetching', end = '', flush = True)
while next != '':
    print('.', end = '', flush = True)
    r = requests.get(next)
    response = r.json()
    for d in response['result']:
        drinks[d['id']] = d
    if 'next' in response.keys():
        next = response['next']
    else:
        next = ''

print(len(drinks.keys()), ' drinks from the Absolut API')

with open('data.json', 'w') as fp:
    json.dump(drinks, fp, sort_keys=True, indent=4)

print("Saved drinks to data.json")

