import logging
from telnetlib import Telnet
import socket
from functools import wraps

from threading import RLock

_LOGGER = logging.getLogger(__name__)

TIMEOUT = 0.8  # Number of seconds before telnet operation timeout


class ZoneStatus(object):
    def __init__(
        self,
        zone: int, # (11 - 16)
        pa: bool,
        power: bool,
        mute: bool,
        do_not_disturb: bool,
        volume: int,  # (0 - 38)
        treble: int,  # (0 - 14) where 0 -> -7,  14 -> +7
        bass: int,  # (0 - 14) where 0 -> -7,  14 -> +7
        balance: int,  # 00 - left, 10 - center, 20 right
        source: int, # (1 - 6)
        keypad: bool,
    ):
        self.zone = zone
        self.pa = bool(pa)
        self.power = bool(power)
        self.mute = bool(mute)
        self.do_not_disturb = bool(do_not_disturb)
        self.volume = volume
        self.treble = treble
        self.bass = bass
        self.balance = balance
        self.source = source
        self.keypad = bool(keypad)

        str(self)

    def __str__(self):
        return f"""
        zone:           {self.zone},
        pa:             {self.pa},
        power:          {self.power},
        mute:           {self.mute},
        do_not_disturb: {self.do_not_disturb},
        volume:         {self.volume},
        treble:         {self.treble},
        bass:           {self.bass},
        balance:        {self.balance},
        source:         {self.source},
        keypad:         {self.keypad}
"""

    @classmethod
    def from_string(cls, match):
        if not match:
            return None
        return ZoneStatus(*[int(m) for m in match.groups()])


class WS66i(object):
    """
    WS66i amplifier interface
    """

    def open(self):
        """
        Open a connection to the Telnet server. Must be the first call.
        """
        raise NotImplementedError

    def close(self):
        """
        Close the connection to the Telnet server. Open() will need to be
        called again to communicate with the server.
        """
        raise NotImplementedError

    def zone_status(self, zone: int):
        """
        Get the structure representing the status of the zone
        :param zone: zone 11..16, 21..26, 31..36
        :return: status of the zone or None. If None is returned
        then an error was occured. This is most likely due to the
        amp being turned off. It will attempt to re-establish a
        connection if a connection was previously present.
        """
        raise NotImplementedError

    def set_power(self, zone: int, power: bool):
        """
        Turn zone on or off
        :param zone: zone 11..16, 21..26, 31..36
        :param power: True to turn on, False to turn off
        """
        raise NotImplementedError

    def set_mute(self, zone: int, mute: bool):
        """
        Mute zone on or off
        :param zone: zone 11..16, 21..26, 31..36
        :param mute: True to mute, False to unmute
        """
        raise NotImplementedError

    def set_volume(self, zone: int, volume: int):
        """
        Set volume for zone
        :param zone: zone 11..16, 21..26, 31..36
        :param volume: integer from 0 to 38 inclusive
        """
        raise NotImplementedError

    def set_treble(self, zone: int, treble: int):
        """
        Set treble for zone
        :param zone: zone 11..16, 21..26, 31..36
        :param treble: integer from 0 to 14 inclusive, where 0 is -7 treble and 14 is +7
        """
        raise NotImplementedError

    def set_bass(self, zone: int, bass: int):
        """
        Set bass for zone
        :param zone: zone 11..16, 21..26, 31..36
        :param bass: integer from 0 to 14 inclusive, where 0 is -7 bass and 14 is +7
        """
        raise NotImplementedError

    def set_balance(self, zone: int, balance: int):
        """
        Set balance for zone
        :param zone: zone 11..16, 21..26, 31..36
        :param balance: integer from 0 to 20 inclusive, where 0 is -10(left), 0 is center and 20 is +10 (right)
        """
        raise NotImplementedError

    def set_source(self, zone: int, source: int):
        """
        Set source for zone
        :param zone: zone 11..16, 21..26, 31..36
        :param source: integer from 0 to 6 inclusive
        """
        raise NotImplementedError

    def restore_zone(self, status: ZoneStatus):
        """
        Restores zone to it's previous state
        :param status: zone state to restore
        """
        raise NotImplementedError


# Helpers


def _format_zone_status_request(zone: int) -> bytes:
    return "?{}\r".format(zone).encode()


def _format_set_power(zone: int, power: bool) -> bytes:
    return "<{}PR{}\r".format(zone, "01" if power else "00").encode()


def _format_set_mute(zone: int, mute: bool) -> bytes:
    return "<{}MU{}\r".format(zone, "01" if mute else "00").encode()


def _format_set_volume(zone: int, volume: int) -> bytes:
    volume = int(max(0, min(volume, 38)))
    return "<{}VO{:02}\r".format(zone, volume).encode()


