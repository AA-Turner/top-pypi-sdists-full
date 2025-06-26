# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1llllll1111_opy_,
    bstack1111111l1l_opy_,
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111111l_opy_(bstack1llllll1111_opy_):
    bstack1l11l1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᏉ")
    bstack1l1l11l11ll_opy_ = bstack11ll1l1_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᏊ")
    bstack1l1l11lllll_opy_ = bstack11ll1l1_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᏋ")
    bstack1l1l1l11111_opy_ = bstack11ll1l1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᏌ")
    bstack1l11l1l1l11_opy_ = bstack11ll1l1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᏍ")
    bstack1l11l1l1lll_opy_ = bstack11ll1l1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᏎ")
    NAME = bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᏏ")
    bstack1l11l1l1l1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1llll1l1_opy_: Any
    bstack1l11l11lll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11ll1l1_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᏐ"), bstack11ll1l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᏑ"), bstack11ll1l1_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᏒ"), bstack11ll1l1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᏓ"), bstack11ll1l1_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᏔ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll1lll1_opy_(methods)
    def bstack111111l111_opy_(self, instance: bstack1111111l1l_opy_, method_name: str, bstack1llll1llll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllll1l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111111lll_opy_, bstack1l11l1l11ll_opy_ = bstack1llllllllll_opy_
        bstack1l11l1l111l_opy_ = bstack1lll111111l_opy_.bstack1l11l11llll_opy_(bstack1llllllllll_opy_)
        if bstack1l11l1l111l_opy_ in bstack1lll111111l_opy_.bstack1l11l1l1l1l_opy_:
            bstack1l11l1l11l1_opy_ = None
            for callback in bstack1lll111111l_opy_.bstack1l11l1l1l1l_opy_[bstack1l11l1l111l_opy_]:
                try:
                    bstack1l11l1l1ll1_opy_ = callback(self, target, exec, bstack1llllllllll_opy_, result, *args, **kwargs)
                    if bstack1l11l1l11l1_opy_ == None:
                        bstack1l11l1l11l1_opy_ = bstack1l11l1l1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᏕ") + str(e) + bstack11ll1l1_opy_ (u"ࠥࠦᏖ"))
                    traceback.print_exc()
            if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.PRE and callable(bstack1l11l1l11l1_opy_):
                return bstack1l11l1l11l1_opy_
            elif bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST and bstack1l11l1l11l1_opy_:
                return bstack1l11l1l11l1_opy_
    def bstack1lllll1l1l1_opy_(
        self, method_name, previous_state: bstack1lllll1ll11_opy_, *args, **kwargs
    ) -> bstack1lllll1ll11_opy_:
        if method_name == bstack11ll1l1_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫᏗ") or method_name == bstack11ll1l1_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭Ꮨ") or method_name == bstack11ll1l1_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨᏙ"):
            return bstack1lllll1ll11_opy_.bstack11111111l1_opy_
        if method_name == bstack11ll1l1_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩᏚ"):
            return bstack1lllll1ll11_opy_.bstack1111111l11_opy_
        if method_name == bstack11ll1l1_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧᏛ"):
            return bstack1lllll1ll11_opy_.QUIT
        return bstack1lllll1ll11_opy_.NONE
    @staticmethod
    def bstack1l11l11llll_opy_(bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_]):
        return bstack11ll1l1_opy_ (u"ࠤ࠽ࠦᏜ").join((bstack1lllll1ll11_opy_(bstack1llllllllll_opy_[0]).name, bstack1llllll1ll1_opy_(bstack1llllllllll_opy_[1]).name))
    @staticmethod
    def bstack1ll11l11lll_opy_(bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_], callback: Callable):
        bstack1l11l1l111l_opy_ = bstack1lll111111l_opy_.bstack1l11l11llll_opy_(bstack1llllllllll_opy_)
        if not bstack1l11l1l111l_opy_ in bstack1lll111111l_opy_.bstack1l11l1l1l1l_opy_:
            bstack1lll111111l_opy_.bstack1l11l1l1l1l_opy_[bstack1l11l1l111l_opy_] = []
        bstack1lll111111l_opy_.bstack1l11l1l1l1l_opy_[bstack1l11l1l111l_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1lll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11l1111l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11l1llll_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1lll111111l_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1l1lllll11l_opy_(instance: bstack1111111l1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1lll111111l_opy_.bstack1l1l11lllll_opy_, default_value)
    @staticmethod
    def bstack1ll1l111ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1lll111111l_opy_.bstack1ll11l1lll1_opy_(method_name):
            return False
        if not bstack1lll111111l_opy_.bstack1l11l1l1l11_opy_ in bstack1lll111111l_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1lll111111l_opy_.bstack1ll1111ll11_opy_(*args)
        return bstack1ll1111lll1_opy_ and bstack11ll1l1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᏝ") in bstack1ll1111lll1_opy_ and bstack11ll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᏞ") in bstack1ll1111lll1_opy_[bstack11ll1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᏟ")]
    @staticmethod
    def bstack1ll11llll1l_opy_(method_name: str, *args):
        if not bstack1lll111111l_opy_.bstack1ll11l1lll1_opy_(method_name):
            return False
        if not bstack1lll111111l_opy_.bstack1l11l1l1l11_opy_ in bstack1lll111111l_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1lll111111l_opy_.bstack1ll1111ll11_opy_(*args)
        return (
            bstack1ll1111lll1_opy_
            and bstack11ll1l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᏠ") in bstack1ll1111lll1_opy_
            and bstack11ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᏡ") in bstack1ll1111lll1_opy_[bstack11ll1l1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᏢ")]
        )
    @staticmethod
    def bstack1l11ll1l11l_opy_(*args):
        return str(bstack1lll111111l_opy_.bstack1ll1l111ll1_opy_(*args)).lower()