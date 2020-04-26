from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
from twilio import twiml
import flask
import csv
import requests
import time

from twilio.rest import Client
import spacy
nlp = spacy.load('en_core_web_sm')
from flask import Flask, jsonify
from flask import request, redirect

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Record, VoiceResponse, Gather
from xml.etree import ElementTree
from twilio.rest import Client

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

app = Flask(__name__)

replytext ='empty msg'

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()

    g = Gather(num_digits=1, action='/handleVoice')
    g.say("Welcome, press one for English", voice='alice', language="en-US")
    g.say("Bienvenido, para español, presione 2", voice='alice', language="es-MX")
    g.say("欢迎，按3为中文", voice='alice', language="zh-CN")

    resp.append(g)

    resp.redirect('/voice')

    return str(resp)


@app.route("/handleVoice", methods=['GET', 'POST'])
def handleVoice():
    resp2 = VoiceResponse()

    if 'Digits' in request.values:
		# Get which digit the caller chose
        choice = request.values['Digits']
        phone = request.values['From']

        if choice == '1':
            gg =Gather(num_digits=1, action='/recordAndSend')
            gg.say("Hi, all our agents are busy right now. If your query is not urgent, would you like to leave a msg for us? We will get back to you with the response very soon. Press 1 to leave a msg. Press 2 to wait for the agent.", voice='alice', language="en-US")

            resp2.append(gg)

            print(resp2)
            return str(resp2)

        elif choice == '2':
            gg =Gather(num_digits=1, action='/recordAndSend')
            gg.say("Hola, todos nuestros agentes están ocupados en este momento. Si su consulta no es urgente, ¿desea dejarnos un mensaje? Nos pondremos en contacto con usted con la respuesta muy pronto. Presione 1 para dejar un mensaje. Presione 2 para esperar al agente.", voice='alice', language="es-MX")

            resp2.append(gg)

            print(resp2)
            return str(resp2)

        elif choice == '3':
            gg =Gather(num_digits=1, action='/recordAndSend')
            gg.say("嗨，我们所有的经纪人现在都在忙。如果您的查询不紧急，您想给我们留言吗？我们会尽快回复您。按1离开留言。按2等待代理。", voice='alice', language="zh-CN")

            resp2.append(gg)

            print(resp2)
            return str(resp2)

        else:
            resp2.say("Sorry, I dint understand the input")
            return ""

    return str(resp2)

@app.route("/handleVoiceResponse", methods=['GET', 'POST'])
def handleVoiceResponse():
    #resp = VoiceResponse()
    soundURL = (request.values['RecordingUrl'])
    print (request.values)
    calltext = request.values['TranscriptionText']
    caller = request.values['From']

    gotreply = False
    global replytext

    with open('FAQ.csv', encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file , delimiter=',')

        for row in csv_reader:
            similarity = nlp(row[0].lower()).similarity(nlp(calltext.lower()))
            #print (similarity)
            #print (str(calltext), str(row[0]))
            if similarity > 0.70:
                gotreply = True
                replytext = str(row[1])

    if gotreply==False:
        replytext = "Jake was not able to answer your query. Our agents will reach you soon."

    print("what caller said--------", calltext)
    print("reply text is ------", replytext)

    account_sid = 'AC81bcf045adf8efd2d60103cec297bdef'
    auth_token = '744d9857238e1d524cee6f6d349deac7'
    client = Client(account_sid, auth_token)
    msgBody = "Hi! This is Jake from State farm. Answer to your query - " + replytext

    message = client.messages.create(
                              body=msgBody,
                              from_='+12056354001',
                              to=caller
                          )


    return 'success'


@app.route("/recordAndSend", methods=['GET','POST'])
def recordAndSend():
    resp = VoiceResponse()

    if 'Digits' in request.values:
        choice = request.values['Digits']

        if choice == '1':
            resp.say("Hi, how can I help you today?", voice='alice', language="en-US")
            resp.record(maxLength = 20,timeout=10, transcribe=True, transcribeCallback="/handleVoiceResponse")

            print (resp)
            return str(resp)

        if choice == '2':
            resp.say("Please stay online.", voice='alice', language="en-US")
            resp.hangup()

    else:
        resp.say("We got your msg. Thank you.", voice='alice', language="en-US")
        resp.hangup()

    return str(resp)

'''
@app.route("/saythis", methods=['GET', 'POST'])
def saythis():
    replytext2 = request.args.get('reptext')

    resp = VoiceResponse()
    resp.say(replytext2, voice='alice', language="en-US")
    return 'ok'
'''

def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp


if __name__=="__main__":
    app.run(debug=True)
