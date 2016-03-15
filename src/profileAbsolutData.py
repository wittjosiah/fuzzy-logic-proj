import os
import json
from absolutDataFetch import fetch

def profile(forceFetch = False):
    drinks = fetch(forceFetch)

    drinkIngredientCount = {}
    drinkTasteCount = {}
    ingredients = {}
    tastes = {}

    print('Profiling', len(drinks.keys()), 'drinks')
    for d in drinks:
        iCount = len(drinks[d]['ingredients']) 
        if iCount in drinkIngredientCount.keys():
            drinkIngredientCount[iCount] += 1
        else:
            drinkIngredientCount[iCount] = 1

        tCount = len(drinks[d]['tastes'])
        if tCount in drinkTasteCount.keys():
            drinkTasteCount[tCount] += 1
        else:
            drinkTasteCount[tCount] = 1

        for i in drinks[d]['ingredients']:
            if i['id'] in ingredients.keys():
                ingredients[i['id']] += 1
            else:
                ingredients[i['id']] = 1

        for t in drinks[d]['tastes']:
            if t['id'] in tastes.keys():
                tastes[t['id']] += 1
            else:
                tastes[t['id']] = 1

    print('Found', len(ingredients.keys()), 'ingredients and',
        len(tastes.keys()), 'tastes')

    directory = '../profiling/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + 'drinkIngredientCount.json', 'w') as fp:
        json.dump(drinkIngredientCount, fp, sort_keys=True, indent=2)

    with open(directory + 'drinkTasteCount.json', 'w') as fp:
        json.dump(drinkTasteCount, fp, sort_keys=True, indent=2)

    with open(directory + 'ingredients.json', 'w') as fp:
        json.dump(ingredients, fp, sort_keys=True, indent=2)

    with open(directory + 'tastes.json', 'w') as fp:
        json.dump(tastes, fp, sort_keys=True, indent=2)

    print('Saved profiling data')

