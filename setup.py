#!/usr/bin/env python

# pylint: disable=bad-whitespace,missing-docstring

import os.path
from setuptools import find_packages, setup

with open('requirements.txt', 'r') as requirements_file:
	REQUIREMENTS = requirements_file.readlines()

with open('Readme.md', 'r') as readme_file:
	README = readme_file.read()

setup(
	name             = 'technic-solder-client',
	version          = '1.0',
	description      = 'Python implementation of a Technic Solder client',
	long_description = README,
	author           = 'Cadyyan',
	author_email     = 'cadyyan@gmail.com',
	url              = 'https://github.com/cadyyan/technic-solder-client',
	license          = 'MIT',
	packages         = find_packages(),
	install_requires = REQUIREMENTS,
	scripts          = [
		os.path.join('bin', 'solder'),
		os.path.join('bin', 'solder.py'),
	],
)

