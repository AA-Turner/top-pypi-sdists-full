# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1lll11ll1l1_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1l1lllll1ll_opy_(bstack1lll11ll1l1_opy_):
    bstack11lll11l1ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᗬ")
    bstack1l111l1l111_opy_ = bstack11l1l11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᗭ")
    bstack1l111l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᗮ")
    bstack1l1111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᗯ")
    bstack11lll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᗰ")
    bstack11lll11l11l_opy_ = bstack11l1l11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᗱ")
    NAME = bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᗲ")
    bstack11lll1l1111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll111l1l1l_opy_: Any
    bstack11lll1l11l1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1l11_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᗳ"), bstack11l1l11_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᗴ"), bstack11l1l11_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᗵ"), bstack11l1l11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᗶ"), bstack11l1l11_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᗷ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1lll11l1_opy_(methods)
    def bstack1ll1ll1l1l1_opy_(self, instance: bstack1ll1llll111_opy_, method_name: str, bstack1lll11l1111_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll111111l_opy_, bstack11lll1l111l_opy_ = bstack1lll11ll111_opy_
        bstack11lll11lll1_opy_ = bstack1l1lllll1ll_opy_.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        if bstack11lll11lll1_opy_ in bstack1l1lllll1ll_opy_.bstack11lll1l1111_opy_:
            bstack11lll11llll_opy_ = None
            for callback in bstack1l1lllll1ll_opy_.bstack11lll1l1111_opy_[bstack11lll11lll1_opy_]:
                try:
                    bstack11lll11l1l1_opy_ = callback(self, target, exec, bstack1lll11ll111_opy_, result, *args, **kwargs)
                    if bstack11lll11llll_opy_ == None:
                        bstack11lll11llll_opy_ = bstack11lll11l1l1_opy_
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᗸ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᗹ"))
                    traceback.print_exc()
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.PRE and callable(bstack11lll11llll_opy_):
                return bstack11lll11llll_opy_
            elif bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST and bstack11lll11llll_opy_:
                return bstack11lll11llll_opy_
    def bstack1lll11l1lll_opy_(
        self, method_name, previous_state: bstack1ll1lll1lll_opy_, *args, **kwargs
    ) -> bstack1ll1lll1lll_opy_:
        if method_name == bstack11l1l11_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬᗺ") or method_name == bstack11l1l11_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᗻ") or method_name == bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩᗼ"):
            return bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪᗽ"):
            return bstack1ll1lll1lll_opy_.bstack1lll11l11l1_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨᗾ"):
            return bstack1ll1lll1lll_opy_.QUIT
        return bstack1ll1lll1lll_opy_.NONE
    @staticmethod
    def bstack11lll11ll11_opy_(bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_]):
        return bstack11l1l11_opy_ (u"ࠥ࠾ࠧᗿ").join((bstack1ll1lll1lll_opy_(bstack1lll11ll111_opy_[0]).name, bstack1lll11l111l_opy_(bstack1lll11ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1l11lll1l_opy_(bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_], callback: Callable):
        bstack11lll11lll1_opy_ = bstack1l1lllll1ll_opy_.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        if not bstack11lll11lll1_opy_ in bstack1l1lllll1ll_opy_.bstack11lll1l1111_opy_:
            bstack1l1lllll1ll_opy_.bstack11lll1l1111_opy_[bstack11lll11lll1_opy_] = []
        bstack1l1lllll1ll_opy_.bstack11lll1l1111_opy_[bstack11lll11lll1_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1ll1111l1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1l11ll1l1_opy_(instance: bstack1ll1llll111_opy_, default_value=None):
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1ll_opy_.bstack1l1111ll11l_opy_, default_value)
    @staticmethod
    def bstack1l1l1111l11_opy_(instance: bstack1ll1llll111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l11ll1ll_opy_(instance: bstack1ll1llll111_opy_, default_value=None):
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1ll_opy_.bstack1l111l1l11l_opy_, default_value)
    @staticmethod
    def bstack1l1l1l11lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1l1111l_opy_(method_name: str, *args):
        if not bstack1l1lllll1ll_opy_.bstack1l1ll1ll1ll_opy_(method_name):
            return False
        if not bstack1l1lllll1ll_opy_.bstack11lll11ll1l_opy_ in bstack1l1lllll1ll_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111llll_opy_ = bstack1l1lllll1ll_opy_.bstack1l1l11l1l11_opy_(*args)
        return bstack1l1l111llll_opy_ and bstack11l1l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᘀ") in bstack1l1l111llll_opy_ and bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᘁ") in bstack1l1l111llll_opy_[bstack11l1l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᘂ")]
    @staticmethod
    def bstack1l1l1llll1l_opy_(method_name: str, *args):
        if not bstack1l1lllll1ll_opy_.bstack1l1ll1ll1ll_opy_(method_name):
            return False
        if not bstack1l1lllll1ll_opy_.bstack11lll11ll1l_opy_ in bstack1l1lllll1ll_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111llll_opy_ = bstack1l1lllll1ll_opy_.bstack1l1l11l1l11_opy_(*args)
        return (
            bstack1l1l111llll_opy_
            and bstack11l1l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᘃ") in bstack1l1l111llll_opy_
            and bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᘄ") in bstack1l1l111llll_opy_[bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᘅ")]
        )
    @staticmethod
    def bstack11llll1l111_opy_(*args):
        return str(bstack1l1lllll1ll_opy_.bstack1l1l1l11lll_opy_(*args)).lower()