from enum import Enum

class BillingFundingStatus(str, Enum):
    Payment_required = "payment_required",
    Processing = "processing",
    Succeeded = "succeeded",
    Failed = "failed",
    Expired = "expired",
    Cancelled = "cancelled",

