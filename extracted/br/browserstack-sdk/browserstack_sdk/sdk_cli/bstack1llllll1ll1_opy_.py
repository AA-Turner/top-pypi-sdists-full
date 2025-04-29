# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import (
    bstack1lllllll11l_opy_,
    bstack111111ll11_opy_,
    bstack11111lll11_opy_,
    bstack1111111l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111l111_opy_(bstack1lllllll11l_opy_):
    bstack1l1l11111ll_opy_ = bstack1llllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣፏ")
    bstack1l1ll111lll_opy_ = bstack1llllll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤፐ")
    bstack1l1ll111ll1_opy_ = bstack1llllll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦፑ")
    bstack1l1ll111l1l_opy_ = bstack1llllll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥፒ")
    bstack1l1l1111111_opy_ = bstack1llllll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣፓ")
    bstack1l11llll1l1_opy_ = bstack1llllll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢፔ")
    NAME = bstack1llllll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦፕ")
    bstack1l1l111111l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1l1ll1_opy_: Any
    bstack1l11llll1ll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1llllll_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣፖ"), bstack1llllll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥፗ"), bstack1llllll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧፘ"), bstack1llllll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥፙ"), bstack1llllll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢፚ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
    def bstack1111111ll1_opy_(self, instance: bstack111111ll11_opy_, method_name: str, bstack11111ll111_opy_: timedelta, *args, **kwargs):
        pass
    def bstack111111ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l1111l_opy_, bstack1l11lllll11_opy_ = bstack1111111lll_opy_
        bstack1l11llllll1_opy_ = bstack1lll111l111_opy_.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        if bstack1l11llllll1_opy_ in bstack1lll111l111_opy_.bstack1l1l111111l_opy_:
            bstack1l11lllll1l_opy_ = None
            for callback in bstack1lll111l111_opy_.bstack1l1l111111l_opy_[bstack1l11llllll1_opy_]:
                try:
                    bstack1l11lllllll_opy_ = callback(self, target, exec, bstack1111111lll_opy_, result, *args, **kwargs)
                    if bstack1l11lllll1l_opy_ == None:
                        bstack1l11lllll1l_opy_ = bstack1l11lllllll_opy_
                except Exception as e:
                    self.logger.error(bstack1llllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦ፛") + str(e) + bstack1llllll_opy_ (u"ࠢࠣ፜"))
                    traceback.print_exc()
            if bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.PRE and callable(bstack1l11lllll1l_opy_):
                return bstack1l11lllll1l_opy_
            elif bstack1l11lllll11_opy_ == bstack1111111l1l_opy_.POST and bstack1l11lllll1l_opy_:
                return bstack1l11lllll1l_opy_
    def bstack1llllllll1l_opy_(
        self, method_name, previous_state: bstack11111lll11_opy_, *args, **kwargs
    ) -> bstack11111lll11_opy_:
        if method_name == bstack1llllll_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࠨ፝") or method_name == bstack1llllll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪ፞") or method_name == bstack1llllll_opy_ (u"ࠪࡲࡪࡽ࡟ࡱࡣࡪࡩࠬ፟"):
            return bstack11111lll11_opy_.bstack1111111l11_opy_
        if method_name == bstack1llllll_opy_ (u"ࠫࡩ࡯ࡳࡱࡣࡷࡧ࡭࠭፠"):
            return bstack11111lll11_opy_.bstack11111l11l1_opy_
        if method_name == bstack1llllll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫ፡"):
            return bstack11111lll11_opy_.QUIT
        return bstack11111lll11_opy_.NONE
    @staticmethod
    def bstack1l1l11111l1_opy_(bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_]):
        return bstack1llllll_opy_ (u"ࠨ࠺ࠣ።").join((bstack11111lll11_opy_(bstack1111111lll_opy_[0]).name, bstack1111111l1l_opy_(bstack1111111lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111l1l_opy_(bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = bstack1lll111l111_opy_.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        if not bstack1l11llllll1_opy_ in bstack1lll111l111_opy_.bstack1l1l111111l_opy_:
            bstack1lll111l111_opy_.bstack1l1l111111l_opy_[bstack1l11llllll1_opy_] = []
        bstack1lll111l111_opy_.bstack1l1l111111l_opy_[bstack1l11llllll1_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1ll111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11lll1ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11lllll1_opy_(instance: bstack111111ll11_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, bstack1lll111l111_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(instance: bstack111111ll11_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1l1lll_opy_(instance: bstack111111ll11_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack111111lll1_opy_(instance, bstack1lll111l111_opy_.bstack1l1ll111ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1lll111l111_opy_.bstack1ll1l1ll111_opy_(method_name):
            return False
        if not bstack1lll111l111_opy_.bstack1l1l1111111_opy_ in bstack1lll111l111_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11ll111l_opy_ = bstack1lll111l111_opy_.bstack1ll11ll1lll_opy_(*args)
        return bstack1ll11ll111l_opy_ and bstack1llllll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፣") in bstack1ll11ll111l_opy_ and bstack1llllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፤") in bstack1ll11ll111l_opy_[bstack1llllll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፥")]
    @staticmethod
    def bstack1ll1l1l111l_opy_(method_name: str, *args):
        if not bstack1lll111l111_opy_.bstack1ll1l1ll111_opy_(method_name):
            return False
        if not bstack1lll111l111_opy_.bstack1l1l1111111_opy_ in bstack1lll111l111_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11ll111l_opy_ = bstack1lll111l111_opy_.bstack1ll11ll1lll_opy_(*args)
        return (
            bstack1ll11ll111l_opy_
            and bstack1llllll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፦") in bstack1ll11ll111l_opy_
            and bstack1llllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢ፧") in bstack1ll11ll111l_opy_[bstack1llllll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፨")]
        )
    @staticmethod
    def bstack1l1l11l1l1l_opy_(*args):
        return str(bstack1lll111l111_opy_.bstack1ll1ll1111l_opy_(*args)).lower()