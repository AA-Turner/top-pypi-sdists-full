# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111ll1_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1lll1l1_opy_(bstack1111111ll1_opy_):
    bstack1l11l1ll1ll_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᎨ")
    bstack1l1l1l11l11_opy_ = bstack11ll11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᎩ")
    bstack1l1l1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᎪ")
    bstack1l1l1l11111_opy_ = bstack11ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎫ")
    bstack1l11l1ll1l1_opy_ = bstack11ll11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᎬ")
    bstack1l11l1llll1_opy_ = bstack11ll11_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᎭ")
    NAME = bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᎮ")
    bstack1l11l1ll111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll111l11l_opy_: Any
    bstack1l11ll11111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11ll11_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᎯ"), bstack11ll11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣᎰ"), bstack11ll11_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᎱ"), bstack11ll11_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᎲ"), bstack11ll11_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᎳ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
    def bstack111111l11l_opy_(self, instance: bstack1llll1ll1ll_opy_, method_name: str, bstack11111111ll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll1lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllllll11l_opy_, bstack1l11l1lll11_opy_ = bstack111111111l_opy_
        bstack1l11l1l1lll_opy_ = bstack1lll1lll1l1_opy_.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        if bstack1l11l1l1lll_opy_ in bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_:
            bstack1l11l1lllll_opy_ = None
            for callback in bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_[bstack1l11l1l1lll_opy_]:
                try:
                    bstack1l11l1lll1l_opy_ = callback(self, target, exec, bstack111111111l_opy_, result, *args, **kwargs)
                    if bstack1l11l1lllll_opy_ == None:
                        bstack1l11l1lllll_opy_ = bstack1l11l1lll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᎴ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨᎵ"))
                    traceback.print_exc()
            if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l1lllll_opy_):
                return bstack1l11l1lllll_opy_
            elif bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l1lllll_opy_:
                return bstack1l11l1lllll_opy_
    def bstack1111111lll_opy_(
        self, method_name, previous_state: bstack1111111l11_opy_, *args, **kwargs
    ) -> bstack1111111l11_opy_:
        if method_name == bstack11ll11_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭Ꮆ") or method_name == bstack11ll11_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᎷ") or method_name == bstack11ll11_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪᎸ"):
            return bstack1111111l11_opy_.bstack1llllll11l1_opy_
        if method_name == bstack11ll11_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫᎹ"):
            return bstack1111111l11_opy_.bstack1lllllll1ll_opy_
        if method_name == bstack11ll11_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᎺ"):
            return bstack1111111l11_opy_.QUIT
        return bstack1111111l11_opy_.NONE
    @staticmethod
    def bstack1l11l1ll11l_opy_(bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_]):
        return bstack11ll11_opy_ (u"ࠦ࠿ࠨᎻ").join((bstack1111111l11_opy_(bstack111111111l_opy_[0]).name, bstack1llllll1111_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l1l1lll_opy_ = bstack1lll1lll1l1_opy_.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        if not bstack1l11l1l1lll_opy_ in bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_:
            bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_[bstack1l11l1l1lll_opy_] = []
        bstack1lll1lll1l1_opy_.bstack1l11l1ll111_opy_[bstack1l11l1l1lll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l11ll1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11lllll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1llll1ll1ll_opy_, default_value=None):
        return bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1ll11111ll1_opy_(instance: bstack1llll1ll1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11lll1ll_opy_(instance: bstack1llll1ll1ll_opy_, default_value=None):
        return bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1l11l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11l1ll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111lll11_opy_(method_name: str, *args):
        if not bstack1lll1lll1l1_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1lll1lll1l1_opy_.bstack1l11l1ll1l1_opy_ in bstack1lll1lll1l1_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1lll1lll1l1_opy_.bstack1ll111l1ll1_opy_(*args)
        return bstack1ll1111lll1_opy_ and bstack11ll11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᎼ") in bstack1ll1111lll1_opy_ and bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᎽ") in bstack1ll1111lll1_opy_[bstack11ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᎾ")]
    @staticmethod
    def bstack1ll11lll1l1_opy_(method_name: str, *args):
        if not bstack1lll1lll1l1_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1lll1lll1l1_opy_.bstack1l11l1ll1l1_opy_ in bstack1lll1lll1l1_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1lll1lll1l1_opy_.bstack1ll111l1ll1_opy_(*args)
        return (
            bstack1ll1111lll1_opy_
            and bstack11ll11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᎿ") in bstack1ll1111lll1_opy_
            and bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᏀ") in bstack1ll1111lll1_opy_[bstack11ll11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᏁ")]
        )
    @staticmethod
    def bstack1l1l11111l1_opy_(*args):
        return str(bstack1lll1lll1l1_opy_.bstack1ll11l1ll1l_opy_(*args)).lower()