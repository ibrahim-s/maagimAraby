# -*- coding: utf-8 -*-
#this module is aimed to get a specific piece in almaany.com page
#that contains the meaning of the selected word

import textInfos
import urllib
import re
import api, ui
from logHandler import log
import threading
import os, sys

currentPath= os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentPath)
from user_agent import generate_user_agent
del sys.path[-1]

import addonHandler
addonHandler.initTranslation()

#the function that specifies if a certain text is selected or not
#and if it is, returns text selected
def isSelectedText():
	obj=api.getFocusObject()
	treeInterceptor=obj.treeInterceptor
	if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
		obj=treeInterceptor
	try:
		info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
	#except (RuntimeError, NotImplementedError):
	except:
		info=None
	if not info or info.isCollapsed:
		return False
	else:
		return info.text

regex1= '(<h1 class="section">[\s\S]+<h1 class="section">[\s\S]+?)<h[2-6]'
regex2= '(<h1 class="section">[\s\S]+?)<h[2-6]'
regex3= '(<h1>[\s\S]+?<h2>[\s\S]+?</h2>[\s\S]+?)<h[2-6]'

class MyThread(threading.Thread):
	def __init__(self, text, query, base_url):
		threading.Thread.__init__(self)
		self.text= text
		self.query= query
		self.base_url= base_url
		self.meaning= ""
		self.daemon=True
		self.error= False

	def run(self):
		text= self.text
		query= self.query
		if query:
			data= urllib.parse.quote(text)+ "/?c="+ urllib.parse.quote(query)
		else:
			data= urllib.parse.quote(text)
		url= self.base_url+ data
		#log.info(url)
		request= urllib.request.Request(url)
		userAgent= generate_user_agent()
		request.add_header('User-Agent', userAgent)
		try:
			handle = urllib.request.urlopen(request)
			html= handle.read().decode(handle.headers.get_content_charset())
			handle.close()
#			log.info(html)
		except Exception as e:
			log.info('', exc_info= True)
			self.error= str(e)
			#raise e
		else:
			try:
				content= re.findall(regex1, html)
				if not content:
					content= re.findall(regex2, html)
				if not content:
					content= re.findall(regex3, html)
				content= content[0]
				#removing unWanted text from the page.
				# regex of unWanted text in tables, third cell in the row.
				toBeRemoved1= r'<td>[\s\S]*?<div class="dropdown text-right">[\s\S]*?<span[\s\S]+?</span>[\s\S]*?<ol class="dropdown-menu">[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?</ol>[\s\S]*?</div>[\s\S]*?</td>'
				#regex of unWanted text outside tables, in lists.
				toBeRemoved2= r'<div class="dropdown text-right"[\s\S]+?<span[\s\S]+?</span>[\s\S]*?<ol class="dropdown-menu">[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?</ol>[\s\S]*?</div>'
				processedContent= re.sub(toBeRemoved1, "", content)
				finalContent= re.sub(toBeRemoved2, "", processedContent)

			except Exception as e:
				log.info('', exc_info= True)
				self.error= str(e)
				#raise e
			else:
				page= finalContent + "<p> <a href=%s>"%(url) + "Look for the meaning on the web site</a></p>"
				self.meaning= page
