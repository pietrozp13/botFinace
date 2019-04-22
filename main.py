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



def addFirebase(acao, valor, quant):
    doc_ref = db.collection(u'acoes').document()
    setF = doc_ref.set({
        u'acao': (u'{}'.format(acao)),
        u'valor': valor,
        u'quant': quant
    })
    return setF

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/fireget")
def firetesteget():

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

    return '{}'.format(msg)


#verificar envio para o whats
@app.route("/data")
def data():

    msg = getData()

    return msg


#metodo para configurar
@app.route("/config", methods=['POST'])
def config():
    req = request.get_json()
    acao = req['codigo']
    valor = req['precoComprado']
    quant = req['quant']

    addFirebase(acao, valor, quant)

    return jsonify(req)


#metodo de envio para o whats
@app.route("/sms", methods=['POST'])
def sms_reply():

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


    resp = MessagingResponse()
    resp.message("{}".format(msg))

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)