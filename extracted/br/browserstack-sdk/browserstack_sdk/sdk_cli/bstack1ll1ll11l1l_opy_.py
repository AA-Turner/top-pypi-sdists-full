# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1llllllll11_opy_,
    bstack1llllllll1l_opy_,
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1lll1lll_opy_(bstack1llllllll11_opy_):
    bstack1l11l11l1l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᐔ")
    bstack1l1l111llll_opy_ = bstack1111l1l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᐕ")
    bstack1l1l111ll11_opy_ = bstack1111l1l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᐖ")
    bstack1l1l111ll1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᐗ")
    bstack1l11l11l1ll_opy_ = bstack1111l1l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᐘ")
    bstack1l11l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᐙ")
    NAME = bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᐚ")
    bstack1l11l11l111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l1l_opy_: Any
    bstack1l11l11ll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1111l1l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᐛ"), bstack1111l1l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᐜ"), bstack1111l1l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᐝ"), bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᐞ"), bstack1111l1l_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᐟ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll111ll_opy_(methods)
    def bstack1lllllll1l1_opy_(self, instance: bstack1llllllll1l_opy_, method_name: str, bstack1lllll1l1l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1llll1_opy_, bstack1l11l111ll1_opy_ = bstack1lllll11ll1_opy_
        bstack1l11l111l11_opy_ = bstack1ll1lll1lll_opy_.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        if bstack1l11l111l11_opy_ in bstack1ll1lll1lll_opy_.bstack1l11l11l111_opy_:
            bstack1l11l111l1l_opy_ = None
            for callback in bstack1ll1lll1lll_opy_.bstack1l11l11l111_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11l11l_opy_ = callback(self, target, exec, bstack1lllll11ll1_opy_, result, *args, **kwargs)
                    if bstack1l11l111l1l_opy_ == None:
                        bstack1l11l111l1l_opy_ = bstack1l11l11l11l_opy_
                except Exception as e:
                    self.logger.error(bstack1111l1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᐠ") + str(e) + bstack1111l1l_opy_ (u"ࠣࠤᐡ"))
                    traceback.print_exc()
            if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.PRE and callable(bstack1l11l111l1l_opy_):
                return bstack1l11l111l1l_opy_
            elif bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST and bstack1l11l111l1l_opy_:
                return bstack1l11l111l1l_opy_
    def bstack1lllll11l11_opy_(
        self, method_name, previous_state: bstack1lllll11111_opy_, *args, **kwargs
    ) -> bstack1lllll11111_opy_:
        if method_name == bstack1111l1l_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᐢ") or method_name == bstack1111l1l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᐣ") or method_name == bstack1111l1l_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᐤ"):
            return bstack1lllll11111_opy_.bstack1lllll1ll11_opy_
        if method_name == bstack1111l1l_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᐥ"):
            return bstack1lllll11111_opy_.bstack1lllll1lll1_opy_
        if method_name == bstack1111l1l_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᐦ"):
            return bstack1lllll11111_opy_.QUIT
        return bstack1lllll11111_opy_.NONE
    @staticmethod
    def bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_]):
        return bstack1111l1l_opy_ (u"ࠢ࠻ࠤᐧ").join((bstack1lllll11111_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1llll1lllll_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1ll1lll1lll_opy_.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l111l11_opy_ in bstack1ll1lll1lll_opy_.bstack1l11l11l111_opy_:
            bstack1ll1lll1lll_opy_.bstack1l11l11l111_opy_[bstack1l11l111l11_opy_] = []
        bstack1ll1lll1lll_opy_.bstack1l11l11l111_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1ll111l111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1111l1ll_opy_(instance: bstack1llllllll1l_opy_, default_value=None):
        return bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l111ll1l_opy_, default_value)
    @staticmethod
    def bstack1l1lllll111_opy_(instance: bstack1llllllll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11l11l1l_opy_(instance: bstack1llllllll1l_opy_, default_value=None):
        return bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l111ll11_opy_, default_value)
    @staticmethod
    def bstack1ll111llll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111ll1_opy_(method_name: str, *args):
        if not bstack1ll1lll1lll_opy_.bstack1ll111l111l_opy_(method_name):
            return False
        if not bstack1ll1lll1lll_opy_.bstack1l11l11l1ll_opy_ in bstack1ll1lll1lll_opy_.bstack1l11ll111l1_opy_(*args):
            return False
        bstack1ll1111l111_opy_ = bstack1ll1lll1lll_opy_.bstack1ll111111l1_opy_(*args)
        return bstack1ll1111l111_opy_ and bstack1111l1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᐨ") in bstack1ll1111l111_opy_ and bstack1111l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᐩ") in bstack1ll1111l111_opy_[bstack1111l1l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᐪ")]
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1ll1lll1lll_opy_.bstack1ll111l111l_opy_(method_name):
            return False
        if not bstack1ll1lll1lll_opy_.bstack1l11l11l1ll_opy_ in bstack1ll1lll1lll_opy_.bstack1l11ll111l1_opy_(*args):
            return False
        bstack1ll1111l111_opy_ = bstack1ll1lll1lll_opy_.bstack1ll111111l1_opy_(*args)
        return (
            bstack1ll1111l111_opy_
            and bstack1111l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐫ") in bstack1ll1111l111_opy_
            and bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᐬ") in bstack1ll1111l111_opy_[bstack1111l1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐭ")]
        )
    @staticmethod
    def bstack1l11ll111l1_opy_(*args):
        return str(bstack1ll1lll1lll_opy_.bstack1ll111llll1_opy_(*args)).lower()