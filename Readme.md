# Technic Solder Client for Python

## Installation

Installation requires pip installed as well as Python 2.7 or greater. To install clone the repository and use the following command:

	pip install /path/to/technic-solder-client

Versions are also hosted on PyPi so feel free to use this instead:

	pip install technic-solder-client

## Usage

There are many commands available. All commands take a URL to the Solder server. This is denoted by the `solder_url` parameter.

### Server Info

Some times you just need to know some basic information about the Solder Server. You can get this information with the info command. This is done like so:

	solder <solder_url> server-info

### Verify

Used to verify that your API key is valid.

	solder <solder_url> verify-api-key <api_key>

### Mods

#### List

Gets a list of all available mods.

	solder <solder_url> mod list

#### Get

Gets information about a specific mod.

	solder <solder_url> mod get <mod_slug>

The `mod_slug` paramter is a URL friendly short name for the mod. This is set by the Solder server.

### Modpacks

There are a few commands available for modpacks.

#### List

This command lists off all the public modpacks that are available on the Solder server.

	solder <solder_url> modpack list

#### Get

This command gives some information about the modpack.

	solder <solder_url> modpack get <modpack_slug>

The `modpack_slug` parameter is a URL friendly short name for the modpack. This is set by the Solder server.

#### Build

This allows you to work with modpack builds.

##### Get

This command gives you the information on a particular build of a modpack.

	solder <solder_url> build <modpack_slug> get <build>

##### Download

This command downloads a build of the modpack.

	solder <solder_url> build <modpack_slug> download <build> [--latest] [--dir DIR] [--upgrade]

The `build` parameter is optional. If you don't give that the recommended build for the mod is chosen unless you also give the `--latest` flag. If you do that then the latest build is downloaded. If you give the `--dir` flag you can set a specific directory to download to. The default is the current directory. If the `--upgrade` flag is given then the bin, config, and mods directory are cleaned (deleted) before downloading the modpack. This flag does nothing if the directories don't exist.

### Configuration

You can use a configuration file to change a bit of how the solder client works. This file is by default located in your user home directory as a file named `.solderrc`. The configuration file is JSON formatted.

#### Solder Cache

You can change the location of your mod cache by setting the `cache` key in the configuration file. This is just a path to a directory.

	{
		...snip...
		"cache": "~/my-solder-cache"
		...snip...
	}

### Notes

All of the commands take an optional `--config <config_file>` flag that allows you to give a different configuration file.

### API

The client uses Python and you are more than welcome to tap into the API that is available for use in other applications.

