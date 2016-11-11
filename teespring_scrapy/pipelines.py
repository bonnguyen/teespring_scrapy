# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import threading
from scrapy import log
from twisted.enterprise import adbapi

insert_critical_lock = threading.Lock()


class TeespringScrapyPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=settings['MYSQL_USE_UNICODE'],
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        with insert_critical_lock:
            # START CRITICAL SECTION
            category_id = -1
            try:
                # create record if doesn't exist.
                # all this block run on it's own thread
                tx.execute("select * from category where category_name = %s and category_url = %s",
                           (item['category_name'], item['category_url'], ))
                result = tx.fetchone()
                if result:
                    category_id = int(result[0])
                    log.msg("Category item already stored in db: %s" % item, level=log.DEBUG)
                else:
                    tx.execute( \
                        "insert into category (category_name, category_url) "
                        "values (%s, %s)",
                        (item['category_name'], item['category_url'])
                    )
                    category_id = int(tx.lastrowid)
                    log.msg("Category item stored in db: %s" % item, level=log.DEBUG)

                # if product existed
                tx.execute("select * from product where product_name = %s and product_url = %s and category_id = %s",
                           (item['product_name'], item['product_url'], category_id, ))
                result = tx.fetchone()
                if result:
                    if item['product_price'] != result[3] or item['product_image_url'] != result[4]:
                        tx.execute( \
                            "update product set product_price = %s, product_image_url = %s "
                            "where product_name = %s and product_url = %s and category_id = %s",
                            (
                                item['product_price'], item['product_image_url'], item['product_name'],
                                item['product_url'],
                                int(category_id))
                        )
                        log.msg("Product item updated in db: %s" % item, level=log.DEBUG)
                    else:
                        log.msg("Product item already stored in db: %s" % item, level=log.DEBUG)
                else:
                    tx.execute( \
                        "insert into product (product_name, product_url, product_price, product_image_url, category_id) "
                        "values (%s, %s, %s, %s, %s)",
                        (item['product_name'], item['product_url'], item['product_price'], item['product_image_url'],
                         int(category_id))
                    )
                    log.msg("Product item stored in db: %s" % item, level=log.DEBUG)
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                # STOP CRITICAL SECTION

    def handle_error(self, e):
        log.err(e)
