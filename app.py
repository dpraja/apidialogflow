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
    '''
    appturl = 'https://ivrinfocuit.herokuapp.com/InsertCustomerRoomBooking'
    headers = {'content-type': 'application/json'}
    
    print("JSON Data, Before requests.post")
    #print(json_data)
    
    result = requests.post(appturl, data = res, headers=headers)
    res = json.loads(result.text)
    print(res,type(res))
    if res['ServiceMessage'] == 'Failure':
            return("bad")
    else:    
      data = res.get('confirmation_number')
      print("confirmation num from data",data)
      return("confirmation num from data",data)
    '''  
    return("bad")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run(host='192.168.1.11',port=5000)#, port=port, )
