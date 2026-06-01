"""Protocol for EV1527 compatible devices 

EV1527, RT1527, FP1527 is a simple 24-bit RF protocol used by self-learning remote controls
and RF switches. It uses Pulse Width Modulation (PWM) encoding where a wide
pulse represents 1 and a short pulse represents 0.
The chip has a fixed 20-bit device id and 4 data pin inputs, which are typically used to encode a button or channel number.
The protocol uses a configurable time base (step duration). Common manufacturers
and their step durations:
- Logilight radio controlled sockets EC0001-EC0004: ~300 µs
- eMylo switches: ~350 µs

Encoding:
Each bit is encoded as follows:

			 ____
Bit 0    : _|    |____________
			|<1a>|<---3a---->|

			 ____________
Bit 1    : _|            |____
			|<----3a---->|<1a>|

			 ____
Sync     : _|    |___________ _ _ _ ____________
			|<1a>|<-----------31a------------->|

Telegram layout:
- Sync
- 24 data bits
- End of transmission

Common data layout:
- 20 bits: device/unit code
- 4 bits: button/channel

Reference:
https://www.seegel-systeme.de/2015/09/05/funksteckdosen-mit-dem-raspberry-pi-steuern/
http://www.sc-tech.cn/en/EV1527.pdf
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_DEFAULT_FREQUENCY = 433_920_000
_DEFAULT_REPEATS = 4
_DEFAULT_TIMEBASE_US = 275


class EV1527Command(RadioFrequencyCommand):
	"""Encode an EV1527-compatible RF command.

	Data layout:
	- 20 bits: device ID
	- 4 bits: data/button (0..15)
	"""

	device_id: int
	data: int
	timebase_us: int

	def __init__(
		self,
		*,
		device_id: int,
		data: int,
		frame_repeats: int = _DEFAULT_REPEATS,
		frequency: int = _DEFAULT_FREQUENCY,
		timebase_us: int = _DEFAULT_TIMEBASE_US,
	) -> None:
		"""Initialize the EV1527 command.

		Args:
			device_id: 20-bit device ID (0..1048575)
			data: Data/button bits (0..15)
			frame_repeats: Number of times to repeat the frame
			frequency: RF frequency in Hz
			timebase_us: Time base in microseconds
		"""

		if device_id < 0 or device_id >= (1 << 20):
			raise ValueError("device_id must be in range 0..1048575 (20-bit)")
		if data < 0 or data > 15:
			raise ValueError("data must be in range 0..15")

		super().__init__(
			frequency=frequency,
			modulation=ModulationType.OOK,
			repeat_count=frame_repeats,
		)
		self.device_id = device_id
		self.data = data
		self.timebase_us = timebase_us

	@override
	def get_raw_timings(self) -> list[int]:
		"""Compute EV1527 frame timings using PWM encoding.

		Encodes: sync + 24 data bits (LSB first).
		"""
		# PWM symbol definitions (1a = short, 3a = long)
		_symbols = {
			"0": [self.timebase_us, -3 * self.timebase_us],
			"1": [3 * self.timebase_us, -self.timebase_us],
			"sync": [self.timebase_us, -31 * self.timebase_us],
		}

		# Encode 20-bit device ID in LSB (reverse bits)
		device_id_bits = format(self.device_id, "020b")[::-1]
		symstr: list[str] = [*device_id_bits]

		# Encode 4-bit data in LSB (reverse bits)
		data_bits = format(self.data, "04b")[::-1]
		symstr.extend(data_bits)

		# Build timings: sync + symbols
		timings: list[int] = []
		timings.extend(_symbols["sync"])
		for s in symstr:
			timings.extend(_symbols[s])

		return timings
