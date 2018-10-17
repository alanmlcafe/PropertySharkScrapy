# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertysharkItem(scrapy.Item):
    #Table 1 column 2-1
    building_addr = scrapy.Field()

    zipcode = scrapy.Field()

    borough = scrapy.Field()

    #Table 1 column 2-2
    lot_size = scrapy.Field()

    building_class = scrapy.Field()

    year_built = scrapy.Field()

    #Table 2 column 2-1
    neighborhood = scrapy.Field()

    school_district = scrapy.Field()

    residential_units =  scrapy.Field()

    commerical_units = scrapy.Field()

    #Table 2 column 2-2
    closest_police_station = scrapy.Field()

    closest_fire_station = scrapy.Field()
