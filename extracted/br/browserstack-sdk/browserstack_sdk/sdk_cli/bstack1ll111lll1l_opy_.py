# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1lll1111l11_opy_,
    bstack1ll1llll11l_opy_,
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll11l11l11_opy_(bstack1lll1111l11_opy_):
    bstack11ll1lll1l1_opy_ = bstack1lll1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᢅ")
    NAME = bstack1lll1l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᢆ")
    bstack1lll1l11ll1_opy_ = bstack1lll1l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᢇ")
    bstack1lll1111ll1_opy_ = bstack1lll1l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᢈ")
    bstack11l1l11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᢉ")
    bstack1lll11ll1l1_opy_ = bstack1lll1l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᢊ")
    bstack11lll11l11l_opy_ = bstack1lll1l_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᢋ")
    bstack11l1l11l1l1_opy_ = bstack1lll1l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᢌ")
    bstack11l1l111lll_opy_ = bstack1lll1l_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᢍ")
    bstack1l1l1lll111_opy_ = bstack1lll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᢎ")
    bstack11llll1l11l_opy_ = bstack1lll1l_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᢏ")
    bstack11l1l11lll1_opy_ = bstack1lll1l_opy_ (u"ࠤࡪࡩࡹࠨᢐ")
    bstack1l11l1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᢑ")
    bstack11ll1ll1ll1_opy_ = bstack1lll1l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᢒ")
    bstack11ll1ll11l1_opy_ = bstack1lll1l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᢓ")
    bstack11l1l11llll_opy_ = bstack1lll1l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᢔ")
    bstack11l1l11l111_opy_: Dict[str, List[Callable]] = dict()
    bstack11lll1lllll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll111l1ll1_opy_: Any
    bstack11ll1lll111_opy_: Dict
    def __init__(
        self,
        bstack11lll1lllll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll111l1ll1_opy_: Dict[str, Any],
        methods=[bstack1lll1l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᢕ"), bstack1lll1l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᢖ"), bstack1lll1l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᢗ"), bstack1lll1l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᢘ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11lll1lllll_opy_ = bstack11lll1lllll_opy_
        self.platform_index = platform_index
        self.bstack1ll1l1l1111_opy_(methods)
        self.bstack1ll111l1ll1_opy_ = bstack1ll111l1ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll1111l11_opy_.get_data(bstack1ll11l11l11_opy_.bstack1lll1111ll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll1111l11_opy_.get_data(bstack1ll11l11l11_opy_.bstack1lll1l11ll1_opy_, target, strict)
    @staticmethod
    def bstack11l1l111l11_opy_(target: object, strict=True):
        return bstack1lll1111l11_opy_.get_data(bstack1ll11l11l11_opy_.bstack11l1l11ll1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll1111l11_opy_.get_data(bstack1ll11l11l11_opy_.bstack1lll11ll1l1_opy_, target, strict)
    @staticmethod
    def bstack1l11lll111l_opy_(instance: bstack1ll1llll11l_opy_) -> bool:
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack11lll11l11l_opy_, False)
    @staticmethod
    def bstack1l1l1lllll1_opy_(instance: bstack1ll1llll11l_opy_, default_value=None):
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1lll1l11ll1_opy_, default_value)
    @staticmethod
    def bstack1l1l11l1111_opy_(instance: bstack1ll1llll11l_opy_, default_value=None):
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1lll11ll1l1_opy_, default_value)
    @staticmethod
    def bstack1l1l111111l_opy_(hub_url: str, bstack11l1l11ll11_opy_=bstack1lll1l_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᢙ")):
        try:
            bstack11l1l111ll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1l111ll1_opy_.endswith(bstack11l1l11ll11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l11lllll_opy_(method_name: str):
        return method_name == bstack1lll1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᢚ")
    @staticmethod
    def bstack1l1l1ll1l11_opy_(method_name: str, *args):
        return (
            bstack1ll11l11l11_opy_.bstack1l1l11lllll_opy_(method_name)
            and bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args) == bstack1ll11l11l11_opy_.bstack11llll1l11l_opy_
        )
    @staticmethod
    def bstack1l1l11lll1l_opy_(method_name: str, *args):
        if not bstack1ll11l11l11_opy_.bstack1l1l11lllll_opy_(method_name):
            return False
        if not bstack1ll11l11l11_opy_.bstack11ll1ll1ll1_opy_ in bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1ll11l11l11_opy_.bstack1l11llll1ll_opy_(*args)
        return bstack1l11lllllll_opy_ and bstack1lll1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᢛ") in bstack1l11lllllll_opy_ and bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᢜ") in bstack1l11lllllll_opy_[bstack1lll1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᢝ")]
    @staticmethod
    def bstack1l1l1l1l1ll_opy_(method_name: str, *args):
        if not bstack1ll11l11l11_opy_.bstack1l1l11lllll_opy_(method_name):
            return False
        if not bstack1ll11l11l11_opy_.bstack11ll1ll1ll1_opy_ in bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1ll11l11l11_opy_.bstack1l11llll1ll_opy_(*args)
        return (
            bstack1l11lllllll_opy_
            and bstack1lll1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᢞ") in bstack1l11lllllll_opy_
            and bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᢟ") in bstack1l11lllllll_opy_[bstack1lll1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᢠ")]
        )
    @staticmethod
    def bstack11lll1lll11_opy_(*args):
        return str(bstack1ll11l11l11_opy_.bstack1l1l1llll1l_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l1llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11llll1ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11lll1l1_opy_(driver):
        command_executor = getattr(driver, bstack1lll1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᢡ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1lll1l_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᢢ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1lll1l_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᢣ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1lll1l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᢤ"), None)
        return hub_url
    def bstack11lll1l1111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1lll1l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᢥ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᢦ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1lll1l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᢧ")):
                setattr(command_executor, bstack1lll1l_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᢨ"), hub_url)
                result = True
        if result:
            self.bstack11lll1lllll_opy_ = hub_url
            bstack1ll11l11l11_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll11l11l11_opy_.bstack1lll1l11ll1_opy_, hub_url)
            bstack1ll11l11l11_opy_.bstack1lll1l11lll_opy_(
                instance, bstack1ll11l11l11_opy_.bstack11lll11l11l_opy_, bstack1ll11l11l11_opy_.bstack1l1l111111l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_]):
        return bstack1lll1l_opy_ (u"ࠨ࠺ᢩࠣ").join((bstack1ll1l1l11ll_opy_(bstack1ll1ll1ll1l_opy_[0]).name, bstack1ll1llll111_opy_(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll1ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_], callback: Callable):
        bstack11ll1lll1ll_opy_ = bstack1ll11l11l11_opy_.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1lll1ll_opy_ in bstack1ll11l11l11_opy_.bstack11l1l11l111_opy_:
            bstack1ll11l11l11_opy_.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_] = []
        bstack1ll11l11l11_opy_.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_].append(callback)
    def bstack1ll1ll11111_opy_(self, instance: bstack1ll1llll11l_opy_, method_name: str, bstack1ll1l1l1l11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᢪ")):
            return
        cmd = args[0] if method_name == bstack1lll1l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤ᢫") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1l11l11l_opy_ = bstack1lll1l_opy_ (u"ࠤ࠽ࠦ᢬").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦ᢭") + bstack11l1l11l11l_opy_, bstack1ll1l1l1l11_opy_)
    def bstack1ll1l1lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1ll1ll11_opy_, bstack11ll1ll1l1l_opy_ = bstack1ll1ll1ll1l_opy_
        bstack11ll1lll1ll_opy_ = bstack1ll11l11l11_opy_.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᢮") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨ᢯"))
        if bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.QUIT:
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.PRE:
                bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1l11l1ll_opy_.value)
                bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, EVENTS.bstack11l1l11l1ll_opy_.value, bstack1ll111111l_opy_)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᢰ").format(instance, method_name, bstack1ll1ll1ll11_opy_, bstack11ll1ll1l1l_opy_))
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST:
                bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1l111l1l_opy_.value)
                bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, EVENTS.bstack11l1l111l1l_opy_.value, bstack1ll111111l_opy_)
        if bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_:
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST and not bstack1ll11l11l11_opy_.bstack1lll1111ll1_opy_ in instance.data:
                session_id = getattr(target, bstack1lll1l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᢱ"), None)
                if session_id:
                    instance.data[bstack1ll11l11l11_opy_.bstack1lll1111ll1_opy_] = session_id
        elif (
            bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_
            and bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args) == bstack1ll11l11l11_opy_.bstack11llll1l11l_opy_
        ):
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.PRE:
                hub_url = bstack1ll11l11l11_opy_.bstack11lll1l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll11l11l11_opy_.bstack1lll1l11ll1_opy_: hub_url,
                            bstack1ll11l11l11_opy_.bstack11lll11l11l_opy_: bstack1ll11l11l11_opy_.bstack1l1l111111l_opy_(hub_url),
                            bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_: int(
                                os.environ.get(bstack1lll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᢲ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11lllllll_opy_ = bstack1ll11l11l11_opy_.bstack1l11llll1ll_opy_(*args)
                bstack11l1l111l11_opy_ = bstack1l11lllllll_opy_.get(bstack1lll1l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᢳ"), None) if bstack1l11lllllll_opy_ else None
                if isinstance(bstack11l1l111l11_opy_, dict):
                    instance.data[bstack1ll11l11l11_opy_.bstack11l1l11ll1l_opy_] = copy.deepcopy(bstack11l1l111l11_opy_)
                    instance.data[bstack1ll11l11l11_opy_.bstack1lll11ll1l1_opy_] = bstack11l1l111l11_opy_
            elif bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1lll1l_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᢴ"), dict()).get(bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᢵ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll11l11l11_opy_.bstack1lll1111ll1_opy_: framework_session_id,
                                bstack1ll11l11l11_opy_.bstack11l1l11l1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_
            and bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args) == bstack1ll11l11l11_opy_.bstack11l1l11llll_opy_
            and bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST
        ):
            instance.data[bstack1ll11l11l11_opy_.bstack11l1l111lll_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll1lll1ll_opy_ in bstack1ll11l11l11_opy_.bstack11l1l11l111_opy_:
            bstack11ll1ll1l11_opy_ = None
            for callback in bstack1ll11l11l11_opy_.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_]:
                try:
                    bstack11ll1ll11ll_opy_ = callback(self, target, exec, bstack1ll1ll1ll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1ll1l11_opy_ == None:
                        bstack11ll1ll1l11_opy_ = bstack11ll1ll11ll_opy_
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᢶ") + str(e) + bstack1lll1l_opy_ (u"ࠨࠢᢷ"))
                    traceback.print_exc()
            if bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.QUIT:
                if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.PRE:
                    bstack1ll111111l_opy_ = bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, EVENTS.bstack11l1l11l1ll_opy_.value)
                    if bstack1ll111111l_opy_!=None:
                        bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1l11l1ll_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᢸ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᢹ"), True, None)
                if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST:
                    bstack1ll111111l_opy_ = bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, EVENTS.bstack11l1l111l1l_opy_.value)
                    if bstack1ll111111l_opy_!=None:
                        bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1l111l1l_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᢺ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᢻ"), True, None)
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.PRE and callable(bstack11ll1ll1l11_opy_):
                return bstack11ll1ll1l11_opy_
            elif bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST and bstack11ll1ll1l11_opy_:
                return bstack11ll1ll1l11_opy_
    def bstack1ll1lll1ll1_opy_(
        self, method_name, previous_state: bstack1ll1l1l11ll_opy_, *args, **kwargs
    ) -> bstack1ll1l1l11ll_opy_:
        if method_name == bstack1lll1l_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᢼ") or method_name == bstack1lll1l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᢽ"):
            return bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_
        if method_name == bstack1lll1l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᢾ"):
            return bstack1ll1l1l11ll_opy_.QUIT
        if method_name == bstack1lll1l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᢿ"):
            if previous_state != bstack1ll1l1l11ll_opy_.NONE:
                command_name = bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args)
                if command_name == bstack1ll11l11l11_opy_.bstack11llll1l11l_opy_:
                    return bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_
            return bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_
        return bstack1ll1l1l11ll_opy_.NONE