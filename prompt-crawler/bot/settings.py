BOT_NAME = 'bot'

SPIDER_MODULES = ['bot.spiders']

NEWSPIDER_MODULE = 'bot.spiders'

# Also, ensure this is set to avoid asyncio conflicts in Docker
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'