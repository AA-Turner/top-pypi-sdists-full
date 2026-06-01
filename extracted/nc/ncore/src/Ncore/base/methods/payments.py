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
from typing import TYPE_CHECKING, overload, Optional, Union, Generic, TypeVar, TypeAlias


from ..builder import build_object
from ..types import aliases
from . import TLMethod, ReturnT


if TYPE_CHECKING:
    from ..types import *
    from ..methods import *

class PaymentsGetPaymentForm(TLMethod[aliases.AnyPaymentsPaymentForm]):
    __slots__ = ()

    @overload
    def __init__(self, invoice: aliases.AnyInputInvoice, theme_params: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, invoice, _='payments.getPaymentForm', **kwargs):
        kwargs['invoice'] = invoice
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invoice(self) -> aliases.AnyInputInvoice:
        return build_object(self['invoice'])

    @property
    def theme_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['theme_params'])


class PaymentsGetPaymentReceipt(TLMethod[aliases.AnyPaymentsPaymentReceipt]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='payments.getPaymentReceipt', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class PaymentsValidateRequestedInfo(TLMethod[aliases.AnyPaymentsValidatedRequestedInfo]):
    __slots__ = ()

    @overload
    def __init__(self, invoice: aliases.AnyInputInvoice, info: aliases.AnyPaymentRequestedInfo, save: Optional[bool] = ...): ...

    def __init__(self, invoice, info, _='payments.validateRequestedInfo', **kwargs):
        kwargs['invoice'] = invoice
        kwargs['info'] = info
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def save(self) -> Optional[bool]:
        return self['save']

    @property
    def invoice(self) -> aliases.AnyInputInvoice:
        return build_object(self['invoice'])

    @property
    def info(self) -> aliases.AnyPaymentRequestedInfo:
        return build_object(self['info'])


class PaymentsSendPaymentForm(TLMethod[aliases.AnyPaymentsPaymentResult]):
    __slots__ = ()

    @overload
    def __init__(self, form_id: int, invoice: aliases.AnyInputInvoice, credentials: aliases.AnyInputPaymentCredentials, requested_info_id: Optional[str] = ..., shipping_option_id: Optional[str] = ..., tip_amount: Optional[int] = ...): ...

    def __init__(self, form_id, invoice, credentials, _='payments.sendPaymentForm', **kwargs):
        kwargs['form_id'] = form_id
        kwargs['invoice'] = invoice
        kwargs['credentials'] = credentials
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def form_id(self) -> int:
        return self['form_id']

    @property
    def invoice(self) -> aliases.AnyInputInvoice:
        return build_object(self['invoice'])

    @property
    def requested_info_id(self) -> Optional[str]:
        return self['requested_info_id']

    @property
    def shipping_option_id(self) -> Optional[str]:
        return self['shipping_option_id']

    @property
    def credentials(self) -> aliases.AnyInputPaymentCredentials:
        return build_object(self['credentials'])

    @property
    def tip_amount(self) -> Optional[int]:
        return self['tip_amount']


class PaymentsGetSavedInfo(TLMethod[aliases.AnyPaymentsSavedInfo]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.getSavedInfo'):
        dict.__init__(self, _=_)


class PaymentsClearSavedInfo(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, credentials: Optional[bool] = ..., info: Optional[bool] = ...): ...

    def __init__(self, _='payments.clearSavedInfo', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def credentials(self) -> Optional[bool]:
        return self['credentials']

    @property
    def info(self) -> Optional[bool]:
        return self['info']


class PaymentsGetBankCardData(TLMethod[aliases.AnyPaymentsBankCardData]):
    __slots__ = ()

    @overload
    def __init__(self, number: str): ...

    def __init__(self, number, _='payments.getBankCardData', **kwargs):
        kwargs['number'] = number
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def number(self) -> str:
        return self['number']


class PaymentsExportInvoice(TLMethod[aliases.AnyPaymentsExportedInvoice]):
    __slots__ = ()

    @overload
    def __init__(self, invoice_media: aliases.AnyInputMedia): ...

    def __init__(self, invoice_media, _='payments.exportInvoice', **kwargs):
        kwargs['invoice_media'] = invoice_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invoice_media(self) -> aliases.AnyInputMedia:
        return build_object(self['invoice_media'])


class PaymentsAssignAppStoreTransaction(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, receipt: bytes, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, receipt, purpose, _='payments.assignAppStoreTransaction', **kwargs):
        kwargs['receipt'] = receipt
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def receipt(self) -> bytes:
        return self['receipt']

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class PaymentsAssignPlayMarketTransaction(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, receipt: aliases.AnyDataJSON, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, receipt, purpose, _='payments.assignPlayMarketTransaction', **kwargs):
        kwargs['receipt'] = receipt
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def receipt(self) -> aliases.AnyDataJSON:
        return build_object(self['receipt'])

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class PaymentsGetPremiumGiftCodeOptions(TLMethod[list[aliases.AnyPremiumGiftCodeOption]]):
    __slots__ = ()

    @overload
    def __init__(self, boost_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, _='payments.getPremiumGiftCodeOptions', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def boost_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['boost_peer'])


class PaymentsCheckGiftCode(TLMethod[aliases.AnyPaymentsCheckedGiftCode]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='payments.checkGiftCode', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class PaymentsApplyGiftCode(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='payments.applyGiftCode', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class PaymentsGetGiveawayInfo(TLMethod[aliases.AnyPaymentsGiveawayInfo]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='payments.getGiveawayInfo', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class PaymentsLaunchPrepaidGiveaway(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, giveaway_id: int, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, peer, giveaway_id, purpose, _='payments.launchPrepaidGiveaway', **kwargs):
        kwargs['peer'] = peer
        kwargs['giveaway_id'] = giveaway_id
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def giveaway_id(self) -> int:
        return self['giveaway_id']

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class PaymentsGetStarsTopupOptions(TLMethod[list[aliases.AnyStarsTopupOption]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.getStarsTopupOptions'):
        dict.__init__(self, _=_)


class PaymentsGetStarsStatus(TLMethod[aliases.AnyPaymentsStarsStatus]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, ton: Optional[bool] = ...): ...

    def __init__(self, peer, _='payments.getStarsStatus', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PaymentsGetStarsTransactions(TLMethod[aliases.AnyPaymentsStarsStatus]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset: str, limit: int, inbound: Optional[bool] = ..., outbound: Optional[bool] = ..., ascending: Optional[bool] = ..., ton: Optional[bool] = ..., subscription_id: Optional[str] = ...): ...

    def __init__(self, peer, offset, limit, _='payments.getStarsTransactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inbound(self) -> Optional[bool]:
        return self['inbound']

    @property
    def outbound(self) -> Optional[bool]:
        return self['outbound']

    @property
    def ascending(self) -> Optional[bool]:
        return self['ascending']

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def subscription_id(self) -> Optional[str]:
        return self['subscription_id']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsSendStarsForm(TLMethod[aliases.AnyPaymentsPaymentResult]):
    __slots__ = ()

    @overload
    def __init__(self, form_id: int, invoice: aliases.AnyInputInvoice): ...

    def __init__(self, form_id, invoice, _='payments.sendStarsForm', **kwargs):
        kwargs['form_id'] = form_id
        kwargs['invoice'] = invoice
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def form_id(self) -> int:
        return self['form_id']

    @property
    def invoice(self) -> aliases.AnyInputInvoice:
        return build_object(self['invoice'])


class PaymentsRefundStarsCharge(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, charge_id: str): ...

    def __init__(self, user_id, charge_id, _='payments.refundStarsCharge', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['charge_id'] = charge_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def charge_id(self) -> str:
        return self['charge_id']


class PaymentsGetStarsRevenueStats(TLMethod[aliases.AnyPaymentsStarsRevenueStats]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, dark: Optional[bool] = ..., ton: Optional[bool] = ...): ...

    def __init__(self, peer, _='payments.getStarsRevenueStats', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PaymentsGetStarsRevenueWithdrawalUrl(TLMethod[aliases.AnyPaymentsStarsRevenueWithdrawalUrl]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, password: aliases.AnyInputCheckPasswordSRP, ton: Optional[bool] = ..., amount: Optional[int] = ...): ...

    def __init__(self, peer, password, _='payments.getStarsRevenueWithdrawalUrl', **kwargs):
        kwargs['peer'] = peer
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def amount(self) -> Optional[int]:
        return self['amount']

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])


class PaymentsGetStarsRevenueAdsAccountUrl(TLMethod[aliases.AnyPaymentsStarsRevenueAdsAccountUrl]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='payments.getStarsRevenueAdsAccountUrl', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PaymentsGetStarsTransactionsByID(TLMethod[aliases.AnyPaymentsStarsStatus]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[aliases.AnyInputStarsTransaction], ton: Optional[bool] = ...): ...

    def __init__(self, peer, id, _='payments.getStarsTransactionsByID', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[aliases.AnyInputStarsTransaction]:
        return build_object(self['id'])


class PaymentsGetStarsGiftOptions(TLMethod[list[aliases.AnyStarsGiftOption]]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: Optional[aliases.AnyInputUser] = ...): ...

    def __init__(self, _='payments.getStarsGiftOptions', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['user_id'])


class PaymentsGetStarsSubscriptions(TLMethod[aliases.AnyPaymentsStarsStatus]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset: str, missing_balance: Optional[bool] = ...): ...

    def __init__(self, peer, offset, _='payments.getStarsSubscriptions', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def missing_balance(self) -> Optional[bool]:
        return self['missing_balance']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset(self) -> str:
        return self['offset']


class PaymentsChangeStarsSubscription(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, subscription_id: str, canceled: Optional[bool] = ...): ...

    def __init__(self, peer, subscription_id, _='payments.changeStarsSubscription', **kwargs):
        kwargs['peer'] = peer
        kwargs['subscription_id'] = subscription_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def subscription_id(self) -> str:
        return self['subscription_id']

    @property
    def canceled(self) -> Optional[bool]:
        return self['canceled']


class PaymentsFulfillStarsSubscription(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, subscription_id: str): ...

    def __init__(self, peer, subscription_id, _='payments.fulfillStarsSubscription', **kwargs):
        kwargs['peer'] = peer
        kwargs['subscription_id'] = subscription_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def subscription_id(self) -> str:
        return self['subscription_id']


class PaymentsGetStarsGiveawayOptions(TLMethod[list[aliases.AnyStarsGiveawayOption]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='payments.getStarsGiveawayOptions'):
        dict.__init__(self, _=_)


class PaymentsGetStarGifts(TLMethod[aliases.AnyPaymentsStarGifts]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='payments.getStarGifts', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class PaymentsSaveStarGift(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, unsave: Optional[bool] = ...): ...

    def __init__(self, stargift, _='payments.saveStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unsave(self) -> Optional[bool]:
        return self['unsave']

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])


class PaymentsConvertStarGift(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift): ...

    def __init__(self, stargift, _='payments.convertStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])


class PaymentsBotCancelStarsSubscription(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, charge_id: str, restore: Optional[bool] = ...): ...

    def __init__(self, user_id, charge_id, _='payments.botCancelStarsSubscription', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['charge_id'] = charge_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def restore(self) -> Optional[bool]:
        return self['restore']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def charge_id(self) -> str:
        return self['charge_id']


class PaymentsGetConnectedStarRefBots(TLMethod[aliases.AnyPaymentsConnectedStarRefBots]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, limit: int, offset_date: Optional[int] = ..., offset_link: Optional[str] = ...): ...

    def __init__(self, peer, limit, _='payments.getConnectedStarRefBots', **kwargs):
        kwargs['peer'] = peer
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset_date(self) -> Optional[int]:
        return self['offset_date']

    @property
    def offset_link(self) -> Optional[str]:
        return self['offset_link']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsGetConnectedStarRefBot(TLMethod[aliases.AnyPaymentsConnectedStarRefBots]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, bot: aliases.AnyInputUser): ...

    def __init__(self, peer, bot, _='payments.getConnectedStarRefBot', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class PaymentsGetSuggestedStarRefBots(TLMethod[aliases.AnyPaymentsSuggestedStarRefBots]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset: str, limit: int, order_by_revenue: Optional[bool] = ..., order_by_date: Optional[bool] = ...): ...

    def __init__(self, peer, offset, limit, _='payments.getSuggestedStarRefBots', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order_by_revenue(self) -> Optional[bool]:
        return self['order_by_revenue']

    @property
    def order_by_date(self) -> Optional[bool]:
        return self['order_by_date']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsConnectStarRefBot(TLMethod[aliases.AnyPaymentsConnectedStarRefBots]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, bot: aliases.AnyInputUser): ...

    def __init__(self, peer, bot, _='payments.connectStarRefBot', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class PaymentsEditConnectedStarRefBot(TLMethod[aliases.AnyPaymentsConnectedStarRefBots]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, link: str, revoked: Optional[bool] = ...): ...

    def __init__(self, peer, link, _='payments.editConnectedStarRefBot', **kwargs):
        kwargs['peer'] = peer
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoked(self) -> Optional[bool]:
        return self['revoked']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> str:
        return self['link']


class PaymentsGetStarGiftUpgradePreview(TLMethod[aliases.AnyPaymentsStarGiftUpgradePreview]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int): ...

    def __init__(self, gift_id, _='payments.getStarGiftUpgradePreview', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']


class PaymentsUpgradeStarGift(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, keep_original_details: Optional[bool] = ...): ...

    def __init__(self, stargift, _='payments.upgradeStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def keep_original_details(self) -> Optional[bool]:
        return self['keep_original_details']

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])


class PaymentsTransferStarGift(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, to_id: aliases.AnyInputPeer): ...

    def __init__(self, stargift, to_id, _='payments.transferStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['to_id'] = to_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])

    @property
    def to_id(self) -> aliases.AnyInputPeer:
        return build_object(self['to_id'])


class PaymentsGetUniqueStarGift(TLMethod[aliases.AnyPaymentsUniqueStarGift]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='payments.getUniqueStarGift', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class PaymentsGetSavedStarGifts(TLMethod[aliases.AnyPaymentsSavedStarGifts]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset: str, limit: int, exclude_unsaved: Optional[bool] = ..., exclude_saved: Optional[bool] = ..., exclude_unlimited: Optional[bool] = ..., exclude_unique: Optional[bool] = ..., sort_by_value: Optional[bool] = ..., exclude_upgradable: Optional[bool] = ..., exclude_unupgradable: Optional[bool] = ..., peer_color_available: Optional[bool] = ..., exclude_hosted: Optional[bool] = ..., collection_id: Optional[int] = ...): ...

    def __init__(self, peer, offset, limit, _='payments.getSavedStarGifts', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_unsaved(self) -> Optional[bool]:
        return self['exclude_unsaved']

    @property
    def exclude_saved(self) -> Optional[bool]:
        return self['exclude_saved']

    @property
    def exclude_unlimited(self) -> Optional[bool]:
        return self['exclude_unlimited']

    @property
    def exclude_unique(self) -> Optional[bool]:
        return self['exclude_unique']

    @property
    def sort_by_value(self) -> Optional[bool]:
        return self['sort_by_value']

    @property
    def exclude_upgradable(self) -> Optional[bool]:
        return self['exclude_upgradable']

    @property
    def exclude_unupgradable(self) -> Optional[bool]:
        return self['exclude_unupgradable']

    @property
    def peer_color_available(self) -> Optional[bool]:
        return self['peer_color_available']

    @property
    def exclude_hosted(self) -> Optional[bool]:
        return self['exclude_hosted']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def collection_id(self) -> Optional[int]:
        return self['collection_id']

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsGetSavedStarGift(TLMethod[aliases.AnyPaymentsSavedStarGifts]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: list[aliases.AnyInputSavedStarGift]): ...

    def __init__(self, stargift, _='payments.getSavedStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> list[aliases.AnyInputSavedStarGift]:
        return build_object(self['stargift'])


class PaymentsGetStarGiftWithdrawalUrl(TLMethod[aliases.AnyPaymentsStarGiftWithdrawalUrl]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, password: aliases.AnyInputCheckPasswordSRP): ...

    def __init__(self, stargift, password, _='payments.getStarGiftWithdrawalUrl', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])


class PaymentsToggleChatStarGiftNotifications(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, enabled: Optional[bool] = ...): ...

    def __init__(self, peer, _='payments.toggleChatStarGiftNotifications', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def enabled(self) -> Optional[bool]:
        return self['enabled']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PaymentsToggleStarGiftsPinnedToTop(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, stargift: list[aliases.AnyInputSavedStarGift]): ...

    def __init__(self, peer, stargift, _='payments.toggleStarGiftsPinnedToTop', **kwargs):
        kwargs['peer'] = peer
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def stargift(self) -> list[aliases.AnyInputSavedStarGift]:
        return build_object(self['stargift'])


class PaymentsCanPurchaseStore(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, purpose, _='payments.canPurchaseStore', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class PaymentsGetResaleStarGifts(TLMethod[aliases.AnyPaymentsResaleStarGifts]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int, offset: str, limit: int, sort_by_price: Optional[bool] = ..., sort_by_num: Optional[bool] = ..., for_craft: Optional[bool] = ..., attributes_hash: Optional[int] = ..., attributes: Optional[list[aliases.AnyStarGiftAttributeId]] = ...): ...

    def __init__(self, gift_id, offset, limit, _='payments.getResaleStarGifts', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sort_by_price(self) -> Optional[bool]:
        return self['sort_by_price']

    @property
    def sort_by_num(self) -> Optional[bool]:
        return self['sort_by_num']

    @property
    def for_craft(self) -> Optional[bool]:
        return self['for_craft']

    @property
    def attributes_hash(self) -> Optional[int]:
        return self['attributes_hash']

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def attributes(self) -> Optional[list[aliases.AnyStarGiftAttributeId]]:
        return build_object(self['attributes'])

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsUpdateStarGiftPrice(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, resell_amount: aliases.AnyStarsAmount): ...

    def __init__(self, stargift, resell_amount, _='payments.updateStarGiftPrice', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['resell_amount'] = resell_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])

    @property
    def resell_amount(self) -> aliases.AnyStarsAmount:
        return build_object(self['resell_amount'])


class PaymentsCreateStarGiftCollection(TLMethod[aliases.AnyStarGiftCollection]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, title: str, stargift: list[aliases.AnyInputSavedStarGift]): ...

    def __init__(self, peer, title, stargift, _='payments.createStarGiftCollection', **kwargs):
        kwargs['peer'] = peer
        kwargs['title'] = title
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def stargift(self) -> list[aliases.AnyInputSavedStarGift]:
        return build_object(self['stargift'])


class PaymentsUpdateStarGiftCollection(TLMethod[aliases.AnyStarGiftCollection]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, collection_id: int, title: Optional[str] = ..., delete_stargift: Optional[list[aliases.AnyInputSavedStarGift]] = ..., add_stargift: Optional[list[aliases.AnyInputSavedStarGift]] = ..., order: Optional[list[aliases.AnyInputSavedStarGift]] = ...): ...

    def __init__(self, peer, collection_id, _='payments.updateStarGiftCollection', **kwargs):
        kwargs['peer'] = peer
        kwargs['collection_id'] = collection_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def collection_id(self) -> int:
        return self['collection_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def delete_stargift(self) -> Optional[list[aliases.AnyInputSavedStarGift]]:
        return build_object(self['delete_stargift'])

    @property
    def add_stargift(self) -> Optional[list[aliases.AnyInputSavedStarGift]]:
        return build_object(self['add_stargift'])

    @property
    def order(self) -> Optional[list[aliases.AnyInputSavedStarGift]]:
        return build_object(self['order'])


class PaymentsReorderStarGiftCollections(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, order: list[int]): ...

    def __init__(self, peer, order, _='payments.reorderStarGiftCollections', **kwargs):
        kwargs['peer'] = peer
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def order(self) -> list[int]:
        return self['order']


class PaymentsDeleteStarGiftCollection(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, collection_id: int): ...

    def __init__(self, peer, collection_id, _='payments.deleteStarGiftCollection', **kwargs):
        kwargs['peer'] = peer
        kwargs['collection_id'] = collection_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def collection_id(self) -> int:
        return self['collection_id']


class PaymentsGetStarGiftCollections(TLMethod[aliases.AnyPaymentsStarGiftCollections]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, hash: int): ...

    def __init__(self, peer, hash, _='payments.getStarGiftCollections', **kwargs):
        kwargs['peer'] = peer
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def hash(self) -> int:
        return self['hash']


class PaymentsGetUniqueStarGiftValueInfo(TLMethod[aliases.AnyPaymentsUniqueStarGiftValueInfo]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='payments.getUniqueStarGiftValueInfo', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class PaymentsCheckCanSendGift(TLMethod[aliases.AnyPaymentsCheckCanSendGiftResult]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int): ...

    def __init__(self, gift_id, _='payments.checkCanSendGift', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']


class PaymentsGetStarGiftAuctionState(TLMethod[aliases.AnyPaymentsStarGiftAuctionState]):
    __slots__ = ()

    @overload
    def __init__(self, auction: aliases.AnyInputStarGiftAuction, version: int): ...

    def __init__(self, auction, version, _='payments.getStarGiftAuctionState', **kwargs):
        kwargs['auction'] = auction
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def auction(self) -> aliases.AnyInputStarGiftAuction:
        return build_object(self['auction'])

    @property
    def version(self) -> int:
        return self['version']


class PaymentsGetStarGiftAuctionAcquiredGifts(TLMethod[aliases.AnyPaymentsStarGiftAuctionAcquiredGifts]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int): ...

    def __init__(self, gift_id, _='payments.getStarGiftAuctionAcquiredGifts', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']


class PaymentsGetStarGiftActiveAuctions(TLMethod[aliases.AnyPaymentsStarGiftActiveAuctions]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='payments.getStarGiftActiveAuctions', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class PaymentsResolveStarGiftOffer(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, offer_msg_id: int, decline: Optional[bool] = ...): ...

    def __init__(self, offer_msg_id, _='payments.resolveStarGiftOffer', **kwargs):
        kwargs['offer_msg_id'] = offer_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def decline(self) -> Optional[bool]:
        return self['decline']

    @property
    def offer_msg_id(self) -> int:
        return self['offer_msg_id']


class PaymentsSendStarGiftOffer(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, slug: str, price: aliases.AnyStarsAmount, duration: int, random_id: int, allow_paid_stars: Optional[int] = ...): ...

    def __init__(self, peer, slug, price, duration, random_id, _='payments.sendStarGiftOffer', **kwargs):
        kwargs['peer'] = peer
        kwargs['slug'] = slug
        kwargs['price'] = price
        kwargs['duration'] = duration
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def price(self) -> aliases.AnyStarsAmount:
        return build_object(self['price'])

    @property
    def duration(self) -> int:
        return self['duration']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']


class PaymentsGetStarGiftUpgradeAttributes(TLMethod[aliases.AnyPaymentsStarGiftUpgradeAttributes]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int): ...

    def __init__(self, gift_id, _='payments.getStarGiftUpgradeAttributes', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']


class PaymentsGetCraftStarGifts(TLMethod[aliases.AnyPaymentsSavedStarGifts]):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int, offset: str, limit: int): ...

    def __init__(self, gift_id, offset, limit, _='payments.getCraftStarGifts', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PaymentsCraftStarGift(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, stargift: list[aliases.AnyInputSavedStarGift]): ...

    def __init__(self, stargift, _='payments.craftStarGift', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> list[aliases.AnyInputSavedStarGift]:
        return build_object(self['stargift'])
