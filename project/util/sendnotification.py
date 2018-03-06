"""Util to send push notifications"""

import sys
import os


def send_notification(title, content):
    """Displays a push notification on the desktop, using notify-send"""

    # Construct the command
    resp = os.system("notify-send '" + title + "' " + "'" + content + "'")

    # Unsuccessful execution; exit with the given command respons
    if resp != 0:
        sys.exit(resp)