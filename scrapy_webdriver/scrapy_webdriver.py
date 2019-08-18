from seleniumwire import webdriver as wire_webdriver
from seleniumwire.webdriver.request import Request
from selenium import webdriver
from bs4 import BeautifulSoup
import requests



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
			self.set_preference('network.proxy.socks', proxy[1][2:])
			self.set_preference('network.proxy.socks_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
		elif 'https' in proxy[0].lower():
			self.set_preference('network.proxy.ssl', proxy[1][2:])
			self.set_preference('network.proxy.ssl_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
		elif 'http' in proxy[0].lower():
			self.set_preference('network.proxy.http', proxy[1][2:])
			self.set_preference('network.proxy.ftp', proxy[1][2:])
			self.set_preference('network.proxy.socks', proxy[1][2:])
			self.set_preference('network.proxy.ssl', proxy[1][2:])
			self.set_preference('network.proxy.http_port', int(proxy[2]))
			self.set_preference('network.proxy.ftp_port', int(proxy[2]))
			self.set_preference('network.proxy.socks_port', int(proxy[2]))
			self.set_preference('network.proxy.ssl_port', int(proxy[2]))
			self.set_preference('network.proxy.type', 1)
			self.set_preference('network.proxy.share_proxy_settings', 'true')

	def disable_cache(self):
		'''Disable browser cache'''
		self.get("about:config")
		self.set_preference('browser.cache.disk.enable', 'false')
		self.set_preference('browser.cache.memory.enable', 'false')
		self.set_preference('browser.cache.offline.enable', 'false')
		self.set_preference('network.http.use-cache', 'false')


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




class ScrapyWebdriverWire(wire_webdriver.Firefox):
	'''Class with methods for scraping on selenium_wire.webdriver(Firefox) base'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.r_session = requests.Session()
		self.proxy = None
		
	def soup(self):
		'''Get soup from page'''
		return BeautifulSoup(self.page_source, 'lxml')


	def change_proxy(self, proxy):
		'''Change proxy(format: <protocol:ip:port>). Only http and https'''
		self.proxy = proxy
		proxies = {'http': self.proxy,
			 	   'https': self.proxy}
		proxy = (proxy.split('://')[0], None, None, proxy.split('://')[1])
		self.r_session.proxies.update(proxies)
		self._client._proxy.proxy_config = {
			'http': proxy,
			'https': proxy,
			'no_proxy': []
		}

	def get(self, url):
		super().get(url)
		cookies_list = self.get_cookies()
		for cookie in cookies_list:
			self.r_session.cookies.set(cookie['name'], cookie['value'])



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

	def repeat_request(self, request, headers=None, body=None):
		'''Repeat request from ScrapyWebdriverWire.requests with requests library.
		You can add params to request.'''
		params = request.__dict__['_data']
		if headers:
			for k in headers:
				params[headers][k] = headers[k]
		if body:
			request.body = body
		if params['method'] == 'GET':
			r = self.r_session.get(params['path'], headers=params['headers'], data=request.body)
		elif params['method'] == 'POST':
			r = self.r_session.post(params.path, headers=params.headers, data=params.body)
		elif params['method'] == 'PUT':
			r = self.r_session.put(params.path, headers=params.headers, data=params.body)
		elif params['method'] == 'DELETE':
			r = self.r_session.delete(params.path, headers=params.headers, data=params.body)
		elif params['method'] == 'HEAD':
			r = self.r_session.head(params.path, headers=params.headers, data=params.body)
		elif params['method'] == 'OPTIONS':
			r = self.r_session.options(params.path, headers=params.headers, data=params.body)
		self.add_cookie(self.r_session.cookies.get_dict())
		return r



if __name__=='__main__':
	wspider = ScrapyWebdriverWire(executable_path='utilites//geckodriver')
	proxy = 'https://103.35.64.12:3128'
	wspider.change_proxy(proxy)
	wspider.get('https://yandex.ru')
