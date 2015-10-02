import technic.solder.cli.command

class ServerInfoCommand(technic.solder.cli.command.Command):
	name         = 'server-info'
	command_help = 'get information about the server'

	def setup(self, parser):
		pass

	def run(self, client, arguments):
		server_info = client.server_info

		self.info('Version {} {}', server_info[0], server_info[1])

class VerifyAPIKeyCommand(technic.solder.cli.command.Command):
	name         = 'verify-api-key'
	command_help = 'verify a client api key'

	def setup(self, parser):
		parser.add_argument(
			'api_key',
			type = str,
			help = 'the client api key',
		)

	def run(self, client, arguments):
		response = client.verify_api_key(arguments.api_key)

		self.success('Key is valid for {}', response['name'])

