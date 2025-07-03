# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import (
    bstack1lllllll111_opy_,
    bstack1lllll1l1l1_opy_,
    bstack1lllll1ll11_opy_,
    bstack1llllll111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll11lll1_opy_(bstack1lllllll111_opy_):
    bstack1l11l1l11l1_opy_ = bstack1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ᐀")
    bstack1l1l11l11ll_opy_ = bstack1l1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᐁ")
    bstack1l1l11l1ll1_opy_ = bstack1l1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᐂ")
    bstack1l1l11l1l1l_opy_ = bstack1l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᐃ")
    bstack1l11l11lll1_opy_ = bstack1l1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᐄ")
    bstack1l11l1l111l_opy_ = bstack1l1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᐅ")
    NAME = bstack1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᐆ")
    bstack1l11l11ll1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll111l111_opy_: Any
    bstack1l11l11llll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᐇ"), bstack1l1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᐈ"), bstack1l1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᐉ"), bstack1l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᐊ"), bstack1l1_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᐋ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllllll1l_opy_(methods)
    def bstack11111111ll_opy_(self, instance: bstack1lllll1l1l1_opy_, method_name: str, bstack1lllll11lll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lllll1lll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1l1l1_opy_, str],
        bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llllll1ll1_opy_, bstack1l11l11l1l1_opy_ = bstack1111111l1l_opy_
        bstack1l11l1l1111_opy_ = bstack1llll11lll1_opy_.bstack1l11l11ll11_opy_(bstack1111111l1l_opy_)
        if bstack1l11l1l1111_opy_ in bstack1llll11lll1_opy_.bstack1l11l11ll1l_opy_:
            bstack1l11l11l1ll_opy_ = None
            for callback in bstack1llll11lll1_opy_.bstack1l11l11ll1l_opy_[bstack1l11l1l1111_opy_]:
                try:
                    bstack1l11l1l11ll_opy_ = callback(self, target, exec, bstack1111111l1l_opy_, result, *args, **kwargs)
                    if bstack1l11l11l1ll_opy_ == None:
                        bstack1l11l11l1ll_opy_ = bstack1l11l1l11ll_opy_
                except Exception as e:
                    self.logger.error(bstack1l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᐌ") + str(e) + bstack1l1_opy_ (u"ࠤࠥᐍ"))
                    traceback.print_exc()
            if bstack1l11l11l1l1_opy_ == bstack1llllll111l_opy_.PRE and callable(bstack1l11l11l1ll_opy_):
                return bstack1l11l11l1ll_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1llllll111l_opy_.POST and bstack1l11l11l1ll_opy_:
                return bstack1l11l11l1ll_opy_
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1lllll1ll11_opy_, *args, **kwargs
    ) -> bstack1lllll1ll11_opy_:
        if method_name == bstack1l1_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᐎ") or method_name == bstack1l1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᐏ") or method_name == bstack1l1_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᐐ"):
            return bstack1lllll1ll11_opy_.bstack1llll1l1lll_opy_
        if method_name == bstack1l1_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨᐑ"):
            return bstack1lllll1ll11_opy_.bstack1lllllll1ll_opy_
        if method_name == bstack1l1_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ᐒ"):
            return bstack1lllll1ll11_opy_.QUIT
        return bstack1lllll1ll11_opy_.NONE
    @staticmethod
    def bstack1l11l11ll11_opy_(bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_]):
        return bstack1l1_opy_ (u"ࠣ࠼ࠥᐓ").join((bstack1lllll1ll11_opy_(bstack1111111l1l_opy_[0]).name, bstack1llllll111l_opy_(bstack1111111l1l_opy_[1]).name))
    @staticmethod
    def bstack1ll111lllll_opy_(bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_], callback: Callable):
        bstack1l11l1l1111_opy_ = bstack1llll11lll1_opy_.bstack1l11l11ll11_opy_(bstack1111111l1l_opy_)
        if not bstack1l11l1l1111_opy_ in bstack1llll11lll1_opy_.bstack1l11l11ll1l_opy_:
            bstack1llll11lll1_opy_.bstack1l11l11ll1l_opy_[bstack1l11l1l1111_opy_] = []
        bstack1llll11lll1_opy_.bstack1l11l11ll1l_opy_[bstack1l11l1l1111_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11ll11ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll111ll11l_opy_(instance: bstack1lllll1l1l1_opy_, default_value=None):
        return bstack1lllllll111_opy_.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l11l1l1l_opy_, default_value)
    @staticmethod
    def bstack1l1llll1ll1_opy_(instance: bstack1lllll1l1l1_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11l111l1_opy_(instance: bstack1lllll1l1l1_opy_, default_value=None):
        return bstack1lllllll111_opy_.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11llll1l_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l11l11lll1_opy_ in bstack1llll11lll1_opy_.bstack1l11llll1l1_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1llll11lll1_opy_.bstack1ll1111l11l_opy_(*args)
        return bstack1ll1111l1ll_opy_ and bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐔ") in bstack1ll1111l1ll_opy_ and bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᐕ") in bstack1ll1111l1ll_opy_[bstack1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐖ")]
    @staticmethod
    def bstack1ll111llll1_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l11l11lll1_opy_ in bstack1llll11lll1_opy_.bstack1l11llll1l1_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1llll11lll1_opy_.bstack1ll1111l11l_opy_(*args)
        return (
            bstack1ll1111l1ll_opy_
            and bstack1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐗ") in bstack1ll1111l1ll_opy_
            and bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᐘ") in bstack1ll1111l1ll_opy_[bstack1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᐙ")]
        )
    @staticmethod
    def bstack1l11llll1l1_opy_(*args):
        return str(bstack1llll11lll1_opy_.bstack1ll11ll1ll1_opy_(*args)).lower()