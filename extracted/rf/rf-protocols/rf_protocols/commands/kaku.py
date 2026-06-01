"""Protocol for KAKU compatible devices.

Pulse Position Modulation with 32 or 36 symbols, used by self-learning
Intertechno-type sockets and compatible devices (for example some Hama models).

Symbols use a time base ``T``:

			 ____      ____
Bit 0    : _|    |____|    |____________________
			|<1T>|<1T>|<1T>|<--------5T-------->|

			 ____                      ____
Bit 1    : _|    |____________________|    |____
			|<1T>|<--------5T-------->|<1T>|<1T>|

			 ____      ____
Bit X    : _|    |____|    |____
			|<1T>|<1T>|<1T>|<1T>|

			 ____
Sync     : _|    |_________ _ _ _ ________
			|<1T>|<----------11T--------->|

			 ____
Pause    : _|    |___________ _ _ _ ____________
			|<1T>|<-----------39T-------------->|

Telegram layout:
- Sync
- 32 or 36 symbols
- Pause

Each transmission is typically repeated four times.

Common bit assignment for KAKU-style devices:
- 26 bits system code
- 1 bit group (0=single, 1=group)
- 1 bit on/off
- 4 bits channel

Dimming commands:
- 26 bits system code
- 1 bit group (0=single, 1=group)
- 1 bit X
- 4 bits channel
- 4 bits dim level (0-15)

Manufacturer-specific notes from the reference:
- Intertechno (self-learning): step duration around 275 us
- Hama 00121938: similar format, step duration around 250 us, inverted channel bits

Reference chapter:
https://www.seegel-systeme.de/2015/09/05/funksteckdosen-mit-dem-raspberry-pi-steuern/
"""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

_DEFAULT_FREQUENCY = 433_920_000
_DEFAULT_REPEATS = 4
_DEFAULT_TIMEBASE_US = 275


class KakuCommand(RadioFrequencyCommand):
	"""Encode a KAKU-compatible PPM frame.

	Data layout is either:
	- 32 symbols: 26-bit id, group bit, on/off bit, 4-bit channel
	- 36 symbols: 26-bit id, group bit, X symbol, 4-bit channel, 4-bit dim level
	"""

	id: int
	group: bool
	channel: int
	on: bool | None
	dimlevel: int | None
	timebase_us: int

	def __init__(
		self,
		*,
		id: int,
		group: bool,
		channel: int | None = None,
		on: bool | None = None,
		dimlevel: int | None = None,
		frame_repeats: int = _DEFAULT_REPEATS,
		frequency: int = _DEFAULT_FREQUENCY,
		timebase_us: int = _DEFAULT_TIMEBASE_US,
	) -> None:
		"""Initialize the KAKU command."""

		if id < 0 or id >= (1 << 26):
			raise ValueError("id must be in range 0..67108863 (26-bit)")
		if channel is None:
			if not group:
				raise ValueError("channel is required when group is False")
			channel = 1
		if channel < 1 or channel > 16:
			raise ValueError("channel must be in range 1..16")
		if (on is None) == (dimlevel is None):
			raise ValueError("provide exactly one of 'on' or 'dimlevel'")
		if dimlevel is not None and (dimlevel < 0 or dimlevel > 100):
			raise ValueError("dimlevel must be in range 0..100")

		super().__init__(
			frequency=frequency,
			modulation=ModulationType.OOK,
			repeat_count=frame_repeats,
		)
		self.id = id
		self.group = group
		self.channel = channel
		self.on = on
		self.dimlevel = dimlevel
		self.timebase_us = timebase_us

	@override
	def get_raw_timings(self) -> list[int]:
		"""Compute KAKU PPM frame timings."""
		_symbols = {
			"0": [self.timebase_us, -self.timebase_us, self.timebase_us, -5 * self.timebase_us],
			"1": [self.timebase_us, -5 * self.timebase_us, self.timebase_us, -self.timebase_us],
			"X": [self.timebase_us, -self.timebase_us, self.timebase_us, -self.timebase_us],
			"sync": [self.timebase_us, -11 * self.timebase_us],
			"pause": [self.timebase_us, -39 * self.timebase_us],
		}

		# add ID and group bit
		symstr: list[str] = [*format(self.id, "026b"), "1" if self.group else "0"]

		if self.dimlevel is None:
			# add on/off bit
			symstr.append("1" if self.on else "0")
		else:
			# add X symbol
			symstr.append("X")

		symstr.extend(format(self.channel - 1, "04b"))
		if self.dimlevel is not None:
			dim_steps = round(self.dimlevel * 15 / 100)
			symstr.extend(format(dim_steps, "04b"))

		timings: list[int] = []
		timings.extend(_symbols["sync"])
		for s in symstr:
			timings.extend(_symbols[s])
		timings.extend(_symbols["pause"])

		return timings
