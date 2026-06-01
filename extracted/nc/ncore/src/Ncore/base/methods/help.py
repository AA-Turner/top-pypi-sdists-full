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

class HelpGetConfig(TLMethod[aliases.AnyConfig]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getConfig'):
        dict.__init__(self, _=_)


class HelpGetNearestDc(TLMethod[aliases.AnyNearestDc]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getNearestDc'):
        dict.__init__(self, _=_)


class HelpGetAppUpdate(TLMethod[aliases.AnyHelpAppUpdate]):
    __slots__ = ()

    @overload
    def __init__(self, source: str): ...

    def __init__(self, source, _='help.getAppUpdate', **kwargs):
        kwargs['source'] = source
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def source(self) -> str:
        return self['source']


class HelpGetInviteText(TLMethod[aliases.AnyHelpInviteText]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getInviteText'):
        dict.__init__(self, _=_)


class HelpGetSupport(TLMethod[aliases.AnyHelpSupport]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getSupport'):
        dict.__init__(self, _=_)


class HelpSetBotUpdatesStatus(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, pending_updates_count: int, message: str): ...

    def __init__(self, pending_updates_count, message, _='help.setBotUpdatesStatus', **kwargs):
        kwargs['pending_updates_count'] = pending_updates_count
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pending_updates_count(self) -> int:
        return self['pending_updates_count']

    @property
    def message(self) -> str:
        return self['message']


class HelpGetCdnConfig(TLMethod[aliases.AnyCdnConfig]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getCdnConfig'):
        dict.__init__(self, _=_)


class HelpGetRecentMeUrls(TLMethod[aliases.AnyHelpRecentMeUrls]):
    __slots__ = ()

    @overload
    def __init__(self, referer: str): ...

    def __init__(self, referer, _='help.getRecentMeUrls', **kwargs):
        kwargs['referer'] = referer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def referer(self) -> str:
        return self['referer']


class HelpGetTermsOfServiceUpdate(TLMethod[aliases.AnyHelpTermsOfServiceUpdate]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getTermsOfServiceUpdate'):
        dict.__init__(self, _=_)


class HelpAcceptTermsOfService(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyDataJSON): ...

    def __init__(self, id, _='help.acceptTermsOfService', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyDataJSON:
        return build_object(self['id'])


class HelpGetDeepLinkInfo(TLMethod[aliases.AnyHelpDeepLinkInfo]):
    __slots__ = ()

    @overload
    def __init__(self, path: str): ...

    def __init__(self, path, _='help.getDeepLinkInfo', **kwargs):
        kwargs['path'] = path
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def path(self) -> str:
        return self['path']


class HelpGetAppConfig(TLMethod[aliases.AnyHelpAppConfig]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='help.getAppConfig', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class HelpSaveAppLog(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, events: list[aliases.AnyInputAppEvent]): ...

    def __init__(self, events, _='help.saveAppLog', **kwargs):
        kwargs['events'] = events
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def events(self) -> list[aliases.AnyInputAppEvent]:
        return build_object(self['events'])


class HelpGetPassportConfig(TLMethod[aliases.AnyHelpPassportConfig]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='help.getPassportConfig', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class HelpGetSupportName(TLMethod[aliases.AnyHelpSupportName]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getSupportName'):
        dict.__init__(self, _=_)


class HelpGetUserInfo(TLMethod[aliases.AnyHelpUserInfo]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser): ...

    def __init__(self, user_id, _='help.getUserInfo', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class HelpEditUserInfo(TLMethod[aliases.AnyHelpUserInfo]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, message: str, entities: list[aliases.AnyMessageEntity]): ...

    def __init__(self, user_id, message, entities, _='help.editUserInfo', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['message'] = message
        kwargs['entities'] = entities
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])


class HelpGetPromoData(TLMethod[aliases.AnyHelpPromoData]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getPromoData'):
        dict.__init__(self, _=_)


class HelpHidePromoData(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='help.hidePromoData', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class HelpDismissSuggestion(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, suggestion: str): ...

    def __init__(self, peer, suggestion, _='help.dismissSuggestion', **kwargs):
        kwargs['peer'] = peer
        kwargs['suggestion'] = suggestion
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def suggestion(self) -> str:
        return self['suggestion']


class HelpGetCountriesList(TLMethod[aliases.AnyHelpCountriesList]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, hash: int): ...

    def __init__(self, lang_code, hash, _='help.getCountriesList', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def hash(self) -> int:
        return self['hash']


class HelpGetPremiumPromo(TLMethod[aliases.AnyHelpPremiumPromo]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.getPremiumPromo'):
        dict.__init__(self, _=_)


class HelpGetPeerColors(TLMethod[aliases.AnyHelpPeerColors]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='help.getPeerColors', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class HelpGetPeerProfileColors(TLMethod[aliases.AnyHelpPeerColors]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='help.getPeerProfileColors', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class HelpGetTimezonesList(TLMethod[aliases.AnyHelpTimezonesList]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='help.getTimezonesList', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']
