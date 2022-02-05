from requests_html import HTMLSession
session = HTMLSession()
r = session.get('https://futbollibre.net/agenda/?update2')
wraper=r.html.find('#wraper')
li=wraper[0].find('li')

print(li[0])
print()
print()
eventos={}
urls=[]
ceven=''
for l in li:
	if(l.attrs['class'][0]=='subitem1'):
			#print(l)
			ev=l.find('a')
			links=list(ev[-1].absolute_links)[-1]
			
			urls.append(links)
			eventos[ceven]=urls
			pass
	else:
		ev=l.find('a')
		#print('ev')
		#print(ev[0].text)		
		ceven=ev[0].text
		ev=l.find('span')
		#print(ev[0].text)
		urls=[]

lista=open('/templates/listasftlb.m3u','w')

def getUrl(url):
	session = HTMLSession()
	r = session.get(url)
	a=r.html.find('a')
	m3us=[]
	for al in a:
		try:
			l=list(al.absolute_links)[-1]
			if l.find('.m3u')>0:
				m3us.append(l)
		except:
			pass
	return m3us


for eve in eventos.keys():
	#print (eventos[eve])
	for url in eventos[eve]:
		if url.find('.m3u')>0:
			lista.write('#EXTINF:-1 group-title="futbol libre",'+eve+'\n')
			lista.write(url+'\n')
			
		else:
			for ul in getUrl(url):
				lista.write('#EXTINF:-1 group-title="futbol libre",'+eve+'\n')
				lista.write(ul+'\n')
			 
			print()
lista.close()
'''	
	try:
		ev=l.find('a')
		#print(ev)
		links=list(ev[1].absolute_links)
		print(links)
		for link in links:
			if(link.find('.m3u')>0):
				print(ev[0].text,link)
			

	except:
		pass

#print(li[0].find('a'))

'''
