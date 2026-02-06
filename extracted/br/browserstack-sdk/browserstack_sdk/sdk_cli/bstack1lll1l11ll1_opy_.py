# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.constants import EVENTS
class bstack1lll11lllll_opy_(bstack1lll1ll1ll1_opy_):
    bstack11llll1llll_opy_ = bstack11lllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᚪ")
    NAME = bstack11lllll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᚫ")
    bstack1l111lll111_opy_ = bstack11lllll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᚬ")
    bstack1l111llll11_opy_ = bstack11lllll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᚭ")
    bstack11ll11l1111_opy_ = bstack11lllll_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᚮ")
    bstack1l11l1111ll_opy_ = bstack11lllll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᚯ")
    bstack1l111111111_opy_ = bstack11lllll_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᚰ")
    bstack11ll111l1ll_opy_ = bstack11lllll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᚱ")
    bstack11ll111ll1l_opy_ = bstack11lllll_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᚲ")
    bstack1l1l1lllll1_opy_ = bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᚳ")
    bstack1l11111ll11_opy_ = bstack11lllll_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᚴ")
    bstack11ll111l111_opy_ = bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺࠢᚵ")
    bstack1l11l1lll11_opy_ = bstack11lllll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᚶ")
    bstack11lllll1l11_opy_ = bstack11lllll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᚷ")
    bstack11lllll1l1l_opy_ = bstack11lllll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᚸ")
    bstack11ll11l11l1_opy_ = bstack11lllll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᚹ")
    bstack11ll111llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l111l11111_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l11l1l1_opy_: Any
    bstack11llll1lll1_opy_: Dict
    def __init__(
        self,
        bstack1l111l11111_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1l11l1l1_opy_: Dict[str, Any],
        methods=[bstack11lllll_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᚺ"), bstack11lllll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᚻ"), bstack11lllll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᚼ"), bstack11lllll_opy_ (u"ࠦࡶࡻࡩࡵࠤᚽ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l111l11111_opy_ = bstack1l111l11111_opy_
        self.platform_index = platform_index
        self.bstack1lll1111lll_opy_(methods)
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll1ll1ll1_opy_.get_data(bstack1lll11lllll_opy_.bstack1l111llll11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll1ll1ll1_opy_.get_data(bstack1lll11lllll_opy_.bstack1l111lll111_opy_, target, strict)
    @staticmethod
    def bstack11ll1111lll_opy_(target: object, strict=True):
        return bstack1lll1ll1ll1_opy_.get_data(bstack1lll11lllll_opy_.bstack11ll11l1111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll1ll1ll1_opy_.get_data(bstack1lll11lllll_opy_.bstack1l11l1111ll_opy_, target, strict)
    @staticmethod
    def bstack1lll1l1llll_opy_(instance: bstack1lll1l1l11l_opy_) -> bool:
        return bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l111111111_opy_, False)
    @staticmethod
    def bstack1l1ll11llll_opy_(instance: bstack1lll1l1l11l_opy_, default_value=None):
        return bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l111lll111_opy_, default_value)
    @staticmethod
    def bstack1l1lll1ll1l_opy_(instance: bstack1lll1l1l11l_opy_, default_value=None):
        return bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l11l1111ll_opy_, default_value)
    @staticmethod
    def bstack1lll1ll11l1_opy_(hub_url: str, bstack11ll111lll1_opy_=bstack11lllll_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᚾ")):
        try:
            bstack11ll111l11l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11ll111l11l_opy_.endswith(bstack11ll111lll1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1ll11ll1l_opy_(method_name: str):
        return method_name == bstack11lllll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᚿ")
    @staticmethod
    def bstack1l1lll1l11l_opy_(method_name: str, *args):
        return (
            bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_(method_name)
            and bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args) == bstack1lll11lllll_opy_.bstack1l11111ll11_opy_
        )
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(method_name: str, *args):
        if not bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_(method_name):
            return False
        if not bstack1lll11lllll_opy_.bstack11lllll1l11_opy_ in bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args):
            return False
        bstack1l1l1l11lll_opy_ = bstack1lll11lllll_opy_.bstack1l1l1l11l11_opy_(*args)
        return bstack1l1l1l11lll_opy_ and bstack11lllll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᛀ") in bstack1l1l1l11lll_opy_ and bstack11lllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᛁ") in bstack1l1l1l11lll_opy_[bstack11lllll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᛂ")]
    @staticmethod
    def bstack1l1l1ll1l1l_opy_(method_name: str, *args):
        if not bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_(method_name):
            return False
        if not bstack1lll11lllll_opy_.bstack11lllll1l11_opy_ in bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args):
            return False
        bstack1l1l1l11lll_opy_ = bstack1lll11lllll_opy_.bstack1l1l1l11l11_opy_(*args)
        return (
            bstack1l1l1l11lll_opy_
            and bstack11lllll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᛃ") in bstack1l1l1l11lll_opy_
            and bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᛄ") in bstack1l1l1l11lll_opy_[bstack11lllll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᛅ")]
        )
    @staticmethod
    def bstack1l111111l1l_opy_(*args):
        return str(bstack1lll11lllll_opy_.bstack1l1l1lll11l_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l1lll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1l11l11_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1llll111_opy_(driver):
        command_executor = getattr(driver, bstack11lllll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᛆ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11lllll_opy_ (u"ࠢࡠࡷࡵࡰࠧᛇ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11lllll_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᛈ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11lllll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᛉ"), None)
        return hub_url
    def bstack1l111l111ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᛊ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᛋ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11lllll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᛌ")):
                setattr(command_executor, bstack11lllll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᛍ"), hub_url)
                result = True
        if result:
            self.bstack1l111l11111_opy_ = hub_url
            bstack1lll11lllll_opy_.bstack1lll1ll1lll_opy_(instance, bstack1lll11lllll_opy_.bstack1l111lll111_opy_, hub_url)
            bstack1lll11lllll_opy_.bstack1lll1ll1lll_opy_(
                instance, bstack1lll11lllll_opy_.bstack1l111111111_opy_, bstack1lll11lllll_opy_.bstack1lll1ll11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11lllll111l_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_]):
        return bstack11lllll_opy_ (u"ࠢ࠻ࠤᛎ").join((bstack1lll1l1ll1l_opy_(bstack1lll1l11lll_opy_[0]).name, bstack1lll1ll11ll_opy_(bstack1lll1l11lll_opy_[1]).name))
    @staticmethod
    def bstack1lll1l1l1ll_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_], callback: Callable):
        bstack11lllll11l1_opy_ = bstack1lll11lllll_opy_.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        if not bstack11lllll11l1_opy_ in bstack1lll11lllll_opy_.bstack11ll111llll_opy_:
            bstack1lll11lllll_opy_.bstack11ll111llll_opy_[bstack11lllll11l1_opy_] = []
        bstack1lll11lllll_opy_.bstack11ll111llll_opy_[bstack11lllll11l1_opy_].append(callback)
    def bstack1lll111l1l1_opy_(self, instance: bstack1lll1l1l11l_opy_, method_name: str, bstack1ll1lll1lll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11lllll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᛏ")):
            return
        cmd = args[0] if method_name == bstack11lllll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᛐ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11ll11l111l_opy_ = bstack11lllll_opy_ (u"ࠥ࠾ࠧᛑ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᛒ") + bstack11ll11l111l_opy_, bstack1ll1lll1lll_opy_)
    def bstack1lll111llll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll11l1l1l_opy_, bstack11lllll1111_opy_ = bstack1lll1l11lll_opy_
        bstack11lllll11l1_opy_ = bstack1lll11lllll_opy_.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᛓ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᛔ"))
        if bstack1lll11l1l1l_opy_ == bstack1lll1l1ll1l_opy_.QUIT:
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.PRE:
                bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack11ll111ll11_opy_.value)
                bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, EVENTS.bstack11ll111ll11_opy_.value, bstack1ll11111l_opy_)
                self.logger.debug(bstack11lllll_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᛕ").format(instance, method_name, bstack1lll11l1l1l_opy_, bstack11lllll1111_opy_))
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST:
                bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack11ll111l1l1_opy_.value)
                bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, EVENTS.bstack11ll111l1l1_opy_.value, bstack1ll11111l_opy_)
        if bstack1lll11l1l1l_opy_ == bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_:
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST and not bstack1lll11lllll_opy_.bstack1l111llll11_opy_ in instance.data:
                session_id = getattr(target, bstack11lllll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᛖ"), None)
                if session_id:
                    instance.data[bstack1lll11lllll_opy_.bstack1l111llll11_opy_] = session_id
        elif (
            bstack1lll11l1l1l_opy_ == bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_
            and bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args) == bstack1lll11lllll_opy_.bstack1l11111ll11_opy_
        ):
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.PRE:
                hub_url = bstack1lll11lllll_opy_.bstack1l1llll111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll11lllll_opy_.bstack1l111lll111_opy_: hub_url,
                            bstack1lll11lllll_opy_.bstack1l111111111_opy_: bstack1lll11lllll_opy_.bstack1lll1ll11l1_opy_(hub_url),
                            bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_: int(
                                os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᛗ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l1l11lll_opy_ = bstack1lll11lllll_opy_.bstack1l1l1l11l11_opy_(*args)
                bstack11ll1111lll_opy_ = bstack1l1l1l11lll_opy_.get(bstack11lllll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᛘ"), None) if bstack1l1l1l11lll_opy_ else None
                if isinstance(bstack11ll1111lll_opy_, dict):
                    instance.data[bstack1lll11lllll_opy_.bstack11ll11l1111_opy_] = copy.deepcopy(bstack11ll1111lll_opy_)
                    instance.data[bstack1lll11lllll_opy_.bstack1l11l1111ll_opy_] = bstack11ll1111lll_opy_
            elif bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11lllll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᛙ"), dict()).get(bstack11lllll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᛚ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll11lllll_opy_.bstack1l111llll11_opy_: framework_session_id,
                                bstack1lll11lllll_opy_.bstack11ll111l1ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll11l1l1l_opy_ == bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_
            and bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args) == bstack1lll11lllll_opy_.bstack11ll11l11l1_opy_
            and bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST
        ):
            instance.data[bstack1lll11lllll_opy_.bstack11ll111ll1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack11lllll11l1_opy_ in bstack1lll11lllll_opy_.bstack11ll111llll_opy_:
            bstack11lllll11ll_opy_ = None
            for callback in bstack1lll11lllll_opy_.bstack11ll111llll_opy_[bstack11lllll11l1_opy_]:
                try:
                    bstack11llll1ll1l_opy_ = callback(self, target, exec, bstack1lll1l11lll_opy_, result, *args, **kwargs)
                    if bstack11lllll11ll_opy_ == None:
                        bstack11lllll11ll_opy_ = bstack11llll1ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᛛ") + str(e) + bstack11lllll_opy_ (u"ࠢࠣᛜ"))
                    traceback.print_exc()
            if bstack1lll11l1l1l_opy_ == bstack1lll1l1ll1l_opy_.QUIT:
                if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.PRE:
                    bstack1ll11111l_opy_ = bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, EVENTS.bstack11ll111ll11_opy_.value)
                    if bstack1ll11111l_opy_!=None:
                        bstack1lll11l1ll_opy_.end(EVENTS.bstack11ll111ll11_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᛝ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᛞ"), True, None)
                if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST:
                    bstack1ll11111l_opy_ = bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, EVENTS.bstack11ll111l1l1_opy_.value)
                    if bstack1ll11111l_opy_!=None:
                        bstack1lll11l1ll_opy_.end(EVENTS.bstack11ll111l1l1_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᛟ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛠ"), True, None)
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.PRE and callable(bstack11lllll11ll_opy_):
                return bstack11lllll11ll_opy_
            elif bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST and bstack11lllll11ll_opy_:
                return bstack11lllll11ll_opy_
    def bstack1ll1llll1ll_opy_(
        self, method_name, previous_state: bstack1lll1l1ll1l_opy_, *args, **kwargs
    ) -> bstack1lll1l1ll1l_opy_:
        if method_name == bstack11lllll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᛡ") or method_name == bstack11lllll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᛢ"):
            return bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_
        if method_name == bstack11lllll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᛣ"):
            return bstack1lll1l1ll1l_opy_.QUIT
        if method_name == bstack11lllll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᛤ"):
            if previous_state != bstack1lll1l1ll1l_opy_.NONE:
                command_name = bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args)
                if command_name == bstack1lll11lllll_opy_.bstack1l11111ll11_opy_:
                    return bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_
            return bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_
        return bstack1lll1l1ll1l_opy_.NONE