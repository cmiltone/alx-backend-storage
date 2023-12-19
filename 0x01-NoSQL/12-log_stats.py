#!/usr/bin/env python3
"""
module provides some stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method = 
["GET", "POST", "PUT", "PATCH", "DELETE"] 
in this order (see example below - warning: it's a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
"""
from pymongo import MongoClient


def print_logs(collection):
    """Prints stats about Nginx request logs in MongoDB"""
    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        total_requests = len(list(collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, total_requests))

    total_status = len(list(
        collection.find({'method': 'GET', 'path': '/status'})
    ))

    print('{} status check'.format(total_status))



if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print('{} logs'.format(collection.count_documents({})))

    print_logs(collection)