def _format_set_treble(zone: int, treble: int) -> bytes:
    treble = int(max(0, min(treble, 14)))
    return "<{}TR{:02}\r".format(zone, treble).encode()


def _format_set_bass(zone: int, bass: int) -> bytes:
    bass = int(max(0, min(bass, 14)))
    return "<{}BS{:02}\r".format(zone, bass).encode()


def _format_set_balance(zone: int, balance: int) -> bytes:
    balance = max(0, min(balance, 20))
    return "<{}BL{:02}\r".format(zone, balance).encode()


def _format_set_source(zone: int, source: int) -> bytes:
    source = int(max(1, min(source, 6)))
    return "<{}CH{:02}\r".format(zone, source).encode()


def get_ws66i(host_name: str, host_port=8080):
    """
    Return synchronous version of the WS66i interface
    :param host_name: host name, i.e. '192.168.1.123'
    :param host_port: must be 8080
    :return: synchronous implementation of WS66i interface
    """

    lock = RLock()

    def synchronized(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    class WS66iSync(WS66i):
        def __init__(self, host_name: str, host_port: int):
            self._host_name = host_name
            self._host_port = host_port
            self._connected = False
            self._telnet = Telnet()

        def __del__(self):
            self._telnet.close()

        def open(self):
            try:
                self._telnet.open(self._host_name, self._host_port, TIMEOUT)
                self._connected = True
            except (TimeoutError, OSError, socket.timeout, socket.gaierror) as err:
                raise ConnectionError from err

        @synchronized
        def close(self):
            self._telnet.close()
            self._connected = False

        def _process_request(self, request: bytes, expect_zone=None):
            """
            :param request: request that is sent to the WS66i
            :param exepct_zone: The zone to fetch data from
            :return: Match object or None
            """
            _LOGGER.debug('Sending "%s"', request)
            try:
                self._telnet.write(request)
                if expect_zone is not None:
                    # Exepct a regex string to prevent unsynchronized behavior when
                    # multiple clients communicate simultaneously with the WS66i
                    expect_str = f"({expect_zone})(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)"
                    resp = self._telnet.expect([expect_str.encode()], timeout=TIMEOUT)
                    _LOGGER.debug('Received "%s"', str(resp[1]))
                    return resp[1]

            except UnboundLocalError:
                _LOGGER.error('Bad Write Request')
            except EOFError:
                _LOGGER.error('Expect str "%s" produced no result', expect_str)
            except (TimeoutError, socket.timeout, BrokenPipeError) as error:
                _LOGGER.error('Timed-Out with exception: %s', repr(error))

            return None

        @synchronized
        def zone_status(self, zone: int):
            # Check if socket is open before reading zone status
            # Did the caller called open first?
            if not self._connected:
                _LOGGER.debug('Connection needed first')
                return None

            if not self._telnet.get_socket():
                # The connection should be established, but an error was
                # encountered (most likely amp was turned off)
                # Attempt to re-establish the connection.
                try:
                    self.open()
                except ConnectionError:
                    return None

            zone_status = ZoneStatus.from_string(self._process_request(_format_zone_status_request(zone), zone))
            if zone_status is None:
                # Amp is most likely turned off. Close the connection.
                # Future calls to zone_status will try to reconnect.
                self._telnet.close()

            return zone_status

        @synchronized
        def set_power(self, zone: int, power: bool):
            self._process_request(_format_set_power(zone, power))

        @synchronized
        def set_mute(self, zone: int, mute: bool):
            self._process_request(_format_set_mute(zone, mute))

        @synchronized
        def set_volume(self, zone: int, volume: int):
            self._process_request(_format_set_volume(zone, volume))

        @synchronized
        def set_treble(self, zone: int, treble: int):
            self._process_request(_format_set_treble(zone, treble))

        @synchronized
        def set_bass(self, zone: int, bass: int):
            self._process_request(_format_set_bass(zone, bass))

        @synchronized
        def set_balance(self, zone: int, balance: int):
            self._process_request(_format_set_balance(zone, balance))

        @synchronized
        def set_source(self, zone: int, source: int):
            self._process_request(_format_set_source(zone, source))

        @synchronized
        def restore_zone(self, status: ZoneStatus):
            self.set_power(status.zone, status.power)
            self.set_mute(status.zone, status.mute)
            self.set_volume(status.zone, status.volume)
            self.set_treble(status.zone, status.treble)
            self.set_bass(status.zone, status.bass)
            self.set_balance(status.zone, status.balance)
            self.set_source(status.zone, status.source)

    return WS66iSync(host_name, host_port)
