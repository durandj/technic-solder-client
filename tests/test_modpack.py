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

class TestModpack(unittest.TestCase):
	def setUp(self):
		self.requests_mock = mock.MagicMock()

		self.client = technic.solder.SolderClient(
			'http://solder.test/',
			requests_module = self.requests_mock,
		)

	def test_get_all(self):
		response = tests.utils.create_mock_response(requests.codes.OK, {
			'modpacks': {
				'test1': {
					'name':          'test1',
					'display_name':  'Test Modpack 1',
					'url':            None,
					'icon':           None,
					'icon_md5':       '',
					'logo':           None,
					'logo_md5':       '',
					'background':     None,
					'background_md5': '',
					'recommended':    'deadbeef',
					'latest':         'deadbeef',
					'builds':         ['deadbeef']
				},
				'test2': {
					'name':          'test2',
					'display_name':  'Test Modpack 2',
					'url':            None,
					'icon':           None,
					'icon_md5':       '',
					'logo':           None,
					'logo_md5':       '',
					'background':     None,
					'background_md5': '',
					'recommended':    'deadbeef',
					'latest':         'deadbeef',
					'builds':         ['deadbeef']
				},
			},
		})

		self.requests_mock.request.return_value = response

		modpacks = self.client.modpacks

		self.requests_mock.request.assert_called_once_with(
			'GET',
			'http://solder.test/api/modpack',
		)

		self.assertEqual(2, len(modpacks))
		self.assertIn('test1', modpacks.keys())
		self.assertIn('test2', modpacks.keys())

	def test_get_modpack(self):
		response = tests.utils.create_mock_response(requests.codes.OK, {
			'name':          'test1',
			'display_name':  'Test Modpack 1',
			'url':            None,
			'icon':           None,
			'icon_md5':       '',
			'logo':           None,
			'logo_md5':       '',
			'background':     None,
			'background_md5': '',
			'recommended':    'deadbeef',
			'latest':         'deadbeef',
			'builds':         ['deadbeef']
		})

		self.requests_mock.request.return_value = response

		modpack = self.client.get_modpack_info('test1')

		self.requests_mock.request.assert_called_once_with(
			'GET',
			'http://solder.test/api/modpack/test1',
		)

		self.assertEqual('test1', modpack['name'])

if __name__ == '__main__':
	unittest.main()

