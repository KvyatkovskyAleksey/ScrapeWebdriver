import pytest
from scrapy.crawler import CrawlerRunner
from twisted.internet.defer import inlineCallbacks

from .test_spider import TestSpider

items_collected = []


class CollectItemsPipeline:
    def process_item(self, item, spider):
        items_collected.append(item)
        return item


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
