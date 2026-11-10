from enum import Enum


class TransactionTypeEnum(str, Enum):
    ADJUSTMENT = "adjustment"
    AFFILIATE_FEE = "affiliate_fee"
    COMPENSATION = "compensation"
    EXPIRY = "expiry"
    HISTORICAL_COMPENSATION = "historical_compensation"
    MINIMAL_DRAW = "minimal_draw"
    PAYOUT = "payout"
    RECLASSIFICATION = "reclassification"
    ROLLBACK = "rollback"
    STAFF_GRANT = "staff_grant"
    TOP_UP = "top_up"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    WITHDRAWABLE_ADJUSTMENT = "withdrawable_adjustment"

    def __str__(self) -> str:
        return str(self.value)
