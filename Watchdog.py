
import threading

import os
import sys

class WatchdogTimer:


    def __init__(self, timeout):
        self.timeout = timeout
        self.timer = None

    def timeout_handler(self):
        print("Watchdog Timer: Code execution took too long! Taking action...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def start(self):
        if self.timer is None or not self.timer.is_alive():
            self.timer = threading.Timer(self.timeout, self.timeout_handler)
            self.timer.daemon = True
            self.timer.start()

    def stop(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()

    def setTimeout(self, timeout):
        self.timeout = timeout
