# build_decoders.py
"""
Registry builder for Anchor IDL v0.30+ format.

IDL Structure (new format):
    instructions: [{name, discriminator: [u8;8], accounts, args: [{name, type}]}]
    accounts:     [{name, discriminator: [u8;8]}]  # fields in types section
    events:       [{name, discriminator: [u8;8]}]  # fields in types section
    types:        [{name, type: {kind, fields}}]
    errors:       [{code, name, msg}]
"""
import struct
import base58
from typing import Dict, Callable, Any, Optional, Tuple, List, Union

# =============================================================================
# TYPE READERS - Primitives
# =============================================================================

def read_pubkey(buf: bytes, o: int) -> Tuple[str, int]:
    return base58.b58encode(buf[o:o+32]).decode(), o + 32

def read_u8(buf: bytes, o: int) -> Tuple[int, int]:
    return buf[o], o + 1

def read_u16(buf: bytes, o: int) -> Tuple[int, int]:
    return struct.unpack_from("<H", buf, o)[0], o + 2

def read_u32(buf: bytes, o: int) -> Tuple[int, int]:
    return struct.unpack_from("<I", buf, o)[0], o + 4

def read_u64(buf: bytes, o: int) -> Tuple[int, int]:
    return struct.unpack_from("<Q", buf, o)[0], o + 8

def read_u128(buf: bytes, o: int) -> Tuple[int, int]:
    lo = struct.unpack_from("<Q", buf, o)[0]
    hi = struct.unpack_from("<Q", buf, o + 8)[0]
    return (hi << 64) | lo, o + 16

def read_i64(buf: bytes, o: int) -> Tuple[int, int]:
    return struct.unpack_from("<q", buf, o)[0], o + 8

def read_i128(buf: bytes, o: int) -> Tuple[int, int]:
    lo = struct.unpack_from("<Q", buf, o)[0]
    hi = struct.unpack_from("<q", buf, o + 8)[0]
    return (hi << 64) | lo, o + 16

def read_bool(buf: bytes, o: int) -> Tuple[bool, int]:
    return buf[o] != 0, o + 1

def read_string(buf: bytes, o: int) -> Tuple[str, int]:
    ln = struct.unpack_from("<I", buf, o)[0]
    o += 4
    return buf[o:o+ln].decode("utf-8", errors="replace"), o + ln

# Base type readers
PRIMITIVE_READERS: Dict[str, Callable[[bytes, int], Tuple[Any, int]]] = {
    "pubkey": read_pubkey,
    "publicKey": read_pubkey,
    "u8": read_u8,
    "u16": read_u16,
    "u32": read_u32,
    "u64": read_u64,
    "u128": read_u128,
    "i8": read_u8,
    "i16": read_u16,
    "i32": read_u32,
    "i64": read_i64,
    "i128": read_i128,
    "bool": read_bool,
    "string": read_string,
}


# =============================================================================
# TYPE RESOLVER - Handles complex types
# =============================================================================

