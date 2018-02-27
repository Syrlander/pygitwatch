#!/usr/bin/python3

# For the RepeatedTimer class
import sched
import time


class RepeatedTimer(object):
    """Timer class which executes a given function every interval (seconds)"""

    def __init__(self, func, interval, *args, auto_start=True, **kwargs):
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.interval = interval

        # Start repeating at auto
        if auto_start:
            self.start()

    def __run(self):
        """Triggers the function"""
        self.func(*self.args, **self.kwargs)
        self.scheduler.enter(self.interval, 1, self.__run)

    def start(self):
        """Starts the repeating timer"""
        self.__run()
        self.scheduler.run()