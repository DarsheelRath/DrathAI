import scrapy
from itemloaders.processors import MapCompose, Join, TakeFirst
import re

def filter_junk(text):
    # Remove excessive tabs, newlines, and weird spacing
    text = re.sub(r'\s+', ' ', text).strip()
    # Return None if the text is just a common nav fragment or too short
    if len(text) < 40 or text.lower() in ['agree & join', 'cookie policy', 'read more']:
        return None
    return text

class ScrapedArticle(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(filter_junk),
        output_processor=Join("\n\n") # Join paragraphs with double newlines
    )
    prompt = scrapy.Field(output_processor=TakeFirst())