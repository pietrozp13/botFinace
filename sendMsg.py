from twilio.rest import Client
import requests
import urllib, json
import datetime

import schedule
import time

TWILIO_ACCOUNT_SID= ''
AUTH_TOKEN= ''

client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

from_whatsapp_number='whatsapp:+14155238886'

to_whatsapp_number='whatsapp:+554891379111'


from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS
import requests
import urllib, json
import time
import sys

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#FIREBASE

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./SecKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#ROTAS

def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"
    return prc.format(f_val)

def getData(cod, valor):
    my_port = valor
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}.SA&interval=15min&apikey=KO6Z7R9AZMI0XZBR".format(cod)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    dataP = data['Time Series (15min)']

    lastRefreshe = data['Meta Data']
    first_data = float(dataP[lastRefreshe['3. Last Refreshed']]['4. close'])
    valor_lucro = first_data / my_port
    calc_percent = valor_lucro - 1
    return floating_decimals((calc_percent * 100), 3)



def job():
    users_ref = db.collection(u'acoes')
    docs = users_ref.get()
    msg = "Acoes: "
    for doc in docs:
        docKey = doc.to_dict()

        cod = docKey['acao']
        valor = docKey['valor']

        resp = getData(cod, valor)
        msg = msg + cod + ': ' + resp + '%\n'
        print(resp)

    msg = client.messages.create(body="{}".format(msg),
                    from_=from_whatsapp_number,
                   to=to_whatsapp_number)
    print(msg.sid)


schedule.every().day.at("09:50").do(job)

schedule.every().day.at("10:30").do(job)

schedule.every().day.at("12:50").do(job)

schedule.every().day.at("15:00").do(job)

schedule.every().day.at("18:00").do(job)

schedule.every().day.at("23:25").do(job)

schedule.every().day.at("23:40").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
