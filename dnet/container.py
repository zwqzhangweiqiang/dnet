import docker
from configobj import ConfigObj
import network
import utils
import time
import os

class dockerapi(object):
	def __init__(self,url):
		self.connection=docker.Client(base_url=url)
		if os.path.isdir("/etc/config"):
			pass
		else:
			utils.execute("mkdir /etc/config")
		self.path="/etc/config/"
		self.net=network.network()
	
	def get_config(self,Id):
		file=self.path+Id
		if os.path.isfile(file):
			config=ConfigObj(file,encoding="UTF8")
			return config["container"]
		else:
			return False

	def input_file(self,Id,Pid,ipaddress,name,hostname,bridgename,gateway,netname):
		file=self.path+Id[0:12]
		config=ConfigObj(file,encoding="UTF8")
		config["container"]={}
		config["container"]["id"]=Id
		config["container"]["Pid"]=Pid
		config["container"]["address"]=ipaddress
		config["container"]["name"]=name
		config["container"]["hostname"]=hostname
		config["container"]["bridgename"]=bridgename
		config["container"]["gateway"]=gateway
		config["container"]["netname"]=netname
		config.write()	

	def update_file(self,Id,pid):
		file=self.path+Id
		config=ConfigObj(file,encoding="UTF8")
		config["container"]["Pid"]=pid
		config.write()

	def create(self,image,hostname,name,bridge,netname,gateway):
		result=self.connection.create_container(image=image,network_disabled=True,stdin_open=True,tty=True,hostname=hostname,name=name)
		Id=result['Id'][0:12]
		self.start_container(name=name)
		Pid=self.get_pid(name=name)
		ipaddress=self.net.get_ip(netname)
		bridgename=self.net.create_bridge(bridge)
		self.net.contain_net(Id,Pid,bridge,ipaddress,gateway)
		self.input_file(Id,Pid,ipaddress,name,hostname,bridge,gateway,netname)

	def start_container(self,name):
		result=self.connection.start(container=name)
		return result

	def get_pid(self,name):
		result=self.connection.inspect_container(container=name)
		return result['State']['Pid']

	def nstop_container(self,name):
		result=self.connection.inspect_container(container=name)
		if result["State"]["Running"]:
			self.connection.stop(container=name)
			self.net.delete_net(result['Id'][0:12])
			return "ok"
		else:
			return "stopping"
	def nstart_container(self,name):
		result=self.connection.inspect_container(container=name)
		if result["State"]["Running"]:
			return "running"
		else:
			Id=result['Id'][0:12]
			file=self.path+Id
			configfile=ConfigObj(file,encoding="UTF8")
			config=configfile["container"]
			self.connection.start(container=name)
			Pid=self.get_pid(name=name)
			self.net.contain_net(config["id"],Pid,config["bridgename"],config["address"],config["gateway"])
			self.update_file(Id,Pid)
			return "ok"
		
	def delete_container(self,name):
		result=self.connection.inspect_container(container=name)
		if result["State"]["Running"]:
			self.nstop_container(name)
			self.connection.remove_container(container=name)
			config=self.get_config(result['Id'][0:12])
			ipaddress=config["address"]
			netname=config["netname"]
			filepath=self.path
			utils.execute("rm -f %s%s" % (filepath,result['Id'][0:12]))
			utils.execute("touch %s/%s" % (netname,ipaddress))
		else:
			self.connection.remove_container(container=name)
			config=self.get_config(result['Id'][0:12])
			if  config is False:
				pass
			else:
				ipaddress=config["address"]
				netname=config["netname"]
				filepath=self.path
				Id=config["id"]
				self.net.delete_net(Id)
				utils.execute("rm -f %s%s" % (filepath,result['Id'][0:12]))
				utils.execute("touch %s/%s" % (netname,ipaddress))
			
	def list_container(self):
		result=self.connection.containers(all=True)
		list=[]
		for i in result:
			Id=i['Id'][0:12]
			Status=i['Status'].split()[0]
			config=self.get_config(Id)
			if config:
				config['Status']=Status.encode('UTF-8')
				list.append(config)
			else:
				pass
		return list
	

	def commit_container(self,name,repository,tag):
		if name:
			self.connection.commit(container=name,repository=repository,tag=tag)
		else:
			return "please choice a container"

	
