import requests
import re
import json
import sys
import demjson

privateLow = 'PrivatePartyExcellentRangeLow'
asking = 'amount_in_currency'

params = {'csv': ''}
args = sys.argv

for key, arg in enumerate(args):
    stripVar = arg.replace('--', '')

    if stripVar in params:
        params[stripVar] = args[key + 1]

def viewSource(url):
    return requests.get(url, allow_redirects=True).content

def keyStrObj(key, source):
    return '{' + re.search('[^\{]*' + key + '[^\}]*', source).group(0).decode('string_escape') + '}'

def objectify(key, source):
    return demjson.decode(keyStrObj(key, source))

def keyRes(key, source):
    return objectify(key, source)[key]

def merge(obj1, obj2):
    store1 = obj1
    store1.update(obj2)

    return store1

if params['csv']:
    allTrucks = params['csv'].split(',')
else:
    with open('marketplace.csv') as truckList: # Use file to refer to the file object
        allTrucks = truckList.read().split(',')

for truck in allTrucks:
    htmlSource = viewSource(truck)

    if privateLow in htmlSource and asking in htmlSource:
        truckObj = merge(objectify(privateLow, htmlSource), objectify(asking, htmlSource))

        if (truckObj[privateLow] / float(truckObj[asking])) >= 2:
            print truck


