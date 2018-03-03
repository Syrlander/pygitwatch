"""Util for custom defined system hooks"""

import sys


class ExitHooks(object):
    """Custom exit hook"""
    def __init__(self):
        # exit code and exception the program threw at exit
        self.exit_code = None
        self.exception = None
        
    def hook(self):
        """Starts the hook"""
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        """Redefinition of sys.exit"""
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc, *args):
        """Redefinition of exc_handler"""
        self.exception = exc
