#!/usr/bin/env python3
"""
module declares a function that lists all documents in a collection:
Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""


def list_all(mongo_collection):
    """lists all docs in a collection"""
    docs = []
    for doc in mongo_collection.find({}):
        docs.append(doc)
    return docs
