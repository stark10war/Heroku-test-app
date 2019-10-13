import pandas as pd
import numpy as np
import os
import json
from flask import Flask, request, make_response, jsonify
import paho.mqtt.client as mqtt


broker_address= "soldier.cloudmqtt.com"
port = 10671
user = "rjzblyan"
password = "YLW-IRQ_Vqlr"
client = mqtt.Client('dialogflow_webhook')
client.username_pw_set(user, password=password)

# flask app for webhook
app = Flask(__name__)
log = app.logger


device_db = pd.read_excel(r'device_database.xlsx')


def handle_device_on(req, response_content):
    location = req.get('queryResult').get('parameters').get('room')
    device = req.get('queryResult').get('parameters').get('device')
    lights = req.get('queryResult').get('parameters').get('lights')
    pin = device_db.loc[(device_db.Location == location)&(device_db.DeviceName == device),'Pin'].values[0] 
    topic = 'home/'+location+'/'+pin
    client.connect(broker_address, port=port)
    client.publish(topic, "on")
    response_msg = "Turned on {} in {} : message broadcasted on topic {}".format(device, location, topic)
    response_content['fulfillmentText']  =  response_msg
    return response_content




def handle_device_off(req, response_content):
    location = req.get('queryResult').get('parameters').get('room')
    device = req.get('queryResult').get('parameters').get('device')
    lights = req.get('queryResult').get('parameters').get('lights')
    pin = device_db.loc[(device_db.Location == location)&(device_db.DeviceName == device),'Pin'].values[0] 
    topic = 'home/'+location+'/'+pin
    client.connect(broker_address, port=port)
    client.publish(topic, "off")
    response_msg = "Turned off {} in {} : message broadcasted on topic {}".format(device, location, topic)
    response_content['fulfillmentText']  =  response_msg
    return response_content



@app.route('/', methods=['GET'])
def test():
    return '''<h>
                Welcome MR. Stark10war            
                \n The Heroku App is up and running 
                \n Just one function for handeling request is defined<h\>'''




@app.route('/iot', methods=['POST'])
def process_request():
    response_content = {'fulfillmentText': ''}
    req = request.get_json(silent = True, force =  True)
    intent_name = req.get('queryResult').get('intent').get('displayName')
    intent_funcs = {'smarthome.device.switch.on': handle_device_on, 'smarthome.device.switch.off': handle_device_off }
    try:
        handle_request = intent_funcs[intent_name]
        response_content = handle_request(req, response_content)
        res = json.dumps(response_content, indent = 4)
        return make_response(res)
    except:
        response_msg = "No Such device founds."
        response_content['fulfillmentText']  =  response_msg
        res = json.dumps(response_content, indent = 4)
        return make_response(res)

    with open('request.json', 'r') as f:
        req = json.load(f)
        



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)