class TypeResolver:
    """
    Resolves IDL types to reader functions.
    Handles primitives, arrays, vecs, options, and defined types.
    """
    
    def __init__(self, types_map: Dict[str, dict]):
        self.types_map = types_map
        self._cache: Dict[str, Callable] = {}
    
    def get_reader(self, type_spec: Union[str, dict]) -> Callable[[bytes, int], Tuple[Any, int]]:
        """Get a reader function for any type specification."""
        
        # String type = primitive or defined type name
        if isinstance(type_spec, str):
            if type_spec in PRIMITIVE_READERS:
                return PRIMITIVE_READERS[type_spec]
            # Look up in types
            if type_spec in self.types_map:
                return self._build_struct_reader(type_spec)
            raise ValueError(f"Unknown type: {type_spec}")
        
        # Dict type = complex type
        if isinstance(type_spec, dict):
            # {"defined": {"name": "TypeName"}} or {"defined": "TypeName"}
            if "defined" in type_spec:
                defined = type_spec["defined"]
                if isinstance(defined, dict):
                    type_name = defined["name"]
                else:
                    type_name = defined
                return self._build_struct_reader(type_name)
            
            # {"option": "type"} or {"option": {...}}
            if "option" in type_spec:
                inner_reader = self.get_reader(type_spec["option"])
                return self._make_option_reader(inner_reader)
            
            # {"vec": "type"} or {"vec": {...}}
            if "vec" in type_spec:
                inner_reader = self.get_reader(type_spec["vec"])
                return self._make_vec_reader(inner_reader)
            
            # {"array": ["type", size]}
            if "array" in type_spec:
                inner_type, size = type_spec["array"]
                inner_reader = self.get_reader(inner_type)
                return self._make_array_reader(inner_reader, size)
            
            raise ValueError(f"Unknown complex type: {type_spec}")
        
        raise ValueError(f"Invalid type specification: {type_spec}")
    
    def _build_struct_reader(self, type_name: str) -> Callable[[bytes, int], Tuple[Any, int]]:
        """Build a reader for a struct type from types_map."""
        if type_name in self._cache:
            return self._cache[type_name]
        
        type_def = self.types_map.get(type_name)
        if not type_def:
            raise ValueError(f"Type not found: {type_name}")
        
        type_info = type_def.get("type", {})
        kind = type_info.get("kind")
        
        if kind == "struct":
            fields = type_info.get("fields", [])
            # Handle tuple struct like OptionBool: {"fields": ["bool"]}
            if fields and isinstance(fields[0], str):
                # Tuple struct - single unnamed field
                inner_reader = self.get_reader(fields[0])
                def tuple_reader(buf: bytes, o: int) -> Tuple[Any, int]:
                    return inner_reader(buf, o)
                self._cache[type_name] = tuple_reader
                return tuple_reader
            
            # Normal struct with named fields
            field_readers = []
            for f in fields:
                name = f["name"]
                reader = self.get_reader(f["type"])
                field_readers.append((name, reader))
            
            def struct_reader(buf: bytes, o: int, _readers=field_readers) -> Tuple[dict, int]:
                out = {}
                for name, reader in _readers:
                    out[name], o = reader(buf, o)
                return out, o
            
            self._cache[type_name] = struct_reader
            return struct_reader
        
        elif kind == "enum":
            # Read enum as u8 variant index
            variants = type_info.get("variants", [])
            
            def enum_reader(buf: bytes, o: int, _variants=variants) -> Tuple[dict, int]:
                idx = buf[o]
                o += 1
                if idx < len(_variants):
                    variant = _variants[idx]
                    return {"variant": variant.get("name", idx)}, o
                return {"variant": idx}, o
            
            self._cache[type_name] = enum_reader
            return enum_reader
        
        raise ValueError(f"Unsupported type kind: {kind} for {type_name}")
    
    def _make_option_reader(self, inner: Callable) -> Callable[[bytes, int], Tuple[Optional[Any], int]]:
        def option_reader(buf: bytes, o: int) -> Tuple[Optional[Any], int]:
            is_some = buf[o] != 0
            o += 1
            if is_some:
                return inner(buf, o)
            return None, o
        return option_reader
    
    def _make_vec_reader(self, inner: Callable) -> Callable[[bytes, int], Tuple[List[Any], int]]:
        def vec_reader(buf: bytes, o: int) -> Tuple[List[Any], int]:
            length = struct.unpack_from("<I", buf, o)[0]
            o += 4
            items = []
            for _ in range(length):
                item, o = inner(buf, o)
                items.append(item)
            return items, o
        return vec_reader
    
    def _make_array_reader(self, inner: Callable, size: int) -> Callable[[bytes, int], Tuple[List[Any], int]]:
        def array_reader(buf: bytes, o: int, _size=size) -> Tuple[List[Any], int]:
            items = []
            for _ in range(_size):
                item, o = inner(buf, o)
                items.append(item)
            return items, o
        return array_reader


# =============================================================================
# DISCRIMINATOR HANDLING
# =============================================================================

def disc_from_array(arr: List[int]) -> bytes:
    """Convert discriminator array [u8; 8] to bytes."""
    return bytes(arr)


# =============================================================================
# DECODER BUILDERS
# =============================================================================

def build_instruction_decoder(ix_def: dict, resolver: TypeResolver) -> Callable[[bytes], dict]:
    """Build decoder for instruction args."""
    args = ix_def.get("args", [])
    field_readers = []
    for arg in args:
        name = arg["name"]
        reader = resolver.get_reader(arg["type"])
        field_readers.append((name, reader))
    
    def decoder(raw: bytes, _readers=field_readers) -> dict:
        o = 8  # skip discriminator
        out = {}
        for name, reader in _readers:
            out[name], o = reader(raw, o)
        return out
    
    return decoder


def build_type_decoder(type_name: str, resolver: TypeResolver) -> Callable[[bytes], dict]:
    """Build decoder for a type (event/account) from types section."""
    inner = resolver._build_struct_reader(type_name)
    
    def decoder(raw: bytes) -> dict:
        result, _ = inner(raw, 8)  # skip discriminator
        return result
    
    return decoder


# =============================================================================
# REGISTRY
# =============================================================================

