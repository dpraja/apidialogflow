from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import datetime
import os
import requests
import sys

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return("welcome")

@app.route('/dialogflow-reservation-french', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    sys.stdout.flush()
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req['result']['action'] != "bookhotels":    
        return {}
    print(req['result']['action'],type(req['result']['action']))
    result = req.get("result")
    parameters = result.get("parameters")
    conf = parameters.get("conf")
    arrival = parameters.get("arrival")
    arrival=arrival.split("-")
    arrival=arrival[1]+arrival[2]
    departure = parameters.get("departure")
    departure=departure.split("-")
    departure=departure[1]+departure[2]
    adult = parameters.get("adult")
    child = parameters.get("child")
    roomtype = parameters.get("roomtype")
    countrycode = parameters.get("countrycode")
    mobile = parameters.get("mobile")
    #pickup = parameters.get("pickup")
    pd = parameters.get("pickup")
    yeslist=['yeah','ya','yup','s','yes','y']
    if pd in yeslist:
        pickup='y'
    nolist=['no','nope','nah','n']
    if pd in nolist:
        pickup='n'
    print("paraaa",parameters)
    
    data = {}
    data['TFN'] = "+18663637049"
    data['customer_name'] = "customer"
    data['customer_arrival_date'] = arrival
    data['customer_depature_date'] = departure
    data['customer_adult'] = adult
    data['customer_child'] = child
    data['customer_room_type'] = roomtype
    data['customer_mobile'] = mobile
    data['cntry_code'] = countrycode
    data['customer_no_of_rooms'] = "1"
    data['customer_cc'] = "0987"
    data['customer_room_rate'] = "1000"
    data['customer_pickup_drop'] = pickup
    data['customer_expirydate'] = "0987"
    data['ivr_language'] = "2"
    print("dataaaaaaaaaaaa",data)
    json_data = json.dumps(data)

    print("Request Parsed,Success...")
    print("Sending JSON Data...")
    print(json_data)

    sys.stdout.flush()
    res = makeWebhookResult(json_data)
    return res

def makeWebhookResult(json_data):

    result = None
    res = None
    confnum = None
    
    appturl = 'https://ivrinfocuit.herokuapp.com/InsertCustomerRoomBooking'
    headers = {'content-type': 'application/json'}
    
    print("JSON Data, Before requests.post")
    print(json_data)
    
    result = requests.post(appturl, data = json_data,headers=headers)
    res = json.loads(result.text)

    print('res',json.dumps(res, indent=4))
    
    if res['ServiceMessage'] == 'Success':
         print("in if statement")
         confirmation_num = str(res.get('conf_no'))
         speech = "Génial! Votre réservation a été confirmée et votre numéro de confirmation est:"+confirmation_num + ". Votre enregistrement commence à 14h00. Vous allez bientôt recevoir un SMS avec tous les détails de la réservation. Nous sommes impatients de vous accueillir bientôt et de vous souhaiter la bienvenue. Nous espérons que votre séjour avec nous sera à la fois agréable et confortable. Passez une bonne journée. "
         print("in if statement")
    else:
        speech = "Sorry "

    print("Response:")
    print(speech)
    
    return{
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
      
    
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run(host='192.168.1.7',port=5000)#, port=port, )
