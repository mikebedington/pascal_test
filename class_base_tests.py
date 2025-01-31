


class env(object):
	def __init__(self):
		self.temp = 10
		self.sal = 32

	def update(self):
		self.temp += 0.1
		self.sal += 0.2




class base1(object):
	def __init__(self, environment, param1, param2):
		self.param1 = param1
		self.param2 = param2
		self.environment = environment

	def print_env(self):
		print(f'Temp = {self.environment.temp}')
		print(f'Sal = {self.environment.sal}')

