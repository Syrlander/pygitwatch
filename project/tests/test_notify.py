#!/usr/bin/env python3
import unittest
import os
from util import sendnotification as SN


class TestNotifyFunction(unittest.TestCase):
    """Unittest for sendnotification.py"""

    def setUp(self):
        pass

    def test_send_notify_empty_str(self):
        with self.assertRaises(SystemExit):
            SN.send_notification("", "")

    def test_send_notify_none(self):
        with self.assertRaises(TypeError):
            SN.send_notification(None, None)

    def test_send_notify_unicode(self):
        with self.assertRaises(TypeError):
            SN.send_notification("another thing".encode(), "something".encode())

    def test_send_notify_semicolon(self):
        try:
            SN.send_notification("Something", "some; gedit;")
        except Exception as e:
            self.fail("send_notifiation title not working with unicode string")

if __name__ == "__main__":
    unittest.main()
