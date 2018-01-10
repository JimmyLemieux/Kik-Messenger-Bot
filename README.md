# Kik-Messenger-Bot
This lightweight bot uses the Kik API to access the webhook capabilites that are available to return json API responses.
  -> An application called 'ngrok' was used in order to tunnel the webhook to the localhost of your computer:
   -> ngrok tunnel session:
  ![ngrok tunnel session](https://i.gyazo.com/b9273fadc572c414ebddea7df9cadb2b.png)
 # Main Bot Init
 ```Python
  def main_init(webhook):
	#This is where I will change the webhook to allow for the decorator of user commands
	kik = KikApi('jarvisentail','7a88d75b-076c-448e-b5f3-8fcdbec0a635')	#(botname,apikey)
	# kik.set_configuration(Configuration(webhook='http://73cf662a.ngrok.io{0}'.format(webhook))) #includes the ngrok tunnel to the localhost
	return kik
  ```
  -> The Kik API returned JSON data as the response of the information that was sent to the bot. The json data is sent to a message handling function which determines what will be done with the inputted text
  ```python
  The message response was in the form of JSON Data
def filter_messages(messages):
	for message in messages:
		message = request.json['messages'][0]
		if 'body' in message:
			#Call the message method
			message_handle(message['from'],message['chatId'],message['body'])
			return message['from'],message['chatId'],message['body']
		else:
			send_message(message['from'],message['chatId'],'Please enter a command, Type !Menu to recieve a list of commands!')
  ```
  NOTE: All feedback is sent back to the user who is interacting with the bot
  # Application Routing
  An powerful feature which the Flask library offers is for certain commands to take place when a specific webhook is in place.
    -> For example, if the user where to enter a command in the form !text for example. The webhook will be changed from (ngrokhost/index) -> (ngrokhost/text)
    -> the @app.route decorator handles these types of situations with ease
   
  ```python
@app.route('/text',methods=['POST'])
def text_to_image():
	messages = messages_from_json(request.json['messages'])
	from_user,chat_id,body = filter_messages(messages)
	send_message(from_user,chat_id,'will return {0} as a picture soon!'.format(body))
	url = textFunction(body)
	pic = str(scrapeImage(url))
	send_pic_message(from_user,chat_id,random.choice(pic))
	return 'ok'
  ```
  *When conncetions are made in the network, the Flask application and ngrok show post status and activity:*
  ![ngrok_session](https://i.gyazo.com/d4d30a93dc8791a6e1d9c1ac5adc2e16.png)
  ![flask_session](https://i.gyazo.com/abcbaa80d2047e86d3d16364c9440fa5.png)
  
  # Working Application
   -> Currently the bot is able to convert text to an image. For example, if the user were to input the text cow. The bot would access a link to the free pixabay website and webcrawl the page of images to find the best matching image for the given text.
   ```python
  def scrapeImage(url):		#The beautifulsoup framework is to make the html response more clean and beautiful
	  imageList = []
	  #Get the html first from urlopen
	  url = urllib.urlopen(url,'utf-8')
	  #This gets the url contents.
	  soup = BeautifulSoup(url,'html.parser') #Use beautifulsoup here
	  imageDiv = soup.find_all('div',{'class':'item'})
	  for div in imageDiv:
		  children = div.findChildren()
		  #Loop children
		  for child in children:
			  img = child.find('img')
			    if img != None: # The source image will give us the direct link to the image that can be sent on kik
				    if 'gif' not in img['src']:imageList.append(str(img['src']))	
	
	return imageList
   ```
   # Limitaions
    -> I never got around to implementing text machine learning that would understand a users emotion based on word choice and sentance structure
    -> The joke mode was never implemented
    -> The weather mode was nver implemented
    -> Some errors occur with the kik api which include not always returning a proper response
