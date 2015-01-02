import requests
import requests.exceptions

try:
	import urlparse
except ImportError:
	# pylint: disable=import-error, no-name-in-module
	import urllib.parse
	urlparse = urllib.parse
	# pylint: enable=import-error, no-name-in-module

from .exceptions import SolderAPIError

class SolderServer(object):
	def __init__(self, solder_url):
		self.solder_url = solder_url

		self._modpacks = None

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

	@property
	def server_info(self):
		info = self._request(
			'/api',
			'GET',
		)

		return (info['version'], info['stream'])

	@property
	def modpacks(self):
		if not self._modpacks:
			self._modpacks = self._request('/api/modpack', 'GET')['modpacks']

		return self._modpacks

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

