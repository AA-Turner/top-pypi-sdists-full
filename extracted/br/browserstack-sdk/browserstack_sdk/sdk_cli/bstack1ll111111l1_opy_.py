# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack111l1ll111_opy_,
    bstack1ll111lllll_opy_,
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from bstack_utils.constants import EVENTS
class bstack1ll11111111_opy_(bstack111l1ll111_opy_):
    bstack11l1llll11l_opy_ = bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᦚ")
    NAME = bstack1ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᦛ")
    bstack1ll11l1lll_opy_ = bstack1ll11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᦜ")
    bstack1ll1l1l1lll_opy_ = bstack1ll11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᦝ")
    bstack11l1111llll_opy_ = bstack1ll11_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᦞ")
    bstack1lll1l1111_opy_ = bstack1ll11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᦟ")
    bstack11ll111lll1_opy_ = bstack1ll11_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᦠ")
    bstack11l111l111l_opy_ = bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᦡ")
    bstack11l111l11l1_opy_ = bstack1ll11_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧᦢ")
    bstack1l11llll11l_opy_ = bstack1ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᦣ")
    bstack11ll1l11lll_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤᦤ")
    bstack11l1111l11l_opy_ = bstack1ll11_opy_ (u"ࠨࡧࡦࡶࠥᦥ")
    bstack11llll1ll11_opy_ = bstack1ll11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᦦ")
    bstack11l1llll1l1_opy_ = bstack1ll11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᦧ")
    bstack11l1lllll1l_opy_ = bstack1ll11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᦨ")
    bstack11l1111ll11_opy_ = bstack1ll11_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᦩ")
    bstack11l1111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack11ll1l1ll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1lll11l_opy_: Any
    bstack11l1lllllll_opy_: Dict
    def __init__(
        self,
        bstack11ll1l1ll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1l1lll11l_opy_: Dict[str, Any],
        methods=[bstack1ll11_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᦪ"), bstack1ll11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᦫ"), bstack1ll11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢ᦬"), bstack1ll11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ᦭")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11ll1l1ll11_opy_ = bstack11ll1l1ll11_opy_
        self.platform_index = platform_index
        self.bstack1ll11l1ll1l_opy_(methods)
        self.bstack1l1l1lll11l_opy_ = bstack1l1l1lll11l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack111l1ll111_opy_.get_data(bstack1ll11111111_opy_.bstack1ll1l1l1lll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack111l1ll111_opy_.get_data(bstack1ll11111111_opy_.bstack1ll11l1lll_opy_, target, strict)
    @staticmethod
    def bstack11l111l1111_opy_(target: object, strict=True):
        return bstack111l1ll111_opy_.get_data(bstack1ll11111111_opy_.bstack11l1111llll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack111l1ll111_opy_.get_data(bstack1ll11111111_opy_.bstack1lll1l1111_opy_, target, strict)
    @staticmethod
    def bstack1l11l111111_opy_(instance: bstack1ll111lllll_opy_) -> bool:
        return bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack11ll111lll1_opy_, False)
    @staticmethod
    def bstack1l11ll11lll_opy_(instance: bstack1ll111lllll_opy_, default_value=None):
        return bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1ll11l1lll_opy_, default_value)
    @staticmethod
    def bstack1l1l111111l_opy_(instance: bstack1ll111lllll_opy_, default_value=None):
        return bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1lll1l1111_opy_, default_value)
    @staticmethod
    def bstack1l11l1111l1_opy_(hub_url: str, bstack11l1111l111_opy_=bstack1ll11_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ᦮")):
        try:
            bstack11l1111l1l1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1111l1l1_opy_.endswith(bstack11l1111l111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l11l1l1lll_opy_(method_name: str):
        return method_name == bstack1ll11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᦯")
    @staticmethod
    def bstack1l11ll1l1ll_opy_(method_name: str, *args):
        return (
            bstack1ll11111111_opy_.bstack1l11l1l1lll_opy_(method_name)
            and bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args) == bstack1ll11111111_opy_.bstack11ll1l11lll_opy_
        )
    @staticmethod
    def bstack1l11lll11ll_opy_(method_name: str, *args):
        if not bstack1ll11111111_opy_.bstack1l11l1l1lll_opy_(method_name):
            return False
        if not bstack1ll11111111_opy_.bstack11l1llll1l1_opy_ in bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args):
            return False
        bstack1l11l1111ll_opy_ = bstack1ll11111111_opy_.bstack1l11l11l1ll_opy_(*args)
        return bstack1l11l1111ll_opy_ and bstack1ll11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᦰ") in bstack1l11l1111ll_opy_ and bstack1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᦱ") in bstack1l11l1111ll_opy_[bstack1ll11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᦲ")]
    @staticmethod
    def bstack1l11ll11ll1_opy_(method_name: str, *args):
        if not bstack1ll11111111_opy_.bstack1l11l1l1lll_opy_(method_name):
            return False
        if not bstack1ll11111111_opy_.bstack11l1llll1l1_opy_ in bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args):
            return False
        bstack1l11l1111ll_opy_ = bstack1ll11111111_opy_.bstack1l11l11l1ll_opy_(*args)
        return (
            bstack1l11l1111ll_opy_
            and bstack1ll11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᦳ") in bstack1l11l1111ll_opy_
            and bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᦴ") in bstack1l11l1111ll_opy_[bstack1ll11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᦵ")]
        )
    @staticmethod
    def bstack11ll11l1l11_opy_(*args):
        return str(bstack1ll11111111_opy_.bstack1l1l111ll11_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l111ll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11l11l1ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l111llll1_opy_(driver):
        command_executor = getattr(driver, bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᦶ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll11_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᦷ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll11_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧᦸ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᦹ"), None)
        return hub_url
    def bstack11ll11lll1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᦺ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᦻ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll11_opy_ (u"ࠣࡡࡸࡶࡱࠨᦼ")):
                setattr(command_executor, bstack1ll11_opy_ (u"ࠤࡢࡹࡷࡲࠢᦽ"), hub_url)
                result = True
        if result:
            self.bstack11ll1l1ll11_opy_ = hub_url
            bstack1ll11111111_opy_.bstack1l11lllll_opy_(instance, bstack1ll11111111_opy_.bstack1ll11l1lll_opy_, hub_url)
            bstack1ll11111111_opy_.bstack1l11lllll_opy_(
                instance, bstack1ll11111111_opy_.bstack11ll111lll1_opy_, bstack1ll11111111_opy_.bstack1l11l1111l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_]):
        return bstack1ll11_opy_ (u"ࠥ࠾ࠧᦾ").join((bstack1ll1l1ll11_opy_(bstack1ll11l11lll_opy_[0]).name, bstack1ll11ll1ll_opy_(bstack1ll11l11lll_opy_[1]).name))
    @staticmethod
    def bstack1l11lll1lll_opy_(bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_], callback: Callable):
        bstack11l1llll111_opy_ = bstack1ll11111111_opy_.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        if not bstack11l1llll111_opy_ in bstack1ll11111111_opy_.bstack11l1111l1ll_opy_:
            bstack1ll11111111_opy_.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_] = []
        bstack1ll11111111_opy_.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_].append(callback)
    def bstack1ll11l11111_opy_(self, instance: bstack1ll111lllll_opy_, method_name: str, bstack1ll11ll111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᦿ")):
            return
        cmd = args[0] if method_name == bstack1ll11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᧀ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l111l11ll_opy_ = bstack1ll11_opy_ (u"ࠨ࠺ࠣᧁ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᧂ") + bstack11l111l11ll_opy_, bstack1ll11ll111l_opy_)
    def bstack1ll1ll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll111l1ll1_opy_, bstack11l1lllll11_opy_ = bstack1ll11l11lll_opy_
        bstack11l1llll111_opy_ = bstack1ll11111111_opy_.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᧃ") + str(kwargs) + bstack1ll11_opy_ (u"ࠤࠥᧄ"))
        if bstack1ll111l1ll1_opy_ == bstack1ll1l1ll11_opy_.QUIT:
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.PRE:
                bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l1111lll1_opy_.value)
                bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, EVENTS.bstack11l1111lll1_opy_.value, bstack1l11ll1ll1_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᧅ").format(instance, method_name, bstack1ll111l1ll1_opy_, bstack11l1lllll11_opy_))
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST:
                bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l1111ll1l_opy_.value)
                bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, EVENTS.bstack11l1111ll1l_opy_.value, bstack1l11ll1ll1_opy_)
        if bstack1ll111l1ll1_opy_ == bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_:
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST and not bstack1ll11111111_opy_.bstack1ll1l1l1lll_opy_ in instance.data:
                session_id = getattr(target, bstack1ll11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᧆ"), None)
                if session_id:
                    instance.data[bstack1ll11111111_opy_.bstack1ll1l1l1lll_opy_] = session_id
        elif (
            bstack1ll111l1ll1_opy_ == bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_
            and bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args) == bstack1ll11111111_opy_.bstack11ll1l11lll_opy_
        ):
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.PRE:
                hub_url = bstack1ll11111111_opy_.bstack1l111llll1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll11111111_opy_.bstack1ll11l1lll_opy_: hub_url,
                            bstack1ll11111111_opy_.bstack11ll111lll1_opy_: bstack1ll11111111_opy_.bstack1l11l1111l1_opy_(hub_url),
                            bstack1ll11111111_opy_.bstack1l11llll11l_opy_: int(
                                os.environ.get(bstack1ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᧇ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11l1111ll_opy_ = bstack1ll11111111_opy_.bstack1l11l11l1ll_opy_(*args)
                bstack11l111l1111_opy_ = bstack1l11l1111ll_opy_.get(bstack1ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᧈ"), None) if bstack1l11l1111ll_opy_ else None
                if isinstance(bstack11l111l1111_opy_, dict):
                    instance.data[bstack1ll11111111_opy_.bstack11l1111llll_opy_] = copy.deepcopy(bstack11l111l1111_opy_)
                    instance.data[bstack1ll11111111_opy_.bstack1lll1l1111_opy_] = bstack11l111l1111_opy_
            elif bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᧉ"), dict()).get(bstack1ll11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦ᧊"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll11111111_opy_.bstack1ll1l1l1lll_opy_: framework_session_id,
                                bstack1ll11111111_opy_.bstack11l111l111l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll111l1ll1_opy_ == bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_
            and bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args) == bstack1ll11111111_opy_.bstack11l1111ll11_opy_
            and bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST
        ):
            instance.data[bstack1ll11111111_opy_.bstack11l111l11l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l1llll111_opy_ in bstack1ll11111111_opy_.bstack11l1111l1ll_opy_:
            bstack11l1llllll1_opy_ = None
            for callback in bstack1ll11111111_opy_.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_]:
                try:
                    bstack11ll1111111_opy_ = callback(self, target, exec, bstack1ll11l11lll_opy_, result, *args, **kwargs)
                    if bstack11l1llllll1_opy_ == None:
                        bstack11l1llllll1_opy_ = bstack11ll1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢ᧋") + str(e) + bstack1ll11_opy_ (u"ࠥࠦ᧌"))
                    traceback.print_exc()
            if bstack1ll111l1ll1_opy_ == bstack1ll1l1ll11_opy_.QUIT:
                if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.PRE:
                    bstack1l11ll1ll1_opy_ = bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, EVENTS.bstack11l1111lll1_opy_.value)
                    if bstack1l11ll1ll1_opy_!=None:
                        bstack11ll11l1ll_opy_.end(EVENTS.bstack11l1111lll1_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᧍"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᧎"), True, None)
                if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST:
                    bstack1l11ll1ll1_opy_ = bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, EVENTS.bstack11l1111ll1l_opy_.value)
                    if bstack1l11ll1ll1_opy_!=None:
                        bstack11ll11l1ll_opy_.end(EVENTS.bstack11l1111ll1l_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᧏"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᧐"), True, None)
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.PRE and callable(bstack11l1llllll1_opy_):
                return bstack11l1llllll1_opy_
            elif bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST and bstack11l1llllll1_opy_:
                return bstack11l1llllll1_opy_
    def bstack1ll11l111l1_opy_(
        self, method_name, previous_state: bstack1ll1l1ll11_opy_, *args, **kwargs
    ) -> bstack1ll1l1ll11_opy_:
        if method_name == bstack1ll11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥ᧑") or method_name == bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤ᧒"):
            return bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_
        if method_name == bstack1ll11_opy_ (u"ࠥࡵࡺ࡯ࡴࠣ᧓"):
            return bstack1ll1l1ll11_opy_.QUIT
        if method_name == bstack1ll11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧ᧔"):
            if previous_state != bstack1ll1l1ll11_opy_.NONE:
                command_name = bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args)
                if command_name == bstack1ll11111111_opy_.bstack11ll1l11lll_opy_:
                    return bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_
            return bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_
        return bstack1ll1l1ll11_opy_.NONE