# build_decoders.py
"""
Registry builder for Anchor IDL-based decoders.

IDL Structure Reference:
    instructions: [{name, docs, accounts, args: [{name, type}]}]
    accounts:     [{name, type: {kind: "struct", fields: [{name, type}]}}]
    events:       [{name, fields: [{name, type, index}]}]
    errors:       [{code, name, msg}]
"""
import hashlib
import struct
import base58,os
from abstract_utilities import *
from typing import Dict, Callable, Any, Optional, Tuple, List
from .pda import *
@dataclass
class InstructionSchema:
    name: str
    discriminator: bytes
    args: list
    pda_accounts: List[PDAAccountSpec]
# =============================================================================
# TYPE READERS
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

import hashlib,os
from .decoders import TYPE_READERS
from abstract_utilities import *

def read_bool(buf: bytes, o: int) -> Tuple[bool, int]:
    return buf[o] == 1, o + 1

def read_string(buf: bytes, o: int) -> Tuple[str, int]:
    ln = struct.unpack_from("<I", buf, o)[0]
    o += 4
    return buf[o:o+ln].decode("utf-8", errors="replace"), o + ln

def read_optional_pubkey(buf: bytes, o: int) -> Tuple[Optional[str], int]:
    """Read pubkey, return None if all zeros."""
    if buf[o:o+32] == bytes(32):
        return None, o + 32
    return base58.b58encode(buf[o:o+32]).decode(), o + 32
def read_pubkey(raw: bytes, offset: int) -> tuple[str, int]:
    """Read 32-byte pubkey, return (base58_str, new_offset)"""
    pk = base58.b58encode(raw[offset:offset+32]).decode()
    return pk, offset + 32


def read_u64(raw: bytes, offset: int) -> tuple[int, int]:
    val, = struct.unpack_from("<Q", raw, offset)
    return val, offset + 8


def read_i64(raw: bytes, offset: int) -> tuple[int, int]:
    val, = struct.unpack_from("<q", raw, offset)
    return val, offset + 8


def read_bool(raw: bytes, offset: int) -> tuple[bool, int]:
    val, = struct.unpack_from("<?", raw, offset)
    return val, offset + 1


def read_string(raw: bytes, offset: int) -> tuple[str, int]:
    ln, = struct.unpack_from("<I", raw, offset)
    offset += 4
    val = raw[offset:offset+ln].decode("utf-8")
    return val, offset + ln


def is_null_pubkey(raw: bytes, offset: int) -> bool:
    return raw[offset:offset+32] == bytes(32)
# idl_types.py
import struct, base58

def read_string(buf, o):
    ln = struct.unpack_from("<I", buf, o)[0]
    o += 4
    return buf[o:o+ln].decode(), o + ln

def read_pubkey(buf, o):
    return base58.b58encode(buf[o:o+32]).decode(), o + 32

def read_u64(buf, o):
    return struct.unpack_from("<Q", buf, o)[0], o + 8

def read_i64(buf, o):
    return struct.unpack_from("<q", buf, o)[0], o + 8

def read_bool(buf, o):
    return buf[o] == 1, o + 1


TYPE_READERS: Dict[str, Callable[[bytes, int], Tuple[Any, int]]] = {
    "publicKey": read_pubkey,
    "u8": read_u8,
    "u16": read_u16,
    "u32": read_u32,
    "u64": read_u64,
    "i64": read_i64,
    "bool": read_bool,
    "string": read_string,
    "optionalPublicKey": read_optional_pubkey,
}

# =============================================================================
# DISCRIMINATOR FUNCTIONS
# =============================================================================

def instruction_discriminator(name: str) -> bytes:
    """sha256('global:{name}')[:8] for instructions"""
    return hashlib.sha256(f"global:{name}".encode()).digest()[:8]

def event_discriminator(name: str) -> bytes:
    """sha256('event:{name}')[:8] for events"""
    return hashlib.sha256(f"event:{name}".encode()).digest()[:8]

