# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack1l1lll1111_opy_,
    bstack1ll11llllll_opy_,
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from bstack_utils.constants import EVENTS
class bstack1ll111l11ll_opy_(bstack1l1lll1111_opy_):
    bstack11ll1111l1l_opy_ = bstack11lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢ᥮")
    NAME = bstack11lll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ᥯")
    bstack11l1111lll_opy_ = bstack11lll1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᥰ")
    bstack1ll1ll1ll1l_opy_ = bstack11lll1_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᥱ")
    bstack11l111ll1ll_opy_ = bstack11lll1_opy_ (u"ࠦ࡮ࡴࡰࡶࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᥲ")
    bstack1l1l111l11_opy_ = bstack11lll1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᥳ")
    bstack11ll111lll1_opy_ = bstack11lll1_opy_ (u"ࠨࡩࡴࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡪࡸࡦࠧᥴ")
    bstack11l111l1l1l_opy_ = bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦ᥵")
    bstack11l11l11111_opy_ = bstack11lll1_opy_ (u"ࠣࡧࡱࡨࡪࡪ࡟ࡢࡶࠥ᥶")
    bstack1l11lll1ll1_opy_ = bstack11lll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥ᥷")
    bstack11ll11llll1_opy_ = bstack11lll1_opy_ (u"ࠥࡲࡪࡽࡳࡦࡵࡶ࡭ࡴࡴࠢ᥸")
    bstack11l111ll111_opy_ = bstack11lll1_opy_ (u"ࠦ࡬࡫ࡴࠣ᥹")
    bstack1l111l1lll1_opy_ = bstack11lll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᥺")
    bstack11ll111l11l_opy_ = bstack11lll1_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤ᥻")
    bstack11ll111l111_opy_ = bstack11lll1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣ᥼")
    bstack11l111ll1l1_opy_ = bstack11lll1_opy_ (u"ࠣࡳࡸ࡭ࡹࠨ᥽")
    bstack11l111lll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack11ll1lll1l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1ll11l1l1_opy_: Any
    bstack11ll1111lll_opy_: Dict
    def __init__(
        self,
        bstack11ll1lll1l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1ll11l1l1_opy_: Dict[str, Any],
        methods=[bstack11lll1_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦ᥾"), bstack11lll1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥ᥿"), bstack11lll1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᦀ"), bstack11lll1_opy_ (u"ࠧࡷࡵࡪࡶࠥᦁ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11ll1lll1l1_opy_ = bstack11ll1lll1l1_opy_
        self.platform_index = platform_index
        self.bstack1ll11ll11l1_opy_(methods)
        self.bstack1l1ll11l1l1_opy_ = bstack1l1ll11l1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1l1lll1111_opy_.get_data(bstack1ll111l11ll_opy_.bstack1ll1ll1ll1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1l1lll1111_opy_.get_data(bstack1ll111l11ll_opy_.bstack11l1111lll_opy_, target, strict)
    @staticmethod
    def bstack11l111llll1_opy_(target: object, strict=True):
        return bstack1l1lll1111_opy_.get_data(bstack1ll111l11ll_opy_.bstack11l111ll1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1l1lll1111_opy_.get_data(bstack1ll111l11ll_opy_.bstack1l1l111l11_opy_, target, strict)
    @staticmethod
    def bstack1l11l111l1l_opy_(instance: bstack1ll11llllll_opy_) -> bool:
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack11ll111lll1_opy_, False)
    @staticmethod
    def bstack1l1l111ll11_opy_(instance: bstack1ll11llllll_opy_, default_value=None):
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack11l1111lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1111lll_opy_(instance: bstack1ll11llllll_opy_, default_value=None):
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l1l111l11_opy_, default_value)
    @staticmethod
    def bstack1l11l11ll1l_opy_(hub_url: str, bstack11l111l1lll_opy_=bstack11lll1_opy_ (u"ࠨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᦂ")):
        try:
            bstack11l111l1ll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l111l1ll1_opy_.endswith(bstack11l111l1lll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l11ll1ll11_opy_(method_name: str):
        return method_name == bstack11lll1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᦃ")
    @staticmethod
    def bstack1l11lll11l1_opy_(method_name: str, *args):
        return (
            bstack1ll111l11ll_opy_.bstack1l11ll1ll11_opy_(method_name)
            and bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args) == bstack1ll111l11ll_opy_.bstack11ll11llll1_opy_
        )
    @staticmethod
    def bstack1l11ll1l111_opy_(method_name: str, *args):
        if not bstack1ll111l11ll_opy_.bstack1l11ll1ll11_opy_(method_name):
            return False
        if not bstack1ll111l11ll_opy_.bstack11ll111l11l_opy_ in bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args):
            return False
        bstack1l11l1l1l11_opy_ = bstack1ll111l11ll_opy_.bstack1l11l11llll_opy_(*args)
        return bstack1l11l1l1l11_opy_ and bstack11lll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᦄ") in bstack1l11l1l1l11_opy_ and bstack11lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᦅ") in bstack1l11l1l1l11_opy_[bstack11lll1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᦆ")]
    @staticmethod
    def bstack1l11ll11l1l_opy_(method_name: str, *args):
        if not bstack1ll111l11ll_opy_.bstack1l11ll1ll11_opy_(method_name):
            return False
        if not bstack1ll111l11ll_opy_.bstack11ll111l11l_opy_ in bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args):
            return False
        bstack1l11l1l1l11_opy_ = bstack1ll111l11ll_opy_.bstack1l11l11llll_opy_(*args)
        return (
            bstack1l11l1l1l11_opy_
            and bstack11lll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᦇ") in bstack1l11l1l1l11_opy_
            and bstack11lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᦈ") in bstack1l11l1l1l11_opy_[bstack11lll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᦉ")]
        )
    @staticmethod
    def bstack11ll1ll1l11_opy_(*args):
        return str(bstack1ll111l11ll_opy_.bstack1l11l1lll11_opy_(*args)).lower()
    @staticmethod
    def bstack1l11l1lll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11l11llll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1111ll1ll_opy_(driver):
        command_executor = getattr(driver, bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᦊ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11lll1_opy_ (u"ࠣࡡࡸࡶࡱࠨᦋ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11lll1_opy_ (u"ࠤࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠥᦌ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11lll1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡢࡷࡪࡸࡶࡦࡴࡢࡥࡩࡪࡲࠣᦍ"), None)
        return hub_url
    def bstack11ll1l11l1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11lll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᦎ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11lll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᦏ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11lll1_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᦐ")):
                setattr(command_executor, bstack11lll1_opy_ (u"ࠢࡠࡷࡵࡰࠧᦑ"), hub_url)
                result = True
        if result:
            self.bstack11ll1lll1l1_opy_ = hub_url
            bstack1ll111l11ll_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1ll111l11ll_opy_.bstack11l1111lll_opy_, hub_url)
            bstack1ll111l11ll_opy_.bstack1ll1ll1l1l_opy_(
                instance, bstack1ll111l11ll_opy_.bstack11ll111lll1_opy_, bstack1ll111l11ll_opy_.bstack1l11l11ll1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1111l11_opy_(bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_]):
        return bstack11lll1_opy_ (u"ࠣ࠼ࠥᦒ").join((bstack111ll1lll1_opy_(bstack1ll1l111111_opy_[0]).name, bstack11lllll11l_opy_(bstack1ll1l111111_opy_[1]).name))
    @staticmethod
    def bstack1l1l111lll1_opy_(bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_], callback: Callable):
        bstack11ll11111ll_opy_ = bstack1ll111l11ll_opy_.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        if not bstack11ll11111ll_opy_ in bstack1ll111l11ll_opy_.bstack11l111lll1l_opy_:
            bstack1ll111l11ll_opy_.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_] = []
        bstack1ll111l11ll_opy_.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_].append(callback)
    def bstack1ll11l1lll1_opy_(self, instance: bstack1ll11llllll_opy_, method_name: str, bstack1ll11ll111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11lll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᦓ")):
            return
        cmd = args[0] if method_name == bstack11lll1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᦔ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l111lllll_opy_ = bstack11lll1_opy_ (u"ࠦ࠿ࠨᦕ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠨᦖ") + bstack11l111lllll_opy_, bstack1ll11ll111l_opy_)
    def bstack1ll1ll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11l1111l_opy_, bstack11ll1111ll1_opy_ = bstack1ll1l111111_opy_
        bstack11ll11111ll_opy_ = bstack1ll111l11ll_opy_.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡ࡫ࡳࡴࡱ࠺ࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᦗ") + str(kwargs) + bstack11lll1_opy_ (u"ࠢࠣᦘ"))
        if bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.QUIT:
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.PRE:
                bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l111ll11l_opy_.value)
                bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, EVENTS.bstack11l111ll11l_opy_.value, bstack11lllll1_opy_)
                self.logger.debug(bstack11lll1_opy_ (u"ࠣ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᦙ").format(instance, method_name, bstack1ll11l1111l_opy_, bstack11ll1111ll1_opy_))
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST:
                bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l111lll11_opy_.value)
                bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, EVENTS.bstack11l111lll11_opy_.value, bstack11lllll1_opy_)
        if bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.bstack1l1111ll11_opy_:
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST and not bstack1ll111l11ll_opy_.bstack1ll1ll1ll1l_opy_ in instance.data:
                session_id = getattr(target, bstack11lll1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᦚ"), None)
                if session_id:
                    instance.data[bstack1ll111l11ll_opy_.bstack1ll1ll1ll1l_opy_] = session_id
        elif (
            bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_
            and bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args) == bstack1ll111l11ll_opy_.bstack11ll11llll1_opy_
        ):
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.PRE:
                hub_url = bstack1ll111l11ll_opy_.bstack1111ll1ll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll111l11ll_opy_.bstack11l1111lll_opy_: hub_url,
                            bstack1ll111l11ll_opy_.bstack11ll111lll1_opy_: bstack1ll111l11ll_opy_.bstack1l11l11ll1l_opy_(hub_url),
                            bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_: int(
                                os.environ.get(bstack11lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᦛ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11l1l1l11_opy_ = bstack1ll111l11ll_opy_.bstack1l11l11llll_opy_(*args)
                bstack11l111llll1_opy_ = bstack1l11l1l1l11_opy_.get(bstack11lll1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᦜ"), None) if bstack1l11l1l1l11_opy_ else None
                if isinstance(bstack11l111llll1_opy_, dict):
                    instance.data[bstack1ll111l11ll_opy_.bstack11l111ll1ll_opy_] = copy.deepcopy(bstack11l111llll1_opy_)
                    instance.data[bstack1ll111l11ll_opy_.bstack1l1l111l11_opy_] = bstack11l111llll1_opy_
            elif bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11lll1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᦝ"), dict()).get(bstack11lll1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᦞ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll111l11ll_opy_.bstack1ll1ll1ll1l_opy_: framework_session_id,
                                bstack1ll111l11ll_opy_.bstack11l111l1l1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_
            and bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args) == bstack1ll111l11ll_opy_.bstack11l111ll1l1_opy_
            and bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST
        ):
            instance.data[bstack1ll111l11ll_opy_.bstack11l11l11111_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll11111ll_opy_ in bstack1ll111l11ll_opy_.bstack11l111lll1l_opy_:
            bstack11ll111l1ll_opy_ = None
            for callback in bstack1ll111l11ll_opy_.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_]:
                try:
                    bstack11ll111l1l1_opy_ = callback(self, target, exec, bstack1ll1l111111_opy_, result, *args, **kwargs)
                    if bstack11ll111l1ll_opy_ == None:
                        bstack11ll111l1ll_opy_ = bstack11ll111l1l1_opy_
                except Exception as e:
                    self.logger.error(bstack11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᦟ") + str(e) + bstack11lll1_opy_ (u"ࠣࠤᦠ"))
                    traceback.print_exc()
            if bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.QUIT:
                if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.PRE:
                    bstack11lllll1_opy_ = bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, EVENTS.bstack11l111ll11l_opy_.value)
                    if bstack11lllll1_opy_!=None:
                        bstack1llll11l_opy_.end(EVENTS.bstack11l111ll11l_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᦡ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᦢ"), True, None)
                if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST:
                    bstack11lllll1_opy_ = bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, EVENTS.bstack11l111lll11_opy_.value)
                    if bstack11lllll1_opy_!=None:
                        bstack1llll11l_opy_.end(EVENTS.bstack11l111lll11_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᦣ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᦤ"), True, None)
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.PRE and callable(bstack11ll111l1ll_opy_):
                return bstack11ll111l1ll_opy_
            elif bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST and bstack11ll111l1ll_opy_:
                return bstack11ll111l1ll_opy_
    def bstack1ll1l1111ll_opy_(
        self, method_name, previous_state: bstack111ll1lll1_opy_, *args, **kwargs
    ) -> bstack111ll1lll1_opy_:
        if method_name == bstack11lll1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᦥ") or method_name == bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᦦ"):
            return bstack111ll1lll1_opy_.bstack1l1111ll11_opy_
        if method_name == bstack11lll1_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᦧ"):
            return bstack111ll1lll1_opy_.QUIT
        if method_name == bstack11lll1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᦨ"):
            if previous_state != bstack111ll1lll1_opy_.NONE:
                command_name = bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args)
                if command_name == bstack1ll111l11ll_opy_.bstack11ll11llll1_opy_:
                    return bstack111ll1lll1_opy_.bstack1l1111ll11_opy_
            return bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_
        return bstack111ll1lll1_opy_.NONE