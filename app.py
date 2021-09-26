
from flask import Flask, render_template, request
import nowLive
import todosFcn
#import iptvhdFcn
#import model
import json
import base64
from urllib.parse import unquote
import importlib
import time
import os
from collections import deque
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port


listadecanales=''
todosChn=''
catsDir='templates/listas/'
infoDir='templates/info.m3u'
def readCats(cats):
	miLista=''
	f=open('templates/info.m3u')
	miLista=f.read()+'\n'
	f.close()
	for cat in cats:
		try:
			#print(cat,flush=True)
			f=open(catsDir+cat+'.m3u',encoding="utf8",errors='ignore')
			miLista=miLista+f.read()+'\n'
			f.close()
		except:
			pass
	return miLista	

def readList():
	global listadecanales, todosChn
	nowLive.updateList()
	data=open('templates/info.m3u')
	listadecanales=data.read()
	data.close()
	for lista in os.listdir('templates/listas'):
		data=open('templates/listas/'+lista,encoding="utf8")
		listadecanales=listadecanales+'\n'+data.read()
		data.close()
	#print (listadecanales)
	todosChn=todosFcn.getTodos()
def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route("/")
def root():
	return render_template("test.html")

@app.route("/index")
def index():
	return render_template("test.html")

@app.route("/todos")
def todos():
	global todosChn
	return json.dumps(todosChn)


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
@app.route("/listaiptv.m3u")
def listaiptvm3u():
	global lasUpdate
	cats = request.args.get('cats', default = '', type = str)
	sr=request.args.get('sr', default = 0, type = int)
	r=int(sr/5)
	cates=Convert(cats)
	items = deque(cates)
	items.rotate(r)
	print(r,flush=True)
	cate=''.join(items)
	cate=cate.split(',')
	print(cate,flush=True)
	try:
		print( ip_address = request.headers['X-Forwarded-For'])
	except:
		pass
	if time.time()-lasUpdate>18000:
		nowLive.updateList()
		#iptvhdFcn.getChannels()
		lasUpdate=time.time()
		readList()
	if cate:
		return readCats(cate)
	else:
		return listadecanales
readList()
lasUpdate=time.time()
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=PORT_NUMBER,debug = True)

