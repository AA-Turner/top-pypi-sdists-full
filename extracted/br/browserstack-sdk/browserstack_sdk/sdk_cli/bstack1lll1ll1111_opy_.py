# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import (
    bstack111111ll11_opy_,
    bstack11111ll111_opy_,
    bstack1llllllllll_opy_,
    bstack11111lll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll11l111_opy_(bstack111111ll11_opy_):
    bstack1l1l1111111_opy_ = bstack1l1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨፔ")
    bstack1l1ll11ll1l_opy_ = bstack1l1lll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢፕ")
    bstack1l1ll11l111_opy_ = bstack1l1lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤፖ")
    bstack1l1ll11ll11_opy_ = bstack1l1lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣፗ")
    bstack1l11llll1l1_opy_ = bstack1l1lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨፘ")
    bstack1l11llllll1_opy_ = bstack1l1lll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧፙ")
    NAME = bstack1l1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤፚ")
    bstack1l1l11111l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll111l11_opy_: Any
    bstack1l1l11111ll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1lll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ፛"), bstack1l1lll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ፜"), bstack1l1lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥ፝"), bstack1l1lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ፞"), bstack1l1lll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧ፟")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111ll1ll_opy_(methods)
    def bstack11111lll11_opy_(self, instance: bstack11111ll111_opy_, method_name: str, bstack1lllllll1ll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack111111l1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111llll1_opy_, bstack1l11lllll11_opy_ = bstack1lllllll1l1_opy_
        bstack1l11lllll1l_opy_ = bstack1llll11l111_opy_.bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_)
        if bstack1l11lllll1l_opy_ in bstack1llll11l111_opy_.bstack1l1l11111l1_opy_:
            bstack1l11lllllll_opy_ = None
            for callback in bstack1llll11l111_opy_.bstack1l1l11111l1_opy_[bstack1l11lllll1l_opy_]:
                try:
                    bstack1l1l111111l_opy_ = callback(self, target, exec, bstack1lllllll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11lllllll_opy_ == None:
                        bstack1l11lllllll_opy_ = bstack1l1l111111l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤ፠") + str(e) + bstack1l1lll_opy_ (u"ࠧࠨ፡"))
                    traceback.print_exc()
            if bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.PRE and callable(bstack1l11lllllll_opy_):
                return bstack1l11lllllll_opy_
            elif bstack1l11lllll11_opy_ == bstack11111lll1l_opy_.POST and bstack1l11lllllll_opy_:
                return bstack1l11lllllll_opy_
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        if method_name == bstack1l1lll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭።") or method_name == bstack1l1lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨ፣") or method_name == bstack1l1lll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪ፤"):
            return bstack1llllllllll_opy_.bstack1111l11lll_opy_
        if method_name == bstack1l1lll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫ፥"):
            return bstack1llllllllll_opy_.bstack11111111l1_opy_
        if method_name == bstack1l1lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩ፦"):
            return bstack1llllllllll_opy_.QUIT
        return bstack1llllllllll_opy_.NONE
    @staticmethod
    def bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_]):
        return bstack1l1lll_opy_ (u"ࠦ࠿ࠨ፧").join((bstack1llllllllll_opy_(bstack1lllllll1l1_opy_[0]).name, bstack11111lll1l_opy_(bstack1lllllll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1l111_opy_(bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_], callback: Callable):
        bstack1l11lllll1l_opy_ = bstack1llll11l111_opy_.bstack1l11llll1ll_opy_(bstack1lllllll1l1_opy_)
        if not bstack1l11lllll1l_opy_ in bstack1llll11l111_opy_.bstack1l1l11111l1_opy_:
            bstack1llll11l111_opy_.bstack1l1l11111l1_opy_[bstack1l11lllll1l_opy_] = []
        bstack1llll11l111_opy_.bstack1l1l11111l1_opy_[bstack1l11lllll1l_opy_].append(callback)
    @staticmethod
    def bstack1ll1ll11111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1lll1l_opy_(instance: bstack11111ll111_opy_, default_value=None):
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, bstack1llll11l111_opy_.bstack1l1ll11ll11_opy_, default_value)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack11111ll111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1llll1_opy_(instance: bstack11111ll111_opy_, default_value=None):
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, bstack1llll11l111_opy_.bstack1l1ll11l111_opy_, default_value)
    @staticmethod
    def bstack1ll1l111lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1llll11l111_opy_.bstack1ll1ll11111_opy_(method_name):
            return False
        if not bstack1llll11l111_opy_.bstack1l11llll1l1_opy_ in bstack1llll11l111_opy_.bstack1l1l11l11l1_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1llll11l111_opy_.bstack1ll11ll1ll1_opy_(*args)
        return bstack1ll11l1lll1_opy_ and bstack1l1lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፨") in bstack1ll11l1lll1_opy_ and bstack1l1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፩") in bstack1ll11l1lll1_opy_[bstack1l1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፪")]
    @staticmethod
    def bstack1ll1l11l1l1_opy_(method_name: str, *args):
        if not bstack1llll11l111_opy_.bstack1ll1ll11111_opy_(method_name):
            return False
        if not bstack1llll11l111_opy_.bstack1l11llll1l1_opy_ in bstack1llll11l111_opy_.bstack1l1l11l11l1_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1llll11l111_opy_.bstack1ll11ll1ll1_opy_(*args)
        return (
            bstack1ll11l1lll1_opy_
            and bstack1l1lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ፫") in bstack1ll11l1lll1_opy_
            and bstack1l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧ፬") in bstack1ll11l1lll1_opy_[bstack1l1lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፭")]
        )
    @staticmethod
    def bstack1l1l11l11l1_opy_(*args):
        return str(bstack1llll11l111_opy_.bstack1ll1l111lll_opy_(*args)).lower()