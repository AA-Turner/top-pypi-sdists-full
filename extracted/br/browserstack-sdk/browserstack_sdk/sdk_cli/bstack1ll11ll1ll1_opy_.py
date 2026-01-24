# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll1ll1l1l_opy_,
    bstack1lll1l1111l_opy_,
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1ll11ll1_opy_(bstack1lll1ll1l1l_opy_):
    bstack11lllll1lll_opy_ = bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᔒ")
    bstack1l11l1111ll_opy_ = bstack1l1111_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᔓ")
    bstack1l111lllll1_opy_ = bstack1l1111_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᔔ")
    bstack1l11l111lll_opy_ = bstack1l1111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔕ")
    bstack11llllll1ll_opy_ = bstack1l1111_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᔖ")
    bstack11lllllll11_opy_ = bstack1l1111_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᔗ")
    NAME = bstack1l1111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᔘ")
    bstack11llllll1l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll11111l1_opy_: Any
    bstack11llllll11l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1111_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᔙ"), bstack1l1111_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᔚ"), bstack1l1111_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᔛ"), bstack1l1111_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᔜ"), bstack1l1111_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᔝ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll1ll1lll_opy_(methods)
    def bstack1lll1ll111l_opy_(self, instance: bstack1lll1l1111l_opy_, method_name: str, bstack1lll11ll111_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lll11l11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll1lll1ll_opy_, bstack11lllllll1l_opy_ = bstack1lll111llll_opy_
        bstack11llllllll1_opy_ = bstack1ll1ll11ll1_opy_.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        if bstack11llllllll1_opy_ in bstack1ll1ll11ll1_opy_.bstack11llllll1l1_opy_:
            bstack1l111111111_opy_ = None
            for callback in bstack1ll1ll11ll1_opy_.bstack11llllll1l1_opy_[bstack11llllllll1_opy_]:
                try:
                    bstack11llllll111_opy_ = callback(self, target, exec, bstack1lll111llll_opy_, result, *args, **kwargs)
                    if bstack1l111111111_opy_ == None:
                        bstack1l111111111_opy_ = bstack11llllll111_opy_
                except Exception as e:
                    self.logger.error(bstack1l1111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᔞ") + str(e) + bstack1l1111_opy_ (u"ࠥࠦᔟ"))
                    traceback.print_exc()
            if bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.PRE and callable(bstack1l111111111_opy_):
                return bstack1l111111111_opy_
            elif bstack11lllllll1l_opy_ == bstack1lll1l1ll1l_opy_.POST and bstack1l111111111_opy_:
                return bstack1l111111111_opy_
    def bstack1lll1l1lll1_opy_(
        self, method_name, previous_state: bstack1lll111lll1_opy_, *args, **kwargs
    ) -> bstack1lll111lll1_opy_:
        if method_name == bstack1l1111_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫᔠ") or method_name == bstack1l1111_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᔡ") or method_name == bstack1l1111_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨᔢ"):
            return bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_
        if method_name == bstack1l1111_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩᔣ"):
            return bstack1lll111lll1_opy_.bstack1lll1l111ll_opy_
        if method_name == bstack1l1111_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧᔤ"):
            return bstack1lll111lll1_opy_.QUIT
        return bstack1lll111lll1_opy_.NONE
    @staticmethod
    def bstack11lllllllll_opy_(bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_]):
        return bstack1l1111_opy_ (u"ࠤ࠽ࠦᔥ").join((bstack1lll111lll1_opy_(bstack1lll111llll_opy_[0]).name, bstack1lll1l1ll1l_opy_(bstack1lll111llll_opy_[1]).name))
    @staticmethod
    def bstack1l1lll1ll11_opy_(bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_], callback: Callable):
        bstack11llllllll1_opy_ = bstack1ll1ll11ll1_opy_.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        if not bstack11llllllll1_opy_ in bstack1ll1ll11ll1_opy_.bstack11llllll1l1_opy_:
            bstack1ll1ll11ll1_opy_.bstack11llllll1l1_opy_[bstack11llllllll1_opy_] = []
        bstack1ll1ll11ll1_opy_.bstack11llllll1l1_opy_[bstack11llllllll1_opy_].append(callback)
    @staticmethod
    def bstack1l1llll111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1lll1lll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1lll1l1ll_opy_(instance: bstack1lll1l1111l_opy_, default_value=None):
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l111lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1l1l1l1_opy_(instance: bstack1lll1l1111l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1ll1lll11_opy_(instance: bstack1lll1l1111l_opy_, default_value=None):
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l111lllll1_opy_, default_value)
    @staticmethod
    def bstack1l1ll111ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1lll11l1l_opy_(method_name: str, *args):
        if not bstack1ll1ll11ll1_opy_.bstack1l1llll111l_opy_(method_name):
            return False
        if not bstack1ll1ll11ll1_opy_.bstack11llllll1ll_opy_ in bstack1ll1ll11ll1_opy_.bstack1l1111ll1ll_opy_(*args):
            return False
        bstack1l1l1ll1l1l_opy_ = bstack1ll1ll11ll1_opy_.bstack1l1l1ll11ll_opy_(*args)
        return bstack1l1l1ll1l1l_opy_ and bstack1l1111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᔦ") in bstack1l1l1ll1l1l_opy_ and bstack1l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔧ") in bstack1l1l1ll1l1l_opy_[bstack1l1111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᔨ")]
    @staticmethod
    def bstack1l1llllll1l_opy_(method_name: str, *args):
        if not bstack1ll1ll11ll1_opy_.bstack1l1llll111l_opy_(method_name):
            return False
        if not bstack1ll1ll11ll1_opy_.bstack11llllll1ll_opy_ in bstack1ll1ll11ll1_opy_.bstack1l1111ll1ll_opy_(*args):
            return False
        bstack1l1l1ll1l1l_opy_ = bstack1ll1ll11ll1_opy_.bstack1l1l1ll11ll_opy_(*args)
        return (
            bstack1l1l1ll1l1l_opy_
            and bstack1l1111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᔩ") in bstack1l1l1ll1l1l_opy_
            and bstack1l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᔪ") in bstack1l1l1ll1l1l_opy_[bstack1l1111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᔫ")]
        )
    @staticmethod
    def bstack1l1111ll1ll_opy_(*args):
        return str(bstack1ll1ll11ll1_opy_.bstack1l1ll111ll1_opy_(*args)).lower()