import scrapy
import re
from scrapy_selenium import SeleniumRequest

class MissingUrlsSpider(scrapy.Spider):
    name = "missing_urls"
    allowed_domains = ["utdallas.edu"]
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "AUTOTHROTTLE_ENABLED": True,
        "ROBOTSTXT_OBEY": False,  # disable to bypass blocked pages if allowed
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "FEEDS": {"missing_data.json": {"format": "json"}}
    }

    def start_requests(self):
        # Read missing URLs from missing_urls.txt
        with open("missing_urls.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse_page, wait_time=5)

    def parse_page(self, response):
        # Check the response status and log warning if not 200
        if response.status != 200:
            self.logger.warning(f"URL {response.url} returned status {response.status}")
            return

        page_title = response.xpath("//title/text()").get()
        page_text = " ".join(response.xpath("//p//text()").getall()).strip()
        cleaned_text = re.sub(r"\s+", " ", page_text)

        yield {
            "url": response.url,
            "title": page_title,
            "content": cleaned_text
        }
