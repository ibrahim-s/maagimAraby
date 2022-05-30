# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "maagimAraby",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Maagim Araby"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""This addon helps get the meaning of arabic words from several arabic dictionaries on www.almaany.com website.
Press nvda+Alt+M, Maagim Araby dialog will be displayed, and you will be standing on an edit field.
If when pressing this command, you were standing on a selected word, the word will be put in the edit field.
Otherwise, enter in the edit field the word you want, tab an choose the dictionary you want and press enter.
The meaning of the word will be displayed in a separate browseable window."""),
	# version
	"addon_version": "1.3",
	# Author(s)
	"addon_author" : u"Ibrahim Hamadeh<ibra.hamadeh@hotmail.com>",
	# URL for the add-on documentation support
	"addon_url" : "https://github.com/ibrahim-s/maagimAraby.git",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3")
	"addon_minimumNVDAVersion" : "2019.3.0",
	# Last NVDA version supported/tested (e.g. "2018.4", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion" : "2022.1.0",
	# Add-on update channel (default is stable or None)
	"addon_updateChannel" : None,
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join("addon", "globalPlugins", "maagimAraby", "*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
