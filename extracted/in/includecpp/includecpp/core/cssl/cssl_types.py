"""
CSSL Data Types - Advanced container types for CSSL

Types:
- datastruct<T>: Universal container (lazy declarator) - can hold any type
- shuffled<T>: Unorganized fast storage for multiple returns
- iterator<T>: Advanced iterator with programmable tasks
- combo<T>: Filter/search spaces for open parameter matching
- dataspace<T>: SQL/data storage container
- openquote<T>: SQL openquote container
"""

from typing import Any, Dict, List, Optional, Callable, Union, TypeVar, Generic
from dataclasses import dataclass, field
import copy
import threading
import queue as py_queue
from collections import deque


T = TypeVar('T')


class Bit:
    """CSSL Bit type - single binary value (0 or 1).

    Usage in CSSL:
        bit flag = 1;
        bit enabled = 0;

        if (flag == 1) { ... }
        flag = 0;  // Toggle
    """

    def __init__(self, value: int = 0):
        if value not in (0, 1):
            raise ValueError(f"Bit must be 0 or 1, got {value}")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, v: int):
        if v not in (0, 1):
            raise ValueError(f"Bit must be 0 or 1, got {v}")
        self._value = v

    def __bool__(self) -> bool:
        return self._value == 1

    def __int__(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        if isinstance(other, Bit):
            return self._value == other._value
        return self._value == other

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return str(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def toggle(self) -> 'Bit':
        """Toggle the bit value (0->1, 1->0)."""
        self._value = 1 if self._value == 0 else 0
        return self

    def switch(self) -> 'Bit':
        """Switch the bit value (0->1, 1->0). Alias for toggle()."""
        return self.toggle()

    def set(self, new: int = 1) -> 'Bit':
        """Set to value (default 1). If new is 0, clears the bit."""
        if new not in (0, 1):
            raise ValueError(f"Bit must be 0 or 1, got {new}")
        self._value = new
        return self

    def clear(self) -> 'Bit':
        """Clear to 0."""
        self._value = 0
        return self

    def assign(self, value: int) -> 'Bit':
        """Assign a new value (0 or 1). Alias for set()."""
        return self.set(value)

    def is_set(self) -> bool:
        """Check if bit is set (1)."""
        return self._value == 1

    def is_clear(self) -> bool:
        """Check if bit is clear (0)."""
        return self._value == 0

    def copy(self) -> 'Bit':
        """Create a copy of this bit."""
        return Bit(self._value)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def and_(self, other: 'Bit') -> 'Bit':
        """Logical AND with another bit."""
        other_val = other._value if isinstance(other, Bit) else int(other)
        return Bit(self._value & other_val)

    def or_(self, other: 'Bit') -> 'Bit':
        """Logical OR with another bit."""
        other_val = other._value if isinstance(other, Bit) else int(other)
        return Bit(self._value | other_val)

    def xor_(self, other: 'Bit') -> 'Bit':
        """Logical XOR with another bit."""
        other_val = other._value if isinstance(other, Bit) else int(other)
        return Bit(self._value ^ other_val)

    def not_(self) -> 'Bit':
        """Logical NOT (invert)."""
        return Bit(1 if self._value == 0 else 0)

    def nand_(self, other: 'Bit') -> 'Bit':
        """Logical NAND with another bit."""
        return self.and_(other).not_()

    def nor_(self, other: 'Bit') -> 'Bit':
        """Logical NOR with another bit."""
        return self.or_(other).not_()

    def xnor_(self, other: 'Bit') -> 'Bit':
        """Logical XNOR with another bit."""
        return self.xor_(other).not_()

    def implies(self, other: 'Bit') -> 'Bit':
        """Logical implication (A implies B = NOT A OR B)."""
        return self.not_().or_(other)

    def to_int(self) -> int:
        """Convert to integer."""
        return self._value

    def to_bool(self) -> bool:
        """Convert to boolean."""
        return self._value == 1

    def to_str(self) -> str:
        """Convert to string."""
        return str(self._value)

    def from_int(self, n: int) -> 'Bit':
        """Set from integer (0 or non-zero)."""
        self._value = 0 if n == 0 else 1
        return self

    def from_bool(self, b: bool) -> 'Bit':
        """Set from boolean."""
        self._value = 1 if b else 0
        return self

    def count(self) -> int:
        """Return count of set bits (0 or 1)."""
        return self._value

    def flip_if(self, condition: bool) -> 'Bit':
        """Flip the bit if condition is true."""
        if condition:
            self.toggle()
        return self

    def set_if(self, condition: bool) -> 'Bit':
        """Set to 1 if condition is true."""
        if condition:
            self._value = 1
        return self

    def clear_if(self, condition: bool) -> 'Bit':
        """Clear to 0 if condition is true."""
        if condition:
            self._value = 0
        return self

    def compare(self, other: 'Bit') -> int:
        """Compare with another bit. Returns -1, 0, or 1."""
        other_val = other._value if isinstance(other, Bit) else int(other)
        if self._value < other_val:
            return -1
        elif self._value > other_val:
            return 1
        return 0

    def equals(self, other: 'Bit') -> bool:
        """Check equality with another bit."""
        return self.__eq__(other)

    def hash(self) -> int:
        """Return hash value."""
        return hash(self._value)

    def serialize(self) -> str:
        """Serialize to string."""
        return str(self._value)

    def deserialize(self, data: str) -> 'Bit':
        """Deserialize from string."""
        self._value = int(data) if data in ('0', '1') else 0
        return self

    def pulse(self) -> 'Bit':
        """Pulse: set to 1 then back to 0, return self."""
        old = self._value
        self._value = 1
        # In real hardware this would have a delay
        self._value = old
        return self

    def latch(self, enable: bool = True) -> 'Bit':
        """Latch: if enable is true, keep current value."""
        # This is a placeholder for hardware-like behavior
        return self

    def rising_edge(self, previous: 'Bit') -> bool:
        """Detect rising edge (0->1 transition)."""
        prev_val = previous._value if isinstance(previous, Bit) else int(previous)
        return prev_val == 0 and self._value == 1

    def falling_edge(self, previous: 'Bit') -> bool:
        """Detect falling edge (1->0 transition)."""
        prev_val = previous._value if isinstance(previous, Bit) else int(previous)
        return prev_val == 1 and self._value == 0

    def swap(self, other: 'Bit') -> 'Bit':
        """Swap values with another bit."""
        self._value, other._value = other._value, self._value
        return self

    def get(self) -> int:
        """Get the bit value."""
        return self._value

    def info(self) -> dict:
        """Return info about the bit."""
        return {'value': self._value, 'is_set': self.is_set(), 'is_clear': self.is_clear()}


class Byte:
    """CSSL Byte type - 8-bit value with special notation.

    Supports special notation:
        byte b = 1^250;   // Binary 1 with weight 250 (value = 250)
        byte b = 0^102;   // Binary 0 with weight 102 (value = 102 as negative context)

    The notation `x^y` means:
        - x: base bit (0 or 1)
        - y: value/weight (0-255)

    When base is 1: value is stored directly (1^250 = 250)
    When base is 0: value is stored as complement (0^102 = -102 or 256-102)

    Usage in CSSL:
        byte high = 1^200;
        byte low = 0^50;

        if (high == low) { ... }
        printl(high.value());  // 200
        printl(low.raw());     // 50
    """

    def __init__(self, base: int = 0, weight: int = 0):
        if base not in (0, 1):
            raise ValueError(f"Byte base must be 0 or 1, got {base}")
        if not (0 <= weight <= 255):
            raise ValueError(f"Byte weight must be 0-255, got {weight}")
        self._base = base
        self._weight = weight

    @property
    def base(self) -> int:
        return self._base

    @property
    def weight(self) -> int:
        return self._weight

    def value(self) -> int:
        """Get the effective value based on base and weight."""
        if self._base == 1:
            return self._weight
        else:
            # 0^x represents complement or negative context
            return -self._weight if self._weight > 0 else 0

    def raw(self) -> int:
        """Get the raw weight value."""
        return self._weight

    def unsigned(self) -> int:
        """Get as unsigned byte (0-255)."""
        if self._base == 1:
            return self._weight
        else:
            return (256 - self._weight) % 256

    def __eq__(self, other) -> bool:
        if isinstance(other, Byte):
            return self._base == other._base and self._weight == other._weight
        if isinstance(other, int):
            return self.value() == other
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if isinstance(other, Byte):
            return self.value() < other.value()
        return self.value() < other

    def __le__(self, other) -> bool:
        if isinstance(other, Byte):
            return self.value() <= other.value()
        return self.value() <= other

    def __gt__(self, other) -> bool:
        if isinstance(other, Byte):
            return self.value() > other.value()
        return self.value() > other

    def __ge__(self, other) -> bool:
        if isinstance(other, Byte):
            return self.value() >= other.value()
        return self.value() >= other

    def __int__(self) -> int:
        return self.value()

    def __repr__(self) -> str:
        return f"Byte({self._base}^{self._weight})"

    def __str__(self) -> str:
        return f"{self._base}^{self._weight}"

    def __add__(self, other) -> 'Byte':
        if isinstance(other, Byte):
            result = (self.unsigned() + other.unsigned()) % 256
        else:
            result = (self.unsigned() + int(other)) % 256
        return Byte(1, result)

    def __sub__(self, other) -> 'Byte':
        if isinstance(other, Byte):
            result = (self.unsigned() - other.unsigned()) % 256
        else:
            result = (self.unsigned() - int(other)) % 256
        return Byte(1, result)

    def __and__(self, other) -> 'Byte':
        """Bitwise AND."""
        if isinstance(other, Byte):
            result = self.unsigned() & other.unsigned()
        else:
            result = self.unsigned() & int(other)
        return Byte(1, result)

    def __or__(self, other) -> 'Byte':
        """Bitwise OR."""
        if isinstance(other, Byte):
            result = self.unsigned() | other.unsigned()
        else:
            result = self.unsigned() | int(other)
        return Byte(1, result)

    def __xor__(self, other) -> 'Byte':
        """Bitwise XOR."""
        if isinstance(other, Byte):
            result = self.unsigned() ^ other.unsigned()
        else:
            result = self.unsigned() ^ int(other)
        return Byte(1, result)

    def __invert__(self) -> 'Byte':
        """Bitwise NOT (complement)."""
        return Byte(1, (~self.unsigned()) & 0xFF)

    def to_bits(self) -> List['Bit']:
        """Convert to list of 8 Bits (MSB first)."""
        val = self.unsigned()
        return [Bit((val >> (7 - i)) & 1) for i in range(8)]

    def reverse(self) -> 'Byte':
        """Reverse the bit order of the byte."""
        val = self.unsigned()
        reversed_val = 0
        for i in range(8):
            if val & (1 << i):
                reversed_val |= (1 << (7 - i))
        return Byte(1, reversed_val)

    def to_str(self) -> str:
        """Convert to binary string representation (8 bits)."""
        return format(self.unsigned(), '08b')

    def copy(self) -> 'Byte':
        """Create a copy of this byte."""
        return Byte(self._base, self._weight)

    def get(self, index: int) -> 'Bit':
        """Get bit at index (0 = LSB, 7 = MSB)."""
        if not (0 <= index <= 7):
            raise IndexError(f"Bit index must be 0-7, got {index}")
        return Bit((self.unsigned() >> index) & 1)

    def set_bit(self, index: int, value: int = 1) -> 'Byte':
        """Set bit at index to value (0 or 1). Internal method."""
        if not (0 <= index <= 7):
            raise IndexError(f"Bit index must be 0-7, got {index}")
        if value not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1, got {value}")
        current = self.unsigned()
        if value:
            current |= (1 << index)
        else:
            current &= ~(1 << index)
        self._base = 1
        self._weight = current
        return self

    def set(self, index: int, new: int) -> 'Byte':
        """Set bit at index to new value (0 or 1)."""
        return self.set_bit(index, new)

    def change(self, index: int, new: int) -> 'Byte':
        """Change bit at index to new value. Alias for set()."""
        return self.set_bit(index, new)

    def switch(self, index: int) -> 'Byte':
        """Toggle bit at index (0->1, 1->0)."""
        if not (0 <= index <= 7):
            raise IndexError(f"Bit index must be 0-7, got {index}")
        current_bit = (self.unsigned() >> index) & 1
        return self.set_bit(index, 1 - current_bit)

    def write(self, index: int, cnt: int) -> 'Byte':
        """Write value to bits starting at index for cnt bits.

        Args:
            index: Starting bit position (0 = LSB)
            cnt: Value to write (will be masked to fit)
        """
        if not (0 <= index <= 7):
            raise IndexError(f"Bit index must be 0-7, got {index}")
        # Calculate how many bits we can write
        max_bits = 8 - index
        mask = (1 << max_bits) - 1
        cnt = cnt & mask

        current = self.unsigned()
        # Clear the bits we're writing to
        clear_mask = ~(mask << index) & 0xFF
        current = current & clear_mask
        # Set the new bits
        current = current | (cnt << index)
        self._base = 1
        self._weight = current
        return self

    def info(self) -> dict:
        """Get detailed information about the byte."""
        return {
            'base': self._base,
            'weight': self._weight,
            'value': self.value(),
            'unsigned': self.unsigned(),
            'binary': self.to_str(),
            'hex': hex(self.unsigned()),
            'bits': [int(b) for b in self.to_bits()]
        }

    def len(self) -> int:
        """Return the number of bits (always 8)."""
        return 8

    def at(self, index: int) -> 'Bit':
        """Get bit at index (0 = LSB, 7 = MSB). Alias for get()."""
        return self.get(index)

    @classmethod
    def from_bits(cls, bits: List['Bit']) -> 'Byte':
        """Create Byte from 8 Bits (MSB first)."""
        if len(bits) != 8:
            raise ValueError("from_bits requires exactly 8 bits")
        val = sum(int(bits[i]) << (7 - i) for i in range(8))
        return cls(1, val)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def rotate_left(self, n: int = 1) -> 'Byte':
        """Rotate bits left by n positions. Modifies in place."""
        val = self.unsigned()
        n = n % 8
        self._weight = ((val << n) | (val >> (8 - n))) & 0xFF
        self._base = 1
        return self

    def rotate_right(self, n: int = 1) -> 'Byte':
        """Rotate bits right by n positions. Modifies in place."""
        val = self.unsigned()
        n = n % 8
        self._weight = ((val >> n) | (val << (8 - n))) & 0xFF
        self._base = 1
        return self

    def shift_left(self, n: int = 1) -> 'Byte':
        """Shift bits left by n positions (fill with 0). Modifies in place."""
        self._weight = (self.unsigned() << n) & 0xFF
        self._base = 1
        return self

    def shift_right(self, n: int = 1) -> 'Byte':
        """Shift bits right by n positions (fill with 0). Modifies in place."""
        self._weight = (self.unsigned() >> n) & 0xFF
        self._base = 1
        return self

    def popcount(self) -> int:
        """Count the number of set bits (1s)."""
        return bin(self.unsigned()).count('1')

    def leading_zeros(self) -> int:
        """Count leading zeros (from MSB)."""
        val = self.unsigned()
        if val == 0:
            return 8
        count = 0
        for i in range(7, -1, -1):
            if (val >> i) & 1:
                break
            count += 1
        return count

    def trailing_zeros(self) -> int:
        """Count trailing zeros (from LSB)."""
        val = self.unsigned()
        if val == 0:
            return 8
        count = 0
        for i in range(8):
            if (val >> i) & 1:
                break
            count += 1
        return count

    def parity(self) -> int:
        """Return parity (0 if even number of 1s, 1 if odd)."""
        return self.popcount() % 2

    def swap_nibbles(self) -> 'Byte':
        """Swap high and low nibbles (4 bits each). Modifies in place."""
        val = self.unsigned()
        self._weight = ((val & 0x0F) << 4) | ((val & 0xF0) >> 4)
        self._base = 1
        return self

    def mirror(self) -> 'Byte':
        """Mirror/reverse all bits. Modifies in place."""
        val = self.unsigned()
        result = 0
        for i in range(8):
            if (val >> i) & 1:
                result |= (1 << (7 - i))
        self._weight = result
        self._base = 1
        return self

    def from_hex(self, s: str) -> 'Byte':
        """Set Byte from hex string (e.g., 'FF', '0x3A'). Modifies in place."""
        val = int(s, 16) & 0xFF
        self._base = 1
        self._weight = val
        return self

    def to_hex(self) -> str:
        """Convert to hex string."""
        return f'{self.unsigned():02X}'

    def from_binary(self, s: str) -> 'Byte':
        """Set Byte from binary string (e.g., '10110101'). Modifies in place."""
        s = s.replace('0b', '').replace(' ', '')
        val = int(s, 2) & 0xFF
        self._base = 1
        self._weight = val
        return self

    def to_binary(self) -> str:
        """Convert to binary string (8 chars)."""
        return f'{self.unsigned():08b}'

    def from_decimal(self, n: int) -> 'Byte':
        """Set Byte from decimal integer. Modifies in place."""
        self._base = 1
        self._weight = n & 0xFF
        return self

    def clamp(self, min_val: int, max_val: int) -> 'Byte':
        """Clamp value to range [min_val, max_val]."""
        val = max(min_val, min(max_val, self.unsigned()))
        return Byte(1, val & 0xFF)

    def saturating_add(self, n: int) -> 'Byte':
        """Add with saturation (max 255)."""
        result = min(255, self.unsigned() + n)
        return Byte(1, result)

    def saturating_sub(self, n: int) -> 'Byte':
        """Subtract with saturation (min 0)."""
        result = max(0, self.unsigned() - n)
        return Byte(1, result)

    def wrapping_add(self, n: int) -> 'Byte':
        """Add with wrapping (overflow wraps around)."""
        result = (self.unsigned() + n) & 0xFF
        return Byte(1, result)

    def wrapping_sub(self, n: int) -> 'Byte':
        """Subtract with wrapping (underflow wraps around)."""
        result = (self.unsigned() - n) & 0xFF
        return Byte(1, result)

    def is_power_of_two(self) -> bool:
        """Check if value is a power of two."""
        val = self.unsigned()
        return val > 0 and (val & (val - 1)) == 0

    def next_power_of_two(self) -> 'Byte':
        """Get next power of two >= current value."""
        val = self.unsigned()
        if val == 0:
            return Byte(1, 1)
        val -= 1
        val |= val >> 1
        val |= val >> 2
        val |= val >> 4
        val += 1
        return Byte(1, min(val, 255))

    def log2(self) -> int:
        """Get floor(log2) of value. Returns -1 for 0."""
        val = self.unsigned()
        if val == 0:
            return -1
        result = 0
        while val > 1:
            val >>= 1
            result += 1
        return result

    def msb(self) -> int:
        """Get most significant bit position (0-7) or -1 if 0."""
        val = self.unsigned()
        if val == 0:
            return -1
        pos = 0
        while val > 1:
            val >>= 1
            pos += 1
        return pos

    def lsb(self) -> int:
        """Get least significant bit position (0-7) or -1 if 0."""
        val = self.unsigned()
        if val == 0:
            return -1
        pos = 0
        while (val & 1) == 0:
            val >>= 1
            pos += 1
        return pos

    def slice_bits(self, start: int, end: int) -> 'Byte':
        """Extract bits from start to end (inclusive)."""
        if start > end:
            start, end = end, start
        mask = ((1 << (end - start + 1)) - 1) << start
        val = (self.unsigned() & mask) >> start
        return Byte(1, val)

    def pack(self, *bytes_list) -> list:
        """Pack this byte with others into a list."""
        return [self] + list(bytes_list)

    def interleave(self, other: 'Byte') -> int:
        """Interleave bits with another byte (returns 16-bit int)."""
        a = self.unsigned()
        b = other.unsigned() if isinstance(other, Byte) else int(other)
        result = 0
        for i in range(8):
            result |= ((a >> i) & 1) << (2 * i)
            result |= ((b >> i) & 1) << (2 * i + 1)
        return result

    def extract_nibble(self, high: bool = False) -> 'Byte':
        """Extract high or low nibble (4 bits) as a new Byte."""
        val = self.unsigned()
        if high:
            return Byte(1, (val >> 4) & 0x0F)
        return Byte(1, val & 0x0F)

    def set_nibble(self, value: int, high: bool = False) -> 'Byte':
        """Set high or low nibble."""
        current = self.unsigned()
        value = value & 0x0F
        if high:
            new_val = (current & 0x0F) | (value << 4)
        else:
            new_val = (current & 0xF0) | value
        return Byte(1, new_val)


class Address:
    """CSSL Address type - Memory reference (pointer-like).

    Stores a memory address and can reflect back to get the original object.
    Works like a pointer but with Python's reference semantics.

    Usage in CSSL:
        string text = "Hello";
        address addr = memory(text).get("address");

        // Reflect to get object
        obj = addr.reflect();
        printl(obj);  // "Hello"

        // Or use builtin
        obj = reflect(addr);
    """

    # Class-level registry to map addresses to objects
    _registry: dict = {}
    _next_id: int = 0

    def __init__(self, address_str: str = None, obj: any = None):
        """Create an Address from an address string or object.

        Args:
            address_str: Memory address string (e.g., "0x7fff3adb4ed8")
            obj: Object to store (auto-generates address if provided)
        """
        if obj is not None:
            # Store object and generate address
            self._address = hex(id(obj))
            Address._registry[self._address] = obj
        elif address_str is not None:
            self._address = address_str
        else:
            self._address = "0x0"  # Null address

    @property
    def value(self) -> str:
        """Get the address value as string."""
        return self._address

    def __str__(self) -> str:
        return self._address

    def __repr__(self) -> str:
        return self._address

    def __eq__(self, other) -> bool:
        if isinstance(other, Address):
            return self._address == other._address
        if isinstance(other, str):
            return self._address == other
        return False

    def __hash__(self) -> int:
        return hash(self._address)

    def reflect(self) -> any:
        """Reflect the address to get the original object.

        Returns:
            The object at this address, or None if not found

        Example:
            string text = "Hello";
            address addr = memory(text).get("address");
            obj = addr.reflect();
            printl(obj);  // "Hello"
        """
        return Address._registry.get(self._address)

    def get_address(self) -> str:
        """Get the address string (hex memory address).

        Returns:
            The address as a hex string (e.g., "0x7f8b2c001a00")

        Example:
            pointer p;
            p.from_object(myObj);
            printl(p.get_address());  // "0x7f8b2c001a00"
        """
        return self._address

    def hex(self) -> str:
        """Get the address as hex string (alias for get_address)."""
        return self._address

    def is_null(self) -> bool:
        """Check if this is a null address."""
        return self._address == "0x0" or self._address is None

    def is_address(self) -> bool:
        """Check if this pointer holds a valid address (not null).

        Returns:
            True if the address is valid (not null), False otherwise.

        Example:
            pointer p = myObj;
            if (p.is_address()) {
                printl("Pointer has valid address: " + p.get_address());
            }
        """
        return not self.is_null()

    def is_valid(self) -> bool:
        """Check if this address points to a valid, accessible object.

        Returns:
            True if the address is not null AND the object exists in registry.

        Example:
            pointer p = myObj;
            if (p.is_valid()) {
                printl("Object still exists");
            }
        """
        if self.is_null():
            return False
        return self._address in Address._registry

    def set(self, value: any) -> 'Address':
        """Set the value at this address.

        Replaces the object stored at this address in the registry.

        Returns:
            This Address (for chaining).

        Example:
            int x = 5;
            address addr = address(x);
            addr.set(10);
            printl(addr.reflect());  // 10
        """
        Address._registry[self._address] = value
        return self

    def copy(self) -> 'Address':
        """Create a copy of this address."""
        addr = Address(self._address)
        return addr

    def from_object(self, obj: any) -> 'Address':
        """Point this Address to an object.

        Args:
            obj: Object to get address of

        Returns:
            self (for chaining)
        """
        self._address = hex(id(obj))
        self._obj_ref = obj
        Address._registry[self._address] = obj
        return self

    @classmethod
    def register(cls, address_str: str, obj: any) -> None:
        """Register an object at a specific address.

        Args:
            address_str: Address string
            obj: Object to store
        """
        cls._registry[address_str] = obj

    def destroy(self) -> bool:
        """Destroy the object at this address and free memory.

        Removes the object from the registry and sets this pointer to null.

        Returns:
            True if successfully destroyed, False if already null or not found.

        Example:
            pointer p;
            p.from_object(myObj);
            p.destroy();  // Object freed, p is now null
            printl(p.is_null());  // true
        """
        if self.is_null():
            return False

        # Remove from registry
        if self._address in Address._registry:
            obj = Address._registry.pop(self._address)
            # Call destructor if object has one
            if hasattr(obj, '__del__'):
                try:
                    obj.__del__()
                except:
                    pass
            elif hasattr(obj, 'destroy'):
                try:
                    obj.destroy()
                except:
                    pass

        # Clear this pointer
        self._address = "0x0"
        self._obj_ref = None
        return True

    def reset(self) -> 'Address':
        """Reset pointer to null without destroying the object.

        Returns:
            self (for chaining)
        """
        self._address = "0x0"
        self._obj_ref = None
        return self

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds


class CSSLNamespace:
    """CSSL Namespace - groups functions, classes, structs, enums, and nested namespaces.

    Provides C++-style namespace organization accessible via the :: operator.

    Usage in CSSL:
        namespace mylib {
            void greet() { printl("Hello!"); }
            class MyClass { ... }
            namespace nested { ... }
        }

        mylib::greet();
        new mylib::MyClass();
        mylib::nested::innerFunc();
    """

    def __init__(self, name: str):
        self.name = name
        self.functions: Dict[str, Any] = {}  # Function AST nodes
        self.classes: Dict[str, Any] = {}    # CSSLClass instances
        self.structs: Dict[str, Any] = {}    # Struct AST nodes
        self.enums: Dict[str, Any] = {}      # Enum dicts
        self.namespaces: Dict[str, 'CSSLNamespace'] = {}  # Nested namespaces
        self.variables: Dict[str, Any] = {}  # Namespace-level variables

    def get(self, member_name: str) -> Any:
        """Get a member by name - searches functions, classes, enums, structs, nested namespaces."""
        # Check nested namespaces first (for chained :: access)
        if member_name in self.namespaces:
            return self.namespaces[member_name]
        # Check classes
        if member_name in self.classes:
            return self.classes[member_name]
        # Check functions
        if member_name in self.functions:
            return self.functions[member_name]
        # Check enums
        if member_name in self.enums:
            return self.enums[member_name]
        # Check structs
        if member_name in self.structs:
            return self.structs[member_name]
        # Check variables
        if member_name in self.variables:
            return self.variables[member_name]
        return None

    def __contains__(self, name: str) -> bool:
        """Check if namespace contains a member."""
        return (name in self.namespaces or
                name in self.classes or
                name in self.functions or
                name in self.enums or
                name in self.structs or
                name in self.variables)

    def __getitem__(self, name: str) -> Any:
        """Dict-like access for compatibility."""
        return self.get(name)

    def __repr__(self) -> str:
        members = []
        if self.functions:
            members.append(f"{len(self.functions)} functions")
        if self.classes:
            members.append(f"{len(self.classes)} classes")
        if self.enums:
            members.append(f"{len(self.enums)} enums")
        if self.structs:
            members.append(f"{len(self.structs)} structs")
        if self.namespaces:
            members.append(f"{len(self.namespaces)} namespaces")
        content = ", ".join(members) if members else "empty"
        return f"<namespace {self.name}: {content}>"


class DataStruct(list):
    """Universal container - lazy declarator that can hold any type.

    Like a vector but more flexible. Can hold strings, ints, floats,
    objects, etc. at the cost of performance. v4.7.1: Thread-safe.

    Usage:
        datastruct<dynamic> myData;
        myData +<== someValue;
        myData.content()  # Returns all elements
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type
        self._metadata: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def content(self) -> list:
        """Return all elements as a list"""
        with self._lock:
            return list(self)

    def add(self, item: Any) -> 'DataStruct':
        """Add an item to the datastruct"""
        with self._lock:
            self.append(item)
        return self

    def remove_where(self, predicate: Callable[[Any], bool]) -> 'DataStruct':
        """Remove items matching predicate"""
        with self._lock:
            to_remove = [item for item in self if predicate(item)]
            for item in to_remove:
                self.remove(item)
        return self

    def find_where(self, predicate: Callable[[Any], bool]) -> Optional[Any]:
        """Find first item matching predicate"""
        with self._lock:
            for item in self:
                if predicate(item):
                    return item
            return None

    def convert(self, target_type: type) -> Any:
        """Convert first element to target type"""
        with self._lock:
            if len(self) > 0:
                return target_type(self[0])
            return None

    def length(self) -> int:
        """Return datastruct length"""
        with self._lock:
            return len(self)

    def size(self) -> int:
        """Return datastruct size (alias for length)"""
        with self._lock:
            return len(self)

    def push(self, item: Any) -> 'DataStruct':
        """Push item to datastruct (alias for add)"""
        with self._lock:
            self.append(item)
        return self

    def isEmpty(self) -> bool:
        """Check if datastruct is empty"""
        with self._lock:
            return len(self) == 0

    def contains(self, item: Any) -> bool:
        """Check if datastruct contains item"""
        with self._lock:
            return item in self

    def at(self, index: int) -> Any:
        """Get item at index with bounds checking (C++ style).

        v4.7.1: Now raises IndexError instead of returning None.
        """
        with self._lock:
            if index < 0 or index >= len(self):
                raise IndexError(f"DataStruct index {index} out of range [0, {len(self)})")
            return self[index]

    # === C++ STL Additional Methods (v4.7.1) ===

    def clear(self) -> 'DataStruct':
        """Clear all elements."""
        with self._lock:
            super().clear()
        return self

    def pop_back(self) -> Any:
        """Remove and return last element."""
        with self._lock:
            if self:
                return self.pop()
            raise IndexError("pop from empty DataStruct")

    def peek(self) -> Any:
        """View last element without removing."""
        with self._lock:
            return self[-1] if self else None

    def first(self) -> Any:
        """Get first element."""
        with self._lock:
            return self[0] if self else None

    def last(self) -> Any:
        """Get last element."""
        with self._lock:
            return self[-1] if self else None

    def slice(self, start: int, end: int = None) -> 'DataStruct':
        """Return slice."""
        with self._lock:
            result = DataStruct(self._element_type)
            if end is None:
                result.extend(self[start:])
            else:
                result.extend(self[start:end])
            return result

    def map(self, func: Callable[[Any], Any]) -> 'DataStruct':
        """Apply function to all elements."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(func(item) for item in self)
            return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'DataStruct':
        """Filter elements by predicate."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(item for item in self if predicate(item))
            return result

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Reduce to single value."""
        with self._lock:
            from functools import reduce as py_reduce
            if initial is None:
                return py_reduce(func, self)
            return py_reduce(func, self, initial)

    def forEach(self, func: Callable[[Any], None]) -> 'DataStruct':
        """Execute function for each element."""
        with self._lock:
            for item in self:
                func(item)
        return self

    def every(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if all elements match predicate."""
        with self._lock:
            return all(predicate(item) for item in self)

    def some(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if any element matches predicate."""
        with self._lock:
            return any(predicate(item) for item in self)

    def reverse_inplace(self) -> 'DataStruct':
        """Reverse in place."""
        with self._lock:
            super().reverse()
        return self

    def sort_inplace(self, key=None, reverse=False) -> 'DataStruct':
        """Sort in place."""
        with self._lock:
            super().sort(key=key, reverse=reverse)
        return self

    def unique(self) -> 'DataStruct':
        """Return with unique elements."""
        with self._lock:
            result = DataStruct(self._element_type)
            seen = set()
            for item in self:
                key = item if isinstance(item, (int, str, float, bool)) else id(item)
                if key not in seen:
                    seen.add(key)
                    result.append(item)
            return result

    def flatten(self, depth: int = 1) -> 'DataStruct':
        """Flatten nested structures."""
        with self._lock:
            result = DataStruct(self._element_type)
            for item in self:
                if isinstance(item, (list, DataStruct)) and depth > 0:
                    nested = DataStruct(self._element_type)
                    nested.extend(item)
                    result.extend(nested.flatten(depth - 1))
                else:
                    result.append(item)
            return result

    def join(self, separator: str = ',') -> str:
        """Join elements into string."""
        with self._lock:
            return separator.join(str(item) for item in self)

    def indexOf(self, item: Any) -> int:
        """Find index of item (-1 if not found)."""
        with self._lock:
            try:
                return list.index(self, item)
            except ValueError:
                return -1

    def count_value(self, item: Any) -> int:
        """Count occurrences of item."""
        with self._lock:
            return list.count(self, item)

    def swap(self, other: 'DataStruct') -> 'DataStruct':
        """Swap contents."""
        with self._lock:
            temp = list(self)
            self[:] = list(other)
            other[:] = temp
        return self

    def copy(self) -> 'DataStruct':
        """Return shallow copy."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(self)
            return result

    def begin(self) -> int:
        """Return iterator to beginning (C++ style)"""
        return 0

    def end(self) -> int:
        """Return iterator to end (C++ style)"""
        return len(self)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def chunk(self, size: int) -> list:
        """Split into chunks of given size."""
        with self._lock:
            return [list(self[i:i+size]) for i in range(0, len(self), size)]

    def partition(self, predicate: Callable) -> tuple:
        """Split into (matching, non-matching)."""
        with self._lock:
            matching = [x for x in self if predicate(x)]
            non_matching = [x for x in self if not predicate(x)]
            return (matching, non_matching)

    def groupBy(self, key_func: Callable) -> dict:
        """Group elements by key function."""
        with self._lock:
            groups = {}
            for x in self:
                k = key_func(x)
                if k not in groups:
                    groups[k] = []
                groups[k].append(x)
            return groups

    def zip_with(self, *others) -> list:
        """Zip with other iterables."""
        with self._lock:
            return list(zip(self, *others))

    def unzip(self) -> tuple:
        """Unzip list of pairs into tuple of lists."""
        with self._lock:
            if not self:
                return ([], [])
            return tuple(list(x) for x in zip(*self))

    def rotate(self, n: int = 1) -> 'DataStruct':
        """Rotate elements by n positions (positive=right)."""
        with self._lock:
            if not self:
                return self
            n = n % len(self)
            self[:] = list(self[-n:]) + list(self[:-n])
            return self

    def interleave(self, other) -> 'DataStruct':
        """Interleave with another sequence."""
        with self._lock:
            result = DataStruct(self._element_type)
            other_list = list(other)
            for i in range(max(len(self), len(other_list))):
                if i < len(self):
                    result.append(self[i])
                if i < len(other_list):
                    result.append(other_list[i])
            return result

    def compact(self) -> 'DataStruct':
        """Remove None values."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend([x for x in self if x is not None])
            return result

    def frequencies(self) -> dict:
        """Count occurrences of each value."""
        with self._lock:
            freq = {}
            for x in self:
                key = x if isinstance(x, (int, str, float, bool)) else str(x)
                freq[key] = freq.get(key, 0) + 1
            return freq

    def sample(self, n: int = 1) -> list:
        """Random sample of n elements."""
        import random
        with self._lock:
            return random.sample(list(self), min(n, len(self)))

    def takeWhile(self, predicate: Callable) -> 'DataStruct':
        """Take elements while predicate is true."""
        with self._lock:
            result = DataStruct(self._element_type)
            for x in self:
                if not predicate(x):
                    break
                result.append(x)
            return result

    def dropWhile(self, predicate: Callable) -> 'DataStruct':
        """Drop elements while predicate is true."""
        with self._lock:
            result = DataStruct(self._element_type)
            dropping = True
            for x in self:
                if dropping and predicate(x):
                    continue
                dropping = False
                result.append(x)
            return result

    def take(self, n: int) -> 'DataStruct':
        """Take first n elements."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(self[:n])
            return result

    def drop(self, n: int) -> 'DataStruct':
        """Drop first n elements."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(self[n:])
            return result

    def head(self, n: int = 1) -> 'DataStruct':
        """Get first n elements."""
        return self.take(n)

    def tail(self, n: int = 1) -> 'DataStruct':
        """Get last n elements."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(self[-n:] if n > 0 else [])
            return result

    def splitAt(self, index: int) -> tuple:
        """Split at index into two DataStructs."""
        with self._lock:
            left = DataStruct(self._element_type)
            right = DataStruct(self._element_type)
            left.extend(self[:index])
            right.extend(self[index:])
            return (left, right)

    def span(self, predicate: Callable) -> tuple:
        """Split where predicate becomes false."""
        with self._lock:
            for i, x in enumerate(self):
                if not predicate(x):
                    left = DataStruct(self._element_type)
                    right = DataStruct(self._element_type)
                    left.extend(self[:i])
                    right.extend(self[i:])
                    return (left, right)
            left = DataStruct(self._element_type)
            left.extend(self)
            return (left, DataStruct(self._element_type))

    def distinct(self) -> 'DataStruct':
        """Remove duplicates (preserving order)."""
        return self.unique()

    def dedupe(self) -> 'DataStruct':
        """Remove consecutive duplicates."""
        with self._lock:
            result = DataStruct(self._element_type)
            prev = None
            for x in self:
                if x != prev:
                    result.append(x)
                    prev = x
            return result

    def min_val(self):
        """Get minimum value."""
        with self._lock:
            return min(self) if self else None

    def max_val(self):
        """Get maximum value."""
        with self._lock:
            return max(self) if self else None

    def sum_val(self):
        """Get sum of values."""
        with self._lock:
            return sum(self) if self else 0

    def avg(self):
        """Get average of values."""
        with self._lock:
            return sum(self) / len(self) if self else 0

    def product(self):
        """Get product of values."""
        with self._lock:
            result = 1
            for x in self:
                result *= x
            return result

    def sortBy(self, key_func: Callable) -> 'DataStruct':
        """Sort by key function."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(sorted(self, key=key_func))
            return result

    def sortDesc(self) -> 'DataStruct':
        """Sort descending."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend(sorted(self, reverse=True))
            return result

    def shuffle_elements(self) -> 'DataStruct':
        """Shuffle elements randomly."""
        import random
        with self._lock:
            items = list(self)
            random.shuffle(items)
            self[:] = items
            return self

    def randomElement(self):
        """Get a random element."""
        import random
        with self._lock:
            return random.choice(list(self)) if self else None

    def findLast(self, predicate: Callable):
        """Find last element matching predicate."""
        with self._lock:
            for x in reversed(self):
                if predicate(x):
                    return x
            return None

    def findLastIndex(self, predicate: Callable) -> int:
        """Find index of last element matching predicate."""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if predicate(self[i]):
                    return i
            return -1

    def countWhere(self, predicate: Callable) -> int:
        """Count elements matching predicate."""
        with self._lock:
            return sum(1 for x in self if predicate(x))

    def none(self, predicate: Callable) -> bool:
        """Check if no elements match predicate."""
        with self._lock:
            return not any(predicate(x) for x in self)

    def insertAt(self, index: int, value) -> 'DataStruct':
        """Insert value at index."""
        with self._lock:
            self.insert(index, value)
            return self

    def removeRange(self, start: int, end: int) -> 'DataStruct':
        """Remove elements in range [start, end)."""
        with self._lock:
            del self[start:end]
            return self

    def replaceAll(self, old_val, new_val) -> 'DataStruct':
        """Replace all occurrences of old_val with new_val."""
        with self._lock:
            for i in range(len(self)):
                if self[i] == old_val:
                    self[i] = new_val
            return self

    def flatMap(self, func: Callable) -> 'DataStruct':
        """Map then flatten."""
        with self._lock:
            result = DataStruct(self._element_type)
            for x in self:
                mapped = func(x)
                if isinstance(mapped, (list, tuple)):
                    result.extend(mapped)
                else:
                    result.append(mapped)
            return result

    def mapIndexed(self, func: Callable) -> 'DataStruct':
        """Map with index: func(index, element)."""
        with self._lock:
            result = DataStruct(self._element_type)
            result.extend([func(i, x) for i, x in enumerate(self)])
            return result

    def forEachIndexed(self, func: Callable) -> None:
        """ForEach with index: func(index, element)."""
        with self._lock:
            for i, x in enumerate(self):
                func(i, x)


class Stack(list):
    """Stack data structure (LIFO). v4.7.1: Thread-safe.

    Standard stack with push/pop operations.

    Usage:
        stack<string> myStack;
        myStack.push("Item1");
        myStack.push("Item2");
        item = myStack.pop();  # Returns "Item2"
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type
        self._lock = threading.RLock()

    def push(self, item: Any) -> 'Stack':
        """Push item onto stack"""
        with self._lock:
            self.append(item)
        return self

    def push_back(self, item: Any) -> 'Stack':
        """Push item onto stack (alias for push)"""
        with self._lock:
            self.append(item)
        return self

    def pop(self) -> Any:
        """Pop and return top element from stack.
        v4.7.1: Now raises IndexError instead of returning None when empty.
        """
        with self._lock:
            if len(self) == 0:
                raise IndexError("pop from empty stack")
            return super().pop()

    def pop_back(self) -> Any:
        """Pop and return top element (alias for pop)"""
        return self.pop()

    def peek(self) -> Any:
        """View top item without removing"""
        with self._lock:
            return self[-1] if self else None

    def is_empty(self) -> bool:
        """Check if stack is empty"""
        with self._lock:
            return len(self) == 0

    def isEmpty(self) -> bool:
        """Check if stack is empty (camelCase alias)"""
        with self._lock:
            return len(self) == 0

    def size(self) -> int:
        """Return stack size"""
        with self._lock:
            return len(self)

    def length(self) -> int:
        """Return stack length (alias for size)"""
        with self._lock:
            return len(self)

    def contains(self, item: Any) -> bool:
        """Check if stack contains item"""
        with self._lock:
            return item in self

    def indexOf(self, item: Any) -> int:
        """Find index of item (-1 if not found)"""
        with self._lock:
            try:
                return self.index(item)
            except ValueError:
                return -1

    def toArray(self) -> list:
        """Convert stack to array"""
        with self._lock:
            return list(self)

    def swap(self) -> 'Stack':
        """Swap top two elements"""
        with self._lock:
            if len(self) >= 2:
                self[-1], self[-2] = self[-2], self[-1]
        return self

    def dup(self) -> 'Stack':
        """Duplicate top element"""
        with self._lock:
            if self:
                self.append(self[-1])
        return self

    # === C++ STL Additional Methods (v4.7.1) ===

    def emplace(self, *args) -> 'Stack':
        """In-place construction at top."""
        with self._lock:
            self.append(args[0] if args else None)
        return self

    def clear(self) -> 'Stack':
        """Clear all elements."""
        with self._lock:
            super().clear()
        return self

    def reverse_stack(self) -> 'Stack':
        """Reverse stack order."""
        with self._lock:
            super().reverse()
        return self

    def copy(self) -> 'Stack':
        """Return shallow copy."""
        with self._lock:
            new_stack = Stack(self._element_type)
            new_stack.extend(self)
            return new_stack

    def peekAt(self, depth: int) -> Any:
        """Peek at specific depth (0 = top)."""
        with self._lock:
            if depth < 0 or depth >= len(self):
                raise IndexError(f"Stack depth {depth} out of range")
            return self[-(depth + 1)]

    def rotate(self, n: int = 1) -> 'Stack':
        """Rotate top n elements."""
        with self._lock:
            if n > len(self):
                n = len(self)
            if n > 0:
                top_n = self[-n:]
                del self[-n:]
                self[:0] = top_n
        return self

    def depth(self) -> int:
        """Alias for size()."""
        with self._lock:
            return len(self)

    def drop(self, n: int = 1) -> 'Stack':
        """Drop top n elements."""
        with self._lock:
            for _ in range(min(n, len(self))):
                super().pop()
        return self

    def nip(self) -> Any:
        """Remove second element (under top)."""
        with self._lock:
            if len(self) < 2:
                raise IndexError("nip requires at least 2 elements")
            return self.pop(-2)

    def tuck(self) -> 'Stack':
        """Copy top under second element."""
        with self._lock:
            if len(self) < 2:
                raise IndexError("tuck requires at least 2 elements")
            self.insert(-1, self[-1])
        return self

    def over(self) -> 'Stack':
        """Copy second element to top."""
        with self._lock:
            if len(self) < 2:
                raise IndexError("over requires at least 2 elements")
            self.append(self[-2])
        return self

    def pick(self, n: int) -> 'Stack':
        """Copy nth element (0-indexed from top) to top."""
        with self._lock:
            self.append(self[-(n + 1)])
        return self

    def begin(self) -> int:
        """Return iterator to beginning (C++ style)"""
        return 0

    def end(self) -> int:
        """Return iterator to end (C++ style)"""
        return len(self)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds


class Vector(list):
    """Dynamic array (vector) data structure. v4.7.1: Thread-safe.

    Resizable array with efficient random access.

    Usage:
        vector<int> myVector;
        myVector.push(1);
        myVector.push(2);
        myVector.at(0);  # Returns 1
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type
        self._lock = threading.RLock()

    def push(self, item: Any) -> 'Vector':
        """Add item to end"""
        with self._lock:
            self.append(item)
        return self

    def push_back(self, item: Any) -> 'Vector':
        """Add item to end (alias for push)"""
        with self._lock:
            self.append(item)
        return self

    def push_front(self, item: Any) -> 'Vector':
        """Add item to front"""
        with self._lock:
            self.insert(0, item)
        return self

    def pop_back(self) -> Any:
        """Remove and return last element"""
        with self._lock:
            return self.pop() if self else None

    def pop_front(self) -> Any:
        """Remove and return first element"""
        with self._lock:
            return self.pop(0) if self else None

    def at(self, index: int) -> Any:
        """Get item at index with bounds checking (C++ style).

        v4.7.1: Now raises IndexError instead of returning None.
        """
        with self._lock:
            if index < 0 or index >= len(self):
                raise IndexError(f"Vector index {index} out of range [0, {len(self)})")
            return self[index]

    def set(self, index: int, value: Any) -> 'Vector':
        """Set item at index"""
        with self._lock:
            if 0 <= index < len(self):
                self[index] = value
        return self

    def size(self) -> int:
        """Return vector size"""
        with self._lock:
            return len(self)

    def length(self) -> int:
        """Return vector length (alias for size)"""
        with self._lock:
            return len(self)

    def empty(self) -> bool:
        """Check if vector is empty"""
        with self._lock:
            return len(self) == 0

    def isEmpty(self) -> bool:
        """Check if vector is empty (camelCase alias)"""
        with self._lock:
            return len(self) == 0

    def front(self) -> Any:
        """Get first element"""
        with self._lock:
            return self[0] if self else None

    def back(self) -> Any:
        """Get last element"""
        with self._lock:
            return self[-1] if self else None

    def contains(self, item: Any) -> bool:
        """Check if vector contains item"""
        with self._lock:
            return item in self

    def indexOf(self, item: Any) -> int:
        """Find index of item (-1 if not found)"""
        with self._lock:
            try:
                return self.index(item)
            except ValueError:
                return -1

    def lastIndexOf(self, item: Any) -> int:
        """Find last index of item (-1 if not found)"""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if self[i] == item:
                    return i
            return -1

    def find(self, predicate: Callable[[Any], bool]) -> Any:
        """Find first item matching predicate"""
        with self._lock:
            for item in self:
                if callable(predicate) and predicate(item):
                    return item
                elif item == predicate:
                    return item
            return None

    def findIndex(self, predicate: Callable[[Any], bool]) -> int:
        """Find index of first item matching predicate"""
        with self._lock:
            for i, item in enumerate(self):
                if callable(predicate) and predicate(item):
                    return i
                elif item == predicate:
                    return i
            return -1

    def slice(self, start: int, end: int = None) -> 'Vector':
        """Return slice of vector"""
        with self._lock:
            result = Vector(self._element_type)
            if end is None:
                result.extend(self[start:])
            else:
                result.extend(self[start:end])
            return result

    def join(self, separator: str = ',') -> str:
        """Join elements into string"""
        with self._lock:
            return separator.join(str(item) for item in self)

    def map(self, func: Callable[[Any], Any]) -> 'Vector':
        """Apply function to all elements"""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(func(item) for item in self)
            return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'Vector':
        """Filter elements by predicate"""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(item for item in self if predicate(item))
            return result

    def forEach(self, func: Callable[[Any], None]) -> 'Vector':
        """Execute function for each element"""
        with self._lock:
            for item in self:
                func(item)
        return self

    def toArray(self) -> list:
        """Convert to plain list"""
        with self._lock:
            return list(self)

    def fill(self, value: Any, start: int = 0, end: int = None) -> 'Vector':
        """Fill range with value"""
        with self._lock:
            if end is None:
                end = len(self)
            for i in range(start, min(end, len(self))):
                self[i] = value
        return self

    def every(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if all elements match predicate"""
        with self._lock:
            return all(predicate(item) for item in self)

    def some(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if any element matches predicate"""
        with self._lock:
            return any(predicate(item) for item in self)

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Reduce vector to single value"""
        with self._lock:
            from functools import reduce as py_reduce
            if initial is None:
                return py_reduce(func, self)
            return py_reduce(func, self, initial)

    # === C++ STL Additional Methods (v4.7.1) ===

    def data(self) -> list:
        """Direct access to underlying list (C++ data())."""
        with self._lock:
            return list(self)

    def max_size(self) -> int:
        """Maximum theoretical size (C++ max_size())."""
        import sys
        return sys.maxsize

    def reserve(self, n: int) -> None:
        """Reserve capacity hint (Python lists auto-resize)."""
        pass  # No-op for Python lists

    def capacity(self) -> int:
        """Current capacity (C++ capacity())."""
        with self._lock:
            return len(self)

    def shrink_to_fit(self) -> None:
        """Release unused memory."""
        with self._lock:
            self[:] = list(self)

    def clear(self) -> 'Vector':
        """Clear all elements."""
        with self._lock:
            super().clear()
        return self

    def insert_at(self, pos: int, value: Any) -> 'Vector':
        """Insert at position (C++ insert())."""
        with self._lock:
            self.insert(pos, value)
        return self

    def insert_range(self, pos: int, values: list) -> 'Vector':
        """Insert multiple values at position."""
        with self._lock:
            for i, v in enumerate(values):
                self.insert(pos + i, v)
        return self

    def erase(self, pos: int) -> Any:
        """Erase at position, return removed element."""
        with self._lock:
            if 0 <= pos < len(self):
                return self.pop(pos)
            raise IndexError(f"Erase position {pos} out of range")

    def erase_range(self, start: int, end: int) -> list:
        """Erase range [start, end), return removed elements."""
        with self._lock:
            removed = list(self[start:end])
            del self[start:end]
            return removed

    def resize(self, count: int, value: Any = None) -> 'Vector':
        """Resize to count elements."""
        with self._lock:
            if count < len(self):
                del self[count:]
            else:
                self.extend([value] * (count - len(self)))
        return self

    def swap(self, other: 'Vector') -> 'Vector':
        """Swap contents with another vector."""
        with self._lock:
            temp = list(self)
            self[:] = list(other)
            other[:] = temp
        return self

    def rbegin(self) -> int:
        """Reverse begin (last valid index)."""
        with self._lock:
            return len(self) - 1 if self else -1

    def rend(self) -> int:
        """Reverse end (-1)."""
        return -1

    def assign(self, values: list) -> 'Vector':
        """Assign new values, replacing all."""
        with self._lock:
            self[:] = list(values)
        return self

    def emplace_back(self, *args, **kwargs) -> 'Vector':
        """Construct in-place at end."""
        with self._lock:
            self.append(args[0] if args else kwargs.get('value'))
        return self

    def reverse_inplace(self) -> 'Vector':
        """Reverse vector in place."""
        with self._lock:
            super().reverse()
        return self

    def sort_inplace(self, key=None, reverse=False) -> 'Vector':
        """Sort vector in place."""
        with self._lock:
            super().sort(key=key, reverse=reverse)
        return self

    def copy(self) -> 'Vector':
        """Return shallow copy."""
        with self._lock:
            new_vec = Vector(self._element_type)
            new_vec.extend(self)
            return new_vec

    def count_value(self, value: Any) -> int:
        """Count occurrences of value."""
        with self._lock:
            return super().count(value)

    def begin(self) -> int:
        """Return iterator to beginning (C++ style)"""
        return 0

    def end(self) -> int:
        """Return iterator to end (C++ style)"""
        return len(self)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def chunk(self, size: int) -> list:
        """Split into chunks of given size."""
        with self._lock:
            return [list(self[i:i+size]) for i in range(0, len(self), size)]

    def partition(self, predicate: Callable) -> tuple:
        """Split into (matching, non-matching)."""
        with self._lock:
            matching = [x for x in self if predicate(x)]
            non_matching = [x for x in self if not predicate(x)]
            return (matching, non_matching)

    def groupBy(self, key_func: Callable) -> dict:
        """Group elements by key function."""
        with self._lock:
            groups = {}
            for x in self:
                k = key_func(x)
                if k not in groups:
                    groups[k] = []
                groups[k].append(x)
            return groups

    def zip_with(self, *others) -> list:
        """Zip with other iterables."""
        with self._lock:
            return list(zip(self, *others))

    def unzip(self) -> tuple:
        """Unzip list of pairs."""
        with self._lock:
            if not self:
                return ([], [])
            return tuple(list(x) for x in zip(*self))

    def rotate(self, n: int = 1) -> 'Vector':
        """Rotate elements by n positions."""
        with self._lock:
            if not self:
                return self
            n = n % len(self)
            self[:] = list(self[-n:]) + list(self[:-n])
            return self

    def interleave(self, other) -> 'Vector':
        """Interleave with another sequence."""
        with self._lock:
            result = Vector(self._element_type)
            other_list = list(other)
            for i in range(max(len(self), len(other_list))):
                if i < len(self):
                    result.append(self[i])
                if i < len(other_list):
                    result.append(other_list[i])
            return result

    def compact(self) -> 'Vector':
        """Remove None values."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend([x for x in self if x is not None])
            return result

    def frequencies(self) -> dict:
        """Count occurrences."""
        with self._lock:
            freq = {}
            for x in self:
                key = x if isinstance(x, (int, str, float, bool)) else str(x)
                freq[key] = freq.get(key, 0) + 1
            return freq

    def sample(self, n: int = 1) -> list:
        """Random sample."""
        import random
        with self._lock:
            return random.sample(list(self), min(n, len(self)))

    def takeWhile(self, predicate: Callable) -> 'Vector':
        """Take while predicate is true."""
        with self._lock:
            result = Vector(self._element_type)
            for x in self:
                if not predicate(x):
                    break
                result.append(x)
            return result

    def dropWhile(self, predicate: Callable) -> 'Vector':
        """Drop while predicate is true."""
        with self._lock:
            result = Vector(self._element_type)
            dropping = True
            for x in self:
                if dropping and predicate(x):
                    continue
                dropping = False
                result.append(x)
            return result

    def take(self, n: int) -> 'Vector':
        """Take first n elements."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(self[:n])
            return result

    def drop(self, n: int) -> 'Vector':
        """Drop first n elements."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(self[n:])
            return result

    def head(self, n: int = 1) -> 'Vector':
        """Get first n elements."""
        return self.take(n)

    def tail(self, n: int = 1) -> 'Vector':
        """Get last n elements."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(self[-n:] if n > 0 else [])
            return result

    def splitAt(self, index: int) -> tuple:
        """Split at index."""
        with self._lock:
            left = Vector(self._element_type)
            right = Vector(self._element_type)
            left.extend(self[:index])
            right.extend(self[index:])
            return (left, right)

    def distinct(self) -> 'Vector':
        """Remove duplicates."""
        with self._lock:
            seen = set()
            result = Vector(self._element_type)
            for x in self:
                key = x if isinstance(x, (int, str, float, bool)) else id(x)
                if key not in seen:
                    seen.add(key)
                    result.append(x)
            return result

    def dedupe(self) -> 'Vector':
        """Remove consecutive duplicates."""
        with self._lock:
            result = Vector(self._element_type)
            prev = object()
            for x in self:
                if x != prev:
                    result.append(x)
                    prev = x
            return result

    def min_val(self):
        """Get minimum."""
        with self._lock:
            return min(self) if self else None

    def max_val(self):
        """Get maximum."""
        with self._lock:
            return max(self) if self else None

    def sum_val(self):
        """Get sum."""
        with self._lock:
            return sum(self) if self else 0

    def avg(self):
        """Get average."""
        with self._lock:
            return sum(self) / len(self) if self else 0

    def product(self):
        """Get product."""
        with self._lock:
            result = 1
            for x in self:
                result *= x
            return result

    def sortBy(self, key_func: Callable) -> 'Vector':
        """Sort by key function."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(sorted(self, key=key_func))
            return result

    def sortDesc(self) -> 'Vector':
        """Sort descending."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend(sorted(self, reverse=True))
            return result

    def shuffle_elements(self) -> 'Vector':
        """Shuffle randomly."""
        import random
        with self._lock:
            items = list(self)
            random.shuffle(items)
            self[:] = items
            return self

    def randomElement(self):
        """Get random element."""
        import random
        with self._lock:
            return random.choice(list(self)) if self else None

    def findLast(self, predicate: Callable):
        """Find last matching."""
        with self._lock:
            for x in reversed(self):
                if predicate(x):
                    return x
            return None

    def findLastIndex(self, predicate: Callable) -> int:
        """Find index of last matching."""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if predicate(self[i]):
                    return i
            return -1

    def countWhere(self, predicate: Callable) -> int:
        """Count matching."""
        with self._lock:
            return sum(1 for x in self if predicate(x))

    def none(self, predicate: Callable) -> bool:
        """Check if none match."""
        with self._lock:
            return not any(predicate(x) for x in self)

    def flatMap(self, func: Callable) -> 'Vector':
        """Map then flatten."""
        with self._lock:
            result = Vector(self._element_type)
            for x in self:
                mapped = func(x)
                if isinstance(mapped, (list, tuple)):
                    result.extend(mapped)
                else:
                    result.append(mapped)
            return result

    def mapIndexed(self, func: Callable) -> 'Vector':
        """Map with index."""
        with self._lock:
            result = Vector(self._element_type)
            result.extend([func(i, x) for i, x in enumerate(self)])
            return result


class Array(list):
    """Array data structure with CSSL methods. v4.7.1: Thread-safe.

    Standard array with push/pop/length operations.

    Usage:
        array<string> arr;
        arr.push("Item");
        arr.length();  # Returns 1
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type
        self._lock = threading.RLock()

    def push(self, item: Any) -> 'Array':
        """Add item to end"""
        with self._lock:
            self.append(item)
        return self

    def push_back(self, item: Any) -> 'Array':
        """Add item to end (alias for push)"""
        with self._lock:
            self.append(item)
        return self

    def push_front(self, item: Any) -> 'Array':
        """Add item to front"""
        with self._lock:
            self.insert(0, item)
        return self

    def pop_back(self) -> Any:
        """Remove and return last element"""
        with self._lock:
            return self.pop() if self else None

    def pop_front(self) -> Any:
        """Remove and return first element"""
        with self._lock:
            return self.pop(0) if self else None

    def at(self, index: int) -> Any:
        """Get item at index with bounds checking (C++ style).

        v4.7.1: Now raises IndexError instead of returning None.
        """
        with self._lock:
            if index < 0 or index >= len(self):
                raise IndexError(f"Array index {index} out of range [0, {len(self)})")
            return self[index]

    def set(self, index: int, value: Any) -> 'Array':
        """Set item at index"""
        with self._lock:
            if 0 <= index < len(self):
                self[index] = value
        return self

    def size(self) -> int:
        """Return array size"""
        with self._lock:
            return len(self)

    def length(self) -> int:
        """Return array length"""
        with self._lock:
            return len(self)

    def empty(self) -> bool:
        """Check if array is empty"""
        with self._lock:
            return len(self) == 0

    def isEmpty(self) -> bool:
        """Check if array is empty (camelCase alias)"""
        with self._lock:
            return len(self) == 0

    def first(self) -> Any:
        """Get first element"""
        with self._lock:
            return self[0] if self else None

    def last(self) -> Any:
        """Get last element"""
        with self._lock:
            return self[-1] if self else None

    def contains(self, item: Any) -> bool:
        """Check if array contains item"""
        with self._lock:
            return item in self

    def indexOf(self, item: Any) -> int:
        """Find index of item (-1 if not found)"""
        with self._lock:
            try:
                return self.index(item)
            except ValueError:
                return -1

    def lastIndexOf(self, item: Any) -> int:
        """Find last index of item (-1 if not found)"""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if self[i] == item:
                    return i
            return -1

    def find(self, predicate: Callable[[Any], bool]) -> Any:
        """Find first item matching predicate"""
        with self._lock:
            for item in self:
                if callable(predicate) and predicate(item):
                    return item
                elif item == predicate:
                    return item
            return None

    def findIndex(self, predicate: Callable[[Any], bool]) -> int:
        """Find index of first item matching predicate"""
        with self._lock:
            for i, item in enumerate(self):
                if callable(predicate) and predicate(item):
                    return i
                elif item == predicate:
                    return i
            return -1

    def slice(self, start: int, end: int = None) -> 'Array':
        """Return slice of array"""
        with self._lock:
            result = Array(self._element_type)
            if end is None:
                result.extend(self[start:])
            else:
                result.extend(self[start:end])
            return result

    def join(self, separator: str = ',') -> str:
        """Join elements into string"""
        with self._lock:
            return separator.join(str(item) for item in self)

    def map(self, func: Callable[[Any], Any]) -> 'Array':
        """Apply function to all elements"""
        with self._lock:
            result = Array(self._element_type)
            result.extend(func(item) for item in self)
            return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'Array':
        """Filter elements by predicate"""
        with self._lock:
            result = Array(self._element_type)
            result.extend(item for item in self if predicate(item))
            return result

    def forEach(self, func: Callable[[Any], None]) -> 'Array':
        """Execute function for each element"""
        with self._lock:
            for item in self:
                func(item)
        return self

    def toArray(self) -> list:
        """Convert to plain list"""
        with self._lock:
            return list(self)

    def fill(self, value: Any, start: int = 0, end: int = None) -> 'Array':
        """Fill range with value"""
        with self._lock:
            if end is None:
                end = len(self)
            for i in range(start, min(end, len(self))):
                self[i] = value
        return self

    def every(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if all elements match predicate"""
        with self._lock:
            return all(predicate(item) for item in self)

    def some(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if any element matches predicate"""
        with self._lock:
            return any(predicate(item) for item in self)

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Reduce array to single value"""
        with self._lock:
            from functools import reduce as py_reduce
            if initial is None:
                return py_reduce(func, self)
            return py_reduce(func, self, initial)

    def concat(self, *arrays) -> 'Array':
        """Concatenate with other arrays"""
        with self._lock:
            result = Array(self._element_type)
            result.extend(self)
            for arr in arrays:
                result.extend(arr)
            return result

    def flat(self, depth: int = 1) -> 'Array':
        """Flatten nested arrays"""
        with self._lock:
            result = Array(self._element_type)
            for item in self:
                if isinstance(item, (list, Array)) and depth > 0:
                    if depth == 1:
                        result.extend(item)
                    else:
                        nested = Array(self._element_type)
                        nested.extend(item)
                        result.extend(nested.flat(depth - 1))
                else:
                    result.append(item)
            return result

    def unique(self) -> 'Array':
        """Return array with unique elements"""
        with self._lock:
            result = Array(self._element_type)
            seen = set()
            for item in self:
                key = item if isinstance(item, (int, str, float, bool)) else id(item)
                if key not in seen:
                    seen.add(key)
                    result.append(item)
            return result

    def begin(self) -> int:
        """Return iterator to beginning (C++ style)"""
        return 0

    def end(self) -> int:
        """Return iterator to end (C++ style)"""
        return len(self)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def chunk(self, size: int) -> list:
        """Split into chunks."""
        with self._lock:
            return [list(self[i:i+size]) for i in range(0, len(self), size)]

    def partition(self, predicate: Callable) -> tuple:
        """Split into (matching, non-matching)."""
        with self._lock:
            matching = [x for x in self if predicate(x)]
            non_matching = [x for x in self if not predicate(x)]
            return (matching, non_matching)

    def groupBy(self, key_func: Callable) -> dict:
        """Group by key function."""
        with self._lock:
            groups = {}
            for x in self:
                k = key_func(x)
                if k not in groups:
                    groups[k] = []
                groups[k].append(x)
            return groups

    def zip_with(self, *others) -> list:
        """Zip with other iterables."""
        with self._lock:
            return list(zip(self, *others))

    def rotate(self, n: int = 1) -> 'Array':
        """Rotate elements."""
        with self._lock:
            if not self:
                return self
            n = n % len(self)
            self[:] = list(self[-n:]) + list(self[:-n])
            return self

    def interleave(self, other) -> 'Array':
        """Interleave with another sequence."""
        with self._lock:
            result = Array(self._element_type)
            other_list = list(other)
            for i in range(max(len(self), len(other_list))):
                if i < len(self):
                    result.append(self[i])
                if i < len(other_list):
                    result.append(other_list[i])
            return result

    def compact(self) -> 'Array':
        """Remove None values."""
        with self._lock:
            result = Array(self._element_type)
            result.extend([x for x in self if x is not None])
            return result

    def frequencies(self) -> dict:
        """Count occurrences."""
        with self._lock:
            freq = {}
            for x in self:
                key = x if isinstance(x, (int, str, float, bool)) else str(x)
                freq[key] = freq.get(key, 0) + 1
            return freq

    def sample(self, n: int = 1) -> list:
        """Random sample."""
        import random
        with self._lock:
            return random.sample(list(self), min(n, len(self)))

    def takeWhile(self, predicate: Callable) -> 'Array':
        """Take while predicate is true."""
        with self._lock:
            result = Array(self._element_type)
            for x in self:
                if not predicate(x):
                    break
                result.append(x)
            return result

    def dropWhile(self, predicate: Callable) -> 'Array':
        """Drop while predicate is true."""
        with self._lock:
            result = Array(self._element_type)
            dropping = True
            for x in self:
                if dropping and predicate(x):
                    continue
                dropping = False
                result.append(x)
            return result

    def take(self, n: int) -> 'Array':
        """Take first n."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(self[:n])
            return result

    def drop(self, n: int) -> 'Array':
        """Drop first n."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(self[n:])
            return result

    def head(self, n: int = 1) -> 'Array':
        """Get first n."""
        return self.take(n)

    def tail(self, n: int = 1) -> 'Array':
        """Get last n."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(self[-n:] if n > 0 else [])
            return result

    def splitAt(self, index: int) -> tuple:
        """Split at index."""
        with self._lock:
            left = Array(self._element_type)
            right = Array(self._element_type)
            left.extend(self[:index])
            right.extend(self[index:])
            return (left, right)

    def distinct(self) -> 'Array':
        """Remove duplicates."""
        return self.unique()

    def dedupe(self) -> 'Array':
        """Remove consecutive duplicates."""
        with self._lock:
            result = Array(self._element_type)
            prev = object()
            for x in self:
                if x != prev:
                    result.append(x)
                    prev = x
            return result

    def min_val(self):
        """Get minimum."""
        with self._lock:
            return min(self) if self else None

    def max_val(self):
        """Get maximum."""
        with self._lock:
            return max(self) if self else None

    def sum_val(self):
        """Get sum."""
        with self._lock:
            return sum(self) if self else 0

    def avg(self):
        """Get average."""
        with self._lock:
            return sum(self) / len(self) if self else 0

    def product(self):
        """Get product."""
        with self._lock:
            result = 1
            for x in self:
                result *= x
            return result

    def sortBy(self, key_func: Callable) -> 'Array':
        """Sort by key function."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(sorted(self, key=key_func))
            return result

    def sortDesc(self) -> 'Array':
        """Sort descending."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(sorted(self, reverse=True))
            return result

    def shuffle_elements(self) -> 'Array':
        """Shuffle randomly."""
        import random
        with self._lock:
            items = list(self)
            random.shuffle(items)
            self[:] = items
            return self

    def randomElement(self):
        """Get random element."""
        import random
        with self._lock:
            return random.choice(list(self)) if self else None

    def findLast(self, predicate: Callable):
        """Find last matching."""
        with self._lock:
            for x in reversed(self):
                if predicate(x):
                    return x
            return None

    def findLastIndex(self, predicate: Callable) -> int:
        """Find index of last matching."""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if predicate(self[i]):
                    return i
            return -1

    def countWhere(self, predicate: Callable) -> int:
        """Count matching."""
        with self._lock:
            return sum(1 for x in self if predicate(x))

    def none(self, predicate: Callable) -> bool:
        """Check if none match."""
        with self._lock:
            return not any(predicate(x) for x in self)

    def flatMap(self, func: Callable) -> 'Array':
        """Map then flatten."""
        with self._lock:
            result = Array(self._element_type)
            for x in self:
                mapped = func(x)
                if isinstance(mapped, (list, tuple)):
                    result.extend(mapped)
                else:
                    result.append(mapped)
            return result

    def mapIndexed(self, func: Callable) -> 'Array':
        """Map with index."""
        with self._lock:
            result = Array(self._element_type)
            result.extend([func(i, x) for i, x in enumerate(self)])
            return result

    def reverse_copy(self) -> 'Array':
        """Return reversed copy."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(reversed(self))
            return result

    def sort_copy(self) -> 'Array':
        """Return sorted copy."""
        with self._lock:
            result = Array(self._element_type)
            result.extend(sorted(self))
            return result


class List(list):
    """Python-like list with all standard operations. v4.7.1: Thread-safe.

    Works exactly like Python lists with additional CSSL methods.

    Usage:
        list myList;
        myList.append("item");
        myList.insert(0, "first");
        myList.pop();
        myList.find("item");  # Returns index or -1
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type
        self._lock = threading.RLock()

    def length(self) -> int:
        """Return list length"""
        with self._lock:
            return len(self)

    def size(self) -> int:
        """Return list size (alias for length)"""
        with self._lock:
            return len(self)

    def isEmpty(self) -> bool:
        """Check if list is empty"""
        with self._lock:
            return len(self) == 0

    def first(self) -> Any:
        """Get first element"""
        with self._lock:
            return self[0] if self else None

    def last(self) -> Any:
        """Get last element"""
        with self._lock:
            return self[-1] if self else None

    def at(self, index: int) -> Any:
        """Get item at index with bounds checking (C++ style).
        v4.7.1: Now raises IndexError instead of returning None.
        """
        with self._lock:
            if index < 0 or index >= len(self):
                raise IndexError(f"List index {index} out of range [0, {len(self)})")
            return self[index]

    def set(self, index: int, value: Any) -> 'List':
        """Set item at index"""
        with self._lock:
            if 0 <= index < len(self):
                self[index] = value
        return self

    def add(self, item: Any) -> 'List':
        """Add item to end (alias for append)"""
        with self._lock:
            self.append(item)
        return self

    def push(self, item: Any) -> 'List':
        """Push item to end (alias for append)"""
        with self._lock:
            self.append(item)
        return self

    def find(self, item: Any) -> int:
        """Find index of item (-1 if not found)"""
        with self._lock:
            try:
                return self.index(item)
            except ValueError:
                return -1

    def contains(self, item: Any) -> bool:
        """Check if list contains item"""
        with self._lock:
            return item in self

    def indexOf(self, item: Any) -> int:
        """Find index of item (-1 if not found)"""
        return self.find(item)

    def lastIndexOf(self, item: Any) -> int:
        """Find last index of item (-1 if not found)"""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if self[i] == item:
                    return i
            return -1

    def removeAt(self, index: int) -> Any:
        """Remove and return item at index"""
        with self._lock:
            if 0 <= index < len(self):
                return self.pop(index)
            return None

    def removeValue(self, value: Any) -> bool:
        """Remove first occurrence of value"""
        with self._lock:
            try:
                self.remove(value)
                return True
            except ValueError:
                return False

    def removeAll(self, value: Any) -> int:
        """Remove all occurrences of value, return count"""
        with self._lock:
            count = 0
            while value in self:
                self.remove(value)
                count += 1
            return count

    def slice(self, start: int, end: int = None) -> 'List':
        """Return slice of list"""
        with self._lock:
            result = List(self._element_type)
            if end is None:
                result.extend(self[start:])
            else:
                result.extend(self[start:end])
            return result

    def join(self, separator: str = ',') -> str:
        """Join elements into string"""
        with self._lock:
            return separator.join(str(item) for item in self)

    def unique(self) -> 'List':
        """Return list with unique elements"""
        with self._lock:
            result = List(self._element_type)
            seen = set()
            for item in self:
                key = item if isinstance(item, (int, str, float, bool)) else id(item)
                if key not in seen:
                    seen.add(key)
                    result.append(item)
            return result

    def sorted(self, reverse: bool = False) -> 'List':
        """Return sorted copy"""
        with self._lock:
            result = List(self._element_type)
            result.extend(sorted(self, reverse=reverse))
            return result

    def reversed(self) -> 'List':
        """Return reversed copy"""
        with self._lock:
            result = List(self._element_type)
            result.extend(reversed(self))
            return result

    def shuffle(self) -> 'List':
        """Shuffle list in place"""
        with self._lock:
            import random
            random.shuffle(self)
        return self

    def fill(self, value: Any, count: int = None) -> 'List':
        """Fill list with value"""
        with self._lock:
            if count is None:
                for i in range(len(self)):
                    self[i] = value
            else:
                self.clear()
                self.extend([value] * count)
        return self

    def map(self, func: Callable[[Any], Any]) -> 'List':
        """Apply function to all elements"""
        with self._lock:
            result = List(self._element_type)
            result.extend(func(item) for item in self)
            return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'List':
        """Filter elements by predicate"""
        with self._lock:
            result = List(self._element_type)
            result.extend(item for item in self if predicate(item))
            return result

    def forEach(self, func: Callable[[Any], None]) -> 'List':
        """Execute function for each element"""
        with self._lock:
            for item in self:
                func(item)
        return self

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Reduce list to single value"""
        with self._lock:
            from functools import reduce as py_reduce
            if initial is None:
                return py_reduce(func, self)
            return py_reduce(func, self, initial)

    def every(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if all elements match predicate"""
        with self._lock:
            return all(predicate(item) for item in self)

    def some(self, predicate: Callable[[Any], bool]) -> bool:
        """Check if any element matches predicate"""
        with self._lock:
            return any(predicate(item) for item in self)

    def begin(self) -> int:
        """Return iterator to beginning"""
        return 0

    def end(self) -> int:
        """Return iterator to end"""
        return len(self)

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds

    def chunk(self, size: int) -> list:
        """Split into chunks."""
        with self._lock:
            return [list(self[i:i+size]) for i in range(0, len(self), size)]

    def partition(self, predicate: Callable) -> tuple:
        """Split into (matching, non-matching)."""
        with self._lock:
            matching = [x for x in self if predicate(x)]
            non_matching = [x for x in self if not predicate(x)]
            return (matching, non_matching)

    def groupBy(self, key_func: Callable) -> dict:
        """Group by key function."""
        with self._lock:
            groups = {}
            for x in self:
                k = key_func(x)
                if k not in groups:
                    groups[k] = []
                groups[k].append(x)
            return groups

    def zip_with(self, *others) -> list:
        """Zip with other iterables."""
        with self._lock:
            return list(zip(self, *others))

    def rotate(self, n: int = 1) -> 'List':
        """Rotate elements."""
        with self._lock:
            if not self:
                return self
            n = n % len(self)
            self[:] = list(self[-n:]) + list(self[:-n])
            return self

    def interleave(self, other) -> 'List':
        """Interleave with another sequence."""
        with self._lock:
            result = List()
            other_list = list(other)
            for i in range(max(len(self), len(other_list))):
                if i < len(self):
                    result.append(self[i])
                if i < len(other_list):
                    result.append(other_list[i])
            return result

    def compact(self) -> 'List':
        """Remove None values."""
        with self._lock:
            result = List()
            result.extend([x for x in self if x is not None])
            return result

    def frequencies(self) -> dict:
        """Count occurrences."""
        with self._lock:
            freq = {}
            for x in self:
                key = x if isinstance(x, (int, str, float, bool)) else str(x)
                freq[key] = freq.get(key, 0) + 1
            return freq

    def sample_items(self, n: int = 1) -> list:
        """Random sample."""
        import random
        with self._lock:
            return random.sample(list(self), min(n, len(self)))

    def takeWhile(self, predicate: Callable) -> 'List':
        """Take while predicate is true."""
        with self._lock:
            result = List()
            for x in self:
                if not predicate(x):
                    break
                result.append(x)
            return result

    def dropWhile(self, predicate: Callable) -> 'List':
        """Drop while predicate is true."""
        with self._lock:
            result = List()
            dropping = True
            for x in self:
                if dropping and predicate(x):
                    continue
                dropping = False
                result.append(x)
            return result

    def take(self, n: int) -> 'List':
        """Take first n."""
        with self._lock:
            result = List()
            result.extend(self[:n])
            return result

    def drop(self, n: int) -> 'List':
        """Drop first n."""
        with self._lock:
            result = List()
            result.extend(self[n:])
            return result

    def head(self, n: int = 1) -> 'List':
        """Get first n."""
        return self.take(n)

    def tail_items(self, n: int = 1) -> 'List':
        """Get last n."""
        with self._lock:
            result = List()
            result.extend(self[-n:] if n > 0 else [])
            return result

    def splitAt(self, index: int) -> tuple:
        """Split at index."""
        with self._lock:
            left = List()
            right = List()
            left.extend(self[:index])
            right.extend(self[index:])
            return (left, right)

    def distinct(self) -> 'List':
        """Remove duplicates."""
        return self.unique()

    def dedupe(self) -> 'List':
        """Remove consecutive duplicates."""
        with self._lock:
            result = List()
            prev = object()
            for x in self:
                if x != prev:
                    result.append(x)
                    prev = x
            return result

    def min_val(self):
        """Get minimum."""
        with self._lock:
            return min(self) if self else None

    def max_val(self):
        """Get maximum."""
        with self._lock:
            return max(self) if self else None

    def sum_val(self):
        """Get sum."""
        with self._lock:
            return sum(self) if self else 0

    def avg(self):
        """Get average."""
        with self._lock:
            return sum(self) / len(self) if self else 0

    def product(self):
        """Get product."""
        with self._lock:
            result = 1
            for x in self:
                result *= x
            return result

    def sortBy(self, key_func: Callable) -> 'List':
        """Sort by key function."""
        with self._lock:
            result = List()
            result.extend(sorted(self, key=key_func))
            return result

    def sortDesc(self) -> 'List':
        """Sort descending."""
        with self._lock:
            result = List()
            result.extend(sorted(self, reverse=True))
            return result

    def randomElement(self):
        """Get random element."""
        import random
        with self._lock:
            return random.choice(list(self)) if self else None

    def findLast(self, predicate: Callable):
        """Find last matching."""
        with self._lock:
            for x in reversed(self):
                if predicate(x):
                    return x
            return None

    def findLastIndex(self, predicate: Callable) -> int:
        """Find index of last matching."""
        with self._lock:
            for i in range(len(self) - 1, -1, -1):
                if predicate(self[i]):
                    return i
            return -1

    def countWhere(self, predicate: Callable) -> int:
        """Count matching."""
        with self._lock:
            return sum(1 for x in self if predicate(x))

    def none(self, predicate: Callable) -> bool:
        """Check if none match."""
        with self._lock:
            return not any(predicate(x) for x in self)

    def flatMap(self, func: Callable) -> 'List':
        """Map then flatten."""
        with self._lock:
            result = List()
            for x in self:
                mapped = func(x)
                if isinstance(mapped, (list, tuple)):
                    result.extend(mapped)
                else:
                    result.append(mapped)
            return result

    def mapIndexed(self, func: Callable) -> 'List':
        """Map with index."""
        with self._lock:
            result = List()
            result.extend([func(i, x) for i, x in enumerate(self)])
            return result

    def concat(self, *others) -> 'List':
        """Concatenate with other lists."""
        with self._lock:
            result = List()
            result.extend(self)
            for other in others:
                result.extend(other)
            return result

    def flatten(self, depth: int = 1) -> 'List':
        """Flatten nested lists."""
        def _flatten(lst, d):
            result = []
            for item in lst:
                if isinstance(item, (list, tuple)) and d > 0:
                    result.extend(_flatten(item, d - 1))
                else:
                    result.append(item)
            return result
        with self._lock:
            flat_list = List()
            flat_list.extend(_flatten(self, depth))
            return flat_list


class Dictionary(dict):
    """Python-like dictionary with all standard operations. v4.7.1: Thread-safe.

    Works exactly like Python dicts with additional CSSL methods.

    Usage:
        dictionary myDict;
        myDict.set("key", "value");
        myDict.get("key");
        myDict.keys();
        myDict.values();
    """

    def __init__(self, key_type: str = 'dynamic', value_type: str = 'dynamic'):
        super().__init__()
        self._key_type = key_type
        self._value_type = value_type
        self._lock = threading.RLock()

    def length(self) -> int:
        """Return dictionary size"""
        with self._lock:
            return len(self)

    def size(self) -> int:
        """Return dictionary size (alias for length)"""
        with self._lock:
            return len(self)

    def isEmpty(self) -> bool:
        """Check if dictionary is empty"""
        with self._lock:
            return len(self) == 0

    def set(self, key: Any, value: Any) -> 'Dictionary':
        """Set key-value pair"""
        with self._lock:
            self[key] = value
        return self

    def hasKey(self, key: Any) -> bool:
        """Check if key exists"""
        with self._lock:
            return key in self

    def hasValue(self, value: Any) -> bool:
        """Check if value exists"""
        with self._lock:
            return value in self.values()

    def remove(self, key: Any) -> Any:
        """Remove and return value for key"""
        with self._lock:
            return self.pop(key, None)

    def getOrDefault(self, key: Any, default: Any = None) -> Any:
        """Get value or default if not found"""
        with self._lock:
            return self.get(key, default)

    def setDefault(self, key: Any, default: Any) -> Any:
        """Set default if key doesn't exist, return value"""
        with self._lock:
            if key not in self:
                self[key] = default
            return self[key]

    def merge(self, other: dict) -> 'Dictionary':
        """Merge another dictionary into this one"""
        with self._lock:
            self.update(other)
        return self

    def keysList(self) -> list:
        """Return keys as list"""
        with self._lock:
            return list(self.keys())

    def valuesList(self) -> list:
        """Return values as list"""
        with self._lock:
            return list(self.values())

    def itemsList(self) -> list:
        """Return items as list of tuples"""
        with self._lock:
            return list(self.items())

    def filter(self, predicate: Callable[[Any, Any], bool]) -> 'Dictionary':
        """Filter dictionary by predicate(key, value)"""
        with self._lock:
            result = Dictionary(self._key_type, self._value_type)
            for k, v in self.items():
                if predicate(k, v):
                    result[k] = v
            return result

    def map(self, func: Callable[[Any, Any], Any]) -> 'Dictionary':
        """Apply function to all values"""
        with self._lock:
            result = Dictionary(self._key_type, self._value_type)
            for k, v in self.items():
                result[k] = func(k, v)
            return result

    def forEach(self, func: Callable[[Any, Any], None]) -> 'Dictionary':
        """Execute function for each key-value pair"""
        with self._lock:
            for k, v in self.items():
                func(k, v)
        return self

    def invert(self) -> 'Dictionary':
        """Swap keys and values"""
        with self._lock:
            result = Dictionary(self._value_type, self._key_type)
            for k, v in self.items():
                result[v] = k
            return result

    def find(self, value: Any) -> Optional[Any]:
        """Find first key with given value"""
        with self._lock:
            for k, v in self.items():
                if v == value:
                    return k
            return None

    def findAll(self, value: Any) -> list:
        """Find all keys with given value"""
        with self._lock:
            return [k for k, v in self.items() if v == value]

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds


class Shuffled(list):
    """Unorganized fast storage for multiple returns.

    Stores data unorganized for fast and efficient access.
    Supports receiving multiple return values from functions.
    Can be used as a function modifier to allow multiple returns.

    Usage:
        shuffled<string> results;
        results +<== someFunc();  # Catches all returns
        results.read()  # Returns all content as list

        # As return modifier:
        shuffled string getData() {
            return "name", "address";  # Returns multiple values
        }
    """

    def __init__(self, element_type: str = 'dynamic'):
        super().__init__()
        self._element_type = element_type

    def read(self) -> list:
        """Return all content as a list"""
        return list(self)

    def collect(self, func: Callable, *args) -> 'Shuffled':
        """Collect all returns from a function"""
        result = func(*args)
        if isinstance(result, (list, tuple)):
            self.extend(result)
        else:
            self.append(result)
        return self

    def add(self, *items) -> 'Shuffled':
        """Add one or more items"""
        for item in items:
            if isinstance(item, (list, tuple)):
                self.extend(item)
            else:
                self.append(item)
        return self

    def first(self) -> Any:
        """Get first element"""
        return self[0] if self else None

    def last(self) -> Any:
        """Get last element"""
        return self[-1] if self else None

    def length(self) -> int:
        """Return shuffled length"""
        return len(self)

    def isEmpty(self) -> bool:
        """Check if empty"""
        return len(self) == 0

    def contains(self, item: Any) -> bool:
        """Check if contains item"""
        return item in self

    def at(self, index: int) -> Any:
        """Get item at index with bounds checking.
        v4.7.1: Now raises IndexError instead of returning None.
        """
        if index < 0 or index >= len(self):
            raise IndexError(f"Shuffled index {index} out of range [0, {len(self)})")
        return self[index]

    def toList(self) -> list:
        """Convert to plain list"""
        return list(self)

    def toTuple(self) -> tuple:
        """Convert to tuple"""
        return tuple(self)


class Iterator:
    """Advanced iterator with programmable tasks.

    Provides iterator positions within a data container with
    the ability to attach tasks (functions) to iterators.

    Usage:
        iterator<int, 16> Map;  # Create 16-element iterator space
        Map::iterator::set(0, 5);  # Set iterator 0 to position 5
        Map::iterator::task(0, myFunc);  # Attach task to iterator
    """

    def __init__(self, element_type: str = 'int', size: int = 16):
        self._element_type = element_type
        self._size = size
        self._data: List[Any] = [None] * size
        self._iterators: Dict[int, int] = {0: 0, 1: 1}  # Default: 2 iterators at positions 0 and 1
        self._tasks: Dict[int, Callable] = {}

    def insert(self, index: int, value: Any) -> 'Iterator':
        """Insert value at index"""
        if 0 <= index < self._size:
            self._data[index] = value
        return self

    def fill(self, value: Any) -> 'Iterator':
        """Fill all positions with value"""
        self._data = [value] * self._size
        return self

    def at(self, index: int) -> Any:
        """Get value at index"""
        if 0 <= index < self._size:
            return self._data[index]
        return None

    def is_all(self, check_value: bool) -> bool:
        """Check if all values are 1 (True) or 0 (False)"""
        expected = 1 if check_value else 0
        return all(v == expected for v in self._data if v is not None)

    def end(self) -> int:
        """Return last index"""
        return self._size - 1

    class IteratorControl:
        """Static methods for iterator control"""

        @staticmethod
        def set(iterator_obj: 'Iterator', iterator_id: int, position: int):
            """Set iterator position"""
            iterator_obj._iterators[iterator_id] = position

        @staticmethod
        def move(iterator_obj: 'Iterator', iterator_id: int, steps: int):
            """Move iterator by steps"""
            if iterator_id in iterator_obj._iterators:
                iterator_obj._iterators[iterator_id] += steps

        @staticmethod
        def insert(iterator_obj: 'Iterator', iterator_id: int, value: Any):
            """Insert value at current iterator position"""
            if iterator_id in iterator_obj._iterators:
                pos = iterator_obj._iterators[iterator_id]
                if 0 <= pos < iterator_obj._size:
                    iterator_obj._data[pos] = value

        @staticmethod
        def pop(iterator_obj: 'Iterator', iterator_id: int):
            """Delete value at current iterator position"""
            if iterator_id in iterator_obj._iterators:
                pos = iterator_obj._iterators[iterator_id]
                if 0 <= pos < iterator_obj._size:
                    iterator_obj._data[pos] = None

        @staticmethod
        def task(iterator_obj: 'Iterator', iterator_id: int, func: Callable):
            """Attach a task function to iterator"""
            iterator_obj._tasks[iterator_id] = func

        @staticmethod
        def dtask(iterator_obj: 'Iterator', iterator_id: int):
            """Clear task from iterator"""
            if iterator_id in iterator_obj._tasks:
                del iterator_obj._tasks[iterator_id]

        @staticmethod
        def run_task(iterator_obj: 'Iterator', iterator_id: int):
            """Run the task at current iterator position"""
            if iterator_id in iterator_obj._tasks and iterator_id in iterator_obj._iterators:
                pos = iterator_obj._iterators[iterator_id]
                task = iterator_obj._tasks[iterator_id]
                # Create a position wrapper
                class IteratorPos:
                    def __init__(self, data, idx):
                        self._data = data
                        self._idx = idx
                    def read(self):
                        return self._data[self._idx]
                    def write(self, value):
                        self._data[self._idx] = value

                task(IteratorPos(iterator_obj._data, pos))


class Combo:
    """Filter/search space for open parameter matching.

    Creates a search/filter space that can match parameters
    based on filter databases and similarity.

    Usage:
        combo<open&string> nameSpace;
        nameSpace +<== [combo::filterdb] filterDB;
        special_name = OpenFind(&nameSpace);
    """

    def __init__(self, element_type: str = 'dynamic'):
        self._element_type = element_type
        self._filterdb: List[Any] = []
        self._blocked: List[Any] = []
        self._data: List[Any] = []
        self._like_pattern: Optional[str] = None

    @property
    def filterdb(self) -> List[Any]:
        return self._filterdb

    @filterdb.setter
    def filterdb(self, value: List[Any]):
        self._filterdb = value

    @property
    def blocked(self) -> List[Any]:
        return self._blocked

    @blocked.setter
    def blocked(self, value: List[Any]):
        self._blocked = value

    def like(self, pattern: str) -> 'Combo':
        """Set similarity pattern (94-100% match)"""
        self._like_pattern = pattern
        return self

    def matches(self, value: Any) -> bool:
        """Check if value matches combo criteria"""
        # Check if blocked
        if value in self._blocked:
            return False

        # Check filterdb if present
        if self._filterdb:
            if value not in self._filterdb:
                return False

        # Check like pattern if present
        if self._like_pattern and isinstance(value, str):
            similarity = self._calculate_similarity(value, self._like_pattern)
            if similarity < 0.94:
                return False

        return True

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity (simple Levenshtein-based)"""
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        # Simple character-based similarity
        s1_lower = s1.lower()
        s2_lower = s2.lower()

        matching = sum(c1 == c2 for c1, c2 in zip(s1_lower, s2_lower))
        return matching / max(len(s1), len(s2))

    def find_match(self, items: List[Any]) -> Optional[Any]:
        """Find first matching item from list"""
        for item in items:
            if self.matches(item):
                return item
        return None


class DataSpace(dict):
    """SQL/data storage container for structured data.

    Used for SQL table definitions and structured data storage.

    Usage:
        dataspace<sql::table> table = { ... };
        @Sql.Structured(&table);
    """

    def __init__(self, space_type: str = 'dynamic'):
        super().__init__()
        self._space_type = space_type
        self._sections: Dict[str, Any] = {}

    def content(self) -> dict:
        """Return all content"""
        return dict(self)

    def section(self, name: str, *types) -> 'DataSpace':
        """Create a section with specified types"""
        self._sections[name] = {
            'types': types,
            'data': []
        }
        return self


class OpenQuote:
    """SQL openquote container for organized data handling.

    Creates a datastruct together with sql::db.oqt() for easy
    data organization and retrieval.

    Usage:
        openquote<datastruct<dynamic>&@sql::db.oqt(@db)> Queue;
        Queue.save("Section", "data1", "data2", 123);
        Queue.where(Section="value", KEY="match");
    """

    def __init__(self, db_reference: Any = None):
        self._data: List[Dict[str, Any]] = []
        self._db_ref = db_reference

    def save(self, section: str, *values) -> 'OpenQuote':
        """Save data to a section"""
        self._data.append({
            'section': section,
            'values': list(values)
        })
        return self

    def where(self, **kwargs) -> Optional[Any]:
        """Find data matching criteria"""
        for entry in self._data:
            if all(entry.get(k) == v or (k == 'Section' and entry.get('section') == v)
                   for k, v in kwargs.items()):
                return entry
        return None

    def all(self) -> List[Dict[str, Any]]:
        """Return all data"""
        return self._data


class Parameter:
    """Parameter accessor for CSSL exec() arguments.

    Provides access to arguments passed to CSSL.exec() via parameter.get(index).

    Usage in CSSL:
        parameter.get(0)  # Get first argument
        parameter.get(1)  # Get second argument
        parameter.count() # Get total argument count
        parameter.all()   # Get all arguments as list
        parameter.return(value)  # Yield a return value (generator-like)
        parameter.returns()  # Get all yielded return values
    """

    def __init__(self, args: List[Any] = None):
        self._args = args if args is not None else []
        self._returns: List[Any] = []

    def get(self, index: int, default: Any = None) -> Any:
        """Get argument at index, returns default if not found"""
        if 0 <= index < len(self._args):
            return self._args[index]
        return default

    def count(self) -> int:
        """Return total number of arguments"""
        return len(self._args)

    def all(self) -> List[Any]:
        """Return all arguments as a list"""
        return list(self._args)

    def has(self, index: int) -> bool:
        """Check if argument exists at index"""
        return 0 <= index < len(self._args)

    # Using 'return_' to avoid Python keyword conflict
    def return_(self, value: Any) -> None:
        """Yield a return value (generator-like behavior).

        Multiple calls accumulate values that can be retrieved via returns().
        The CSSL runtime will collect these as the exec() return value.
        """
        self._returns.append(value)

    def returns(self) -> List[Any]:
        """Get all yielded return values"""
        return list(self._returns)

    def clear_returns(self) -> None:
        """Clear all yielded return values"""
        self._returns.clear()

    def has_returns(self) -> bool:
        """Check if any values have been returned"""
        return len(self._returns) > 0

    def __iter__(self):
        return iter(self._args)

    def __len__(self):
        return len(self._args)

    def __getitem__(self, index: int) -> Any:
        return self.get(index)


def OpenFind(combo_or_type: Union[Combo, type], index: int = 0) -> Optional[Any]:
    """Find open parameter by type or combo space.

    Usage:
        string name = OpenFind<string>(0);  # Find string at index 0
        string special = OpenFind(&@comboSpace);  # Find by combo
    """
    if isinstance(combo_or_type, Combo):
        # Find by combo space
        return combo_or_type.find_match([])  # Would need open params context
    elif isinstance(combo_or_type, type):
        # Find by type at index - needs open params context
        pass
    return None


# Type factory functions for CSSL
def create_datastruct(element_type: str = 'dynamic') -> DataStruct:
    return DataStruct(element_type)

def create_shuffled(element_type: str = 'dynamic') -> Shuffled:
    return Shuffled(element_type)

def create_iterator(element_type: str = 'int', size: int = 16) -> Iterator:
    return Iterator(element_type, size)

def create_combo(element_type: str = 'dynamic') -> Combo:
    return Combo(element_type)

def create_dataspace(space_type: str = 'dynamic') -> DataSpace:
    return DataSpace(space_type)

def create_openquote(db_ref: Any = None) -> OpenQuote:
    return OpenQuote(db_ref)

def create_stack(element_type: str = 'dynamic') -> Stack:
    return Stack(element_type)

def create_vector(element_type: str = 'dynamic') -> Vector:
    return Vector(element_type)

def create_parameter(args: List[Any] = None) -> Parameter:
    """Create a Parameter object for accessing exec arguments"""
    return Parameter(args)

def create_array(element_type: str = 'dynamic') -> Array:
    """Create an Array object"""
    return Array(element_type)


def create_list(element_type: str = 'dynamic') -> List:
    """Create a List object"""
    return List(element_type)


def create_dictionary(key_type: str = 'dynamic', value_type: str = 'dynamic') -> Dictionary:
    """Create a Dictionary object"""
    return Dictionary(key_type, value_type)


class Map(dict):
    """C++ style map container with ordered key-value pairs. v4.7.1: Thread-safe.

    Similar to Dictionary but with C++ map semantics.
    Keys are maintained in sorted order.

    Usage:
        map<string, int> ages;
        ages.insert("Alice", 30);
        ages.find("Alice");
        ages.erase("Alice");
    """

    def __init__(self, key_type: str = 'dynamic', value_type: str = 'dynamic'):
        super().__init__()
        self._key_type = key_type
        self._value_type = value_type
        self._lock = threading.RLock()

    def insert(self, key: Any, value: Any) -> 'Map':
        """Insert key-value pair (C++ style)"""
        with self._lock:
            self[key] = value
        return self

    def set(self, key: Any, value: Any) -> 'Map':
        """Set key-value pair (alias for insert)."""
        return self.insert(key, value)

    def find(self, key: Any) -> Optional[Any]:
        """Find value by key, returns None if not found (C++ style)"""
        with self._lock:
            return self.get(key, None)

    def erase(self, key: Any) -> bool:
        """Erase key-value pair, returns True if existed"""
        with self._lock:
            if key in self:
                del self[key]
                return True
            return False

    def contains(self, key: Any) -> bool:
        """Check if key exists (C++20 style)"""
        with self._lock:
            return key in self

    def count(self, key: Any) -> int:
        """Return 1 if key exists, 0 otherwise (C++ style)"""
        with self._lock:
            return 1 if key in self else 0

    def size(self) -> int:
        """Return map size"""
        with self._lock:
            return len(self)

    def empty(self) -> bool:
        """Check if map is empty"""
        with self._lock:
            return len(self) == 0

    def at(self, key: Any) -> Any:
        """Get value at key, raises error if not found (C++ style)"""
        with self._lock:
            if key not in self:
                raise KeyError(f"Key '{key}' not found in map")
            return self[key]

    def begin(self) -> Optional[tuple]:
        """Return first key-value pair"""
        with self._lock:
            if len(self) == 0:
                return None
            first_key = next(iter(self))
            return (first_key, self[first_key])

    def end(self) -> Optional[tuple]:
        """Return last key-value pair"""
        with self._lock:
            if len(self) == 0:
                return None
            last_key = list(self.keys())[-1]
            return (last_key, self[last_key])

    def lower_bound(self, key: Any) -> Optional[Any]:
        """Find first key >= given key (for sorted keys)"""
        with self._lock:
            sorted_keys = sorted(self.keys())
            for k in sorted_keys:
                if k >= key:
                    return k
            return None

    def upper_bound(self, key: Any) -> Optional[Any]:
        """Find first key > given key (for sorted keys)"""
        with self._lock:
            sorted_keys = sorted(self.keys())
            for k in sorted_keys:
                if k > key:
                    return k
            return None

    # === C++ STL Additional Methods (v4.7.1) ===

    def equal_range(self, key: Any) -> tuple:
        """Return (lower_bound, upper_bound) for key."""
        return (self.lower_bound(key), self.upper_bound(key))

    def emplace(self, key: Any, value: Any) -> bool:
        """Insert if not exists, return True if inserted."""
        with self._lock:
            if key in self:
                return False
            self[key] = value
            return True

    def insert_or_assign(self, key: Any, value: Any) -> bool:
        """Insert or update, return True if inserted."""
        with self._lock:
            existed = key in self
            self[key] = value
            return not existed

    def try_emplace(self, key: Any, *args) -> bool:
        """Insert only if key doesn't exist."""
        with self._lock:
            if key in self:
                return False
            self[key] = args[0] if args else None
            return True

    def extract(self, key: Any) -> Any:
        """Remove and return value."""
        with self._lock:
            return self.pop(key, None)

    def merge(self, other: 'Map') -> 'Map':
        """Merge another map (doesn't overwrite existing)."""
        with self._lock:
            for k, v in other.items():
                if k not in self:
                    self[k] = v
        return self

    def clear(self) -> 'Map':
        """Clear all entries."""
        with self._lock:
            super().clear()
        return self

    def swap(self, other: 'Map') -> 'Map':
        """Swap contents."""
        with self._lock:
            temp = dict(self)
            super().clear()
            super().update(other)
            other.clear()
            other.update(temp)
        return self

    def keys_list(self) -> list:
        """Return all keys as list."""
        with self._lock:
            return list(self.keys())

    def values_list(self) -> list:
        """Return all values as list."""
        with self._lock:
            return list(self.values())

    def items_list(self) -> list:
        """Return all (key, value) pairs as list."""
        with self._lock:
            return list(self.items())

    def get_or_default(self, key: Any, default: Any = None) -> Any:
        """Get with default."""
        with self._lock:
            return self.get(key, default)

    def set_default(self, key: Any, default: Any = None) -> Any:
        """Set default if not exists, return value."""
        with self._lock:
            return self.setdefault(key, default)

    def pop_item(self, key: Any, default: Any = None) -> Any:
        """Remove and return, or default."""
        with self._lock:
            return self.pop(key, default)

    def update_from(self, other: dict) -> 'Map':
        """Update from dict."""
        with self._lock:
            self.update(other)
        return self

    def copy(self) -> 'Map':
        """Return shallow copy."""
        with self._lock:
            new_map = Map(self._key_type, self._value_type)
            new_map.update(self)
            return new_map

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds


def create_map(key_type: str = 'dynamic', value_type: str = 'dynamic') -> Map:
    """Create a Map object"""
    return Map(key_type, value_type)




class Queue:
    """Thread-safe FIFO queue with optional size limits.

    Provides basic queue operations with thread-safety via locks.
    Supports bounded and dynamic sizing.

    Usage:
        queue<string, dynamic> TaskQueue;    // Unlimited size
        queue<int, 256> BoundedQueue;        // Fixed size 256

        // Basic operations
        TaskQueue.push("item");
        item = TaskQueue.pop();
        item = TaskQueue.peek();

        // Thread control
        TaskQueue.run(processFunc);          // Start auto-processing
        TaskQueue.stop();                    // Stop thread
    """

    def __init__(self, element_type: str = 'dynamic', size: Union[int, str] = 'dynamic'):
        self._element_type = element_type
        self._max_size = None if size == 'dynamic' else int(size)
        self._data: deque = deque(maxlen=self._max_size)
        self._lock = threading.RLock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._process_func: Optional[Callable] = None
        self._triggers: List[Callable] = []

    def push(self, item: Any) -> 'Queue':
        """Push item to end of queue."""
        with self._lock:
            if self._max_size is not None and len(self._data) >= self._max_size:
                # Remove oldest item when full (bounded queue behavior)
                self._data.popleft()
            self._data.append(item)
        return self

    def pop(self) -> Any:
        """Pop and return first item from queue (FIFO)."""
        with self._lock:
            if len(self._data) == 0:
                return None
            return self._data.popleft()

    def peek(self) -> Any:
        """View first item without removing."""
        with self._lock:
            return self._data[0] if self._data else None

    def size(self) -> int:
        """Return queue size."""
        with self._lock:
            return len(self._data)

    def isEmpty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._data) == 0

    def isFull(self) -> bool:
        """Check if queue is full (only for bounded queues)."""
        if self._max_size is None:
            return False
        with self._lock:
            return len(self._data) >= self._max_size

    def clear(self) -> 'Queue':
        """Clear all items from queue."""
        with self._lock:
            self._data.clear()
        return self

    def toList(self) -> list:
        """Convert queue to list."""
        with self._lock:
            return list(self._data)

    def content(self) -> list:
        """Return all content as list (alias for toList)."""
        return self.toList()

    def contains(self, item: Any) -> bool:
        """Check if queue contains item."""
        with self._lock:
            return item in self._data

    def at(self, index: int) -> Any:
        """Get item at index (safe access)."""
        with self._lock:
            if 0 <= index < len(self._data):
                return self._data[index]
            return None

    # Thread control methods
    def run(self, process_func: Callable = None) -> 'Queue':
        """Start auto-processing thread.

        Args:
            process_func: Function to call for each item.
        """
        if self._running:
            return self

        self._process_func = process_func
        self._running = True
        self._stop_event.clear()

        def _process_loop():
            while not self._stop_event.is_set():
                item = None
                with self._lock:
                    if len(self._data) > 0:
                        item = self._data.popleft()

                if item is not None:
                    # Process the item
                    if self._process_func:
                        try:
                            self._process_func(item)
                        except Exception as e:
                            pass  # TODO: Log error in v4.7.1

                    # Call triggers
                    for trigger in self._triggers:
                        try:
                            trigger(item)
                        except Exception:
                            pass
                else:
                    # No item, wait a bit
                    self._stop_event.wait(0.01)

        self._thread = threading.Thread(target=_process_loop, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> 'Queue':
        """Stop auto-processing thread."""
        if not self._running:
            return self

        self._running = False
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None

        return self

    def running(self) -> bool:
        """Check if processing thread is running."""
        return self._running

    def add_trigger(self, trigger: Callable) -> None:
        """Add a trigger callback to be called for each processed item."""
        self._triggers.append(trigger)

    def __len__(self) -> int:
        """Return queue length."""
        return self.size()

    def __iter__(self):
        """Iterate over queue items (creates a snapshot)."""
        with self._lock:
            return iter(list(self._data))

    def __repr__(self) -> str:
        with self._lock:
            return f"Queue<{self._element_type}, {self._max_size or 'dynamic'}>({len(self._data)} items)"

    # === C++ STL Additional Methods (v4.7.1) ===

    def back(self) -> Any:
        """Get last element (newest)."""
        with self._lock:
            if not self._data:
                return None
            return self._data[-1]

    def front(self) -> Any:
        """Get first element (oldest) - alias for peek."""
        return self.peek()

    def emplace(self, *args) -> 'Queue':
        """In-place push."""
        return self.push(args[0] if args else None)

    def swap(self, other: 'Queue') -> 'Queue':
        """Swap contents."""
        with self._lock:
            with other._lock:
                self._data, other._data = other._data, self._data
        return self

    def extend(self, items) -> 'Queue':
        """Push multiple items."""
        with self._lock:
            for item in items:
                if self._max_size is not None and len(self._data) >= self._max_size:
                    self._data.popleft()
                self._data.append(item)
        return self

    def drain(self) -> list:
        """Pop all items, return list."""
        with self._lock:
            result = list(self._data)
            self._data.clear()
            return result

    def peek_all(self) -> list:
        """View all items without removing."""
        return self.toList()

    def rotate(self) -> 'Queue':
        """Move front to back."""
        with self._lock:
            if self._data:
                self._data.append(self._data.popleft())
        return self

    def capacity(self) -> int:
        """Get max capacity (-1 for dynamic)."""
        return self._max_size if self._max_size else -1

    def remaining(self) -> int:
        """Get remaining capacity (-1 for dynamic)."""
        if not self._max_size:
            return -1
        with self._lock:
            return self._max_size - len(self._data)

    def length(self) -> int:
        """Return queue length (alias for size)."""
        return self.size()

    def copy(self) -> 'Queue':
        """Return shallow copy."""
        with self._lock:
            new_queue = Queue(self._element_type, self._max_size or 'dynamic')
            new_queue._data = deque(self._data, maxlen=self._max_size)
            return new_queue

    # v4.9.2: New methods
    def methods(self) -> 'DataStruct':
        """Return a DataStruct containing all method names."""
        method_names = [m for m in dir(self) if not m.startswith('_') and callable(getattr(self, m))]
        ds = DataStruct('string')
        ds.extend(method_names)
        return ds


def create_queue(element_type: str = 'dynamic', size: Union[int, str] = 'dynamic') -> Queue:
    """Create a Queue object."""
    return Queue(element_type, size)


class ByteArrayed:
    """Function-to-byte mapping with pattern matching (v4.2.5).

    Maps function references to byte positions and executes pattern matching
    based on function return values.

    Usage:
        bytearrayed MyBytes {
            &func1;              // Position 0x0
            &func2;              // Position 0x1
            case {0, 1} {        // Match when func1=0, func2=1
                printl("Match!");
            }
            default {
                printl("No match");
            }
        }

        MyBytes();           // Execute pattern matching
        x = MyBytes["0x0"];  // Get value at position 0
        x = MyBytes[0];      // Get value at position 0
    """

    def __init__(self, name: str, func_refs: List[Dict], cases: List[Dict],
                 default_block: Any = None, runtime: Any = None):
        self.name = name
        self.func_refs = func_refs  # [{position, hex_pos, func_ref}, ...]
        self.cases = cases          # [{pattern, body}, ...]
        self.default_block = default_block
        self._runtime = runtime
        self._cached_values: Dict[int, Any] = {}  # Cached return values

    def __call__(self, *args, **kwargs) -> Any:
        """Execute pattern matching - probe functions and match cases.

        Functions are executed "invisibly" (side-effect free where possible)
        to get their current return values, then patterns are matched.
        """
        # Get current return values from all referenced functions
        values = self._probe_functions()

        # Try to match each case pattern
        for case in self.cases:
            pattern = case['pattern']
            body = case['body']
            if self._match_pattern(pattern, values):
                return self._execute_body(body)

        # No case matched - execute default if present
        if self.default_block:
            return self._execute_body(self.default_block)

        return None

    def _probe_functions(self, simulate: bool = True) -> List[Any]:
        """Probe referenced functions to get their return values.

        v4.3.2: When simulate=True, analyzes function return statements without
        full execution. This is more precise for pattern matching.

        Args:
            simulate: If True, analyze return values without executing.
                     If False, execute functions to get actual return values.
        """
        values = []
        for ref in self.func_refs:
            func_name = ref['func_ref']
            position = ref['position']
            func_args = ref.get('args', [])  # v4.3.2: Support function arguments

            # Look up the function in runtime scope
            func = None
            if self._runtime:
                func = self._runtime.scope.get(func_name)
                if func is None:
                    func = self._runtime.global_scope.get(func_name)
                if func is None:
                    func = self._runtime.builtins.get_function(func_name)

            result = None

            if func is not None:
                try:
                    # v4.3.2: Evaluate arguments if present
                    evaluated_args = []
                    for arg in func_args:
                        if hasattr(arg, 'type'):
                            evaluated_args.append(self._runtime._evaluate(arg))
                        else:
                            evaluated_args.append(arg)

                    if simulate and hasattr(func, 'type') and func.type == 'function':
                        # v4.3.2: Simulate - analyze return statements without full execution
                        result = self._simulate_function_return(func, evaluated_args)
                    elif callable(func):
                        result = func(*evaluated_args) if evaluated_args else func()
                    elif hasattr(func, 'type') and func.type == 'function':
                        # CSSL function node - execute with args
                        result = self._runtime._call_function(func, evaluated_args)
                    else:
                        result = func
                except Exception:
                    result = None

            values.append(result)
            self._cached_values[position] = result

        return values

    def _simulate_function_return(self, func_node, args: List[Any] = None) -> Any:
        """Simulate a function and extract its return value without full execution.

        v4.3.2: Analyzes the function's return statements and evaluates them
        in isolation to get precise return values for pattern matching.
        """
        if not self._runtime or not func_node:
            return None

        # Create a temporary scope with function parameters bound to args
        func_info = func_node.value
        params = func_info.get('params', [])
        args = args or []

        # Bind parameters to arguments in a temporary scope
        old_scope = self._runtime.scope
        # v4.3.2: Create child scope manually (Scope is a dataclass)
        from includecpp.core.cssl.cssl_runtime import Scope
        self._runtime.scope = Scope(variables={}, parent=old_scope)

        try:
            # Bind parameters
            for i, param in enumerate(params):
                if isinstance(param, dict):
                    param_name = param.get('name')
                    default_value = param.get('default')
                    if i < len(args):
                        self._runtime.scope.set(param_name, args[i])
                    elif default_value is not None:
                        val = self._runtime._evaluate(default_value) if hasattr(default_value, 'type') else default_value
                        self._runtime.scope.set(param_name, val)
                else:
                    if i < len(args):
                        self._runtime.scope.set(param, args[i])

            # Find and evaluate the first return statement
            for child in func_node.children:
                ret_val = self._extract_return_value(child)
                if ret_val is not None:
                    return ret_val

            return None
        finally:
            # Restore original scope
            self._runtime.scope = old_scope

    def _extract_return_value(self, node) -> Any:
        """Extract return value from a node, handling conditionals and blocks.

        v4.3.2: Properly evaluates if/else conditions to find the correct return path.
        """
        if not hasattr(node, 'type'):
            return None

        if node.type == 'return':
            # Found a return - evaluate it
            if node.value is None:
                return None
            if isinstance(node.value, dict) and node.value.get('multiple'):
                # Multiple return values (shuffled)
                return tuple(
                    self._runtime._evaluate(v) for v in node.value.get('values', [])
                )
            return self._runtime._evaluate(node.value)

        # v4.3.2: Handle if statements by evaluating condition
        if node.type == 'if':
            condition = node.value.get('condition')
            if condition:
                # Evaluate the condition
                cond_result = self._runtime._evaluate(condition)
                if cond_result:
                    # Condition is true - check children (then block)
                    if node.children:
                        for child in node.children:
                            ret_val = self._extract_return_value(child)
                            if ret_val is not None:
                                return ret_val
                else:
                    # Condition is false - check else_block if present
                    else_block = node.value.get('else_block')
                    if else_block:
                        for child in else_block:
                            ret_val = self._extract_return_value(child)
                            if ret_val is not None:
                                return ret_val
            return None

        # Check children for returns
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                ret_val = self._extract_return_value(child)
                if ret_val is not None:
                    return ret_val

        return None

    def _match_pattern(self, pattern: List[Dict], values: List[Any]) -> bool:
        """Check if pattern matches the current values."""
        for i, p in enumerate(pattern):
            if i >= len(values):
                return False

            p_type = p.get('type')
            value = values[i]

            if p_type == 'wildcard':
                # _ matches anything
                continue
            elif p_type == 'value':
                # Exact value match
                if value != p.get('value'):
                    return False
            elif p_type == 'indexed':
                # Match at specific index
                idx = p.get('index')
                if isinstance(idx, str) and idx.startswith('0x'):
                    idx = int(idx, 16)
                if idx < len(values):
                    if values[idx] != self._runtime._evaluate(p.get('value')) if hasattr(p.get('value'), 'type') else p.get('value'):
                        return False
            elif p_type == 'type_match':
                # Match by type
                type_name = p.get('type_name')
                if not self._check_type(value, type_name):
                    return False
            elif p_type == 'variable':
                # Match against variable value
                var_name = p.get('name')
                var_value = self._runtime.scope.get(var_name)
                if var_value is None:
                    var_value = self._runtime.global_scope.get(var_name)
                if value != var_value:
                    return False
            elif p_type == 'list':
                # v4.3.2: Match against list value: ["read", "write"]
                pattern_list = p.get('values', [])
                if not isinstance(value, (list, tuple)):
                    return False
                if len(value) != len(pattern_list):
                    return False
                for j, pval in enumerate(pattern_list):
                    if value[j] != pval:
                        return False

        return True

    def _check_type(self, value: Any, type_name: str) -> bool:
        """Check if value matches the specified type."""
        type_checks = {
            'int': lambda v: isinstance(v, int) and not isinstance(v, bool),
            'float': lambda v: isinstance(v, float),
            'string': lambda v: isinstance(v, str),
            'bool': lambda v: isinstance(v, bool),
            'list': lambda v: isinstance(v, list),
            'dict': lambda v: isinstance(v, dict),
            'dynamic': lambda v: True,
        }
        if type_name in type_checks:
            return type_checks[type_name](value)
        # Check for generic types like vector<string>
        if '<' in type_name:
            base = type_name.split('<')[0]
            return isinstance(value, (list, tuple, set))
        return True

    def _execute_body(self, body: List) -> Any:
        """Execute a case body block."""
        if not self._runtime:
            return None
        result = None
        try:
            for node in body:
                result = self._runtime._execute_node(node)
        except Exception as e:
            # v4.3.2: Catch CSSLReturn exception by name to handle return statements
            if type(e).__name__ == 'CSSLReturn':
                return e.value
            raise
        return result

    def __getitem__(self, key: Union[int, str]) -> Any:
        """Access byte value by index or hex position.

        MyBytes[0]      - Get value at position 0
        MyBytes["0x0"]  - Get value at position 0
        """
        if isinstance(key, str):
            if key.startswith('0x') or key.startswith('0X'):
                key = int(key, 16)
            elif key.isdigit():
                key = int(key)
            else:
                raise KeyError(f"Invalid bytearrayed key: {key}")

        if key in self._cached_values:
            return self._cached_values[key]

        # Probe functions to get values if not cached
        if not self._cached_values:
            self._probe_functions()

        return self._cached_values.get(key)

    def __len__(self) -> int:
        """Return number of byte positions."""
        return len(self.func_refs)

    def __repr__(self) -> str:
        return f"ByteArrayed({self.name}, positions={len(self.func_refs)})"


class CSSLClass:
    """Represents a CSSL class definition.

    Stores class name, member variables, methods, and constructor.
    Used by the runtime to instantiate CSSLInstance objects.
    Supports inheritance via the 'parent' attribute.
    """

    def __init__(self, name: str, members: Dict[str, Any] = None,
                 methods: Dict[str, Any] = None, constructor: Any = None,
                 parent: Any = None):
        self.name = name
        self.members = members or {}  # Default member values/types
        self.methods = methods or {}  # Method AST nodes
        self.constructor = constructor  # Constructor AST node
        self.parent = parent  # Parent class (CSSLClass or CSSLizedPythonObject)

    def get_all_members(self) -> Dict[str, Any]:
        """Get all members including inherited ones."""
        all_members = {}
        # First add parent members (can be overridden)
        if self.parent:
            if hasattr(self.parent, 'get_all_members'):
                all_members.update(self.parent.get_all_members())
            elif hasattr(self.parent, 'members'):
                all_members.update(self.parent.members)
            elif hasattr(self.parent, '_python_obj'):
                # CSSLizedPythonObject - get attributes from Python object
                py_obj = self.parent._python_obj
                if hasattr(py_obj, '__dict__'):
                    for key, val in py_obj.__dict__.items():
                        if not key.startswith('_'):
                            all_members[key] = {'type': 'dynamic', 'default': val}
        # Then add own members (override parent)
        all_members.update(self.members)
        return all_members

    def get_all_methods(self) -> Dict[str, Any]:
        """Get all methods including inherited ones."""
        all_methods = {}
        # First add parent methods (can be overridden)
        if self.parent:
            if hasattr(self.parent, 'get_all_methods'):
                all_methods.update(self.parent.get_all_methods())
            elif hasattr(self.parent, 'methods'):
                all_methods.update(self.parent.methods)
            elif hasattr(self.parent, '_python_obj'):
                # CSSLizedPythonObject - get methods from Python object
                py_obj = self.parent._python_obj
                for name in dir(py_obj):
                    if not name.startswith('_'):
                        attr = getattr(py_obj, name, None)
                        if callable(attr):
                            all_methods[name] = ('python_method', attr)
        # Then add own methods (override parent)
        all_methods.update(self.methods)
        return all_methods

    def __repr__(self):
        parent_info = f" extends {self.parent.name}" if self.parent and hasattr(self.parent, 'name') else ""
        return f"<CSSLClass '{self.name}'{parent_info} with {len(self.methods)} methods>"


class CSSLInstance:
    """Represents an instance of a CSSL class.

    Holds instance member values and provides access to class methods.
    Supports this-> member access pattern.
    """

    def __init__(self, class_def: CSSLClass):
        self._class = class_def
        self._members: Dict[str, Any] = {}
        # Initialize members with defaults from class definition (including inherited)
        all_members = class_def.get_all_members() if hasattr(class_def, 'get_all_members') else class_def.members
        for name, default in all_members.items():
            if isinstance(default, dict):
                # Type declaration with optional default
                member_type = default.get('type')
                member_default = default.get('default')

                if member_default is not None:
                    self._members[name] = member_default
                elif member_type:
                    # Create instance of container types
                    self._members[name] = self._create_default_for_type(member_type)
                else:
                    self._members[name] = None
            else:
                self._members[name] = default

    def _create_default_for_type(self, type_name: str) -> Any:
        """Create a default value for a given type name."""
        # Container types
        if type_name == 'map':
            return Map()
        elif type_name in ('stack',):
            return Stack()
        elif type_name in ('vector',):
            return Vector()
        elif type_name in ('array',):
            return Array()
        elif type_name in ('list',):
            return List()
        elif type_name in ('dictionary', 'dict'):
            return Dictionary()
        elif type_name == 'datastruct':
            return DataStruct()
        elif type_name == 'dataspace':
            return DataSpace()
        elif type_name == 'shuffled':
            return Shuffled()
        elif type_name == 'iterator':
            return Iterator()
        elif type_name == 'combo':
            return Combo()
        # Primitive types
        elif type_name == 'int':
            return 0
        elif type_name == 'float':
            return 0.0
        elif type_name == 'string':
            return ""
        elif type_name == 'bool':
            return False
        elif type_name == 'json':
            return {}
        return None

    def get_member(self, name: str) -> Any:
        """Get member value by name"""
        if name in self._members:
            return self._members[name]
        raise AttributeError(f"'{self._class.name}' has no member '{name}'")

    def set_member(self, name: str, value: Any) -> None:
        """Set member value by name"""
        self._members[name] = value

    def has_member(self, name: str) -> bool:
        """Check if member exists"""
        return name in self._members

    def get_method(self, name: str) -> Any:
        """Get method AST node by name (including inherited methods)"""
        # Use get_all_methods to include inherited methods
        all_methods = self._class.get_all_methods() if hasattr(self._class, 'get_all_methods') else self._class.methods
        if name in all_methods:
            return all_methods[name]
        raise AttributeError(f"'{self._class.name}' has no method '{name}'")

    def has_method(self, name: str) -> bool:
        """Check if method exists (including inherited methods)"""
        all_methods = self._class.get_all_methods() if hasattr(self._class, 'get_all_methods') else self._class.methods
        return name in all_methods

    def __getattr__(self, name: str) -> Any:
        """Allow direct attribute access for members and methods"""
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._members:
            return self._members[name]
        # Also check methods so CSSL instances work from Python without pythonize
        if self.has_method(name):
            method_node = self.get_method(name)
            if isinstance(method_node, tuple) and method_node[0] == 'python_method':
                python_method = method_node[1]
                return lambda *args, **kwargs: python_method(*args, **kwargs)
            # Need runtime to call CSSL methods - check if available
            runtime = getattr(self, '_runtime_ref', None)
            if runtime is not None:
                return lambda *args, **kwargs: runtime._call_method(self, method_node, list(args), kwargs)
            # Fallback: return method node info so caller knows it exists
            return method_node
        raise AttributeError(f"'{self._class.name}' has no member '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow direct attribute setting for members"""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            if hasattr(self, '_members'):
                self._members[name] = value
            else:
                object.__setattr__(self, name, value)

    def __repr__(self):
        return f"<{self._class.name} instance at 0x{id(self):x}>"

    def __str__(self):
        return f"<{self._class.name} instance at 0x{id(self):x}>"


class UniversalInstance:
    """Universal shared container accessible from CSSL, Python, and C++.

    Created via instance<"name"> syntax in CSSL or getInstance("name") in Python.
    Supports dynamic member/method injection via +<<== operator.

    Example CSSL:
        instance<"myContainer"> container;
        container +<<== { void sayHello() { printl("Hello!"); } }
        container.sayHello();

    Example Python:
        container = cssl.getInstance("myContainer")
        container.sayHello()
    """

    # Global registry for all universal instances
    _registry: Dict[str, 'UniversalInstance'] = {}

    def __init__(self, name: str):
        self._name = name
        self._members: Dict[str, Any] = {}
        self._methods: Dict[str, Any] = {}  # Method name -> AST node or callable
        self._injections: List[Any] = []  # Code blocks injected via +<<==
        self._runtime = None  # Weak reference to CSSL runtime for method calls
        # Register globally
        UniversalInstance._registry[name] = self

    @classmethod
    def get_or_create(cls, name: str) -> 'UniversalInstance':
        """Get existing instance or create new one."""
        if name in cls._registry:
            return cls._registry[name]
        return cls(name)

    @classmethod
    def get(cls, name: str) -> Optional['UniversalInstance']:
        """Get existing instance by name, returns None if not found."""
        return cls._registry.get(name)

    @classmethod
    def exists(cls, name: str) -> bool:
        """Check if instance exists."""
        return name in cls._registry

    @classmethod
    def delete(cls, name: str) -> bool:
        """Delete instance from registry."""
        if name in cls._registry:
            del cls._registry[name]
            return True
        return False

    @classmethod
    def clear_all(cls) -> int:
        """Clear all instances. Returns count of cleared instances."""
        count = len(cls._registry)
        cls._registry.clear()
        return count

    @classmethod
    def list_all(cls) -> List[str]:
        """List all instance names."""
        return list(cls._registry.keys())

    @property
    def name(self) -> str:
        """Get instance name."""
        return self._name

    def set_member(self, name: str, value: Any) -> None:
        """Set a member value."""
        self._members[name] = value

    def get_member(self, name: str) -> Any:
        """Get a member value."""
        if name in self._members:
            return self._members[name]
        raise AttributeError(f"Instance '{self._name}' has no member '{name}'")

    def has_member(self, name: str) -> bool:
        """Check if member exists."""
        return name in self._members

    def set_runtime(self, runtime: Any) -> None:
        """Set the runtime reference for method calls from Python."""
        import weakref
        self._runtime = weakref.ref(runtime)

    def set_method(self, name: str, method: Any, runtime: Any = None) -> None:
        """Set a method (AST node or callable)."""
        self._methods[name] = method
        if runtime is not None and self._runtime is None:
            self.set_runtime(runtime)

    def get_method(self, name: str) -> Any:
        """Get a method by name."""
        if name in self._methods:
            return self._methods[name]
        raise AttributeError(f"Instance '{self._name}' has no method '{name}'")

    def has_method(self, name: str) -> bool:
        """Check if method exists."""
        return name in self._methods

    def add_injection(self, code_block: Any) -> None:
        """Add a code injection (from +<<== operator)."""
        self._injections.append(code_block)

    def get_injections(self) -> List[Any]:
        """Get all injected code blocks."""
        return self._injections

    def get_all_members(self) -> Dict[str, Any]:
        """Get all members."""
        return dict(self._members)

    def get_all_methods(self) -> Dict[str, Any]:
        """Get all methods."""
        return dict(self._methods)

    def __getattr__(self, name: str) -> Any:
        """Allow direct attribute access for members and methods."""
        if name.startswith('_'):
            raise AttributeError(name)
        if name in object.__getattribute__(self, '_members'):
            return object.__getattribute__(self, '_members')[name]
        if name in object.__getattribute__(self, '_methods'):
            method = object.__getattribute__(self, '_methods')[name]
            runtime_ref = object.__getattribute__(self, '_runtime')

            # If method is an AST node and we have a runtime, create a callable wrapper
            if hasattr(method, 'type') and method.type == 'function' and runtime_ref is not None:
                runtime = runtime_ref()  # Dereference weakref
                if runtime is not None:
                    instance = self
                    def method_caller(*args, **kwargs):
                        # Set 'this' context and call the method
                        old_this = runtime.scope.get('this')
                        runtime.scope.set('this', instance)
                        try:
                            return runtime._call_function(method, list(args))
                        finally:
                            if old_this is not None:
                                runtime.scope.set('this', old_this)
                            elif hasattr(runtime.scope, 'remove'):
                                runtime.scope.remove('this')
                    return method_caller
            # Return method directly if already callable or no runtime
            return method
        raise AttributeError(f"Instance '{object.__getattribute__(self, '_name')}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow direct attribute setting for members."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            if hasattr(self, '_members'):
                self._members[name] = value
            else:
                object.__setattr__(self, name, value)

    def __repr__(self):
        members = len(self._members)
        methods = len(self._methods)
        return f"<UniversalInstance '{self._name}' ({members} members, {methods} methods)>"

    def __str__(self):
        return f"<UniversalInstance '{self._name}'>"


# =============================================================================
# C++ I/O Streams & C-Style Types (v4.8.4)
# =============================================================================

class CStruct:
    """C-style struct with named fields.

    Fast, lightweight struct for performance-critical code.
    Unlike Python classes, fields are fixed at creation time.

    Usage:
        struct Point { int x; int y; };
        Point p = {10, 20};
        p.x = 30;
    """

    __slots__ = ('_fields', '_values', '_name', '_frozen')

    def __init__(self, name: str, fields: Dict[str, str] = None, values: Dict[str, Any] = None):
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_fields', fields or {})  # field_name -> type
        object.__setattr__(self, '_values', values or {})
        object.__setattr__(self, '_frozen', False)

    def _freeze(self) -> 'CStruct':
        """Freeze the struct (no new fields can be added)."""
        object.__setattr__(self, '_frozen', True)
        return self

    def _set_field(self, name: str, field_type: str, value: Any = None) -> None:
        """Define a field (during struct definition)."""
        if self._frozen:
            raise TypeError(f"Cannot add field to frozen struct '{self._name}'")
        self._fields[name] = field_type
        # Set default value based on type
        if value is not None:
            self._values[name] = value
        elif field_type == 'int':
            self._values[name] = 0
        elif field_type == 'float' or field_type == 'double':
            self._values[name] = 0.0
        elif field_type == 'bool':
            self._values[name] = False
        elif field_type == 'string' or field_type == 'str':
            self._values[name] = ""
        else:
            self._values[name] = None

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        values = object.__getattribute__(self, '_values')
        if name in values:
            return values[name]
        raise AttributeError(f"Struct '{object.__getattribute__(self, '_name')}' has no field '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        values = object.__getattribute__(self, '_values')
        fields = object.__getattribute__(self, '_fields')
        if name in fields:
            values[name] = value
        else:
            raise AttributeError(f"Struct '{object.__getattribute__(self, '_name')}' has no field '{name}'")

    def to_dict(self) -> Dict[str, Any]:
        """Convert struct to dictionary."""
        return dict(self._values)

    @classmethod
    def from_dict(cls, name: str, fields: Dict[str, str], data: Dict[str, Any]) -> 'CStruct':
        """Create struct from dictionary."""
        s = cls(name, fields)
        for k, v in data.items():
            if k in fields:
                s._values[k] = v
        return s._freeze()

    def sizeof(self) -> int:
        """Return estimated memory size (like C sizeof)."""
        size = 0
        for name, ftype in self._fields.items():
            if ftype in ('int', 'bool'):
                size += 4
            elif ftype in ('float',):
                size += 4
            elif ftype in ('double', 'long'):
                size += 8
            elif ftype in ('char',):
                size += 1
            elif ftype in ('string', 'str'):
                size += len(str(self._values.get(name, ''))) + 24  # Python string overhead
            else:
                size += 8  # pointer size
        return size

    def copy(self) -> 'CStruct':
        """Return a copy of the struct."""
        return CStruct(self._name, dict(self._fields), dict(self._values))._freeze()

    def __repr__(self):
        vals = ', '.join(f"{k}={v!r}" for k, v in self._values.items())
        return f"{self._name}{{{vals}}}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, CStruct):
            return self._values == other._values
        if isinstance(other, dict):
            return self._values == other
        return False

    def __hash__(self):
        return hash((self._name, tuple(sorted(self._values.items()))))


class OutputStream:
    """C++ style output stream (cout, cerr, clog).

    Supports << operator for chained output.

    Usage:
        cout << "Hello" << " " << "World" << endl;
        cerr << "Error: " << errMsg << endl;
    """

    def __init__(self, stream_type: str = 'stdout', target=None):
        self._type = stream_type
        self._buffer = []
        self._target = target  # Custom target (file, string, etc.)
        self._auto_flush = stream_type == 'cerr'
        self._precision = 6
        self._width = 0
        self._fill = ' '
        self._flags = set()  # 'fixed', 'scientific', 'hex', 'oct', 'showpoint', etc.

    def _get_target(self):
        """Get the actual output target."""
        import sys
        if self._target is not None:
            return self._target
        if self._type == 'stdout' or self._type == 'cout':
            return sys.stdout
        elif self._type == 'stderr' or self._type == 'cerr':
            return sys.stderr
        elif self._type == 'clog':
            return sys.stderr
        return sys.stdout

    def write(self, data: Any) -> 'OutputStream':
        """Write data to stream (<<)."""
        if data == 'endl' or data == '\n':
            self._buffer.append('\n')
            self.flush()
        elif data == 'flush':
            self.flush()
        elif data == 'ends':
            self._buffer.append('\0')
        else:
            formatted = self._format_value(data)
            self._buffer.append(formatted)
            if self._auto_flush:
                self.flush()
        return self

    def _format_value(self, value: Any) -> str:
        """Format value according to stream settings."""
        if isinstance(value, float):
            if 'fixed' in self._flags:
                result = f"{value:.{self._precision}f}"
            elif 'scientific' in self._flags:
                result = f"{value:.{self._precision}e}"
            else:
                result = str(value)
        elif isinstance(value, int) and not isinstance(value, bool):
            if 'hex' in self._flags:
                result = hex(value)
            elif 'oct' in self._flags:
                result = oct(value)
            else:
                result = str(value)
        else:
            result = str(value)

        # Apply width padding
        if self._width > 0 and len(result) < self._width:
            result = result.rjust(self._width, self._fill)
            self._width = 0  # Reset after use

        return result

    def flush(self) -> 'OutputStream':
        """Flush buffer to target."""
        if self._buffer:
            target = self._get_target()
            output = ''.join(self._buffer)
            target.write(output)
            if hasattr(target, 'flush'):
                target.flush()
            self._buffer.clear()
        return self

    def setprecision(self, n: int) -> 'OutputStream':
        """Set floating point precision."""
        self._precision = n
        return self

    def setw(self, n: int) -> 'OutputStream':
        """Set field width for next output."""
        self._width = n
        return self

    def setfill(self, c: str) -> 'OutputStream':
        """Set fill character."""
        self._fill = c[0] if c else ' '
        return self

    def fixed(self) -> 'OutputStream':
        """Use fixed-point notation."""
        self._flags.discard('scientific')
        self._flags.add('fixed')
        return self

    def scientific(self) -> 'OutputStream':
        """Use scientific notation."""
        self._flags.discard('fixed')
        self._flags.add('scientific')
        return self

    def hex(self) -> 'OutputStream':
        """Use hexadecimal for integers."""
        self._flags.discard('oct')
        self._flags.add('hex')
        return self

    def oct(self) -> 'OutputStream':
        """Use octal for integers."""
        self._flags.discard('hex')
        self._flags.add('oct')
        return self

    def dec(self) -> 'OutputStream':
        """Use decimal for integers (default)."""
        self._flags.discard('hex')
        self._flags.discard('oct')
        return self

    def __lshift__(self, other) -> 'OutputStream':
        """<< operator for stream output."""
        return self.write(other)

    def __repr__(self):
        return f"<OutputStream type='{self._type}'>"


class InputStream:
    """C++ style input stream (cin).

    Supports >> operator for reading input.

    Usage:
        string name;
        cin >> name;
        int age;
        cin >> age;
    """

    def __init__(self, stream_type: str = 'stdin', source=None):
        self._type = stream_type
        self._source = source
        self._buffer = []
        self._eof = False
        self._fail = False
        self._skipws = True  # Skip whitespace by default

    def _get_source(self):
        """Get the actual input source."""
        import sys
        if self._source is not None:
            return self._source
        return sys.stdin

    def read(self, target_type: type = str) -> Any:
        """Read next token from stream (>>)."""
        if self._eof:
            self._fail = True
            return None

        # If buffer is empty, read more input
        if not self._buffer:
            source = self._get_source()
            try:
                line = source.readline()
                if not line:
                    self._eof = True
                    return None
                if self._skipws:
                    self._buffer.extend(line.split())
                else:
                    self._buffer.append(line.rstrip('\n'))
            except Exception:
                self._fail = True
                return None

        if not self._buffer:
            self._eof = True
            return None

        token = self._buffer.pop(0)

        # Convert to target type
        try:
            if target_type == int:
                return int(token)
            elif target_type == float:
                return float(token)
            elif target_type == bool:
                return token.lower() in ('true', '1', 'yes')
            else:
                return str(token)
        except ValueError:
            self._fail = True
            return None

    def getline(self) -> str:
        """Read entire line (like std::getline)."""
        source = self._get_source()
        try:
            line = source.readline()
            if not line:
                self._eof = True
                return ""
            return line.rstrip('\n')
        except Exception:
            self._fail = True
            return ""

    def get(self) -> str:
        """Read single character."""
        source = self._get_source()
        try:
            c = source.read(1)
            if not c:
                self._eof = True
            return c
        except Exception:
            self._fail = True
            return ''

    def peek(self) -> str:
        """Peek at next character without consuming."""
        if self._buffer:
            return self._buffer[0][0] if self._buffer[0] else ''
        # For actual stdin, we can't truly peek
        return ''

    def ignore(self, n: int = 1, delim: str = None) -> 'InputStream':
        """Ignore n characters or until delimiter."""
        source = self._get_source()
        for _ in range(n):
            c = source.read(1)
            if not c or (delim and c == delim):
                break
        return self

    def eof(self) -> bool:
        """Check if end of stream."""
        return self._eof

    def fail(self) -> bool:
        """Check if stream is in fail state."""
        return self._fail

    def good(self) -> bool:
        """Check if stream is good."""
        return not self._eof and not self._fail

    def clear(self) -> 'InputStream':
        """Clear error flags."""
        self._fail = False
        return self

    def noskipws(self) -> 'InputStream':
        """Don't skip whitespace."""
        self._skipws = False
        return self

    def skipws(self) -> 'InputStream':
        """Skip whitespace (default)."""
        self._skipws = True
        return self

    def __rshift__(self, other) -> Any:
        """>> operator for stream input."""
        if callable(other):
            # If a type is passed, read and convert
            return self.read(other)
        # Return the stream for chaining
        return self

    def __bool__(self) -> bool:
        """Allow if(cin) checks."""
        return self.good()

    def __repr__(self):
        return f"<InputStream type='{self._type}' eof={self._eof} fail={self._fail}>"


class FileStream:
    """C++ style file stream (fstream, ifstream, ofstream).

    Fast file I/O with C++ semantics.

    Usage:
        fstream file("data.txt", "r");
        file >> data;
        file << "output" << endl;
        file.close();
    """

    def __init__(self, filename: str = None, mode: str = 'r'):
        self._filename = filename
        self._mode = self._convert_mode(mode)
        self._file = None
        self._eof = False
        self._fail = False
        self._buffer = []
        self._precision = 6

        if filename:
            self.open(filename, mode)

    def _convert_mode(self, mode: str) -> str:
        """Convert C++ mode to Python mode."""
        mode_map = {
            'in': 'r',
            'out': 'w',
            'app': 'a',
            'ate': 'r+',
            'binary': 'rb',
            'in|out': 'r+',
            'out|in': 'w+',
            'r': 'r', 'w': 'w', 'a': 'a',
            'rb': 'rb', 'wb': 'wb', 'ab': 'ab',
            'r+': 'r+', 'w+': 'w+', 'a+': 'a+',
        }
        return mode_map.get(mode, mode)

    def open(self, filename: str, mode: str = 'r') -> 'FileStream':
        """Open file."""
        try:
            self._filename = filename
            self._mode = self._convert_mode(mode)
            self._file = open(filename, self._mode)
            self._eof = False
            self._fail = False
        except Exception as e:
            self._fail = True
            raise IOError(f"Failed to open '{filename}': {e}")
        return self

    def close(self) -> 'FileStream':
        """Close file."""
        if self._file:
            self._file.close()
            self._file = None
        return self

    def is_open(self) -> bool:
        """Check if file is open."""
        return self._file is not None and not self._file.closed

    def read(self, target_type: type = str) -> Any:
        """Read next token from file (>>)."""
        if not self.is_open() or self._eof:
            self._fail = True
            return None

        # Read tokens separated by whitespace
        if not self._buffer:
            line = self._file.readline()
            if not line:
                self._eof = True
                return None
            self._buffer.extend(line.split())

        if not self._buffer:
            self._eof = True
            return None

        token = self._buffer.pop(0)

        try:
            if target_type == int:
                return int(token)
            elif target_type == float:
                return float(token)
            elif target_type == bool:
                return token.lower() in ('true', '1', 'yes')
            return str(token)
        except ValueError:
            self._fail = True
            return None

    def write(self, data: Any) -> 'FileStream':
        """Write data to file (<<)."""
        if not self.is_open():
            self._fail = True
            return self

        if data == 'endl' or data == '\n':
            self._file.write('\n')
            self._file.flush()
        elif data == 'flush':
            self._file.flush()
        else:
            if isinstance(data, float):
                self._file.write(f"{data:.{self._precision}f}")
            else:
                self._file.write(str(data))
        return self

    def getline(self) -> str:
        """Read entire line."""
        if not self.is_open():
            return ""
        line = self._file.readline()
        if not line:
            self._eof = True
            return ""
        return line.rstrip('\n')

    def readlines(self) -> List[str]:
        """Read all lines."""
        if not self.is_open():
            return []
        return [line.rstrip('\n') for line in self._file.readlines()]

    def readall(self) -> str:
        """Read entire file."""
        if not self.is_open():
            return ""
        return self._file.read()

    def seekg(self, pos: int, whence: int = 0) -> 'FileStream':
        """Seek get position."""
        if self.is_open():
            self._file.seek(pos, whence)
            self._eof = False
        return self

    def seekp(self, pos: int, whence: int = 0) -> 'FileStream':
        """Seek put position (same as seekg for Python)."""
        return self.seekg(pos, whence)

    def tellg(self) -> int:
        """Tell get position."""
        if self.is_open():
            return self._file.tell()
        return -1

    def tellp(self) -> int:
        """Tell put position."""
        return self.tellg()

    def eof(self) -> bool:
        """Check end of file."""
        return self._eof

    def fail(self) -> bool:
        """Check fail state."""
        return self._fail

    def good(self) -> bool:
        """Check if stream is good."""
        return self.is_open() and not self._eof and not self._fail

    def setprecision(self, n: int) -> 'FileStream':
        """Set float precision."""
        self._precision = n
        return self

    def flush(self) -> 'FileStream':
        """Flush file buffer."""
        if self.is_open():
            self._file.flush()
        return self

    def __lshift__(self, other) -> 'FileStream':
        """<< operator."""
        return self.write(other)

    def __rshift__(self, other) -> Any:
        """>> operator."""
        if callable(other):
            return self.read(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __bool__(self) -> bool:
        return self.good()

    def __repr__(self):
        return f"<FileStream '{self._filename}' mode='{self._mode}' open={self.is_open()}>"


class Pipe:
    """Unix-style pipe for data transformation.

    Supports | operator for chaining transformations.

    Usage:
        data | filter(x => x > 0) | map(x => x * 2) | collect();
    """

    def __init__(self, data: Any = None):
        self._data = data
        self._transforms = []

    def __or__(self, other) -> 'Pipe':
        """| operator - pipe data through transformation."""
        if callable(other):
            # Apply transformation
            result = other(self._data)
            return Pipe(result)
        elif isinstance(other, Pipe):
            # Chain pipes
            for transform in other._transforms:
                self._transforms.append(transform)
            return self
        else:
            # Treat as data to pipe into
            return Pipe(other)

    def __ror__(self, other) -> 'Pipe':
        """Reverse | for starting a pipe."""
        return Pipe(other)

    def collect(self) -> Any:
        """Collect final result."""
        return self._data

    def to_list(self) -> list:
        """Convert to list."""
        if hasattr(self._data, '__iter__') and not isinstance(self._data, str):
            return list(self._data)
        return [self._data]

    def to_string(self, sep: str = '') -> str:
        """Convert to string."""
        if isinstance(self._data, (list, tuple)):
            return sep.join(str(x) for x in self._data)
        return str(self._data)

    @staticmethod
    def filter(predicate: Callable) -> Callable:
        """Create filter transform."""
        def _filter(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return [x for x in data if predicate(x)]
            return data if predicate(data) else None
        return _filter

    @staticmethod
    def map(func: Callable) -> Callable:
        """Create map transform."""
        def _map(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return [func(x) for x in data]
            return func(data)
        return _map

    @staticmethod
    def reduce(func: Callable, initial: Any = None) -> Callable:
        """Create reduce transform."""
        def _reduce(data):
            from functools import reduce as py_reduce
            if hasattr(data, '__iter__') and not isinstance(data, str):
                if initial is not None:
                    return py_reduce(func, data, initial)
                return py_reduce(func, data)
            return data
        return _reduce

    @staticmethod
    def sort(key: Callable = None, reverse: bool = False) -> Callable:
        """Create sort transform."""
        def _sort(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return sorted(data, key=key, reverse=reverse)
            return data
        return _sort

    @staticmethod
    def take(n: int) -> Callable:
        """Take first n elements."""
        def _take(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return list(data)[:n]
            return data
        return _take

    @staticmethod
    def skip(n: int) -> Callable:
        """Skip first n elements."""
        def _skip(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return list(data)[n:]
            return data
        return _skip

    @staticmethod
    def unique() -> Callable:
        """Remove duplicates."""
        def _unique(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                seen = set()
                result = []
                for x in data:
                    key = x if isinstance(x, (int, str, float, bool)) else id(x)
                    if key not in seen:
                        seen.add(key)
                        result.append(x)
                return result
            return data
        return _unique

    @staticmethod
    def reverse() -> Callable:
        """Reverse order."""
        def _reverse(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return list(reversed(list(data)))
            return data
        return _reverse

    @staticmethod
    def grep(pattern: str) -> Callable:
        """Filter by regex pattern."""
        import re
        compiled = re.compile(pattern)
        def _grep(data):
            if hasattr(data, '__iter__') and not isinstance(data, str):
                return [x for x in data if compiled.search(str(x))]
            return data if compiled.search(str(data)) else None
        return _grep

    @staticmethod
    def tee(callback: Callable) -> Callable:
        """Tap into pipe without modifying data."""
        def _tee(data):
            callback(data)
            return data
        return _tee

    def __repr__(self):
        return f"<Pipe data={type(self._data).__name__}>"


# Global stream instances (C++ style)
def _create_cout() -> OutputStream:
    return OutputStream('stdout')

def _create_cerr() -> OutputStream:
    return OutputStream('stderr')

def _create_clog() -> OutputStream:
    return OutputStream('clog')

def _create_cin() -> InputStream:
    return InputStream('stdin')


# Factory functions for new types
def create_struct(name: str, fields: Dict[str, str] = None) -> CStruct:
    """Create a new C-style struct."""
    return CStruct(name, fields)

def create_fstream(filename: str = None, mode: str = 'r') -> FileStream:
    """Create a file stream."""
    return FileStream(filename, mode)

def create_ifstream(filename: str = None) -> FileStream:
    """Create input file stream."""
    return FileStream(filename, 'r')

def create_ofstream(filename: str = None) -> FileStream:
    """Create output file stream."""
    return FileStream(filename, 'w')

def create_pipe(data: Any = None) -> Pipe:
    """Create a new pipe."""
    return Pipe(data)


# ============================================================================
# v4.9.3: Async/Await/Generator Types
# ============================================================================

class CSSLFuture:
    """CSSL Future - represents an async operation result.

    Usage in CSSL:
        future f = async.run(myAsyncFunc);
        result = await f;
        // or
        result = f.result();
    """

    # States
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

    def __init__(self, func_name: str = None):
        self._state = CSSLFuture.PENDING
        self._result = None
        self._exception = None
        self._func_name = func_name
        self._callbacks: List[Callable] = []
        self._lock = threading.Lock()
        self._event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    @property
    def state(self) -> str:
        return self._state

    def is_pending(self) -> bool:
        return self._state == CSSLFuture.PENDING

    def is_running(self) -> bool:
        return self._state == CSSLFuture.RUNNING

    def is_done(self) -> bool:
        return self._state in (CSSLFuture.COMPLETED, CSSLFuture.CANCELLED, CSSLFuture.FAILED)

    def is_completed(self) -> bool:
        return self._state == CSSLFuture.COMPLETED

    def is_cancelled(self) -> bool:
        return self._state == CSSLFuture.CANCELLED

    def is_failed(self) -> bool:
        return self._state == CSSLFuture.FAILED

    def result(self, timeout: float = None) -> Any:
        """Get the result, blocking if not ready."""
        if not self._event.wait(timeout):
            raise TimeoutError(f"Future '{self._func_name}' timed out")
        if self._exception:
            raise self._exception
        return self._result

    def set_result(self, result: Any):
        """Set the result (called internally)."""
        with self._lock:
            self._result = result
            self._state = CSSLFuture.COMPLETED
            self._event.set()
            for cb in self._callbacks:
                try:
                    cb(self)
                except:
                    pass

    def set_exception(self, exc: Exception):
        """Set an exception (called internally)."""
        with self._lock:
            self._exception = exc
            self._state = CSSLFuture.FAILED
            self._event.set()

    def cancel(self) -> bool:
        """Attempt to cancel the future."""
        with self._lock:
            if self._state in (CSSLFuture.PENDING, CSSLFuture.RUNNING):
                self._state = CSSLFuture.CANCELLED
                self._event.set()
                return True
            return False

    def add_callback(self, callback: Callable):
        """Add a callback to run when done."""
        with self._lock:
            if self.is_done():
                callback(self)
            else:
                self._callbacks.append(callback)

    def then(self, callback: Callable) -> 'CSSLFuture':
        """Chain a callback, return new future for chaining."""
        new_future = CSSLFuture(f"{self._func_name}.then")

        def on_complete(f):
            try:
                result = callback(f.result())
                new_future.set_result(result)
            except Exception as e:
                new_future.set_exception(e)

        self.add_callback(on_complete)
        return new_future

    def __repr__(self):
        return f"<Future '{self._func_name}' state={self._state}>"

    def __str__(self):
        if self.is_completed():
            return str(self._result)
        return f"<Future {self._state}>"


class CSSLGenerator:
    """CSSL Generator - supports yield for lazy iteration.

    Usage in CSSL:
        generator define range(n) {
            for (int i = 0; i < n; i++) {
                yield i;
            }
        }

        foreach (x in range(10)) {
            printl(x);
        }
    """

    def __init__(self, func_name: str, iterator=None):
        self._func_name = func_name
        self._iterator = iterator
        self._cached_values: List[Any] = []
        self._cache_index = 0
        self._exhausted = False
        self._peeked = False
        self._peeked_value = None
        self._started = False  # Track if generator has been started
        self._sent_value = {'value': None}  # Mutable container for sent values

    def _fetch_next(self) -> bool:
        """Fetch the next value from iterator if available. Returns True if value available."""
        if self._exhausted:
            return False
        if self._peeked:
            return True
        if self._iterator is None:
            return self._cache_index < len(self._cached_values)

        try:
            self._peeked_value = next(self._iterator)
            self._peeked = True
            self._started = True
            return True
        except StopIteration:
            self._exhausted = True
            return False

    def send(self, value: Any = None) -> Any:
        """Send a value into the generator.

        The sent value becomes the result of the yield expression in CSSL.
        Example:
            counter = Counter();
            counter.next();      // returns 0
            counter.send(100);   // resumes, sets received=100, returns next value
        """
        if self._peeked:
            # Return peeked value, but store sent value for the yield expression
            result = self._peeked_value
            self._peeked = False
            self._peeked_value = None
            self._sent_value['value'] = value
            return result

        if self._iterator is not None:
            try:
                # Use iterator's send() if available and generator has started
                if hasattr(self._iterator, 'send') and self._started:
                    result = self._iterator.send(value)
                else:
                    result = next(self._iterator)
                    self._started = True
                return result
            except StopIteration:
                self._exhausted = True
                raise

        if self._cache_index < len(self._cached_values):
            result = self._cached_values[self._cache_index]
            self._cache_index += 1
            return result

        self._exhausted = True
        raise StopIteration

    def get_sent_value(self) -> Any:
        """Get the last value sent via send(). Used internally for yield expressions."""
        return self._sent_value['value']

    def __next__(self) -> Any:
        return self.send(None)

    def __iter__(self):
        return self

    def next(self) -> Any:
        """Get next value (CSSL style). Returns None when exhausted."""
        try:
            return self.send(None)
        except StopIteration:
            return None

    def has_next(self) -> bool:
        """Check if more values available."""
        return self._fetch_next()

    def to_list(self) -> list:
        """Consume generator into list."""
        result = []
        for item in self:
            result.append(item)
        return result

    def take(self, n: int) -> list:
        """Take up to n values."""
        result = []
        for _ in range(n):
            try:
                result.append(next(self))
            except StopIteration:
                break
        return result

    def skip(self, n: int) -> 'CSSLGenerator':
        """Skip n values."""
        for _ in range(n):
            try:
                next(self)
            except StopIteration:
                break
        return self

    def map(self, func: Callable) -> 'CSSLGenerator':
        """Map a function over values."""
        new_gen = CSSLGenerator(f"{self._func_name}.map")
        new_gen._iterator = (func(x) for x in self)
        return new_gen

    def filter(self, predicate: Callable) -> 'CSSLGenerator':
        """Filter values by predicate."""
        new_gen = CSSLGenerator(f"{self._func_name}.filter")
        new_gen._iterator = (x for x in self if predicate(x))
        return new_gen

    def __repr__(self):
        return f"<Generator '{self._func_name}' exhausted={self._exhausted}>"


class CSSLAsyncFunction:
    """Wrapper for async-defined functions in CSSL.

    Usage in CSSL:
        async define fetchData(url) {
            result = await http.get(url);
            return result;
        }

        future f = fetchData("http://example.com");  // Returns Future immediately
        data = await f;                               // Wait for result

        // Or use async module:
        future f = async.run(fetchData, "http://example.com");
    """

    def __init__(self, name: str, func_node, runtime=None):
        self._name = name
        self._func_node = func_node
        self._runtime = runtime
        self._is_generator = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_async(self) -> bool:
        return True

    @property
    def is_generator(self) -> bool:
        return self._is_generator

    @property
    def func_node(self):
        """Access to the underlying function AST node."""
        return self._func_node

    def __repr__(self):
        return f"<AsyncFunction '{self._name}'>"

    def __call__(self, *args, **kwargs):
        """Calling an async function starts execution and returns a Future."""
        return AsyncModule.run(self, *args, runtime=self._runtime, **kwargs)

    def start(self, *args, **kwargs) -> 'CSSLFuture':
        """Start the async function and return its Future."""
        return self.__call__(*args, **kwargs)


class AsyncModule:
    """CSSL async module - provides async utilities.

    Usage in CSSL:
        // Run async function
        future f = async.run(myFunc, arg1, arg2);

        // Wait for result
        result = await f;
        // or
        result = async.wait(f);

        // Run multiple and wait for all
        results = async.all([f1, f2, f3]);

        // Run multiple and get first completed
        result = async.race([f1, f2, f3]);

        // Stop async operation
        async.stop(f);

        // Sleep
        async.sleep(1000);  // ms
    """

    _active_futures: Dict[str, CSSLFuture] = {}
    _executor_pool: List[threading.Thread] = []
    _lock = threading.Lock()

    @classmethod
    def run(cls, func, *args, runtime=None, **kwargs) -> CSSLFuture:
        """Run a function asynchronously."""
        if isinstance(func, CSSLAsyncFunction):
            func_name = func.name
        elif callable(func):
            func_name = getattr(func, '__name__', 'anonymous')
        else:
            func_name = str(func)

        future = CSSLFuture(func_name)
        future._state = CSSLFuture.RUNNING

        def execute():
            try:
                if isinstance(func, CSSLAsyncFunction) and runtime:
                    result = runtime._call_function(func._func_node, list(args), kwargs)
                elif callable(func):
                    result = func(*args, **kwargs)
                else:
                    result = func
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                with cls._lock:
                    cls._active_futures.pop(func_name, None)

        thread = threading.Thread(target=execute, daemon=True)
        future._thread = thread

        with cls._lock:
            cls._active_futures[func_name] = future

        thread.start()
        return future

    @classmethod
    def stop(cls, future_or_name) -> bool:
        """Stop an async operation."""
        if isinstance(future_or_name, CSSLFuture):
            return future_or_name.cancel()
        elif isinstance(future_or_name, str):
            with cls._lock:
                future = cls._active_futures.get(future_or_name)
                if future:
                    return future.cancel()
        return False

    @classmethod
    def wait(cls, future, timeout: float = None) -> Any:
        """Wait for a future to complete, or sleep for a duration (seconds).

        If a number is passed instead of a Future, sleeps for that many seconds.
        """
        if isinstance(future, (int, float)):
            # Treat as sleep duration in seconds
            import time
            time.sleep(float(future))
            return future
        return future.result(timeout)

    @classmethod
    def all(cls, futures: List[CSSLFuture], timeout: float = None) -> List[Any]:
        """Wait for all futures to complete."""
        results = []
        for f in futures:
            results.append(f.result(timeout))
        return results

    @classmethod
    def race(cls, futures: List[CSSLFuture], timeout: float = None) -> Any:
        """Return result of first completed future."""
        import time
        start = time.time()
        while True:
            for f in futures:
                if f.is_done():
                    # Cancel others
                    for other in futures:
                        if other != f:
                            other.cancel()
                    return f.result()
            if timeout and (time.time() - start) > timeout:
                raise TimeoutError("async.race() timed out")
            time.sleep(0.001)  # Small sleep to prevent busy waiting

    @classmethod
    def sleep(cls, ms: int) -> CSSLFuture:
        """Async sleep for ms milliseconds."""
        import time
        future = CSSLFuture("sleep")
        future._state = CSSLFuture.RUNNING

        def do_sleep():
            time.sleep(ms / 1000.0)
            future.set_result(None)

        thread = threading.Thread(target=do_sleep, daemon=True)
        thread.start()
        return future

    @classmethod
    def create_generator(cls, func_name: str, values: list = None) -> CSSLGenerator:
        """Create a generator."""
        gen = CSSLGenerator(func_name)
        if values:
            gen._values = list(values)
        return gen

    @classmethod
    def is_future(cls, obj) -> bool:
        """Check if object is a Future."""
        return isinstance(obj, CSSLFuture)

    @classmethod
    def is_generator(cls, obj) -> bool:
        """Check if object is a Generator."""
        return isinstance(obj, CSSLGenerator)


# Factory functions for async types
def create_future(name: str = None) -> CSSLFuture:
    """Create a new Future."""
    return CSSLFuture(name)

def create_generator(name: str, values: list = None) -> CSSLGenerator:
    """Create a new Generator."""
    return AsyncModule.create_generator(name, values)

def create_async_function(name: str, func_node, runtime=None) -> CSSLAsyncFunction:
    """Create an async function wrapper."""
    return CSSLAsyncFunction(name, func_node, runtime)


__all__ = [
    'DataStruct', 'Shuffled', 'Iterator', 'Combo', 'DataSpace', 'OpenQuote',
    'OpenFind', 'Parameter', 'Stack', 'Vector', 'Array', 'List', 'Dictionary', 'Map',
    'Queue',
    'CSSLClass', 'CSSLInstance', 'UniversalInstance',
    # v4.8.4: C++ I/O Streams & C-Style Types
    'CStruct', 'OutputStream', 'InputStream', 'FileStream', 'Pipe',
    # v4.9.3: Async/Await/Generator Types
    'CSSLFuture', 'CSSLGenerator', 'CSSLAsyncFunction', 'AsyncModule',
    # Factory functions
    'create_datastruct', 'create_shuffled', 'create_iterator',
    'create_combo', 'create_dataspace', 'create_openquote', 'create_parameter',
    'create_stack', 'create_vector', 'create_array', 'create_list', 'create_dictionary', 'create_map',
    'create_queue',
    # v4.8.4: New factory functions
    'create_struct', 'create_fstream', 'create_ifstream', 'create_ofstream', 'create_pipe',
    '_create_cout', '_create_cerr', '_create_clog', '_create_cin',
    # v4.9.3: Async factory functions
    'create_future', 'create_generator', 'create_async_function',
]
