from github import Github
import base64
import requests # see https://2.python-requests.org/en/master/
  
#g = Github("tvliveapp@protonmail.ch", "tvliveapp@protonmail.ch")
g = Github("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")
repo = g.get_user().get_repo("listasIptv")







def commit(val,f=''):
	
	repo.update_file(contents.path, "lio", val, contents.sha)
def commitContent(val,f=''):
	contents = repo.get_contents(f)
	repo.update_file(contents.path, "lio", val, contents.sha)
def readContent(f=''):
	contents = repo.get_contents(f)
	return base64.b64decode(contents.content).decode("UTF-8")
def createFile(name,val):
    try:
        
        repo.create_file(name, "init commit", val)
        data = {
        "url": "https://raw.githubusercontent.com/tvliveapp/listasIptv/main/"+name
        }
 
        login = requests.post("https://git.io/create", data=data)
        print("Login status: ", login.status_code if login.status_code != 200 else "OK/200")

        return "https://git.io/"+login.text
    except:
        return "error"
def updateIps(ip):
	ips=readContent("ips.json")
	print(ips)
	ips=ips+"\n"+ip
	commitContent(ips,'ips.json')

