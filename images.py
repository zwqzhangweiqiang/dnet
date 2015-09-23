import docker


class image(object):
	def __init__(self,url):
		self.connection=docker.Client(base_url=url)

	def get_images(self):
		return self.connection.images()

