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
from frenchflow import webhook

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return("welcome")

@app.route('/dialogflow-reservation-french', methods=['POST'])
def french():
    return webhook(req)

@app.route('/dialogflow-reservation', methods=['POST'])
def webhookeng():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    sys.stdout.flush()
    print(req['result']['action'])
    if req['result']['action'] == "bookhotels":
        print(req['result']['action'])
        res = processRequesteng(req)
    elif req['result']['action'] == "modify":
        print(req['result']['action'])
        res = processRequestmodify(req)
    elif req['result']['action'] == "cancelbook":
        print(req['result']['action'])
        res = processRequestcancel(req)
    else:
        return {}
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequesteng(req):
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
    print(data)
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
         speech = "Great! Your booking has been confirmed and your Confirmation number is :"+confirmation_num + ". Your check-in starts at 14:00. You will shortly receive an SMS with all booking details. We look forward to host you soon and extend you a very warm welcome. We hope and trust your stay with us will be both enjoyable and comfortable. Have a great day. "
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

#Modify
def processRequestmodify(req):
    if req['result']['action'] != "modify":    
        return {}
    print(req['result']['action'],type(req['result']['action']))
    result = req.get("result")
    parameters = result.get("parameters")
    conf_no = parameters.get("conf_no")
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
    data['confirmation_number'] = conf_no
    data['customer_name'] = "customer"
    data['customer_arrival_date'] = arrival
    data['customer_depature_date'] = departure
    data['customer_adult'] = adult
    data['customer_child'] = child
    data['customer_room_type'] = roomtype
    data['customer_mobile'] = mobile
    data['customer_cc'] = "0987"
    data['customer_room_rate'] = "1000"
    data['customer_pickup_drop'] = pickup
    data['customer_expirydate'] = "0987"
    
    print(data)
    json_data = json.dumps(data)
    
#def makeWebhookResult(json_data):
    
    result = None
    res = None
    confnum = None
    
    appturl = 'https://ivrinfocuit.herokuapp.com/UpdateExistingBooking'
    headers = {'content-type': 'application/json'}
    
    print("JSON Data, Before requests.post")
    print(json_data)
    
    result = requests.post(appturl, data = json_data,headers=headers)
    res = json.loads(result.text)

    print('res',json.dumps(res, indent=4))
    
    if res['ServiceMessage'] == 'Success':
         print("in if statement")
         speech = "Great! Your booking has been modified. Your check-in starts at 14:00. You will shortly receive an SMS with all booking details. We look forward to host you soon and extend you a very warm welcome. We hope and trust your stay with us will be both enjoyable and comfortable. Have a great day. "
         print("in if statement")
    else:
        speech = "Sorry Currently we are unable to process. Please try again."

    print("Response:")
    print(speech)
    
    return{
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

#Cancel
def processRequestcancel(req):
    if req['result']['action'] != "cancelbook":    
        return {}
    #print(req['result']['action'],type(req['result']['action']))
    result = req.get("result")
    parameters = result.get("parameters")
    conf_no = parameters.get("conf_no")
    print("paraaa",parameters)
    sys.stdout.flush()
    
    result = None
    res = None
    confnum = None
    
    appturl = "https://ivrinfocuit.herokuapp.com/CancelCurrentbooking?conf_no="+str(conf_no)+""
    headers = {'content-type': 'application/json'}
    
    
    result = requests.get(appturl)
    res = json.loads(result.text)

    print('res',json.dumps(res, indent=4))
    
    if res['Return_Code'] == 'RCS':
         print("in if statement")
         speech = "Great! Your booking has been cancelled. Thank you. Have a great day."
         print("in if statement")
    if res['Return_Code'] == 'ICN':
         print("in if statement")
         speech = "Sorry, that was not a valid confirmation number. Please try again later."
         print("in if statement")
    else:
        speech = "Sorry Currently we are unable to process. Please try again."

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
