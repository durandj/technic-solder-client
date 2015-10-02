import tabulate

import technic.solder.cli.command

class ModCommand(technic.solder.cli.command.Command):
	name         = 'mod'
	command_help = 'Get information about mods'

	def setup(self, parser):
		subparsers = parser.add_subparsers()

		self.add_subcommand(subparsers, ListModsCommand())
		self.add_subcommand(subparsers, GetModCommand())

	def run(self, client, arguments):
		pass # This is a wrapper command so it will never actually be called

	def skip_handling(self):
		return True

class ListModsCommand(technic.solder.cli.command.Command):
	name         = 'list'
	command_help = 'List all available mods'

	def setup(self, parser):
		pass

	def run(self, client, arguments):
		self.output(
			'',
			tabulate.tabulate(
				[
					[slug, name]
					for slug, name in client.mods.iteritems()
				],
				headers = ['Slug', 'Name'],
			)
		)

class GetModCommand(technic.solder.cli.command.Command):
	name         = 'get'
	command_help = 'Get information about a specific mod'

	def setup(self, parser):
		parser.add_argument(
			'mod_slug',
			type = str,
			help = 'The mod slug',
		)

	def run(self, client, arguments):
		mod = client.get_mod_info(arguments.mod_slug)

		self.success(mod['pretty_name'])

		self.output(
			'',
			tabulate.tabulate(
				[
					['Slug',        mod['name']],
					['Author',      mod['author']],
					['Description', mod['description']],
					['Website',     mod['link']],
					['Donate URL',  mod['donate']],
					['Versions',    ', '.join(mod['versions'][:10])],
				]
			)
		)

