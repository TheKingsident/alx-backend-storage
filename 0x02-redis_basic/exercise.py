#!/usr/bin/env python3
"""0. Writing strings to Redis"""

import redis
from functools import wraps
import uuid
from typing import Union, Callable

def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method Callable argument"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        cache_key = f"call_count:{key}"
        self._redis.incr(cache_key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class, Writing strings to Redis """
    def __init__(self) -> None:
        """store an instance of the Redis client as a private"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, float]:
        """get method that take a key string argument"""
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data
    
    def get_str(self, key: str) -> Union[str, None]:
        """automatically parametrize Cache.get"""
        return self.get(key, lambda x: x.decode("utf-8") if x else None)
    

    def get_int(self, key: str) -> Union[int, None]:
        """automatically parametrize Cache.get"""
        return self.get(key, lambda x: int(x) if x else None)
