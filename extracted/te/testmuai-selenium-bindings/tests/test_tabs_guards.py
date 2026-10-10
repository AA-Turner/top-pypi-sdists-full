# selenium-python/tests/test_tabs_guards.py
import pytest
from testmu_selenium._helpers.tabs import new_tab, close_tab


class FakeDriver:
    def __init__(self, handles):
        self.window_handles = list(handles)
        self.navigated = None
        self.switched = None

    def execute_script(self, *_):
        self.window_handles.append(f"h{len(self.window_handles)}")

    def get(self, url):
        self.navigated = url

    def close(self):
        self.window_handles.pop()

    class _S:
        def __init__(self, d):
            self.d = d
        def window(self, h):
            self.d.switched = h

    @property
    def switch_to(self):
        return FakeDriver._S(self)


def test_blank_new_tab_navigates_google():
    d = FakeDriver(["h0"])
    new_tab(d, url=None)
    assert d.navigated == "https://www.google.com"


def test_close_only_tab_recovers_and_continues():
    # TE-20324 / auteur-utils #952: the only-tab close no longer hard-fails —
    # the target being un-closable means the session would die; V2 recovers to
    # the newest handle and continues, and so do we.
    d = FakeDriver(["h0"])
    close_tab(d)  # must not raise
    assert d.window_handles == ["h0"]  # close() never ran
    assert d.switched == "h0"
