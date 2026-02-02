from .imports import *
from .registry import *

# ============================================================================
# DECODER ENVIRONMENT
# ============================================================================

class DecoderEnvironment:
    """
    Wires up all decoders.
    Single entry point for decoding.
    """

    def __init__(self):
        self.registry = EventRegistry()
        self._wire()

    # ------------------------------------------------------------------
    # Wiring
    # ------------------------------------------------------------------

    def _wire(self):
        r = self.registry

        r.register_raw("e445a52e51cb9a1d", "CreateEvent", decode_create_event)
        r.register_raw("9b91c1cfc87a1d45", "TradeEvent", decode_trade_event)
        r.register_raw("c7a6c5b0b6d0b61d", "SetParamsEvent", decode_set_params_event)
        r.register_raw("b3c99d8a92e3e4aa", "CompleteEvent", decode_complete_event)
        r.register_raw("7a027f010ebf0caf", "CollectCreatorFeeEvent", decode_collect_creator_fee_event)

        r.register_raw("1b72a94ddeeb6376", "CreateEventV2", CreateDecoder)
        r.register_raw("33e685a4017f83ad", "SellEvent", SellDecoder)
        r.register_raw("bddb7fd34ee661ee", "BuyEvent", BuyDecoder)

        r.register_raw("e8f5c2eeeada3a59", "CollectCoinCreatorFee", decode_collect_creator_fee_event)
        r.register_raw("6161d7905d92167c", "ExtendAccount", decode_extend_account_event)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def decode(self, b64: str, **ctx) -> Optional[Any]:
        return self.registry.decode(b64, **ctx)

    def decode_row(self, row: dict) -> Optional[Any]:
        return self.registry.decode(
            row["b64"],
            signature=row.get("signature"),
            program_id=row.get("program_id"),
        )

    @property
    def errors(self) -> List[DecodeError]:
        return self.registry.errors


# ============================================================================
# LAZY SINGLETON ACCESSOR
# ============================================================================

_ENV: Optional[DecoderEnvironment] = None
def get_decoder_env() -> DecoderEnvironment:
    global _ENV

    if _ENV is None:
        _ENV = DecoderEnvironment()

    return _ENV
