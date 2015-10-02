import argparse

import technic.solder.app
import technic.solder.cli.command
import technic.solder.cli.commands

# pylint: disable=too-few-public-methods

class CLIApplication(technic.solder.app.Application):
	def run(self, *args, **kwargs):
		parser = argparse.ArgumentParser(
			description = 'Solder command line client',
		)

		parser.add_argument(
			'--config',
			type    = str,
			default = None,
			help    = 'the Solder client config file (defaults to ~/.solderrc)',
		)

		parser.add_argument(
			'solder_url',
			type = str,
			help = 'the Solder server url',
		)

		commands = self._get_all_commands()
		self._register_commands(parser, commands)

		arguments = parser.parse_args()
		arguments.func(arguments)

	def _get_all_commands(self):
		commands_module = technic.solder.cli.commands

		commands = [
			getattr(commands_module, command)
			for command in dir(commands_module)
		]

		return [
			command()
			for command in commands
			if isinstance(command, type) and
			issubclass(command, technic.solder.cli.command.Command)
		]

	def _register_commands(self, parser, commands):
		subparsers = parser.add_subparsers()

		for command in commands:
			command_parser = subparsers.add_parser(
				command.get_name(),
				help = command.get_command_help(),
			)

			command.setup(command_parser)
			if not command.skip_handling():
				command_parser.set_defaults(func = command.cli_handler)

