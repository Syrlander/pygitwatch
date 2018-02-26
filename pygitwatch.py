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
    if (resp == 0):
        return True
    return False


def get_input_string(msg):
    """Tries to get user input, kills application on KeyboardInterrupt"""
    try:
        return input(msg)
    except KeyboardInterrupt:
        # Graceful exit, using sys
        sys.exit()


def kill_app(msg=""):
    """Prints exit message, then kills application"""
    print(msg)
    sys.exit()


class Github_ApiHandler(object):
    """Class holds a login session for a given github account"""

    def __init__(self, base_url="https://api.github.com/", access_token=""):
        """Class constructor"""
        # Default Github api base url
        self.base_url = base_url

        # Prompt for account access token, if non given
        if access_token:
            self.access_token = access_token
        else:
            print("Access tokens can be generated at: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/")
            self.access_token = get_input_string("Github access token: ")

        # Validate access token (auth)
        if self.__auth_validate():
            print("Valid access token!")
        else:
            kill_app("Error: Invalid access token!")

    def __send_get(self, url, payload=""):
        """Sends a get request using the given url and optional payload"""
        try:
            return requests.get(url, params=payload)
        except ConnectionError:
            kill_app("Error: Unable to connect to Github!")

    def __auth_validate(self):
        """Try to authenticate the access token
            Returns: True (success, valid access token)
                     False (failure, invalid access token)"""
        payload = {'access_token': self.access_token}

        res = self.__send_get(self.base_url, payload=payload)

        return (res.status_code == 200)

    def get_repos(self):
        """Gets the list of current events"""
        payload = {'access_token': self.access_token}

        res = self.__send_get(self.base_url + "user/repos", payload=payload)

        # Test print
        for item in res.json():
            print(item, end="\n\n")

        return (res.status_code == 200)


class RepeatedTimer(object):
    """Timer class which executes a given function every interval"""

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
    print(github_session.get_repos())

    # Test of the RepeatedTimer
    # def hello(name):
    #     print("Hello " + name)
    # rt = RepeatedTimer(hello, 5.0, "World")

if __name__ == '__main__':
    Main()
