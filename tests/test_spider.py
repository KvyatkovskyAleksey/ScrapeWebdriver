from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

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

    def parse(self, response):
        yield {"title": response.css("title::text").get()}


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            # Example: store results in items.json
            "FEEDS": {
                "items.json": {"format": "json"},
            },
        }
    )

    process.crawl(TestSpider)
    process.start()
