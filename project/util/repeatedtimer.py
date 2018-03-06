"""Repeated timer util"""

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

        self._running = False

        # Start repeating at auto
        if auto_start:
            self.start()

    def __run(self):
        """Triggers the function"""
        if self._running:
            self.func(*self.args, **self.kwargs)
            self.event = self.scheduler.enter(self.interval, 1, self.__run)

    def start(self):
        """Starts the repeating timer"""
        self._running = True
        self.__run()
        self.scheduler.run()

    def stop(self):
        """Stops the repeating timer"""
        self._running = False
        if self.scheduler and self.event:
            self.scheduler.cancel(self.event)
