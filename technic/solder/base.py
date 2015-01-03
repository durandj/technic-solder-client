import hashlib
import json
import os
import os.path
import requests
import requests.exceptions
import shutil
import zipfile

try:
	import urlparse
except ImportError:
	# pylint: disable=import-error, no-name-in-module
	import urllib.parse
	urlparse = urllib.parse
	# pylint: enable=import-error, no-name-in-module

from .exceptions import SolderAPIError

class SolderServer(object):
	USER_CONFIG  = os.path.join(os.path.expanduser('~'), '.solderrc')
	SOLDER_CACHE = os.path.join(os.path.expanduser('~'), '.solder-cache')

	def __init__(self, solder_url, config_file = None):
		self.solder_url = solder_url

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

	def download_modpack(self, slug, build = None, callback = None, latest = False):
		if not build:
			modpack_info = self.get_modpack_info(slug)

			if latest:
				build = modpack_info['latest']
			else:
				build = modpack_info['recommended']

			if not build:
				raise SolderAPIError('Could not find a build to use')

		build_info = self.get_modpack_build_info(slug, build)

		for mod in build_info['mods']:
			self._download_mod(mod, callback)

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

		resp = requests.request(method, url)

		if not resp.status_code == 200:
			raise SolderAPIError('API connection error ({})'.format(resp.status_code))

		json_resp = resp.json()
		if 'error' in json_resp:
			raise SolderAPIError(json_resp['error'])

		return json_resp

	def _download_mod(self, mod_info, callback = None):
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

		if os.path.exists(os.path.join(self.solder_cache, filename)):
			callback('mod.download.cache')

			shutil.copy(os.path.join(self.solder_cache, filename), '.')
		else:
			resp = requests.get(url, stream = True)
			with open(filename, 'wb') as file_handle:
				for chunk in resp.iter_content(chunk_size = 1024):
					if chunk:
						file_handle.write(chunk)
						file_handle.flush()

			callback('mod.download.verify')

			md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
			if md5 != mod_info['md5']:
				callback('mod.download.verify.error')

				return

			shutil.copy(filename, os.path.join(self.solder_cache, filename))

		callback('mod.download.unpack')

		with zipfile.ZipFile(filename, 'r') as zip_handle:
			zip_handle.extractall()

		callback('mod.download.clean')

		os.remove(filename)

		callback('mod.download.finish')