class DecoderRegistry:
    """
    Registry mapping discriminator bytes -> (name, category, decoder).
    """
    __slots__ = ('instructions', 'events', 'accounts', 'errors', 'unified', 'resolver')
    
    def __init__(self):
        self.instructions: Dict[bytes, Tuple[str, Callable]] = {}
        self.events: Dict[bytes, Tuple[str, Callable]] = {}
        self.accounts: Dict[bytes, Tuple[str, Callable]] = {}
        self.errors: Dict[int, dict] = {}
        self.unified: Dict[bytes, Tuple[str, str, Callable]] = {}
        self.resolver: Optional[TypeResolver] = None
    
    def register_idl(self, idl: dict) -> None:
        """Register all decoders from an IDL."""
        
        # Build types map
        types_map = {}
        for t in idl.get("types", []):
            types_map[t["name"]] = t
        
        self.resolver = TypeResolver(types_map)
        
        # Instructions
        for ix in idl.get("instructions", []):
            name = ix["name"]
            disc_arr = ix.get("discriminator")
            if not disc_arr:
                continue
            disc = disc_from_array(disc_arr)
            try:
                decoder = build_instruction_decoder(ix, self.resolver)
                self.instructions[disc] = (name, decoder)
                self.unified[disc] = (name, "instruction", decoder)
            except ValueError as e:
                print(f"Skipping instruction {name}: {e}")
        
        # Events
        for event in idl.get("events", []):
            name = event["name"]
            disc_arr = event.get("discriminator")
            if not disc_arr:
                continue
            disc = disc_from_array(disc_arr)
            try:
                decoder = build_type_decoder(name, self.resolver)
                self.events[disc] = (name, decoder)
                self.unified[disc] = (name, "event", decoder)
            except ValueError as e:
                print(f"Skipping event {name}: {e}")
        
        # Accounts
        for acc in idl.get("accounts", []):
            name = acc["name"]
            disc_arr = acc.get("discriminator")
            if not disc_arr:
                continue
            disc = disc_from_array(disc_arr)
            try:
                decoder = build_type_decoder(name, self.resolver)
                self.accounts[disc] = (name, decoder)
                self.unified[disc] = (name, "account", decoder)
            except ValueError as e:
                print(f"Skipping account {name}: {e}")
        
        # Errors
        for err in idl.get("errors", []):
            self.errors[err["code"]] = err
    
    def decode(self, raw: bytes) -> Optional[Tuple[str, str, dict]]:
        """
        Decode using unified registry.
        Returns (name, category, decoded_dict) or None.
        """
        disc = raw[:8]
        if disc in self.unified:
            name, category, decoder = self.unified[disc]
            return name, category, decoder(raw)
        return None
    
    def decode_event(self, raw: bytes) -> Optional[Tuple[str, dict]]:
        """Decode as event. Returns (name, data) or None."""
        disc = raw[:8]
        if disc in self.events:
            name, decoder = self.events[disc]
            return name, decoder(raw)
        return None
    
    def decode_instruction(self, raw: bytes) -> Optional[Tuple[str, dict]]:
        """Decode as instruction. Returns (name, data) or None."""
        disc = raw[:8]
        if disc in self.instructions:
            name, decoder = self.instructions[disc]
            return name, decoder(raw)
        return None
    
    def decode_account(self, raw: bytes) -> Optional[Tuple[str, dict]]:
        """Decode as account. Returns (name, data) or None."""
        disc = raw[:8]
        if disc in self.accounts:
            name, decoder = self.accounts[disc]
            return name, decoder(raw)
        return None
    
    def get_error(self, code: int) -> Optional[dict]:
        """Lookup error by code."""
        return self.errors.get(code)
    
    def list_events(self) -> List[Tuple[str, str]]:
        """List all registered events as (name, disc_hex)."""
        return [(name, disc.hex()) for disc, (name, _) in self.events.items()]
    
    def list_instructions(self) -> List[Tuple[str, str]]:
        """List all registered instructions as (name, disc_hex)."""
        return [(name, disc.hex()) for disc, (name, _) in self.instructions.items()]
    
    def list_accounts(self) -> List[Tuple[str, str]]:
        """List all registered accounts as (name, disc_hex)."""
        return [(name, disc.hex()) for disc, (name, _) in self.accounts.items()]


def build_registry_from_idl(idl: dict) -> DecoderRegistry:
    """Build registry from a single IDL."""
    registry = DecoderRegistry()
    registry.register_idl(idl)
    return registry


def build_registry_from_idls(idls: List[dict]) -> DecoderRegistry:
    """Build registry from multiple IDLs."""
    registry = DecoderRegistry()
    for idl in idls:
        if idl:
            registry.register_idl(idl)
    return registry


# =============================================================================
# UTILITIES
# =============================================================================

def build_discriminator_table(idl: dict) -> Dict[str, str]:
    """Build name -> hex discriminator lookup."""
    table = {}
    
    for ix in idl.get("instructions", []):
        disc = ix.get("discriminator")
        if disc:
            table[f"instruction:{ix['name']}"] = bytes(disc).hex()
    
    for event in idl.get("events", []):
        disc = event.get("discriminator")
        if disc:
            table[f"event:{event['name']}"] = bytes(disc).hex()
    
    for acc in idl.get("accounts", []):
        disc = acc.get("discriminator")
        if disc:
            table[f"account:{acc['name']}"] = bytes(disc).hex()
    
    return table


def print_discriminator_table(idl: dict) -> None:
    """Pretty print discriminator table."""
    table = build_discriminator_table(idl)
    for name, disc in sorted(table.items()):
        print(f"{disc}  {name}")
