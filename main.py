from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import requests
import urllib, json
import time
import sys

def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"
    return prc.format(f_val)

def getData():
    my_port = 12.01
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=ITSA4.SA&interval=15min&apikey=KO6Z7R9AZMI0XZBR"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    dataP = data['Time Series (15min)']

    lastRefreshe = data['Meta Data']
    first_data = float(dataP[lastRefreshe['3. Last Refreshed']]['1. open'])

    valor_lucro = first_data / my_port
    calc_percent = valor_lucro - 1
    return floating_decimals((calc_percent * 100), 3)


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/data")
def data():

    msg = getData()

    return msg

@app.route("/sms", methods=['POST'])
def sms_reply():

    msg = getData()

    resp = MessagingResponse()
    resp.message("ITSA4 now: {}".format(msg))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)