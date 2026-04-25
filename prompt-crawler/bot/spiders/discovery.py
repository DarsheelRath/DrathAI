import scrapy
import httpx
import os
import json
from scrapy.loader import ItemLoader
from bot.items import ScrapedArticle

class DiscoverySpider(scrapy.Spider):
    name = "prompt_bot"

    def __init__(self, prompt=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Priority: Command line arg -> Env Var -> Fallback
        self.prompt = prompt or os.getenv('CRAWL_PROMPT') or "latest code breakthroughs"
        self.api_url = os.getenv('DUX_API_URL', 'http://dux-node:4479')

    def start_requests(self):
        self.logger.info(f"🚀 [INIT] Querying Dux Node for: {self.prompt}")
        
        # We yield the request to the Dux API
        yield scrapy.Request(
            url=f"{self.api_url}/search/text",
            method='POST',
            body=json.dumps({"query": self.prompt, "max_results": 5}),
            headers={'Content-Type': 'application/json'},
            callback=self.parse_discovery
        )

    def parse_discovery(self, response):
        links = response.json().get('results', [])
        if not links:
            self.logger.warning("⚠️ No links found in search results.")
            return

        for item in links:
            self.logger.info(f"🔗 [FOUND] {item['href']}")
            yield scrapy.Request(
                url=item['href'],
                callback=self.parse_site,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0'}
            )

    def parse_site(self, response):
        self.logger.info(f"✅ [SCRAPING] {response.url}")
        l = ItemLoader(item=ScrapedArticle(), response=response)
        
        l.add_value('url', response.url)
        l.add_css('title', 'title::text')
        l.add_value('prompt', self.prompt)
        
        # Targeted selectors for article bodies
        l.add_css('content', 'article p::text, main p::text, .content p::text, p::text')
        
        yield l.load_item()