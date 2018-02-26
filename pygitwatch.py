#!/usr/bin/python3

import os
import sys
import requests

# For the RepeatedTimer class
import sched
import time

# For test pretty printing json
import json


def pp_json(j):
    """Pretty prints given json"""
    parsed = json.loads(j)
    print(json.dumps(parsed, indent=4, sort_keys=True))


def send_notification(title, content):
    """Displays a push notification on the desktop, using notify-send.
    (This makes the script dependant on notify-send
    Returns True: successful notification execution
            False: unsuccessful notification execution"""

    # Construct the command
    base_command = "notify-send"
    resp = os.system(base_command + " '" + title + "' " + "'" + content + "'")

    # 0 == successfully executed
    return not bool(resp)


def get_input_string(msg):
    """Tries to get user input, kills application on KeyboardInterrupt"""
    try:
        return input(msg)
    except KeyboardInterrupt:
        # Graceful exit, using sys
        sys.exit()


class Github_ApiHandler(object):
    """Class holds a login session for a given github account"""

    def __init__(self, base_url="https://api.github.com/", access_token=""):
        """Class constructor"""
        # Default Github api base url
        self.base_url = base_url

        # Github username
        self.username = ""

        # Remaining rate limit default, 1 for auth request
        self.remaining_rate_limit = 2

        # Prompt for account access token, if non given
        if access_token:
            self.access_token = access_token
        else:
            print("Access tokens can be generated at: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/")
            self.access_token = get_input_string("Github access token: ")

        # Validate access token (auth)
        if self.__auth_validate():
            print("Valid access token!")

            # Set current rate limit
            self.__set_rate_limit()

            # Set username
            self.__set_username()
        else:
            raise Exception("Error: Invalid access token!")

    def __send_get(self, url, payload={}):
        """Sends a get request using the given url and optional payload"""
        # Append the access token to each get request
        payload['access_token'] = self.access_token

        try:
            if self.remaining_rate_limit > 0:
                # Decrement rate limit
                self.remaining_rate_limit -= 1
                return requests.get(url, params=payload)
            else:
                raise Exception("Error: Rate limit exceeded or not set, please wait until the next hourly reset.")
        except ConnectionError:
            raise Exception("Error: Unable to connect to Github!")

    def __auth_validate(self):
        """Try to authenticate the access token, using basic auth
            Returns: True (success, valid access token)
                     False (failure, invalid access token)"""
        res = self.__send_get(self.base_url)

        return (res.status_code == 200)

    def __set_username(self):
        """Sets the username corresponding to the given access token"""
        res = self.__send_get(self.base_url + "user")

        # Find the username via. the json respons
        if res.status_code == 200:
            try:
                self.username = res.json()['login']
            except KeyError:
                raise Exception("Error: Unable to retrieve username! (access token possibly configured incorrectly)")    
        else:
            raise Exception("Error: Unable to connect to github!")

    def __set_rate_limit(self):
        """Sets the remaining rate limit"""
        res = self.__send_get(self.base_url + "rate_limit")

        if res.status_code == 200:
            self.remaining_rate_limit = res.json()['rate']['remaining']
        else:
            raise Exception("Error: Unable to connect to Github!")

    def get_repos(self):
        """Returns a list of all repos for the authenticated user"""
        res = self.__send_get(self.base_url + "user/repos")

        if res.status_code == 200:
            return res.json()
        else:
            raise Exception("Error: Unable to retrieve repos! (access token possibly configured incorrectly)")

    def get_repo_events(self, username, repo_name):
        """Returns all latest events from repo"""
        res = self.__send_get(self.base_url + "repos/" + username + "/" + repo_name + "/events")

        if res.status_code == 200:
            return res.json()
        raise Exception("Error: Invalid username or repository name.")


class RepeatedTimer(object):
    """Timer class which executes a given function every interval (seconds)"""

    def __init__(self, func, interval, *args, **kwargs):
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.interval = interval

        # Start repeating
        self.start()

    def __run(self):
        """Triggers the function"""
        self.func(*self.args, **self.kwargs)
        self.scheduler.enter(self.interval, 1, self.__run)

    def start(self):
        """Starts the repeating timer"""
        self.__run()
        self.scheduler.run()


def Main():
    """Program entrypoint"""
    # Test token: 53ef1c95a035a7e7084077ce8dd2ec5af04123fb
    github_session = Github_ApiHandler(
        access_token="53ef1c95a035a7e7084077ce8dd2ec5af04123fb")

    # Get list of authenticated users repos
    repos = github_session.get_repos()
    print(repos)

    # Get repo events test
    # resp = github_session.get_repo_events("Nephz", "interaktionsdesign")
    # for item in resp:
    #     print(item, end="\n\n")

    # Test of the RepeatedTimer
    # def hello(name):
    #     print("Hello " + name)
    # rt = RepeatedTimer(hello, 5.0, "World")

if __name__ == '__main__':
    Main()
