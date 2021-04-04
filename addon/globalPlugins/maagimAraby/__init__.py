# -*- coding: utf-8 -*-
# Copyright (C) Ibrahim Hamadeh, released under GPLv2.0
# See the file COPYING for more details.
# This addon is aimed to get meaning of arabic words from arabic dictionaries using almaany.com website dictionaries.
#press nvda+Alt+M, a dialog will be displayed, and you will be standing on an edit box
#write the word you want, tab and choose the dictionary, press enter and the meaning will be displayed in a separate browseable window .

import gui, wx
from gui import guiHelper
import config
import globalPluginHandler
from .myDialog import MyDialog
from logHandler import log
import addonHandler
addonHandler.initTranslation()

#default configuration 
configspec={
	"windowType": "integer(default=0)",
	"closeDialogAfterRequiringTranslation": "boolean(default= False)"
}
config.conf.spec["maagimAraby"]= configspec

INSTANCE= None

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory= _('Maagim Araby')

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(DictionariesAlmaany)

	def terminate(self):
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(DictionariesAlmaany)

	def script_showDialog(self, gesture):
		global INSTANCE
		if not INSTANCE:
			d= MyDialog(gui.mainFrame)
			#d= MyDialog(None)
#			log.info('after creating object')
			d.postInit()
			d.Raise()
			d.Show()
			INSTANCE= d
		else:
			INSTANCE.Raise()
	script_showDialog.__doc__= _('Opens Maagim araby dialog to get meaning of arabic words.')

	__gestures= {
		'kb:nvda+alt+m': 'showDialog'
	}

#make  SettingsPanel  class
class DictionariesAlmaany(gui.SettingsPanel):
	# Translators: title of the dialog
	title= _("Maagim Araby")

	def makeSettings(self, sizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		# Translators: Type of windows to display translation result.
		windowTypes= [_("Default full browser"), _("Browser window only"), _("NVDA browseable message box(choose it after testing)")]
		self.resultWindowComboBox= settingsSizerHelper.addLabeledControl(
		# Translators: label of cumbo box to choose type of window to display result.
		_("Choose type of window To Display Result:"), 
		wx.Choice, choices= windowTypes)
		self.resultWindowComboBox.SetSelection(config.conf["maagimAraby"]["windowType"])

		# Translators: label of the check box 
		self.closeDialogCheckBox=wx.CheckBox(self,label=_("&Close Maagim Araby Dialog after requesting translation"))
		self.closeDialogCheckBox.SetValue(config.conf["maagimAraby"]["closeDialogAfterRequiringTranslation"])
		settingsSizerHelper.addItem(self.closeDialogCheckBox)

	def onSave(self):
		config.conf["maagimAraby"]["windowType"]= self.resultWindowComboBox.GetSelection()
		config.conf["maagimAraby"]["closeDialogAfterRequiringTranslation"]= self.closeDialogCheckBox.IsChecked() 
