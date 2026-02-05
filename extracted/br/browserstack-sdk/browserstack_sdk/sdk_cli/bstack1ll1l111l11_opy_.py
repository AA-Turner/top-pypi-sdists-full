# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111llll_opy_,
    bstack1lll11lll1l_opy_,
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll111ll1l1_opy_(bstack1lll111llll_opy_):
    bstack11llllll111_opy_ = bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᔘ")
    bstack1l111lll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᔙ")
    bstack1l111llll11_opy_ = bstack11l1ll1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᔚ")
    bstack1l11l111lll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔛ")
    bstack11lllll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᔜ")
    bstack11lllllll11_opy_ = bstack11l1ll1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᔝ")
    NAME = bstack11l1ll1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᔞ")
    bstack11lllll1l1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1lll1l1l_opy_: Any
    bstack11lllll1ll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11l1ll1_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᔟ"), bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᔠ"), bstack11l1ll1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᔡ"), bstack11l1ll1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᔢ"), bstack11l1ll1_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᔣ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll11l1l11_opy_(methods)
    def bstack1lll1lll1l1_opy_(self, instance: bstack1lll11lll1l_opy_, method_name: str, bstack1lll111ll1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lll11llll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll1ll1111_opy_, bstack11llllll1l1_opy_ = bstack1lll1l1ll11_opy_
        bstack11lllll1lll_opy_ = bstack1ll111ll1l1_opy_.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        if bstack11lllll1lll_opy_ in bstack1ll111ll1l1_opy_.bstack11lllll1l1l_opy_:
            bstack11llllll11l_opy_ = None
            for callback in bstack1ll111ll1l1_opy_.bstack11lllll1l1l_opy_[bstack11lllll1lll_opy_]:
                try:
                    bstack11lllllll1l_opy_ = callback(self, target, exec, bstack1lll1l1ll11_opy_, result, *args, **kwargs)
                    if bstack11llllll11l_opy_ == None:
                        bstack11llllll11l_opy_ = bstack11lllllll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᔤ") + str(e) + bstack11l1ll1_opy_ (u"ࠤࠥᔥ"))
                    traceback.print_exc()
            if bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.PRE and callable(bstack11llllll11l_opy_):
                return bstack11llllll11l_opy_
            elif bstack11llllll1l1_opy_ == bstack1lll1ll1l11_opy_.POST and bstack11llllll11l_opy_:
                return bstack11llllll11l_opy_
    def bstack1lll1ll1ll1_opy_(
        self, method_name, previous_state: bstack1lll111lll1_opy_, *args, **kwargs
    ) -> bstack1lll111lll1_opy_:
        if method_name == bstack11l1ll1_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᔦ") or method_name == bstack11l1ll1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᔧ") or method_name == bstack11l1ll1_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᔨ"):
            return bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_
        if method_name == bstack11l1ll1_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨᔩ"):
            return bstack1lll111lll1_opy_.bstack1lll1l11l11_opy_
        if method_name == bstack11l1ll1_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ᔪ"):
            return bstack1lll111lll1_opy_.QUIT
        return bstack1lll111lll1_opy_.NONE
    @staticmethod
    def bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_]):
        return bstack11l1ll1_opy_ (u"ࠣ࠼ࠥᔫ").join((bstack1lll111lll1_opy_(bstack1lll1l1ll11_opy_[0]).name, bstack1lll1ll1l11_opy_(bstack1lll1l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l1ll11llll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_], callback: Callable):
        bstack11lllll1lll_opy_ = bstack1ll111ll1l1_opy_.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        if not bstack11lllll1lll_opy_ in bstack1ll111ll1l1_opy_.bstack11lllll1l1l_opy_:
            bstack1ll111ll1l1_opy_.bstack11lllll1l1l_opy_[bstack11lllll1lll_opy_] = []
        bstack1ll111ll1l1_opy_.bstack11lllll1l1l_opy_[bstack11lllll1lll_opy_].append(callback)
    @staticmethod
    def bstack1l1ll111111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1ll11l1l1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1llll111l_opy_(instance: bstack1lll11lll1l_opy_, default_value=None):
        return bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll111ll1l1_opy_.bstack1l11l111lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1l11ll1_opy_(instance: bstack1lll11lll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l1llllll_opy_(instance: bstack1lll11lll1l_opy_, default_value=None):
        return bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll111ll1l1_opy_.bstack1l111llll11_opy_, default_value)
    @staticmethod
    def bstack1l1llll11l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(method_name: str, *args):
        if not bstack1ll111ll1l1_opy_.bstack1l1ll111111_opy_(method_name):
            return False
        if not bstack1ll111ll1l1_opy_.bstack11lllll1l11_opy_ in bstack1ll111ll1l1_opy_.bstack1l1111ll111_opy_(*args):
            return False
        bstack1l1l1l1llll_opy_ = bstack1ll111ll1l1_opy_.bstack1l1l1lll111_opy_(*args)
        return bstack1l1l1l1llll_opy_ and bstack11l1ll1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᔬ") in bstack1l1l1l1llll_opy_ and bstack11l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔭ") in bstack1l1l1l1llll_opy_[bstack11l1ll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᔮ")]
    @staticmethod
    def bstack1l1ll11111l_opy_(method_name: str, *args):
        if not bstack1ll111ll1l1_opy_.bstack1l1ll111111_opy_(method_name):
            return False
        if not bstack1ll111ll1l1_opy_.bstack11lllll1l11_opy_ in bstack1ll111ll1l1_opy_.bstack1l1111ll111_opy_(*args):
            return False
        bstack1l1l1l1llll_opy_ = bstack1ll111ll1l1_opy_.bstack1l1l1lll111_opy_(*args)
        return (
            bstack1l1l1l1llll_opy_
            and bstack11l1ll1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᔯ") in bstack1l1l1l1llll_opy_
            and bstack11l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᔰ") in bstack1l1l1l1llll_opy_[bstack11l1ll1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᔱ")]
        )
    @staticmethod
    def bstack1l1111ll111_opy_(*args):
        return str(bstack1ll111ll1l1_opy_.bstack1l1llll11l1_opy_(*args)).lower()