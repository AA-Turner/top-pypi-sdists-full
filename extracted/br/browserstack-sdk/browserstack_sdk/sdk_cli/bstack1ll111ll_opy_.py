# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack1l1l1ll11l_opy_,
    bstack1l1l111l1l1_opy_,
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack11ll1lllll_opy_(bstack1l1l1ll11l_opy_):
    bstack111lllll111_opy_ = bstack111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᥝ")
    bstack1ll11111111_opy_ = bstack111l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᥞ")
    bstack11l1ll111l_opy_ = bstack111l_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᥟ")
    bstack1111lll1_opy_ = bstack111l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᥠ")
    bstack111lllll11l_opy_ = bstack111l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᥡ")
    bstack111llll1l11_opy_ = bstack111l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᥢ")
    NAME = bstack111l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᥣ")
    bstack111llll1lll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l111l11_opy_: Any
    bstack111llllll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111l_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦᥤ"), bstack111l_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᥥ"), bstack111l_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᥦ"), bstack111l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᥧ"), bstack111l_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥᥨ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1l111ll11_opy_(methods)
    def bstack1l1l11l1111_opy_(self, instance: bstack1l1l111l1l1_opy_, method_name: str, bstack1l1l111lll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11l11ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1111lll_opy_, bstack111llll11ll_opy_ = bstack1l1l1lllll1_opy_
        bstack111llllll11_opy_ = bstack11ll1lllll_opy_.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        if bstack111llllll11_opy_ in bstack11ll1lllll_opy_.bstack111llll1lll_opy_:
            bstack111lllll1ll_opy_ = None
            for callback in bstack11ll1lllll_opy_.bstack111llll1lll_opy_[bstack111llllll11_opy_]:
                try:
                    bstack111lllll1l1_opy_ = callback(self, target, exec, bstack1l1l1lllll1_opy_, result, *args, **kwargs)
                    if bstack111lllll1ll_opy_ == None:
                        bstack111lllll1ll_opy_ = bstack111lllll1l1_opy_
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᥩ") + str(e) + bstack111l_opy_ (u"ࠥࠦᥪ"))
                    traceback.print_exc()
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.PRE and callable(bstack111lllll1ll_opy_):
                return bstack111lllll1ll_opy_
            elif bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST and bstack111lllll1ll_opy_:
                return bstack111lllll1ll_opy_
    def bstack1l11lll1l11_opy_(
        self, method_name, previous_state: bstack11l1ll1l1_opy_, *args, **kwargs
    ) -> bstack11l1ll1l1_opy_:
        if method_name == bstack111l_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫᥫ") or method_name == bstack111l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᥬ") or method_name == bstack111l_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨᥭ"):
            return bstack11l1ll1l1_opy_.bstack11llll111l_opy_
        if method_name == bstack111l_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩ᥮"):
            return bstack11l1ll1l1_opy_.bstack1l11lll1ll1_opy_
        if method_name == bstack111l_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧ᥯"):
            return bstack11l1ll1l1_opy_.QUIT
        return bstack11l1ll1l1_opy_.NONE
    @staticmethod
    def bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_]):
        return bstack111l_opy_ (u"ࠤ࠽ࠦᥰ").join((bstack11l1ll1l1_opy_(bstack1l1l1lllll1_opy_[0]).name, bstack1lll1l11l1_opy_(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack11llll1l1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_], callback: Callable):
        bstack111llllll11_opy_ = bstack11ll1lllll_opy_.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        if not bstack111llllll11_opy_ in bstack11ll1lllll_opy_.bstack111llll1lll_opy_:
            bstack11ll1lllll_opy_.bstack111llll1lll_opy_[bstack111llllll11_opy_] = []
        bstack11ll1lllll_opy_.bstack111llll1lll_opy_[bstack111llllll11_opy_].append(callback)
    @staticmethod
    def bstack11llll111l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack11lll1l11l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack11ll1lllll_opy_.bstack11l11l1l11l_opy_(*args)
        if command_name in [bstack111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࠡࡤࡵࡳࡼࡹࡥࡳࠤᥱ"), bstack111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥࡶࡴࡽࡳࡦࡴࠥᥲ")]:
            return True
        return False
    @staticmethod
    def bstack11lll11111l_opy_(instance: bstack1l1l111l1l1_opy_, default_value=None):
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack11ll1lllll_opy_.bstack1111lll1_opy_, default_value)
    @staticmethod
    def bstack11ll1l11l11_opy_(instance: bstack1l1l111l1l1_opy_) -> bool:
        return True
    @staticmethod
    def bstack11ll1ll1lll_opy_(instance: bstack1l1l111l1l1_opy_, default_value=None):
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack11ll1lllll_opy_.bstack11l1ll111l_opy_, default_value)
    @staticmethod
    def bstack11lll1ll11l_opy_(*args):
        bstack111llll1ll1_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack111llll1ll1_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack111llll1ll1_opy_ = args[0]
        if not bstack111llll1ll1_opy_:
            return None
        return bstack111llll1ll1_opy_.strip()
    @staticmethod
    def bstack11lll111l11_opy_(method_name: str, *args):
        if not bstack11ll1lllll_opy_.bstack11llll111l1_opy_(method_name):
            return False
        bstack11ll1l1l1l1_opy_ = args[0][1]
        if not isinstance(bstack11ll1l1l1l1_opy_, dict) or bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪᥳ") not in bstack11ll1l1l1l1_opy_:
            return False
        args_list = bstack11ll1l1l1l1_opy_.get(bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᥴ"), [])
        return any(bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠩ᥵") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11lll1l1l1l_opy_(method_name: str, *args):
        if not bstack11ll1lllll_opy_.bstack11llll111l1_opy_(method_name):
            return False
        bstack11ll1l1l1l1_opy_ = args[0][1]
        if not isinstance(bstack11ll1l1l1l1_opy_, dict) or bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᥶") not in bstack11ll1l1l1l1_opy_:
            return False
        args_list = bstack11ll1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᥷"), [])
        return any(bstack111l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࠪࠬࠫ᥸") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l11l1l11l_opy_(*args):
        return str(bstack11ll1lllll_opy_.bstack11lll1ll11l_opy_(*args)).lower()