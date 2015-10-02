import tabulate

import technic.solder.cli.command

class ModpackCommand(technic.solder.cli.command.Command):
	name         = 'modpack'
	command_help = 'Get information about modpacks'

	def setup(self, parser):
		subparsers = parser.add_subparsers()

		self.add_subcommand(subparsers, ListModpacksCommand())
		self.add_subcommand(subparsers, GetModpackCommand())

	def run(self, client, arguments):
		pass # This is a wrapper command so it will never actually be called

	def skip_handling(self):
		return True

class ListModpacksCommand(technic.solder.cli.command.Command):
	name         = 'list'
	command_help = 'List all available modpacks'

	def setup(self, parser):
		pass

	def run(self, client, arguments):
		self.output(
			'',
			tabulate.tabulate(
				[
					[slug, name]
					for slug, name in client.modpacks.iteritems()
				],
				headers = ['Slug', 'Name'],
			)
		)

class GetModpackCommand(technic.solder.cli.command.Command):
	name         = 'get'
	command_help = 'Get information about a modpack'

	def setup(self, parser):
		parser.add_argument(
			'modpack_slug',
			type = str,
			help = 'The modpack slug',
		)

	def run(self, client, arguments):
		modpack = client.get_modpack_info(arguments.modpack_slug)

		self.success(modpack['display_name'])

		self.output(
			'',
			tabulate.tabulate(
				[
					['Slug',              modpack['name']],
					['URL',               modpack['url']],
					['Recommended Build', modpack['recommended']],
					['Latest Build',      modpack['latest']],
					['Builds',            ', '.join(modpack['builds'][:10])],
				]
			)
		)

