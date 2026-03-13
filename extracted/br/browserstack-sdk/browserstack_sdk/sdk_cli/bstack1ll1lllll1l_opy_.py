# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1llll111_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1llllll1_opy_(bstack1ll1llll111_opy_):
    bstack11ll11llll1_opy_ = bstack1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᜯ")
    bstack1ll1llll1l1_opy_ = bstack1111l_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᜰ")
    bstack1lll1111ll1_opy_ = bstack1111l_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᜱ")
    bstack1ll1lll1lll_opy_ = bstack1111l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᜲ")
    bstack11ll1l11l11_opy_ = bstack1111l_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᜳ")
    bstack11ll1l111l1_opy_ = bstack1111l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧ᜴ࠧ")
    NAME = bstack1111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᜵")
    bstack11ll1l111ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1ll111l11_opy_: Any
    bstack11ll11lll11_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1111l_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ᜶"), bstack1111l_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ᜷"), bstack1111l_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥ᜸"), bstack1111l_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ᜹"), bstack1111l_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧ᜺")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1ll11111_opy_(methods)
    def bstack1ll11llll11_opy_(self, instance: bstack1ll1l1lll1l_opy_, method_name: str, bstack1ll1l11111l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1l111111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1ll111l1_opy_, bstack11ll1l1111l_opy_ = bstack1ll1l111l11_opy_
        bstack11ll11lllll_opy_ = bstack1ll1llllll1_opy_.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        if bstack11ll11lllll_opy_ in bstack1ll1llllll1_opy_.bstack11ll1l111ll_opy_:
            bstack11ll11lll1l_opy_ = None
            for callback in bstack1ll1llllll1_opy_.bstack11ll1l111ll_opy_[bstack11ll11lllll_opy_]:
                try:
                    bstack11ll1l11111_opy_ = callback(self, target, exec, bstack1ll1l111l11_opy_, result, *args, **kwargs)
                    if bstack11ll11lll1l_opy_ == None:
                        bstack11ll11lll1l_opy_ = bstack11ll1l11111_opy_
                except Exception as e:
                    self.logger.error(bstack1111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤ᜻") + str(e) + bstack1111l_opy_ (u"ࠧࠨ᜼"))
                    traceback.print_exc()
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.PRE and callable(bstack11ll11lll1l_opy_):
                return bstack11ll11lll1l_opy_
            elif bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST and bstack11ll11lll1l_opy_:
                return bstack11ll11lll1l_opy_
    def bstack1ll1l11l1l1_opy_(
        self, method_name, previous_state: bstack1ll1l1l1lll_opy_, *args, **kwargs
    ) -> bstack1ll1l1l1lll_opy_:
        if method_name == bstack1111l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭᜽") or method_name == bstack1111l_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨ᜾") or method_name == bstack1111l_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪ᜿"):
            return bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_
        if method_name == bstack1111l_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫᝀ"):
            return bstack1ll1l1l1lll_opy_.bstack1ll1l11lll1_opy_
        if method_name == bstack1111l_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᝁ"):
            return bstack1ll1l1l1lll_opy_.QUIT
        return bstack1ll1l1l1lll_opy_.NONE
    @staticmethod
    def bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_]):
        return bstack1111l_opy_ (u"ࠦ࠿ࠨᝂ").join((bstack1ll1l1l1lll_opy_(bstack1ll1l111l11_opy_[0]).name, bstack1ll1ll1111l_opy_(bstack1ll1l111l11_opy_[1]).name))
    @staticmethod
    def bstack1l1l11llll1_opy_(bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_], callback: Callable):
        bstack11ll11lllll_opy_ = bstack1ll1llllll1_opy_.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        if not bstack11ll11lllll_opy_ in bstack1ll1llllll1_opy_.bstack11ll1l111ll_opy_:
            bstack1ll1llllll1_opy_.bstack11ll1l111ll_opy_[bstack11ll11lllll_opy_] = []
        bstack1ll1llllll1_opy_.bstack11ll1l111ll_opy_[bstack11ll11lllll_opy_].append(callback)
    @staticmethod
    def bstack1l1l1111111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l11l11ll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1l1ll1111_opy_(instance: bstack1ll1l1lll1l_opy_, default_value=None):
        return bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1lll1lll_opy_, default_value)
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1ll1l1lll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l11lll11_opy_(instance: bstack1ll1l1lll1l_opy_, default_value=None):
        return bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_, default_value)
    @staticmethod
    def bstack1l11llll1ll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11lll1l1l_opy_(method_name: str, *args):
        if not bstack1ll1llllll1_opy_.bstack1l1l1111111_opy_(method_name):
            return False
        if not bstack1ll1llllll1_opy_.bstack11ll1l11l11_opy_ in bstack1ll1llllll1_opy_.bstack11lll1l1lll_opy_(*args):
            return False
        bstack1l11ll11l1l_opy_ = bstack1ll1llllll1_opy_.bstack1l11ll11lll_opy_(*args)
        return bstack1l11ll11l1l_opy_ and bstack1111l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᝃ") in bstack1l11ll11l1l_opy_ and bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᝄ") in bstack1l11ll11l1l_opy_[bstack1111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᝅ")]
    @staticmethod
    def bstack1l1l1l11l1l_opy_(method_name: str, *args):
        if not bstack1ll1llllll1_opy_.bstack1l1l1111111_opy_(method_name):
            return False
        if not bstack1ll1llllll1_opy_.bstack11ll1l11l11_opy_ in bstack1ll1llllll1_opy_.bstack11lll1l1lll_opy_(*args):
            return False
        bstack1l11ll11l1l_opy_ = bstack1ll1llllll1_opy_.bstack1l11ll11lll_opy_(*args)
        return (
            bstack1l11ll11l1l_opy_
            and bstack1111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᝆ") in bstack1l11ll11l1l_opy_
            and bstack1111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᝇ") in bstack1l11ll11l1l_opy_[bstack1111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᝈ")]
        )
    @staticmethod
    def bstack11lll1l1lll_opy_(*args):
        return str(bstack1ll1llllll1_opy_.bstack1l11llll1ll_opy_(*args)).lower()