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


class PaymentsPaymentForm(dict):
    __slots__ = ()

    @overload
    def __init__(self, form_id: int, bot_id: int, title: str, description: str, invoice: aliases.AnyInvoice, provider_id: int, url: str, users: list[aliases.AnyUser], can_save_credentials: Optional[bool] = ..., password_missing: Optional[bool] = ..., photo: Optional[aliases.AnyWebDocument] = ..., native_provider: Optional[str] = ..., native_params: Optional[aliases.AnyDataJSON] = ..., additional_methods: Optional[list[aliases.AnyPaymentFormMethod]] = ..., saved_info: Optional[aliases.AnyPaymentRequestedInfo] = ..., saved_credentials: Optional[list[aliases.AnyPaymentSavedCredentials]] = ...): ...

    def __init__(self, form_id, bot_id, title, description, invoice, provider_id, url, users, _='payments.paymentForm', **kwargs):
        kwargs['form_id'] = form_id
        kwargs['bot_id'] = bot_id
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['provider_id'] = provider_id
        kwargs['url'] = url
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_save_credentials(self) -> Optional[bool]:
        return self['can_save_credentials']

    @property
    def password_missing(self) -> Optional[bool]:
        return self['password_missing']

    @property
    def form_id(self) -> int:
        return self['form_id']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def provider_id(self) -> int:
        return self['provider_id']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def native_provider(self) -> Optional[str]:
        return self['native_provider']

    @property
    def native_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['native_params'])

    @property
    def additional_methods(self) -> Optional[list[aliases.AnyPaymentFormMethod]]:
        return build_object(self['additional_methods'])

    @property
    def saved_info(self) -> Optional[aliases.AnyPaymentRequestedInfo]:
        return build_object(self['saved_info'])

    @property
    def saved_credentials(self) -> Optional[list[aliases.AnyPaymentSavedCredentials]]:
        return build_object(self['saved_credentials'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsPaymentFormStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, form_id: int, bot_id: int, title: str, description: str, invoice: aliases.AnyInvoice, users: list[aliases.AnyUser], photo: Optional[aliases.AnyWebDocument] = ...): ...

    def __init__(self, form_id, bot_id, title, description, invoice, users, _='payments.paymentFormStars', **kwargs):
        kwargs['form_id'] = form_id
        kwargs['bot_id'] = bot_id
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def form_id(self) -> int:
        return self['form_id']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsPaymentFormStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, form_id: int, invoice: aliases.AnyInvoice): ...

    def __init__(self, form_id, invoice, _='payments.paymentFormStarGift', **kwargs):
        kwargs['form_id'] = form_id
        kwargs['invoice'] = invoice
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def form_id(self) -> int:
        return self['form_id']

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])


class PaymentsValidatedRequestedInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: Optional[str] = ..., shipping_options: Optional[list[aliases.AnyShippingOption]] = ...): ...

    def __init__(self, _='payments.validatedRequestedInfo', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> Optional[str]:
        return self['id']

    @property
    def shipping_options(self) -> Optional[list[aliases.AnyShippingOption]]:
        return build_object(self['shipping_options'])


class PaymentsPaymentResult(dict):
    __slots__ = ()

    @overload
    def __init__(self, updates: aliases.AnyUpdates): ...

    def __init__(self, updates, _='payments.paymentResult', **kwargs):
        kwargs['updates'] = updates
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def updates(self) -> aliases.AnyUpdates:
        return build_object(self['updates'])


class PaymentsPaymentVerificationNeeded(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='payments.paymentVerificationNeeded', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class PaymentsPaymentReceipt(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, bot_id: int, provider_id: int, title: str, description: str, invoice: aliases.AnyInvoice, currency: str, total_amount: int, credentials_title: str, users: list[aliases.AnyUser], photo: Optional[aliases.AnyWebDocument] = ..., info: Optional[aliases.AnyPaymentRequestedInfo] = ..., shipping: Optional[aliases.AnyShippingOption] = ..., tip_amount: Optional[int] = ...): ...

    def __init__(self, date, bot_id, provider_id, title, description, invoice, currency, total_amount, credentials_title, users, _='payments.paymentReceipt', **kwargs):
        kwargs['date'] = date
        kwargs['bot_id'] = bot_id
        kwargs['provider_id'] = provider_id
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['credentials_title'] = credentials_title
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def provider_id(self) -> int:
        return self['provider_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def info(self) -> Optional[aliases.AnyPaymentRequestedInfo]:
        return build_object(self['info'])

    @property
    def shipping(self) -> Optional[aliases.AnyShippingOption]:
        return build_object(self['shipping'])

    @property
    def tip_amount(self) -> Optional[int]:
        return self['tip_amount']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def credentials_title(self) -> str:
        return self['credentials_title']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsPaymentReceiptStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, bot_id: int, title: str, description: str, invoice: aliases.AnyInvoice, currency: str, total_amount: int, transaction_id: str, users: list[aliases.AnyUser], photo: Optional[aliases.AnyWebDocument] = ...): ...

    def __init__(self, date, bot_id, title, description, invoice, currency, total_amount, transaction_id, users, _='payments.paymentReceiptStars', **kwargs):
        kwargs['date'] = date
        kwargs['bot_id'] = bot_id
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['transaction_id'] = transaction_id
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def transaction_id(self) -> str:
        return self['transaction_id']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsSavedInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, has_saved_credentials: Optional[bool] = ..., saved_info: Optional[aliases.AnyPaymentRequestedInfo] = ...): ...

    def __init__(self, _='payments.savedInfo', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_saved_credentials(self) -> Optional[bool]:
        return self['has_saved_credentials']

    @property
    def saved_info(self) -> Optional[aliases.AnyPaymentRequestedInfo]:
        return build_object(self['saved_info'])


class PaymentsBankCardData(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, open_urls: list[aliases.AnyBankCardOpenUrl]): ...

    def __init__(self, title, open_urls, _='payments.bankCardData', **kwargs):
        kwargs['title'] = title
        kwargs['open_urls'] = open_urls
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def open_urls(self) -> list[aliases.AnyBankCardOpenUrl]:
        return build_object(self['open_urls'])


class PaymentsExportedInvoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='payments.exportedInvoice', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class PaymentsCheckedGiftCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, days: int, chats: list[aliases.AnyChat], users: list[aliases.AnyUser], via_giveaway: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., giveaway_msg_id: Optional[int] = ..., to_id: Optional[int] = ..., used_date: Optional[int] = ...): ...

    def __init__(self, date, days, chats, users, _='payments.checkedGiftCode', **kwargs):
        kwargs['date'] = date
        kwargs['days'] = days
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_giveaway(self) -> Optional[bool]:
        return self['via_giveaway']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def giveaway_msg_id(self) -> Optional[int]:
        return self['giveaway_msg_id']

    @property
    def to_id(self) -> Optional[int]:
        return self['to_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def days(self) -> int:
        return self['days']

    @property
    def used_date(self) -> Optional[int]:
        return self['used_date']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsGiveawayInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, start_date: int, participating: Optional[bool] = ..., preparing_results: Optional[bool] = ..., joined_too_early_date: Optional[int] = ..., admin_disallowed_chat_id: Optional[int] = ..., disallowed_country: Optional[str] = ...): ...

    def __init__(self, start_date, _='payments.giveawayInfo', **kwargs):
        kwargs['start_date'] = start_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participating(self) -> Optional[bool]:
        return self['participating']

    @property
    def preparing_results(self) -> Optional[bool]:
        return self['preparing_results']

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def joined_too_early_date(self) -> Optional[int]:
        return self['joined_too_early_date']

    @property
    def admin_disallowed_chat_id(self) -> Optional[int]:
        return self['admin_disallowed_chat_id']

    @property
    def disallowed_country(self) -> Optional[str]:
        return self['disallowed_country']


class PaymentsGiveawayInfoResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, start_date: int, finish_date: int, winners_count: int, winner: Optional[bool] = ..., refunded: Optional[bool] = ..., gift_code_slug: Optional[str] = ..., stars_prize: Optional[int] = ..., activated_count: Optional[int] = ...): ...

    def __init__(self, start_date, finish_date, winners_count, _='payments.giveawayInfoResults', **kwargs):
        kwargs['start_date'] = start_date
        kwargs['finish_date'] = finish_date
        kwargs['winners_count'] = winners_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def winner(self) -> Optional[bool]:
        return self['winner']

    @property
    def refunded(self) -> Optional[bool]:
        return self['refunded']

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def gift_code_slug(self) -> Optional[str]:
        return self['gift_code_slug']

    @property
    def stars_prize(self) -> Optional[int]:
        return self['stars_prize']

    @property
    def finish_date(self) -> int:
        return self['finish_date']

    @property
    def winners_count(self) -> int:
        return self['winners_count']

    @property
    def activated_count(self) -> Optional[int]:
        return self['activated_count']


class PaymentsStarsStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, balance: aliases.AnyStarsAmount, chats: list[aliases.AnyChat], users: list[aliases.AnyUser], subscriptions: Optional[list[aliases.AnyStarsSubscription]] = ..., subscriptions_next_offset: Optional[str] = ..., subscriptions_missing_balance: Optional[int] = ..., history: Optional[list[aliases.AnyStarsTransaction]] = ..., next_offset: Optional[str] = ...): ...

    def __init__(self, balance, chats, users, _='payments.starsStatus', **kwargs):
        kwargs['balance'] = balance
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def balance(self) -> aliases.AnyStarsAmount:
        return build_object(self['balance'])

    @property
    def subscriptions(self) -> Optional[list[aliases.AnyStarsSubscription]]:
        return build_object(self['subscriptions'])

    @property
    def subscriptions_next_offset(self) -> Optional[str]:
        return self['subscriptions_next_offset']

    @property
    def subscriptions_missing_balance(self) -> Optional[int]:
        return self['subscriptions_missing_balance']

    @property
    def history(self) -> Optional[list[aliases.AnyStarsTransaction]]:
        return build_object(self['history'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsStarsRevenueStats(dict):
    __slots__ = ()

    @overload
    def __init__(self, revenue_graph: aliases.AnyStatsGraph, status: aliases.AnyStarsRevenueStatus, usd_rate: float, top_hours_graph: Optional[aliases.AnyStatsGraph] = ...): ...

    def __init__(self, revenue_graph, status, usd_rate, _='payments.starsRevenueStats', **kwargs):
        kwargs['revenue_graph'] = revenue_graph
        kwargs['status'] = status
        kwargs['usd_rate'] = usd_rate
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def top_hours_graph(self) -> Optional[aliases.AnyStatsGraph]:
        return build_object(self['top_hours_graph'])

    @property
    def revenue_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['revenue_graph'])

    @property
    def status(self) -> aliases.AnyStarsRevenueStatus:
        return build_object(self['status'])

    @property
    def usd_rate(self) -> float:
        return self['usd_rate']


class PaymentsStarsRevenueWithdrawalUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='payments.starsRevenueWithdrawalUrl', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class PaymentsStarsRevenueAdsAccountUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='payments.starsRevenueAdsAccountUrl', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class PaymentsStarGiftsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.starGiftsNotModified'):
        dict.__init__(self, _=_)


class PaymentsStarGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, gifts: list[aliases.AnyStarGift], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, hash, gifts, chats, users, _='payments.starGifts', **kwargs):
        kwargs['hash'] = hash
        kwargs['gifts'] = gifts
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def gifts(self) -> list[aliases.AnyStarGift]:
        return build_object(self['gifts'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsConnectedStarRefBots(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, connected_bots: list[aliases.AnyConnectedBotStarRef], users: list[aliases.AnyUser]): ...

    def __init__(self, count, connected_bots, users, _='payments.connectedStarRefBots', **kwargs):
        kwargs['count'] = count
        kwargs['connected_bots'] = connected_bots
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def connected_bots(self) -> list[aliases.AnyConnectedBotStarRef]:
        return build_object(self['connected_bots'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsSuggestedStarRefBots(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, suggested_bots: list[aliases.AnyStarRefProgram], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, suggested_bots, users, _='payments.suggestedStarRefBots', **kwargs):
        kwargs['count'] = count
        kwargs['suggested_bots'] = suggested_bots
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def suggested_bots(self) -> list[aliases.AnyStarRefProgram]:
        return build_object(self['suggested_bots'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']


class PaymentsStarGiftUpgradePreview(dict):
    __slots__ = ()

    @overload
    def __init__(self, sample_attributes: list[aliases.AnyStarGiftAttribute], prices: list[aliases.AnyStarGiftUpgradePrice], next_prices: list[aliases.AnyStarGiftUpgradePrice]): ...

    def __init__(self, sample_attributes, prices, next_prices, _='payments.starGiftUpgradePreview', **kwargs):
        kwargs['sample_attributes'] = sample_attributes
        kwargs['prices'] = prices
        kwargs['next_prices'] = next_prices
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sample_attributes(self) -> list[aliases.AnyStarGiftAttribute]:
        return build_object(self['sample_attributes'])

    @property
    def prices(self) -> list[aliases.AnyStarGiftUpgradePrice]:
        return build_object(self['prices'])

    @property
    def next_prices(self) -> list[aliases.AnyStarGiftUpgradePrice]:
        return build_object(self['next_prices'])


class PaymentsUniqueStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, gift, chats, users, _='payments.uniqueStarGift', **kwargs):
        kwargs['gift'] = gift
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsSavedStarGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, gifts: list[aliases.AnySavedStarGift], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], chat_notifications_enabled: Optional[bool] = ..., next_offset: Optional[str] = ...): ...

    def __init__(self, count, gifts, chats, users, _='payments.savedStarGifts', **kwargs):
        kwargs['count'] = count
        kwargs['gifts'] = gifts
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def chat_notifications_enabled(self) -> Optional[bool]:
        return self['chat_notifications_enabled']

    @property
    def gifts(self) -> list[aliases.AnySavedStarGift]:
        return build_object(self['gifts'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsStarGiftWithdrawalUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='payments.starGiftWithdrawalUrl', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class PaymentsResaleStarGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, gifts: list[aliases.AnyStarGift], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ..., attributes: Optional[list[aliases.AnyStarGiftAttribute]] = ..., attributes_hash: Optional[int] = ..., counters: Optional[list[aliases.AnyStarGiftAttributeCounter]] = ...): ...

    def __init__(self, count, gifts, chats, users, _='payments.resaleStarGifts', **kwargs):
        kwargs['count'] = count
        kwargs['gifts'] = gifts
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def gifts(self) -> list[aliases.AnyStarGift]:
        return build_object(self['gifts'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def attributes(self) -> Optional[list[aliases.AnyStarGiftAttribute]]:
        return build_object(self['attributes'])

    @property
    def attributes_hash(self) -> Optional[int]:
        return self['attributes_hash']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def counters(self) -> Optional[list[aliases.AnyStarGiftAttributeCounter]]:
        return build_object(self['counters'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PaymentsStarGiftCollectionsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.starGiftCollectionsNotModified'):
        dict.__init__(self, _=_)


class PaymentsStarGiftCollections(dict):
    __slots__ = ()

    @overload
    def __init__(self, collections: list[aliases.AnyStarGiftCollection]): ...

    def __init__(self, collections, _='payments.starGiftCollections', **kwargs):
        kwargs['collections'] = collections
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collections(self) -> list[aliases.AnyStarGiftCollection]:
        return build_object(self['collections'])


class PaymentsUniqueStarGiftValueInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, value: int, initial_sale_date: int, initial_sale_stars: int, initial_sale_price: int, last_sale_on_fragment: Optional[bool] = ..., value_is_average: Optional[bool] = ..., last_sale_date: Optional[int] = ..., last_sale_price: Optional[int] = ..., floor_price: Optional[int] = ..., average_price: Optional[int] = ..., listed_count: Optional[int] = ..., fragment_listed_count: Optional[int] = ..., fragment_listed_url: Optional[str] = ...): ...

    def __init__(self, currency, value, initial_sale_date, initial_sale_stars, initial_sale_price, _='payments.uniqueStarGiftValueInfo', **kwargs):
        kwargs['currency'] = currency
        kwargs['value'] = value
        kwargs['initial_sale_date'] = initial_sale_date
        kwargs['initial_sale_stars'] = initial_sale_stars
        kwargs['initial_sale_price'] = initial_sale_price
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def last_sale_on_fragment(self) -> Optional[bool]:
        return self['last_sale_on_fragment']

    @property
    def value_is_average(self) -> Optional[bool]:
        return self['value_is_average']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def value(self) -> int:
        return self['value']

    @property
    def initial_sale_date(self) -> int:
        return self['initial_sale_date']

    @property
    def initial_sale_stars(self) -> int:
        return self['initial_sale_stars']

    @property
    def initial_sale_price(self) -> int:
        return self['initial_sale_price']

    @property
    def last_sale_date(self) -> Optional[int]:
        return self['last_sale_date']

    @property
    def last_sale_price(self) -> Optional[int]:
        return self['last_sale_price']

    @property
    def floor_price(self) -> Optional[int]:
        return self['floor_price']

    @property
    def average_price(self) -> Optional[int]:
        return self['average_price']

    @property
    def listed_count(self) -> Optional[int]:
        return self['listed_count']

    @property
    def fragment_listed_count(self) -> Optional[int]:
        return self['fragment_listed_count']

    @property
    def fragment_listed_url(self) -> Optional[str]:
        return self['fragment_listed_url']


class PaymentsCheckCanSendGiftResultOk(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.checkCanSendGiftResultOk'):
        dict.__init__(self, _=_)


class PaymentsCheckCanSendGiftResultFail(dict):
    __slots__ = ()

    @overload
    def __init__(self, reason: aliases.AnyTextWithEntities): ...

    def __init__(self, reason, _='payments.checkCanSendGiftResultFail', **kwargs):
        kwargs['reason'] = reason
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reason(self) -> aliases.AnyTextWithEntities:
        return build_object(self['reason'])


class PaymentsStarGiftAuctionState(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, state: aliases.AnyStarGiftAuctionState, user_state: aliases.AnyStarGiftAuctionUserState, timeout: int, users: list[aliases.AnyUser], chats: list[aliases.AnyChat]): ...

    def __init__(self, gift, state, user_state, timeout, users, chats, _='payments.starGiftAuctionState', **kwargs):
        kwargs['gift'] = gift
        kwargs['state'] = state
        kwargs['user_state'] = user_state
        kwargs['timeout'] = timeout
        kwargs['users'] = users
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def state(self) -> aliases.AnyStarGiftAuctionState:
        return build_object(self['state'])

    @property
    def user_state(self) -> aliases.AnyStarGiftAuctionUserState:
        return build_object(self['user_state'])

    @property
    def timeout(self) -> int:
        return self['timeout']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])


class PaymentsStarGiftAuctionAcquiredGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self, gifts: list[aliases.AnyStarGiftAuctionAcquiredGift], users: list[aliases.AnyUser], chats: list[aliases.AnyChat]): ...

    def __init__(self, gifts, users, chats, _='payments.starGiftAuctionAcquiredGifts', **kwargs):
        kwargs['gifts'] = gifts
        kwargs['users'] = users
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gifts(self) -> list[aliases.AnyStarGiftAuctionAcquiredGift]:
        return build_object(self['gifts'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])


class PaymentsStarGiftActiveAuctionsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.starGiftActiveAuctionsNotModified'):
        dict.__init__(self, _=_)


class PaymentsStarGiftActiveAuctions(dict):
    __slots__ = ()

    @overload
    def __init__(self, auctions: list[aliases.AnyStarGiftActiveAuctionState], users: list[aliases.AnyUser], chats: list[aliases.AnyChat]): ...

    def __init__(self, auctions, users, chats, _='payments.starGiftActiveAuctions', **kwargs):
        kwargs['auctions'] = auctions
        kwargs['users'] = users
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def auctions(self) -> list[aliases.AnyStarGiftActiveAuctionState]:
        return build_object(self['auctions'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])


class PaymentsStarGiftUpgradeAttributes(dict):
    __slots__ = ()

    @overload
    def __init__(self, attributes: list[aliases.AnyStarGiftAttribute]): ...

    def __init__(self, attributes, _='payments.starGiftUpgradeAttributes', **kwargs):
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attributes(self) -> list[aliases.AnyStarGiftAttribute]:
        return build_object(self['attributes'])
