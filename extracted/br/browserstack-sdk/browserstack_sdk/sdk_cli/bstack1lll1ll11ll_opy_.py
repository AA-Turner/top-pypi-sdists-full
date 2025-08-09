# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1lllll111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1llllll_opy_(bstack1lllll111ll_opy_):
    bstack1l11l11lll1_opy_ = bstack11l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᐉ")
    bstack1l1l11l1l11_opy_ = bstack11l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᐊ")
    bstack1l1l1l11111_opy_ = bstack11l1_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᐋ")
    bstack1l1l11l1lll_opy_ = bstack11l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᐌ")
    bstack1l11l1l11ll_opy_ = bstack11l1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᐍ")
    bstack1l11l1l1l11_opy_ = bstack11l1_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᐎ")
    NAME = bstack11l1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᐏ")
    bstack1l11l11l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l1ll1l_opy_: Any
    bstack1l11l1l111l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᐐ"), bstack11l1_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᐑ"), bstack11l1_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᐒ"), bstack11l1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᐓ"), bstack11l1_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᐔ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1111111111_opy_(methods)
    def bstack1111111ll1_opy_(self, instance: bstack1lllll1ll1l_opy_, method_name: str, bstack1llllll11l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1111111l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1lll1l_opy_, bstack1l11l11llll_opy_ = bstack1lllllll11l_opy_
        bstack1l11l1l11l1_opy_ = bstack1lll1llllll_opy_.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        if bstack1l11l1l11l1_opy_ in bstack1lll1llllll_opy_.bstack1l11l11l1ll_opy_:
            bstack1l11l11ll11_opy_ = None
            for callback in bstack1lll1llllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l1l11l1_opy_]:
                try:
                    bstack1l11l11ll1l_opy_ = callback(self, target, exec, bstack1lllllll11l_opy_, result, *args, **kwargs)
                    if bstack1l11l11ll11_opy_ == None:
                        bstack1l11l11ll11_opy_ = bstack1l11l11ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᐕ") + str(e) + bstack11l1_opy_ (u"ࠦࠧᐖ"))
                    traceback.print_exc()
            if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.PRE and callable(bstack1l11l11ll11_opy_):
                return bstack1l11l11ll11_opy_
            elif bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST and bstack1l11l11ll11_opy_:
                return bstack1l11l11ll11_opy_
    def bstack111111111l_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        if method_name == bstack11l1_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬᐗ") or method_name == bstack11l1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᐘ") or method_name == bstack11l1_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩᐙ"):
            return bstack1llllllllll_opy_.bstack1llllll11ll_opy_
        if method_name == bstack11l1_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪᐚ"):
            return bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_
        if method_name == bstack11l1_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨᐛ"):
            return bstack1llllllllll_opy_.QUIT
        return bstack1llllllllll_opy_.NONE
    @staticmethod
    def bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_]):
        return bstack11l1_opy_ (u"ࠥ࠾ࠧᐜ").join((bstack1llllllllll_opy_(bstack1lllllll11l_opy_[0]).name, bstack1llll1lll11_opy_(bstack1lllllll11l_opy_[1]).name))
    @staticmethod
    def bstack1ll11lll111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_], callback: Callable):
        bstack1l11l1l11l1_opy_ = bstack1lll1llllll_opy_.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        if not bstack1l11l1l11l1_opy_ in bstack1lll1llllll_opy_.bstack1l11l11l1ll_opy_:
            bstack1lll1llllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l1l11l1_opy_] = []
        bstack1lll1llllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l1l11l1_opy_].append(callback)
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll111l1111_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11l1llll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l11l1lll_opy_, default_value)
    @staticmethod
    def bstack1ll11111l11_opy_(instance: bstack1lllll1ll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll111ll1ll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1ll1l11l11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll11ll_opy_(method_name: str, *args):
        if not bstack1lll1llllll_opy_.bstack1ll11ll111l_opy_(method_name):
            return False
        if not bstack1lll1llllll_opy_.bstack1l11l1l11ll_opy_ in bstack1lll1llllll_opy_.bstack1l11lllll11_opy_(*args):
            return False
        bstack1ll1111llll_opy_ = bstack1lll1llllll_opy_.bstack1ll11111lll_opy_(*args)
        return bstack1ll1111llll_opy_ and bstack11l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐝ") in bstack1ll1111llll_opy_ and bstack11l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᐞ") in bstack1ll1111llll_opy_[bstack11l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐟ")]
    @staticmethod
    def bstack1ll1l1111l1_opy_(method_name: str, *args):
        if not bstack1lll1llllll_opy_.bstack1ll11ll111l_opy_(method_name):
            return False
        if not bstack1lll1llllll_opy_.bstack1l11l1l11ll_opy_ in bstack1lll1llllll_opy_.bstack1l11lllll11_opy_(*args):
            return False
        bstack1ll1111llll_opy_ = bstack1lll1llllll_opy_.bstack1ll11111lll_opy_(*args)
        return (
            bstack1ll1111llll_opy_
            and bstack11l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᐠ") in bstack1ll1111llll_opy_
            and bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᐡ") in bstack1ll1111llll_opy_[bstack11l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐢ")]
        )
    @staticmethod
    def bstack1l11lllll11_opy_(*args):
        return str(bstack1lll1llllll_opy_.bstack1ll1l11l11l_opy_(*args)).lower()