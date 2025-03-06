import os
import re
from itertools import cycle

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.command import Command

from .extension_creator import create_extension, create_anticaptcha_extension


# fixme need to refactor mixin and add type checking
class ChangeProxyMixin:
    """Mixin with methods for scraping on selenium.webdriver(Firefox) base"""

    def __init__(
        self,
        change_proxies_on_each_request=True,
        proxies=None,
        install_adblock=True,
        anticaptcha_api_key=None,
        *args,
        **kwargs,
    ):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.change_proxies_on_each_request = change_proxies_on_each_request
        self.proxies = proxies
        if self.proxies:
            self.proxies = cycle(self.proxies)
        super().__init__(*args, **kwargs)
        self.execute(Command.GET, {"url": "about:config"})
        # need for install extensions
        self.set_preference("xpinstall.signatures.required", "false")
        if install_adblock:
            self.install_addon(
                f"{self.path}/extensions/adblocker_ultimate-3.7.10-an+fx.xpi"
            )
        if anticaptcha_api_key:
            create_anticaptcha_extension(anticaptcha_api_key)
            self.install_addon(
                f"{self.path}/extensions/anticaptcha-plugin.xpi", temporary=True
            )
        if self.proxies:
            proxy = self.proxies.__next__()
            self.change_proxy(proxy)

    def soup(self):
        """Get soup from page"""
        return BeautifulSoup(self.page_source, "lxml")

    def change_proxy(self, proxy: str):
        """Open config page and change proxy"""
        proxy_data = re.split(":|@", proxy)
        proxy_username = None
        proxy_password = None
        proxy_type = proxy_data[0]
        proxy_address = proxy_data[-2]
        proxy_port = int(proxy_data[-1])
        if len(proxy_data) > 3:
            proxy_username = proxy_data[1].strip("//")
            proxy_password = proxy_data[2]
        self.execute(Command.GET, {"url": "about:config"})
        if "socks" in proxy_type:
            self.set_preference("network.proxy.socks_version", int(proxy_type[-1]))
            self.set_preference("network.proxy.socks", proxy_address)
            self.set_preference("network.proxy.socks_port", proxy_port)
            self.set_preference("network.proxy.type", 1)
        elif proxy_type.lower() == "https":
            self.set_preference("network.proxy.ssl", proxy_address)
            self.set_preference("network.proxy.ssl_port", proxy_port)
            self.set_preference("network.proxy.type", 1)
        elif proxy_type.lower() == "http":
            self.set_preference("network.proxy.http", proxy_address)
            self.set_preference("network.proxy.ftp", proxy_address)
            self.set_preference("network.proxy.socks", proxy_address)
            self.set_preference("network.proxy.ssl", proxy_address)
            self.set_preference("network.proxy.http_port", proxy_port)
            self.set_preference("network.proxy.ftp_port", proxy_port)
            self.set_preference("network.proxy.socks_port", proxy_port)
            self.set_preference("network.proxy.ssl_port", proxy_port)
            self.set_preference("network.proxy.type", 1)
            self.set_preference("network.proxy.share_proxy_settings", "true")
        if proxy_username and proxy_password:
            create_extension(proxy_username, proxy_password)
            self.install_addon(f"{self.path}/extensions/extension.xpi", temporary=True)

    def disable_cache(self):
        """Disable browser cache"""
        self.execute(Command.GET, {"url": "about:config"})
        self.set_preference("browser.cache.disk.enable", "false")
        self.set_preference("browser.cache.memory.enable", "false")
        self.set_preference("browser.cache.offline.enable", "false")
        self.set_preference("network.http.use-cache", "false")

    def set_preference(self, pref, params):
        """Set preference in 'about:config'"""
        if params in ["false", "true"]:
            self.execute_script(
                'Components.classes["@mozilla.org/preferences-service;1"]\
                .getService(Components.interfaces.nsIPrefBranch).setBoolPref("'
                + pref
                + '", '
                + str(params)
                + ");"
            )
        elif type(params) == int:
            self.execute_script(
                'Components.classes["@mozilla.org/preferences-service;1"]\
                .getService(Components.interfaces.nsIPrefBranch).setIntPref("'
                + pref
                + '", '
                + str(params)
                + ");"
            )
        elif type(params) == str:
            self.execute_script(
                'Components.classes["@mozilla.org/preferences-service;1"]\
                .getService(Components.interfaces.nsIPrefBranch).setCharPref("'
                + pref
                + '", "'
                + params
                + '");'
            )

    def get(self, url):
        """Loads a web page in the current browser session."""
        if (
            self.change_proxies_on_each_request
            and self.proxies
            and url != "about:config"
        ):
            proxy = self.proxies.__next__()
            self.change_proxy(proxy)
        self.execute(Command.GET, {"url": url})


class ScrapyWebdriver(ChangeProxyMixin, webdriver.Firefox):
    pass
