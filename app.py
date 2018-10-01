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
    res = request.json
    print(res)
   
    #req = request.get_json(silent=True, force=True)
    '''
    print("Request1:")
    print(json.dumps(req, indent=4))
    sys.stdout.flush()
    res = processRequest(req)
    
    return(res)
    '''
    appturl = 'https://ivrinfocuit.herokuapp.com/InsertCustomerRoomBooking'
    headers = {'content-type': 'application/json'}
    
    print("JSON Data, Before requests.post")
    #print(json_data)
    
    result = requests.post(appturl, data = res, headers=headers)
    res = json.loads(result.text)
    
    print(json.dumps(res, indent=4))
    data = res.get('confirmation_number')
    print("confirmation num from data",data)
    return("fine")
if __name__ == '__main__':

     app.run(host='192.168.1.11',port=5000)#, port=port, )
