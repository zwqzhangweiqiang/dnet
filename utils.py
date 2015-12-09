from eventlet.green import subprocess
import os
import time

def login(logname):
	try:

		if not os.path.isfile("./dnet.log"):
			os.system("touch ./dnet.log")	
		f=open("./dnet.log",'a')
		f.write(logname+"\n")
		f.close()
	except:
		return "filed file"
def execute(*cmd):
	try:
		obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		result=obj.communicate()
		logtime=time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
		logname=logtime+".....>  exec command '"+cmd[0]+"'  result is  sucess"
		login(logname)
		return True
	except:
		logtime=time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
		logname=logtime+".....>  exec command '"+cmd[0]+"' is filed"
		login(logname)
		return False
