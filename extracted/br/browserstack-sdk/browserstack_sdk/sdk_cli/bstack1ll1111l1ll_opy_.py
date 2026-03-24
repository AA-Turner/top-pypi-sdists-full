# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111lll11l_opy_,
    bstack1ll11l1l111_opy_,
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from bstack_utils.constants import EVENTS
class bstack1l1llll1111_opy_(bstack111lll11l_opy_):
    bstack11ll1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᥱ")
    NAME = bstack1ll1lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᥲ")
    bstack1l111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᥳ")
    bstack1ll1l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᥴ")
    bstack11l111lll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᥵")
    bstack11111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᥶")
    bstack11ll11l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣ᥷")
    bstack11l111ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ᥸")
    bstack11l111l1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨ᥹")
    bstack1l11llll111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨ᥺")
    bstack11ll1lll111_opy_ = bstack1ll1lll_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥ᥻")
    bstack11l111ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࠦ᥼")
    bstack11lllllll11_opy_ = bstack1ll1lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᥽")
    bstack11ll11111l1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧ᥾")
    bstack11ll11111ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦ᥿")
    bstack11l111l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᦀ")
    bstack11l111l11l1_opy_: Dict[str, List[Callable]] = dict()
    bstack11ll1lll1ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1lll111ll_opy_: Any
    bstack11ll1111lll_opy_: Dict
    def __init__(
        self,
        bstack11ll1lll1ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1lll111ll_opy_: Dict[str, Any],
        methods=[bstack1ll1lll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᦁ"), bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᦂ"), bstack1ll1lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᦃ"), bstack1ll1lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᦄ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11ll1lll1ll_opy_ = bstack11ll1lll1ll_opy_
        self.platform_index = platform_index
        self.bstack1ll11l11lll_opy_(methods)
        self.bstack1l1lll111ll_opy_ = bstack1l1lll111ll_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack111lll11l_opy_.get_data(bstack1l1llll1111_opy_.bstack1ll1l1l111l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack111lll11l_opy_.get_data(bstack1l1llll1111_opy_.bstack1l111ll111_opy_, target, strict)
    @staticmethod
    def bstack11l111l1l11_opy_(target: object, strict=True):
        return bstack111lll11l_opy_.get_data(bstack1l1llll1111_opy_.bstack11l111lll11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack111lll11l_opy_.get_data(bstack1l1llll1111_opy_.bstack11111l11l_opy_, target, strict)
    @staticmethod
    def bstack1l111lllll1_opy_(instance: bstack1ll11l1l111_opy_) -> bool:
        return bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack11ll11l1lll_opy_, False)
    @staticmethod
    def bstack1l11ll111ll_opy_(instance: bstack1ll11l1l111_opy_, default_value=None):
        return bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l111ll111_opy_, default_value)
    @staticmethod
    def bstack1l11ll11l1l_opy_(instance: bstack1ll11l1l111_opy_, default_value=None):
        return bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack11111l11l_opy_, default_value)
    @staticmethod
    def bstack1l11l1l11l1_opy_(hub_url: str, bstack11l111ll11l_opy_=bstack1ll1lll_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᦅ")):
        try:
            bstack11l111lll1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l111lll1l_opy_.endswith(bstack11l111ll11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l111l1ll_opy_(method_name: str):
        return method_name == bstack1ll1lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᦆ")
    @staticmethod
    def bstack1l1l111l11l_opy_(method_name: str, *args):
        return (
            bstack1l1llll1111_opy_.bstack1l1l111l1ll_opy_(method_name)
            and bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args) == bstack1l1llll1111_opy_.bstack11ll1lll111_opy_
        )
    @staticmethod
    def bstack1l1l111l1l1_opy_(method_name: str, *args):
        if not bstack1l1llll1111_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1l1llll1111_opy_.bstack11ll11111l1_opy_ in bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args):
            return False
        bstack1l11l1l11ll_opy_ = bstack1l1llll1111_opy_.bstack1l11l11lll1_opy_(*args)
        return bstack1l11l1l11ll_opy_ and bstack1ll1lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᦇ") in bstack1l11l1l11ll_opy_ and bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᦈ") in bstack1l11l1l11ll_opy_[bstack1ll1lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᦉ")]
    @staticmethod
    def bstack1l11ll1111l_opy_(method_name: str, *args):
        if not bstack1l1llll1111_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1l1llll1111_opy_.bstack11ll11111l1_opy_ in bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args):
            return False
        bstack1l11l1l11ll_opy_ = bstack1l1llll1111_opy_.bstack1l11l11lll1_opy_(*args)
        return (
            bstack1l11l1l11ll_opy_
            and bstack1ll1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᦊ") in bstack1l11l1l11ll_opy_
            and bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᦋ") in bstack1l11l1l11ll_opy_[bstack1ll1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᦌ")]
        )
    @staticmethod
    def bstack11ll1l11ll1_opy_(*args):
        return str(bstack1l1llll1111_opy_.bstack1l1l1111l1l_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l1111l1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11l11lll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll111lll_opy_(driver):
        command_executor = getattr(driver, bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᦍ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll1lll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᦎ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll1lll_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᦏ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll1lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᦐ"), None)
        return hub_url
    def bstack11ll11llll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᦑ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᦒ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll1lll_opy_ (u"ࠤࡢࡹࡷࡲࠢᦓ")):
                setattr(command_executor, bstack1ll1lll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᦔ"), hub_url)
                result = True
        if result:
            self.bstack11ll1lll1ll_opy_ = hub_url
            bstack1l1llll1111_opy_.bstack1l1l11lll_opy_(instance, bstack1l1llll1111_opy_.bstack1l111ll111_opy_, hub_url)
            bstack1l1llll1111_opy_.bstack1l1l11lll_opy_(
                instance, bstack1l1llll1111_opy_.bstack11ll11l1lll_opy_, bstack1l1llll1111_opy_.bstack1l11l1l11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_]):
        return bstack1ll1lll_opy_ (u"ࠦ࠿ࠨᦕ").join((bstack111l11ll_opy_(bstack1ll11l1ll11_opy_[0]).name, bstack1lll1ll11_opy_(bstack1ll11l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_], callback: Callable):
        bstack11ll111l11l_opy_ = bstack1l1llll1111_opy_.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        if not bstack11ll111l11l_opy_ in bstack1l1llll1111_opy_.bstack11l111l11l1_opy_:
            bstack1l1llll1111_opy_.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_] = []
        bstack1l1llll1111_opy_.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_].append(callback)
    def bstack1ll11l11l1l_opy_(self, instance: bstack1ll11l1l111_opy_, method_name: str, bstack1ll11lll11l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᦖ")):
            return
        cmd = args[0] if method_name == bstack1ll1lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᦗ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠢ࠻ࠤᦘ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᦙ") + bstack11l111ll111_opy_, bstack1ll11lll11l_opy_)
    def bstack11111lll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11ll11ll_opy_, bstack11ll111111l_opy_ = bstack1ll11l1ll11_opy_
        bstack11ll111l11l_opy_ = bstack1l1llll1111_opy_.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᦚ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᦛ"))
        if bstack1ll11ll11ll_opy_ == bstack111l11ll_opy_.QUIT:
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.PRE:
                bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l111l11ll_opy_.value)
                bstack111lll11l_opy_.bstack1l1l11lll_opy_(instance, EVENTS.bstack11l111l11ll_opy_.value, bstack11ll1ll1l_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᦜ").format(instance, method_name, bstack1ll11ll11ll_opy_, bstack11ll111111l_opy_))
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST:
                bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l111l1lll_opy_.value)
                bstack111lll11l_opy_.bstack1l1l11lll_opy_(instance, EVENTS.bstack11l111l1lll_opy_.value, bstack11ll1ll1l_opy_)
        if bstack1ll11ll11ll_opy_ == bstack111l11ll_opy_.bstack11ll1lll1_opy_:
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST and not bstack1l1llll1111_opy_.bstack1ll1l1l111l_opy_ in instance.data:
                session_id = getattr(target, bstack1ll1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᦝ"), None)
                if session_id:
                    instance.data[bstack1l1llll1111_opy_.bstack1ll1l1l111l_opy_] = session_id
        elif (
            bstack1ll11ll11ll_opy_ == bstack111l11ll_opy_.bstack1ll1ll111l1_opy_
            and bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args) == bstack1l1llll1111_opy_.bstack11ll1lll111_opy_
        ):
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.PRE:
                hub_url = bstack1l1llll1111_opy_.bstack1ll111lll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l1llll1111_opy_.bstack1l111ll111_opy_: hub_url,
                            bstack1l1llll1111_opy_.bstack11ll11l1lll_opy_: bstack1l1llll1111_opy_.bstack1l11l1l11l1_opy_(hub_url),
                            bstack1l1llll1111_opy_.bstack1l11llll111_opy_: int(
                                os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᦞ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11l1l11ll_opy_ = bstack1l1llll1111_opy_.bstack1l11l11lll1_opy_(*args)
                bstack11l111l1l11_opy_ = bstack1l11l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᦟ"), None) if bstack1l11l1l11ll_opy_ else None
                if isinstance(bstack11l111l1l11_opy_, dict):
                    instance.data[bstack1l1llll1111_opy_.bstack11l111lll11_opy_] = copy.deepcopy(bstack11l111l1l11_opy_)
                    instance.data[bstack1l1llll1111_opy_.bstack11111l11l_opy_] = bstack11l111l1l11_opy_
            elif bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll1lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᦠ"), dict()).get(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᦡ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l1llll1111_opy_.bstack1ll1l1l111l_opy_: framework_session_id,
                                bstack1l1llll1111_opy_.bstack11l111ll1ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll11ll11ll_opy_ == bstack111l11ll_opy_.bstack1ll1ll111l1_opy_
            and bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args) == bstack1l1llll1111_opy_.bstack11l111l1ll1_opy_
            and bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST
        ):
            instance.data[bstack1l1llll1111_opy_.bstack11l111l1l1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll111l11l_opy_ in bstack1l1llll1111_opy_.bstack11l111l11l1_opy_:
            bstack11ll111l111_opy_ = None
            for callback in bstack1l1llll1111_opy_.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_]:
                try:
                    bstack11ll1111111_opy_ = callback(self, target, exec, bstack1ll11l1ll11_opy_, result, *args, **kwargs)
                    if bstack11ll111l111_opy_ == None:
                        bstack11ll111l111_opy_ = bstack11ll1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᦢ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᦣ"))
                    traceback.print_exc()
            if bstack1ll11ll11ll_opy_ == bstack111l11ll_opy_.QUIT:
                if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.PRE:
                    bstack11ll1ll1l_opy_ = bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, EVENTS.bstack11l111l11ll_opy_.value)
                    if bstack11ll1ll1l_opy_!=None:
                        bstack1lll1lll11_opy_.end(EVENTS.bstack11l111l11ll_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᦤ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᦥ"), True, None)
                if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST:
                    bstack11ll1ll1l_opy_ = bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, EVENTS.bstack11l111l1lll_opy_.value)
                    if bstack11ll1ll1l_opy_!=None:
                        bstack1lll1lll11_opy_.end(EVENTS.bstack11l111l1lll_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᦦ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᦧ"), True, None)
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.PRE and callable(bstack11ll111l111_opy_):
                return bstack11ll111l111_opy_
            elif bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST and bstack11ll111l111_opy_:
                return bstack11ll111l111_opy_
    def bstack1ll1l111111_opy_(
        self, method_name, previous_state: bstack111l11ll_opy_, *args, **kwargs
    ) -> bstack111l11ll_opy_:
        if method_name == bstack1ll1lll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᦨ") or method_name == bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᦩ"):
            return bstack111l11ll_opy_.bstack11ll1lll1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᦪ"):
            return bstack111l11ll_opy_.QUIT
        if method_name == bstack1ll1lll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᦫ"):
            if previous_state != bstack111l11ll_opy_.NONE:
                command_name = bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args)
                if command_name == bstack1l1llll1111_opy_.bstack11ll1lll111_opy_:
                    return bstack111l11ll_opy_.bstack11ll1lll1_opy_
            return bstack111l11ll_opy_.bstack1ll1ll111l1_opy_
        return bstack111l11ll_opy_.NONE