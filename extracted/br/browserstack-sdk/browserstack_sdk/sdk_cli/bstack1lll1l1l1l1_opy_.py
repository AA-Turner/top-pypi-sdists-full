# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1llllllll1l_opy_,
    bstack1lllllll111_opy_,
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1l1l1lll_opy_(bstack1llllllll1l_opy_):
    bstack1l11l1111ll_opy_ = bstack1l11ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᕺ")
    NAME = bstack1l11ll1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᕻ")
    bstack1l1l11l1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᕼ")
    bstack1l1l11l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᕽ")
    bstack11llll1l11l_opy_ = bstack1l11ll1_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕾ")
    bstack1l1l111lll1_opy_ = bstack1l11ll1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᕿ")
    bstack1l11l1l1l11_opy_ = bstack1l11ll1_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᖀ")
    bstack11llll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᖁ")
    bstack11llll111l1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᖂ")
    bstack1ll1111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᖃ")
    bstack1l11ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᖄ")
    bstack11llll11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠢࡨࡧࡷࠦᖅ")
    bstack1l1l1lllll1_opy_ = bstack1l11ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᖆ")
    bstack1l11l11l111_opy_ = bstack1l11ll1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᖇ")
    bstack1l11l111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᖈ")
    bstack11llll11l11_opy_ = bstack1l11ll1_opy_ (u"ࠦࡶࡻࡩࡵࠤᖉ")
    bstack11llll1l111_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11lll11l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1111l1l_opy_: Any
    bstack1l11l111lll_opy_: Dict
    def __init__(
        self,
        bstack1l11lll11l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1111l1l_opy_: Dict[str, Any],
        methods=[bstack1l11ll1_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᖊ"), bstack1l11ll1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᖋ"), bstack1l11ll1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖌ"), bstack1l11ll1_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᖍ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11lll11l1_opy_ = bstack1l11lll11l1_opy_
        self.platform_index = platform_index
        self.bstack1llllll11ll_opy_(methods)
        self.bstack1lll1111l1l_opy_ = bstack1lll1111l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllllll1l_opy_.get_data(bstack1ll1l1l1lll_opy_.bstack1l1l11l1l1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllllll1l_opy_.get_data(bstack1ll1l1l1lll_opy_.bstack1l1l11l1ll1_opy_, target, strict)
    @staticmethod
    def bstack11llll11lll_opy_(target: object, strict=True):
        return bstack1llllllll1l_opy_.get_data(bstack1ll1l1l1lll_opy_.bstack11llll1l11l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllllll1l_opy_.get_data(bstack1ll1l1l1lll_opy_.bstack1l1l111lll1_opy_, target, strict)
    @staticmethod
    def bstack1l1lllll1l1_opy_(instance: bstack1lllllll111_opy_) -> bool:
        return bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l11l1l1l11_opy_, False)
    @staticmethod
    def bstack1ll11lll111_opy_(instance: bstack1lllllll111_opy_, default_value=None):
        return bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll11l1ll1l_opy_(instance: bstack1lllllll111_opy_, default_value=None):
        return bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l1l111lll1_opy_, default_value)
    @staticmethod
    def bstack1ll11111ll1_opy_(hub_url: str, bstack11llll1l1l1_opy_=bstack1l11ll1_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᖎ")):
        try:
            bstack11llll1111l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1111l_opy_.endswith(bstack11llll1l1l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11l11l11_opy_(method_name: str):
        return method_name == bstack1l11ll1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᖏ")
    @staticmethod
    def bstack1ll11l1lll1_opy_(method_name: str, *args):
        return (
            bstack1ll1l1l1lll_opy_.bstack1ll11l11l11_opy_(method_name)
            and bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1l1l1lll_opy_.bstack1l11ll111ll_opy_
        )
    @staticmethod
    def bstack1ll111l111l_opy_(method_name: str, *args):
        if not bstack1ll1l1l1lll_opy_.bstack1ll11l11l11_opy_(method_name):
            return False
        if not bstack1ll1l1l1lll_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll11111111_opy_ = bstack1ll1l1l1lll_opy_.bstack1l1llllll1l_opy_(*args)
        return bstack1ll11111111_opy_ and bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᖐ") in bstack1ll11111111_opy_ and bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖑ") in bstack1ll11111111_opy_[bstack1l11ll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᖒ")]
    @staticmethod
    def bstack1ll11ll11l1_opy_(method_name: str, *args):
        if not bstack1ll1l1l1lll_opy_.bstack1ll11l11l11_opy_(method_name):
            return False
        if not bstack1ll1l1l1lll_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll11111111_opy_ = bstack1ll1l1l1lll_opy_.bstack1l1llllll1l_opy_(*args)
        return (
            bstack1ll11111111_opy_
            and bstack1l11ll1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᖓ") in bstack1ll11111111_opy_
            and bstack1l11ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᖔ") in bstack1ll11111111_opy_[bstack1l11ll1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᖕ")]
        )
    @staticmethod
    def bstack1l11ll1l11l_opy_(*args):
        return str(bstack1ll1l1l1lll_opy_.bstack1ll1l111111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1llllll1l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack111111111_opy_(driver):
        command_executor = getattr(driver, bstack1l11ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖖ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l11ll1_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᖗ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l11ll1_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᖘ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l11ll1_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᖙ"), None)
        return hub_url
    def bstack1l11ll1l1ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l11ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖚ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l11ll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᖛ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l11ll1_opy_ (u"ࠤࡢࡹࡷࡲࠢᖜ")):
                setattr(command_executor, bstack1l11ll1_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᖝ"), hub_url)
                result = True
        if result:
            self.bstack1l11lll11l1_opy_ = hub_url
            bstack1ll1l1l1lll_opy_.bstack1llllll1ll1_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l1l11l1ll1_opy_, hub_url)
            bstack1ll1l1l1lll_opy_.bstack1llllll1ll1_opy_(
                instance, bstack1ll1l1l1lll_opy_.bstack1l11l1l1l11_opy_, bstack1ll1l1l1lll_opy_.bstack1ll11111ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_]):
        return bstack1l11ll1_opy_ (u"ࠦ࠿ࠨᖞ").join((bstack1lllll1l111_opy_(bstack1lllll1llll_opy_[0]).name, bstack1llll1l11ll_opy_(bstack1lllll1llll_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll111l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1ll1l1l1lll_opy_.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        if not bstack1l11l111l11_opy_ in bstack1ll1l1l1lll_opy_.bstack11llll1l111_opy_:
            bstack1ll1l1l1lll_opy_.bstack11llll1l111_opy_[bstack1l11l111l11_opy_] = []
        bstack1ll1l1l1lll_opy_.bstack11llll1l111_opy_[bstack1l11l111l11_opy_].append(callback)
    def bstack1llll1ll1l1_opy_(self, instance: bstack1lllllll111_opy_, method_name: str, bstack1lllll1ll1l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l11ll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᖟ")):
            return
        cmd = args[0] if method_name == bstack1l11ll1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᖠ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll11ll1_opy_ = bstack1l11ll1_opy_ (u"ࠢ࠻ࠤᖡ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᖢ") + bstack11llll11ll1_opy_, bstack1lllll1ll1l_opy_)
    def bstack1llll1l11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1l1l11_opy_, bstack1l11l11l1l1_opy_ = bstack1lllll1llll_opy_
        bstack1l11l111l11_opy_ = bstack1ll1l1l1lll_opy_.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᖣ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠥࠦᖤ"))
        if bstack1llll1l1l11_opy_ == bstack1lllll1l111_opy_.QUIT:
            if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.PRE:
                bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1ll1llll1_opy_.value)
                bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, EVENTS.bstack1ll1llll1_opy_.value, bstack1ll111l1lll_opy_)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᖥ").format(instance, method_name, bstack1llll1l1l11_opy_, bstack1l11l11l1l1_opy_))
        if bstack1llll1l1l11_opy_ == bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_:
            if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST and not bstack1ll1l1l1lll_opy_.bstack1l1l11l1l1l_opy_ in instance.data:
                session_id = getattr(target, bstack1l11ll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᖦ"), None)
                if session_id:
                    instance.data[bstack1ll1l1l1lll_opy_.bstack1l1l11l1l1l_opy_] = session_id
        elif (
            bstack1llll1l1l11_opy_ == bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_
            and bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1l1l1lll_opy_.bstack1l11ll111ll_opy_
        ):
            if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.PRE:
                hub_url = bstack1ll1l1l1lll_opy_.bstack111111111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1l1l1lll_opy_.bstack1l1l11l1ll1_opy_: hub_url,
                            bstack1ll1l1l1lll_opy_.bstack1l11l1l1l11_opy_: bstack1ll1l1l1lll_opy_.bstack1ll11111ll1_opy_(hub_url),
                            bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_: int(
                                os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᖧ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11111111_opy_ = bstack1ll1l1l1lll_opy_.bstack1l1llllll1l_opy_(*args)
                bstack11llll11lll_opy_ = bstack1ll11111111_opy_.get(bstack1l11ll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᖨ"), None) if bstack1ll11111111_opy_ else None
                if isinstance(bstack11llll11lll_opy_, dict):
                    instance.data[bstack1ll1l1l1lll_opy_.bstack11llll1l11l_opy_] = copy.deepcopy(bstack11llll11lll_opy_)
                    instance.data[bstack1ll1l1l1lll_opy_.bstack1l1l111lll1_opy_] = bstack11llll11lll_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l11ll1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᖩ"), dict()).get(bstack1l11ll1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᖪ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1l1l1lll_opy_.bstack1l1l11l1l1l_opy_: framework_session_id,
                                bstack1ll1l1l1lll_opy_.bstack11llll111ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1llll1l1l11_opy_ == bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_
            and bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1l1l1lll_opy_.bstack11llll11l11_opy_
            and bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST
        ):
            instance.data[bstack1ll1l1l1lll_opy_.bstack11llll111l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l111l11_opy_ in bstack1ll1l1l1lll_opy_.bstack11llll1l111_opy_:
            bstack1l11l111l1l_opy_ = None
            for callback in bstack1ll1l1l1lll_opy_.bstack11llll1l111_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11ll11_opy_ = callback(self, target, exec, bstack1lllll1llll_opy_, result, *args, **kwargs)
                    if bstack1l11l111l1l_opy_ == None:
                        bstack1l11l111l1l_opy_ = bstack1l11l11ll11_opy_
                except Exception as e:
                    self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᖫ") + str(e) + bstack1l11ll1_opy_ (u"ࠦࠧᖬ"))
                    traceback.print_exc()
            if bstack1llll1l1l11_opy_ == bstack1lllll1l111_opy_.QUIT:
                if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST:
                    bstack1ll111l1lll_opy_ = bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, EVENTS.bstack1ll1llll1_opy_.value)
                    if bstack1ll111l1lll_opy_!=None:
                        bstack1lll11111l1_opy_.end(EVENTS.bstack1ll1llll1_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᖭ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᖮ"), True, None)
            if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.PRE and callable(bstack1l11l111l1l_opy_):
                return bstack1l11l111l1l_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST and bstack1l11l111l1l_opy_:
                return bstack1l11l111l1l_opy_
    def bstack1llll1ll11l_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1l11ll1_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᖯ") or method_name == bstack1l11ll1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᖰ"):
            return bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_
        if method_name == bstack1l11ll1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᖱ"):
            return bstack1lllll1l111_opy_.QUIT
        if method_name == bstack1l11ll1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᖲ"):
            if previous_state != bstack1lllll1l111_opy_.NONE:
                command_name = bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args)
                if command_name == bstack1ll1l1l1lll_opy_.bstack1l11ll111ll_opy_:
                    return bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_
            return bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_
        return bstack1lllll1l111_opy_.NONE