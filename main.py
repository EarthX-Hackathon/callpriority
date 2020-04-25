from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
from twilio import twiml
import flask
import csv
import requests

from twilio.rest import Client
import spacy
nlp = spacy.load('en_core_web_sm')
from flask import Flask, jsonify
from flask import request, redirect

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Record, VoiceResponse, Gather
from xml.etree import ElementTree


app = Flask(__name__)


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
    resp = VoiceResponse()

    if 'Digits' in request.values:
		# Get which digit the caller chose
        choice = request.values['Digits']
        phone = request.values['From']

        if choice == '1':
            resp2 = VoiceResponse()
            resp2.say("Hi, how can I help you today?", voice='alice', language="en-US")

            resp2.record(maxLength = 20,timeout=10, transcribe=True, transcribeCallback="/handleVoiceResponse")
            print(resp2)
            return str(resp2)

        elif choice == '2':
            resp2 = VoiceResponse()
            resp2.say("Hola como puedo ayudarte hoy?", voice='alice', language="es-MX")

            resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
            print(resp2)
            return str(resp2)

        elif choice == '3':
            resp2 = VoiceResponse()
            resp2.say("嗨，我今天怎么能帮到你？", voice='alice', language="zh-CN")

            resp2.record(maxLength = 20, timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
            print(resp2)
            return str(resp2)

        else:
            resp.say("Sorry, I dint understand the input")
            return ""

    xmlrep = "<?xml version='1.0' encoding='UTF-8'?><Response><Hangup/></Response>"
    tree = ElementTree.fromstring(xmlrep)
    return xmlrep

@app.route("/handleVoiceResponse", methods=['GET', 'POST'])
def handleVoiceREsponse():
    resp = VoiceResponse()
    soundURL = (request.values['RecordingUrl'])
    print (request.values)
    calltext = request.values['TranscriptionText']
    replytext ='nothing came'
    gotreply = False

    with open('FAQ.csv', encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file , delimiter=',')

        for row in csv_reader:
            similarity = nlp(row[0].lower()).similarity(nlp(calltext.lower()))
            print (similarity)
            print (str(calltext), str(row[0]))
            if similarity > 0.80:
                gotreply = True
                replytext = str(row[1])

    if gotreply==False:
        replytext = "Thank you for calling. Currently all our helpers are busy, we will reach back to you soon."

    resp.play('https://api.twilio.com/cowbell.mp3', loop=5)
    #resp3.say("ok, bye. Good night.", voice='alice', language="en-US")
    print("here is the reply",resp)
    xmlrep = "<?xml version='1.0' encoding='UTF-8'?><Response><Hangup/></Response>"
    tree = ElementTree.fromstring(xmlrep)
    return xmlrep


if __name__=="__main__":
    app.run(debug=True)
