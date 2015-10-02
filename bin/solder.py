#!/usr/bin/env python

from __future__ import print_function

import argparse
import colorama

import technic.solder.cli.app

def main():
	try:
		technic.solder.cli.app.CLIApplication().run()
	except technic.solder.SolderAPIError as ex:
		print(colorama.Fore.RED + ex.message + colorama.Style.RESET_ALL)

if __name__ == '__main__':
	main()

