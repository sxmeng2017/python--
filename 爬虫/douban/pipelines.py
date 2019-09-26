import hashlib

import 爬虫.douban.database as db

from 爬虫.douban.items import Comment, BookMeta, MovieMeta, Subject

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import to_bytes

from twisted.internet.defer import DeferredList

cursor = db.connection.cursor()


class DoubanPipeline(object):
    def get_subject(self, item):
        sql = 'SELECT id FROM subjects WHERE douban_id=%s'% item['douban_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_subject(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO subject (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_movie_meta(self, item):
        sql = 'SELECT id FROM movies WHERE douban_id=%s' % item['douban_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_movie_meta(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO movies (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def update_movie_meta(self, item):
        douban_id = item.pop('douban_id')
        keys = item.keys()
        values = tuple(item.values())
        values.append(douban_id)
        fields = ['%s=' % i + '%s' for i in keys]
        sql = 'UPDATE movies SET %s WHERE douban_id=%s' % (','.join(fields), '%s')
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def get_book_meta(self, item):
        sql = 'SELECT id FROM books WHERE douban_id=%s' % item['douban_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_book_meta(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO books (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def update_book_meta(self, item):
        douban_id = item.pop('douban_id')
        keys = item.keys()
        values = tuple(item.values())
        values.append(douban_id)
        fields = ['%s=' % i + '%s' for i in keys]
        sql = 'UPDATE books SET %s WHERE douban_id=%s' % (','.join(fields), '%s')
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_comment(self, item):
        sql = 'SELECT * FROM comments WHERE douban_comment_id=%s\
        ' % item['douban_comment_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_comment(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO comments (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def process_item(self, item, spider):
        if isinstance(item, Subject):
            '''
            subject
            '''
            exist = self.get_subject(item)
            if not exist:
                self.save_subject(item)
        elif isinstance(item, MovieMeta):
            '''
            meta
            '''
            exist = self.get_movie_meta(item)
            if not exist:
                try:
                    self.save_movie_meta(item)
                except Exception as e:
                    print(item)
                    print(e)
            else:
                self.update_movie_meta(item)
        elif isinstance(item, BookMeta):
            '''
            meta
            '''
            exist = self.get_book_meta(item)
            if not exist:
                try:
                    self.save_book_meta(item)
                except Exception as e:
                    print(item)
                    print(e)
            else:
                self.update_book_meta(item)
        elif isinstance(item, Comment):
            '''
            comment
            '''
            exist = self.get_comment(item)
            if not exist:
                try:
                    self.save_comment(item)
                except Exception as e:
                    print(item)
                    print(e)
        return item




