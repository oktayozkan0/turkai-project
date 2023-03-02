# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InterpolItem(scrapy.Item):
    forename = scrapy.Field()
    name = scrapy.Field()
    date_of_birth = scrapy.Field()
    entity_id = scrapy.Field()
    thumbnail = scrapy.Field()
    url = scrapy.Field()