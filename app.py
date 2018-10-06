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
from dateutil import parser


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

def arrival_date(arr_date):
    print("arrival_date",arr_date)
    #arr_date = datetime.datetime.strptime(arr_date, '%d-%m-%Y').date()     #datetime format
    #dep_date = datetime.datetime.strptime(date2, '%d-%m-%Y').date()
    #arr_date = arr_date.strftime("%Y-%m-%d")                             #formatted string datetime
    #dep_date = dep_date.strftime("%Y-%m-%d")
    arr_date = datetime.datetime.strptime(arr_date, '%Y-%m-%d').date()   #convert string to datetime format
    #dep_date = datetime.datetime.strptime(dep_date, '%Y-%m-%d').date()
    #print(arr_date,dep_date)
    print(arr_date,type(arr_date))
    #arr_date = datetime.datetime.strptime(arr_date, '%d-%m-%Y').date()
    #arr = parser.parse(arr_date).date().strftime('%d-%m-%Y')
    today_date = datetime.datetime.utcnow().date()
    
    print(today_date)
    if arr_date >= today_date:
       return (True)
    else:
        return (False)
        '''
        return {
            "speech": "Arrival date must be scheduled atleast one day in advance.",
            "displayText": "Arrival date must be scheduled atleast one day in advance."
            }
        '''    
    #return(arr)

def departure_date(departure_date,arrival):
    print("arrival_date inside validation fun",departure_date)
    dept = datetime.datetime.strptime(departure_date, '%Y-%m-%d').date()
    arrival = datetime.datetime.strptime(arrival, '%Y-%m-%d').date()
    today_date = datetime.datetime.utcnow().date()
    print(today_date)
    restrict_days =  today_date + datetime.timedelta(days=90)
    print(restrict_days)
    arr_date = arrival
    print("departure********************", arr_date,dept,type(arr_date),type(dept))
    if  dept >= arr_date :
        if dept <= restrict_days:
            print("its cameeeeeeeeeeeee")
            return (True)
        else:
            return (False,1)
          
    else:
        #print("its not cameeeeeeeeeee")
        print("departure",dept)
        return (False,2)
      
    
def adult_fun(adult):
    print("adult inside validation fun",adult)
    if adult<=10:
        return (True)
    else:
        return (False)

def child_fun(child):
    print("child inside validation fun",child)
    if child<=10:
        return (True)
    else:
        return (False)
    
def mob_fun(mobile):
    no = mobile 
    string = (no + '.')[:-1]
    #print(string,type(string),string[0:1],type(string[0:1]))
    st = string[0:1]
    list1 = [i for i in range(len(string)) if string.startswith(st, i)]
    #print("li:",len(list1),type(len(list1)))
    if len(no) == 10 and 10 != len(list1):
        print(len(no))
        return(True)
    else:
        return (False)


def processRequesteng(req):
    if req['result']['action'] != "bookhotels":    
        return {}
    print("test req",req)
    print(req['result']['action'],type(req['result']['action']))
    result = req.get("result")
    parameters = result.get("parameters")
    #i = 5 if a > 7 else 0
    if True == arrival_date(parameters.get("arrival")):
        arrival = parameters.get("arrival")
        #arrival=arrival.split("-")
        #arrival=arrival[1]+arrival[2]
    else:
        return {
            "speech": "Arrival date must be scheduled atleast one day in advance.",
            "displayText": "Arrival date must be scheduled atleast one day in advance."
            }
    print(arrival,type(arrival))

    
    if True == departure_date(parameters.get("departure"),arrival):
       departure = parameters.get("departure")
       departure=departure.split("-")
       departure=departure[1]+departure[2]
    elif (False,1) == departure_date(parameters.get("departure"),arrival):
        return {
            "speech": "Departure date should not exceed 90 days than arrival.",
            "displayText": "Departure date should not exceed 90 days than arrival."
            }
    else:
        return {
            "speech": "Departure date should not be in past date than arrival",
            "displayText": "Departure date should not be in past date than arrival"
            }
        

    if True == adult_fun(parameters.get("adult")):
        adult = parameters.get("adult")
    else:
        return {
            "speech": "Sorry, Adult count should not exceed 10.",
            "displayText": "Sorry, Adult count should not exceed 10."
            }
        
        
    if True == child_fun(parameters.get("child")):
        child = parameters.get("child")
    else:
        return {
            "speech": "Sorry, Child count should not exceed 10.",
            "displayText": "Sorry, Child count should not exceed 10."
            }
        
    roomtype = parameters.get("roomtype")
    countrycode = parameters.get("countrycode")
    if True== mob_fun(mobile = parameters.get("mobile")):
        mobile = parameters.get("mobile")
    else:
        return {
            "speech": "Sorry, the phone number is invalid.",
            "displayText": "Sorry, the phone number is invalid."
            }
    
    #pickup = parameters.get("pickup")
    pd = parameters.get("pickup")
    yeslist=['yeah','ya','yup','s','yes','y']
    nolist=['no','nope','nah','n']
    if (pd in yeslist):
        pickup='y'
    
    elif (pd in nolist):
        pickup='n'
    else:
        return {
            "speech": "Sorry, that was not a valid input.",
            "displayText": "Sorry, that was not a valid input."
            }
        
    conf = parameters.get("conf")
#splitting arrival date for webservice format(mmdd)
    arrival=arrival.split("-")
    arrival=arrival[1]+arrival[2]

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
         speech = "Great! Your booking has been confirmed and your Confirmation number is "+confirmation_num + ". Your check-in starts at 14:00. You will shortly receive an SMS with all booking details. We look forward to host you soon and extend you a very warm welcome. We hope and trust your stay with us will be both enjoyable and comfortable. Have a great day. "
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
