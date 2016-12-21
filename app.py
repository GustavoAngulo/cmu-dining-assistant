import requests
from unidecode import unidecode
import ast
import json

locations = requests.get('http://apis.scottylabs.org/dining/v1/locations')
locations = locations.json()
for i in range(len(locations["locations"])):
    print(unidecode(locations["locations"][i]["name"]))
    print(unidecode(locations["locations"][i]["location"]))
