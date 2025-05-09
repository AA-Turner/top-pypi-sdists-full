# This file was auto-generated by Fern from our API Definition.

import typing_extensions
from .money import MoneyParams


class GiftCardActivityImportReversalParams(typing_extensions.TypedDict):
    """
    Represents details about an `IMPORT_REVERSAL` [gift card activity type](entity:GiftCardActivityType).
    """

    amount_money: MoneyParams
    """
    The amount of money cleared from the third-party gift card when 
    the import was reversed.
    """
