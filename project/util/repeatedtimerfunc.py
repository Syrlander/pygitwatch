"""Util function to work with the repeatedtimer util.
This is in a class so variables like the self.previous_repos can imitate
the properties of a global variable without being creating overly messy code."""
from util import sendnotification as SN
from util import githubapi
from util import jsonfilehandler


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
        # Get current repos data
        current_repos = githubapi.get_reformatted_repo_json(self.github_session)

        # Check for changes between the two json objects
        for repo in current_repos:
            try:
                if self.previous_repos[repo] != current_repos[repo]:
                    SN.send_notification(self.app_name, "Changes made to repo: " + repo)
            except KeyError:
                # This error means that the repo can be found in storage, therefore it's a new repo
                SN.send_notification(self.app_name, "Added repo: " + repo)

        # Check for deleted repos
        for repo in self.previous_repos:
            if repo not in current_repos:
                SN.send_notification(self.app_name, "Deleted repo: " + repo)

        # Set previous repos to current
        self.previous_repos = current_repos

        # Save current
        jsonfilehandler.save_file(self.temp_storage_file, current_repos)