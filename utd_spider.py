import scrapy
import re
from scrapy_selenium import SeleniumRequest

class UTDScraper(scrapy.Spider):
    name = "utd"
    allowed_domains = ["utdallas.edu"]
    start_urls = ["https://www.utdallas.edu/wp-sitemap.xml"]  # Start with main sitemap

    custom_settings = {
        "DOWNLOAD_DELAY": 5,  
        "FEEDS": {"utd_data.json": {"format": "json"}},  # Save scraped data in JSON
        "AUTOTHROTTLE_ENABLED": True,
        "ROBOTSTXT_OBEY": False,  # Allow Scrapy to follow all sitemap links
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"  # Prevent blocking
    }

    def parse(self, response):
        """Extract URLs from the main sitemap and follow sub-sitemaps or scrape content pages."""
        urls = response.xpath("//*[local-name()='loc']/text()").getall()
        self.logger.info(f"Extracted {len(urls)} URLs from {response.url}")

        for url in urls:
            if url.endswith(".xml"):  # If it's a sub-sitemap, follow it
                self.logger.info(f"Following sub-sitemap: {url}")
                yield scrapy.Request(url, callback=self.parse)
            else:  # If it's a content page, scrape it
                self.logger.info(f"Scraping page: {url}")
                yield SeleniumRequest(url=url, callback=self.parse_page, wait_time=5)

    def parse_page(self, response):
        """Extract page content."""
        page_title = response.xpath("//title/text()").get()
        page_text = " ".join(response.xpath("//p//text()").getall()).strip()
        page_url = response.url

        cleaned_text = re.sub(r"\s+", " ", page_text)  # Remove extra whitespace

        if cleaned_text:
            yield {
                "url": page_url,
                "title": page_title,
                "content": cleaned_text
            }
