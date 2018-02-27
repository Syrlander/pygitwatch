#!/usr/bin/python3

import os

import Github_Api
import Repeated_Timer
import JSON_FileHandler


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


def get_repo_json(github_session):
    """Returns repo json gotten from github api"""
    ret_json = {}
    repos_json = github_session.get_repos()
    for repo_json in repos_json:
        ret_json[repo_json['name']] = repo_json['pushed_at']
    return ret_json


def Main(app_name=""):
    """Program entrypoint"""
    # Temporary storage file name
    temp_store_name = "repo_temp_storage.json"

    # Create github session using github handler
    github_session = Github_Api.Github_ApiHandler()

    # Display starting message
    send_notification(app_name, "Connected to Github")

    # Get previous repos from temp storage
    global previous_repos
    previous_repos = JSON_FileHandler.load_file(temp_store_name)

    # If unable to find or load from temp storeage, get from github api
    if not previous_repos:
        previous_repos = get_repo_json(github_session)

    def update_checker():
        """Checks for changes between the current and the previous repo data"""
        global previous_repos

        # Get the current repos
        current_repos = get_repo_json(github_session)

        # Check for changes between the two json objects
        for repo in current_repos:
            try:
                if previous_repos[repo] != current_repos[repo]:
                    send_notification(app_name, "Changes made to repo: " + repo)
            except KeyError:
                # This error means that the repo can be found in storage, therefore it's a new repo
                send_notification(app_name, "New repo created: " + repo)

        # Check for deleted repos
        for repo in previous_repos:
            if repo not in current_repos:
                send_notification(app_name, "Deleted repo: " + repo)

        # Set previous repos to current
        previous_repos = current_repos

        # Save current
        JSON_FileHandler.save_file(temp_store_name, current_repos)

    # Create repeating timer using the update_checker
    rp_timer = Repeated_Timer.RepeatedTimer(update_checker, 30.0)

if __name__ == '__main__':
    Main(app_name="Octowatch")
