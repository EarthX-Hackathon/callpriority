from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
from twilio import twiml
import flask

from twilio.rest import Client
import spacy
nlp = spacy.load('en')
from flask import Flask, jsonify
from flask import request, redirect

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather


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

			resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
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

			resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
			print(resp2)
			return str(resp2)

		else:
			resp.say("Sorry, I dint understand the input")
			return ""



	return ""




if __name__=="__main__":
    app.run(debug=True)
