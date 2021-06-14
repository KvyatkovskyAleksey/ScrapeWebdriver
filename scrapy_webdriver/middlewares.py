from scrapy.crawler import Crawler
from scrapy import signals

from .middleware_utils.http import SeleniumRequest
from .middleware_utils.drivers import DriverPool


class AsyncSeleniumMiddleware:
    def __init__(self,
                 drivers_number: int,
                 proxies: tuple,
                 change_proxy_on_each_request: bool,
                 install_adblock: bool,
                 anticaptcha_api_key: str):
        self.driver_pool = DriverPool(drivers_number,
                                      proxies=proxies,
                                      change_proxy_on_each_request=change_proxy_on_each_request,
                                      install_adblock=install_adblock,
                                      anticaptcha_api_key=anticaptcha_api_key)

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        drivers_number = crawler.settings.getint("SELENIUM_POOL_SIZE", 1)
        proxies = crawler.settings.get("SELENIUM_PROXY_POOL", ())
        change_proxy_on_each_request = crawler.settings.get("SELENIUM_CHANGE_PROXY_ON_EACH_REQUEST", True)
        install_adblock = crawler.settings.get("SELENIUM_INSTALL_ADBLOCK", True)
        anticaptcha_api_key = crawler.settings.get("SELENIUM_ANTICAPTCHA_API_KEY", None)
        middleware = cls(drivers_number, proxies, change_proxy_on_each_request, install_adblock, anticaptcha_api_key)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request: SeleniumRequest, spider):
        try:
            request.is_selenium
        except AttributeError:
            return None

        return self.driver_pool.get_response(request)

    def spider_closed(self, spider):
        self.driver_pool.close()
