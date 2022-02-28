import requests, json
from pprint import pprint
import pandas as pd
# base url for all FPL API endpoints


# get data from bootstrap-static endpoint


# show the top level fields
#pprint(r, indent=2, depth=1, compact=True)

# get player data from 'elements' field
# show data for first player
#players = pd.json_normalize(r['elements'])

def getPlayer():
    base_url = 'https://fantasy.premierleague.com/api/'
    r = requests.get(base_url+'bootstrap-static/').json()
    players = pd.json_normalize(r['elements'])
    return players