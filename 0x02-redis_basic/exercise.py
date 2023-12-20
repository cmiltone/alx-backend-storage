#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input data
in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float.
"""
import redis
import uuid
from typing import Union, Callable

Data = Union[str, bytes, int, float]


class Cache:
    """cache class"""
    def __init__(self) -> None:
        """inits class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Data) -> str:
        """stores data to redis"""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Callable) -> Data:
        """
        Redis only allows to store string, bytes and numbers
        (and lists thereof). Whatever you store as single
        elements, it will be returned as a byte string.
        Hence if you store "a" as a UTF-8 string,
        it will be returned as b"a" when retrieved
        from the server.

        In this exercise we will create a get method that take
        a key string argument and an optional Callable argument
        named fn. This callable will be used to convert the data
        back to the desired format.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """parametizes get"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """parametizes get"""
        return self.get(key, lambda x: int(x))
