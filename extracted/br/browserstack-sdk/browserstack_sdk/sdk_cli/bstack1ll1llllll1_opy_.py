# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll111l_opy_,
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll11lll1_opy_(bstack1111111l11_opy_):
    bstack1l11ll1ll11_opy_ = bstack111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ᎚")
    bstack1l1l1llll11_opy_ = bstack111lll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ᎛")
    bstack1l1l1lll1l1_opy_ = bstack111lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤ᎜")
    bstack1l1l1l1l1ll_opy_ = bstack111lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᎝")
    bstack1l11ll1l111_opy_ = bstack111lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨ᎞")
    bstack1l11ll1lll1_opy_ = bstack111lll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧ᎟")
    NAME = bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᎠ")
    bstack1l11ll1l11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1l1ll1_opy_: Any
    bstack1l11ll1llll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111lll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᎡ"), bstack111lll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣᎢ"), bstack111lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᎣ"), bstack111lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᎤ"), bstack111lll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᎥ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll1l1ll_opy_(methods)
    def bstack11111111l1_opy_(self, instance: bstack1llllll111l_opy_, method_name: str, bstack111111111l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll1llll_opy_, bstack1l11ll1l1l1_opy_ = bstack11111l1l11_opy_
        bstack1l11ll1ll1l_opy_ = bstack1llll11lll1_opy_.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        if bstack1l11ll1ll1l_opy_ in bstack1llll11lll1_opy_.bstack1l11ll1l11l_opy_:
            bstack1l11ll1l1ll_opy_ = None
            for callback in bstack1llll11lll1_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1ll1l_opy_]:
                try:
                    bstack1l11ll11lll_opy_ = callback(self, target, exec, bstack11111l1l11_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l1ll_opy_ == None:
                        bstack1l11ll1l1ll_opy_ = bstack1l11ll11lll_opy_
                except Exception as e:
                    self.logger.error(bstack111lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᎦ") + str(e) + bstack111lll_opy_ (u"ࠧࠨᎧ"))
                    traceback.print_exc()
            if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.PRE and callable(bstack1l11ll1l1ll_opy_):
                return bstack1l11ll1l1ll_opy_
            elif bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST and bstack1l11ll1l1ll_opy_:
                return bstack1l11ll1l1ll_opy_
    def bstack1llllll1ll1_opy_(
        self, method_name, previous_state: bstack1111111111_opy_, *args, **kwargs
    ) -> bstack1111111111_opy_:
        if method_name == bstack111lll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭Ꭸ") or method_name == bstack111lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᎩ") or method_name == bstack111lll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪᎪ"):
            return bstack1111111111_opy_.bstack1lllllll1l1_opy_
        if method_name == bstack111lll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫᎫ"):
            return bstack1111111111_opy_.bstack1lllll1lll1_opy_
        if method_name == bstack111lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᎬ"):
            return bstack1111111111_opy_.QUIT
        return bstack1111111111_opy_.NONE
    @staticmethod
    def bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_]):
        return bstack111lll_opy_ (u"ࠦ࠿ࠨᎭ").join((bstack1111111111_opy_(bstack11111l1l11_opy_[0]).name, bstack11111l1ll1_opy_(bstack11111l1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll1l1l_opy_(bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_], callback: Callable):
        bstack1l11ll1ll1l_opy_ = bstack1llll11lll1_opy_.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        if not bstack1l11ll1ll1l_opy_ in bstack1llll11lll1_opy_.bstack1l11ll1l11l_opy_:
            bstack1llll11lll1_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1ll1l_opy_] = []
        bstack1llll11lll1_opy_.bstack1l11ll1l11l_opy_[bstack1l11ll1ll1l_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l11l111_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l11l11l_opy_(instance: bstack1llllll111l_opy_, default_value=None):
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll111l111l_opy_(instance: bstack1llllll111l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1l11l1_opy_(instance: bstack1llllll111l_opy_, default_value=None):
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1lll1l1_opy_, default_value)
    @staticmethod
    def bstack1ll1l111lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l11ll1l111_opy_ in bstack1llll11lll1_opy_.bstack1l1l111l11l_opy_(*args):
            return False
        bstack1ll11l11ll1_opy_ = bstack1llll11lll1_opy_.bstack1ll11l11lll_opy_(*args)
        return bstack1ll11l11ll1_opy_ and bstack111lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᎮ") in bstack1ll11l11ll1_opy_ and bstack111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᎯ") in bstack1ll11l11ll1_opy_[bstack111lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᎰ")]
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l11ll1l111_opy_ in bstack1llll11lll1_opy_.bstack1l1l111l11l_opy_(*args):
            return False
        bstack1ll11l11ll1_opy_ = bstack1llll11lll1_opy_.bstack1ll11l11lll_opy_(*args)
        return (
            bstack1ll11l11ll1_opy_
            and bstack111lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᎱ") in bstack1ll11l11ll1_opy_
            and bstack111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᎲ") in bstack1ll11l11ll1_opy_[bstack111lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᎳ")]
        )
    @staticmethod
    def bstack1l1l111l11l_opy_(*args):
        return str(bstack1llll11lll1_opy_.bstack1ll1l111lll_opy_(*args)).lower()