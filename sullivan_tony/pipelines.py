# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class SullivanTonyPipeline(object):
    def process_item(self, item, spider):

        db = MySQLdb.connect(
            host='localhost', user="root", passwd="passme", db="synergy")
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        sql = """
                    INSERT INTO forclosure_master(
                        auctiondt, auctiontm, propaddr, propcity, propstate, deposit, totalrooms, bedrooms,
                        bathrooms, halfbaths, auctioneer, lotsize, livingarea, style)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % \
                    (
                        item['AUCTIONDATE'], item['AUCTIONTIME'], item['STREET'], item['CITY'], item['STATE'],
                        item['DEPOSITE'], item['ROOMS_TOTAL'], item['ROOMS_BED'], item['ROOMS_BATH'],
                        item['ROOMS_HALFBATH'], item['AUCTIONEER'], item['LOTSIZE'], item['LIVINGAREA'],
                        item['STYLE']
                    )
        cursor.execute(sql)
        db.commit()

