class State:

    def __init__(self, initial_value):

        self._value = initial_value

        self._listeners = []

    def get(self):

        return self._value

    def set(self, new_value):

        if self._value != new_value:

            self._value = new_value

            self.notify()

    def add_listener(self, callback):

        self._listeners.append(callback)

        try:

            from android.os import Looper

            if Looper.myLooper() == Looper.getMainLooper():

                callback(self._value)

                return

        except ImportError:

            pass

        try:

            from android_utils import run_on_ui_thread

            run_on_ui_thread(lambda: callback(self._value))

        except ImportError:

            callback(self._value)

    def remove_listener(self, callback):

        if callback in self._listeners:

            self._listeners.remove(callback)

    def notify(self):

        try:

            from android.os import Looper

            if Looper.myLooper() == Looper.getMainLooper():

                for listener in self._listeners:

                    listener(self._value)

                return

        except ImportError:

            pass

        try:

            from android_utils import run_on_ui_thread

            for listener in self._listeners:

                run_on_ui_thread(lambda cb=listener: cb(self._value))

        except ImportError:

            for listener in self._listeners:

                listener(self._value)

from alib.ui import Widget, Container, VBox, HBox, Card, Label, Field, Button, Icon, Toggle, RowItem, Selector, Slider, AltSeekbar, ActionRow, to_setting, show_bottom_sheet, Header, Radio
from alib.threading import main_thread, background_thread, run_on_ui, run_on_background, run_main, run_bg
from alib.reflect import get_field, set_field, call_method
from alib.db import SimpleDB
from alib.event import EventBus
from alib.net import cached_request, rate_limit

