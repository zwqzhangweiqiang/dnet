
dnet

简介：

Dnet 旨在开发管理docker网络，实现跨主机连通，container管理更轻便，提供restful api调用。 实现集群管理，让集群更简便，部署更简便，只需要开通一个端口，即可管理整个集群。灵活的scheduler机制，分布创建虚拟机。使用container实现使用vm的习惯，支持vnc远程，ssh服务。不改变习惯照样使用docker container。超越vm。

功能：

网络：创建网络，创建IP地址段，分配container静态IP地址，删除IP地址，回收IP地址

生命周期管理：创建container，删除container（回收IP地址），启动（IP地址不变，实现配置文件管理）、关闭，快照

image：获取images列表

后续功能开发：

网络：支持openvswitch、vlan技术

container：完善restful api，完善其他导入、导出等功能

images：删除image，打tag等

使用方法：
1.查看命令集

  python agentcli.py


2.查看命令帮助

   python agentcli.py  help  network_list


3.查看镜像列表

   python agentcli.py   image_list

4.创建网络

   python agentcli.py  network  --name   vlan100   --cidr  10.10.10.0/24

5.列出网络

  python agentcli.py   network_list

6.创建虚拟机

  python agentcli.py  container_create --image   ubuntu   --hostname  test  --name  test   --bridge  br100 --netname  vlan100   --gateway  10.10.0.1

7.删除虚拟机

  python agentcli.py   container_delete   id

8.列出虚拟机列表

  python agentcli.py   container_list

9.停止虚拟机

  python agentcli.py   container_stop   id

10.启动虚拟机

  python agentcli.py  container_start  id
  
