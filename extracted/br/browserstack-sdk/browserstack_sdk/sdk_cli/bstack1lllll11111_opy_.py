# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import (
    bstack111111ll11_opy_,
    bstack11111ll111_opy_,
    bstack1llllllllll_opy_,
    bstack11111lll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import EVENTS
class bstack1lll11lllll_opy_(bstack111111ll11_opy_):
    bstack1l1l1111111_opy_ = bstack1l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᒽ")
    NAME = bstack1l1lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᒾ")
    bstack1l1ll11l111_opy_ = bstack1l1lll_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᒿ")
    bstack1l1ll11ll1l_opy_ = bstack1l1lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᓀ")
    bstack1l1111ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᓁ")
    bstack1l1ll11ll11_opy_ = bstack1l1lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᓂ")
    bstack1l1l111l1l1_opy_ = bstack1l1lll_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᓃ")
    bstack1l1111lll11_opy_ = bstack1l1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᓄ")
    bstack1l111l11111_opy_ = bstack1l1lll_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᓅ")
    bstack1ll1l1lllll_opy_ = bstack1l1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᓆ")
    bstack1l1l1l11111_opy_ = bstack1l1lll_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᓇ")
    bstack1l1111lllll_opy_ = bstack1l1lll_opy_ (u"ࠢࡨࡧࡷࠦᓈ")
    bstack1l1llll1ll1_opy_ = bstack1l1lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᓉ")
    bstack1l11llll1l1_opy_ = bstack1l1lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᓊ")
    bstack1l11llllll1_opy_ = bstack1l1lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᓋ")
    bstack1l1111ll1l1_opy_ = bstack1l1lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᓌ")
    bstack1l1111lll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11ll111_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll111l11_opy_: Any
    bstack1l1l11111ll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11ll111_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll111l11_opy_: Dict[str, Any],
        methods=[bstack1l1lll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᓍ"), bstack1l1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᓎ"), bstack1l1lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᓏ"), bstack1l1lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᓐ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11ll111_opy_ = bstack1l1l11ll111_opy_
        self.platform_index = platform_index
        self.bstack11111ll1ll_opy_(methods)
        self.bstack1llll111l11_opy_ = bstack1llll111l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack111111ll11_opy_.get_data(bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack111111ll11_opy_.get_data(bstack1lll11lllll_opy_.bstack1l1ll11l111_opy_, target, strict)
    @staticmethod
    def bstack1l111l1111l_opy_(target: object, strict=True):
        return bstack111111ll11_opy_.get_data(bstack1lll11lllll_opy_.bstack1l1111ll1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack111111ll11_opy_.get_data(bstack1lll11lllll_opy_.bstack1l1ll11ll11_opy_, target, strict)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack11111ll111_opy_) -> bool:
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l111l1l1_opy_, False)
    @staticmethod
    def bstack1ll1l1llll1_opy_(instance: bstack11111ll111_opy_, default_value=None):
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, bstack1lll11lllll_opy_.bstack1l1ll11l111_opy_, default_value)
    @staticmethod
    def bstack1ll1l1lll1l_opy_(instance: bstack11111ll111_opy_, default_value=None):
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, bstack1lll11lllll_opy_.bstack1l1ll11ll11_opy_, default_value)
    @staticmethod
    def bstack1ll11ll11l1_opy_(hub_url: str, bstack1l1111ll111_opy_=bstack1l1lll_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᓑ")):
        try:
            bstack1l1111llll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111llll1_opy_.endswith(bstack1l1111ll111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1ll11111_opy_(method_name: str):
        return method_name == bstack1l1lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓒ")
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(method_name: str, *args):
        return (
            bstack1lll11lllll_opy_.bstack1ll1ll11111_opy_(method_name)
            and bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args) == bstack1lll11lllll_opy_.bstack1l1l1l11111_opy_
        )
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1lll11lllll_opy_.bstack1ll1ll11111_opy_(method_name):
            return False
        if not bstack1lll11lllll_opy_.bstack1l11llll1l1_opy_ in bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1lll11lllll_opy_.bstack1ll11ll1ll1_opy_(*args)
        return bstack1ll11l1lll1_opy_ and bstack1l1lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓓ") in bstack1ll11l1lll1_opy_ and bstack1l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓔ") in bstack1ll11l1lll1_opy_[bstack1l1lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓕ")]
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args):
        if not bstack1lll11lllll_opy_.bstack1ll1ll11111_opy_(method_name):
            return False
        if not bstack1lll11lllll_opy_.bstack1l11llll1l1_opy_ in bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1lll11lllll_opy_.bstack1ll11ll1ll1_opy_(*args)
        return (
            bstack1ll11l1lll1_opy_
            and bstack1l1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓖ") in bstack1ll11l1lll1_opy_
            and bstack1l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᓗ") in bstack1ll11l1lll1_opy_[bstack1l1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓘ")]
        )
    @staticmethod
    def bstack1l1l11l11l1_opy_(*args):
        return str(bstack1lll11lllll_opy_.bstack1ll1l111lll_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll1ll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1ll1llll_opy_(driver):
        command_executor = getattr(driver, bstack1l1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓙ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1lll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓚ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1lll_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᓛ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᓜ"), None)
        return hub_url
    def bstack1l1l1l1l111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓝ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᓞ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1lll_opy_ (u"ࠤࡢࡹࡷࡲࠢᓟ")):
                setattr(command_executor, bstack1l1lll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᓠ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11ll111_opy_ = hub_url
            bstack1lll11lllll_opy_.bstack1111l11l1l_opy_(instance, bstack1lll11lllll_opy_.bstack1l1ll11l111_opy_, hub_url)
            bstack1lll11lllll_opy_.bstack1111l11l1l_opy_(
                instance, bstack1lll11lllll_opy_.bstack1l1l111l1l1_opy_, bstack1lll11lllll_opy_.bstack1ll11ll11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_]):
        return bstack1l1lll_opy_ (u"ࠦ࠿ࠨᓡ").join((bstack1llllllllll_opy_(bstack1lllllll1l1_opy_[0]).name, bstack11111lll1l_opy_(bstack1lllllll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1l111_opy_(bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_], callback: Callable):
        bstack1l11lllll1l_opy_ = bstack1lll11lllll_opy_.bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_)
        if not bstack1l11lllll1l_opy_ in bstack1lll11lllll_opy_.bstack1l1111lll1l_opy_:
            bstack1lll11lllll_opy_.bstack1l1111lll1l_opy_[bstack1l11lllll1l_opy_] = []
        bstack1lll11lllll_opy_.bstack1l1111lll1l_opy_[bstack1l11lllll1l_opy_].append(callback)
    def bstack11111lll11_opy_(self, instance: bstack11111ll111_opy_, method_name: str, bstack1lllllll1ll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓢ")):
            return
        cmd = args[0] if method_name == bstack1l1lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓣ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111ll11l_opy_ = bstack1l1lll_opy_ (u"ࠢ࠻ࠤᓤ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᓥ") + bstack1l1111ll11l_opy_, bstack1lllllll1ll_opy_)
    def bstack111111l1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111llll1_opy_, bstack1l11lllll11_opy_ = bstack1lllllll1l1_opy_
        bstack1l11lllll1l_opy_ = bstack1lll11lllll_opy_.bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_)
        self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᓦ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠥࠦᓧ"))
        if bstack11111llll1_opy_ == bstack1llllllllll_opy_.QUIT:
            if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.PRE:
                bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1l11lll1ll_opy_.value)
                bstack111111ll11_opy_.bstack1111l11l1l_opy_(instance, EVENTS.bstack1l11lll1ll_opy_.value, bstack1ll1l11lll1_opy_)
                self.logger.debug(bstack1l1lll_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᓨ").format(instance, method_name, bstack11111llll1_opy_, bstack1l11lllll11_opy_))
        if bstack11111llll1_opy_ == bstack1llllllllll_opy_.bstack1111l11lll_opy_:
            if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST and not bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_ in instance.data:
                session_id = getattr(target, bstack1l1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᓩ"), None)
                if session_id:
                    instance.data[bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_] = session_id
        elif (
            bstack11111llll1_opy_ == bstack1llllllllll_opy_.bstack1111l11111_opy_
            and bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args) == bstack1lll11lllll_opy_.bstack1l1l1l11111_opy_
        ):
            if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.PRE:
                hub_url = bstack1lll11lllll_opy_.bstack1l1ll1llll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll11lllll_opy_.bstack1l1ll11l111_opy_: hub_url,
                            bstack1lll11lllll_opy_.bstack1l1l111l1l1_opy_: bstack1lll11lllll_opy_.bstack1ll11ll11l1_opy_(hub_url),
                            bstack1lll11lllll_opy_.bstack1ll1l1lllll_opy_: int(
                                os.environ.get(bstack1l1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᓪ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l1lll1_opy_ = bstack1lll11lllll_opy_.bstack1ll11ll1ll1_opy_(*args)
                bstack1l111l1111l_opy_ = bstack1ll11l1lll1_opy_.get(bstack1l1lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓫ"), None) if bstack1ll11l1lll1_opy_ else None
                if isinstance(bstack1l111l1111l_opy_, dict):
                    instance.data[bstack1lll11lllll_opy_.bstack1l1111ll1ll_opy_] = copy.deepcopy(bstack1l111l1111l_opy_)
                    instance.data[bstack1lll11lllll_opy_.bstack1l1ll11ll11_opy_] = bstack1l111l1111l_opy_
            elif bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᓬ"), dict()).get(bstack1l1lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᓭ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_: framework_session_id,
                                bstack1lll11lllll_opy_.bstack1l1111lll11_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111llll1_opy_ == bstack1llllllllll_opy_.bstack1111l11111_opy_
            and bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args) == bstack1lll11lllll_opy_.bstack1l1111ll1l1_opy_
            and bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST
        ):
            instance.data[bstack1lll11lllll_opy_.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11lllll1l_opy_ in bstack1lll11lllll_opy_.bstack1l1111lll1l_opy_:
            bstack1l11lllllll_opy_ = None
            for callback in bstack1lll11lllll_opy_.bstack1l1111lll1l_opy_[bstack1l11lllll1l_opy_]:
                try:
                    bstack1l1l111111l_opy_ = callback(self, target, exec, bstack1lllllll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11lllllll_opy_ == None:
                        bstack1l11lllllll_opy_ = bstack1l1l111111l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᓮ") + str(e) + bstack1l1lll_opy_ (u"ࠦࠧᓯ"))
                    traceback.print_exc()
            if bstack11111llll1_opy_ == bstack1llllllllll_opy_.QUIT:
                if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST:
                    bstack1ll1l11lll1_opy_ = bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, EVENTS.bstack1l11lll1ll_opy_.value)
                    if bstack1ll1l11lll1_opy_!=None:
                        bstack1lll1lll111_opy_.end(EVENTS.bstack1l11lll1ll_opy_.value, bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᓰ"), bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᓱ"), True, None)
            if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.PRE and callable(bstack1l11lllllll_opy_):
                return bstack1l11lllllll_opy_
            elif bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST and bstack1l11lllllll_opy_:
                return bstack1l11lllllll_opy_
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        if method_name == bstack1l1lll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓲ") or method_name == bstack1l1lll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓳ"):
            return bstack1llllllllll_opy_.bstack1111l11lll_opy_
        if method_name == bstack1l1lll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᓴ"):
            return bstack1llllllllll_opy_.QUIT
        if method_name == bstack1l1lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓵ"):
            if previous_state != bstack1llllllllll_opy_.NONE:
                bstack1ll1l11l111_opy_ = bstack1lll11lllll_opy_.bstack1l1l11l11l1_opy_(*args)
                if bstack1ll1l11l111_opy_ == bstack1lll11lllll_opy_.bstack1l1l1l11111_opy_:
                    return bstack1llllllllll_opy_.bstack1111l11lll_opy_
            return bstack1llllllllll_opy_.bstack1111l11111_opy_
        return bstack1llllllllll_opy_.NONE