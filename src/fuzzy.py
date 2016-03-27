from absolutDataFetch import fetch
import itertools
import os
import json
import numpy as np
import skfuzzy as fuzz

def fuzzyDistance(drink1, drink2):
  commonIngredients = getCommonPercentage(
    drink1['ingredients'],
    drink2['ingredients'])
  commonTastes = getCommonPercentage(drink1['tastes'], drink2['tastes'])
  commonTools = getCommonPercentage(drink1['tools'], drink2['tools'])
  x = np.arange(101)
  farByIngredients = fuzz.trapmf(x, [0, 0, 20, 30])
  avgByIngredients = fuzz.trimf(x, [20, 40, 60])
  closeByIngredients = fuzz.trapmf(x, [50, 60, 100, 100])
  farByTastes = fuzz.trapmf(x, [0, 0, 20, 30])
  avgByTastes = fuzz.trimf(x, [20, 40, 60])
  closeByTastes = fuzz.trapmf(x, [50, 60, 100, 100])
  farByTools = fuzz.trapmf(x, [0, 0, 40, 50])
  avgByTools = fuzz.trimf(x, [40, 60, 80])
  closeByTools = fuzz.trapmf(x, [70, 80, 100, 100])
  lowSim = fuzz.trapmf(x, [0, 0, 40, 60])
  highSim = fuzz.trapmf(x, [40, 60, 100, 100])

  fuzzyDist = []

  # If far by tools and far by ingredients and far by tastes then low similarity
  tNorm = min(farByTools[commonTools], farByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and far by ingredients and avg by tastes then low similarity
  tNorm = min(farByTools[commonTools], farByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and far by ingredients and close by tastes then low similarity
  tNorm = min(farByTools[commonTools], farByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and avg by ingredients and far by tastes then low similarity
  tNorm = min(farByTools[commonTools], avgByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and avg by ingredients and avg by tastes then low similarity
  tNorm = min(farByTools[commonTools], avgByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and avg by ingredients and close by tastes then low similarity
  tNorm = min(farByTools[commonTools], avgByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and close by ingredients and far by tastes then low similarity
  tNorm = min(farByTools[commonTools], closeByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and close by ingredients and avg by tastes then low similarity
  tNorm = min(farByTools[commonTools], closeByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If far by tools and close by ingredients and close by tastes then high similarity
  tNorm = min(farByTools[commonTools], closeByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If avg by tools and far by ingredients and far by tastes then low similarity
  tNorm = min(avgByTools[commonTools], farByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If avg by tools and far by ingredients and avg by tastes then low similarity
  tNorm = min(avgByTools[commonTools], farByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If avg by tools and far by ingredients and close by tastes then low similarity
  tNorm = min(avgByTools[commonTools], farByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If avg by tools and avg by ingredients and far by tastes then low similarity
  tNorm = min(avgByTools[commonTools], avgByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If avg by tools and avg by ingredients and avg by tastes then high similarity
  tNorm = min(avgByTools[commonTools], avgByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If avg by tools and avg by ingredients and close by tastes then high similarity
  tNorm = min(avgByTools[commonTools], avgByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If avg by tools and close by ingredients and far by tastes then low similarity
  tNorm = min(avgByTools[commonTools], closeByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If avg by tools and close by ingredients and avg by tastes then high similarity
  tNorm = min(avgByTools[commonTools], closeByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If avg by tools and close by ingredients and close by tastes then high similarity
  tNorm = min(avgByTools[commonTools], closeByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If close by tools and far by ingredients and far by tastes then low similarity
  tNorm = min(closeByTools[commonTools], farByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If close by tools and far by ingredients and avg by tastes then low similarity
  tNorm = min(closeByTools[commonTools], farByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If close by tools and far by ingredients and close by tastes then low similarity
  tNorm = min(closeByTools[commonTools], farByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If close by tools and avg by ingredients and far by tastes then low similarity
  tNorm = min(closeByTools[commonTools], avgByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If close by tools and avg by ingredients and avg by tastes then low similarity
  tNorm = min(closeByTools[commonTools], avgByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If close by tools and avg by ingredients and close by tastes then high similarity
  tNorm = min(closeByTools[commonTools], avgByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If close by tools and close by ingredients and far by tastes then low similarity
  tNorm = min(closeByTools[commonTools], closeByIngredients[commonIngredients], farByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in lowSim])

  # If close by tools and close by ingredients and avg by tastes then high similarity
  tNorm = min(closeByTools[commonTools], closeByIngredients[commonIngredients], avgByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  # If close by tools and close by ingredients and close by tastes then high similarity
  tNorm = min(closeByTools[commonTools], closeByIngredients[commonIngredients], closeByTastes[commonTastes])
  fuzzyDist.append([d if d <= tNorm else tNorm for d in highSim])

  unionDist = [0] * 101
  for dist in fuzzyDist:
    (x, unionDist) = fuzz.fuzzy_or(x, unionDist, x, dist)

  return fuzz.defuzzify.centroid(x, np.array(unionDist))

def getDrinkPairs(drinks):
  drinkPairs = []
  for drink1 in drinks:
      for drink2 in drinks:
          if drink1['id'] < drink2['id']:
              drinkPairs.append((drink1['id'], drink2['id']))
  return drinkPairs

def getDrinkDistances(drinkPairs, drinkDict):
  drinkDistances = {}
  count = 0
  total = len(drinkPairs)
  for (drink1, drink2) in drinkPairs:
    count += 1
    if (count % 10000 == 0):
      print('.', end = '', flush = True)
    d1 = drinkDict[drink1]
    d2 = drinkDict[drink2]
    drinkDistances[str((drink1, drink2))] = fuzzyDistance(d1, d2)
  return drinkDistances

def getCommonPercentage(drink1, drink2):
  common = len(set(drink1).intersection(set(drink2)))
  percent1 = common / len(drink1)
  percent2 = common / len(drink2)
  percent = (percent1 + percent2) / 2
  return int(percent * 100)

def fuzzySim(drinkPairs, drinkDict, force = False):
  directory = '../datasets/'
  fileName = directory + 'dist.json'
  drinkDistances = {}
  if not force and os.path.isfile(fileName):
    with open(fileName) as fp:
      drinkDistances = json.load(fp)
  else:
    drinkDistances = getDrinkDistances(drinkPairs, drinkDict)
    if not os.path.exists(directory):
      os.makedirs(directory)
    with open(fileName, 'w') as fp:
      json.dump(drinkDistances, fp, sort_keys=True)
  return drinkDistances

def inferRatings(drinks, drinkDistances, userRatings, forceCalc = False):
  directory = '../datasets/'
  fileName = directory + 'ratings.json'
  ratingEstimates = {}
  for drink in drinks.keys():
    if drink not in userRatings.keys():
      similarities = []
      for ratedDrink in userRatings.keys():
        if drink < ratedDrink:
          similarities.append((ratedDrink, drinkDistances[str((drink, ratedDrink))]))
        else:
          similarities.append((ratedDrink, drinkDistances[str((ratedDrink, drink))]))
      similarities = sorted(similarities, key = lambda x: x[1])
      similarities = similarities[0:10]
      similarities = [s for s in similarities if s[1] >= 50]
      ratingEstimate = 0
      if len(similarities) > 0:
        simSum = sum([s[1] for s in similarities])
        for s in similarities:
          ratingEstimate += s[1] * userRatings[s[0]]
        ratingEstimate /= simSum
      ratingEstimates[drink] = ratingEstimate

  if not os.path.exists(directory):
    os.makedirs(directory)
  with open(fileName, 'w') as fp:
    json.dump(ratingEstimates, fp, sort_keys=True)

  return ratingEstimates

def run():
  drinks = fetch()
  # drinks = drinks[0:100]
  drinkDict = {}
  for key, group in itertools.groupby(drinks, lambda d: d['id']):
    drinkDict[key] = list(group)[0]
  print("Drinks:", len(drinks))

  drinkPairs = getDrinkPairs(drinks)
  print("Drink Pairs:", len(drinkPairs))

  drinkDistances = fuzzySim(drinkPairs, drinkDict)
  print("Drink Distances:", len(drinkDistances.keys()))

  userRatings = {
    'golden-gleam': 5,
    'whispers-of-the-frost': 4,
    'blue-lady': 4,
    'pepparmint-frape': 1
  }

  ratings = inferRatings(drinkDict, drinkDistances, userRatings, True)
  print("Estimated Ratings:", len(ratings.keys()))

  return ratings
