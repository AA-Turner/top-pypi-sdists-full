# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111llll_opy_,
    bstack1lll11lll1l_opy_,
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1ll1lll1_opy_(bstack1lll111llll_opy_):
    bstack11llllll111_opy_ = bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᚊ")
    NAME = bstack11l1ll1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᚋ")
    bstack1l111llll11_opy_ = bstack11l1ll1_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᚌ")
    bstack1l111lll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᚍ")
    bstack11ll11l1l11_opy_ = bstack11l1ll1_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᚎ")
    bstack1l11l111lll_opy_ = bstack11l1ll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᚏ")
    bstack1l111111l11_opy_ = bstack11l1ll1_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᚐ")
    bstack11ll11ll11l_opy_ = bstack11l1ll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᚑ")
    bstack11ll11l1111_opy_ = bstack11l1ll1_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧᚒ")
    bstack1l1l1lll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᚓ")
    bstack1l11111llll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤᚔ")
    bstack11ll11l11l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡧࡦࡶࠥᚕ")
    bstack1l1l11l11ll_opy_ = bstack11l1ll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᚖ")
    bstack11lllll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᚗ")
    bstack11lllllll11_opy_ = bstack11l1ll1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᚘ")
    bstack11ll111llll_opy_ = bstack11l1ll1_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᚙ")
    bstack11ll11l1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1111l1l1l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1lll1l1l_opy_: Any
    bstack11lllll1ll1_opy_: Dict
    def __init__(
        self,
        bstack1l1111l1l1l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1lll1l1l_opy_: Dict[str, Any],
        methods=[bstack11l1ll1_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᚚ"), bstack11l1ll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᚛"), bstack11l1ll1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢ᚜"), bstack11l1ll1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ᚝")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1111l1l1l_opy_ = bstack1l1111l1l1l_opy_
        self.platform_index = platform_index
        self.bstack1lll11l1l11_opy_(methods)
        self.bstack1ll1lll1l1l_opy_ = bstack1ll1lll1l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll111llll_opy_.get_data(bstack1ll1ll1lll1_opy_.bstack1l111lll1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll111llll_opy_.get_data(bstack1ll1ll1lll1_opy_.bstack1l111llll11_opy_, target, strict)
    @staticmethod
    def bstack11ll11l1lll_opy_(target: object, strict=True):
        return bstack1lll111llll_opy_.get_data(bstack1ll1ll1lll1_opy_.bstack11ll11l1l11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll111llll_opy_.get_data(bstack1ll1ll1lll1_opy_.bstack1l11l111lll_opy_, target, strict)
    @staticmethod
    def bstack1l1l1l11ll1_opy_(instance: bstack1lll11lll1l_opy_) -> bool:
        return bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111111l11_opy_, False)
    @staticmethod
    def bstack1l1l1llllll_opy_(instance: bstack1lll11lll1l_opy_, default_value=None):
        return bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111llll11_opy_, default_value)
    @staticmethod
    def bstack1l1llll111l_opy_(instance: bstack1lll11lll1l_opy_, default_value=None):
        return bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l11l111lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1ll11l1_opy_(hub_url: str, bstack11ll11l111l_opy_=bstack11l1ll1_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ᚞")):
        try:
            bstack11ll11ll111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11ll11ll111_opy_.endswith(bstack11ll11l111l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1ll111111_opy_(method_name: str):
        return method_name == bstack11l1ll1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᚟")
    @staticmethod
    def bstack1l1ll11l1l1_opy_(method_name: str, *args):
        return (
            bstack1ll1ll1lll1_opy_.bstack1l1ll111111_opy_(method_name)
            and bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args) == bstack1ll1ll1lll1_opy_.bstack1l11111llll_opy_
        )
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(method_name: str, *args):
        if not bstack1ll1ll1lll1_opy_.bstack1l1ll111111_opy_(method_name):
            return False
        if not bstack1ll1ll1lll1_opy_.bstack11lllll1l11_opy_ in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args):
            return False
        bstack1l1l1l1llll_opy_ = bstack1ll1ll1lll1_opy_.bstack1l1l1lll111_opy_(*args)
        return bstack1l1l1l1llll_opy_ and bstack11l1ll1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᚠ") in bstack1l1l1l1llll_opy_ and bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᚡ") in bstack1l1l1l1llll_opy_[bstack11l1ll1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᚢ")]
    @staticmethod
    def bstack1l1ll11111l_opy_(method_name: str, *args):
        if not bstack1ll1ll1lll1_opy_.bstack1l1ll111111_opy_(method_name):
            return False
        if not bstack1ll1ll1lll1_opy_.bstack11lllll1l11_opy_ in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args):
            return False
        bstack1l1l1l1llll_opy_ = bstack1ll1ll1lll1_opy_.bstack1l1l1lll111_opy_(*args)
        return (
            bstack1l1l1l1llll_opy_
            and bstack11l1ll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᚣ") in bstack1l1l1l1llll_opy_
            and bstack11l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᚤ") in bstack1l1l1l1llll_opy_[bstack11l1ll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᚥ")]
        )
    @staticmethod
    def bstack1l1111ll111_opy_(*args):
        return str(bstack1ll1ll1lll1_opy_.bstack1l1llll11l1_opy_(*args)).lower()
    @staticmethod
    def bstack1l1llll11l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1lll111_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1l111ll_opy_(driver):
        command_executor = getattr(driver, bstack11l1ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᚦ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1ll1_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᚧ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1ll1_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧᚨ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1ll1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᚩ"), None)
        return hub_url
    def bstack1l1111l11l1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᚪ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᚫ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1ll1_opy_ (u"ࠣࡡࡸࡶࡱࠨᚬ")):
                setattr(command_executor, bstack11l1ll1_opy_ (u"ࠤࡢࡹࡷࡲࠢᚭ"), hub_url)
                result = True
        if result:
            self.bstack1l1111l1l1l_opy_ = hub_url
            bstack1ll1ll1lll1_opy_.bstack1lll1l1111l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111llll11_opy_, hub_url)
            bstack1ll1ll1lll1_opy_.bstack1lll1l1111l_opy_(
                instance, bstack1ll1ll1lll1_opy_.bstack1l111111l11_opy_, bstack1ll1ll1lll1_opy_.bstack1l1l1ll11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_]):
        return bstack11l1ll1_opy_ (u"ࠥ࠾ࠧᚮ").join((bstack1lll111lll1_opy_(bstack1lll1l1ll11_opy_[0]).name, bstack1lll1ll1l11_opy_(bstack1lll1l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l1ll11llll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_], callback: Callable):
        bstack11lllll1lll_opy_ = bstack1ll1ll1lll1_opy_.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        if not bstack11lllll1lll_opy_ in bstack1ll1ll1lll1_opy_.bstack11ll11l1ll1_opy_:
            bstack1ll1ll1lll1_opy_.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_] = []
        bstack1ll1ll1lll1_opy_.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_].append(callback)
    def bstack1lll1lll1l1_opy_(self, instance: bstack1lll11lll1l_opy_, method_name: str, bstack1lll111ll1l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1ll1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᚯ")):
            return
        cmd = args[0] if method_name == bstack11l1ll1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᚰ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11ll111lll1_opy_ = bstack11l1ll1_opy_ (u"ࠨ࠺ࠣᚱ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᚲ") + bstack11ll111lll1_opy_, bstack1lll111ll1l_opy_)
    def bstack1lll11llll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll1ll1111_opy_, bstack11llllll1l1_opy_ = bstack1lll1l1ll11_opy_
        bstack11lllll1lll_opy_ = bstack1ll1ll1lll1_opy_.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᚳ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᚴ"))
        if bstack1lll1ll1111_opy_ == bstack1lll111lll1_opy_.QUIT:
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.PRE:
                bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11ll11l1l1l_opy_.value)
                bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, EVENTS.bstack11ll11l1l1l_opy_.value, bstack1lll1llll1_opy_)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᚵ").format(instance, method_name, bstack1lll1ll1111_opy_, bstack11llllll1l1_opy_))
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST:
                bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11ll11l11ll_opy_.value)
                bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, EVENTS.bstack11ll11l11ll_opy_.value, bstack1lll1llll1_opy_)
        if bstack1lll1ll1111_opy_ == bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_:
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST and not bstack1ll1ll1lll1_opy_.bstack1l111lll1ll_opy_ in instance.data:
                session_id = getattr(target, bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᚶ"), None)
                if session_id:
                    instance.data[bstack1ll1ll1lll1_opy_.bstack1l111lll1ll_opy_] = session_id
        elif (
            bstack1lll1ll1111_opy_ == bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_
            and bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args) == bstack1ll1ll1lll1_opy_.bstack1l11111llll_opy_
        ):
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.PRE:
                hub_url = bstack1ll1ll1lll1_opy_.bstack1l1l111ll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1ll1lll1_opy_.bstack1l111llll11_opy_: hub_url,
                            bstack1ll1ll1lll1_opy_.bstack1l111111l11_opy_: bstack1ll1ll1lll1_opy_.bstack1l1l1ll11l1_opy_(hub_url),
                            bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_: int(
                                os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᚷ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l1l1llll_opy_ = bstack1ll1ll1lll1_opy_.bstack1l1l1lll111_opy_(*args)
                bstack11ll11l1lll_opy_ = bstack1l1l1l1llll_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᚸ"), None) if bstack1l1l1l1llll_opy_ else None
                if isinstance(bstack11ll11l1lll_opy_, dict):
                    instance.data[bstack1ll1ll1lll1_opy_.bstack11ll11l1l11_opy_] = copy.deepcopy(bstack11ll11l1lll_opy_)
                    instance.data[bstack1ll1ll1lll1_opy_.bstack1l11l111lll_opy_] = bstack11ll11l1lll_opy_
            elif bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1ll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᚹ"), dict()).get(bstack11l1ll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᚺ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1ll1lll1_opy_.bstack1l111lll1ll_opy_: framework_session_id,
                                bstack1ll1ll1lll1_opy_.bstack11ll11ll11l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll1ll1111_opy_ == bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_
            and bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args) == bstack1ll1ll1lll1_opy_.bstack11ll111llll_opy_
            and bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST
        ):
            instance.data[bstack1ll1ll1lll1_opy_.bstack11ll11l1111_opy_] = datetime.now(tz=timezone.utc)
        if bstack11lllll1lll_opy_ in bstack1ll1ll1lll1_opy_.bstack11ll11l1ll1_opy_:
            bstack11llllll11l_opy_ = None
            for callback in bstack1ll1ll1lll1_opy_.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_]:
                try:
                    bstack11lllllll1l_opy_ = callback(self, target, exec, bstack1lll1l1ll11_opy_, result, *args, **kwargs)
                    if bstack11llllll11l_opy_ == None:
                        bstack11llllll11l_opy_ = bstack11lllllll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᚻ") + str(e) + bstack11l1ll1_opy_ (u"ࠥࠦᚼ"))
                    traceback.print_exc()
            if bstack1lll1ll1111_opy_ == bstack1lll111lll1_opy_.QUIT:
                if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.PRE:
                    bstack1lll1llll1_opy_ = bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, EVENTS.bstack11ll11l1l1l_opy_.value)
                    if bstack1lll1llll1_opy_!=None:
                        bstack1ll1111ll_opy_.end(EVENTS.bstack11ll11l1l1l_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᚽ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᚾ"), True, None)
                if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST:
                    bstack1lll1llll1_opy_ = bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, EVENTS.bstack11ll11l11ll_opy_.value)
                    if bstack1lll1llll1_opy_!=None:
                        bstack1ll1111ll_opy_.end(EVENTS.bstack11ll11l11ll_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᚿ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛀ"), True, None)
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.PRE and callable(bstack11llllll11l_opy_):
                return bstack11llllll11l_opy_
            elif bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST and bstack11llllll11l_opy_:
                return bstack11llllll11l_opy_
    def bstack1lll1ll1ll1_opy_(
        self, method_name, previous_state: bstack1lll111lll1_opy_, *args, **kwargs
    ) -> bstack1lll111lll1_opy_:
        if method_name == bstack11l1ll1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᛁ") or method_name == bstack11l1ll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᛂ"):
            return bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_
        if method_name == bstack11l1ll1_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᛃ"):
            return bstack1lll111lll1_opy_.QUIT
        if method_name == bstack11l1ll1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᛄ"):
            if previous_state != bstack1lll111lll1_opy_.NONE:
                command_name = bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args)
                if command_name == bstack1ll1ll1lll1_opy_.bstack1l11111llll_opy_:
                    return bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_
            return bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_
        return bstack1lll111lll1_opy_.NONE