def account_discriminator(name: str) -> bytes:
    """sha256('account:{name}')[:8] for accounts"""
    return hashlib.sha256(f"account:{name}".encode()).digest()[:8]

def error_discriminator(code: int) -> bytes:
    """Error codes are u32 LE"""
    return struct.pack("<I", code)

# =============================================================================
# DECODER BUILDERS
# =============================================================================

def build_instruction_decoder(ix_def: dict) -> Callable[[bytes], dict]:
    """
    Build decoder for instruction args.
    
    IDL: {name, docs, accounts, args: [{name, type}]}
    """
    args = ix_def.get("args", [])
    
    def decoder(raw: bytes) -> dict:
        o = 8  # skip discriminator
        out = {}
        for arg in args:
            type_name = arg["type"]
            if type_name not in TYPE_READERS:
                raise ValueError(f"Unknown type: {type_name}")
            out[arg["name"]], o = TYPE_READERS[type_name](raw, o)
        return out
    
    return decoder


def build_event_decoder(event_def: dict) -> Callable[[bytes], dict]:
    """
    Build decoder for event fields.
    
    IDL: {name, fields: [{name, type, index}]}
    """
    fields = event_def.get("fields", [])
    
    def decoder(raw: bytes) -> dict:
        o = 8  # skip discriminator
        out = {}
        for f in fields:
            type_name = f["type"]
            if type_name not in TYPE_READERS:
                raise ValueError(f"Unknown type: {type_name}")
            out[f["name"]], o = TYPE_READERS[type_name](raw, o)
        return out
    
    return decoder


def build_account_decoder(acc_def: dict) -> Callable[[bytes], dict]:
    """
    Build decoder for account data.
    
    IDL: {name, type: {kind: "struct", fields: [{name, type}]}}
    """
    type_info = acc_def.get("type", {})
    fields = type_info.get("fields", [])
    
    def decoder(raw: bytes) -> dict:
        o = 8  # skip discriminator
        out = {}
        for f in fields:
            type_name = f["type"]
            if type_name not in TYPE_READERS:
                raise ValueError(f"Unknown type: {type_name}")
            out[f["name"]], o = TYPE_READERS[type_name](raw, o)
        return out
    
    return decoder


# =============================================================================
# REGISTRY BUILDER
# =============================================================================
def extract_pda_accounts(ix_def: dict) -> List[PDAAccountSpec]:
    out = []

    for acc in ix_def.get("accounts", []):
        pda = acc.get("pda")
        if not pda:
            continue

        seeds = []
        for s in pda.get("seeds", []):
            seeds.append(PDASeed(
                kind=s.get("kind"),
                type=s.get("type"),
                value=s.get("value"),
                path=s.get("path"),
            ))

        out.append(PDAAccountSpec(
            account_name=acc["name"],
            seeds=seeds
        ))

    return out

