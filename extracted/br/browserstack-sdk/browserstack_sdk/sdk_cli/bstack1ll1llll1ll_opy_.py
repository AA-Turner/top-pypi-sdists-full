# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111l11l_opy_,
    bstack11111111ll_opy_,
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111ll11_opy_(bstack111111l11l_opy_):
    bstack1l11lllll11_opy_ = bstack1l11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨፍ")
    bstack1l1ll111l1l_opy_ = bstack1l11lll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢፎ")
    bstack1l1ll11l1ll_opy_ = bstack1l11lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤፏ")
    bstack1l1ll11llll_opy_ = bstack1l11lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣፐ")
    bstack1l1l11111l1_opy_ = bstack1l11lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨፑ")
    bstack1l1l1111111_opy_ = bstack1l11lll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧፒ")
    NAME = bstack1l11lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤፓ")
    bstack1l1l11111ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1llll1l_opy_: Any
    bstack1l1l111111l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11lll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨፔ"), bstack1l11lll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣፕ"), bstack1l11lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥፖ"), bstack1l11lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣፗ"), bstack1l11lll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧፘ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111l1l11_opy_(methods)
    def bstack11111lll1l_opy_(self, instance: bstack11111111ll_opy_, method_name: str, bstack1lllllll11l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllllll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11l1l_opy_, bstack1l11lllll1l_opy_ = bstack11111l11ll_opy_
        bstack1l11llll1ll_opy_ = bstack1lll111ll11_opy_.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        if bstack1l11llll1ll_opy_ in bstack1lll111ll11_opy_.bstack1l1l11111ll_opy_:
            bstack1l11llll1l1_opy_ = None
            for callback in bstack1lll111ll11_opy_.bstack1l1l11111ll_opy_[bstack1l11llll1ll_opy_]:
                try:
                    bstack1l11llllll1_opy_ = callback(self, target, exec, bstack11111l11ll_opy_, result, *args, **kwargs)
                    if bstack1l11llll1l1_opy_ == None:
                        bstack1l11llll1l1_opy_ = bstack1l11llllll1_opy_
                except Exception as e:
                    self.logger.error(bstack1l11lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤፙ") + str(e) + bstack1l11lll_opy_ (u"ࠧࠨፚ"))
                    traceback.print_exc()
            if bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.PRE and callable(bstack1l11llll1l1_opy_):
                return bstack1l11llll1l1_opy_
            elif bstack1l11lllll1l_opy_ == bstack111111l1l1_opy_.POST and bstack1l11llll1l1_opy_:
                return bstack1l11llll1l1_opy_
    def bstack11111l1l1l_opy_(
        self, method_name, previous_state: bstack111111lll1_opy_, *args, **kwargs
    ) -> bstack111111lll1_opy_:
        if method_name == bstack1l11lll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭፛") or method_name == bstack1l11lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨ፜") or method_name == bstack1l11lll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪ፝"):
            return bstack111111lll1_opy_.bstack111111l111_opy_
        if method_name == bstack1l11lll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫ፞"):
            return bstack111111lll1_opy_.bstack1llllllllll_opy_
        if method_name == bstack1l11lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩ፟"):
            return bstack111111lll1_opy_.QUIT
        return bstack111111lll1_opy_.NONE
    @staticmethod
    def bstack1l11lllllll_opy_(bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_]):
        return bstack1l11lll_opy_ (u"ࠦ࠿ࠨ፠").join((bstack111111lll1_opy_(bstack11111l11ll_opy_[0]).name, bstack111111l1l1_opy_(bstack11111l11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l1l_opy_(bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_], callback: Callable):
        bstack1l11llll1ll_opy_ = bstack1lll111ll11_opy_.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        if not bstack1l11llll1ll_opy_ in bstack1lll111ll11_opy_.bstack1l1l11111ll_opy_:
            bstack1lll111ll11_opy_.bstack1l1l11111ll_opy_[bstack1l11llll1ll_opy_] = []
        bstack1lll111ll11_opy_.bstack1l1l11111ll_opy_[bstack1l11llll1ll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l1ll11l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l11l111_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll111ll11_opy_.bstack1l1ll11llll_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(instance: bstack11111111ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack11111111ll_opy_, default_value=None):
        return bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll111ll11_opy_.bstack1l1ll11l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1ll11ll1_opy_(method_name: str, *args):
        if not bstack1lll111ll11_opy_.bstack1ll1l1ll1l1_opy_(method_name):
            return False
        if not bstack1lll111ll11_opy_.bstack1l1l11111l1_opy_ in bstack1lll111ll11_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1lll111ll11_opy_.bstack1ll11l1lll1_opy_(*args)
        return bstack1ll11ll1ll1_opy_ and bstack1l11lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፡") in bstack1ll11ll1ll1_opy_ and bstack1l11lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ።") in bstack1ll11ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፣")]
    @staticmethod
    def bstack1ll11lll1l1_opy_(method_name: str, *args):
        if not bstack1lll111ll11_opy_.bstack1ll1l1ll1l1_opy_(method_name):
            return False
        if not bstack1lll111ll11_opy_.bstack1l1l11111l1_opy_ in bstack1lll111ll11_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1lll111ll11_opy_.bstack1ll11l1lll1_opy_(*args)
        return (
            bstack1ll11ll1ll1_opy_
            and bstack1l11lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ፤") in bstack1ll11ll1ll1_opy_
            and bstack1l11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧ፥") in bstack1ll11ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፦")]
        )
    @staticmethod
    def bstack1l1l1l1l111_opy_(*args):
        return str(bstack1lll111ll11_opy_.bstack1ll1l111111_opy_(*args)).lower()