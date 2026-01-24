# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll1ll1l1l_opy_,
    bstack1lll1l1111l_opy_,
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1l111l1l_opy_(bstack1lll1ll1l1l_opy_):
    bstack11lllll1lll_opy_ = bstack1l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᚄ")
    NAME = bstack1l1111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᚅ")
    bstack1l111lllll1_opy_ = bstack1l1111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᚆ")
    bstack1l11l1111ll_opy_ = bstack1l1111_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᚇ")
    bstack11ll11ll111_opy_ = bstack1l1111_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᚈ")
    bstack1l11l111lll_opy_ = bstack1l1111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᚉ")
    bstack1l11111l11l_opy_ = bstack1l1111_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᚊ")
    bstack11ll11l11l1_opy_ = bstack1l1111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᚋ")
    bstack11ll11l1l1l_opy_ = bstack1l1111_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᚌ")
    bstack1l1ll1l11ll_opy_ = bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᚍ")
    bstack1l111l11111_opy_ = bstack1l1111_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᚎ")
    bstack11ll11l11ll_opy_ = bstack1l1111_opy_ (u"ࠢࡨࡧࡷࠦᚏ")
    bstack1l11ll1ll11_opy_ = bstack1l1111_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᚐ")
    bstack11llllll1ll_opy_ = bstack1l1111_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᚑ")
    bstack11lllllll11_opy_ = bstack1l1111_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᚒ")
    bstack11ll11ll1ll_opy_ = bstack1l1111_opy_ (u"ࠦࡶࡻࡩࡵࠤᚓ")
    bstack11ll11l111l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l111l11ll1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll11111l1_opy_: Any
    bstack11llllll11l_opy_: Dict
    def __init__(
        self,
        bstack1l111l11ll1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll11111l1_opy_: Dict[str, Any],
        methods=[bstack1l1111_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᚔ"), bstack1l1111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᚕ"), bstack1l1111_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᚖ"), bstack1l1111_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᚗ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l111l11ll1_opy_ = bstack1l111l11ll1_opy_
        self.platform_index = platform_index
        self.bstack1lll1ll1lll_opy_(methods)
        self.bstack1lll11111l1_opy_ = bstack1lll11111l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll1ll1l1l_opy_.get_data(bstack1ll1l111l1l_opy_.bstack1l11l1111ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll1ll1l1l_opy_.get_data(bstack1ll1l111l1l_opy_.bstack1l111lllll1_opy_, target, strict)
    @staticmethod
    def bstack11ll11ll1l1_opy_(target: object, strict=True):
        return bstack1lll1ll1l1l_opy_.get_data(bstack1ll1l111l1l_opy_.bstack11ll11ll111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll1ll1l1l_opy_.get_data(bstack1ll1l111l1l_opy_.bstack1l11l111lll_opy_, target, strict)
    @staticmethod
    def bstack1l1l1l1l1l1_opy_(instance: bstack1lll1l1111l_opy_) -> bool:
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11111l11l_opy_, False)
    @staticmethod
    def bstack1l1ll1lll11_opy_(instance: bstack1lll1l1111l_opy_, default_value=None):
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111lllll1_opy_, default_value)
    @staticmethod
    def bstack1l1lll1l1ll_opy_(instance: bstack1lll1l1111l_opy_, default_value=None):
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l111lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1ll1lll_opy_(hub_url: str, bstack11ll11l1lll_opy_=bstack1l1111_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᚘ")):
        try:
            bstack11ll11lll11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11ll11lll11_opy_.endswith(bstack11ll11l1lll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1llll111l_opy_(method_name: str):
        return method_name == bstack1l1111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᚙ")
    @staticmethod
    def bstack1l1lll1lll1_opy_(method_name: str, *args):
        return (
            bstack1ll1l111l1l_opy_.bstack1l1llll111l_opy_(method_name)
            and bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args) == bstack1ll1l111l1l_opy_.bstack1l111l11111_opy_
        )
    @staticmethod
    def bstack1l1lll11l1l_opy_(method_name: str, *args):
        if not bstack1ll1l111l1l_opy_.bstack1l1llll111l_opy_(method_name):
            return False
        if not bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_ in bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args):
            return False
        bstack1l1l1ll1l1l_opy_ = bstack1ll1l111l1l_opy_.bstack1l1l1ll11ll_opy_(*args)
        return bstack1l1l1ll1l1l_opy_ and bstack1l1111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᚚ") in bstack1l1l1ll1l1l_opy_ and bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᚛") in bstack1l1l1ll1l1l_opy_[bstack1l1111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᚜")]
    @staticmethod
    def bstack1l1llllll1l_opy_(method_name: str, *args):
        if not bstack1ll1l111l1l_opy_.bstack1l1llll111l_opy_(method_name):
            return False
        if not bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_ in bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args):
            return False
        bstack1l1l1ll1l1l_opy_ = bstack1ll1l111l1l_opy_.bstack1l1l1ll11ll_opy_(*args)
        return (
            bstack1l1l1ll1l1l_opy_
            and bstack1l1111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᚝") in bstack1l1l1ll1l1l_opy_
            and bstack1l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦ᚞") in bstack1l1l1ll1l1l_opy_[bstack1l1111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ᚟")]
        )
    @staticmethod
    def bstack1l1111ll1ll_opy_(*args):
        return str(bstack1ll1l111l1l_opy_.bstack1l1ll111ll1_opy_(*args)).lower()
    @staticmethod
    def bstack1l1ll111ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1ll11ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1l11l1_opy_(driver):
        command_executor = getattr(driver, bstack1l1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᚠ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1111_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᚡ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1111_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᚢ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1111_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᚣ"), None)
        return hub_url
    def bstack1l1111lll1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᚤ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᚥ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1111_opy_ (u"ࠤࡢࡹࡷࡲࠢᚦ")):
                setattr(command_executor, bstack1l1111_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᚧ"), hub_url)
                result = True
        if result:
            self.bstack1l111l11ll1_opy_ = hub_url
            bstack1ll1l111l1l_opy_.bstack1lll11l1ll1_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111lllll1_opy_, hub_url)
            bstack1ll1l111l1l_opy_.bstack1lll11l1ll1_opy_(
                instance, bstack1ll1l111l1l_opy_.bstack1l11111l11l_opy_, bstack1ll1l111l1l_opy_.bstack1l1l1ll1lll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11lllllllll_opy_(bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_]):
        return bstack1l1111_opy_ (u"ࠦ࠿ࠨᚨ").join((bstack1lll111lll1_opy_(bstack1lll111llll_opy_[0]).name, bstack1lll1l1ll1l_opy_(bstack1lll111llll_opy_[1]).name))
    @staticmethod
    def bstack1l1lll1ll11_opy_(bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_], callback: Callable):
        bstack11llllllll1_opy_ = bstack1ll1l111l1l_opy_.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        if not bstack11llllllll1_opy_ in bstack1ll1l111l1l_opy_.bstack11ll11l111l_opy_:
            bstack1ll1l111l1l_opy_.bstack11ll11l111l_opy_[bstack11llllllll1_opy_] = []
        bstack1ll1l111l1l_opy_.bstack11ll11l111l_opy_[bstack11llllllll1_opy_].append(callback)
    def bstack1lll1ll111l_opy_(self, instance: bstack1lll1l1111l_opy_, method_name: str, bstack1lll11ll111_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᚩ")):
            return
        cmd = args[0] if method_name == bstack1l1111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᚪ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11ll11l1ll1_opy_ = bstack1l1111_opy_ (u"ࠢ࠻ࠤᚫ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᚬ") + bstack11ll11l1ll1_opy_, bstack1lll11ll111_opy_)
    def bstack1lll11l11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll1lll1ll_opy_, bstack11lllllll1l_opy_ = bstack1lll111llll_opy_
        bstack11llllllll1_opy_ = bstack1ll1l111l1l_opy_.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᚭ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᚮ"))
        if bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.QUIT:
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.PRE:
                bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll11ll11l_opy_.value)
                bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, EVENTS.bstack11ll11ll11l_opy_.value, bstack1ll1111lll_opy_)
                self.logger.debug(bstack1l1111_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᚯ").format(instance, method_name, bstack1lll1lll1ll_opy_, bstack11lllllll1l_opy_))
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST:
                bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll11l1l11_opy_.value)
                bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, EVENTS.bstack11ll11l1l11_opy_.value, bstack1ll1111lll_opy_)
        if bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_:
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST and not bstack1ll1l111l1l_opy_.bstack1l11l1111ll_opy_ in instance.data:
                session_id = getattr(target, bstack1l1111_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᚰ"), None)
                if session_id:
                    instance.data[bstack1ll1l111l1l_opy_.bstack1l11l1111ll_opy_] = session_id
        elif (
            bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_
            and bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args) == bstack1ll1l111l1l_opy_.bstack1l111l11111_opy_
        ):
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.PRE:
                hub_url = bstack1ll1l111l1l_opy_.bstack1l1l11l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1l111l1l_opy_.bstack1l111lllll1_opy_: hub_url,
                            bstack1ll1l111l1l_opy_.bstack1l11111l11l_opy_: bstack1ll1l111l1l_opy_.bstack1l1l1ll1lll_opy_(hub_url),
                            bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_: int(
                                os.environ.get(bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᚱ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l1ll1l1l_opy_ = bstack1ll1l111l1l_opy_.bstack1l1l1ll11ll_opy_(*args)
                bstack11ll11ll1l1_opy_ = bstack1l1l1ll1l1l_opy_.get(bstack1l1111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᚲ"), None) if bstack1l1l1ll1l1l_opy_ else None
                if isinstance(bstack11ll11ll1l1_opy_, dict):
                    instance.data[bstack1ll1l111l1l_opy_.bstack11ll11ll111_opy_] = copy.deepcopy(bstack11ll11ll1l1_opy_)
                    instance.data[bstack1ll1l111l1l_opy_.bstack1l11l111lll_opy_] = bstack11ll11ll1l1_opy_
            elif bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᚳ"), dict()).get(bstack1l1111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᚴ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1l111l1l_opy_.bstack1l11l1111ll_opy_: framework_session_id,
                                bstack1ll1l111l1l_opy_.bstack11ll11l11l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_
            and bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args) == bstack1ll1l111l1l_opy_.bstack11ll11ll1ll_opy_
            and bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST
        ):
            instance.data[bstack1ll1l111l1l_opy_.bstack11ll11l1l1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack11llllllll1_opy_ in bstack1ll1l111l1l_opy_.bstack11ll11l111l_opy_:
            bstack1l111111111_opy_ = None
            for callback in bstack1ll1l111l1l_opy_.bstack11ll11l111l_opy_[bstack11llllllll1_opy_]:
                try:
                    bstack11llllll111_opy_ = callback(self, target, exec, bstack1lll111llll_opy_, result, *args, **kwargs)
                    if bstack1l111111111_opy_ == None:
                        bstack1l111111111_opy_ = bstack11llllll111_opy_
                except Exception as e:
                    self.logger.error(bstack1l1111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᚵ") + str(e) + bstack1l1111_opy_ (u"ࠦࠧᚶ"))
                    traceback.print_exc()
            if bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.QUIT:
                if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.PRE:
                    bstack1ll1111lll_opy_ = bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, EVENTS.bstack11ll11ll11l_opy_.value)
                    if bstack1ll1111lll_opy_!=None:
                        bstack11ll111lll_opy_.end(EVENTS.bstack11ll11ll11l_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᚷ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᚸ"), True, None)
                if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST:
                    bstack1ll1111lll_opy_ = bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, EVENTS.bstack11ll11l1l11_opy_.value)
                    if bstack1ll1111lll_opy_!=None:
                        bstack11ll111lll_opy_.end(EVENTS.bstack11ll11l1l11_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᚹ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᚺ"), True, None)
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.PRE and callable(bstack1l111111111_opy_):
                return bstack1l111111111_opy_
            elif bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST and bstack1l111111111_opy_:
                return bstack1l111111111_opy_
    def bstack1lll1l1lll1_opy_(
        self, method_name, previous_state: bstack1lll111lll1_opy_, *args, **kwargs
    ) -> bstack1lll111lll1_opy_:
        if method_name == bstack1l1111_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᚻ") or method_name == bstack1l1111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᚼ"):
            return bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_
        if method_name == bstack1l1111_opy_ (u"ࠦࡶࡻࡩࡵࠤᚽ"):
            return bstack1lll111lll1_opy_.QUIT
        if method_name == bstack1l1111_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᚾ"):
            if previous_state != bstack1lll111lll1_opy_.NONE:
                command_name = bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args)
                if command_name == bstack1ll1l111l1l_opy_.bstack1l111l11111_opy_:
                    return bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_
            return bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_
        return bstack1lll111lll1_opy_.NONE