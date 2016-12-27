import requests
import json
import flask
import sys
import os
from unidecode import unidecode
from response_functions.get_time_response import get_time_response
from response_functions.get_location_response import get_location_response
from response_functions.get_info_response import get_info_response

# Help taken from https://github.com/svet4/shipping-costs-sample/blob/master/app.py


app = flask.Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    
    locations = requests.get('http://apis.scottylabs.org/dining/v1/locations')
    locations = locations.json()
    CMU_Dining_Dict = {}
    for i in range(len(locations["locations"])):
        CMU_Dining_Dict[unidecode(locations["locations"][i]["name"])] = locations["locations"][i]


    req = flask.request.get_json(silent=True, force=True)

    print("Request:")
    sys.stdout.flush()
    print(json.dumps(req, indent=4))
    sys.stdout.flush()

    res = makeWebhookResult(req, CMU_Dining_Dict)

    res = json.dumps(res, indent=4)
    print(res)
    sys.stdout.flush()
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req, CMU_Dining_Dict):
    if req.get("result").get("action") == "get_time":
        speech = get_time_response(req, CMU_Dining_Dict)
    
    elif req.get("result").get("action") == "get_location":
        speech = get_location_response(req, CMU_Dining_Dict)

    elif req.get("result").get("action") == "get_info":
        speech = get_info_response(req, CMU_Dining_Dict)

    else:
        speech = {}

    print("Response:")
    print(unidecode(speech))

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-cmu-dining-assisant"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)
    sys.stdout.flush()

    app.run(debug=True, port=port, host='0.0.0.0')


