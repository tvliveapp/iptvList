import os
baseDir='templates/listas/'
todos={}
def getTodos():
	for cat in os.listdir(baseDir):
		todos[cat.replace('.m3u','')]=[]
		f=open(baseDir+cat,encoding="utf8",errors='ignore')
		for line in f.readlines():
			try:
				ch=line.split(',')[1].replace('\n','')
				todos[cat.replace('.m3u','')].append(ch)
			except:
				pass
	#print(todos[cat])
	return todos
print(getTodos())