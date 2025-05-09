# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import (
    bstack11111l1ll1_opy_,
    bstack111111l1ll_opy_,
    bstack1lllllll1l1_opy_,
    bstack1llllllll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1lll111_opy_(bstack11111l1ll1_opy_):
    bstack1l1l111111l_opy_ = bstack11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨፔ")
    bstack1l1l1llll11_opy_ = bstack11lll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢፕ")
    bstack1l1ll11l1l1_opy_ = bstack11lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤፖ")
    bstack1l1l1llllll_opy_ = bstack11lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣፗ")
    bstack1l11lllll11_opy_ = bstack11lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨፘ")
    bstack1l11llll1ll_opy_ = bstack11lll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧፙ")
    NAME = bstack11lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤፚ")
    bstack1l11llllll1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll11ll111_opy_: Any
    bstack1l11llll111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11lll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ፛"), bstack11lll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ፜"), bstack11lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥ፝"), bstack11lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ፞"), bstack11lll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧ፟")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111lll11_opy_(methods)
    def bstack111111lll1_opy_(self, instance: bstack111111l1ll_opy_, method_name: str, bstack11111l1l11_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11111_opy_, bstack1l11lllll1l_opy_ = bstack1111111ll1_opy_
        bstack1l11llll1l1_opy_ = bstack1lll1lll111_opy_.bstack1l11llll11l_opy_(bstack1111111ll1_opy_)
        if bstack1l11llll1l1_opy_ in bstack1lll1lll111_opy_.bstack1l11llllll1_opy_:
            bstack1l11lllllll_opy_ = None
            for callback in bstack1lll1lll111_opy_.bstack1l11llllll1_opy_[bstack1l11llll1l1_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1111111ll1_opy_, result, *args, **kwargs)
                    if bstack1l11lllllll_opy_ == None:
                        bstack1l11lllllll_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack11lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤ፠") + str(e) + bstack11lll_opy_ (u"ࠧࠨ፡"))
                    traceback.print_exc()
            if bstack1l11lllll1l_opy_ == bstack1llllllll1l_opy_.PRE and callable(bstack1l11lllllll_opy_):
                return bstack1l11lllllll_opy_
            elif bstack1l11lllll1l_opy_ == bstack1llllllll1l_opy_.POST and bstack1l11lllllll_opy_:
                return bstack1l11lllllll_opy_
    def bstack11111ll1ll_opy_(
        self, method_name, previous_state: bstack1lllllll1l1_opy_, *args, **kwargs
    ) -> bstack1lllllll1l1_opy_:
        if method_name == bstack11lll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭።") or method_name == bstack11lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨ፣") or method_name == bstack11lll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪ፤"):
            return bstack1lllllll1l1_opy_.bstack11111ll11l_opy_
        if method_name == bstack11lll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫ፥"):
            return bstack1lllllll1l1_opy_.bstack11111111ll_opy_
        if method_name == bstack11lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩ፦"):
            return bstack1lllllll1l1_opy_.QUIT
        return bstack1lllllll1l1_opy_.NONE
    @staticmethod
    def bstack1l11llll11l_opy_(bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_]):
        return bstack11lll_opy_ (u"ࠦ࠿ࠨ፧").join((bstack1lllllll1l1_opy_(bstack1111111ll1_opy_[0]).name, bstack1llllllll1l_opy_(bstack1111111ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_], callback: Callable):
        bstack1l11llll1l1_opy_ = bstack1lll1lll111_opy_.bstack1l11llll11l_opy_(bstack1111111ll1_opy_)
        if not bstack1l11llll1l1_opy_ in bstack1lll1lll111_opy_.bstack1l11llllll1_opy_:
            bstack1lll1lll111_opy_.bstack1l11llllll1_opy_[bstack1l11llll1l1_opy_] = []
        bstack1lll1lll111_opy_.bstack1l11llllll1_opy_[bstack1l11llll1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l11ll1l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1l11ll_opy_(instance: bstack111111l1ll_opy_, default_value=None):
        return bstack11111l1ll1_opy_.bstack111111l1l1_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l1llllll_opy_, default_value)
    @staticmethod
    def bstack1ll1l1llll1_opy_(instance: bstack111111l1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1l1lll_opy_(instance: bstack111111l1ll_opy_, default_value=None):
        return bstack11111l1ll1_opy_.bstack111111l1l1_opy_(instance, bstack1lll1lll111_opy_.bstack1l1ll11l1l1_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111ll1_opy_(method_name: str, *args):
        if not bstack1lll1lll111_opy_.bstack1ll1l1l1ll1_opy_(method_name):
            return False
        if not bstack1lll1lll111_opy_.bstack1l11lllll11_opy_ in bstack1lll1lll111_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11l1ll11_opy_ = bstack1lll1lll111_opy_.bstack1ll11ll1111_opy_(*args)
        return bstack1ll11l1ll11_opy_ and bstack11lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፨") in bstack1ll11l1ll11_opy_ and bstack11lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፩") in bstack1ll11l1ll11_opy_[bstack11lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፪")]
    @staticmethod
    def bstack1ll11lll111_opy_(method_name: str, *args):
        if not bstack1lll1lll111_opy_.bstack1ll1l1l1ll1_opy_(method_name):
            return False
        if not bstack1lll1lll111_opy_.bstack1l11lllll11_opy_ in bstack1lll1lll111_opy_.bstack1l1l11l1l1l_opy_(*args):
            return False
        bstack1ll11l1ll11_opy_ = bstack1lll1lll111_opy_.bstack1ll11ll1111_opy_(*args)
        return (
            bstack1ll11l1ll11_opy_
            and bstack11lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ፫") in bstack1ll11l1ll11_opy_
            and bstack11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧ፬") in bstack1ll11l1ll11_opy_[bstack11lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፭")]
        )
    @staticmethod
    def bstack1l1l11l1l1l_opy_(*args):
        return str(bstack1lll1lll111_opy_.bstack1ll1l1l1l11_opy_(*args)).lower()