

import scrapy
from scrapy.http import Request
from datetime import datetime
from sullivan_tony.items import SullivanTonyItem
import re
from dateutil import parser
import sys
import webbrowser
reload(sys)
sys.setdefaultencoding("UTF-8")



class SullivanSpider(scrapy.Spider):
    name = "sullivanspider"
    allowed_domains = ["sullivan-auctioneers.com"]
    start_urls = [
                    "http://www.sullivan-auctioneers.com/auction-calendar-ma.htm",
                    ]
    base_url = "http://www.sullivan-auctioneers.com"

    def parse(self, response):
        item_link = response.selector.xpath("//table[@width='700']/tr/td[@colspan='2']/a/@href").extract()
        limit = 0
        for item in item_link:
            webbrowser.open(url=self.base_url+item)
            yield Request(url=self.base_url+item, callback=self.fetch_item)




    def fetch_item(self, response):
        print "------------------------------"
        print response.url

        #BUYER = None
        AUCTIONTIME = None
        DEPOSITE = None
        #ATTORNEY = None
        #ATTYPHONE = None
        AUCTIONEER = 'Sullivan'
        STREET = None
        CITY = None
        STATE = None
        #ZIPCODE = None
        #COUNTRY = None
        #STYLE = None
        #YEARBUILD = None
        LOTSIZE = None
        LIVINGAREA = None
        ROOMS_TOTAL = None
        ROOMS_BED = None
        ROOMS_BATH = None
        ROOMS_HALFBATH = None
        #ASSDVALUE = None
        #LAST_SOLD_DATE = None
        #LAST_SOLD_PRICE = None
        #LAST_MORT_DATE = None
        #LAST_MORT_AMT = None
        #NOTES = None
        #VALUE = None
        #AUTOMLS = None
        AUCTIONDATE = None
        #BID = None


        #fetching address
        title = response.selector.xpath("//td/span[@class='cattitle']/text()").extract()[0].strip()
        # fetching STREET details
        STREET = title.split(' - ')[0].title()
        # fetching CITY details
        CITY = (title.split(' - ')[1].split(',')[0]).strip().title()
        # fetching STATE
        STATE = (title.split(' - ')[1].split(',')[1]).strip()



        # fetching auction_details
        auction_details = response.selector.xpath("//td[@class='celltopborder' and not(contains(@valign, 'top'))]")[0]

        # fetching prop_details
        prop_details = auction_details.xpath("//td/p[1]")[0]

        # fetching auction_info
        auction_info = prop_details.xpath("//p/font[1]/b/font[1]/text()").extract()
        auction_info = ' ' .join([x.strip() for x in auction_info if x.strip()])

        # fetching AUCTIONTIME
        AUCTIONDATE, AUCTIONTIME = self.find_date_n_time(auction_info)

        # fetching property_specs
        property_specs = prop_details.xpath("//p/font[last()]/text()").extract()
        property_specs = ' '.join([x.strip() for x in property_specs if x.strip()])


        # fetching property_specs
        property_specs = property_specs.encode('ascii','ignore')
        # fetching bedrooms
        if re.findall(r'\d*\.*\d*\s*bedrooms?', property_specs):
            ROOMS_BED = re.findall(r'\d*\.*\d*\s*bedrooms?', property_specs)[0].split(" ")[0]
        # fetching rooms
        if re.findall(r'\d*\.*\d*\s*rooms?', property_specs):
            ROOMS_TOTAL = re.findall(r'\d*\.*\d*\s*rooms?', property_specs)[0].split(" ")[0]
        # fetching bathrooms
        if "bath" in property_specs:
            if "full" in property_specs or "half" in property_specs:
                ROOMS_BATH = re.findall(r'\d*\.*\d*\s*full', property_specs)[0].split(" ")[0]
                ROOMS_HALFBATH = re.findall(r'\d*\.*\d*\s*half baths?', property_specs)[0].split(" ")[0]
            else:
                ROOMS_BATH = re.findall(r'\d*\.*\d*\s*baths?', property_specs)[0].split(" ")[0]
        # fetching lotsize
        if re.findall(r'(\d*,\d*)\s*sf\s*lot', property_specs):
            LOTSIZE = re.findall(r'(\d*,\d*)\s*sf\s*lot',property_specs)[0].replace(',', '')
        # fetching LIVINGAREA
        if re.findall(r'(\d*,\d*)\s*sf\s*liv\s*sp', property_specs):
            LIVINGAREA = re.findall(r'(\d*,\d*)\s*sf\s*liv\s*sp', property_specs)[0].replace(',', '')


        # fetching terms_of_sale
        terms_of_sale = auction_details.xpath("//td/p[last()]//text()").extract()
        terms_of_sale = ' ' .join([x.strip() for x in terms_of_sale if x.strip()])
        DEPOSITE = re.findall(r'\$\d*,*\d*', terms_of_sale)[0].replace(',', '').replace('$', '')


        item = SullivanTonyItem(STREET = STREET,
                         CITY = CITY,
                         STATE = STATE,
                         AUCTIONDATE = AUCTIONDATE,
                         AUCTIONTIME = AUCTIONTIME,
                         ROOMS_TOTAL = ROOMS_TOTAL,
                         ROOMS_BED = ROOMS_BED,
                         ROOMS_BATH = ROOMS_BATH,
                         ROOMS_HALFBATH = ROOMS_HALFBATH,
                         DEPOSITE = DEPOSITE,
                         AUCTIONEER = AUCTIONEER,
                         LOTSIZE = LOTSIZE,
                         LIVINGAREA = LIVINGAREA,
                         )
        print "\n***********ITEM"
        print item
        yield item


    def find_date_n_time(self, auction_info):
        '''
        function to fetch date n time
        '''
        auction_info = auction_info.decode('ascii', 'ignore')
        time = re.findall(r'\d*:\d*\s[AaPp][Mm]', auction_info)
        time_count = len(time)

        if time_count == 1:
            time = time[0]
            date = re.findall(r'\w*\s-?\s\w*\s\d*,\s\d*', auction_info)[0]
            date = parser.parse(date).strftime("%Y-%m-%d")
            time = datetime.strptime(time, "%I:%M %p").strftime("%H:%M:%S")
            return date, time
        else:
            if "Real Estate:" in auction_info:
                time = re.findall(r'Real Estate:\s*(\d*:\d*\s[AaPp][Mm])', auction_info)[0]
                time = datetime.strptime(time, "%I:%M %p").strftime("%H:%M:%S")
            date = parser.parse(re.findall(r'\w*\s-?\s\w*\s\d*,\s\d*', auction_info)[0]).strftime("%Y-%m-%d")
            return date, time