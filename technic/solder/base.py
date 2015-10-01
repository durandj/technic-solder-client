import hashlib
import json
import os
import os.path
import requests
import requests.exceptions
import shutil
import zipfile

# Provide Python 2 and Python 3 support
try:
	import urlparse
except ImportError:
	# pylint: disable=import-error, no-member, no-name-in-module
	import urllib.parse
	urlparse = urllib.parse
	# pylint: enable=import-error, no-member, no-name-in-module

from .exceptions import SolderAPIError

class SolderServer(object):
	USER_CONFIG  = os.path.join(os.path.expanduser('~'), '.solderrc')
	SOLDER_CACHE = os.path.join(os.path.expanduser('~'), '.solder-cache')

	def __init__(self, solder_url, config_file = None, requests_module = None):
		self.solder_url       = solder_url
		self._requests_module = requests_module if requests_module else requests

		config_file = config_file or SolderServer.USER_CONFIG
		if os.path.exists(config_file):
			with open(config_file, 'r') as file_handle:
				config = json.load(file_handle)
		else:
			config = {}

		self.solder_cache = os.path.expanduser(
			os.path.expandvars(
				config.get('cache', SolderServer.SOLDER_CACHE)
			)
		)

	def verify_api_key(self, api_key):
		return self._request(
			'/api/verify/{key}',
			'GET',
			key = api_key,
		)

	def get_mod_info(self, slug):
		return self._request(
			'/api/mod/{slug}',
			'GET',
			slug = slug,
		)

	def get_modpack_info(self, slug):
		return self._request(
			'/api/modpack/{slug}',
			'GET',
			slug = slug,
		)

	def get_modpack_build_info(self, slug, build):
		return self._request(
			'/api/modpack/{slug}/{build}',
			'GET',
			slug  = slug,
			build = build,
		)

	# pylint: disable=too-many-arguments
	def download_modpack(self, slug,
			build = None, callback = None, latest = False, directory = None, upgrade = False):
		if not build:
			modpack_info = self.get_modpack_info(slug)

			if latest:
				build = modpack_info['latest']
			else:
				build = modpack_info['recommended']

			if not build:
				raise SolderAPIError('Could not find a build to use')

		if not directory:
			directory = '.'

		build_info = self.get_modpack_build_info(slug, build)

		if upgrade:
			for path in ['bin', 'config', 'mods']:
				if os.path.exists(os.path.join(directory, path)):
					shutil.rmtree(os.path.join(directory, path))

		for mod in build_info['mods']:
			self._download_mod(mod, directory, callback = callback)
	# pylint: disable=too-many-arguments

	@property
	def server_info(self):
		info = self._request(
			'/api',
			'GET',
		)

		return (info['version'], info['stream'])

	@property
	def modpacks(self):
		return self._request('/api/modpack', 'GET')['modpacks']

	@property
	def mods(self):
		return self._request('/api/mod', 'GET')['mods']

	def _request(self, url, method, **kwargs):
		url_parts = urlparse.urlparse(self.solder_url)

		url = urlparse.urlunparse(
			(
				url_parts.scheme,
				url_parts.netloc,
				url.format(**kwargs),
				'',
				'',
				'',
			)
		)

		resp = self._requests_module.request(method, url)

		if not resp.status_code == 200:
			raise SolderAPIError('API connection error ({})'.format(resp.status_code))

		json_resp = resp.json()
		if 'error' in json_resp:
			raise SolderAPIError(json_resp['error'])

		return json_resp

	def _download_mod(self, mod_info, directory, callback = None):
		if not callback:
			# pylint: disable=unused-argument
			def skip(status, *args, **kwargs):
				pass

			callback = skip
			# pylint: enable=unused-argument

		callback('mod.download.start', name = mod_info['name'])

		url      = mod_info['url']
		filename = os.path.basename(url)

		if not os.path.exists(self.solder_cache):
			os.mkdir(self.solder_cache)

		file_path = os.path.join(directory, filename)

		if os.path.exists(os.path.join(self.solder_cache, filename)):
			callback('mod.download.cache')

			shutil.copy(os.path.join(self.solder_cache, filename), directory)
		else:
			resp = self._requests_module.get(url, stream = True)
			with open(file_path, 'wb') as file_handle:
				for chunk in resp.iter_content(chunk_size = 1024):
					if chunk:
						file_handle.write(chunk)
						file_handle.flush()

			callback('mod.download.verify')

			md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
			if md5 != mod_info['md5']:
				callback('mod.download.verify.error')
				return

			shutil.copy(file_path, os.path.join(self.solder_cache, filename))

		callback('mod.download.unpack')

		with zipfile.ZipFile(file_path, 'r') as zip_handle:
			zip_handle.extractall(directory)

		callback('mod.download.clean')

		os.remove(file_path)

		callback('mod.download.finish')

