"""WiLight Protocol Support."""
import asyncio
from collections import deque
import logging
import codecs
import binascii

from ..const import (
    WL_MODELS,
    WL_DIRECTION_OFF,
    WL_DIRECTION_FORWARD,
    WL_DIRECTION_REVERSE,
    WL_SPEED_HIGH,
    WL_SPEED_LOW,
    WL_SPEED_MEDIUM,
    WL_CLOSE,
    WL_CLOSING,
    WL_OPEN,
    WL_OPENING,
    WL_STOP,
    WL_STOPPED,
)
from .support import (
    check_config_ex_len,
    get_item_sub_types,
    get_num_items,
    get_states_from_sub_item,
)
from .protocol_ex import (
    codeCmd,
    decodeData,
)

class WiLightProtocol(asyncio.Protocol):
    """WiLight device control protocol."""

    _transport = None  # type: asyncio.Transport

    def __init__(self, client, disconnect_callback=None, loop=None,
                 logger=None):
        """Initialize the WiLight protocol."""
        self._client = client
        self._loop = loop
        self._logger = logger
        self._buffer = b''
        self._disconnect_callback_protocol = disconnect_callback
        self._timeout = None
        self._cmd_timeout = None
        self._keep_alive = None

    def connection_made(self, transport):
        """Initialize protocol transport."""
        self._transport = transport
        self._reset_timeout()

    def _send_keepalive_packet(self):
        """Send a keep alive packet."""
        packet = self.format_packet("000000", self._client._num_serial)
        asyncio.get_running_loop().create_task(self._client._send(packet))

    def _reset_timeout(self):
        """Reset timeout for date keep alive."""
        if self._timeout:
            self._timeout.cancel()
        self._timeout = self._loop.call_later(self._client._timeout,
                                              self._transport.close)
        if self._keep_alive:
            self._keep_alive.cancel()
        self._keep_alive = self._loop.call_later(
            self._client._keep_alive_interval,
            self._send_keepalive_packet)

    def reset_cmd_timeout(self):
        """Reset timeout for command execution."""
        if self._cmd_timeout:
            self._cmd_timeout.cancel()
        self._cmd_timeout = self._loop.call_later(self._client._timeout,
                                                 self._transport.close)

    def data_received(self, data):
        """Add incoming data to buffer."""
        self._reset_timeout()
        #self._buffer = data
        self._buffer = decodeData(data)
        if self._valid_packet(self, self._buffer):
            self._handle_packet(self._buffer)

    @staticmethod
    def _valid_packet(self, packet):
        """Validate incoming packet."""
        if packet[0:1] != b'&':
            return False
        if self._client._model == "0001":
            if len(packet) < 80:
                return False
        elif self._client._model == "0002":
            if len(packet) < 82:
                return False
        elif self._client._model == "0100":
            if len(packet) < 90:
                return False
        elif self._client._model == "0102":
            if len(packet) < 84:
                return False
        elif self._client._model == "0103":
            if len(packet) < 82:
                return False
        elif self._client._model == "0104":
            if len(packet) < 51:
                return False
        elif self._client._model == "0105":
            if len(packet) < 81:
                return False
        elif self._client._model == "0107":
            if len(packet) < 40:
                return False
        elif self._client._model == "0110":
            if len(packet) < 40:
                return False
        elif self._client._model == "0112":
            if len(packet) < 30:
                return False
        b_num_serial = self._client._num_serial.encode()
        for i in range(0, 12):
            if packet[i + 1] != b_num_serial[i]:
                return False
        return True

    def _handle_packet(self, packet):
        """Parse incoming packet."""
        if self._client._model == "0001":
            self._handle_0001_packet(packet)
        elif self._client._model == "0002":
            self._handle_0002_packet(packet)
        elif self._client._model == "0100":
            self._handle_0100_packet(packet)
        elif self._client._model == "0102":
            self._handle_0102_packet(packet)
        elif self._client._model == "0103":
            self._handle_0103_packet(packet)
        elif self._client._model == "0104":
            self._handle_0104_packet(packet)
        elif self._client._model == "0105":
            self._handle_0105_packet(packet)
        elif self._client._model == "0107":
            self._handle_0107_packet(packet)
        elif self._client._model == "0110":
            self._handle_0110_packet(packet)
        elif self._client._model == "0112":
            self._handle_0112_packet(packet)

    def _handle_0001_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0002_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0100_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            brightness = int(packet[26+3*index:29+3*index])
            states[format(index, 'x')] = {"on": on, "brightness": brightness}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("brightness" in client_state):
                if (client_state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_0102_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0103_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            motor_state = WL_STOPPED
            if (packet[23:24] == b'1'):
                motor_state = WL_OPENING
            if (packet[23:24] == b'0'):
                motor_state = WL_CLOSING
            position_target = int(packet[24:27])
            position_current = int(packet[27:30])
            states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}
            changed = False
            if ("motor_state" in client_state):
                if (client_state["motor_state"] != motor_state):
                    changed = True
            else:
                changed = True
            if ("position_target" in client_state):
                if (client_state["position_target"] != position_target):
                    changed = True
            else:
                changed = True
            if ("position_current" in client_state):
                if (client_state["position_current"] != position_current):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}

        self._handle_packet_end(states, changes)

    def _handle_0104_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 2):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}

            if index == 0:

                on = (packet[23:24] == b'1')
                states[format(index, 'x')] = {"on": on}
                changed = False
                if ("on" in client_state):
                    if (client_state["on"] is not on):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self._client._states[format(index, 'x')] = {"on": on}

            elif index == 1:

                direction = WL_DIRECTION_OFF
                if (packet[24:25] == b'0'):
                    direction = WL_DIRECTION_FORWARD
                if (packet[24:25] == b'2'):
                    direction = WL_DIRECTION_REVERSE
                speed = WL_SPEED_LOW
                if (packet[25:26] == b'1'):
                    speed = WL_SPEED_MEDIUM
                if (packet[25:26] == b'2'):
                    speed = WL_SPEED_HIGH
                states[format(index, 'x')] = {"direction": direction, "speed": speed}
                changed = False
                if ("direction" in client_state):
                    if (client_state["direction"] != direction):
                        changed = True
                else:
                    changed = True
                if ("speed" in client_state):
                    if (client_state["speed"] != speed):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self._client._states[format(index, 'x')] = {"direction": direction, "speed": speed}

        self._handle_packet_end(states, changes)

    def _handle_0105_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 2):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            timer_target = int(packet[25+5*index:30+5*index])
            timer_current = int(packet[35+5*index:40+5*index])
            trigger_1 = "" + packet[48+index:56].decode()
            trigger_2 = "" + packet[56+index:64].decode()
            trigger_3 = "" + packet[64+index:72].decode()
            trigger_4 = "" + packet[72+index:80].decode()
            states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current, "trigger_1": trigger_1, "trigger_2": trigger_2, "trigger_3": trigger_3, "trigger_4": trigger_4}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("timer_target" in client_state):
                if (client_state["timer_target"] != timer_target):
                    changed = True
            else:
                changed = True
            if ("timer_current" in client_state):
                if (client_state["timer_current"] != timer_current):
                    changed = True
            else:
                changed = True
            if ("trigger_1" in client_state):
                if (client_state["trigger_1"] != trigger_1):
                    changed = True
            else:
                changed = True
            if ("trigger_2" in client_state):
                if (client_state["trigger_2"] != trigger_2):
                    changed = True
            else:
                changed = True
            if ("trigger_3" in client_state):
                if (client_state["trigger_3"] != trigger_3):
                    changed = True
            else:
                changed = True
            if ("trigger_4" in client_state):
                if (client_state["trigger_4"] != trigger_4):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current, "trigger_1": trigger_1, "trigger_2": trigger_2, "trigger_3": trigger_3, "trigger_4": trigger_4}

        self._handle_packet_end(states, changes)

    def _handle_0107_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23:24] == b'1')
            hue = int(packet[36:39])
            saturation = int(packet[39:42])
            brightness = int(packet[42:45])
            states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("hue" in client_state):
                if (client_state["hue"] != hue):
                    changed = True
            else:
                changed = True
            if ("saturation" in client_state):
                if (client_state["saturation"] != saturation):
                    changed = True
            else:
                changed = True
            if ("brightness" in client_state):
                if (client_state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_0110_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            brightness = int(packet[26+3*index:29+3*index])
            states[format(index, 'x')] = {"on": on, "brightness": brightness}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("brightness" in client_state):
                if (client_state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_0112_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self._client._states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self._client._states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_packet_end(self, states, changes):
        """Finalizes packet handling."""
        for index in changes:
            for status_cb in self._client._status_callbacks.get(index, []):
                status_cb(states[index])
        if self._cmd_timeout:
            self._cmd_timeout.cancel()

    @staticmethod
    def format_packet(command, num_serial):
        """Format packet to be sent."""
        #return b"!" + num_serial.encode() + command.encode()
        return codeCmd(command, num_serial)

    def connection_lost(self, exc):
        """Log when connection is closed, if needed call callback."""
        if exc:
            self._logger.error('disconnected due to error')
        else:
            self._logger.info('disconnected because of close/abort.')
        if self._keep_alive:
            self._keep_alive.cancel()
        if self._disconnect_callback_protocol:
            asyncio.ensure_future(self._disconnect_callback_protocol(), loop=self._loop)

class WiLightClient:
    """WiLight client wrapper class."""

    def __init__(self, device_id=None, host=None,
                 port=None, model=None, config_ex=None,
                 disconnect_callback=None, reconnect_callback=None,
                 loop=None, logger=None, timeout=None, reconnect_interval=None,
                 keep_alive_interval=None):
        # Initialize the WiLight client wrapper.
        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
        self._num_serial = device_id[2:]
        self._device_id = device_id
        self._host = host
        self._port = port
        self._model = model
        self._config_ex = config_ex
        self._transport = None
        self._protocol = None
        self._is_connected = False
        self._reconnect = True
        self._timeout = timeout
        self._reconnect_interval = reconnect_interval
        self._keep_alive_interval = keep_alive_interval
        self._disconnect_callback = disconnect_callback
        self._reconnect_callback = reconnect_callback
        self._status_callbacks = {}
        self._states = {}
        self._lock = asyncio.Lock()
        self._reconnect_timer = None

    async def setup(self, can_reconnect):
        """Set up the connection with automatic retry."""
        self._is_connected = False
        if self._reconnect_timer:
            self._reconnect_timer.cancel()
        fut = self._loop.create_connection(
            lambda: WiLightProtocol(
                self,
                disconnect_callback=self.handle_disconnect_callback,
                loop=self._loop,
                logger=self._logger),
            host=self._host,
            port=self._port)
        try:
            self._transport, self._protocol = \
                await asyncio.wait_for(fut, timeout=self._timeout)
        except asyncio.TimeoutError:
            self._logger.warning("Could not connect due to timeout error.")
        except OSError as exc:
            self._logger.warning("Could not connect due to error: %s",
                                str(exc))
        else:
            self._is_connected = True
            if self._reconnect_callback:
                self._reconnect_callback()
        if can_reconnect and not self._is_connected:
            self._reconnect_timer = self._loop.call_later(
                self._reconnect_interval,
                self.do_reconnect
            )

    def do_reconnect(self):
        """Reconnect transport."""
        asyncio.ensure_future(self.setup(True), loop=self._loop)

    def stop(self):
        """Shut down transport."""
        self._reconnect = False
        if self._transport:
            self._transport.close()

    async def handle_disconnect_callback(self):
        """Reconnect automatically unless stopping."""
        self._is_connected = False
        if self._disconnect_callback:
            self._disconnect_callback()
        if self._reconnect:
            await self.setup(True)
            self._protocol.reset_cmd_timeout()
            packet = self._protocol.format_packet("000000", self._num_serial)
            await self._send(packet)

    def register_status_callback(self, callback, index):
        """Register a callback which will fire when state changes."""
        if self._status_callbacks.get(index, None) is None:
            self._status_callbacks[index] = []
        self._status_callbacks[index].append(callback)

    @property
    def is_connected(self):
        return self._is_connected

    async def _send(self, packet):
        """Add packet to send queue."""
        self._protocol.reset_cmd_timeout()
        async with self._lock:
            self._protocol._transport.write(packet)
            await asyncio.sleep(0.1)

    async def turn_on(self, index=None):
        """Turn on device."""
        if index is not None:
            commands_on = ["001000", "003000", "005000"]
            packet = self._protocol.format_packet(commands_on[int(index)], self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def turn_off(self, index=None):
        """Turn off device."""
        if index is not None:
            commands_off = ["002000", "004000", "006000"]
            packet = self._protocol.format_packet(commands_off[int(index)], self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_brightness(self, index=None, brightness=None):
        """Set device's brightness."""
        if (index is not None and brightness is not None):
            commands_brigthness = ["007003", "008003", "009003"]
            command = commands_brigthness[int(index)] + '{:0>3}'.format(brightness)
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_hs_color(self, index=None, hue=None, saturation=None):
        """Set device's hue and saturation."""
        if (index is not None and hue is not None and saturation is not None):
            command = "012006" + '{:0>3}'.format(hue) + '{:0>3}'.format(saturation)
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_hsb_color(self, index=None, hue=None, saturation=None, brightness=None):
        """Set device's hue, saturation and brightness."""
        if (index is not None and hue is not None and saturation is not None and brightness is not None):
            command = "011009" + '{:0>3}'.format(hue) + '{:0>3}'.format(saturation) + '{:0>3}'.format(brightness)
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_fan_direction(self, index=None, direction=None):
        """Set fan direction."""
        if (index is not None and direction is not None):
            command = "000000"
            if direction == WL_DIRECTION_FORWARD:
                command = "003000"
            elif direction == WL_DIRECTION_OFF:
                command = "004000"
            elif direction == WL_DIRECTION_REVERSE:
                command = "005000"
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_fan_speed(self, index=None, speed=None):
        """Set fan speed."""
        if (index is not None and speed is not None):
            command = "000000"
            if speed == WL_SPEED_LOW:
                command = "006000"
            elif speed == WL_SPEED_MEDIUM:
                command = "007000"
            elif speed == WL_SPEED_HIGH:
                command = "008000"
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def cover_command(self, index=None, cv_command=None):
        """Send cover command."""
        if (index is not None and cv_command is not None):
            command = "000000"
            if cv_command == WL_OPEN:
                command = "001000"
            elif cv_command == WL_CLOSE:
                command = "002000"
            elif cv_command == WL_STOP:
                command = "003000"
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_cover_position(self, index=None, position=None):
        """Set cover position."""
        if (index is not None and position is not None):
            command = "007003" + '{:0>3}'.format(position)
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_switch_time(self, index=None, target_time=None):
        """Set switch time."""
        if (index is not None and target_time is not None):
            commands_target_time = ["005005", "006005"]
            command = commands_target_time[int(index)] + '{:0>5}'.format(target_time)
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_switch_trigger_1(self, index=None, trigger=None):
        """Set switch trigger 1."""
        if (trigger is not None and (len(trigger) == 8)):
            command = "020008" + trigger
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_switch_trigger_2(self, index=None, trigger=None):
        """Set switch trigger 2."""
        if (trigger is not None and (len(trigger) == 8)):
            command = "021008" + trigger
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_switch_trigger_3(self, index=None, trigger=None):
        """Set switch trigger 3."""
        if (trigger is not None and (len(trigger) == 8)):
            command = "022008" + trigger
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def set_switch_trigger_4(self, index=None, trigger=None):
        """Set switch trigger 4."""
        if (trigger is not None and (len(trigger) == 8)):
            command = "023008" + trigger
            packet = self._protocol.format_packet(command, self._num_serial)
        else:
            packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

    async def status(self, index=None):
        """Get current device status."""
        packet = self._protocol.format_packet("000000", self._num_serial)
        await self._send(packet)

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
class DummyClient:
    """Dummy client wrapper class."""
    def __init__(self, model=None, config_ex=None):
        self._model = model
        self._config_ex = config_ex
        self._is_connected = True
        self._status = self._config_status()
        self._status_callbacks = {}
        self._config_status()

    def _config_status(self):
        status = {}

        if self._model not in WL_MODELS:
            return status

        if not check_config_ex_len(self._model, self._config_ex):
            return status

        num_items = get_num_items(self._model, self._config_ex)

        for i in range(0, num_items):
            index = f"{i:01x}"
            item_sub_type = get_item_sub_types(i+1, self._model, self._config_ex)
            state = get_states_from_sub_item(item_sub_type)
            status[index] = state

        return status

    async def _update(self, index=None):
        self._status_callbacks[index](self._status[index])

    def register_status_callback(self, callback, index):
        """Register a callback which will fire when state changes."""
        self._status_callbacks[index] = callback

    def stop(self):
        pass

    def set_status(self, status, index):
        """Inicializa estado para o index"""
        self._status[index] = status

    def set_is_connected(self, connected):
        self._is_connected = connected

    @property
    def is_connected(self):
        return self._is_connected

    async def status(self, index=None):
        if index is not None:
            await self._update(index)

    async def turn_on(self, index=None):
        if index is not None:
            self._status[index]["on"] = True
            await self._update(index)

    async def turn_off(self, index=None):
        if index is not None:
            self._status[index]["on"] = False
            await self._update(index)

    async def set_brightness(self, index=None, brightness=None):
        if (index is not None and brightness is not None):
            self._status[index]["brightness"] = brightness
            if brightness == 0:
                self._status[index]["on"] = False
            else:
                self._status[index]["on"] = True
            await self._update(index)

    async def set_hs_color(self, index=None, hue=None, saturation=None):
        if (index is not None and hue is not None and saturation is not None):
            self._status[index]["hue"] = hue
            self._status[index]["saturation"] = saturation
            await self._update(index)

    async def set_hsb_color(
        self, index=None, hue=None, saturation=None, brightness=None
    ):
        if (index is not None and hue is not None and saturation is not None and brightness is not None):
            self._status[index]["hue"] = hue
            self._status[index]["saturation"] = saturation
            self._status[index]["brightness"] = brightness
            if brightness == 0:
                self._status[index]["on"] = False
            else:
                self._status[index]["on"] = True
            await self._update(index)

    async def cover_command(self, index=None, cv_command=None):
        """Send cover command."""
        if (index is not None and cv_command is not None):
            if cv_command == WL_OPEN:
                motor_state = WL_OPENING
                position_target = 0
            elif cv_command == WL_CLOSE:
                motor_state = WL_CLOSING
                position_target = 255
            elif cv_command == WL_STOP:
                motor_state = WL_STOPPED
                position_target = 127
            self._status[index]["motor_state"] = motor_state
            self._status[index]["position_target"] = position_target
            self._status[index]["position_current"] = 127
            await self._update(index)

    async def set_cover_position(self, index=None, position=None):
        if (index is not None and position is not None):
            self._status[index]["motor_state"] = WL_STOPPED
            self._status[index]["position_target"] = position
            self._status[index]["position_current"] = position
            await self._update(index)

    async def set_fan_direction(self, index=None, direction=None):
        if (index is not None and direction is not None):
            self._status[index]["direction"] = direction
            await self._update(index)

    async def set_fan_speed(self, index=None, speed=None):
        if (index is not None and speed is not None):
            self._status[index]["speed"] = speed
            await self._update(index)

    async def set_switch_time(self, index=None, target_time=None):
        if (index is not None and target_time is not None):
            self._status[index]["timer_target"] = target_time
            await self._update(index)

    async def set_switch_trigger_1(self, index=None, trigger=None):
        """Set switch trigger 1."""
        if (trigger is not None and (len(trigger) == 8)):
            self._status[index]["trigger_1"] = trigger
            await self._update(index)

    async def set_switch_trigger_2(self, index=None, trigger=None):
        """Set switch trigger 2."""
        if (trigger is not None and (len(trigger) == 8)):
            self._status[index]["trigger_2"] = trigger
            await self._update(index)

    async def set_switch_trigger_3(self, index=None, trigger=None):
        """Set switch trigger 3."""
        if (trigger is not None and (len(trigger) == 8)):
            self._status[index]["trigger_3"] = trigger
            await self._update(index)

    async def set_switch_trigger_4(self, index=None, trigger=None):
        """Set switch trigger 4."""
        if (trigger is not None and (len(trigger) == 8)):
            self._status[index]["trigger_4"] = trigger
            await self._update(index)
