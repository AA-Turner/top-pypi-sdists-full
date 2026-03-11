# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1l111l_opy_,
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from bstack_utils.constants import EVENTS
class bstack1ll11lll111_opy_(bstack1ll1lllllll_opy_):
    bstack11ll1l111l1_opy_ = bstack1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᣮ")
    NAME = bstack1ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᣯ")
    bstack1lll111l1ll_opy_ = bstack1ll111_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᣰ")
    bstack1ll1lll111l_opy_ = bstack1ll111_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᣱ")
    bstack11l11ll11l1_opy_ = bstack1ll111_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᣲ")
    bstack1ll1lll1l1l_opy_ = bstack1ll111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᣳ")
    bstack11ll1ll1ll1_opy_ = bstack1ll111_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᣴ")
    bstack11l11lll111_opy_ = bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᣵ")
    bstack11l11ll1lll_opy_ = bstack1ll111_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣ᣶")
    bstack1l1l1l1ll11_opy_ = bstack1ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣ᣷")
    bstack11ll1ll1lll_opy_ = bstack1ll111_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᣸")
    bstack11l11ll1l11_opy_ = bstack1ll111_opy_ (u"ࠤࡪࡩࡹࠨ᣹")
    bstack1l11l11ll11_opy_ = bstack1ll111_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᣺")
    bstack11ll1l11lll_opy_ = bstack1ll111_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢ᣻")
    bstack11ll1l111ll_opy_ = bstack1ll111_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨ᣼")
    bstack11l11ll111l_opy_ = bstack1ll111_opy_ (u"ࠨࡱࡶ࡫ࡷࠦ᣽")
    bstack11l11lll1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack11lll1l1lll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llllll1l_opy_: Any
    bstack11ll1l11111_opy_: Dict
    def __init__(
        self,
        bstack11lll1l1lll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1llllll1l_opy_: Dict[str, Any],
        methods=[bstack1ll111_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤ᣾"), bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᣿"), bstack1ll111_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᤀ"), bstack1ll111_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᤁ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11lll1l1lll_opy_ = bstack11lll1l1lll_opy_
        self.platform_index = platform_index
        self.bstack1ll1ll11l11_opy_(methods)
        self.bstack1l1llllll1l_opy_ = bstack1l1llllll1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1lllllll_opy_.get_data(bstack1ll11lll111_opy_.bstack1ll1lll111l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1lllllll_opy_.get_data(bstack1ll11lll111_opy_.bstack1lll111l1ll_opy_, target, strict)
    @staticmethod
    def bstack11l11ll1ll1_opy_(target: object, strict=True):
        return bstack1ll1lllllll_opy_.get_data(bstack1ll11lll111_opy_.bstack11l11ll11l1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1lllllll_opy_.get_data(bstack1ll11lll111_opy_.bstack1ll1lll1l1l_opy_, target, strict)
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1ll1l1l111l_opy_) -> bool:
        return bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack11ll1ll1ll1_opy_, False)
    @staticmethod
    def bstack1l1l111ll1l_opy_(instance: bstack1ll1l1l111l_opy_, default_value=None):
        return bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1lll111l1ll_opy_, default_value)
    @staticmethod
    def bstack1l11lllll1l_opy_(instance: bstack1ll1l1l111l_opy_, default_value=None):
        return bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1ll1lll1l1l_opy_, default_value)
    @staticmethod
    def bstack1l11ll1l1l1_opy_(hub_url: str, bstack11l11llll11_opy_=bstack1ll111_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᤂ")):
        try:
            bstack11l11ll1l1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l11ll1l1l_opy_.endswith(bstack11l11llll11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l111111l_opy_(method_name: str):
        return method_name == bstack1ll111_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᤃ")
    @staticmethod
    def bstack1l1l11l1ll1_opy_(method_name: str, *args):
        return (
            bstack1ll11lll111_opy_.bstack1l1l111111l_opy_(method_name)
            and bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args) == bstack1ll11lll111_opy_.bstack11ll1ll1lll_opy_
        )
    @staticmethod
    def bstack1l1l1l1111l_opy_(method_name: str, *args):
        if not bstack1ll11lll111_opy_.bstack1l1l111111l_opy_(method_name):
            return False
        if not bstack1ll11lll111_opy_.bstack11ll1l11lll_opy_ in bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args):
            return False
        bstack1l11ll1l1ll_opy_ = bstack1ll11lll111_opy_.bstack1l11ll1l11l_opy_(*args)
        return bstack1l11ll1l1ll_opy_ and bstack1ll111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᤄ") in bstack1l11ll1l1ll_opy_ and bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᤅ") in bstack1l11ll1l1ll_opy_[bstack1ll111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᤆ")]
    @staticmethod
    def bstack1l1l11l11l1_opy_(method_name: str, *args):
        if not bstack1ll11lll111_opy_.bstack1l1l111111l_opy_(method_name):
            return False
        if not bstack1ll11lll111_opy_.bstack11ll1l11lll_opy_ in bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args):
            return False
        bstack1l11ll1l1ll_opy_ = bstack1ll11lll111_opy_.bstack1l11ll1l11l_opy_(*args)
        return (
            bstack1l11ll1l1ll_opy_
            and bstack1ll111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᤇ") in bstack1l11ll1l1ll_opy_
            and bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᤈ") in bstack1l11ll1l1ll_opy_[bstack1ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᤉ")]
        )
    @staticmethod
    def bstack11lll11llll_opy_(*args):
        return str(bstack1ll11lll111_opy_.bstack1l1l11l1l11_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l11l1l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11ll1l11l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll1l111_opy_(driver):
        command_executor = getattr(driver, bstack1ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᤊ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll111_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᤋ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll111_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᤌ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll111_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᤍ"), None)
        return hub_url
    def bstack11lll1ll1ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᤎ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᤏ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll111_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᤐ")):
                setattr(command_executor, bstack1ll111_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᤑ"), hub_url)
                result = True
        if result:
            self.bstack11lll1l1lll_opy_ = hub_url
            bstack1ll11lll111_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1lll111l1ll_opy_, hub_url)
            bstack1ll11lll111_opy_.bstack1ll1ll1lll1_opy_(
                instance, bstack1ll11lll111_opy_.bstack11ll1ll1ll1_opy_, bstack1ll11lll111_opy_.bstack1l11ll1l1l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_]):
        return bstack1ll111_opy_ (u"ࠨ࠺ࠣᤒ").join((bstack1ll1l1l11l1_opy_(bstack1ll1l1l1l1l_opy_[0]).name, bstack1ll1l11ll1l_opy_(bstack1ll1l1l1l1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1111111_opy_(bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_], callback: Callable):
        bstack11ll1l1111l_opy_ = bstack1ll11lll111_opy_.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        if not bstack11ll1l1111l_opy_ in bstack1ll11lll111_opy_.bstack11l11lll1l1_opy_:
            bstack1ll11lll111_opy_.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_] = []
        bstack1ll11lll111_opy_.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_].append(callback)
    def bstack1ll1l1l1l11_opy_(self, instance: bstack1ll1l1l111l_opy_, method_name: str, bstack1ll11llllll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᤓ")):
            return
        cmd = args[0] if method_name == bstack1ll111_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᤔ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l11lll1ll_opy_ = bstack1ll111_opy_ (u"ࠤ࠽ࠦᤕ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᤖ") + bstack11l11lll1ll_opy_, bstack1ll11llllll_opy_)
    def bstack1ll1l11ll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1l1ll11l_opy_, bstack11ll11lllll_opy_ = bstack1ll1l1l1l1l_opy_
        bstack11ll1l1111l_opy_ = bstack1ll11lll111_opy_.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᤗ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᤘ"))
        if bstack1ll1l1ll11l_opy_ == bstack1ll1l1l11l1_opy_.QUIT:
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.PRE:
                bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11l11ll11ll_opy_.value)
                bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, EVENTS.bstack11l11ll11ll_opy_.value, bstack1l1l1l111_opy_)
                self.logger.debug(bstack1ll111_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᤙ").format(instance, method_name, bstack1ll1l1ll11l_opy_, bstack11ll11lllll_opy_))
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST:
                bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11l11lll11l_opy_.value)
                bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, EVENTS.bstack11l11lll11l_opy_.value, bstack1l1l1l111_opy_)
        if bstack1ll1l1ll11l_opy_ == bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_:
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST and not bstack1ll11lll111_opy_.bstack1ll1lll111l_opy_ in instance.data:
                session_id = getattr(target, bstack1ll111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᤚ"), None)
                if session_id:
                    instance.data[bstack1ll11lll111_opy_.bstack1ll1lll111l_opy_] = session_id
        elif (
            bstack1ll1l1ll11l_opy_ == bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_
            and bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args) == bstack1ll11lll111_opy_.bstack11ll1ll1lll_opy_
        ):
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.PRE:
                hub_url = bstack1ll11lll111_opy_.bstack1ll1l111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll11lll111_opy_.bstack1lll111l1ll_opy_: hub_url,
                            bstack1ll11lll111_opy_.bstack11ll1ll1ll1_opy_: bstack1ll11lll111_opy_.bstack1l11ll1l1l1_opy_(hub_url),
                            bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_: int(
                                os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᤛ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11ll1l1ll_opy_ = bstack1ll11lll111_opy_.bstack1l11ll1l11l_opy_(*args)
                bstack11l11ll1ll1_opy_ = bstack1l11ll1l1ll_opy_.get(bstack1ll111_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᤜ"), None) if bstack1l11ll1l1ll_opy_ else None
                if isinstance(bstack11l11ll1ll1_opy_, dict):
                    instance.data[bstack1ll11lll111_opy_.bstack11l11ll11l1_opy_] = copy.deepcopy(bstack11l11ll1ll1_opy_)
                    instance.data[bstack1ll11lll111_opy_.bstack1ll1lll1l1l_opy_] = bstack11l11ll1ll1_opy_
            elif bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᤝ"), dict()).get(bstack1ll111_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᤞ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll11lll111_opy_.bstack1ll1lll111l_opy_: framework_session_id,
                                bstack1ll11lll111_opy_.bstack11l11lll111_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1l1ll11l_opy_ == bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_
            and bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args) == bstack1ll11lll111_opy_.bstack11l11ll111l_opy_
            and bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST
        ):
            instance.data[bstack1ll11lll111_opy_.bstack11l11ll1lll_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll1l1111l_opy_ in bstack1ll11lll111_opy_.bstack11l11lll1l1_opy_:
            bstack11ll1l1l111_opy_ = None
            for callback in bstack1ll11lll111_opy_.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_]:
                try:
                    bstack11ll1l11l1l_opy_ = callback(self, target, exec, bstack1ll1l1l1l1l_opy_, result, *args, **kwargs)
                    if bstack11ll1l1l111_opy_ == None:
                        bstack11ll1l1l111_opy_ = bstack11ll1l11l1l_opy_
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥ᤟") + str(e) + bstack1ll111_opy_ (u"ࠨࠢᤠ"))
                    traceback.print_exc()
            if bstack1ll1l1ll11l_opy_ == bstack1ll1l1l11l1_opy_.QUIT:
                if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.PRE:
                    bstack1l1l1l111_opy_ = bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, EVENTS.bstack11l11ll11ll_opy_.value)
                    if bstack1l1l1l111_opy_!=None:
                        bstack111ll11111_opy_.end(EVENTS.bstack11l11ll11ll_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᤡ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᤢ"), True, None)
                if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST:
                    bstack1l1l1l111_opy_ = bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, EVENTS.bstack11l11lll11l_opy_.value)
                    if bstack1l1l1l111_opy_!=None:
                        bstack111ll11111_opy_.end(EVENTS.bstack11l11lll11l_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᤣ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᤤ"), True, None)
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.PRE and callable(bstack11ll1l1l111_opy_):
                return bstack11ll1l1l111_opy_
            elif bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST and bstack11ll1l1l111_opy_:
                return bstack11ll1l1l111_opy_
    def bstack1ll11lllll1_opy_(
        self, method_name, previous_state: bstack1ll1l1l11l1_opy_, *args, **kwargs
    ) -> bstack1ll1l1l11l1_opy_:
        if method_name == bstack1ll111_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᤥ") or method_name == bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᤦ"):
            return bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_
        if method_name == bstack1ll111_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᤧ"):
            return bstack1ll1l1l11l1_opy_.QUIT
        if method_name == bstack1ll111_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᤨ"):
            if previous_state != bstack1ll1l1l11l1_opy_.NONE:
                command_name = bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args)
                if command_name == bstack1ll11lll111_opy_.bstack11ll1ll1lll_opy_:
                    return bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_
            return bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_
        return bstack1ll1l1l11l1_opy_.NONE