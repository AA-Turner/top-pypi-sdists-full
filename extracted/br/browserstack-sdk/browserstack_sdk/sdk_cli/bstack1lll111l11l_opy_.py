# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1lll1111l11_opy_,
    bstack1ll1llll11l_opy_,
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111l1ll_opy_(bstack1lll1111l11_opy_):
    bstack11ll1lll1l1_opy_ = bstack1lll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᚃ")
    bstack1lll1111ll1_opy_ = bstack1lll1l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᚄ")
    bstack1lll1l11ll1_opy_ = bstack1lll1l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᚅ")
    bstack1lll11ll1l1_opy_ = bstack1lll1l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᚆ")
    bstack11ll1ll1ll1_opy_ = bstack1lll1l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᚇ")
    bstack11ll1ll11l1_opy_ = bstack1lll1l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᚈ")
    NAME = bstack1lll1l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᚉ")
    bstack11ll1lll11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll111l1ll1_opy_: Any
    bstack11ll1lll111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1lll1l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᚊ"), bstack1lll1l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᚋ"), bstack1lll1l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᚌ"), bstack1lll1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᚍ"), bstack1lll1l_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᚎ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1l1l1111_opy_(methods)
    def bstack1ll1ll11111_opy_(self, instance: bstack1ll1llll11l_opy_, method_name: str, bstack1ll1l1l1l11_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1l1lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1ll1ll11_opy_, bstack11ll1ll1l1l_opy_ = bstack1ll1ll1ll1l_opy_
        bstack11ll1lll1ll_opy_ = bstack1lll111l1ll_opy_.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        if bstack11ll1lll1ll_opy_ in bstack1lll111l1ll_opy_.bstack11ll1lll11l_opy_:
            bstack11ll1ll1l11_opy_ = None
            for callback in bstack1lll111l1ll_opy_.bstack11ll1lll11l_opy_[bstack11ll1lll1ll_opy_]:
                try:
                    bstack11ll1ll11ll_opy_ = callback(self, target, exec, bstack1ll1ll1ll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1ll1l11_opy_ == None:
                        bstack11ll1ll1l11_opy_ = bstack11ll1ll11ll_opy_
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᚏ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᚐ"))
                    traceback.print_exc()
            if bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.PRE and callable(bstack11ll1ll1l11_opy_):
                return bstack11ll1ll1l11_opy_
            elif bstack11ll1ll1l1l_opy_ == bstack1ll1llll111_opy_.POST and bstack11ll1ll1l11_opy_:
                return bstack11ll1ll1l11_opy_
    def bstack1ll1lll1ll1_opy_(
        self, method_name, previous_state: bstack1ll1l1l11ll_opy_, *args, **kwargs
    ) -> bstack1ll1l1l11ll_opy_:
        if method_name == bstack1lll1l_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᚑ") or method_name == bstack1lll1l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᚒ") or method_name == bstack1lll1l_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᚓ"):
            return bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_
        if method_name == bstack1lll1l_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᚔ"):
            return bstack1ll1l1l11ll_opy_.bstack1ll1l1ll111_opy_
        if method_name == bstack1lll1l_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᚕ"):
            return bstack1ll1l1l11ll_opy_.QUIT
        return bstack1ll1l1l11ll_opy_.NONE
    @staticmethod
    def bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_]):
        return bstack1lll1l_opy_ (u"ࠢ࠻ࠤᚖ").join((bstack1ll1l1l11ll_opy_(bstack1ll1ll1ll1l_opy_[0]).name, bstack1ll1llll111_opy_(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll1ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_], callback: Callable):
        bstack11ll1lll1ll_opy_ = bstack1lll111l1ll_opy_.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1lll1ll_opy_ in bstack1lll111l1ll_opy_.bstack11ll1lll11l_opy_:
            bstack1lll111l1ll_opy_.bstack11ll1lll11l_opy_[bstack11ll1lll1ll_opy_] = []
        bstack1lll111l1ll_opy_.bstack11ll1lll11l_opy_[bstack11ll1lll1ll_opy_].append(callback)
    @staticmethod
    def bstack1l1l11lllll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l1ll1l11_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1l11l1111_opy_(instance: bstack1ll1llll11l_opy_, default_value=None):
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll11ll1l1_opy_, default_value)
    @staticmethod
    def bstack1l11lll111l_opy_(instance: bstack1ll1llll11l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l1lllll1_opy_(instance: bstack1ll1llll11l_opy_, default_value=None):
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_, default_value)
    @staticmethod
    def bstack1l1l1llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l11lll1l_opy_(method_name: str, *args):
        if not bstack1lll111l1ll_opy_.bstack1l1l11lllll_opy_(method_name):
            return False
        if not bstack1lll111l1ll_opy_.bstack11ll1ll1ll1_opy_ in bstack1lll111l1ll_opy_.bstack11lll1lll11_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1lll111l1ll_opy_.bstack1l11llll1ll_opy_(*args)
        return bstack1l11lllllll_opy_ and bstack1lll1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᚗ") in bstack1l11lllllll_opy_ and bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᚘ") in bstack1l11lllllll_opy_[bstack1lll1l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᚙ")]
    @staticmethod
    def bstack1l1l1l1l1ll_opy_(method_name: str, *args):
        if not bstack1lll111l1ll_opy_.bstack1l1l11lllll_opy_(method_name):
            return False
        if not bstack1lll111l1ll_opy_.bstack11ll1ll1ll1_opy_ in bstack1lll111l1ll_opy_.bstack11lll1lll11_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1lll111l1ll_opy_.bstack1l11llll1ll_opy_(*args)
        return (
            bstack1l11lllllll_opy_
            and bstack1lll1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᚚ") in bstack1l11lllllll_opy_
            and bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣ᚛") in bstack1l11lllllll_opy_[bstack1lll1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᚜")]
        )
    @staticmethod
    def bstack11lll1lll11_opy_(*args):
        return str(bstack1lll111l1ll_opy_.bstack1l1l1llll1l_opy_(*args)).lower()