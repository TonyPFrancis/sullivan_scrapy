# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SullivanTonyItem(scrapy.Item):

    BUYER = scrapy.Field()
    AUCTIONTIME = scrapy.Field()
    DEPOSITE = scrapy.Field()
    ATTORNEY = scrapy.Field()
    ATTYPHONE = scrapy.Field()
    AUCTIONEER = scrapy.Field()
    STREET = scrapy.Field()
    CITY = scrapy.Field()
    STATE = scrapy.Field()
    ZIPCODE = scrapy.Field()
    COUNTRY = scrapy.Field()
    STYLE = scrapy.Field()
    YEARBUILD = scrapy.Field()
    LIVINGAREA = scrapy.Field()
    ROOMS_TOTAL = scrapy.Field()
    ROOMS_BED = scrapy.Field()
    ROOMS_BATH = scrapy.Field()
    ROOMS_HALFBATH = scrapy.Field()
    ASSDVALUE = scrapy.Field()
    LAST_SOLD_DATE = scrapy.Field()
    LAST_SOLD_PRICE = scrapy.Field()
    LAST_MORT_DATE = scrapy.Field()
    LAST_MORT_AMT = scrapy.Field()
    NOTES = scrapy.Field()
    VALUE = scrapy.Field()
    AUTOMLS = scrapy.Field()
    # newly added items rather found in "http://daisher-chiles.com/auctions/auction_home.php"
    AUCTIONDATE = scrapy.Field()
    BID = scrapy.Field()
