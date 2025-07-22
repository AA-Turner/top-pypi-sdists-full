# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack11111111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1llll11l_opy_(bstack11111111ll_opy_):
    bstack1l11l11lll1_opy_ = bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᐇ")
    bstack1l1l111lll1_opy_ = bstack111l111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᐈ")
    bstack1l1l11l11l1_opy_ = bstack111l111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᐉ")
    bstack1l1l111ll1l_opy_ = bstack111l111_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᐊ")
    bstack1l11l11l111_opy_ = bstack111l111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᐋ")
    bstack1l11l1l1111_opy_ = bstack111l111_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᐌ")
    NAME = bstack111l111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᐍ")
    bstack1l11l1l111l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll1l1l1_opy_: Any
    bstack1l11l11ll11_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111l111_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᐎ"), bstack111l111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᐏ"), bstack111l111_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᐐ"), bstack111l111_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᐑ"), bstack111l111_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᐒ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
    def bstack1llll1ll1l1_opy_(self, instance: bstack1lllll1ll1l_opy_, method_name: str, bstack1lllllll1l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lllll11l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll1lll1_opy_, bstack1l11l11l11l_opy_ = bstack1llllll111l_opy_
        bstack1l11l11l1l1_opy_ = bstack1ll1llll11l_opy_.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        if bstack1l11l11l1l1_opy_ in bstack1ll1llll11l_opy_.bstack1l11l1l111l_opy_:
            bstack1l11l11l1ll_opy_ = None
            for callback in bstack1ll1llll11l_opy_.bstack1l11l1l111l_opy_[bstack1l11l11l1l1_opy_]:
                try:
                    bstack1l11l11llll_opy_ = callback(self, target, exec, bstack1llllll111l_opy_, result, *args, **kwargs)
                    if bstack1l11l11l1ll_opy_ == None:
                        bstack1l11l11l1ll_opy_ = bstack1l11l11llll_opy_
                except Exception as e:
                    self.logger.error(bstack111l111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᐓ") + str(e) + bstack111l111_opy_ (u"ࠤࠥᐔ"))
                    traceback.print_exc()
            if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l11l1ll_opy_):
                return bstack1l11l11l1ll_opy_
            elif bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l11l1ll_opy_:
                return bstack1l11l11l1ll_opy_
    def bstack1111111l11_opy_(
        self, method_name, previous_state: bstack1lllllll11l_opy_, *args, **kwargs
    ) -> bstack1lllllll11l_opy_:
        if method_name == bstack111l111_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᐕ") or method_name == bstack111l111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᐖ") or method_name == bstack111l111_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᐗ"):
            return bstack1lllllll11l_opy_.bstack1lllll11lll_opy_
        if method_name == bstack111l111_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨᐘ"):
            return bstack1lllllll11l_opy_.bstack111111111l_opy_
        if method_name == bstack111l111_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ᐙ"):
            return bstack1lllllll11l_opy_.QUIT
        return bstack1lllllll11l_opy_.NONE
    @staticmethod
    def bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_]):
        return bstack111l111_opy_ (u"ࠣ࠼ࠥᐚ").join((bstack1lllllll11l_opy_(bstack1llllll111l_opy_[0]).name, bstack1llllll1111_opy_(bstack1llllll111l_opy_[1]).name))
    @staticmethod
    def bstack1ll11l1l11l_opy_(bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l11l1l1_opy_ = bstack1ll1llll11l_opy_.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        if not bstack1l11l11l1l1_opy_ in bstack1ll1llll11l_opy_.bstack1l11l1l111l_opy_:
            bstack1ll1llll11l_opy_.bstack1l11l1l111l_opy_[bstack1l11l11l1l1_opy_] = []
        bstack1ll1llll11l_opy_.bstack1l11l1l111l_opy_[bstack1l11l11l1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l11l11l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll111ll1ll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1l111ll1l_opy_, default_value)
    @staticmethod
    def bstack1l1llllll1l_opy_(instance: bstack1lllll1ll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111lll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1l11l11l1_opy_, default_value)
    @staticmethod
    def bstack1ll11llllll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111l1111_opy_(method_name: str, *args):
        if not bstack1ll1llll11l_opy_.bstack1ll11l1111l_opy_(method_name):
            return False
        if not bstack1ll1llll11l_opy_.bstack1l11l11l111_opy_ in bstack1ll1llll11l_opy_.bstack1l11llll11l_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1ll1llll11l_opy_.bstack1ll111111ll_opy_(*args)
        return bstack1ll1111l1ll_opy_ and bstack111l111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐛ") in bstack1ll1111l1ll_opy_ and bstack111l111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᐜ") in bstack1ll1111l1ll_opy_[bstack111l111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐝ")]
    @staticmethod
    def bstack1ll11ll1111_opy_(method_name: str, *args):
        if not bstack1ll1llll11l_opy_.bstack1ll11l1111l_opy_(method_name):
            return False
        if not bstack1ll1llll11l_opy_.bstack1l11l11l111_opy_ in bstack1ll1llll11l_opy_.bstack1l11llll11l_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1ll1llll11l_opy_.bstack1ll111111ll_opy_(*args)
        return (
            bstack1ll1111l1ll_opy_
            and bstack111l111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐞ") in bstack1ll1111l1ll_opy_
            and bstack111l111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᐟ") in bstack1ll1111l1ll_opy_[bstack111l111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᐠ")]
        )
    @staticmethod
    def bstack1l11llll11l_opy_(*args):
        return str(bstack1ll1llll11l_opy_.bstack1ll11llllll_opy_(*args)).lower()