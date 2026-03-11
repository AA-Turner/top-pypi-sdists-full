# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1l111l_opy_,
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll111l1l1_opy_(bstack1ll1lllllll_opy_):
    bstack11ll1l111l1_opy_ = bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ᛬")
    bstack1ll1lll111l_opy_ = bstack1ll111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥ᛭")
    bstack1lll111l1ll_opy_ = bstack1ll111_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᛮ")
    bstack1ll1lll1l1l_opy_ = bstack1ll111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᛯ")
    bstack11ll1l11lll_opy_ = bstack1ll111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᛰ")
    bstack11ll1l111ll_opy_ = bstack1ll111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᛱ")
    NAME = bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᛲ")
    bstack11ll1l11ll1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llllll1l_opy_: Any
    bstack11ll1l11111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll111_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᛳ"), bstack1ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᛴ"), bstack1ll111_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᛵ"), bstack1ll111_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᛶ"), bstack1ll111_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣᛷ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll1ll11l11_opy_(methods)
    def bstack1ll1l1l1l11_opy_(self, instance: bstack1ll1l1l111l_opy_, method_name: str, bstack1ll11llllll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1l11ll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1l1ll11l_opy_, bstack11ll11lllll_opy_ = bstack1ll1l1l1l1l_opy_
        bstack11ll1l1111l_opy_ = bstack1lll111l1l1_opy_.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        if bstack11ll1l1111l_opy_ in bstack1lll111l1l1_opy_.bstack11ll1l11ll1_opy_:
            bstack11ll1l1l111_opy_ = None
            for callback in bstack1lll111l1l1_opy_.bstack11ll1l11ll1_opy_[bstack11ll1l1111l_opy_]:
                try:
                    bstack11ll1l11l1l_opy_ = callback(self, target, exec, bstack1ll1l1l1l1l_opy_, result, *args, **kwargs)
                    if bstack11ll1l1l111_opy_ == None:
                        bstack11ll1l1l111_opy_ = bstack11ll1l11l1l_opy_
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᛸ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤ᛹"))
                    traceback.print_exc()
            if bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.PRE and callable(bstack11ll1l1l111_opy_):
                return bstack11ll1l1l111_opy_
            elif bstack11ll11lllll_opy_ == bstack1ll1l11ll1l_opy_.POST and bstack11ll1l1l111_opy_:
                return bstack11ll1l1l111_opy_
    def bstack1ll11lllll1_opy_(
        self, method_name, previous_state: bstack1ll1l1l11l1_opy_, *args, **kwargs
    ) -> bstack1ll1l1l11l1_opy_:
        if method_name == bstack1ll111_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩ᛺") or method_name == bstack1ll111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫ᛻") or method_name == bstack1ll111_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭᛼"):
            return bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_
        if method_name == bstack1ll111_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧ᛽"):
            return bstack1ll1l1l11l1_opy_.bstack1ll1ll111l1_opy_
        if method_name == bstack1ll111_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬ᛾"):
            return bstack1ll1l1l11l1_opy_.QUIT
        return bstack1ll1l1l11l1_opy_.NONE
    @staticmethod
    def bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_]):
        return bstack1ll111_opy_ (u"ࠢ࠻ࠤ᛿").join((bstack1ll1l1l11l1_opy_(bstack1ll1l1l1l1l_opy_[0]).name, bstack1ll1l11ll1l_opy_(bstack1ll1l1l1l1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1111111_opy_(bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_], callback: Callable):
        bstack11ll1l1111l_opy_ = bstack1lll111l1l1_opy_.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        if not bstack11ll1l1111l_opy_ in bstack1lll111l1l1_opy_.bstack11ll1l11ll1_opy_:
            bstack1lll111l1l1_opy_.bstack11ll1l11ll1_opy_[bstack11ll1l1111l_opy_] = []
        bstack1lll111l1l1_opy_.bstack11ll1l11ll1_opy_[bstack11ll1l1111l_opy_].append(callback)
    @staticmethod
    def bstack1l1l111111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l11l1ll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1l11lllll1l_opy_(instance: bstack1ll1l1l111l_opy_, default_value=None):
        return bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll1l1l_opy_, default_value)
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1ll1l1l111l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l111ll1l_opy_(instance: bstack1ll1l1l111l_opy_, default_value=None):
        return bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_, default_value)
    @staticmethod
    def bstack1l1l11l1l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1l1111l_opy_(method_name: str, *args):
        if not bstack1lll111l1l1_opy_.bstack1l1l111111l_opy_(method_name):
            return False
        if not bstack1lll111l1l1_opy_.bstack11ll1l11lll_opy_ in bstack1lll111l1l1_opy_.bstack11lll11llll_opy_(*args):
            return False
        bstack1l11ll1l1ll_opy_ = bstack1lll111l1l1_opy_.bstack1l11ll1l11l_opy_(*args)
        return bstack1l11ll1l1ll_opy_ and bstack1ll111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᜀ") in bstack1l11ll1l1ll_opy_ and bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᜁ") in bstack1l11ll1l1ll_opy_[bstack1ll111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᜂ")]
    @staticmethod
    def bstack1l1l11l11l1_opy_(method_name: str, *args):
        if not bstack1lll111l1l1_opy_.bstack1l1l111111l_opy_(method_name):
            return False
        if not bstack1lll111l1l1_opy_.bstack11ll1l11lll_opy_ in bstack1lll111l1l1_opy_.bstack11lll11llll_opy_(*args):
            return False
        bstack1l11ll1l1ll_opy_ = bstack1lll111l1l1_opy_.bstack1l11ll1l11l_opy_(*args)
        return (
            bstack1l11ll1l1ll_opy_
            and bstack1ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᜃ") in bstack1l11ll1l1ll_opy_
            and bstack1ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᜄ") in bstack1l11ll1l1ll_opy_[bstack1ll111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᜅ")]
        )
    @staticmethod
    def bstack11lll11llll_opy_(*args):
        return str(bstack1lll111l1l1_opy_.bstack1l1l11l1l11_opy_(*args)).lower()