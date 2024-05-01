#!/usr/bin/env python3
"""0. Writing strings to Redis"""

import redis
from functools import wraps
import uuid
from typing import Union, Callable

def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method Callable argument"""
    count_key = method.__qualname__ + "_count"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(count_key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        self._redis.rpush(inputs_key, str(args))
        rlt = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(rlt))

        return rlt
    return wrapper

def replay(method: Callable):
    """function to display the history of calls of a particular function"""
    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"
    
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)
    
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for i, (input_args, output) in enumerate(zip(inputs, outputs)):
        print(f"{method.__qualname__}(*{input_args.decode()}) -> {output.decode()}")

class Cache:

    """Cache class, Writing strings to Redis """
    def __init__(self) -> None:
        """store an instance of the Redis client as a private"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @call_history
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

