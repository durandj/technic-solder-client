import tabulate

import technic.solder.cli.command

class BuildCommand(technic.solder.cli.command.Command):
	name         = 'build'
	command_help = 'Get information about a modpack build'

	def setup(self, parser):
		parser.add_argument(
			'modpack_slug',
			type = str,
			help = 'the modpack slug',
		)

		subparsers = parser.add_subparsers()

		self.add_subcommand(subparsers, GetBuildCommand())
		self.add_subcommand(subparsers, DownloadBuildCommand())

	def run(self, client, arguments):
		pass # This is a wrapper command so it will never actually be called

	def skip_handling(self):
		return True

class GetBuildCommand(technic.solder.cli.command.Command):
	name         = 'get'
	command_help = 'Get information about a modpack build'

	def setup(self, parser):
		parser.add_argument(
			'build',
			type = str,
			help = 'the build number',
		)

	def run(self, client, arguments):
		build_info = client.get_modpack_build_info(
			arguments.modpack_slug,
			arguments.build
		)

		self.success(
			'{modpack} Build {build}',
			modpack = arguments.modpack_slug,
			build   = arguments.build,
		)

		self.output(
			'',
			tabulate.tabulate(
				[
					['Minecraft Version', build_info['minecraft']],
					['Forge',             build_info['forge']],
					['Mod Count',         len(build_info['mods'])],
				]
			)
		)

class DownloadBuildCommand(technic.solder.cli.command.Command):
	name         = 'download'
	command_help = 'Download a specific modpack build'

	def setup(self, parser):
		build_group = parser.add_mutually_exclusive_group()

		build_group.add_argument(
			'build',
			type    = str,
			default = None,
			nargs   = '?',
			help    = 'the build number',
		)

		build_group.add_argument(
			'--latest',
			action = 'store_true',
			dest   = 'latest',
			help   = 'use the latest build',
		)

		parser.add_argument(
			'--directory',
			type = str,
			help = 'the directory to download the modpack to',
		)

		parser.add_argument(
			'--upgrade',
			action = 'store_true',
			help   = 'upgrade the current installation (wipes out existing changes)',
		)

	def run(self, client, arguments):
		self.info(
			'Starting download of build {build} for {modpack}...',
			build   = arguments.modpack_slug,
			modpack = arguments.build,
		)

		client.download_modpack(
			arguments.modpack_slug,
			arguments.build,
			latest    = arguments.latest,
			directory = arguments.directory,
			upgrade   = arguments.upgrade,
			callback  = self.download_callback,
		)

		self.success('Finished downloading modpack build!')

	def download_callback(self, status, *args, **kwargs):
		if status == 'mod.download.start':
			self.info('\t{}', kwargs['name'])
			self.warning('\t\tDownloading...')
		elif status == 'mod.download.cache':
			self.warning('\t\tMod cached, skipping')
		elif status == 'mod.download.verify':
			self.warning('\t\tVerifying integrity...')
		elif status == 'mod.download.verify.error':
			self.error('\t\tFile did not download correct!')
		elif status == 'mod.download.unpack':
			self.warning('\t\tUnpacking mod...')
		elif status == 'mod.download.clean':
			self.warning('\t\tCleaning up...')
		elif status == 'mod.download.finish':
			self.success('\t\tFinished!')

