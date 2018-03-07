"""Keyring handler for securely storing local user data"""
import keyring
from util import jsonfilehandler


def set_username(usr, file):
    """Save a password to a given file"""
    k = {'username': usr}
    jsonfilehandler.save_file(file, k)


def get_username(file):
    """Returns a username loaded from a given file, None if unable to load"""
    k = jsonfilehandler.load_file(file)
    try:
        return k['username']
    except (KeyError, TypeError):
        return None


def set_password(usr, psw):
    """Set a password using keyring"""
    keyring.set_password("system", usr, psw)


def get_password(usr):
    """Returns a retrieved password for at given username"""
    ret = keyring.get_password("system", usr)

    if not ret:
        return None
    return ret
