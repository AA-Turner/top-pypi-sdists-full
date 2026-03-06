# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1lll11l1ll1_opy_,
    bstack1ll1ll1l111_opy_,
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll11l11ll_opy_(bstack1lll11l1ll1_opy_):
    bstack11ll1lll11l_opy_ = bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᚄ")
    bstack1lll1l1l1l1_opy_ = bstack1111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᚅ")
    bstack1lll11lll1l_opy_ = bstack1111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᚆ")
    bstack1lll1111l11_opy_ = bstack1111_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᚇ")
    bstack11ll1ll1ll1_opy_ = bstack1111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᚈ")
    bstack11ll1lll111_opy_ = bstack1111_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᚉ")
    NAME = bstack1111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᚊ")
    bstack11ll1ll1111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llll111l_opy_: Any
    bstack11ll1ll1l1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1111_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᚋ"), bstack1111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᚌ"), bstack1111_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᚍ"), bstack1111_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᚎ"), bstack1111_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᚏ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1llll111_opy_(methods)
    def bstack1ll1ll1111l_opy_(self, instance: bstack1ll1ll1l111_opy_, method_name: str, bstack1ll1ll11ll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1l11llll_opy_, bstack11ll1ll11l1_opy_ = bstack1ll1ll1ll1l_opy_
        bstack11ll1ll11ll_opy_ = bstack1lll11l11ll_opy_.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        if bstack11ll1ll11ll_opy_ in bstack1lll11l11ll_opy_.bstack11ll1ll1111_opy_:
            bstack11ll1ll1lll_opy_ = None
            for callback in bstack1lll11l11ll_opy_.bstack11ll1ll1111_opy_[bstack11ll1ll11ll_opy_]:
                try:
                    bstack11ll1ll111l_opy_ = callback(self, target, exec, bstack1ll1ll1ll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1ll1lll_opy_ == None:
                        bstack11ll1ll1lll_opy_ = bstack11ll1ll111l_opy_
                except Exception as e:
                    self.logger.error(bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᚐ") + str(e) + bstack1111_opy_ (u"ࠤࠥᚑ"))
                    traceback.print_exc()
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.PRE and callable(bstack11ll1ll1lll_opy_):
                return bstack11ll1ll1lll_opy_
            elif bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST and bstack11ll1ll1lll_opy_:
                return bstack11ll1ll1lll_opy_
    def bstack1ll1l1ll1l1_opy_(
        self, method_name, previous_state: bstack1ll1lll1ll1_opy_, *args, **kwargs
    ) -> bstack1ll1lll1ll1_opy_:
        if method_name == bstack1111_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᚒ") or method_name == bstack1111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᚓ") or method_name == bstack1111_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᚔ"):
            return bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_
        if method_name == bstack1111_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨᚕ"):
            return bstack1ll1lll1ll1_opy_.bstack1ll1ll1l11l_opy_
        if method_name == bstack1111_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ᚖ"):
            return bstack1ll1lll1ll1_opy_.QUIT
        return bstack1ll1lll1ll1_opy_.NONE
    @staticmethod
    def bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_]):
        return bstack1111_opy_ (u"ࠣ࠼ࠥᚗ").join((bstack1ll1lll1ll1_opy_(bstack1ll1ll1ll1l_opy_[0]).name, bstack1ll1l1lll1l_opy_(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1ll1111ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_], callback: Callable):
        bstack11ll1ll11ll_opy_ = bstack1lll11l11ll_opy_.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1ll11ll_opy_ in bstack1lll11l11ll_opy_.bstack11ll1ll1111_opy_:
            bstack1lll11l11ll_opy_.bstack11ll1ll1111_opy_[bstack11ll1ll11ll_opy_] = []
        bstack1lll11l11ll_opy_.bstack11ll1ll1111_opy_[bstack11ll1ll11ll_opy_].append(callback)
    @staticmethod
    def bstack1l1l111l1ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l1lllll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1l1ll1ll1_opy_(instance: bstack1ll1ll1l111_opy_, default_value=None):
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1111l11_opy_, default_value)
    @staticmethod
    def bstack1l11ll1lll1_opy_(instance: bstack1ll1ll1l111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1ll111111_opy_(instance: bstack1ll1ll1l111_opy_, default_value=None):
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_, default_value)
    @staticmethod
    def bstack1l1l1l11lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l11l1111_opy_(method_name: str, *args):
        if not bstack1lll11l11ll_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1lll11l11ll_opy_.bstack11ll1ll1ll1_opy_ in bstack1lll11l11ll_opy_.bstack11lll1ll1ll_opy_(*args):
            return False
        bstack1l1l1111111_opy_ = bstack1lll11l11ll_opy_.bstack1l11lllllll_opy_(*args)
        return bstack1l1l1111111_opy_ and bstack1111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᚘ") in bstack1l1l1111111_opy_ and bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᚙ") in bstack1l1l1111111_opy_[bstack1111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᚚ")]
    @staticmethod
    def bstack1l1l1lll11l_opy_(method_name: str, *args):
        if not bstack1lll11l11ll_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1lll11l11ll_opy_.bstack11ll1ll1ll1_opy_ in bstack1lll11l11ll_opy_.bstack11lll1ll1ll_opy_(*args):
            return False
        bstack1l1l1111111_opy_ = bstack1lll11l11ll_opy_.bstack1l11lllllll_opy_(*args)
        return (
            bstack1l1l1111111_opy_
            and bstack1111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᚛") in bstack1l1l1111111_opy_
            and bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤ᚜") in bstack1l1l1111111_opy_[bstack1111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᚝")]
        )
    @staticmethod
    def bstack11lll1ll1ll_opy_(*args):
        return str(bstack1lll11l11ll_opy_.bstack1l1l1l11lll_opy_(*args)).lower()