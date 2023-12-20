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
from functools import wraps

Data = Union[str, bytes, int, float]



def count_calls(method: Callable) -> Callable:
    """
    Familiarize yourself with the INCR command and its python equivalent.
    In this task, we will implement a system to count how many times methods
    of the Cache class are called.

    Above Cache define a count_calls decorator that takes a single method
    Callable argument and returns a Callable.

    As a key, use the qualified name of method using the __qualname__ dunder
    method.

    Create and return function that increments the count for that key every
    time the method is called and returns the value returned by the original
    method.

    Remember that the first argument of the wrapped function will be self which
    is the instance itself, which lets you access the Redis instance.

    Protip: when defining a decorator it is useful to use functool.wraps to
    conserve the original function's name, docstring, etc. Make sure you
    use it as described here:
    https://docs.python.org/3.7/library/functools.html#functools.wraps

    Decorate Cache.store with count_calls.
    """
    @wraps(method)
    def caller(self, *args, **kwargs):
        """calls the method"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return caller

def call_history(method: Callable) -> Callable:
    """
    Familiarize yourself with the INCR command and its python equivalent.

    In this task, we will implement a system to count how many times methods
    of the Cache class are called.

    Above Cache define a count_calls decorator that takes a single method
    Callable argument and returns a Callable.

    As a key, use the qualified name of method using the __qualname__ dunder
    method.

    Create and return function that increments the count for that key every
    time the method is called and returns the value returned by the original
    method.

    Remember that the first argument of the wrapped function will be self which
    is the instance itself, which lets you access the Redis instance.

    Protip: when defining a decorator it is useful to use functool.wraps to
    conserve the original function’s name, docstring, etc. Make sure you use it
    as described here:
    https://docs.python.org/3.7/library/functools.html#functools.wraps

    Decorate Cache.store with count_calls.
    """
    @wraps(method)
    def caller(self, *args, **kwargs):
        """calls the method"""
        key_of_input = '{}:inputs'.format(method.__qualname__)
        key_of_output = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(key_of_input, str(args))
        return_val = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(key_of_output, return_val)
        return return_val
    return caller


def replay(fn: Callable) -> None:
    """
    In this tasks, we will implement a replay function to display the
    history of calls of a particular function.

    Use keys generated in previous tasks to generate the following output:
    >>> cache = Cache()
    >>> cache.store("foo")
    >>> cache.store("bar")
    >>> cache.store(42)
    >>> replay(cache.store)
    Cache.store was called 3 times:
    Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
    Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
    Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    store = getattr(fn.__self__, '_redis', None)
    if not isinstance(store, redis.Redis):
        return
    function = fn.__qualname__
    in_key = '{}:inputs'.format(function)
    out_key = '{}:outputs'.format(function)
    calls = 0
    if store.exists(function) != 0:
        calls = int(store.get(function))
    print('{} was called {} times:'.format(function, calls))
    inputs = store.lrange(in_key, 0, -1)
    outputs = store.lrange(out_key, 0, -1)
    for input, output in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            function,
            input.decode("utf-8"),
            output,
        ))

class Cache:
    """cache class"""
    def __init__(self) -> None:
        """inits class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Data) -> str:
        """stores data to redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Data:
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
        if fn is None:
            return self._redis.get(key)
        else:
            return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """parametizes get"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """parametizes get"""
        return self.get(key, lambda x: int(x))
