# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1llllll1lll_opy_,
    bstack1111111111_opy_,
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1lllllll_opy_(bstack1llllll1lll_opy_):
    bstack1l11l1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᎩ")
    bstack1l1l11lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᎪ")
    bstack1l1l11lllll_opy_ = bstack1l1l1l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᎫ")
    bstack1l1l1l1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎬ")
    bstack1l11l1ll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᎭ")
    bstack1l11ll11111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᎮ")
    NAME = bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᎯ")
    bstack1l11l1lll11_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l1l_opy_: Any
    bstack1l11l1lll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1l1l1_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᎰ"), bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᎱ"), bstack1l1l1l1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᎲ"), bstack1l1l1l1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᎳ"), bstack1l1l1l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᎴ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllll1l1l_opy_(methods)
    def bstack1111111l11_opy_(self, instance: bstack1111111111_opy_, method_name: str, bstack1llllllll1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lllll1lll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111111l1_opy_, bstack1l11l1l1lll_opy_ = bstack1lllll11ll1_opy_
        bstack1l11l1ll1ll_opy_ = bstack1ll1lllllll_opy_.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        if bstack1l11l1ll1ll_opy_ in bstack1ll1lllllll_opy_.bstack1l11l1lll11_opy_:
            bstack1l11l1llll1_opy_ = None
            for callback in bstack1ll1lllllll_opy_.bstack1l11l1lll11_opy_[bstack1l11l1ll1ll_opy_]:
                try:
                    bstack1l11l1ll11l_opy_ = callback(self, target, exec, bstack1lllll11ll1_opy_, result, *args, **kwargs)
                    if bstack1l11l1llll1_opy_ == None:
                        bstack1l11l1llll1_opy_ = bstack1l11l1ll11l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᎵ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢᎶ"))
                    traceback.print_exc()
            if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.PRE and callable(bstack1l11l1llll1_opy_):
                return bstack1l11l1llll1_opy_
            elif bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST and bstack1l11l1llll1_opy_:
                return bstack1l11l1llll1_opy_
    def bstack111111l11l_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1l1l1l1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧᎷ") or method_name == bstack1l1l1l1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᎸ") or method_name == bstack1l1l1l1_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫᎹ"):
            return bstack1lllll1l111_opy_.bstack1111111lll_opy_
        if method_name == bstack1l1l1l1_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬᎺ"):
            return bstack1lllll1l111_opy_.bstack1lllll1l1l1_opy_
        if method_name == bstack1l1l1l1_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪᎻ"):
            return bstack1lllll1l111_opy_.QUIT
        return bstack1lllll1l111_opy_.NONE
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_]):
        return bstack1l1l1l1_opy_ (u"ࠧࡀࠢᎼ").join((bstack1lllll1l111_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1lllll1llll_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_], callback: Callable):
        bstack1l11l1ll1ll_opy_ = bstack1ll1lllllll_opy_.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l1ll1ll_opy_ in bstack1ll1lllllll_opy_.bstack1l11l1lll11_opy_:
            bstack1ll1lllllll_opy_.bstack1l11l1lll11_opy_[bstack1l11l1ll1ll_opy_] = []
        bstack1ll1lllllll_opy_.bstack1l11l1lll11_opy_[bstack1l11l1ll1ll_opy_].append(callback)
    @staticmethod
    def bstack1ll11l111ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll111ll11l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11l1l11l_opy_(instance: bstack1111111111_opy_, default_value=None):
        return bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l1l1lll1_opy_, default_value)
    @staticmethod
    def bstack1ll11111l11_opy_(instance: bstack1111111111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll11ll_opy_(instance: bstack1111111111_opy_, default_value=None):
        return bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, default_value)
    @staticmethod
    def bstack1ll11l1ll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11ll11_opy_(method_name: str, *args):
        if not bstack1ll1lllllll_opy_.bstack1ll11l111ll_opy_(method_name):
            return False
        if not bstack1ll1lllllll_opy_.bstack1l11l1ll1l1_opy_ in bstack1ll1lllllll_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll111l11ll_opy_ = bstack1ll1lllllll_opy_.bstack1ll111l11l1_opy_(*args)
        return bstack1ll111l11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᎽ") in bstack1ll111l11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᎾ") in bstack1ll111l11ll_opy_[bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᎿ")]
    @staticmethod
    def bstack1ll1l1l111l_opy_(method_name: str, *args):
        if not bstack1ll1lllllll_opy_.bstack1ll11l111ll_opy_(method_name):
            return False
        if not bstack1ll1lllllll_opy_.bstack1l11l1ll1l1_opy_ in bstack1ll1lllllll_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll111l11ll_opy_ = bstack1ll1lllllll_opy_.bstack1ll111l11l1_opy_(*args)
        return (
            bstack1ll111l11ll_opy_
            and bstack1l1l1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᏀ") in bstack1ll111l11ll_opy_
            and bstack1l1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᏁ") in bstack1ll111l11ll_opy_[bstack1l1l1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᏂ")]
        )
    @staticmethod
    def bstack1l1l11111l1_opy_(*args):
        return str(bstack1ll1lllllll_opy_.bstack1ll11l1ll11_opy_(*args)).lower()