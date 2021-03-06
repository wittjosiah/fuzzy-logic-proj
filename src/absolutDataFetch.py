import requests
import os
import json
from string import Template

def fetch(forceFetch = False):
    directory = '../datasets/'
    fileName = directory + 'data.json'
    drinks = []
    if not forceFetch and os.path.isfile(fileName):
        with open(fileName) as fp:
            drinks = json.load(fp)
    else:
        apiKey = os.environ['ABSOLUT_API_KEY']
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
                drinks.append({
                    'id': d['id'],
                    'ingredients': [i['id'] for i in d['ingredients']],
                    'tastes': [t['id'] for t in d['tastes']],
                    'tools': [t['id'] for t in d['tools']]
                })
            if 'next' in response.keys():
                next = response['next']
            else:
                next = ''

        print(len(drinks), ' drinks from the Absolut API')

        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(fileName, 'w') as fp:
            # json.dump(drinks, fp, sort_keys=True, indent=2)
            json.dump(drinks, fp, sort_keys=True)

        print("Saved drinks data")

    return drinks
