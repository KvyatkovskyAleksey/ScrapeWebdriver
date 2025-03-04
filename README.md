# ScrapeWebdriver
Class based on selenium webdriver.Firefox with methods for scraping.
Allow dynamically change proxies with change of `"about:config".  

Changelog presented in CHANGELOG.md.

### Installation
`pip install scrapy_webdriver`

### Basic usage

For use selenium, need to yield `SeleniumRequest` and if you need to make some actions on page, can use driver_func.

```python
from typing import Iterable
import scrapy 
from scrapy.http import Request

from scrapy_webdriver.middleware_utils.drivers import Driver
from scrapy_webdriver.middleware_utils.http import SeleniumRequest


class TestSpider(scrapy.Spider):
    name = "simple_spider"
    start_urls = ["http://example.org"]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                driver_func=self.parse_page_with_driver,
            )

    def parse_page_with_driver(self, driver: Driver):
        self.logger.info("Page opened")

    def parse(self, response, **kwargs):
        yield {"title": response.css("title::text").get()}
```

### Available options

 - `SELENIUM_POOL_SIZE` - how many concurrent browser instances will be opened at same time, default 1
 - `SELENIUM_PROXY_POOL` - proxy pool in format `Iteable[http://user:pass@host:port]`, default `()`.
 - `SELENIUM_CHANGE_PROXY_ON_EACH_REQUEST` - change or not proxy before each request, default `True`.
 - `SELENIUM_INSTALL_ADBLOCK` - install adblock extension for block some requests, default `True`.
 - `SELENIUM_RUN_PYVIRTUAL_DISPLAY` - run py virtual display for not run drivers in headless on server, default `False`. 