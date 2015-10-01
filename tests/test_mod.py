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

class TestMod(unittest.TestCase):
	def setUp(self):
		self.requests_mock = mock.MagicMock()

		self.client = technic.solder.SolderServer(
			'http://solder.test/',
			requests_module = self.requests_mock,
		)

	# TODO: add check for getting all mods

	def test_get_mod(self):
		response = tests.utils.create_mock_response(requests.codes.OK, {
			'name':        'mymod',
			'pretty_name': 'My Mod',
			'author':      'me',
			'description': 'This is my mod',
			'link':        'mymod.test',
			'donate':      '',
			'versions':    [],
		})

		self.requests_mock.request.return_value = response

		mod = self.client.get_mod_info('mymod')

		self.requests_mock.request.assert_called_once_with(
			'GET',
			'http://solder.test/api/mod/mymod',
		)

		self.assertEqual('mymod', mod['name'])

if __name__ == '__main__':
	unittest.main()

