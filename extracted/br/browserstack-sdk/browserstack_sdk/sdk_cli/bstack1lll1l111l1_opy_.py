# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1lll11l_opy_(bstack1lll1ll1ll1_opy_):
    bstack11llll1llll_opy_ = bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᔸ")
    bstack1l111llll11_opy_ = bstack11lllll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᔹ")
    bstack1l111lll111_opy_ = bstack11lllll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᔺ")
    bstack1l11l1111ll_opy_ = bstack11lllll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᔻ")
    bstack11lllll1l11_opy_ = bstack11lllll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᔼ")
    bstack11lllll1l1l_opy_ = bstack11lllll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᔽ")
    NAME = bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᔾ")
    bstack11lllll1ll1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l11l1l1_opy_: Any
    bstack11llll1lll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11lllll_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢᔿ"), bstack11lllll_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᕀ"), bstack11lllll_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᕁ"), bstack11lllll_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᕂ"), bstack11lllll_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᕃ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lll1111lll_opy_(methods)
    def bstack1lll111l1l1_opy_(self, instance: bstack1lll1l1l11l_opy_, method_name: str, bstack1ll1lll1lll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lll111llll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll11l1l1l_opy_, bstack11lllll1111_opy_ = bstack1lll1l11lll_opy_
        bstack11lllll11l1_opy_ = bstack1lll1lll11l_opy_.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        if bstack11lllll11l1_opy_ in bstack1lll1lll11l_opy_.bstack11lllll1ll1_opy_:
            bstack11lllll11ll_opy_ = None
            for callback in bstack1lll1lll11l_opy_.bstack11lllll1ll1_opy_[bstack11lllll11l1_opy_]:
                try:
                    bstack11llll1ll1l_opy_ = callback(self, target, exec, bstack1lll1l11lll_opy_, result, *args, **kwargs)
                    if bstack11lllll11ll_opy_ == None:
                        bstack11lllll11ll_opy_ = bstack11llll1ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᕄ") + str(e) + bstack11lllll_opy_ (u"ࠨࠢᕅ"))
                    traceback.print_exc()
            if bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.PRE and callable(bstack11lllll11ll_opy_):
                return bstack11lllll11ll_opy_
            elif bstack11lllll1111_opy_ == bstack1lll1ll11ll_opy_.POST and bstack11lllll11ll_opy_:
                return bstack11lllll11ll_opy_
    def bstack1ll1llll1ll_opy_(
        self, method_name, previous_state: bstack1lll1l1ll1l_opy_, *args, **kwargs
    ) -> bstack1lll1l1ll1l_opy_:
        if method_name == bstack11lllll_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧᕆ") or method_name == bstack11lllll_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᕇ") or method_name == bstack11lllll_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫᕈ"):
            return bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_
        if method_name == bstack11lllll_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬᕉ"):
            return bstack1lll1l1ll1l_opy_.bstack1ll1llllll1_opy_
        if method_name == bstack11lllll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪᕊ"):
            return bstack1lll1l1ll1l_opy_.QUIT
        return bstack1lll1l1ll1l_opy_.NONE
    @staticmethod
    def bstack11lllll111l_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_]):
        return bstack11lllll_opy_ (u"ࠧࡀࠢᕋ").join((bstack1lll1l1ll1l_opy_(bstack1lll1l11lll_opy_[0]).name, bstack1lll1ll11ll_opy_(bstack1lll1l11lll_opy_[1]).name))
    @staticmethod
    def bstack1lll1l1l1ll_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_], callback: Callable):
        bstack11lllll11l1_opy_ = bstack1lll1lll11l_opy_.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        if not bstack11lllll11l1_opy_ in bstack1lll1lll11l_opy_.bstack11lllll1ll1_opy_:
            bstack1lll1lll11l_opy_.bstack11lllll1ll1_opy_[bstack11lllll11l1_opy_] = []
        bstack1lll1lll11l_opy_.bstack11lllll1ll1_opy_[bstack11lllll11l1_opy_].append(callback)
    @staticmethod
    def bstack1l1ll11ll1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1lll1l11l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l1lll1ll1l_opy_(instance: bstack1lll1l1l11l_opy_, default_value=None):
        return bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1lll1lll11l_opy_.bstack1l11l1111ll_opy_, default_value)
    @staticmethod
    def bstack1lll1l1llll_opy_(instance: bstack1lll1l1l11l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1ll11llll_opy_(instance: bstack1lll1l1l11l_opy_, default_value=None):
        return bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111lll111_opy_, default_value)
    @staticmethod
    def bstack1l1l1lll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(method_name: str, *args):
        if not bstack1lll1lll11l_opy_.bstack1l1ll11ll1l_opy_(method_name):
            return False
        if not bstack1lll1lll11l_opy_.bstack11lllll1l11_opy_ in bstack1lll1lll11l_opy_.bstack1l111111l1l_opy_(*args):
            return False
        bstack1l1l1l11lll_opy_ = bstack1lll1lll11l_opy_.bstack1l1l1l11l11_opy_(*args)
        return bstack1l1l1l11lll_opy_ and bstack11lllll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᕌ") in bstack1l1l1l11lll_opy_ and bstack11lllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᕍ") in bstack1l1l1l11lll_opy_[bstack11lllll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᕎ")]
    @staticmethod
    def bstack1l1l1ll1l1l_opy_(method_name: str, *args):
        if not bstack1lll1lll11l_opy_.bstack1l1ll11ll1l_opy_(method_name):
            return False
        if not bstack1lll1lll11l_opy_.bstack11lllll1l11_opy_ in bstack1lll1lll11l_opy_.bstack1l111111l1l_opy_(*args):
            return False
        bstack1l1l1l11lll_opy_ = bstack1lll1lll11l_opy_.bstack1l1l1l11l11_opy_(*args)
        return (
            bstack1l1l1l11lll_opy_
            and bstack11lllll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᕏ") in bstack1l1l1l11lll_opy_
            and bstack11lllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᕐ") in bstack1l1l1l11lll_opy_[bstack11lllll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᕑ")]
        )
    @staticmethod
    def bstack1l111111l1l_opy_(*args):
        return str(bstack1lll1lll11l_opy_.bstack1l1l1lll11l_opy_(*args)).lower()