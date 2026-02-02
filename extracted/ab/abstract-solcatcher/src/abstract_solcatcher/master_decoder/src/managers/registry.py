from .imports import *
from .schema import *
class EventRegistry:
    """
    Maps discriminators to decoders.
    Tracks errors for later analysis.
    """
    
    def __init__(self):
        self._decoders: Dict[bytes, Callable[[bytes], Any]] = {}
        self._names: Dict[bytes, str] = {}
        self.errors: List[DecodeError] = []
    
    def register(self, disc: bytes, name: str, decoder: Callable[[bytes], Any]):
        self._decoders[disc] = decoder
        self._names[disc] = name
    
    def register_by_name(self, event_name: str, decoder: Callable[[bytes], Any]):
        """Register using event:{name} discriminator"""
        disc = event_discriminator(event_name)
        self.register(disc, event_name, decoder)
    
    def register_raw(self, disc_hex: str, name: str, decoder: Callable[[bytes], Any]):
        """Register using raw hex discriminator"""
        self.register(bytes.fromhex(disc_hex), name, decoder)
    
    def decode(
        self,
        b64_data: str,
        *,
        signature: Optional[str] = None,
        program_id: Optional[str] = None,
    ) -> Optional[Any]:
        """Decode b64 data, return event or None (logs error)"""
        raw = base64.b64decode(b64_data)
        disc = raw[:8]
        disc_hex = disc.hex()
        
        if disc not in self._decoders:
            self.errors.append(DecodeError(
                signature=signature,
                program_id=program_id,
                discriminator=disc_hex,
                payload_len=len(raw) - 8,
                reason="unknown discriminator",
                b64=b64_data,
            ))
            return None
        
        try:
            return registry[raw[:8]](raw) 
        except Exception as e:
            self.errors.append(DecodeError(
                signature=signature,
                program_id=program_id,
                discriminator=disc_hex,
                payload_len=len(raw) - 8,
                reason=f"decode failed: {e}",
                b64=b64_data,
            ))
            return None
    
    def event_name(self, disc_hex: str) -> Optional[str]:
        """Get event name for a discriminator"""
        return self._names.get(bytes.fromhex(disc_hex))
    
    def errors_by_discriminator(self) -> Dict[str, List[DecodeError]]:
        out: Dict[str, List[DecodeError]] = {}
        for e in self.errors:
            out.setdefault(e.discriminator, []).append(e)
        return out

class InstructionRegistry:
    """
    Maps discriminators to decoders.
    Tracks errors for later analysis.
    """
    
    def __init__(self):
        self._decoders: Dict[bytes, Callable[[bytes], Any]] = {}
        self._names: Dict[bytes, str] = {}
        self.errors: List[DecodeError] = []
    
    def register(self, disc: bytes, name: str, decoder: Callable[[bytes], Any]):
        self._decoders[disc] = decoder
        self._names[disc] = name
    
    def register_by_name(self, event_name: str, decoder: Callable[[bytes], Any]):
        """Register using event:{name} discriminator"""
        disc = event_discriminator(event_name)
        self.register(disc, event_name, decoder)
    
    def register_raw(self, disc_hex: str, name: str, decoder: Callable[[bytes], Any]):
        """Register using raw hex discriminator"""
        self.register(bytes.fromhex(disc_hex), name, decoder)
    
    def decode(
        self,
        b64_data: str,
        *,
        signature: Optional[str] = None,
        program_id: Optional[str] = None,
    ) -> Optional[Any]:
        """Decode b64 data, return event or None (logs error)"""
        raw = base64.b64decode(b64_data)
        disc = raw[:8]
        disc_hex = disc.hex()
        
        if disc not in self._decoders:
            self.errors.append(DecodeError(
                signature=signature,
                program_id=program_id,
                discriminator=disc_hex,
                payload_len=len(raw) - 8,
                reason="unknown discriminator",
                b64=b64_data,
            ))
            return None
        
        try:
            return registry[raw[:8]](raw) 
        except Exception as e:
            self.errors.append(DecodeError(
                signature=signature,
                program_id=program_id,
                discriminator=disc_hex,
                payload_len=len(raw) - 8,
                reason=f"decode failed: {e}",
                b64=b64_data,
            ))
            return None
    
    def event_name(self, disc_hex: str) -> Optional[str]:
        """Get event name for a discriminator"""
        return self._names.get(bytes.fromhex(disc_hex))
    
    def errors_by_discriminator(self) -> Dict[str, List[DecodeError]]:
        out: Dict[str, List[DecodeError]] = {}
        for e in self.errors:
            out.setdefault(e.discriminator, []).append(e)
        return out

