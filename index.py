#James Lemieux

#This is where all the functions are routed back too:
#Ill have the main setup here off my main app and everything
#I need to have a global init function that will be the return from all the functions
#I could have a global webhook variable that can change the webhook on the fly
from flask import Flask,request
from kik import KikApi,Configuration
from kik.messages import TextMessage,messages_from_json,PictureMessage
from pictureFunctions import textFunction,scrapeImage
import random

#Declare the app
#The application allows for the application to be listened on the port
#ngrok is used to tunnel the response from the webhook into the Flask application
app = Flask(__name__)
cmds = ['/text','/img','/game','/Mot','/Weat','/?','/joke']
def main_init(webhook):
	#This is where I will change the webhook to allow for the decorator of user commands
	kik = KikApi('jarvisentail','7a88d75b-076c-448e-b5f3-8fcdbec0a635')
	kik.set_configuration(Configuration(webhook='http://c1d01f00.ngrok.io{0}'.format(webhook)))
	return kik
	
	
#The message response was in the form of JSON Data
def filter_messages(messages):
	for message in messages:
		message = request.json['messages'][0]
		if 'body' in message:
			#Call the message method
			message_handle(message['from'],message['chatId'],message['body'])
			return message['from'],message['chatId'],message['body']
		else:
			send_message(message['from'],message['chatId'],'Please enter a command, Type !Menu to recieve a list of commands!')
			
	
def message_handle(user,chat_id,body):
	if body == 'help' or body == '!Menu':
		send_message(user,chat_id,''.join(cmds))
	elif body in cmds:
		kik = main_init(body)
		return send_message(user,chat_id,body)
	
@app.route('/index',methods=['POST'])
def show_menu():
	#Assuming the func = main_init;
	#Handle the message here first	
	messages = messages_from_json(request.json['messages'])
	filter_messages(messages)
	return 'ok'
	
@app.route('/text',methods=['POST'])
def text_to_image():
	messages = messages_from_json(request.json['messages'])
	from_user,chat_id,body = filter_messages(messages)
	send_message(from_user,chat_id,'will return {0} as a picture soon!'.format(body))
	url = textFunction(body)
	pic = str(scrapeImage(url))
	send_pic_message(from_user,chat_id,random.choice(pic))
	return 'ok'
	
	 
def send_message(user,chatId,body):
	kik.send_messages([
		TextMessage(
			to=user,
			chat_id=chatId,
			body=body
		)
	])
	
def send_pic_message(user,chatId,picLink):
	kik.send_messages([
		PictureMessage(
			to=user,
			chat_id=chatId,
			pic_url=picLink	
		)
	
	])



#Down here will be the main loop of the app

#Set the webhook here


#Init set to index
kik = main_init('/index')
while True:
	app.run(port=8080,debug=True)