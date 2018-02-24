from sys import exit
from getpass import getpass


def get_input(msg="", get_pass=False):
    """Tries to get user input, kills application on KeyboardInterrupt"""
    try:
        if get_pass:
            # getpass(), prompts the "password: " by itself
            return getpass()
        else:
            return input(msg)
    except KeyboardInterrupt:
        # Graceful exit, using sys
        exit()


def get_username(min_len, max_len):
    """Returns a successful username entry"""
    user_inp = get_input(msg="username: ")
    while (not user_inp and min_len > len(user_inp) and max_len < len(user_inp)):
        user_inp = get_input(msg="username: ")
    return user_inp


def get_password(min_len, max_len):
    """Returns a successful password entry"""
    user_inp = get_input(get_pass=True)
    while (not user_inp and min_len > len(user_inp) and max_len < len(user_inp)):
        user_inp = get_input(get_pass=True)
    return user_inp
