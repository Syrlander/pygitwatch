#!/usr/bin/python3
"""Library to simplify interactions with json files"""

import json


def load_file(file_name):
    """Loads a json object from a given file"""
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_file(file_name, json_obj):
    """Saves a given json object to a given file"""
    with open(file_name, "w") as file:
        json.dump(json_obj, file)
