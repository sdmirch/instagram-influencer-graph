import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import requests
from pymongo import MongoClient


def setup_mongo_client(db_name, collection_name, address='mongodb://localhost:27017/'):
    """ Return Mongo client and collection for record insertion.

    Args:
        db_name (str): Database name.
        collection_name (str): Collection name.
        address (Optional[str]): Address to mongo database.
            Defaults to 'mongodb://localhost:27017/)'.

    Returns:
        client (pymongo.MongoClient): Intantiated pymongo client.
        collection (pymongo.Collection): Collection object for record insertion.
    """
    client = MongoClient(address)
    db = client[db_name]
    collection = db[collection_name]
    return client, collection

def write_list(l, filepath):
    """
    Write list to file as text.

    Args:
        l (list): List to be written to file.
        filepath (str): Filepath where list will be saved as text.

    Output: None
    """
    with open(filepath, "w") as myfile:
        for item in l:
            myfile.write(str(item) + '\n')

def load_list(filepath):
    """
    Load list from file.

    Args:
        filepath (str): Filepath with list.

    Output:
        l (list): List from filepath.
    """
    l = []
    with open(filepath, "r") as myfile:
        for line in myfile:
            l.append(line.strip())
    return l

def write_json(d, filepath):
    """
    Write dictionary to file using json.dump.

    Args:
        d (dict): Dictionary to be written to file.
        filepath (str): Filepath where dictionary will be saved.

    Output: None
    """
    with open(filepath, 'w') as fp:
        json.dump(d, fp)

def load_json(filepath):
    """
    Load json from file using json.load.

    Args:
        filepath (str): Filepath with dictionary.

    Output:
        d (dict): Dictionary from filepath.
    """
    with open(filepath, 'r') as myfile:
        d = json.load(myfile)
    return d

def load_last_line(filepath):
    """Load json in last line of given file into dictionary.

    Args:
        filepath (str): Path to file with json.

    Returns:
        last_line (dict): Last line in file loaded as a dictionary.

    Usage Example:
        user_dict = load_last_line(page_info_filepath)
    """
    with open(filepath, "r") as myfile:
        last_line = json.loads(myfile.readlines()[-1])
    return last_line

def add_new_line(new_line,filepath):
    """Add json in last line of given file as a dictionary.

    Args:
        filepath (str): Path to file with json.
        new_line (dict): New line to be added to file.

    Returns: None

    Usage Example:
        add_new_line(user_dict,page_info_filepath)
    """
    with open(filepath, "a") as myfile:
        myfile.write(json.dumps(new_line) + '\n')

def write_text(text,filepath):
    """Write text to file.

    Args:
        filepath (str): Path to file.
        text (str): Text written to file.

    Returns: None
    """
    with open(filepath, "w") as myfile:
        myfile.write(text)
