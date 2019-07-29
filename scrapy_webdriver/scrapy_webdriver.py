from selenium import webdriver
from bs4 import BeautifulSoup

class ScrapyWebdriver(webdriver.Firefox):
	'''Class with methods for scraping on selenium.webdriver(Firefox) base'''
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
			self.set_preference('network.proxy.socks_version', int(proxy[0][-1]))
			self.set_preference('network.proxy.socks', proxy[1])
			self.set_preference('network.proxy.socks_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
		elif 'https' in proxy[0].lower():
			self.set_preference('network.proxy.ssl', proxy[1])
			self.set_preference('network.proxy.ssl_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
		elif 'http' in proxy[0].lower():
			self.set_preference('network.proxy.http', proxy[1])
			self.set_preference('network.proxy.ftp', proxy[1])
			self.set_preference('network.proxy.socks', proxy[1])
			self.set_preference('network.proxy.ssl', proxy[1])
			self.set_preference('network.proxy.http_port', int(proxy[2]))
			self.set_preference('network.proxy.ftp_port', int(proxy[2]))
			self.set_preference('network.proxy.socks_port', int(proxy[2]))
			self.set_preference('network.proxy.ssl_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
			self.set_preference('network.proxy.share_proxy_settings', 'true')

	def set_preference(self, pref, params):
		'''Set preference in 'about:config' '''
		if params in ['false', 'true']:
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"]\
				.getService(Components.interfaces.nsIPrefBranch).setBoolPref("'+pref+'", '+str(params)+');')
		elif type(params)==int:
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"]\
				.getService(Components.interfaces.nsIPrefBranch).setIntPref("'+pref+'", '+str(params)+');')
		elif type(params)==str:
			self.execute_script('Components.classes["@mozilla.org/preferences-service;1"]\
				.getService(Components.interfaces.nsIPrefBranch).setCharPref("'+pref+'", "'+params+'");')

	