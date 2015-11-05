from bottle import route, run,request
import images
import container
import network

ContainerApi=container.dockerapi(url="tcp://0.0.0.0:2375")
NetworkApi=network.network()

#create container
@route("/create",method="POST")

def create():
	body = request.json
	image=body.get("image")
	hostname=body.get("hostname")
	name=body.get("name")
	bridge=body.get("bridge")
	netname=body.get("netname")
	gateway=body.get("gateway")
	ContainerApi.create(image,hostname,name,bridge,netname,gateway)
	return {"name":name,
		"hostname":hostname,
		"image":image,
		"netname":netname,
		"bridge":bridge,
		"gateway":gateway
		}

#delete container
@route("/delete/<ContainName>",method="DELETE")

def delete(ContainName):
	ContainerApi.delete_container(ContainName)
	return {"result":"sucess!"}


#start container
@route("/start/<ContainName>",method="POST")

def start(ContainName):
	result=ContainerApi.nstart_container(ContainName)
	if result=="running":
		return {"result":ContainName+" is running"}
	elif result=="ok":
		return {"result":ContainName+" is started"}


#stop container
@route("/stop/<ContainName>",method="POST")

def stop(ContainName):
	result=ContainerApi.nstop_container(ContainName)
	if result=="ok":
		return {"result":ContainName+" is stoped"}
	elif result=="stopping":
		return {"result":ContainName+" is stopping"}


#list containers
@route("/list/container",method="GET")

def list_container():
	result=ContainerApi.list_container()
	return {"lists":result}


#create network
@route("/network/create",method="POST")

def network_create():
	body = request.json
	NetName=body.get("name")
	cidr=body.get("cidr")
	NetworkApi.create_network(NetName,cidr)
	return {"result":"sucess",
		"NetName":NetName,
		"cidr":cidr
		}



run(host="0.0.0.0",port="8000")
	
