from selenium import webdriver
from bs4 import BeautifulSoup

class ScrapyWebdriver(webdriver.Firefox):
	'''Class with methods for scraping on selenium(Firefox) base'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		    
	def soup(self):
		'''Get soup from page'''
		return BeautifulSoup(self.page_source, 'lxml')

	def change_proxy(self, proxy):
		'''Open config page and change proxy'''
		proxy = proxy.split(':')
		self.get('about:config')
		if 'socks' in proxy[0].lower():
			set_preference(self, 'network.proxy.socks_version', int(proxy[0][-1]))
			set_preference(self, 'network.proxy.socks', proxy[1])
			set_preference(self, 'network.proxy.socks_port', int(proxy[2]))
			set_preference(self, 'network.proxy.type', 1)
		elif 'https' in proxy[0].lower():
			set_preference(self, 'network.proxy.ssl', proxy[1])
			set_preference(self, 'network.proxy.ssl_port', int(proxy[2]))
			set_preference(self, 'network.proxy.type', 1)
		elif 'http' in proxy[0].lower():
			set_preference(self, 'network.proxy.http', proxy[1])
			set_preference(self, 'network.proxy.ftp', proxy[1])
			set_preference(self, 'network.proxy.socks', proxy[1])
			set_preference(self, 'network.proxy.ssl', proxy[1])
			set_preference(self, 'network.proxy.http_port', int(proxy[2]))
			set_preference(self, 'network.proxy.ftp_port', int(proxy[2]))
			set_preference(self, 'network.proxy.socks_port', int(proxy[2]))
			set_preference(self, 'network.proxy.ssl_port', int(proxy[2]))
			set_preference(self, 'network.proxy.type', 1)
			set_preference(self, 'network.proxy.share_proxy_settings', 'true')

	def set_preference(self, pref, params):
		if params in ['false', 'true']:
			print('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setBoolPref("'+pref+'", '+str(params)+');')
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setBoolPref("'+pref+'", '+str(params)+');')
		elif type(params)==int:
			print('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setIntPref("'+pref+'", '+str(params)+');')
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setIntPref("'+pref+'", '+str(params)+');')
		elif type(params)==str:
			print('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setIntPref("'+pref+'", "'+params+'");')
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch).setCharPref("'+pref+'", "'+params+'");')