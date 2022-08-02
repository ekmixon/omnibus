#!/usr/bin/env python
##
# omnibus - deadbits.
# mongodb interaction
##

import pymongo

from common import error

from common import get_option


class Mongo(object):
    def __init__(self, config):
        self._host = get_option('mongo', 'host', config)
        self._port = int(get_option('mongo', 'port', config))
        self._server = f'{self._host}:{self._port}'
        try:
            self.conn = pymongo.MongoClient(self._server)
        except Exception as err:
            error(f'failed to connect to Mongo instance: {str(err)}')
            raise err

        self.db = self.conn['omnibus']
        self.collections = ['email', 'user', 'host', 'hash', 'bitcoin']


    def use_coll(self, collection):
        return self.db[collection]


    def get_value(self, collection, query, key):
        """ get value of given key from db query """
        coll = self.use_coll(collection)
        result = dict(coll.find_one(query, {key: 1}))
        return result[key] if result else None


    def exists(self, collection, query):
        coll = self.use_coll(collection)
        result = coll.find_one(query)
        return result is not None


    def count(self, collection, query={}):
        coll = self.use_coll(collection)
        return coll.count(query)


    def insert_one(self, collection, data):
        if isinstance(data, object):
            data = data.__dict__

        coll = self.use_coll(collection)
        doc_id = None

        try:
            doc_id = coll.insert(data)
        except Exception as err:
            error(f'failed to index data: {str(err)}')
        return str(doc_id)


    def update_one(self, collection, query, new_data):
        coll = self.use_coll(collection)
        doc_id = None

        try:
            doc_id = coll.update(query, {'$set': new_data})
        except:
            error(f'failed to update documents: {query}')

        return doc_id


    def delete_one(self, collection, query):
        coll = self.use_coll(collection)
        try:
            coll.remove(query)
        except:
            error(f'failed to delete documets: {query}')


    def find_recent(self, collection, query={}, num_items=25, offset=0):
        coll = self.use_coll(collection)
        total = self.count(collection, query)
        result = []

        if total < num_items:
            return list(coll.find(query))

        elif offset <= 0:
            return list(coll.find(query).limit(num_items).sort([('_id', -1)]))

        else:
            return list(coll.find(query).skip(offset).limit(num_items).sort([('_id', -1)]))


    def find(self, collection, query, one=False):
        """ return multiple query results as dict or single result as list """
        coll = self.use_coll(collection)

        if one:
            result = coll.find_one(query)

            if result is not None:
                d = dict(result)
                del d['_id']
                return d

            return {}

        else:
            result = coll.find(query)

            if result is not None:
                l = list(result)
                for i in l:
                    del i['_id']
                return l

            return []
