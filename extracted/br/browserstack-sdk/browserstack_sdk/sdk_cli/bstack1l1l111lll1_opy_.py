# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack11l1l1ll11_opy_,
    bstack1l1ll11l1ll_opy_,
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils.constants import EVENTS
class bstack1l1l111l111_opy_(bstack11l1l1ll11_opy_):
    bstack11l111lll11_opy_ = bstack1l1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ᫫")
    NAME = bstack1l1111l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨ᫬")
    bstack11111llll_opy_ = bstack1l1111l_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨ᫭")
    bstack1l1lllll1l1_opy_ = bstack1l1111l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨ᫮")
    bstack111l1l1lll1_opy_ = bstack1l1111l_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᫯")
    bstack1l111111l_opy_ = bstack1l1111l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᫰")
    bstack11l11l1l11l_opy_ = bstack1l1111l_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣ᫱")
    bstack111l1l1l11l_opy_ = bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ᫲")
    bstack111l1l1l111_opy_ = bstack1l1111l_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨ᫳")
    bstack1l111l1l111_opy_ = bstack1l1111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨ᫴")
    bstack11l11lll111_opy_ = bstack1l1111l_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥ᫵")
    bstack111l1l1llll_opy_ = bstack1l1111l_opy_ (u"ࠢࡨࡧࡷࠦ᫶")
    bstack11ll11lll1l_opy_ = bstack1l1111l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᫷")
    bstack11l111ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧ᫸")
    bstack11l111l1ll1_opy_ = bstack1l1111l_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦ᫹")
    bstack111l1l1ll1l_opy_ = bstack1l1111l_opy_ (u"ࠦࡶࡻࡩࡵࠤ᫺")
    bstack111l1l11lll_opy_: Dict[str, List[Callable]] = dict()
    bstack11l11lll11l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11lll1l11_opy_: Any
    bstack11l111lllll_opy_: Dict
    def __init__(
        self,
        bstack11l11lll11l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l11lll1l11_opy_: Dict[str, Any],
        methods=[bstack1l1111l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢ᫻"), bstack1l1111l_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨ᫼"), bstack1l1111l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣ᫽"), bstack1l1111l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨ᫾")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l11lll11l_opy_ = bstack11l11lll11l_opy_
        self.platform_index = platform_index
        self.bstack1l1ll111l11_opy_(methods)
        self.bstack1l11lll1l11_opy_ = bstack1l11lll1l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11l1l1ll11_opy_.get_data(bstack1l1l111l111_opy_.bstack1l1lllll1l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11l1l1ll11_opy_.get_data(bstack1l1l111l111_opy_.bstack11111llll_opy_, target, strict)
    @staticmethod
    def bstack111l1l1ll11_opy_(target: object, strict=True):
        return bstack11l1l1ll11_opy_.get_data(bstack1l1l111l111_opy_.bstack111l1l1lll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11l1l1ll11_opy_.get_data(bstack1l1l111l111_opy_.bstack1l111111l_opy_, target, strict)
    @staticmethod
    def bstack11lll1l1ll1_opy_(instance: bstack1l1ll11l1ll_opy_) -> bool:
        return bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack11l11l1l11l_opy_, False)
    @staticmethod
    def bstack11lllll1l1l_opy_(instance: bstack1l1ll11l1ll_opy_, default_value=None):
        return bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack11111llll_opy_, default_value)
    @staticmethod
    def bstack1l111l11l11_opy_(instance: bstack1l1ll11l1ll_opy_, default_value=None):
        return bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111111l_opy_, default_value)
    @staticmethod
    def bstack11llll1lll1_opy_(hub_url: str, bstack111l1ll11l1_opy_=bstack1l1111l_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ᫿")):
        try:
            bstack111l1ll1111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1ll1111_opy_.endswith(bstack111l1ll11l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1111l111l_opy_(method_name: str):
        return method_name == bstack1l1111l_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᬀ")
    @staticmethod
    def bstack1l111l1llll_opy_(method_name: str, *args):
        return (
            bstack1l1l111l111_opy_.bstack1l1111l111l_opy_(method_name)
            and bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args) == bstack1l1l111l111_opy_.bstack11l11lll111_opy_
        )
    @staticmethod
    def bstack11lllll1111_opy_(method_name: str, *args):
        if not bstack1l1l111l111_opy_.bstack1l1111l111l_opy_(method_name):
            return False
        if not bstack1l1l111l111_opy_.bstack11l111ll1ll_opy_ in bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args):
            return False
        bstack11llll1l1l1_opy_ = bstack1l1l111l111_opy_.bstack11llll11ll1_opy_(*args)
        return bstack11llll1l1l1_opy_ and bstack1l1111l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᬁ") in bstack11llll1l1l1_opy_ and bstack1l1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᬂ") in bstack11llll1l1l1_opy_[bstack1l1111l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᬃ")]
    @staticmethod
    def bstack1l1111111l1_opy_(method_name: str, *args):
        if not bstack1l1l111l111_opy_.bstack1l1111l111l_opy_(method_name):
            return False
        if not bstack1l1l111l111_opy_.bstack11l111ll1ll_opy_ in bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args):
            return False
        bstack11llll1l1l1_opy_ = bstack1l1l111l111_opy_.bstack11llll11ll1_opy_(*args)
        return (
            bstack11llll1l1l1_opy_
            and bstack1l1111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᬄ") in bstack11llll1l1l1_opy_
            and bstack1l1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᬅ") in bstack11llll1l1l1_opy_[bstack1l1111l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᬆ")]
        )
    @staticmethod
    def bstack11l1l11l1ll_opy_(*args):
        return str(bstack1l1l111l111_opy_.bstack1l1111l11l1_opy_(*args)).lower()
    @staticmethod
    def bstack1l1111l11l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11llll11ll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l11111l1l_opy_(driver):
        command_executor = getattr(driver, bstack1l1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᬇ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1111l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᬈ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1111l_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᬉ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1111l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᬊ"), None)
        return hub_url
    def bstack11l11lllll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᬋ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᬌ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1111l_opy_ (u"ࠤࡢࡹࡷࡲࠢᬍ")):
                setattr(command_executor, bstack1l1111l_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᬎ"), hub_url)
                result = True
        if result:
            self.bstack11l11lll11l_opy_ = hub_url
            bstack1l1l111l111_opy_.bstack111l1llll1_opy_(instance, bstack1l1l111l111_opy_.bstack11111llll_opy_, hub_url)
            bstack1l1l111l111_opy_.bstack111l1llll1_opy_(
                instance, bstack1l1l111l111_opy_.bstack11l11l1l11l_opy_, bstack1l1l111l111_opy_.bstack11llll1lll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_]):
        return bstack1l1111l_opy_ (u"ࠦ࠿ࠨᬏ").join((bstack1lll11l1l1_opy_(bstack1l1ll1ll111_opy_[0]).name, bstack1111llll1l_opy_(bstack1l1ll1ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1111lllll_opy_(bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_], callback: Callable):
        bstack11l111ll111_opy_ = bstack1l1l111l111_opy_.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        if not bstack11l111ll111_opy_ in bstack1l1l111l111_opy_.bstack111l1l11lll_opy_:
            bstack1l1l111l111_opy_.bstack111l1l11lll_opy_[bstack11l111ll111_opy_] = []
        bstack1l1l111l111_opy_.bstack111l1l11lll_opy_[bstack11l111ll111_opy_].append(callback)
    def bstack1l1l1lllll1_opy_(self, instance: bstack1l1ll11l1ll_opy_, method_name: str, bstack1l1l1llll11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᬐ")):
            return
        cmd = args[0] if method_name == bstack1l1111l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᬑ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l1ll111l_opy_ = bstack1l1111l_opy_ (u"ࠢ࠻ࠤᬒ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᬓ") + bstack111l1ll111l_opy_, bstack1l1l1llll11_opy_)
    def bstack1llll111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1llll1l_opy_, bstack11l111lll1l_opy_ = bstack1l1ll1ll111_opy_
        bstack11l111ll111_opy_ = bstack1l1l111l111_opy_.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᬔ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠥࠦᬕ"))
        if bstack1l1l1llll1l_opy_ == bstack1lll11l1l1_opy_.QUIT:
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.PRE:
                bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111l1l1l1ll_opy_.value)
                bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, EVENTS.bstack111l1l1l1ll_opy_.value, bstack1l11l1l11_opy_)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᬖ").format(instance, method_name, bstack1l1l1llll1l_opy_, bstack11l111lll1l_opy_))
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST:
                bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111l1l1l1l1_opy_.value)
                bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, EVENTS.bstack111l1l1l1l1_opy_.value, bstack1l11l1l11_opy_)
        if bstack1l1l1llll1l_opy_ == bstack1lll11l1l1_opy_.bstack1lll1l111_opy_:
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST and not bstack1l1l111l111_opy_.bstack1l1lllll1l1_opy_ in instance.data:
                session_id = getattr(target, bstack1l1111l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᬗ"), None)
                if session_id:
                    instance.data[bstack1l1l111l111_opy_.bstack1l1lllll1l1_opy_] = session_id
        elif (
            bstack1l1l1llll1l_opy_ == bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_
            and bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args) == bstack1l1l111l111_opy_.bstack11l11lll111_opy_
        ):
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.PRE:
                hub_url = bstack1l1l111l111_opy_.bstack1l11111l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l1l111l111_opy_.bstack11111llll_opy_: hub_url,
                            bstack1l1l111l111_opy_.bstack11l11l1l11l_opy_: bstack1l1l111l111_opy_.bstack11llll1lll1_opy_(hub_url),
                            bstack1l1l111l111_opy_.bstack1l111l1l111_opy_: int(
                                os.environ.get(bstack1l1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᬘ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11llll1l1l1_opy_ = bstack1l1l111l111_opy_.bstack11llll11ll1_opy_(*args)
                bstack111l1l1ll11_opy_ = bstack11llll1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᬙ"), None) if bstack11llll1l1l1_opy_ else None
                if isinstance(bstack111l1l1ll11_opy_, dict):
                    instance.data[bstack1l1l111l111_opy_.bstack111l1l1lll1_opy_] = copy.deepcopy(bstack111l1l1ll11_opy_)
                    instance.data[bstack1l1l111l111_opy_.bstack1l111111l_opy_] = bstack111l1l1ll11_opy_
            elif bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1111l_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᬚ"), dict()).get(bstack1l1111l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᬛ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l1l111l111_opy_.bstack1l1lllll1l1_opy_: framework_session_id,
                                bstack1l1l111l111_opy_.bstack111l1l1l11l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1l1llll1l_opy_ == bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_
            and bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args) == bstack1l1l111l111_opy_.bstack111l1l1ll1l_opy_
            and bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST
        ):
            instance.data[bstack1l1l111l111_opy_.bstack111l1l1l111_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l111ll111_opy_ in bstack1l1l111l111_opy_.bstack111l1l11lll_opy_:
            bstack11l111l1l1l_opy_ = None
            for callback in bstack1l1l111l111_opy_.bstack111l1l11lll_opy_[bstack11l111ll111_opy_]:
                try:
                    bstack11l111ll1l1_opy_ = callback(self, target, exec, bstack1l1ll1ll111_opy_, result, *args, **kwargs)
                    if bstack11l111l1l1l_opy_ == None:
                        bstack11l111l1l1l_opy_ = bstack11l111ll1l1_opy_
                except Exception as e:
                    self.logger.error(bstack1l1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᬜ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᬝ"))
                    traceback.print_exc()
            if bstack1l1l1llll1l_opy_ == bstack1lll11l1l1_opy_.QUIT:
                if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.PRE:
                    bstack1l11l1l11_opy_ = bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, EVENTS.bstack111l1l1l1ll_opy_.value)
                    if bstack1l11l1l11_opy_!=None:
                        bstack11lll1111_opy_.end(EVENTS.bstack111l1l1l1ll_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᬞ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᬟ"), True, None)
                if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST:
                    bstack1l11l1l11_opy_ = bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, EVENTS.bstack111l1l1l1l1_opy_.value)
                    if bstack1l11l1l11_opy_!=None:
                        bstack11lll1111_opy_.end(EVENTS.bstack111l1l1l1l1_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᬠ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᬡ"), True, None)
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.PRE and callable(bstack11l111l1l1l_opy_):
                return bstack11l111l1l1l_opy_
            elif bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST and bstack11l111l1l1l_opy_:
                return bstack11l111l1l1l_opy_
    def bstack1l1ll11ll11_opy_(
        self, method_name, previous_state: bstack1lll11l1l1_opy_, *args, **kwargs
    ) -> bstack1lll11l1l1_opy_:
        if method_name == bstack1l1111l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᬢ") or method_name == bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᬣ"):
            return bstack1lll11l1l1_opy_.bstack1lll1l111_opy_
        if method_name == bstack1l1111l_opy_ (u"ࠦࡶࡻࡩࡵࠤᬤ"):
            return bstack1lll11l1l1_opy_.QUIT
        if method_name == bstack1l1111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᬥ"):
            if previous_state != bstack1lll11l1l1_opy_.NONE:
                command_name = bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args)
                if command_name == bstack1l1l111l111_opy_.bstack11l11lll111_opy_:
                    return bstack1lll11l1l1_opy_.bstack1lll1l111_opy_
            return bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_
        return bstack1lll11l1l1_opy_.NONE