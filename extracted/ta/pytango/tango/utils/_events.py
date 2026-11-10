# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Event callbacks that print what they receive, for interactive use."""

import sys

from tango import (
    AttrConfEventData,
    DataReadyEventData,
    DevIntrChangeEventData,
    EventData,
    EventReason,
)


class EventCallback:
    """
    Useful event callback for test purposes

    Usage::

        >>> dev = tango.DeviceProxy(dev_name)
        >>> cb = tango.utils.EventCallback()
        >>> id = dev.subscribe_event("state", tango.EventType.CHANGE_EVENT, cb, [])
        2011-04-06 15:33:18.910474 sys/tg_test/1 STATE CHANGE [ATTR_VALID] ON

    Allowed format keys are:

    - date (event timestamp)
    - reception_date (event reception timestamp)
    - type (event type)
    - reason (event subscription reason)
    - dev_name (device name)
    - name (attribute name)
    - value (event value)

    .. versionadded:: 7.1.4
    """

    def __init__(
        self,
        format="{date} {dev_name} {name} {type} {reason} {value}",
        fd=sys.stdout,
        max_buf=100,
    ):
        self._msg = format
        self._fd = fd
        self._evts = []
        self._max_buf = max_buf

    def get_events(self):
        """Returns the list of events received by this callback

        :return: the list of events received by this callback
        :rtype: sequence<obj>
        """
        return self._evts

    def push_event(self, evt):
        """Internal usage only"""
        try:
            self._push_event(evt)
        except Exception as e:
            print(f"Unexpected error in callback for {evt}: {e}", file=self._fd)

    def _push_event(self, evt):
        """Internal usage only"""
        self._append(evt)
        import datetime

        now = datetime.datetime.now()

        try:
            date = self._get_date(evt)
        except Exception:
            date = now

        try:
            reception_date = evt.reception_date.todatetime()
        except Exception:
            reception_date = now

        try:
            evt_type = evt.event.upper()
        except Exception:
            evt_type = "<UNKNOWN>"

        try:
            evt_reason = str(evt.event_reason).upper()
        except Exception:
            evt_reason = "<UNKNOWN>"

        try:
            dev_name = evt.device.dev_name().upper()
        except Exception:
            dev_name = "<UNKNOWN>"

        try:
            if hasattr(evt, "attr_name"):
                attr_name = evt.attr_name.split("/")[-1].upper()
                attr_name = attr_name.removesuffix("#DBASE=NO")
            else:
                attr_name = "<N/A>"
        except Exception:
            attr_name = "<UNKNOWN>"

        try:
            value = self._get_value(evt)
        except Exception as e:
            value = f"Unexpected exception in getting event value: {e}"

        d = {
            "date": date,
            "reception_date": reception_date,
            "type": evt_type,
            "reason": evt_reason,
            "dev_name": dev_name,
            "name": attr_name,
            "value": value,
        }
        print(self._msg.format(**d), file=self._fd)

    def _append(self, evt):
        """Internal usage only"""
        evts = self._evts
        while evts and len(evts) >= self._max_buf:
            evts.pop(0)
        if self._max_buf > 0:
            evts.append(evt)

    def _get_date(self, evt):
        if isinstance(evt, EventData):
            return evt.attr_value.time.todatetime()
        else:
            return evt.get_date().todatetime()

    def _get_value(self, evt):
        """Internal usage only"""
        if evt.err:
            e = evt.errors[0]
            return f"[{e.reason}] {e.desc}"

        if isinstance(evt, EventData):
            if evt.attr_value is None and evt.event_reason == EventReason.SubSuccess:
                return "<N/A>"  # assume EventSubMode.Async which provides no value
            else:
                return f"[{evt.attr_value.quality}] {evt.attr_value.value}"
        elif isinstance(evt, AttrConfEventData):
            cfg = evt.attr_conf
            return f"label='{cfg.label}'; unit='{cfg.unit}'"
        elif isinstance(evt, DataReadyEventData):
            return f"ctr={evt.ctr}"
        elif isinstance(evt, DevIntrChangeEventData):
            return f"dev_started={evt.dev_started}; {len(evt.cmd_list)} commands; {len(evt.att_list)} attrs"
        return repr(evt)


class AsyncEventCallback(EventCallback):
    async def push_event(self, evt):
        """Internal usage only"""
        try:
            self._push_event(evt)
        except Exception as e:
            print(f"Unexpected error in callback for {evt}: {e}", file=self._fd)
