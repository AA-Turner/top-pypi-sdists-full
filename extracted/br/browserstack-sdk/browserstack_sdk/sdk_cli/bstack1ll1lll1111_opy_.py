# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1llllll1111_opy_,
    bstack1llll1ll111_opy_,
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1lll111_opy_(bstack1llllll1111_opy_):
    bstack1l11l11l11l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᐓ")
    bstack1l1l111l111_opy_ = bstack1ll11ll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᐔ")
    bstack1l1l11l1ll1_opy_ = bstack1ll11ll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᐕ")
    bstack1l1l11ll111_opy_ = bstack1ll11ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᐖ")
    bstack1l11l11l111_opy_ = bstack1ll11ll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᐗ")
    bstack1l11l111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᐘ")
    NAME = bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᐙ")
    bstack1l11l11ll11_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1111l1l_opy_: Any
    bstack1l11l1111ll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll11ll_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣᐚ"), bstack1ll11ll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᐛ"), bstack1ll11ll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᐜ"), bstack1ll11ll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᐝ"), bstack1ll11ll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢᐞ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll11l11_opy_(methods)
    def bstack1lllllll1ll_opy_(self, instance: bstack1llll1ll111_opy_, method_name: str, bstack1lllll11111_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll1ll11l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll111l1_opy_, bstack1l11l11l1l1_opy_ = bstack1llll1ll1l1_opy_
        bstack1l11l111l11_opy_ = bstack1lll1lll111_opy_.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        if bstack1l11l111l11_opy_ in bstack1lll1lll111_opy_.bstack1l11l11ll11_opy_:
            bstack1l11l111lll_opy_ = None
            for callback in bstack1lll1lll111_opy_.bstack1l11l11ll11_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11l1ll_opy_ = callback(self, target, exec, bstack1llll1ll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11l111lll_opy_ == None:
                        bstack1l11l111lll_opy_ = bstack1l11l11l1ll_opy_
                except Exception as e:
                    self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᐟ") + str(e) + bstack1ll11ll_opy_ (u"ࠢࠣᐠ"))
                    traceback.print_exc()
            if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.PRE and callable(bstack1l11l111lll_opy_):
                return bstack1l11l111lll_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST and bstack1l11l111lll_opy_:
                return bstack1l11l111lll_opy_
    def bstack1lllll11ll1_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1ll11ll_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࠨᐡ") or method_name == bstack1ll11ll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪᐢ") or method_name == bstack1ll11ll_opy_ (u"ࠪࡲࡪࡽ࡟ࡱࡣࡪࡩࠬᐣ"):
            return bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_
        if method_name == bstack1ll11ll_opy_ (u"ࠫࡩ࡯ࡳࡱࡣࡷࡧ࡭࠭ᐤ"):
            return bstack1lllll1l111_opy_.bstack1lllll1ll11_opy_
        if method_name == bstack1ll11ll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫᐥ"):
            return bstack1lllll1l111_opy_.QUIT
        return bstack1lllll1l111_opy_.NONE
    @staticmethod
    def bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_]):
        return bstack1ll11ll_opy_ (u"ࠨ࠺ࠣᐦ").join((bstack1lllll1l111_opy_(bstack1llll1ll1l1_opy_[0]).name, bstack1lllll111ll_opy_(bstack1llll1ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1lll1lll111_opy_.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        if not bstack1l11l111l11_opy_ in bstack1lll1lll111_opy_.bstack1l11l11ll11_opy_:
            bstack1lll1lll111_opy_.bstack1l11l11ll11_opy_[bstack1l11l111l11_opy_] = []
        bstack1lll1lll111_opy_.bstack1l11l11ll11_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll111lll11_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll11ll_opy_(instance: bstack1llll1ll111_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l11ll111_opy_, default_value)
    @staticmethod
    def bstack1l1llll11ll_opy_(instance: bstack1llll1ll111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11ll1111_opy_(instance: bstack1llll1ll111_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1lll1lll111_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll111ll1l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str, *args):
        if not bstack1lll1lll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
            return False
        if not bstack1lll1lll111_opy_.bstack1l11l11l111_opy_ in bstack1lll1lll111_opy_.bstack1l11ll111ll_opy_(*args):
            return False
        bstack1ll11111lll_opy_ = bstack1lll1lll111_opy_.bstack1ll11111l11_opy_(*args)
        return bstack1ll11111lll_opy_ and bstack1ll11ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᐧ") in bstack1ll11111lll_opy_ and bstack1ll11ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᐨ") in bstack1ll11111lll_opy_[bstack1ll11ll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐩ")]
    @staticmethod
    def bstack1ll1111l1ll_opy_(method_name: str, *args):
        if not bstack1lll1lll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
            return False
        if not bstack1lll1lll111_opy_.bstack1l11l11l111_opy_ in bstack1lll1lll111_opy_.bstack1l11ll111ll_opy_(*args):
            return False
        bstack1ll11111lll_opy_ = bstack1lll1lll111_opy_.bstack1ll11111l11_opy_(*args)
        return (
            bstack1ll11111lll_opy_
            and bstack1ll11ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᐪ") in bstack1ll11111lll_opy_
            and bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᐫ") in bstack1ll11111lll_opy_[bstack1ll11ll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐬ")]
        )
    @staticmethod
    def bstack1l11ll111ll_opy_(*args):
        return str(bstack1lll1lll111_opy_.bstack1ll111ll1l1_opy_(*args)).lower()