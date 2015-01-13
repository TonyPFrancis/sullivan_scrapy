"""

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
        #AUCTIONEER = None
        STREET = None
        CITY = None
        STATE = None
        #ZIPCODE = None
        #COUNTRY = None
        #STYLE = None
        #YEARBUILD = None
        #LIVINGAREA = None
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
        auction_info = self.clear_space_list(prop_details.xpath("//p/font[1]/b/font[1]/text()").extract())

        # fetching AUCTIONTIME
        AUCTIONDATE, AUCTIONTIME = self.find_date_n_time(auction_info)

        # fetching property_specs
        property_specs = self.clear_space_list(prop_details.xpath("//p/font[last()]/text()").extract())

        # fetching rooms
        for x in property_specs:
            # fetching bedrooms
            if re.findall(r'\d*\.*\d*\sbedrooms?', x):
                ROOMS_BED = re.findall(r'\d*\.*\d*\sbedrooms?', x)[0].split(" ")[0]
            # fetching rooms
            elif re.findall(r'\d*\.*\d*\srooms?', x):
                ROOMS_TOTAL = re.findall(r'\d*\.*\d*\srooms?', x)[0].split(" ")[0]
            elif "bath" in x:
                if "full" in x or "half" in x:
                    ROOMS_BATH = re.findall(r'\d*\.*\d*\sfull', x)[0].split(" ")[0]
                    ROOMS_HALFBATH = re.findall(r'\d*\.*\d*\shalf baths?', x)[0].split(" ")[0]
                else:
                    ROOMS_BATH = re.findall(r'\d*\.*\d*\sbaths?', x)[0].split(" ")[0]



        # fetching terms_of_sale
        terms_of_sale = self.clear_space_block(auction_details.xpath("//td/p[last()]//text()").extract())
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
                         )
        print "\n***********ITEM"
        print item
        yield item





    def clear_space_block(self, list):
        '''
        removes blank and joins the line to form a return block
        :param list:
        :return:
        '''
        new_block = "".join([x.strip() for x in list])
        return new_block

    def clear_space_list(self, list):
        '''
        removes blank line and returns as list of striped items
        :param list:
        :return:
        '''
        for x in list:
            if re.match(r'^(\s)*$', x):
                list.remove(x)
        for x in list:
            list[list.index(x)] = x.strip()
        return list

    def find_date_n_time(self, auction_info):
        '''
        function to fetch date n time
        '''
        time_count = 0
        date_n_time = ''
        date = ''
        time = ''
        for x in auction_info:
            if re.search(r'\d{1,2}:\d{1,2} ([aApP][mM])', x):
                time_count += 1
                date_n_time = x

        if time_count == 1:
            date, time = re.split(r'at|@', date_n_time, flags=re.I)
            print date, time
            try:
                date = datetime.strptime(date.strip(), "%A - %B %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                date = date.decode('ascii', 'ignore')
                date = parser.parse(date).strftime("%Y-%m-%d")
            time = datetime.strptime(time.strip(), "%I:%M %p").strftime("%H:%M:%S")
            return date, time
        else:
            for x in auction_info:
                if "Real Estate:" in x:
                    time = datetime.strptime(re.findall(r'\d*:\d*\s[aApP][mM]', x)[0], "%I:%M %p").strftime("%H:%M:%S")
                if re.findall(r'\w*\s-\s\w*\s\d*,\s\d*', x):
                    date = datetime.strptime(re.findall(r'\w*\s-\s\w*\s\d*,\s\d*', x)[0], "%A - %B %d, %Y").strftime("%Y-%m-%d")
            return date, time
"""