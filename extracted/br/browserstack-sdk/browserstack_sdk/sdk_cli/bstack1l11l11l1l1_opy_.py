# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack111l1ll1ll_opy_,
    bstack1l1ll1lllll_opy_,
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
from bstack_utils.constants import EVENTS
class bstack1l11l1ll1l1_opy_(bstack111l1ll1ll_opy_):
    bstack11l111lllll_opy_ = bstack1l111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ᫩")
    NAME = bstack1l111l_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᫪")
    bstack11llll1l11_opy_ = bstack1l111l_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦ᫫")
    bstack1ll1111lll1_opy_ = bstack1l111l_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ᫬")
    bstack111l1ll1l11_opy_ = bstack1l111l_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᫭")
    bstack11lll111l_opy_ = bstack1l111l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᫮")
    bstack11l11l11l1l_opy_ = bstack1l111l_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨ᫯")
    bstack111l1l1l1ll_opy_ = bstack1l111l_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧ᫰")
    bstack111l1l1l11l_opy_ = bstack1l111l_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦ᫱")
    bstack1l111l1111l_opy_ = bstack1l111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦ᫲")
    bstack11l11llllll_opy_ = bstack1l111l_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᫳")
    bstack111l1ll11l1_opy_ = bstack1l111l_opy_ (u"ࠧ࡭ࡥࡵࠤ᫴")
    bstack11lll111l1l_opy_ = bstack1l111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᫵")
    bstack11l111ll111_opy_ = bstack1l111l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥ᫶")
    bstack11l111lll11_opy_ = bstack1l111l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤ᫷")
    bstack111l1l1ll11_opy_ = bstack1l111l_opy_ (u"ࠤࡴࡹ࡮ࡺࠢ᫸")
    bstack111l1ll111l_opy_: Dict[str, List[Callable]] = dict()
    bstack11l1l1l111l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1lll1l1_opy_: Any
    bstack11l11l11111_opy_: Dict
    def __init__(
        self,
        bstack11l1l1l111l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1l1lll1l1_opy_: Dict[str, Any],
        methods=[bstack1l111l_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧ᫹"), bstack1l111l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦ᫺"), bstack1l111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨ᫻"), bstack1l111l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦ᫼")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l1l1l111l_opy_ = bstack11l1l1l111l_opy_
        self.platform_index = platform_index
        self.bstack1l1ll1llll1_opy_(methods)
        self.bstack1l1l1lll1l1_opy_ = bstack1l1l1lll1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack111l1ll1ll_opy_.get_data(bstack1l11l1ll1l1_opy_.bstack1ll1111lll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack111l1ll1ll_opy_.get_data(bstack1l11l1ll1l1_opy_.bstack11llll1l11_opy_, target, strict)
    @staticmethod
    def bstack111l1l1lll1_opy_(target: object, strict=True):
        return bstack111l1ll1ll_opy_.get_data(bstack1l11l1ll1l1_opy_.bstack111l1ll1l11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack111l1ll1ll_opy_.get_data(bstack1l11l1ll1l1_opy_.bstack11lll111l_opy_, target, strict)
    @staticmethod
    def bstack11lll1lllll_opy_(instance: bstack1l1ll1lllll_opy_) -> bool:
        return bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack11l11l11l1l_opy_, False)
    @staticmethod
    def bstack1l1111l1l11_opy_(instance: bstack1l1ll1lllll_opy_, default_value=None):
        return bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack11llll1l11_opy_, default_value)
    @staticmethod
    def bstack1l111ll11l1_opy_(instance: bstack1l1ll1lllll_opy_, default_value=None):
        return bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack11lll111l_opy_, default_value)
    @staticmethod
    def bstack11llll11ll1_opy_(hub_url: str, bstack111l1l1ll1l_opy_=bstack1l111l_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᫽")):
        try:
            bstack111l1ll11ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1ll11ll_opy_.endswith(bstack111l1l1ll1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack11lllll1ll1_opy_(method_name: str):
        return method_name == bstack1l111l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤ᫾")
    @staticmethod
    def bstack1l111l111l1_opy_(method_name: str, *args):
        return (
            bstack1l11l1ll1l1_opy_.bstack11lllll1ll1_opy_(method_name)
            and bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args) == bstack1l11l1ll1l1_opy_.bstack11l11llllll_opy_
        )
    @staticmethod
    def bstack1l111l1l111_opy_(method_name: str, *args):
        if not bstack1l11l1ll1l1_opy_.bstack11lllll1ll1_opy_(method_name):
            return False
        if not bstack1l11l1ll1l1_opy_.bstack11l111ll111_opy_ in bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args):
            return False
        bstack11llll1ll11_opy_ = bstack1l11l1ll1l1_opy_.bstack11llll1lll1_opy_(*args)
        return bstack11llll1ll11_opy_ and bstack1l111l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ᫿") in bstack11llll1ll11_opy_ and bstack1l111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᬀ") in bstack11llll1ll11_opy_[bstack1l111l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᬁ")]
    @staticmethod
    def bstack11lllll111l_opy_(method_name: str, *args):
        if not bstack1l11l1ll1l1_opy_.bstack11lllll1ll1_opy_(method_name):
            return False
        if not bstack1l11l1ll1l1_opy_.bstack11l111ll111_opy_ in bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args):
            return False
        bstack11llll1ll11_opy_ = bstack1l11l1ll1l1_opy_.bstack11llll1lll1_opy_(*args)
        return (
            bstack11llll1ll11_opy_
            and bstack1l111l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᬂ") in bstack11llll1ll11_opy_
            and bstack1l111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᬃ") in bstack11llll1ll11_opy_[bstack1l111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᬄ")]
        )
    @staticmethod
    def bstack11l1l1l1111_opy_(*args):
        return str(bstack1l11l1ll1l1_opy_.bstack1l111111l11_opy_(*args)).lower()
    @staticmethod
    def bstack1l111111l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11llll1lll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1lll111l_opy_(driver):
        command_executor = getattr(driver, bstack1l111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᬅ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l111l_opy_ (u"ࠤࡢࡹࡷࡲࠢᬆ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l111l_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᬇ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l111l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᬈ"), None)
        return hub_url
    def bstack11l11lll111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᬉ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᬊ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l111l_opy_ (u"ࠢࡠࡷࡵࡰࠧᬋ")):
                setattr(command_executor, bstack1l111l_opy_ (u"ࠣࡡࡸࡶࡱࠨᬌ"), hub_url)
                result = True
        if result:
            self.bstack11l1l1l111l_opy_ = hub_url
            bstack1l11l1ll1l1_opy_.bstack11111ll11l_opy_(instance, bstack1l11l1ll1l1_opy_.bstack11llll1l11_opy_, hub_url)
            bstack1l11l1ll1l1_opy_.bstack11111ll11l_opy_(
                instance, bstack1l11l1ll1l1_opy_.bstack11l11l11l1l_opy_, bstack1l11l1ll1l1_opy_.bstack11llll11ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_]):
        return bstack1l111l_opy_ (u"ࠤ࠽ࠦᬍ").join((bstack1l1l11ll1l_opy_(bstack1l1l1lllll1_opy_[0]).name, bstack1ll1llll1l_opy_(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack1l11111ll11_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_], callback: Callable):
        bstack11l11l1111l_opy_ = bstack1l11l1ll1l1_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        if not bstack11l11l1111l_opy_ in bstack1l11l1ll1l1_opy_.bstack111l1ll111l_opy_:
            bstack1l11l1ll1l1_opy_.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_] = []
        bstack1l11l1ll1l1_opy_.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_].append(callback)
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1l1ll1lllll_opy_, method_name: str, bstack1l1ll1l11l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᬎ")):
            return
        cmd = args[0] if method_name == bstack1l111l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᬏ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l1l1l1l1_opy_ = bstack1l111l_opy_ (u"ࠧࡀࠢᬐ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢᬑ") + bstack111l1l1l1l1_opy_, bstack1l1ll1l11l1_opy_)
    def bstack1l1l1llll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll1l111l_opy_, bstack11l111ll1ll_opy_ = bstack1l1l1lllll1_opy_
        bstack11l11l1111l_opy_ = bstack1l11l1ll1l1_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        self.logger.debug(bstack1l111l_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᬒ") + str(kwargs) + bstack1l111l_opy_ (u"ࠣࠤᬓ"))
        if bstack1l1ll1l111l_opy_ == bstack1l1l11ll1l_opy_.QUIT:
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.PRE:
                bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack111l1l1llll_opy_.value)
                bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, EVENTS.bstack111l1l1llll_opy_.value, bstack1l11l11l_opy_)
                self.logger.debug(bstack1l111l_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᬔ").format(instance, method_name, bstack1l1ll1l111l_opy_, bstack11l111ll1ll_opy_))
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST:
                bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack111l1ll1111_opy_.value)
                bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, EVENTS.bstack111l1ll1111_opy_.value, bstack1l11l11l_opy_)
        if bstack1l1ll1l111l_opy_ == bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_:
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST and not bstack1l11l1ll1l1_opy_.bstack1ll1111lll1_opy_ in instance.data:
                session_id = getattr(target, bstack1l111l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᬕ"), None)
                if session_id:
                    instance.data[bstack1l11l1ll1l1_opy_.bstack1ll1111lll1_opy_] = session_id
        elif (
            bstack1l1ll1l111l_opy_ == bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_
            and bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args) == bstack1l11l1ll1l1_opy_.bstack11l11llllll_opy_
        ):
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.PRE:
                hub_url = bstack1l11l1ll1l1_opy_.bstack1l1lll111l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l11l1ll1l1_opy_.bstack11llll1l11_opy_: hub_url,
                            bstack1l11l1ll1l1_opy_.bstack11l11l11l1l_opy_: bstack1l11l1ll1l1_opy_.bstack11llll11ll1_opy_(hub_url),
                            bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_: int(
                                os.environ.get(bstack1l111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᬖ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11llll1ll11_opy_ = bstack1l11l1ll1l1_opy_.bstack11llll1lll1_opy_(*args)
                bstack111l1l1lll1_opy_ = bstack11llll1ll11_opy_.get(bstack1l111l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᬗ"), None) if bstack11llll1ll11_opy_ else None
                if isinstance(bstack111l1l1lll1_opy_, dict):
                    instance.data[bstack1l11l1ll1l1_opy_.bstack111l1ll1l11_opy_] = copy.deepcopy(bstack111l1l1lll1_opy_)
                    instance.data[bstack1l11l1ll1l1_opy_.bstack11lll111l_opy_] = bstack111l1l1lll1_opy_
            elif bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l111l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᬘ"), dict()).get(bstack1l111l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᬙ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l11l1ll1l1_opy_.bstack1ll1111lll1_opy_: framework_session_id,
                                bstack1l11l1ll1l1_opy_.bstack111l1l1l1ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1ll1l111l_opy_ == bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_
            and bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args) == bstack1l11l1ll1l1_opy_.bstack111l1l1ll11_opy_
            and bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST
        ):
            instance.data[bstack1l11l1ll1l1_opy_.bstack111l1l1l11l_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l11l1111l_opy_ in bstack1l11l1ll1l1_opy_.bstack111l1ll111l_opy_:
            bstack11l111lll1l_opy_ = None
            for callback in bstack1l11l1ll1l1_opy_.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_]:
                try:
                    bstack11l111llll1_opy_ = callback(self, target, exec, bstack1l1l1lllll1_opy_, result, *args, **kwargs)
                    if bstack11l111lll1l_opy_ == None:
                        bstack11l111lll1l_opy_ = bstack11l111llll1_opy_
                except Exception as e:
                    self.logger.error(bstack1l111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᬚ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᬛ"))
                    traceback.print_exc()
            if bstack1l1ll1l111l_opy_ == bstack1l1l11ll1l_opy_.QUIT:
                if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.PRE:
                    bstack1l11l11l_opy_ = bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, EVENTS.bstack111l1l1llll_opy_.value)
                    if bstack1l11l11l_opy_!=None:
                        bstack111ll11l1_opy_.end(EVENTS.bstack111l1l1llll_opy_.value, bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᬜ"), bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᬝ"), True, None)
                if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST:
                    bstack1l11l11l_opy_ = bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, EVENTS.bstack111l1ll1111_opy_.value)
                    if bstack1l11l11l_opy_!=None:
                        bstack111ll11l1_opy_.end(EVENTS.bstack111l1ll1111_opy_.value, bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᬞ"), bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᬟ"), True, None)
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.PRE and callable(bstack11l111lll1l_opy_):
                return bstack11l111lll1l_opy_
            elif bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST and bstack11l111lll1l_opy_:
                return bstack11l111lll1l_opy_
    def bstack1l1l1llll1l_opy_(
        self, method_name, previous_state: bstack1l1l11ll1l_opy_, *args, **kwargs
    ) -> bstack1l1l11ll1l_opy_:
        if method_name == bstack1l111l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᬠ") or method_name == bstack1l111l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᬡ"):
            return bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_
        if method_name == bstack1l111l_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᬢ"):
            return bstack1l1l11ll1l_opy_.QUIT
        if method_name == bstack1l111l_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᬣ"):
            if previous_state != bstack1l1l11ll1l_opy_.NONE:
                command_name = bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args)
                if command_name == bstack1l11l1ll1l1_opy_.bstack11l11llllll_opy_:
                    return bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_
            return bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_
        return bstack1l1l11ll1l_opy_.NONE