# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import (
    bstack1lllllll11l_opy_,
    bstack111111ll11_opy_,
    bstack11111lll11_opy_,
    bstack1111111l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll11ll1ll_opy_(bstack1lllllll11l_opy_):
    bstack1l1l11111ll_opy_ = bstack1llllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᒸ")
    NAME = bstack1llllll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᒹ")
    bstack1l1ll111ll1_opy_ = bstack1llllll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᒺ")
    bstack1l1ll111lll_opy_ = bstack1llllll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᒻ")
    bstack1l111l1111l_opy_ = bstack1llllll_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒼ")
    bstack1l1ll111l1l_opy_ = bstack1llllll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᒽ")
    bstack1l1l111l111_opy_ = bstack1llllll_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᒾ")
    bstack1l1111ll111_opy_ = bstack1llllll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᒿ")
    bstack1l1111ll1l1_opy_ = bstack1llllll_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᓀ")
    bstack1ll11lll1l1_opy_ = bstack1llllll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᓁ")
    bstack1l1l1l11lll_opy_ = bstack1llllll_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓂ")
    bstack1l111l11111_opy_ = bstack1llllll_opy_ (u"ࠤࡪࡩࡹࠨᓃ")
    bstack1l1llll11l1_opy_ = bstack1llllll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᓄ")
    bstack1l1l1111111_opy_ = bstack1llllll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᓅ")
    bstack1l11llll1l1_opy_ = bstack1llllll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᓆ")
    bstack1l1111ll1ll_opy_ = bstack1llllll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᓇ")
    bstack1l1111lll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l111l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1l1ll1_opy_: Any
    bstack1l11llll1ll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l111l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll1l1ll1_opy_: Dict[str, Any],
        methods=[bstack1llllll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓈ"), bstack1llllll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓉ"), bstack1llllll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᓊ"), bstack1llllll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᓋ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l111l_opy_ = bstack1l1l11l111l_opy_
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
        self.bstack1llll1l1ll1_opy_ = bstack1llll1l1ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1lll11ll1ll_opy_.bstack1l1ll111lll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1lll11ll1ll_opy_.bstack1l1ll111ll1_opy_, target, strict)
    @staticmethod
    def bstack1l1111lll1l_opy_(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1lll11ll1ll_opy_.bstack1l111l1111l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1lll11ll1ll_opy_.bstack1l1ll111l1l_opy_, target, strict)
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(instance: bstack111111ll11_opy_) -> bool:
        return bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_, False)
    @staticmethod
    def bstack1ll1l1l1lll_opy_(instance: bstack111111ll11_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1ll111ll1_opy_, default_value)
    @staticmethod
    def bstack1ll11lllll1_opy_(instance: bstack111111ll11_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11ll11l1_opy_(hub_url: str, bstack1l1111ll11l_opy_=bstack1llllll_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᓌ")):
        try:
            bstack1l1111llll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111llll1_opy_.endswith(bstack1l1111ll11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1ll111_opy_(method_name: str):
        return method_name == bstack1llllll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓍ")
    @staticmethod
    def bstack1ll11lll1ll_opy_(method_name: str, *args):
        return (
            bstack1lll11ll1ll_opy_.bstack1ll1l1ll111_opy_(method_name)
            and bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args) == bstack1lll11ll1ll_opy_.bstack1l1l1l11lll_opy_
        )
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1lll11ll1ll_opy_.bstack1ll1l1ll111_opy_(method_name):
            return False
        if not bstack1lll11ll1ll_opy_.bstack1l1l1111111_opy_ in bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11ll111l_opy_ = bstack1lll11ll1ll_opy_.bstack1ll11ll1lll_opy_(*args)
        return bstack1ll11ll111l_opy_ and bstack1llllll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓎ") in bstack1ll11ll111l_opy_ and bstack1llllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓏ") in bstack1ll11ll111l_opy_[bstack1llllll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓐ")]
    @staticmethod
    def bstack1ll1l1l111l_opy_(method_name: str, *args):
        if not bstack1lll11ll1ll_opy_.bstack1ll1l1ll111_opy_(method_name):
            return False
        if not bstack1lll11ll1ll_opy_.bstack1l1l1111111_opy_ in bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11ll111l_opy_ = bstack1lll11ll1ll_opy_.bstack1ll11ll1lll_opy_(*args)
        return (
            bstack1ll11ll111l_opy_
            and bstack1llllll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓑ") in bstack1ll11ll111l_opy_
            and bstack1llllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᓒ") in bstack1ll11ll111l_opy_[bstack1llllll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓓ")]
        )
    @staticmethod
    def bstack1l1l11l1l1l_opy_(*args):
        return str(bstack1lll11ll1ll_opy_.bstack1ll1ll1111l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1ll1111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll1lll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1l1ll11_opy_(driver):
        command_executor = getattr(driver, bstack1llllll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓔ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1llllll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᓕ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1llllll_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᓖ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1llllll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᓗ"), None)
        return hub_url
    def bstack1l1l1l11ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1llllll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓘ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1llllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓙ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1llllll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓚ")):
                setattr(command_executor, bstack1llllll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᓛ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l111l_opy_ = hub_url
            bstack1lll11ll1ll_opy_.bstack1111l11lll_opy_(instance, bstack1lll11ll1ll_opy_.bstack1l1ll111ll1_opy_, hub_url)
            bstack1lll11ll1ll_opy_.bstack1111l11lll_opy_(
                instance, bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_, bstack1lll11ll1ll_opy_.bstack1ll11ll11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l11111l1_opy_(bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_]):
        return bstack1llllll_opy_ (u"ࠨ࠺ࠣᓜ").join((bstack11111lll11_opy_(bstack1111111lll_opy_[0]).name, bstack1111111l1l_opy_(bstack1111111lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111l1l_opy_(bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = bstack1lll11ll1ll_opy_.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        if not bstack1l11llllll1_opy_ in bstack1lll11ll1ll_opy_.bstack1l1111lll11_opy_:
            bstack1lll11ll1ll_opy_.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_] = []
        bstack1lll11ll1ll_opy_.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_].append(callback)
    def bstack1111111ll1_opy_(self, instance: bstack111111ll11_opy_, method_name: str, bstack11111ll111_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1llllll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓝ")):
            return
        cmd = args[0] if method_name == bstack1llllll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᓞ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111lllll_opy_ = bstack1llllll_opy_ (u"ࠤ࠽ࠦᓟ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᓠ") + bstack1l1111lllll_opy_, bstack11111ll111_opy_)
    def bstack111111ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l1111l_opy_, bstack1l11lllll11_opy_ = bstack1111111lll_opy_
        bstack1l11llllll1_opy_ = bstack1lll11ll1ll_opy_.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓡ") + str(kwargs) + bstack1llllll_opy_ (u"ࠧࠨᓢ"))
        if bstack1111l1111l_opy_ == bstack11111lll11_opy_.QUIT:
            if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.PRE:
                bstack1ll1ll111l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack1ll111ll1_opy_.value)
                bstack1lllllll11l_opy_.bstack1111l11lll_opy_(instance, EVENTS.bstack1ll111ll1_opy_.value, bstack1ll1ll111l1_opy_)
                self.logger.debug(bstack1llllll_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᓣ").format(instance, method_name, bstack1111l1111l_opy_, bstack1l11lllll11_opy_))
        if bstack1111l1111l_opy_ == bstack11111lll11_opy_.bstack1111111l11_opy_:
            if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST and not bstack1lll11ll1ll_opy_.bstack1l1ll111lll_opy_ in instance.data:
                session_id = getattr(target, bstack1llllll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᓤ"), None)
                if session_id:
                    instance.data[bstack1lll11ll1ll_opy_.bstack1l1ll111lll_opy_] = session_id
        elif (
            bstack1111l1111l_opy_ == bstack11111lll11_opy_.bstack11111l111l_opy_
            and bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args) == bstack1lll11ll1ll_opy_.bstack1l1l1l11lll_opy_
        ):
            if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.PRE:
                hub_url = bstack1lll11ll1ll_opy_.bstack1l1l1ll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll11ll1ll_opy_.bstack1l1ll111ll1_opy_: hub_url,
                            bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_: bstack1lll11ll1ll_opy_.bstack1ll11ll11l1_opy_(hub_url),
                            bstack1lll11ll1ll_opy_.bstack1ll11lll1l1_opy_: int(
                                os.environ.get(bstack1llllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᓥ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll111l_opy_ = bstack1lll11ll1ll_opy_.bstack1ll11ll1lll_opy_(*args)
                bstack1l1111lll1l_opy_ = bstack1ll11ll111l_opy_.get(bstack1llllll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓦ"), None) if bstack1ll11ll111l_opy_ else None
                if isinstance(bstack1l1111lll1l_opy_, dict):
                    instance.data[bstack1lll11ll1ll_opy_.bstack1l111l1111l_opy_] = copy.deepcopy(bstack1l1111lll1l_opy_)
                    instance.data[bstack1lll11ll1ll_opy_.bstack1l1ll111l1l_opy_] = bstack1l1111lll1l_opy_
            elif bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1llllll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᓧ"), dict()).get(bstack1llllll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᓨ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll11ll1ll_opy_.bstack1l1ll111lll_opy_: framework_session_id,
                                bstack1lll11ll1ll_opy_.bstack1l1111ll111_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111l1111l_opy_ == bstack11111lll11_opy_.bstack11111l111l_opy_
            and bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args) == bstack1lll11ll1ll_opy_.bstack1l1111ll1ll_opy_
            and bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST
        ):
            instance.data[bstack1lll11ll1ll_opy_.bstack1l1111ll1l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11llllll1_opy_ in bstack1lll11ll1ll_opy_.bstack1l1111lll11_opy_:
            bstack1l11lllll1l_opy_ = None
            for callback in bstack1lll11ll1ll_opy_.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_]:
                try:
                    bstack1l11lllllll_opy_ = callback(self, target, exec, bstack1111111lll_opy_, result, *args, **kwargs)
                    if bstack1l11lllll1l_opy_ == None:
                        bstack1l11lllll1l_opy_ = bstack1l11lllllll_opy_
                except Exception as e:
                    self.logger.error(bstack1llllll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᓩ") + str(e) + bstack1llllll_opy_ (u"ࠨࠢᓪ"))
                    traceback.print_exc()
            if bstack1111l1111l_opy_ == bstack11111lll11_opy_.QUIT:
                if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST:
                    bstack1ll1ll111l1_opy_ = bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, EVENTS.bstack1ll111ll1_opy_.value)
                    if bstack1ll1ll111l1_opy_!=None:
                        bstack1lll1llll1l_opy_.end(EVENTS.bstack1ll111ll1_opy_.value, bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᓫ"), bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᓬ"), True, None)
            if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.PRE and callable(bstack1l11lllll1l_opy_):
                return bstack1l11lllll1l_opy_
            elif bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST and bstack1l11lllll1l_opy_:
                return bstack1l11lllll1l_opy_
    def bstack1llllllll1l_opy_(
        self, method_name, previous_state: bstack11111lll11_opy_, *args, **kwargs
    ) -> bstack11111lll11_opy_:
        if method_name == bstack1llllll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᓭ") or method_name == bstack1llllll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᓮ"):
            return bstack11111lll11_opy_.bstack1111111l11_opy_
        if method_name == bstack1llllll_opy_ (u"ࠦࡶࡻࡩࡵࠤᓯ"):
            return bstack11111lll11_opy_.QUIT
        if method_name == bstack1llllll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓰ"):
            if previous_state != bstack11111lll11_opy_.NONE:
                bstack1ll1l1lll1l_opy_ = bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args)
                if bstack1ll1l1lll1l_opy_ == bstack1lll11ll1ll_opy_.bstack1l1l1l11lll_opy_:
                    return bstack11111lll11_opy_.bstack1111111l11_opy_
            return bstack11111lll11_opy_.bstack11111l111l_opy_
        return bstack11111lll11_opy_.NONE