
from flask import Flask, render_template, request
import nowLive
#import iptvhdFcn
#import model
import json
import base64
from urllib.parse import unquote
import importlib
import time
import os
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port

listadecanales=''
def readList():
	global listadecanales
	nowLive.updateList()
	data=open('templates/info.m3u')
	listadecanales=data.read()
	data.close()
	for lista in os.listdir('templates/listas'):
		data=open('templates/listas/'+lista,encoding="utf8")
		listadecanales=listadecanales+'\n'+data.read()
		data.close()
	print (listadecanales)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route("/")
def root():
	return render_template("index.html")

@app.route("/index")
def index():
	return render_template("index.html")

listaUsuarios=[]
@app.route("/listaiptv")
def listaiptv():
	global lasUpdate
	try:
		print( ip_address = request.headers['X-Forwarded-For'])
	except:
		pass
	if time.time()-lasUpdate>18000:
		nowLive.updateList()
		#iptvhdFcn.getChannels()
		lasUpdate=time.time()
		readList()
	return listadecanales
readList()
lasUpdate=time.time()
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=PORT_NUMBER,debug = True)

