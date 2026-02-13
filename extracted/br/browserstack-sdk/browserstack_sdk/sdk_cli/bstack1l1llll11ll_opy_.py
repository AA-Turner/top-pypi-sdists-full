# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1ll11l11_opy_,
    bstack1ll1l1ll1ll_opy_,
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1l1lllll11l_opy_(bstack1ll1ll11l11_opy_):
    bstack11lll1111l1_opy_ = bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᗢ")
    bstack1l1111ll1ll_opy_ = bstack11l11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᗣ")
    bstack1l11111lll1_opy_ = bstack11l11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᗤ")
    bstack1l1111l1lll_opy_ = bstack11l11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᗥ")
    bstack11ll1lll1ll_opy_ = bstack11l11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᗦ")
    bstack11lll111111_opy_ = bstack11l11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᗧ")
    NAME = bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᗨ")
    bstack11ll1llllll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llll111l_opy_: Any
    bstack11lll11111l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l11_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᗩ"), bstack11l11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᗪ"), bstack11l11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᗫ"), bstack11l11_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᗬ"), bstack11l11_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᗭ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1llllll1_opy_(methods)
    def bstack1ll1lll1ll1_opy_(self, instance: bstack1ll1l1ll1ll_opy_, method_name: str, bstack1ll1ll1l111_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1ll11ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1lll11ll_opy_, bstack11ll1lll1l1_opy_ = bstack1ll1l1lll1l_opy_
        bstack11ll1llll11_opy_ = bstack1l1lllll11l_opy_.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        if bstack11ll1llll11_opy_ in bstack1l1lllll11l_opy_.bstack11ll1llllll_opy_:
            bstack11ll1lllll1_opy_ = None
            for callback in bstack1l1lllll11l_opy_.bstack11ll1llllll_opy_[bstack11ll1llll11_opy_]:
                try:
                    bstack11lll1111ll_opy_ = callback(self, target, exec, bstack1ll1l1lll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1lllll1_opy_ == None:
                        bstack11ll1lllll1_opy_ = bstack11lll1111ll_opy_
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᗮ") + str(e) + bstack11l11_opy_ (u"ࠣࠤᗯ"))
                    traceback.print_exc()
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.PRE and callable(bstack11ll1lllll1_opy_):
                return bstack11ll1lllll1_opy_
            elif bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST and bstack11ll1lllll1_opy_:
                return bstack11ll1lllll1_opy_
    def bstack1ll1ll1lll1_opy_(
        self, method_name, previous_state: bstack1ll1lllllll_opy_, *args, **kwargs
    ) -> bstack1ll1lllllll_opy_:
        if method_name == bstack11l11_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᗰ") or method_name == bstack11l11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᗱ") or method_name == bstack11l11_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᗲ"):
            return bstack1ll1lllllll_opy_.bstack1lll1111111_opy_
        if method_name == bstack11l11_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᗳ"):
            return bstack1ll1lllllll_opy_.bstack1ll1ll1111l_opy_
        if method_name == bstack11l11_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᗴ"):
            return bstack1ll1lllllll_opy_.QUIT
        return bstack1ll1lllllll_opy_.NONE
    @staticmethod
    def bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_]):
        return bstack11l11_opy_ (u"ࠢ࠻ࠤᗵ").join((bstack1ll1lllllll_opy_(bstack1ll1l1lll1l_opy_[0]).name, bstack1ll1l1llll1_opy_(bstack1ll1l1lll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1l111ll_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_], callback: Callable):
        bstack11ll1llll11_opy_ = bstack1l1lllll11l_opy_.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        if not bstack11ll1llll11_opy_ in bstack1l1lllll11l_opy_.bstack11ll1llllll_opy_:
            bstack1l1lllll11l_opy_.bstack11ll1llllll_opy_[bstack11ll1llll11_opy_] = []
        bstack1l1lllll11l_opy_.bstack11ll1llllll_opy_[bstack11ll1llll11_opy_].append(callback)
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l11l1lll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1l1l111l1_opy_(instance: bstack1ll1l1ll1ll_opy_, default_value=None):
        return bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1l1lllll11l_opy_.bstack1l1111l1lll_opy_, default_value)
    @staticmethod
    def bstack1l11lllll11_opy_(instance: bstack1ll1l1ll1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l1ll1l1l_opy_(instance: bstack1ll1l1ll1ll_opy_, default_value=None):
        return bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1l1lllll11l_opy_.bstack1l11111lll1_opy_, default_value)
    @staticmethod
    def bstack1l1l11ll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1llllll_opy_(method_name: str, *args):
        if not bstack1l1lllll11l_opy_.bstack1l1l1l1ll1l_opy_(method_name):
            return False
        if not bstack1l1lllll11l_opy_.bstack11ll1lll1ll_opy_ in bstack1l1lllll11l_opy_.bstack11lllll1ll1_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1l1lllll11l_opy_.bstack1l1l1111111_opy_(*args)
        return bstack1l11lllllll_opy_ and bstack11l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᗶ") in bstack1l11lllllll_opy_ and bstack11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᗷ") in bstack1l11lllllll_opy_[bstack11l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᗸ")]
    @staticmethod
    def bstack1l1l1l1lll1_opy_(method_name: str, *args):
        if not bstack1l1lllll11l_opy_.bstack1l1l1l1ll1l_opy_(method_name):
            return False
        if not bstack1l1lllll11l_opy_.bstack11ll1lll1ll_opy_ in bstack1l1lllll11l_opy_.bstack11lllll1ll1_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1l1lllll11l_opy_.bstack1l1l1111111_opy_(*args)
        return (
            bstack1l11lllllll_opy_
            and bstack11l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᗹ") in bstack1l11lllllll_opy_
            and bstack11l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᗺ") in bstack1l11lllllll_opy_[bstack11l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᗻ")]
        )
    @staticmethod
    def bstack11lllll1ll1_opy_(*args):
        return str(bstack1l1lllll11l_opy_.bstack1l1l11ll11l_opy_(*args)).lower()