class DecoderRegistry:
    """
    Registry mapping discriminator bytes -> decoder function.
    
    Separate registries for each category to avoid collision.
    """
    __slots__ = (
        'instructions',
        'events',
        'accounts',
        'errors',
        'unified',
        'instruction_schemas',   # 👈 NEW
    )

    def __init__(self):
        self.instructions: Dict[bytes, Callable] = {}
        self.events: Dict[bytes, Callable] = {}
        self.accounts: Dict[bytes, Callable] = {}
        self.errors: Dict[bytes, dict] = {}  # errors are just metadata
        self.unified: Dict[bytes, Tuple[str, Callable]] = {}  # (category, decoder)
        self.instruction_schemas: Dict[bytes, InstructionSchema] = {}
    def get_instruction_schema(self, disc: bytes) -> Optional[InstructionSchema]:
        return self.instruction_schemas.get(disc)
    def register_idl(self, idl: dict) -> None:
        """Register all decoders from an IDL."""
        
        # Instructions
        for ix in idl.get("instructions", []):
            disc = instruction_discriminator(ix["name"])
            decoder = build_instruction_decoder(ix)
            self.instructions[disc] = decoder
            self.unified[disc] = ("instruction", decoder)
            # 🔑 NEW: instruction schema
            self.instruction_schemas[disc] = InstructionSchema(
                name=ix["name"],
                discriminator=disc,
                args=ix.get("args", []),
                pda_accounts=extract_pda_accounts(ix),
            )
            
        # Events
        for event in idl.get("events", []):
            disc = event_discriminator(event["name"])
            decoder = build_event_decoder(event)
            self.events[disc] = decoder
            self.unified[disc] = ("event", decoder)
        
        # Accounts
        for acc in idl.get("accounts", []):
            disc = account_discriminator(acc["name"])
            decoder = build_account_decoder(acc)
            self.accounts[disc] = decoder
            self.unified[disc] = ("account", decoder)
        
        # Errors (just store metadata)
        for err in idl.get("errors", []):
            disc = error_discriminator(err["code"])
            self.errors[disc] = err
    
    def decode(self, raw: bytes) -> Optional[Tuple[str, dict]]:
        """
        Attempt decode using unified registry.
        Returns (category, decoded_dict) or None.
        """
        disc = raw[:8]
        if disc in self.unified:
            category, decoder = self.unified[disc]
            return category, decoder(raw)
        return None
    
    def decode_event(self, raw: bytes) -> Optional[dict]:
        """Decode as event only."""
        disc = raw[:8]
        if disc in self.events:
            return self.events[disc](raw)
        return None
    
    def decode_instruction(self, raw: bytes) -> Optional[dict]:
        """Decode as instruction only."""
        disc = raw[:8]
        if disc in self.instructions:
            return self.instructions[disc](raw)
        return None
    
    def decode_account(self, raw: bytes) -> Optional[dict]:
        """Decode as account only."""
        disc = raw[:8]
        if disc in self.accounts:
            return self.accounts[disc](raw)
        return None
    



def build_registry_from_idls(idls: List[dict]) -> DecoderRegistry:
    """Build registry from multiple IDLs."""
    registry = DecoderRegistry()
    for idl in idls:
        if idl:
            registry.register_idl(idl)
    return registry


def get_all_idls():
    directory = '/home/flerb/Downloads/solana-defi-main/PumpFun/Typescript/'
    idl_dirs = """grpc-stream-and-parse-pump-amm-account
grpc-stream-and-parse-pump-amm-transaction
stream_and_parse_pump_fun_transactions
stream_new_pool_pump_swap_amm
stream_pump_amm_token_price
stream_pump_amm_transactions_and_detect_buy_sell_events
stream_pump_fun_new_minted_tokens
stream_pumpfun_token_price
stream_pumpfun_to_pumpAmm_migration_transactions
stream_pump_fun_transactions_and_detect_buy_sell_events
stream_pumpfun_txns_fetch_bonding_pool_liquidity""".split('\n')
    idls=[]
    for idl_dir in idl_dirs:
        idls_directory = os.path.join(directory,idl_dir,'idls')
        dirs,files = get_files_and_dirs(idls_directory)
        for file in files:
            data = safe_load_from_json(file)
            idls.append(data)
    return idls
def build_event_registry():
    registry = {}
    for idl in get_all_idls():
        if idl:

            accounts = idl.get("accounts") or []
            for acc in  accounts:
                name = acc["name"]
                disc = account_discriminator(name)
                registry[disc] =  build_instruction_decoder(acc)
            instructions = idl.get("instructions") or []
            for ix in  instructions:
                name = ix["name"]
                disc = instruction_discriminator(name)
                registry[disc] =  build_instruction_decoder(ix)
            events = idl.get("events") or []
            for event in  events:
                name = event["name"]
                disc = event_discriminator(name)
                registry[disc] = build_event_decoder(event)
    
    return registry
