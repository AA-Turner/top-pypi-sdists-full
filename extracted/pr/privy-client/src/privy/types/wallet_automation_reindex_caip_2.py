# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .evm_caip_2 import EvmCaip2
from .tron_caip_2 import TronCaip2

__all__ = ["WalletAutomationReindexCaip2"]

WalletAutomationReindexCaip2: TypeAlias = Union[EvmCaip2, TronCaip2]
