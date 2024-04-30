#!/usr/bin/env python3
"""Python function that inserts a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """function that inserts a new document in a collection"""
    rlt = mongo_collection.insert_one(kwargs)
    return rlt.inserted_id
