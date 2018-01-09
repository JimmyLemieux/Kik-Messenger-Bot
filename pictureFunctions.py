from flask import Flask,request
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage,PictureMessage
import json
from selenium import webdriver #This is the exe that will run the chrome ext
from selenium.webdriver.common.keys import Keys #This allows for auto input
from bs4 import BeautifulSoup
import time
import urllib
import random


errorImage = 'https://cdn.pixabay.com/photo/2016/10/18/18/19/question-mark-1750942_960_720.png'

def textFunction(bodyText):
	#Here we are going to do something cool with binary
	#This is just for now
	url = 'https://pixabay.com/en/photos/?hp=&image_type=&cat=&min_width=&min_height=&q={0}&order=popular'.format(bodyText)
	return url
	


	


def scrapeImage(url):
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
			if img != None:
				if 'gif' not in img['src']:imageList.append(str(img['src']))
	
	return imageList
	


