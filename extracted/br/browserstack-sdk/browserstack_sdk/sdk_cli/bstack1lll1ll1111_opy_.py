# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lllll11111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1l1lll_opy_,
    bstack1lllllllll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll1l11l1_opy_(bstack1lllll11111_opy_):
    bstack1l11l11l1l1_opy_ = bstack1l11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᐈ")
    bstack1l1l11l11ll_opy_ = bstack1l11l11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᐉ")
    bstack1l1l11lll11_opy_ = bstack1l11l11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᐊ")
    bstack1l1l11l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᐋ")
    bstack1l11l11l1ll_opy_ = bstack1l11l11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᐌ")
    bstack1l11l11ll11_opy_ = bstack1l11l11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᐍ")
    NAME = bstack1l11l11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᐎ")
    bstack1l11l111lll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll111ll_opy_: Any
    bstack1l11l11ll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11l11_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᐏ"), bstack1l11l11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᐐ"), bstack1l11l11_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᐑ"), bstack1l11l11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᐒ"), bstack1l11l11_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᐓ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llll1lll1l_opy_(methods)
    def bstack111111111l_opy_(self, instance: bstack1lllll111ll_opy_, method_name: str, bstack11111111l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lllllll1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll111ll_opy_, str],
        bstack1llllll11l1_opy_: Tuple[bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll1l1l1_opy_, bstack1l11l11l11l_opy_ = bstack1llllll11l1_opy_
        bstack1l11l11l111_opy_ = bstack1llll1l11l1_opy_.bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_)
        if bstack1l11l11l111_opy_ in bstack1llll1l11l1_opy_.bstack1l11l111lll_opy_:
            bstack1l11l11llll_opy_ = None
            for callback in bstack1llll1l11l1_opy_.bstack1l11l111lll_opy_[bstack1l11l11l111_opy_]:
                try:
                    bstack1l11l111ll1_opy_ = callback(self, target, exec, bstack1llllll11l1_opy_, result, *args, **kwargs)
                    if bstack1l11l11llll_opy_ == None:
                        bstack1l11l11llll_opy_ = bstack1l11l111ll1_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᐔ") + str(e) + bstack1l11l11_opy_ (u"ࠥࠦᐕ"))
                    traceback.print_exc()
            if bstack1l11l11l11l_opy_ == bstack1lllllllll1_opy_.PRE and callable(bstack1l11l11llll_opy_):
                return bstack1l11l11llll_opy_
            elif bstack1l11l11l11l_opy_ == bstack1lllllllll1_opy_.POST and bstack1l11l11llll_opy_:
                return bstack1l11l11llll_opy_
    def bstack1lllll1l111_opy_(
        self, method_name, previous_state: bstack1llll1l1lll_opy_, *args, **kwargs
    ) -> bstack1llll1l1lll_opy_:
        if method_name == bstack1l11l11_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫᐖ") or method_name == bstack1l11l11_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᐗ") or method_name == bstack1l11l11_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨᐘ"):
            return bstack1llll1l1lll_opy_.bstack1111111111_opy_
        if method_name == bstack1l11l11_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩᐙ"):
            return bstack1llll1l1lll_opy_.bstack1lllll1lll1_opy_
        if method_name == bstack1l11l11_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧᐚ"):
            return bstack1llll1l1lll_opy_.QUIT
        return bstack1llll1l1lll_opy_.NONE
    @staticmethod
    def bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_: Tuple[bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_]):
        return bstack1l11l11_opy_ (u"ࠤ࠽ࠦᐛ").join((bstack1llll1l1lll_opy_(bstack1llllll11l1_opy_[0]).name, bstack1lllllllll1_opy_(bstack1llllll11l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111l11_opy_(bstack1llllll11l1_opy_: Tuple[bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_], callback: Callable):
        bstack1l11l11l111_opy_ = bstack1llll1l11l1_opy_.bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_)
        if not bstack1l11l11l111_opy_ in bstack1llll1l11l1_opy_.bstack1l11l111lll_opy_:
            bstack1llll1l11l1_opy_.bstack1l11l111lll_opy_[bstack1l11l11l111_opy_] = []
        bstack1llll1l11l1_opy_.bstack1l11l111lll_opy_[bstack1l11l11l111_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1llll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11lll11l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll111lll11_opy_(instance: bstack1lllll111ll_opy_, default_value=None):
        return bstack1lllll11111_opy_.bstack1lllllll11l_opy_(instance, bstack1llll1l11l1_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1l1lllll1l1_opy_(instance: bstack1lllll111ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll1l1l_opy_(instance: bstack1lllll111ll_opy_, default_value=None):
        return bstack1lllll11111_opy_.bstack1lllllll11l_opy_(instance, bstack1llll1l11l1_opy_.bstack1l1l11lll11_opy_, default_value)
    @staticmethod
    def bstack1ll11l1lll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l11lll_opy_(method_name: str, *args):
        if not bstack1llll1l11l1_opy_.bstack1ll11l1llll_opy_(method_name):
            return False
        if not bstack1llll1l11l1_opy_.bstack1l11l11l1ll_opy_ in bstack1llll1l11l1_opy_.bstack1l11lll1111_opy_(*args):
            return False
        bstack1ll1111l1l1_opy_ = bstack1llll1l11l1_opy_.bstack1ll1111l11l_opy_(*args)
        return bstack1ll1111l1l1_opy_ and bstack1l11l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᐜ") in bstack1ll1111l1l1_opy_ and bstack1l11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᐝ") in bstack1ll1111l1l1_opy_[bstack1l11l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐞ")]
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str, *args):
        if not bstack1llll1l11l1_opy_.bstack1ll11l1llll_opy_(method_name):
            return False
        if not bstack1llll1l11l1_opy_.bstack1l11l11l1ll_opy_ in bstack1llll1l11l1_opy_.bstack1l11lll1111_opy_(*args):
            return False
        bstack1ll1111l1l1_opy_ = bstack1llll1l11l1_opy_.bstack1ll1111l11l_opy_(*args)
        return (
            bstack1ll1111l1l1_opy_
            and bstack1l11l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐟ") in bstack1ll1111l1l1_opy_
            and bstack1l11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᐠ") in bstack1ll1111l1l1_opy_[bstack1l11l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᐡ")]
        )
    @staticmethod
    def bstack1l11lll1111_opy_(*args):
        return str(bstack1llll1l11l1_opy_.bstack1ll11l1lll1_opy_(*args)).lower()