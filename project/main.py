#!/usr/bin/env python3
"""Notify application to inform users of changes in their github repos"""

import sys
import os
import atexit

from util import githubapi
from util import customhooks
from util import jsonfilehandler
from util import repeatedtimer
from util import sendnotification as SN


def on_exit(exit_hook, app_name=""):
    """Function called upon program exit"""
    # Displays information regarding the programs exit
    if exit_hook.exit_code is not None:
        SN.send_notification(app_name, "Program exit with exit code: {0}".format(exit_hook.exit_code))
    elif exit_hook.exception is not None:
        SN.send_notification(app_name, "Program exit by exception: {0}".format(exit_hook.exception))


class UpdateChecker(object):
    """Checks for changes between the current and the previous repo data"""

    def __init__(self, app_name, temp_storage_file, github_session):
        self.app_name = app_name
        self.temp_storage_file = temp_storage_file
        self.github_session = github_session

        # Load initial repo data
        self.previous_repos = jsonfilehandler.load_file(temp_storage_file)

        # If not found in temp storage file
        if not self.previous_repos:
            self.previous_repos = githubapi.get_reformatted_repo_json(self.github_session)

    def tick(self):
        """Function which makes the checks between the repo data"""
        print("Tick")
        # Get current repos data
        current_repos = githubapi.get_reformatted_repo_json(self.github_session)

        # Check for changes between the two json objects
        for repo in current_repos:
            try:
                if self.previous_repos[repo] != current_repos[repo]:
                    SN.send_notification(self.app_name, "Changes made to repo: " + repo)
            except KeyError:
                # This error means that the repo can be found in storage, therefore it's a new repo
                SN.send_notification(app_name, "Added repo: " + repo)

        # Check for deleted repos
        for repo in self.previous_repos:
            if repo not in current_repos:
                SN.send_notification(app_name, "Deleted repo: " + repo)

        # Set previous repos to current
        self.previous_repos = current_repos

        # Save current
        jsonfilehandler.save_file(self.temp_storage_file, current_repos)


def main(app_name=""):
    """Program entrypoint"""
    # Create github session instance
    github_session = githubapi.Github_ApiHandler()

    # Display successful login message
    SN.send_notification(app_name, "Connected to Github")

    # Create and initialize repeated timer, using the UpdateChecker instance
    UC = UpdateChecker(app_name, "repo_temp_storage.json", github_session)
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
