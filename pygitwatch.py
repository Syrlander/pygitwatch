#!/usr/bin/python3

import os
import sys
import requests


def get_input_string(msg):
    """Tries to get user input, kills application on KeyboardInterrupt"""
    try:
        return input(msg)
    except KeyboardInterrupt:
        # Graceful exit, using sys
        sys.exit()


class GitHub(object):
    """Class holds a login session for a given github account"""

    def __init__(self):
        """Class constructor"""
        # Default Github api base url
        self.base_url = "https://api.github.com/"

        # Get account access token
        # Test token: 53ef1c95a035a7e7084077ce8dd2ec5af04123fb
        print("Access tokens can be generated at: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/")
        self.access_token = get_input_string("Github access token: ")

        # Auth user
        if self.__auth_validate():
            print("Valid access token!")
        else:
            print("Invalid access token!")
            sys.exit()

    def __auth_validate(self):
        """Try to authenticate the user login
            Returns: True (success, valid access token)
                     False (failure, invalid access token)"""
        payload = {'access_token': self.access_token}
        res = requests.get(self.base_url, params=payload)
        if (res.status_code == 200):
            return True
        else:
            return False


def Main():
    """Program entrypoint"""
    github_session = GitHub()


if __name__ == '__main__':
    Main()
