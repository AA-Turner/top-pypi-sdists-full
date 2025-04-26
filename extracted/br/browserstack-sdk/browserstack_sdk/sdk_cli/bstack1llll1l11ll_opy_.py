# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111l11l_opy_,
    bstack11111111ll_opy_,
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1lll1l1_opy_(bstack111111l11l_opy_):
    bstack1l11lllll11_opy_ = bstack1l11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᒶ")
    NAME = bstack1l11lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᒷ")
    bstack1l1ll11l1ll_opy_ = bstack1l11lll_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᒸ")
    bstack1l1ll111l1l_opy_ = bstack1l11lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᒹ")
    bstack1l111l11111_opy_ = bstack1l11lll_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᒺ")
    bstack1l1ll11llll_opy_ = bstack1l11lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒻ")
    bstack1l1l111l111_opy_ = bstack1l11lll_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᒼ")
    bstack1l1111ll111_opy_ = bstack1l11lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᒽ")
    bstack1l1111llll1_opy_ = bstack1l11lll_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᒾ")
    bstack1ll1l111lll_opy_ = bstack1l11lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᒿ")
    bstack1l1l1l11l11_opy_ = bstack1l11lll_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᓀ")
    bstack1l1111lll11_opy_ = bstack1l11lll_opy_ (u"ࠢࡨࡧࡷࠦᓁ")
    bstack1ll111l11l1_opy_ = bstack1l11lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᓂ")
    bstack1l1l11111l1_opy_ = bstack1l11lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᓃ")
    bstack1l1l1111111_opy_ = bstack1l11lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᓄ")
    bstack1l1111ll1l1_opy_ = bstack1l11lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᓅ")
    bstack1l1111lllll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11lll1l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1llll1l_opy_: Any
    bstack1l1l111111l_opy_: Dict
    def __init__(
        self,
        bstack1l1l11lll1l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1llll1l_opy_: Dict[str, Any],
        methods=[bstack1l11lll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᓆ"), bstack1l11lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᓇ"), bstack1l11lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᓈ"), bstack1l11lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᓉ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11lll1l_opy_ = bstack1l1l11lll1l_opy_
        self.platform_index = platform_index
        self.bstack11111l1l11_opy_(methods)
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack111111l11l_opy_.get_data(bstack1lll1lll1l1_opy_.bstack1l1ll111l1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack111111l11l_opy_.get_data(bstack1lll1lll1l1_opy_.bstack1l1ll11l1ll_opy_, target, strict)
    @staticmethod
    def bstack1l111l1111l_opy_(target: object, strict=True):
        return bstack111111l11l_opy_.get_data(bstack1lll1lll1l1_opy_.bstack1l111l11111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack111111l11l_opy_.get_data(bstack1lll1lll1l1_opy_.bstack1l1ll11llll_opy_, target, strict)
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(instance: bstack11111111ll_opy_) -> bool:
        return bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l111l111_opy_, False)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1ll11l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll1l11l111_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1ll11llll_opy_, default_value)
    @staticmethod
    def bstack1ll11lll111_opy_(hub_url: str, bstack1l1111ll11l_opy_=bstack1l11lll_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᓊ")):
        try:
            bstack1l1111lll1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111lll1l_opy_.endswith(bstack1l1111ll11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str):
        return method_name == bstack1l11lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓋ")
    @staticmethod
    def bstack1ll1l1ll11l_opy_(method_name: str, *args):
        return (
            bstack1lll1lll1l1_opy_.bstack1ll1l1ll1l1_opy_(method_name)
            and bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args) == bstack1lll1lll1l1_opy_.bstack1l1l1l11l11_opy_
        )
    @staticmethod
    def bstack1ll1ll11ll1_opy_(method_name: str, *args):
        if not bstack1lll1lll1l1_opy_.bstack1ll1l1ll1l1_opy_(method_name):
            return False
        if not bstack1lll1lll1l1_opy_.bstack1l1l11111l1_opy_ in bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1lll1lll1l1_opy_.bstack1ll11l1lll1_opy_(*args)
        return bstack1ll11ll1ll1_opy_ and bstack1l11lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓌ") in bstack1ll11ll1ll1_opy_ and bstack1l11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓍ") in bstack1ll11ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓎ")]
    @staticmethod
    def bstack1ll11lll1l1_opy_(method_name: str, *args):
        if not bstack1lll1lll1l1_opy_.bstack1ll1l1ll1l1_opy_(method_name):
            return False
        if not bstack1lll1lll1l1_opy_.bstack1l1l11111l1_opy_ in bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1lll1lll1l1_opy_.bstack1ll11l1lll1_opy_(*args)
        return (
            bstack1ll11ll1ll1_opy_
            and bstack1l11lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓏ") in bstack1ll11ll1ll1_opy_
            and bstack1l11lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᓐ") in bstack1ll11ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓑ")]
        )
    @staticmethod
    def bstack1l1l1l1l111_opy_(*args):
        return str(bstack1lll1lll1l1_opy_.bstack1ll1l111111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l1lll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll1llll_opy_(driver):
        command_executor = getattr(driver, bstack1l11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓒ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l11lll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓓ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l11lll_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᓔ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l11lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᓕ"), None)
        return hub_url
    def bstack1l1l11l111l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l11lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓖ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l11lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᓗ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l11lll_opy_ (u"ࠤࡢࡹࡷࡲࠢᓘ")):
                setattr(command_executor, bstack1l11lll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᓙ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11lll1l_opy_ = hub_url
            bstack1lll1lll1l1_opy_.bstack1111l111ll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1ll11l1ll_opy_, hub_url)
            bstack1lll1lll1l1_opy_.bstack1111l111ll_opy_(
                instance, bstack1lll1lll1l1_opy_.bstack1l1l111l111_opy_, bstack1lll1lll1l1_opy_.bstack1ll11lll111_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11lllllll_opy_(bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_]):
        return bstack1l11lll_opy_ (u"ࠦ࠿ࠨᓚ").join((bstack111111lll1_opy_(bstack11111l11ll_opy_[0]).name, bstack111111l1l1_opy_(bstack11111l11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l1l_opy_(bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_], callback: Callable):
        bstack1l11llll1ll_opy_ = bstack1lll1lll1l1_opy_.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        if not bstack1l11llll1ll_opy_ in bstack1lll1lll1l1_opy_.bstack1l1111lllll_opy_:
            bstack1lll1lll1l1_opy_.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_] = []
        bstack1lll1lll1l1_opy_.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_].append(callback)
    def bstack11111lll1l_opy_(self, instance: bstack11111111ll_opy_, method_name: str, bstack1lllllll11l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l11lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓛ")):
            return
        cmd = args[0] if method_name == bstack1l11lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓜ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111ll1ll_opy_ = bstack1l11lll_opy_ (u"ࠢ࠻ࠤᓝ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᓞ") + bstack1l1111ll1ll_opy_, bstack1lllllll11l_opy_)
    def bstack1llllllll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11l1l_opy_, bstack1l11lllll1l_opy_ = bstack11111l11ll_opy_
        bstack1l11llll1ll_opy_ = bstack1lll1lll1l1_opy_.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᓟ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠥࠦᓠ"))
        if bstack1111l11l1l_opy_ == bstack111111lll1_opy_.QUIT:
            if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.PRE:
                bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack11ll1111l1_opy_.value)
                bstack111111l11l_opy_.bstack1111l111ll_opy_(instance, EVENTS.bstack11ll1111l1_opy_.value, bstack1ll1ll1l111_opy_)
                self.logger.debug(bstack1l11lll_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᓡ").format(instance, method_name, bstack1111l11l1l_opy_, bstack1l11lllll1l_opy_))
        if bstack1111l11l1l_opy_ == bstack111111lll1_opy_.bstack111111l111_opy_:
            if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST and not bstack1lll1lll1l1_opy_.bstack1l1ll111l1l_opy_ in instance.data:
                session_id = getattr(target, bstack1l11lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᓢ"), None)
                if session_id:
                    instance.data[bstack1lll1lll1l1_opy_.bstack1l1ll111l1l_opy_] = session_id
        elif (
            bstack1111l11l1l_opy_ == bstack111111lll1_opy_.bstack1111l11ll1_opy_
            and bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args) == bstack1lll1lll1l1_opy_.bstack1l1l1l11l11_opy_
        ):
            if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.PRE:
                hub_url = bstack1lll1lll1l1_opy_.bstack1ll1llll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1lll1l1_opy_.bstack1l1ll11l1ll_opy_: hub_url,
                            bstack1lll1lll1l1_opy_.bstack1l1l111l111_opy_: bstack1lll1lll1l1_opy_.bstack1ll11lll111_opy_(hub_url),
                            bstack1lll1lll1l1_opy_.bstack1ll1l111lll_opy_: int(
                                os.environ.get(bstack1l11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᓣ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll1ll1_opy_ = bstack1lll1lll1l1_opy_.bstack1ll11l1lll1_opy_(*args)
                bstack1l111l1111l_opy_ = bstack1ll11ll1ll1_opy_.get(bstack1l11lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓤ"), None) if bstack1ll11ll1ll1_opy_ else None
                if isinstance(bstack1l111l1111l_opy_, dict):
                    instance.data[bstack1lll1lll1l1_opy_.bstack1l111l11111_opy_] = copy.deepcopy(bstack1l111l1111l_opy_)
                    instance.data[bstack1lll1lll1l1_opy_.bstack1l1ll11llll_opy_] = bstack1l111l1111l_opy_
            elif bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l11lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᓥ"), dict()).get(bstack1l11lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᓦ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1lll1l1_opy_.bstack1l1ll111l1l_opy_: framework_session_id,
                                bstack1lll1lll1l1_opy_.bstack1l1111ll111_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111l11l1l_opy_ == bstack111111lll1_opy_.bstack1111l11ll1_opy_
            and bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args) == bstack1lll1lll1l1_opy_.bstack1l1111ll1l1_opy_
            and bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST
        ):
            instance.data[bstack1lll1lll1l1_opy_.bstack1l1111llll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11llll1ll_opy_ in bstack1lll1lll1l1_opy_.bstack1l1111lllll_opy_:
            bstack1l11llll1l1_opy_ = None
            for callback in bstack1lll1lll1l1_opy_.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_]:
                try:
                    bstack1l11llllll1_opy_ = callback(self, target, exec, bstack11111l11ll_opy_, result, *args, **kwargs)
                    if bstack1l11llll1l1_opy_ == None:
                        bstack1l11llll1l1_opy_ = bstack1l11llllll1_opy_
                except Exception as e:
                    self.logger.error(bstack1l11lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᓧ") + str(e) + bstack1l11lll_opy_ (u"ࠦࠧᓨ"))
                    traceback.print_exc()
            if bstack1111l11l1l_opy_ == bstack111111lll1_opy_.QUIT:
                if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST:
                    bstack1ll1ll1l111_opy_ = bstack111111l11l_opy_.bstack1111111111_opy_(instance, EVENTS.bstack11ll1111l1_opy_.value)
                    if bstack1ll1ll1l111_opy_!=None:
                        bstack1ll1llll111_opy_.end(EVENTS.bstack11ll1111l1_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᓩ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᓪ"), True, None)
            if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.PRE and callable(bstack1l11llll1l1_opy_):
                return bstack1l11llll1l1_opy_
            elif bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST and bstack1l11llll1l1_opy_:
                return bstack1l11llll1l1_opy_
    def bstack11111l1l1l_opy_(
        self, method_name, previous_state: bstack111111lll1_opy_, *args, **kwargs
    ) -> bstack111111lll1_opy_:
        if method_name == bstack1l11lll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓫ") or method_name == bstack1l11lll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓬ"):
            return bstack111111lll1_opy_.bstack111111l111_opy_
        if method_name == bstack1l11lll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᓭ"):
            return bstack111111lll1_opy_.QUIT
        if method_name == bstack1l11lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓮ"):
            if previous_state != bstack111111lll1_opy_.NONE:
                bstack1ll11lll11l_opy_ = bstack1lll1lll1l1_opy_.bstack1l1l1l1l111_opy_(*args)
                if bstack1ll11lll11l_opy_ == bstack1lll1lll1l1_opy_.bstack1l1l1l11l11_opy_:
                    return bstack111111lll1_opy_.bstack111111l111_opy_
            return bstack111111lll1_opy_.bstack1111l11ll1_opy_
        return bstack111111lll1_opy_.NONE