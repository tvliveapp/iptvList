# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup   
import json
from requests.structures import CaseInsensitiveDict
import re
headers = CaseInsensitiveDict()
headers["Referer"] = "http://apk.radiotormentamx.com/"
'''
http://iptvhd.club/aptv/vip/cablehd.php?id=2_
http://aptv.radiotormentamx.com/aptv/vip/cablehd.php?id='+fid+'_#
http://apk.radiotormentamx.com/latino.html
http://apk.radiotormentamx.com/
http://iptvhd.club/apstream/vip/cablehd.php?id=635_
'''
urlList={'mexico':{'url':'http://apk.radiotormentamx.com/mexico.html','div':'imObjectGallery_333_1400'},'latino':{'url':'http://apk.radiotormentamx.com/latino.html','div':'imObjectGallery_178_01'},'premium':{'url':'http://apk.radiotormentamx.com/premium.html','div':'imObjectGallery_322_1789'},'kids':{'url':'http://apk.radiotormentamx.com/kids.html','div':'imObjectGallery_477_1789'}}
baseUrl='http://apk.radiotormentamx.com/'
channels={}
url="https://raw.githubusercontent.com/tvliveapp/channels/master/aptv.json"
tk='lld9yN7t6J'
def updateChns():
    global tk
    try:
    #if 1:
        finalUrl="http://iptvhd.club/apstream/vip/cablehd.php?id=609_#"
        print('tk',tk)
        #print(finalUrl)
        r = requests.get(finalUrl,headers=headers)
        a=r.content.decode('latin-1')
        a=a.replace('==','!=',1)
        #print(a)
        a=a.split('Clappr.Player(')[1]
        b=a.split('{')[1]
        b=b.split('\'')[1]
        print('new url',b)
        newTk = re.search('token=(.*)&', b)
        #newTk=b.split("/live/aptvall/")[1].split('/')[0]
        newTk=newTk.group(1)
        print (tk,newTk)
        if 0:#newTk==tk:
            pass
        else:
            f=open('templates/listas/leoList.m3u','r')
            nLst=f.read()
            f.close()
            #nLst=nLst.replace(tk,newTk)
            nLst=re.sub('token=.*?&','token='+newTk+'&',nLst, flags=re.DOTALL)
            tk=newTk
            #print(nLst)
            f=open('templates/listas/leoList.m3u','w')
            f.write(nLst)
            f.close()
            
    except:
        pass
updateChns()     
def getUrl(url):
    #print(url)
    resp = requests.get(url)
    try:
        id=resp.text.split("fid='")[1].split("'")[0]
        
        finalUrl="http://iptvhd.club/apstream/vip/cablehd.php?id="+id+'_#'
        #print(finalUrl)
        r = requests.get(finalUrl,headers=headers)
        a=r.content.decode('latin-1')
        a=a.replace('==','!=',1)
        a=a.split('Clappr.Player(')[1]
        b=a.split('{')[1]
        b=b.split('\'')[1]
        #print (b)
        return b
    except:
        b=resp.text.split('new Clappr.Player')[1].split('source:')[1].split(',')[0]
        #print(b)
        return b

def getChannels():
    global channels
    canales=[]
    leolist=open('templates/listas/leoList.m3u','w')
    leolist.write('#EXTM3U\n')
    for grupo in urlList:
        cUrl=urlList[grupo]['url']
        #resp = requests.get('http://apk.radiotormentamx.com/latino.html')

        resp = requests.get(cUrl)
        
        #print(resp.text)
        soup = BeautifulSoup(resp.text)
    
        #print(soup.find("div", {"id": "imObjectGallery_178_01"}).find_all('a'))
        #ass=soup.find("div", {"id": "imObjectGallery_178_01"}).find_all('a')
        cId=urlList[grupo]['div']
        ass=soup.find("div", {"id": cId}).find_all('a')
        
        
        for a in ass:
            try:
                canales.append('http://apk.radiotormentamx.com/'+a['href'])
                chName=a['href'].split('.')
                chUrl=getUrl(canales[-1])
                print(chName[0],chUrl.replace('"',''))
                leolist.write('#EXTINF:-1 group-title="'+ grupo+'",'+chName[0]+'\n')
                leolist.write(chUrl.replace('"','')+'\n')
            except:
                print('error')
    
    leolist.close()
    channels['latino']=canales   
        #print(channels)

def iptvhdFcn(id):
    print('id',id,channels[id]["srclink"])
    if channels[id]["srclink"]== "iptvhd":
        headers = CaseInsensitiveDict()
        r = requests.get(channels[id]['stream_link'])
        print(r.status_code)
        a=r.content.decode('latin-1')
        a=a.replace('==','!=',1)
        a=a.split('Clappr.Player(')[1]
        b=a.split('{')[1]
        b=b.split('\'')[1]
        print (b)
        return b
    else:
        return channels[id]['stream_link']
    
#print(iptvhdFcn('aptv11'))
getChannels()
