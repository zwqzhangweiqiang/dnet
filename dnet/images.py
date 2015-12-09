import docker


class image(object):
	def __init__(self,url):
		self.connection=docker.Client(base_url=url)

	def get_images(self):
		result= self.connection.images()
		list=[]
		for i in result:
			list.append(i['RepoTags'][0])
		return list

