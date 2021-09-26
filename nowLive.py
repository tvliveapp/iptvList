
import requests
from bs4 import BeautifulSoup   
import json
from requests.structures import CaseInsensitiveDict
import json
import re
from urllib.parse import unquote
'''                          urls={
	'cat_id': "1"...
	'cat_name': "Entertainment"...
	'channel_name': "20 Mediaset"...
	'country': "IT"...
	'img': ""...
	'link_to_play': "0"...
	'pk_id': "795"
} 
''' 
urls={'5':'http://cablehd.online/catogoria/deportes/','1':'http://cablehd.online/catogoria/series','6':'http://cablehd.online/catogoria/documentales/','7':'http://cablehd.online/catogoria/infantil/','2':'http://cablehd.online/catogoria/peliculas/'} 
catId={'1':"Entertainment",'5':"Sports",'6':'Documentary','7':'Kids','2':'Movies'}  
url='http://nowlive.pro/'
#soup = BeautifulSoup(requests.get("http://cablehd.online/catogoria/deportes/").content)
epgDel='-------------------------------------------------------------------------------'
epgIni='"gold">'
epgEnd='</p>'
epg={}
def getEpg():
	try:
		req = requests.get(url)

		#response = req.text
		print(response)
		n=0
		for line in (str(response).split(epgDel)[1:-1]):
			n=n+1
			epg['Channel '+str(n)]=[]
			evs=(re.findall('"gold">(.*?)</p>',line))
			for ev in evs:
				ev=ev.split('-')
				if len(ev)>1:
					#print(ev)
					epg['Channel '+str(n)].append('|'.join(ev))
			#print(line[line.find(epgIni):line.find(epgEnd)])
	except:
		pass
	return(epg)

def getChannels():
	links=[]
	getEpg()
	if 1:
		req = requests.get(url)
		response = req.text
		try:
			result=str(response)
		
		except:
		
			result=response.read()
		#print(result)
		soup = BeautifulSoup(result)
		
		for link in soup.find_all("center"):
		#for link in soup.find_all("center", {"class": "card"}):
		#cchName=link.
			#cName=link.a.decode_contents().encode('ascii','ignore'))
			try:
				#print(link.a.get('href'))
				#print(link.a)#print(link['a']['href'])
			
				name=link.a.decode_contents()
				link_to_play=getStreamLink('http://nowlive.pro'+link.a.get('href'))
				links.append({'link_to_play':link_to_play,
				'cat_id':'6',
				'cat_name':'Sports',
				'channel_name':name,
				'country': "INT",
				'epg':epg[name],
				'img':'sport.jpg'
			
			})
			except:
				print('nop')
				pass
	return links

my_referer='http://latino-webtv.com/fox-sports-2-en-vivo'

 #
    # NowLive support
    #
def getStreamLink(referUrl):
        #
        # Global variables
        #
        USER_AGENT = "Mozilla/5.0 (X11 Linux i686 rv:41.0) Gecko/20100101 Firefox/41.0 Iceweasel/41.0.2"
        videoContentId=str(referUrl.split('/')[-1].split('.')[0])
        url="http://nowlive.pro/1/" + videoContentId + ".html?id=" + videoContentId + videoContentId
        if 1:#try:
            # Get the decodeURL
            print ("VideoContent id: " + videoContentId)
            #("URL: " + referUrl + " --> " + unquote(referUrl))
            
            req = requests.get(url)
            response = req.text
            #html = getRequest("http://nowlive.pro/1/" + videoContentId + ".html?id=" + videoContentId + videoContentId, unquote(referUrl), USER_AGENT)
            html=str(response)
            
            m = re.compile('application\/x-mpegurl.*\/\/(.*?)m3u8').search(html)
            decodedURL ="http://"+ m.group(1)+"m3u8"
            #print ("decodedURL: " + decodedURL)
                        
            # Parse the final URL
            #u = "http://" + decodedURL + "m3u8" + "|Referer=" + unquote(referUrl) + "&User-Agent=" + USER_AGENT
            print ("Final URL: " + decodedURL)
            return unquote(decodedURL)
        #except:
            pass 

 #
    # NowLive support
  

  #

def updateList():
	canales=getChannels()
	playLits=open('templates/listas/evd2.m3u','w')
	#playLits.write('#EXTM3U\n')
	for canal in canales:
		for even in canal['epg']:
			playLits.write('#EXTINF:-1 group-title="nowLive: solo durante eventos"'+','+even+'\n')
			playLits.write(canal['link_to_play']+'\n')
		print(canal)
		print()
	playLits.close()
updateList()
#print(getStreamLink('http://nowlive.pro/1/101.html'))
'''
  def getStreamLink (videoContentId):
        #
        # Global variables
        #
        USER_AGENT = "Mozilla/5.0 (X11 Linux i686 rv:41.0) Gecko/20100101 Firefox/41.0 Iceweasel/41.0.2"

        try:
            # Get the decodeURL
            print ("VideoContent id: " + videoContentId)
            #("URL: " + referUrl + " --> " + unquote(referUrl))
            html = self.getRequest("http://nowlive.pro" + videoContentId + ".html?id=" + videoContentId + videoContentId, unquote(referUrl), USER_AGENT)
            m = re.compile('application\/x-mpegurl.*\/\/(.*?)m3u8').search(html)
            decodedURL = m.group(1)
            print ("decodedURL: " + decodedURL)
                        
            # Parse the final URL
            u = "http://" + decodedURL + "m3u8" + "|Referer=" + unquote(referUrl) + "&User-Agent=" + USER_AGENT
            print ("Final URL: " + u)
            return u
        except:
            pass
'''
'''	
url='http://nowlive.pro/1/102.html?id=102'
url='https://premium.limpi.tv/embed.js'

rapid='http://www.rapifutbol.tv/Insert.jsf?id=736'
f=open('leo.html','w')
f.write(json.dumps(getStreamLink('http://cablehd.online/fox-sports-2-en-vivo/'), ensure_ascii=True))
f.close()	
'''
#print(getNowLive('http://nowlive.pro/1/102.html'))

'''
#soup.findAll("div", {"class": "stylelistrow"})
f=open('leo.txt','w')
f.write(str(soup.find_all("a", {"class": "card"})))
f.close()
links=[]
startN='title="'
endN='"'
for link in soup.find_all("a", {"class": "card"}):
    #cchName=link.
	print link['href']

'''
