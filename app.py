import requests
import json
import flask
# from flask import Flask
# from flask import request
# from flask import make_response
from unidecode import unidecode

# Help taken from https://github.com/svet4/shipping-costs-sample/blob/master/app.py

locations = requests.get('http://apis.scottylabs.org/dining/v1/locations')
locations = locations.json()
CMU_Dining_Dict = {}
for i in range(len(locations["locations"])):
    CMU_Dining_Dict[unidecode(locations["locations"][i]["name"])] = locations["locations"][i]

# for i in range(len(locations["locations"])):
#     print(unidecode(locations["locations"][i]["name"]))
#     print(unidecode(locations["locations"][i]["location"]))




app = flask.Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = flask.request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") == "get_time":
        speech = get_time_response(req)
    else:
        speech = {}

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }

def get_time_response(req):
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")
    location_status = parameters.get("location-status")
    if location_status == "open":
        time_hour = CMU_Dining_Dict[location]["times"][0]


