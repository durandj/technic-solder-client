from __future__ import print_function

import abc
import colorama

import technic.solder.client

class Command(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def setup(self, parser):
		pass

	@abc.abstractmethod
	def run(self, client, cli_args):
		pass

	# pylint: disable=no-member
	def output(self, color, message, *args, **kwargs):
		message = color + message + colorama.Style.RESET_ALL

		print(
			message.format(
				*args,
				**kwargs
			)
		)

	def success(self, message, *args, **kwargs):
		self.output(colorama.Fore.GREEN, message, *args, **kwargs)

	def info(self, message, *args, **kwargs):
		self.output(colorama.Fore.BLUE, message, *args, **kwargs)

	def warning(self, message, *args, **kwargs):
		self.output(colorama.Fore.YELLOW, message, *args, **kwargs)

	def error(self, message, *args, **kwargs):
		self.output(colorama.Fore.RED, message, *args, **kwargs)
	# pylint: enable=no-member

	def get_name(self):
		if getattr(self, 'name'):
			return getattr(self, 'name')

		raise Exception('Commands must have the name attribute set')

	def get_command_help(self):
		if getattr(self, 'command_help'):
			return getattr(self, 'command_help')

		raise Exception('Commands must have the command_help attribute set')

	def skip_handling(self):
		return False

	def add_subcommand(self, subparsers, command):
		parser = subparsers.add_parser(
			command.get_name(),
			help = command.get_command_help(),
		)

		command.setup(parser)

		if not command.skip_handling():
			parser.set_defaults(func = command.cli_handler)

	def cli_handler(self, cli_args):
		client = technic.solder.client.SolderClient(
			cli_args.solder_url,
			config_file = cli_args.config,
		)

		self.run(client, cli_args)

