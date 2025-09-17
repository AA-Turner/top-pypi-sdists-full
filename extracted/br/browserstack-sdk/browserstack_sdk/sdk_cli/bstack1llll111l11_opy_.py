# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1llllllll1l_opy_,
    bstack1lllllll111_opy_,
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1l1lllll_opy_(bstack1llllllll1l_opy_):
    bstack1l11l1111ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᐒ")
    bstack1l1l11l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᐓ")
    bstack1l1l11l1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᐔ")
    bstack1l1l111lll1_opy_ = bstack1l11ll1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᐕ")
    bstack1l11l11l111_opy_ = bstack1l11ll1_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᐖ")
    bstack1l11l111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᐗ")
    NAME = bstack1l11ll1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᐘ")
    bstack1l11l11l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1111l1l_opy_: Any
    bstack1l11l111lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11ll1_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᐙ"), bstack1l11ll1_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᐚ"), bstack1l11ll1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᐛ"), bstack1l11ll1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᐜ"), bstack1l11ll1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᐝ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllll11ll_opy_(methods)
    def bstack1llll1ll1l1_opy_(self, instance: bstack1lllllll111_opy_, method_name: str, bstack1lllll1ll1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll1l11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1l1l11_opy_, bstack1l11l11l1l1_opy_ = bstack1lllll1llll_opy_
        bstack1l11l111l11_opy_ = bstack1ll1l1lllll_opy_.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        if bstack1l11l111l11_opy_ in bstack1ll1l1lllll_opy_.bstack1l11l11l1ll_opy_:
            bstack1l11l111l1l_opy_ = None
            for callback in bstack1ll1l1lllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11ll11_opy_ = callback(self, target, exec, bstack1lllll1llll_opy_, result, *args, **kwargs)
                    if bstack1l11l111l1l_opy_ == None:
                        bstack1l11l111l1l_opy_ = bstack1l11l11ll11_opy_
                except Exception as e:
                    self.logger.error(bstack1l11ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᐞ") + str(e) + bstack1l11ll1_opy_ (u"ࠨࠢᐟ"))
                    traceback.print_exc()
            if bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.PRE and callable(bstack1l11l111l1l_opy_):
                return bstack1l11l111l1l_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1llll1l11ll_opy_.POST and bstack1l11l111l1l_opy_:
                return bstack1l11l111l1l_opy_
    def bstack1llll1ll11l_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1l11ll1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧᐠ") or method_name == bstack1l11ll1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᐡ") or method_name == bstack1l11ll1_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫᐢ"):
            return bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_
        if method_name == bstack1l11ll1_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬᐣ"):
            return bstack1lllll1l111_opy_.bstack1lllll11ll1_opy_
        if method_name == bstack1l11ll1_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪᐤ"):
            return bstack1lllll1l111_opy_.QUIT
        return bstack1lllll1l111_opy_.NONE
    @staticmethod
    def bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_]):
        return bstack1l11ll1_opy_ (u"ࠧࡀࠢᐥ").join((bstack1lllll1l111_opy_(bstack1lllll1llll_opy_[0]).name, bstack1llll1l11ll_opy_(bstack1lllll1llll_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll111l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1ll1l1lllll_opy_.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        if not bstack1l11l111l11_opy_ in bstack1ll1l1lllll_opy_.bstack1l11l11l1ll_opy_:
            bstack1ll1l1lllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l111l11_opy_] = []
        bstack1ll1l1lllll_opy_.bstack1l11l11l1ll_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1ll11l11l11_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11l1lll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11l1ll1l_opy_(instance: bstack1lllllll111_opy_, default_value=None):
        return bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l111lll1_opy_, default_value)
    @staticmethod
    def bstack1l1lllll1l1_opy_(instance: bstack1lllllll111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11lll111_opy_(instance: bstack1lllllll111_opy_, default_value=None):
        return bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111l111l_opy_(method_name: str, *args):
        if not bstack1ll1l1lllll_opy_.bstack1ll11l11l11_opy_(method_name):
            return False
        if not bstack1ll1l1lllll_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1lllll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll11111111_opy_ = bstack1ll1l1lllll_opy_.bstack1l1llllll1l_opy_(*args)
        return bstack1ll11111111_opy_ and bstack1l11ll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐦ") in bstack1ll11111111_opy_ and bstack1l11ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᐧ") in bstack1ll11111111_opy_[bstack1l11ll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᐨ")]
    @staticmethod
    def bstack1ll11ll11l1_opy_(method_name: str, *args):
        if not bstack1ll1l1lllll_opy_.bstack1ll11l11l11_opy_(method_name):
            return False
        if not bstack1ll1l1lllll_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1lllll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll11111111_opy_ = bstack1ll1l1lllll_opy_.bstack1l1llllll1l_opy_(*args)
        return (
            bstack1ll11111111_opy_
            and bstack1l11ll1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐩ") in bstack1ll11111111_opy_
            and bstack1l11ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᐪ") in bstack1ll11111111_opy_[bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐫ")]
        )
    @staticmethod
    def bstack1l11ll1l11l_opy_(*args):
        return str(bstack1ll1l1lllll_opy_.bstack1ll1l111111_opy_(*args)).lower()