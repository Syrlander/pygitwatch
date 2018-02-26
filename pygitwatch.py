#!/usr/bin/python3

import os

import Github_Api
import Repeated_Timer

# For debug pretty printing json
import json


def pp_json(j):
    """Pretty prints given json (Debugging)"""
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


def Main():
    """Program entrypoint"""
    # Test token: 53ef1c95a035a7e7084077ce8dd2ec5af04123fb
    github_session = Github_Api.Github_ApiHandler(
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
    # rt = Repeated_Timer.RepeatedTimer(hello, 5.0, "World")

if __name__ == '__main__':
    Main()
