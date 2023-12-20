#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page
function (prototype: def get_page(url: str) -> str:).
The core of the function is very simple. It uses the requests
module to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code written in
exercise.py.

Inside get_page track how many times a particular URL was accessed in
the key "count:{url}" and cache the result with an expiration time of
10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response
and test your caching.

Bonus: implement this use case with decorators.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def cached(method: Callable) -> Callable:
    """decorator"""
    @wraps(method)
    def caller(url) -> str:
        """calls the method"""
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return caller


@cached
def get_page(url: str) -> str:
    """gets HTML from url"""
    return requests.get(url).text
