# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1ll1lllll11_opy_,
    bstack1lll1llll11_opy_,
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1lll1l1l_opy_(bstack1ll1lllll11_opy_):
    bstack1l1llllllll_opy_ = bstack11l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤተ")
    bstack1ll1l1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥቱ")
    bstack1ll1ll1l111_opy_ = bstack11l1111_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧቲ")
    bstack1ll1ll11l11_opy_ = bstack11l1111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦታ")
    bstack1ll11111lll_opy_ = bstack11l1111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤቴ")
    bstack1ll1111l111_opy_ = bstack11l1111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣት")
    NAME = bstack11l1111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧቶ")
    bstack1l1lllll1l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll11l11l11_opy_: Any
    bstack1ll111111ll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1111_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤቷ"), bstack11l1111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦቸ"), bstack11l1111_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨቹ"), bstack11l1111_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦቺ"), bstack11l1111_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣቻ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1lllllll1_opy_(methods)
    def bstack1ll1111l11l_opy_(self, instance: bstack1lll1llll11_opy_, method_name: str, bstack1ll11111l1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll11111ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1lllll1ll_opy_, bstack1l1llll1lll_opy_ = bstack1llll11l111_opy_
        bstack1ll11111111_opy_ = bstack1ll1lll1l1l_opy_.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        if bstack1ll11111111_opy_ in bstack1ll1lll1l1l_opy_.bstack1l1lllll1l1_opy_:
            bstack1l1lllll11l_opy_ = None
            for callback in bstack1ll1lll1l1l_opy_.bstack1l1lllll1l1_opy_[bstack1ll11111111_opy_]:
                try:
                    bstack1l1llllll1l_opy_ = callback(self, target, exec, bstack1llll11l111_opy_, result, *args, **kwargs)
                    if bstack1l1lllll11l_opy_ == None:
                        bstack1l1lllll11l_opy_ = bstack1l1llllll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧቼ") + str(e) + bstack11l1111_opy_ (u"ࠣࠤች"))
                    traceback.print_exc()
            if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l1lllll11l_opy_):
                return bstack1l1lllll11l_opy_
            elif bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l1lllll11l_opy_:
                return bstack1l1lllll11l_opy_
    def bstack1ll1111111l_opy_(
        self, method_name, previous_state: bstack1lll1llllll_opy_, *args, **kwargs
    ) -> bstack1lll1llllll_opy_:
        if method_name == bstack11l1111_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩቾ") or method_name == bstack11l1111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫቿ") or method_name == bstack11l1111_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ኀ"):
            return bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_
        if method_name == bstack11l1111_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧኁ"):
            return bstack1lll1llllll_opy_.bstack1ll1l1ll11l_opy_
        if method_name == bstack11l1111_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬኂ"):
            return bstack1lll1llllll_opy_.QUIT
        return bstack1lll1llllll_opy_.NONE
    @staticmethod
    def bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_]):
        return bstack11l1111_opy_ (u"ࠢ࠻ࠤኃ").join((bstack1lll1llllll_opy_(bstack1llll11l111_opy_[0]).name, bstack1llllll1l1l_opy_(bstack1llll11l111_opy_[1]).name))
    @staticmethod
    def bstack1lllll1llll_opy_(bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1ll11111111_opy_ = bstack1ll1lll1l1l_opy_.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        if not bstack1ll11111111_opy_ in bstack1ll1lll1l1l_opy_.bstack1l1lllll1l1_opy_:
            bstack1ll1lll1l1l_opy_.bstack1l1lllll1l1_opy_[bstack1ll11111111_opy_] = []
        bstack1ll1lll1l1l_opy_.bstack1l1lllll1l1_opy_[bstack1ll11111111_opy_].append(callback)
    @staticmethod
    def bstack1lllll11ll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11l11111_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1llllll11_opy_(instance: bstack1lll1llll11_opy_, default_value=None):
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1ll1ll11l11_opy_, default_value)
    @staticmethod
    def bstack1ll1lllll1l_opy_(instance: bstack1lll1llll11_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1lllll111_opy_(instance: bstack1lll1llll11_opy_, default_value=None):
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1ll1ll1l111_opy_, default_value)
    @staticmethod
    def bstack1lllll1ll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111111l1_opy_(method_name: str, *args):
        if not bstack1ll1lll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
            return False
        if not bstack1ll1lll1l1l_opy_.bstack1ll11111lll_opy_ in bstack1ll1lll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args):
            return False
        bstack1lll1111111_opy_ = bstack1ll1lll1l1l_opy_.bstack1lll111llll_opy_(*args)
        return bstack1lll1111111_opy_ and bstack11l1111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣኄ") in bstack1lll1111111_opy_ and bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥኅ") in bstack1lll1111111_opy_[bstack11l1111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥኆ")]
    @staticmethod
    def bstack1ll11111l11_opy_(method_name: str, *args):
        if not bstack1ll1lll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
            return False
        if not bstack1ll1lll1l1l_opy_.bstack1ll11111lll_opy_ in bstack1ll1lll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args):
            return False
        bstack1lll1111111_opy_ = bstack1ll1lll1l1l_opy_.bstack1lll111llll_opy_(*args)
        return (
            bstack1lll1111111_opy_
            and bstack11l1111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦኇ") in bstack1lll1111111_opy_
            and bstack11l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣኈ") in bstack1lll1111111_opy_[bstack11l1111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ኉")]
        )
    @staticmethod
    def bstack1ll11l1l1ll_opy_(*args):
        return str(bstack1ll1lll1l1l_opy_.bstack1lllll1ll11_opy_(*args)).lower()