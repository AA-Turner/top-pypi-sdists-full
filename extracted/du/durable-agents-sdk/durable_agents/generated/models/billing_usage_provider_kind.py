from enum import Enum

class BillingUsage_provider_kind(str, Enum):
    None_ = "none",
    Stripe = "stripe",

