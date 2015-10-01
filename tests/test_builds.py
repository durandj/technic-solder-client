import requests
import unittest

# Provide Python 2 and Python 3 support
try:
	# pylint: disable=import-error, no-name-in-module
	from unittest import mock
	# pylint: enable=import-error, no-name-in-module
except ImportError:
	import mock

import technic.solder
import tests.utils

# pylint: disable=no-member

class TestModpackBuilds(unittest.TestCase):
	def setUp(self):
		self.requests_mock = mock.MagicMock()

		self.client = technic.solder.SolderClient(
			'http://solder.test/',
			requests_module = self.requests_mock,
		)

	def test_get_build(self):
		response = tests.utils.create_mock_response(requests.codes.OK, {
			'minecraft': '2.0.0',
			'java': '',
			'memory': '0',
			'forge': None,
			'mods': [
				{
					'name': 'mymod',
					'version': '1.0.0',
					'md5': 'deadbeef',
					'url': 'http://mods.solder.test/mods/mymod-1.0.0.zip',
				}
			],
		})

		self.requests_mock.request.return_value = response

		build = self.client.get_modpack_build_info('test1', '1.0.1')

		self.requests_mock.request.assert_called_once_with(
			'GET',
			'http://solder.test/api/modpack/test1/1.0.1'
		)

		self.assertEqual('2.0.0', build['minecraft'])

if __name__ == '__main__':
	unittest.main()

