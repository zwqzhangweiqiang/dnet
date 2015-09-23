import docker
from configobj import ConfigObj
import network
import utils
import time
import os

class dockerapi(object):
	def __init__(self,url):
		self.connection=docker.Client(base_url=url)
		self.path="config/"
		self.net=network.network()
	
	def get_config(self,Id):
		file=self.path+Id
		if os.path.isfile(file):
			config=ConfigObj(file,encoding="UTF8")
			return config["container"]
		else:
			return False

	def input_file(self,Id,Pid,address,name,hostname,bridgename,gateway,netname):
		file=self.path+Id[0:12]
		config=ConfigObj(file,encoding="UTF8")
		config["container"]={}
		config["container"]["id"]=Id
		config["container"]["Pid"]=Pid
		config["container"]["address"]=address
		config["container"]["name"]=name
		config["container"]["hostname"]=hostname
		config["container"]["bridgename"]=bridgename
		config["container"]["gateway"]=gateway
		config["container"]["netname"]=netname
		config.write()	

	def update_file(self,Id,pid):
		file=self.path+Id
		config=ConfigObj(file,encoding="UTF8")
		config["Id"]["Pid"]=pid
		config.write()

	def create(self,image,hostname,name,bridge,netname,gateway):
		result=self.connection.create_container(image=image,network_disabled=True,stdin_open=True,tty=True,hostname=hostname,name=name)
		Id=result['Id'][0:12]
		self.start_container(name=name)
		Pid=self.get_pid(name=name)
		ipaddress=self.net.get_ip(netname)
		bridgename=self.net.create_bridge(bridge)
		self.net.contain_net(Id,Pid,bridgename,ipaddress,gateway)
		self.input_file(Id,Pid,ipaddress,name,hostname,bridgename,gateway,netname)

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
		else:
			return "container "+name+" is stoped"
	def nstart_container(self,name):
		reult=self.connection.inspect_container(container=name)
		if not result["State"]["Running"]:
			Id=result['Id'][0:12]
			file=self.path+Id[0:12]
			configfile=ConfigObj(file,encoding="UTF8")
			config=configfile["container"]
			self.connection.start(container=name)
			self.net.contain_net(config["Id"],config["Pid"],config["bridgename"],config["address"],config["gateway"])
			Pid=self.get_pid(name=name)
			self.update_file(Id,Pid)
		else:
			return "container "+name+" is started"

		
	def delete_container(self,name):
		result=self.connection.inspect_container(container=name)
		if result["State"]["Running"]:
			self.nstop_container(name)
			time.sleep(3)
			self.connection.remove_container(container=name)
			config=self.get_config(result['Id'][0:12])
			ipaddress=config["ipaddress"]
			netname=config["netname"]
			utils.execute("rm -f config/%s" % (result['Id'][0:12]))
			utils.execute("touch %s/%s" % (netname,ipaddress))
		else:
			self.connection.remove_container(container=name)
			self.net.delete_net(result['Id'][0:12])
			config=self.get_config(result['Id'][0:12])
			if  config is False:
				pass
			else:
				ipaddress=config["address"]
				netname=config["netname"]
				utils.execute("rm -f config/%s" % (result['Id'][0:12]))
				utils.execute("touch %s/%s" % (netname,ipaddress))
			
	def commit_container(self,name,repository,tag):
		if name:
			self.connection.commit(container=name,repository=repository,tag=tag)
		else:
			return "please choice a container"

	
