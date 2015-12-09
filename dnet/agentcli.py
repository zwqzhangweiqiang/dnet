import requests
import argparse
import sys
import os
import json
import re


BASE_URL="http://0.0.0.0:8000"
HEADERS = {'content-type': 'application/json'}
FUNC_MAPPER = {}

def cmd(cmd, args=[], opt_args=[]):
	FUNC_MAPPER[cmd] = {"args": args,"opt_args": opt_args}
	def deco(func):
		FUNC_MAPPER[cmd]["func"] = func
		FUNC_MAPPER[cmd]["description"] = func.__doc__
		def wrapper():
			pass
		return wrapper
	return deco


@cmd("container_create",args=[],opt_args=["image","hostname","name","bridge","netname","gateway"])
def container_create(argv):
	body = dict()
	if (argv.image):
		body["image"]=argv.image
	if(argv.hostname):
		body["hostname"]=argv.hostname
	if(argv.name):
		body["name"]=argv.name
	if (argv.bridge):
		body["bridge"]=argv.bridge
	if (argv.netname):
		body["netname"]=argv.netname
	if (argv.gateway):
		body["gateway"]=argv.gateway
	r = requests.post(BASE_URL+"/create",data=json.dumps(body), headers=HEADERS)
	print argv.netname
	print r.text


@cmd("container_delete",args=["id"], opt_args=[])
def container_delete(argv):
	r = requests.delete(BASE_URL + "/delete/%s" % argv.id)
	print r.text

@cmd("container_start",args=["id"], opt_args=[])
def container_start(argv):
	r = requests.post(BASE_URL+"/start/%s" % argv.id,headers=HEADERS)
	print r.text


@cmd("container_stop",args=["id"], opt_args=[])
def container_stop(argv):
	r = requests.post(BASE_URL+"/stop/%s" % argv.id,headers=HEADERS)
	print r.text


@cmd("container_list", args=[], opt_args=[])
def container_list(argv):
	r = requests.get(BASE_URL+"/list/container",headers=HEADERS)
	print  r.text



@cmd("network_create",args=[], opt_args=["name","cidr"])
def network_create(argv):
	body = dict()
	if (argv.name):
		body["name"]=argv.name
	if (argv.cidr):
		body["cidr"]=argv.cidr
	r = requests.post(BASE_URL+"/network/create",data=json.dumps(body), headers=HEADERS)
	print r.text	


@cmd("network_list",args=[], opt_args=[])
def network_list(argv):
	r=requests.get(BASE_URL+"/network/list",headers=HEADERS)
	print r.text



@cmd("image_list",args=[], opt_args=[])
def image_list(argv):
	r=requests.get(BASE_URL+"/image/list",headers=HEADERS)
	return r.text


@cmd("help", args=["action"])
def cli_help(argv):
	cmd_name = argv.action
	if cmd_name in FUNC_MAPPER.keys():
		func_info = FUNC_MAPPER.get(cmd_name)
		args = func_info["args"]
		opt_args = func_info["opt_args"]
		sub_parser = argparse.ArgumentParser(prog="agentctl %s" % cmd_name,
			description=func_info["description"],
			add_help=False)
		for i in args:
			sub_parser.add_argument(i)
		for i in opt_args:
			sub_parser.add_argument("--%s" % i, default=None)
		help_str = sub_parser.format_help()
		print re.sub("  -h, --help.+", "", help_str, flags=re.M)
	else:
		print "Only actions: %s available !" % " | ".join(FUNC_MAPPER.keys())

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		print ">> sub commands >>>>>>>"
		for i in FUNC_MAPPER.keys():
			print i
		sys.exit(0)
	if args[0] in ["-h", "--help"]:
		print "Usage: agentctl [sub_cmd] argvs..."
		print "Tips: agentctl help [sub_cmd]  to see usage of sub command"
		print "\nsub commands:"
		s = "\t" + "\n\t".join(FUNC_MAPPER.keys())
		print s	
		sys.exit(0)
	cmd_name = args[0]
	sub_arguments = args[1:]

	if cmd_name in FUNC_MAPPER.keys():
		sub_parser = argparse.ArgumentParser()
		func_info = FUNC_MAPPER.get(cmd_name)
		args = func_info["args"]
		opt_args = func_info["opt_args"]
		for i in args:
			sub_parser.add_argument(i)
		for i in opt_args:
			sub_parser.add_argument("--%s" % i, default=None)
		sub_args = sub_parser.parse_args(sub_arguments)
		print sub_args
		func = func_info["func"]
		ret = func(sub_args)
		sys.exit(ret)
	else:
		print "Only actions: %s available !" % " | ".join(FUNC_MAPPER.keys())
		sys.exit(1)

