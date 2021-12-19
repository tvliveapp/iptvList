
from flask import Flask, render_template, request
#import nowLive
import todosFcn
import iptvhdFcn
#import model
import json
import base64
from urllib.parse import unquote
import importlib
import time
import os
#import pastebin
from collections import deque
#import myGit
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
	#nowLive.updateList()
	#iptvhdFcn.updateChns()
	data=open('templates/info.m3u')
	listadecanales=data.read()
	data.close()
	for lista in os.listdir('templates/listas'):
		data=open('templates/listas/'+lista,encoding="utf8",errors='ignore')
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

@app.route("/crear")
def crear():
	return render_template("crearlista.html")


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
	readList()
	print('update',time.time()-lasUpdate)
	if time.time()-lasUpdate>7200:
		#nowLive.updateList()
		lasUpdate=time.time()
		iptvhdFcn.getChannels()
		
		readList()
	return listadecanales
@app.route("/listaiptv.m3u")
def listaiptvm3u():
	global lasUpdate
	cats = request.args.get('cats', default = 'all', type = str)
	sr=request.args.get('sr', default = 0, type = int)
	r=int(sr/5)
	cates=Convert(cats)
	items = deque(cates)
	items.rotate(r)
	print(r,flush=True)
	cate=''.join(items)
	cate=cate.split(',')
	print('cate',cate,flush=True)
	readList()
	try:
		print( ip_address = request.headers['X-Forwarded-For'])
	except:
		pass
	if time.time()-lasUpdate>7200:
		lasUpdate=time.time()
		#nowLive.updateList()
		iptvhdFcn.getChannels()
		lasUpdate=time.time()
		readList()
	if cate[0]=='all':
		print('todas')
		readList()
		return listadecanales
	else:
		print('categorias')
		return readCats(cate)
@app.route("/leo")
def leo():
	return render_template("/listas/leoList.m3u")	
		
@app.route("/paste")
def paste():
    name = request.args.get('name', default = 'newList', type = str)
    lista=request.args.get('list', default = "", type = str)
    print(name)
    base64_bytes = lista.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    resp="none"
    '''
    pastebin.data['api_paste_code']=message
    pastebin.data['api_paste_name']=name
    #     resp=pastebin.pasteBin(pastebin.data)
    '''
    #resp=myGit.createFile(str(time.time()),message)
    print (resp)
    return resp
    
readList()
lasUpdate=time.time()
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=PORT_NUMBER,debug = False)

