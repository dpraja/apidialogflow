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
    return("welcome thalaivi banupriya")

@app.route('/dialogflow-reservation', methods=['POST'])
def webhook():
    
    re = request.json
    print("re",re)
    res = re['queryResult']['parameters']
    print("res",res)
    data = {}
    data['TFN'] = "+18663637049"
    data['customer_name'] = "customer"
    data['customer_arrival_date'] = res['arrival']
    data['customer_depature_date'] = res['departure']
    data['customer_adult'] = res['adult']    
    data['customer_child'] = res['child']
    data['customer_room_type'] = res['roomtype']
    data['customer_mobile'] = res['mobile']
    data['cntry_code'] = res['countrycode']
    data['customer_no_of_rooms'] = "1"
    data['customer_cc'] = "0987"
    data['customer_room_rate'] = "1000"
    data['customer_pickup_drop'] = res['pickup']
    data['customer_expirydate'] = "0987"
    data['ivr_language'] = "2"
    
    appturl = 'https://ivrinfocuit.herokuapp.com/InsertCustomerRoomBooking'
    headers = {'content-type': 'application/json'}
    
    print("JSON Data, Before requests.post")
    #print(json_data)
    
    result = requests.post(appturl, data = res, headers=headers)
    res = json.loads(result.text)
    print(res,type(res))
    if res['ServiceMessage'] == 'Failure':
         print("in if statement")
         speech = "Sorry"  
         print("in if statement")
    else:    
      data = res.get('confirmation_number')
      print("confirmation num from data",data)
      speech = "confirmation:"+data
      #return("confirmation num from data",data)
    #result = json.dumps(res, indent=4)
    return(json.dumps({
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    },indent=4))
    '''  
    return("bad")
    '''

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run(host='192.168.1.11',port=5000)#, port=port, )
