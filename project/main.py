#!/usr/bin/env python3
"""Notify application to inform users of changes in their github repos"""

import sys
import os
import atexit

from util import githubapi
from util import customhooks
from util import jsonfilehandler
from util import repeatedtimer
from util import repeatedtimerfunc
from util import sendnotification as SN


def on_exit(exit_hook, app_name=""):
    """Function called upon program exit"""
    # Displays information regarding the programs exit
    if exit_hook.exit_code is not None:
        SN.send_notification(app_name, "Program exit with exit code: {0}".format(exit_hook.exit_code))
    elif exit_hook.exception is not None:
        SN.send_notification(app_name, "Program exit by exception: {0}".format(exit_hook.exception))


def main(app_name=""):
    """Program entrypoint"""
    # Create github session instance
    github_session = githubapi.Github_ApiHandler()

    # Display successful login message
    SN.send_notification(app_name, "Connected to Github as user: " + github_session.usr)

    # Create and initialize repeated timer, using the UpdateChecker instance
    UC = repeatedtimerfunc.UpdateChecker(app_name, "repo_temp_storage.json", github_session)
    rp_timer = repeatedtimer.RepeatedTimer(UC.tick, 30.0)

if __name__ == '__main__':
    # Set program name
    app_name = "Octowatch"

    # Create exit hook
    exit_hook = customhooks.ExitHook()
    exit_hook.hook()

    # Register application exit function, with the given hook
    atexit.register(on_exit, exit_hook, app_name=app_name)

    main(app_name=app_name)
