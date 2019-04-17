from twilio.rest import Client

TWILIO_ACCOUNT_SID= 'AC162cdc9d6dfc3b6aa25176cb41d9c4e7'
AUTH_TOKEN= '57881f18adb87bdcbf666086f3f50f56'

client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

from_whatsapp_number='whatsapp:+14155238886'

to_whatsapp_number='whatsapp:+554891379111'

import requests
import urllib, json
import time
import sys

def clock():
    while True:
        from datetime import datetime
        now = datetime.now()
        print ("%s/%s/%s %s:%s:%s" % (now.month,now.day,now.year,now.hour,now.minute,now.second))
        print("\r"),
        time.sleep(1)
        if now.second == 10 and now.minute == 43 and now.hour == 15:
            print(now.second)
        sys.stdout.flush()

def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"
    return prc.format(f_val)

def getData():
    my_port = 12.01
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=ITSA4.SA&interval=15min&apikey=KO6Z7R9AZMI0XZBR"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    dataP = data['Time Series (15min)']
    first_key = (dataP.keys())[0]

    first_data = float(dataP[first_key]['1. open'])
    valor_lucro = first_data / my_port
    calc_percent = valor_lucro - 1
    print floating_decimals((calc_percent * 100), 3)


getData() 
#msg = client.messages.create(body='pietro e top!',
#                    from_=from_whatsapp_number,
#                   to=to_whatsapp_number)
#print(msg.sid)