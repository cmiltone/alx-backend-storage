#!/usr/bin/env python3
"""
module declares a function that inserts a new document
in a collection based on kwargs:
Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""


def insert_school(mongo_collection, **kwargs):
    """inserts item into collection"""
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
