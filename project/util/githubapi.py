"""Util to simplify interaction with the github api"""

import requests
import getpass
import sys

from util import keyringhandler


def get_input_string(msg):
    """Tries to get user input, kills application on KeyboardInterrupt"""
    try:
        return input(msg)
    except KeyboardInterrupt:
        # Graceful exit, using sys
        sys.exit()


def get_reformatted_repo_json(github_session):
    """Returns only the used information from each repo json"""
    ret_json = {}
    for repo_json in github_session.get_repos():
        ret_json[repo_json['name']] = repo_json['pushed_at']
    return ret_json


class Github_ApiHandler(object):
    """Github session class for a given github account"""

    def __init__(self, usr_file="", base_url="https://api.github.com", auth=None):
        """Class initializer"""
        # Api entrypoint
        self.base_url = base_url

        # requests session
        self.github_session = requests.Session()

        # Remaining rate limit default, 2 for auth request
        self.remaining_rate_limit = 2

        # Get auth
        if auth:
            self.auth = auth
            self.usr = self.auth[0]
        else:
            # Get from manual input if no auth specified
            self.usr = get_input_string("Username: ")
            psw = getpass.getpass()
            self.auth = (self.usr, psw)

        # Validate auth
        if not self.__validate_auth(self.auth):
            raise requests.ConnectionError("Invalid authentication")
        else:
            self.github_session.auth = self.auth
            self.__set_rate_limit()

            keyringhandler.set_username(self.auth[0], usr_file)
            keyringhandler.set_password(self.auth[0], self.auth[1])

    def __get_entrypoint(self, entrypoint, payload={}):
        """Sends a get request using the github session"""        
        if self.remaining_rate_limit > 0:
            self.remaining_rate_limit -= 1

            try:
                return self.github_session.get(self.base_url + entrypoint, params=payload)
            except ConnectionError:
                raise ConnectionError("Error: Unable to connect to Github!")
        else:
            raise ConnectionError("Error: Rate limit exceeded or not set, please wait until the next hourly reset.")

    def __validate_auth(self, auth):
        """Returns true, if valid auth"""
        res = self.__get_entrypoint("/")

        return (res.status_code == 200)

    def __set_rate_limit(self):
        """Sets the remaining rate limit"""
        res = self.__get_entrypoint("/rate_limit")

        if res.status_code == 200:
            self.remaining_rate_limit = res.json()['rate']['remaining']
        else:
            raise ConnectionError("Error: Unable to connect to Github!")

    def get_repos(self):
        """Returns a list of all repos for the authenticated user"""
        res = self.__get_entrypoint("/user/repos")

        if res.status_code == 200:
            return res.json()
        else:
            raise ConnectionError("Error: Unable to information about repos!")
