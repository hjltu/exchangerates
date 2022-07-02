#!/usr/bin/env pyton3

"""
20jun22 hjltu
database for get_crypto
"""


import shelve


class DB():

    def __init__(self,db: str):
        self.db = db

    def write(self, key, val=None):

        """ Add new value to persistent data storage,
            new value stored in db as dict { key : val }
        Input:
            key: str, new key,
            val:new value
        Output: new value or None
        Usage:
            db = DB
            new = db._add_to_db("new", val)
            db.get_from_db(new) """

        with shelve.open(self.db) as db:
            if val:
                db[key] = val
            val = db.get(key)

        return val if val else None


    def read(self, val):

        """ Get value or all values from db """

        with shelve.open(self.db) as db:
            return db.get(val)
