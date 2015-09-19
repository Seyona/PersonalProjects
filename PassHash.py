"""
    David Baker
    Last Revision : 09/19/2015

    Goal : Develop a safe method to hide passwords.  (or other data, but this will primarily be used for passwords)
    Note : This will not store the hashed password any where, but is supposed to be used in conjunction with a database, or
        another place that may need to store passwords
"""

import bcrypt

'''
    Hash a given input
'''


def hash_input(input):
    return bcrypt.hashpw(input.encode(encoding='UTF-8'),bcrypt.gensalt())

'''
    Checks if given input matches the hashed value
'''


def validate(input,hash):
    return bcrypt.hashpw(input.encode(encoding='UTF-8'),hash) == hash

