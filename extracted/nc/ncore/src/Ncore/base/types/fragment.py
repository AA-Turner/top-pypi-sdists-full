# Copyright 2026 zovdev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import TYPE_CHECKING, overload, Optional


from ..builder import build_object
from . import aliases


if TYPE_CHECKING:
    from ..types import *


class FragmentCollectibleInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, purchase_date: int, currency: str, amount: int, crypto_currency: str, crypto_amount: int, url: str): ...

    def __init__(self, purchase_date, currency, amount, crypto_currency, crypto_amount, url, _='fragment.collectibleInfo', **kwargs):
        kwargs['purchase_date'] = purchase_date
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['crypto_currency'] = crypto_currency
        kwargs['crypto_amount'] = crypto_amount
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purchase_date(self) -> int:
        return self['purchase_date']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def crypto_currency(self) -> str:
        return self['crypto_currency']

    @property
    def crypto_amount(self) -> int:
        return self['crypto_amount']

    @property
    def url(self) -> str:
        return self['url']
