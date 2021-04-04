# -*- coding: utf-8 -*-
#This module is responsible for displaying MaagimAraby dialog

import wx
import queueHandler
import config
import sys
import webbrowser
from .fetchtext import MyThread
from .fetchtext import isSelectedText
from .getbrowsers import getBrowsers
from tones import beep
from logHandler import log
import time
import subprocess
import threading
import tempfile
import ui
import os
import addonHandler
addonHandler.initTranslation()

#browsers as dictionary with label as key, and executable path as value.
browsers= getBrowsers()

def appIsRunning(app):
	'''Checks if specific app is running or not.'''
	processes= subprocess.check_output('tasklist', shell=True).decode('mbcs')
	return app in processes

def openBrowserWindow(label, meaning, directive, default= False):
	html= """
	<!DOCTYPE html>
	<meta charset=utf-8>
	<title>{title}</title>
	<meta name=viewport content='initial-scale=1.0'>
	""".format(title= _('Maagim Araby')) + meaning 
	temp= tempfile.NamedTemporaryFile(delete=False)
	path = temp.name + ".html"
	f = open(path, "w", encoding="utf-8")
	f.write(html)
	f.close()
	if default:
		webbrowser.open(path)
	else:
		subprocess.Popen(browsers[label] + directive + path)
	t=threading.Timer(30.0, os.remove, [f.name])
	t.start()

# Base url for all Arabic dictionaries.
DICTIONARIES_BASE_URL= 'https://www.almaany.com/ar/dict/ar-ar/'
#dictionaries name and query for Arabic maagim
dictionaries_nameAndQuery= [(u'معجم المَعاني الجامع- معجم عربي عربي', ''),
(u'المعجم الوسيط-قاموس عربي عربي', 'المعجم الوسيط'),
(u'معجم اللغة العربية المعاصر-قاموس عربي عربي', 'اللغة العربية المعاصر'),
(u'معجم القاموس المحيط-قاموس عربي عربي', 'القاموس المحيط'),
(u'معجم الرائد-قاموس عربي عربي', 'الرائد'),
(u'معجم لسان العرب-قاموس عربي عربي', 'لسان العرب'),
(u'معجم الغني-قاموس عربي عربي', 'الغني'),
(u'قاموس قرآن-قاموس عربي عربي', 'قرآن'),
(u'قاموس مختار الصحاح. قاموس عربي عربي', 'مختار الصحاح'),
(u'قاموس مصطلحات فقهية. قاموس عربي عربي', 'مصطلحات فقهية'),
(u'معجم الاصوات. قاموس عربي عربي', 'معجم الاصوات'),
(u'قاموس عربي عامة. قاموس عربي عربي', 'عربي عامة'),
(u'قاموس الأعشاب. قاموس عربي عربي', 'الأعشاب'),
(u'قاموس تعابير شائعة. قاموس عربي عربي', 'تعابير شائعة')
]

class MyDialog(wx.Dialog):
	def __init__(self, parent,  word=""):
		super(MyDialog, self).__init__(parent, title = 'المعاجم العربية', size = (300, 500))
		self.word= word
		#list of available dictionaries
		self.dictionaries= [name for name, query in dictionaries_nameAndQuery]
		panel = wx.Panel(self, -1)
		editTextLabel= wx.StaticText(panel, -1, _("Enter a word please"))
		editBoxSizer =  wx.BoxSizer(wx.HORIZONTAL)
		editBoxSizer.Add(editTextLabel, 0, wx.ALL, 5)
		self.editTextControl= wx.TextCtrl(panel)
		editBoxSizer.Add(self.editTextControl, 1, wx.ALL|wx.EXPAND, 5)

		cumboSizer= wx.BoxSizer(wx.HORIZONTAL)
		cumboLabel= wx.StaticText(panel, -1, _("Choose Dictionary"))
		cumboSizer.Add(cumboLabel, 0, wx.ALL, 5)
		self.cumbo= wx.Choice(panel, -1, choices= self.dictionaries)
		cumboSizer.Add(self.cumbo, 1, wx.EXPAND|wx.ALL, 5)

		buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.ok= wx.Button(panel, -1, _('OK'))
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.onOk)
		buttonSizer.Add(self.ok, 0,wx.ALL, 10)
		self.cancel = wx.Button(panel, wx.ID_CANCEL, _('cancel'))
		self.cancel.Bind(wx.EVT_BUTTON, self.onCancel)
		buttonSizer.Add(self.cancel, 0, wx.EXPAND|wx.ALL, 10)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(editBoxSizer, 1, wx.EXPAND|wx.ALL, 10)
		mainSizer.Add(cumboSizer, 1, wx.EXPAND|wx.ALL,10)
		mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 5)
		panel.SetSizer(mainSizer)
	def postInit(self):
		if isSelectedText():
			self.editTextControl.SetValue(isSelectedText())
		self.cumbo.SetSelection(0)
		self.editTextControl.SetFocus()

	def getMeaning(self, text, query, base_url):
		t= MyThread(text, query, base_url)
		t.start()
		#log.info(t.is_alive())
		while not t.meaning and not t.error and t.is_alive():
			beep(500, 100)
			time.sleep(0.5)
		t.join()
		#log.info(t.is_alive())

		title= u'المَعَاني message box'
		useDefaultFullBrowser= config.conf["maagimAraby"]["windowType"]== 0
		useBrowserWindowOnly= config.conf["maagimAraby"]["windowType"]== 1
		useNvdaMessageBox= config.conf["maagimAraby"]["windowType"]== 2
		if t.meaning and useDefaultFullBrowser:
			openBrowserWindow('default', t.meaning, directive= '', default= True)
		elif t.meaning and useBrowserWindowOnly:
			if 'Firefox' in browsers and not appIsRunning('firefox.exe'):
				openBrowserWindow('Firefox', t.meaning, directive= ' --kiosk ')
			elif 'Google Chrome' in browsers and not appIsRunning('chrome.exe'):
				openBrowserWindow('Google Chrome', t.meaning, directive= ' -kiosk ')
			elif 'Internet Explorer' in browsers:
				openBrowserWindow('Internet Explorer', t.meaning, directive= ' -k -private ')
		elif t.meaning and useNvdaMessageBox:
			queueHandler.queueFunction(queueHandler.eventQueue, ui.browseableMessage, t.meaning, title=title, isHtml=True)
			return
		elif t.error:
			if t.error== "HTTP Error 410: Gone":
				msg= "No meaning found"
			elif t.error== "<urlopen error [Errno 11001] getaddrinfo failed>":
				msg= "Most likely no internet connection"
			else:
				msg= t.error
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Sorry, Service not available({})".format(msg)))

	def onOk(self, e):
		word= self.editTextControl.GetValue()
		if not word:
			self.editTextControl.SetFocus()
			return
		else:
			i= self.cumbo.GetSelection()
			querey_url= dictionaries_nameAndQuery[i][1]
			self.getMeaning(word, querey_url, DICTIONARIES_BASE_URL)
			#wx.CallAfter(self.getMeaning, word, dict_url)
			closeDialogAfterRequiringTranslation= config.conf["maagimAraby"]["closeDialogAfterRequiringTranslation"]
			if closeDialogAfterRequiringTranslation:
				wx.CallLater(4000, self.Destroy)

	def onCancel (self, e):
		self.Destroy()
