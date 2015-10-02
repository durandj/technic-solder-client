import abc

class Application(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def run(self, *args, **kwargs):
		pass

