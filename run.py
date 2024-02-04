# Import statements
import random
import os
import bcrypt
import pwinput
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Global variables

# code taken here:
# https://www.geeksforgeeks.org/how-to-print-a-deck-of-cards-in-python/
# a list of all the suits in unicode. Resulting characters: ♣ ♥ ♦ ♠
suits = ["\u2663", "\u2665",
         "\u2666", "\u2660"]
# a list of all the ranks
ranks = ['A', '2', '3', '4', '5',
         '6', '7', '8', '9', '10',
         'J', 'Q', 'K']
# A dictonary determining the value of each card rank.
default_card_value = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}
card_value = default_card_value
highest_value = 21
dealers_score = 0
players_score = 0
credits = 1000
deck_count = 1
deck = []

# Functions


def connect_to_DB():
    '''Connect to the MongoDB database'''
    # Load the .env file before anything else
    load_dotenv()

    # Get database credentials and create connection to database
    DBCREDS = os.getenv('DBCREDS')
    global db_client
    db_client = MongoClient(DBCREDS, server_api=ServerApi('1'))
    global db
    db = db_client["blackjack"]

    # Try if the database can be accessed
    try:
        db_client.admin.command('ping')
        print("Database connected")
    except Exception as e:
        print("Database exception:", e)


def create_account():
    '''Create an account and put it into the database'''

    username = input("username: ")
    # Pwinput is used here to make the password hidden when the
    # user is typing it
    password = pwinput.pwinput(mask="*")

    # The data is made into a dictionary and put into the db
    data = {"username": username, "password": password}
    db["player"].insert_one(data)

# Both password functions reference this tutorial:
# https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/


def hash_password(password):
    '''Hashes the password'''
    # Converts the password to bytes
    bytes = password.encode("utf-8")
    # Generates salt for a more secure encryption
    salt = bcrypt.gensalt()
    # Finally hashes the password
    hash = bcrypt.hashpw(bytes, salt)



def check_password(password):
    '''Checks if the password is correct'''
    bytes = password.encode("utf-8")

    print(bcrypt.checkpw(bytes, hash))

