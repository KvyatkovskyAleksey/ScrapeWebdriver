import pytest
from scrapy.crawler import CrawlerRunner
from twisted.internet.defer import inlineCallbacks

from .test_spider import TestSpider

items_collected = []


class CollectItemsPipeline:
    def process_item(self, item, spider):
        items_collected.append(item)
        return item


def read_proxies():
    with open("proxies.txt") as file:
        return file.readlines()


def convert_proxies_to_standard_format(proxy_lines: list[str]):
    """
    Convert lines of proxies of the form:
      host:port:user:pass
    into:
      http://user:pass@host:port

    :param proxy_lines: List of proxy strings (e.g., ["u1.p.webshare.io:80:foo:bar", ...])
    :return: A list of proxy URLs in the format "http://user:pass@host:port".
    """
    standard_proxies = []
    for line in proxy_lines:
        line = line.strip()
        # Split by ":" into [host, port, user, password]
        try:
            host, port, username, password = line.split(":")
            standard_proxies.append(f"http://{username}:{password}@{host}:{port}")
        except ValueError:
            # If formatted differently, handle or skip accordingly
            pass
    return standard_proxies


@pytest.mark.twisted
@inlineCallbacks
def test_my_middleware():
    runner = CrawlerRunner(
        settings={
            "DOWNLOADER_MIDDLEWARES": {
                "scrapy_webdriver.middlewares.AsyncSeleniumMiddleware": 543,
            },
            "ITEM_PIPELINES": {
                "tests.test_scrapy_middleware.CollectItemsPipeline": 100,
            },
        }
    )

    yield runner.crawl(TestSpider)

    assert len(items_collected) > 0
    assert "title" in items_collected[0]


@pytest.mark.twisted
@inlineCallbacks
def test_my_middleware_with_proxy():
    runner = CrawlerRunner(
        settings={
            "DOWNLOADER_MIDDLEWARES": {
                "scrapy_webdriver.middlewares.AsyncSeleniumMiddleware": 543,
            },
            "ITEM_PIPELINES": {
                "tests.test_scrapy_middleware.CollectItemsPipeline": 100,
            },
            "SELENIUM_PROXY_POOL": convert_proxies_to_standard_format(read_proxies()),
        }
    )

    yield runner.crawl(TestSpider)

    assert len(items_collected) > 0
    assert "title" in items_collected[0]
