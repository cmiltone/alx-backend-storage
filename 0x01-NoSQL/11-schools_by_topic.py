#!/usr/bin/env python3
"""
module declares a function that returns
the list of school having a specific topic:

Prototype: def schools_by_topic(mongo_collection, topic):
mongo_collection will be the pymongo collection object
topic (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """lists school by topic"""
    docs = []
    for doc in mongo_collection.find({'topics': {'$in': [topic]}}):
        docs.append(doc)

    return docs
