# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1lll1_opy_,
    bstack1ll1lll1111_opy_,
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll11l1111l_opy_(bstack1ll1ll1lll1_opy_):
    bstack11lll11l1l1_opy_ = bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᗩ")
    bstack1l111l111l1_opy_ = bstack11ll111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᗪ")
    bstack1l111l11ll1_opy_ = bstack11ll111_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᗫ")
    bstack1l111l11111_opy_ = bstack11ll111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᗬ")
    bstack11lll11ll11_opy_ = bstack11ll111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᗭ")
    bstack11lll11ll1l_opy_ = bstack11ll111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᗮ")
    NAME = bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᗯ")
    bstack11lll1l1111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l1l1111_opy_: Any
    bstack11lll11lll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11ll111_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᗰ"), bstack11ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᗱ"), bstack11ll111_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᗲ"), bstack11ll111_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᗳ"), bstack11ll111_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᗴ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll111ll1l_opy_(methods)
    def bstack1lll11l1l11_opy_(self, instance: bstack1ll1lll1111_opy_, method_name: str, bstack1lll11l111l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1lll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll111111l_opy_, bstack11lll11l111_opy_ = bstack1ll1ll1llll_opy_
        bstack11lll11l1ll_opy_ = bstack1ll11l1111l_opy_.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        if bstack11lll11l1ll_opy_ in bstack1ll11l1111l_opy_.bstack11lll1l1111_opy_:
            bstack11lll11llll_opy_ = None
            for callback in bstack1ll11l1111l_opy_.bstack11lll1l1111_opy_[bstack11lll11l1ll_opy_]:
                try:
                    bstack11lll11l11l_opy_ = callback(self, target, exec, bstack1ll1ll1llll_opy_, result, *args, **kwargs)
                    if bstack11lll11llll_opy_ == None:
                        bstack11lll11llll_opy_ = bstack11lll11l11l_opy_
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᗵ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᗶ"))
                    traceback.print_exc()
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.PRE and callable(bstack11lll11llll_opy_):
                return bstack11lll11llll_opy_
            elif bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST and bstack11lll11llll_opy_:
                return bstack11lll11llll_opy_
    def bstack1lll1111lll_opy_(
        self, method_name, previous_state: bstack1ll1ll1l1l1_opy_, *args, **kwargs
    ) -> bstack1ll1ll1l1l1_opy_:
        if method_name == bstack11ll111_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᗷ") or method_name == bstack11ll111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᗸ") or method_name == bstack11ll111_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ᗹ"):
            return bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_
        if method_name == bstack11ll111_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧᗺ"):
            return bstack1ll1ll1l1l1_opy_.bstack1lll111lll1_opy_
        if method_name == bstack11ll111_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬᗻ"):
            return bstack1ll1ll1l1l1_opy_.QUIT
        return bstack1ll1ll1l1l1_opy_.NONE
    @staticmethod
    def bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_]):
        return bstack11ll111_opy_ (u"ࠢ࠻ࠤᗼ").join((bstack1ll1ll1l1l1_opy_(bstack1ll1ll1llll_opy_[0]).name, bstack1lll111l1l1_opy_(bstack1ll1ll1llll_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll11l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_], callback: Callable):
        bstack11lll11l1ll_opy_ = bstack1ll11l1111l_opy_.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        if not bstack11lll11l1ll_opy_ in bstack1ll11l1111l_opy_.bstack11lll1l1111_opy_:
            bstack1ll11l1111l_opy_.bstack11lll1l1111_opy_[bstack11lll11l1ll_opy_] = []
        bstack1ll11l1111l_opy_.bstack11lll1l1111_opy_[bstack11lll11l1ll_opy_].append(callback)
    @staticmethod
    def bstack1l1l1l11111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l11lll1l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1ll1l11ll_opy_(instance: bstack1ll1lll1111_opy_, default_value=None):
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll11l1111l_opy_.bstack1l111l11111_opy_, default_value)
    @staticmethod
    def bstack1l1l1111l1l_opy_(instance: bstack1ll1lll1111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1ll1l1111_opy_(instance: bstack1ll1lll1111_opy_, default_value=None):
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll11l1111l_opy_.bstack1l111l11ll1_opy_, default_value)
    @staticmethod
    def bstack1l1l11ll111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1ll111l1l_opy_(method_name: str, *args):
        if not bstack1ll11l1111l_opy_.bstack1l1l1l11111_opy_(method_name):
            return False
        if not bstack1ll11l1111l_opy_.bstack11lll11ll11_opy_ in bstack1ll11l1111l_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111lll1_opy_ = bstack1ll11l1111l_opy_.bstack1l1l111llll_opy_(*args)
        return bstack1l1l111lll1_opy_ and bstack11ll111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᗽ") in bstack1l1l111lll1_opy_ and bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᗾ") in bstack1l1l111lll1_opy_[bstack11ll111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᗿ")]
    @staticmethod
    def bstack1l1l1llll11_opy_(method_name: str, *args):
        if not bstack1ll11l1111l_opy_.bstack1l1l1l11111_opy_(method_name):
            return False
        if not bstack1ll11l1111l_opy_.bstack11lll11ll11_opy_ in bstack1ll11l1111l_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111lll1_opy_ = bstack1ll11l1111l_opy_.bstack1l1l111llll_opy_(*args)
        return (
            bstack1l1l111lll1_opy_
            and bstack11ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᘀ") in bstack1l1l111lll1_opy_
            and bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᘁ") in bstack1l1l111lll1_opy_[bstack11ll111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᘂ")]
        )
    @staticmethod
    def bstack11llll1l111_opy_(*args):
        return str(bstack1ll11l1111l_opy_.bstack1l1l11ll111_opy_(*args)).lower()