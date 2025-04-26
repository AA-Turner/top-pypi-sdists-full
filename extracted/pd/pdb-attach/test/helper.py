# -*- mode: python -*-
"""Helper functions and classes for tests."""
import os
from abc import ABC, abstractmethod


class BaseTest(ABC):

    @abstractmethod
    def setup_debugger(self, input_text):
        """Return a debugger."""
        raise ValueError

    def test(self):
        keep_running = True
        debugger = self.setup_debugger("keep_running=False" + os.linesep + "detach" + os.linesep)
        debugger.set_trace()

        while keep_running:
            continue

        assert keep_running is False
        debugger.stdout.seek(0)
        assert debugger.stdout.read() != ""
