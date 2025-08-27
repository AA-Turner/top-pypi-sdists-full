# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack11111111l1_opy_,
    bstack1lllll1ll11_opy_,
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll1l1l11_opy_(bstack11111111l1_opy_):
    bstack1l11l11llll_opy_ = bstack1111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᐏ")
    bstack1l1l11ll1l1_opy_ = bstack1111lll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᐐ")
    bstack1l1l11l1l1l_opy_ = bstack1111lll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᐑ")
    bstack1l1l11llll1_opy_ = bstack1111lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᐒ")
    bstack1l11l11l1l1_opy_ = bstack1111lll_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᐓ")
    bstack1l11l11ll11_opy_ = bstack1111lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᐔ")
    NAME = bstack1111lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᐕ")
    bstack1l11l11l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l111l1_opy_: Any
    bstack1l11l1l1111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1111lll_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᐖ"), bstack1111lll_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᐗ"), bstack1111lll_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᐘ"), bstack1111lll_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᐙ"), bstack1111lll_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᐚ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll1l1l1_opy_(methods)
    def bstack1111111111_opy_(self, instance: bstack1lllll1ll11_opy_, method_name: str, bstack1llll1lllll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1ll111_opy_, bstack1l11l1l11l1_opy_ = bstack1llllll11ll_opy_
        bstack1l11l11l11l_opy_ = bstack1llll1l1l11_opy_.bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_)
        if bstack1l11l11l11l_opy_ in bstack1llll1l1l11_opy_.bstack1l11l11l1ll_opy_:
            bstack1l11l1l111l_opy_ = None
            for callback in bstack1llll1l1l11_opy_.bstack1l11l11l1ll_opy_[bstack1l11l11l11l_opy_]:
                try:
                    bstack1l11l11ll1l_opy_ = callback(self, target, exec, bstack1llllll11ll_opy_, result, *args, **kwargs)
                    if bstack1l11l1l111l_opy_ == None:
                        bstack1l11l1l111l_opy_ = bstack1l11l11ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack1111lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᐛ") + str(e) + bstack1111lll_opy_ (u"ࠥࠦᐜ"))
                    traceback.print_exc()
            if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l1l111l_opy_):
                return bstack1l11l1l111l_opy_
            elif bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l1l111l_opy_:
                return bstack1l11l1l111l_opy_
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1lllll1lll1_opy_, *args, **kwargs
    ) -> bstack1lllll1lll1_opy_:
        if method_name == bstack1111lll_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫᐝ") or method_name == bstack1111lll_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᐞ") or method_name == bstack1111lll_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨᐟ"):
            return bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_
        if method_name == bstack1111lll_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩᐠ"):
            return bstack1lllll1lll1_opy_.bstack1llllll11l1_opy_
        if method_name == bstack1111lll_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧᐡ"):
            return bstack1lllll1lll1_opy_.QUIT
        return bstack1lllll1lll1_opy_.NONE
    @staticmethod
    def bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_]):
        return bstack1111lll_opy_ (u"ࠤ࠽ࠦᐢ").join((bstack1lllll1lll1_opy_(bstack1llllll11ll_opy_[0]).name, bstack1llllll1111_opy_(bstack1llllll11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll11l111l1_opy_(bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l11l11l_opy_ = bstack1llll1l1l11_opy_.bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_)
        if not bstack1l11l11l11l_opy_ in bstack1llll1l1l11_opy_.bstack1l11l11l1ll_opy_:
            bstack1llll1l1l11_opy_.bstack1l11l11l1ll_opy_[bstack1l11l11l11l_opy_] = []
        bstack1llll1l1l11_opy_.bstack1l11l11l1ll_opy_[bstack1l11l11l11l_opy_].append(callback)
    @staticmethod
    def bstack1ll11llllll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11ll1l11_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll1l1l_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1l11llll1_opy_, default_value)
    @staticmethod
    def bstack1l1lllll11l_opy_(instance: bstack1lllll1ll11_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11l11111_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1llll1l1l11_opy_.bstack1l1l11l1l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11lll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11lllll1_opy_(method_name: str, *args):
        if not bstack1llll1l1l11_opy_.bstack1ll11llllll_opy_(method_name):
            return False
        if not bstack1llll1l1l11_opy_.bstack1l11l11l1l1_opy_ in bstack1llll1l1l11_opy_.bstack1l11lll1l1l_opy_(*args):
            return False
        bstack1ll111111ll_opy_ = bstack1llll1l1l11_opy_.bstack1ll1111l1ll_opy_(*args)
        return bstack1ll111111ll_opy_ and bstack1111lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᐣ") in bstack1ll111111ll_opy_ and bstack1111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᐤ") in bstack1ll111111ll_opy_[bstack1111lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐥ")]
    @staticmethod
    def bstack1ll111l11l1_opy_(method_name: str, *args):
        if not bstack1llll1l1l11_opy_.bstack1ll11llllll_opy_(method_name):
            return False
        if not bstack1llll1l1l11_opy_.bstack1l11l11l1l1_opy_ in bstack1llll1l1l11_opy_.bstack1l11lll1l1l_opy_(*args):
            return False
        bstack1ll111111ll_opy_ = bstack1llll1l1l11_opy_.bstack1ll1111l1ll_opy_(*args)
        return (
            bstack1ll111111ll_opy_
            and bstack1111lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐦ") in bstack1ll111111ll_opy_
            and bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᐧ") in bstack1ll111111ll_opy_[bstack1111lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᐨ")]
        )
    @staticmethod
    def bstack1l11lll1l1l_opy_(*args):
        return str(bstack1llll1l1l11_opy_.bstack1ll11lll11l_opy_(*args)).lower()