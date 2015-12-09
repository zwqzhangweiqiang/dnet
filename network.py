import utils
from configobj import ConfigObj
import os
import netaddr

class network(object):
	def __init__(self):
		self.path="/etc/network/"

	def input_file(self,name):
		file=self.path+"networklist"
		config=ConfigObj(file,encoding="UTF8")
		config['networklist']=[]
		config['networklist'].append(name)
		config.write()
		

	def create_network(self,name,cidr):
		path=self.path+name
		if name:
			if os.path.isdir(path):
				return name+"  is exist"
			else:
				os.system("mkdir -p %s" % path)
		cc=str(netaddr.IPNetwork(cidr)).split('/')[0]
		for i in netaddr.IPNetwork(cidr):
			utils.execute("touch %s/%s" % (path,i))
			utils.execute("rm -f %s/%s" % (path,cc))
		network={}
		network[name]=cidr
		self.input_file(network)	
		
	def list_network(self):
		file=self.path+"networklist"
		config=ConfigObj(file,encoding="UTF8")
		return config['networklist']	

	def get_ip(self,name):
		files = os.listdir(name)
		ip=files.pop(0)
		utils.execute("rm -f %s/%s" % (name,ip))
		return ip		

	def create_bridge(self,bridgename):
		if bridgename:
			if os.path.isdir("/sys/class/net/%s/bridge" % bridgename):
				pass
			else:
				utils.execute("brctl addbr %s" % bridgename)
				utils.execute("ip link set %s up" % bridgename)
				utils.execute("brctl addif %s eth1" % bridgename)
				return bridgename
	

	def contain_net(self,Id,Pid,bridgename,ipaddress,gateway):
		if Id:
			utils.execute("ip link add name %s type veth peer name %s" %("t-"+Id,"p-"+Id))
		utils.execute("ip link set %s up" % ("t-"+Id))
		utils.execute("ip link set %s up" % ("p-"+Id))
		utils.execute("brctl addif %s %s" % (bridgename,"t-"+Id))
		if os.path.isdir("/var/run/netns"):
			pass
		else:
			utils.execute("mkdir /var/run/netns")
		utils.execute("ln -s /proc/%s/ns/net /var/run/netns/%s" %(Pid,"nets-"+Id))
		utils.execute("ip link set %s netns %s" %("p-"+Id,"nets-"+Id))
		utils.execute("ip netns exec %s  ip link set %s name eth0" %("nets-"+Id,"p-"+Id))
		utils.execute("ip netns exec %s ip link set eth0  up" % ("nets-"+Id))
		utils.execute("ip netns exec %s  ip addr add  %s/24 dev eth0" % ("nets-"+Id,ipaddress))
		utils.execute("ip netns exec %s ip route add 0.0.0.0/0 via %s dev eth0" % ("nets-"+Id,gateway))
		utils.execute("ip link set lo up")
	
	def delete_net(self,Id):
		if Id:
			utils.execute("rm -f /var/run/netns/%s" % ("nets-"+Id))
		if os.path.isdir("/sys/class/net/%s" % ("t-"+Id)):
			utils.execute("ip link del %s" % ("t-"+Id))
		else:
			pass
