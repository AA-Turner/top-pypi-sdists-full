# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack111l1ll111_opy_,
    bstack1ll111lllll_opy_,
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1l111lllll_opy_(bstack111l1ll111_opy_):
    bstack11l1llll11l_opy_ = bstack1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦព")
    bstack1ll1l1l1lll_opy_ = bstack1ll11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧភ")
    bstack1ll11l1lll_opy_ = bstack1ll11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢម")
    bstack1lll1l1111_opy_ = bstack1ll11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨយ")
    bstack11l1llll1l1_opy_ = bstack1ll11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦរ")
    bstack11l1lllll1l_opy_ = bstack1ll11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥល")
    NAME = bstack1ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢវ")
    bstack11l1llll1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1lll11l_opy_: Any
    bstack11l1lllllll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll11_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦឝ"), bstack1ll11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨឞ"), bstack1ll11_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣស"), bstack1ll11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨហ"), bstack1ll11_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥឡ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll11l1ll1l_opy_(methods)
    def bstack1ll11l11111_opy_(self, instance: bstack1ll111lllll_opy_, method_name: str, bstack1ll11ll111l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1ll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll111l1ll1_opy_, bstack11l1lllll11_opy_ = bstack1ll11l11lll_opy_
        bstack11l1llll111_opy_ = bstack1l111lllll_opy_.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        if bstack11l1llll111_opy_ in bstack1l111lllll_opy_.bstack11l1llll1ll_opy_:
            bstack11l1llllll1_opy_ = None
            for callback in bstack1l111lllll_opy_.bstack11l1llll1ll_opy_[bstack11l1llll111_opy_]:
                try:
                    bstack11ll1111111_opy_ = callback(self, target, exec, bstack1ll11l11lll_opy_, result, *args, **kwargs)
                    if bstack11l1llllll1_opy_ == None:
                        bstack11l1llllll1_opy_ = bstack11ll1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢអ") + str(e) + bstack1ll11_opy_ (u"ࠥࠦឣ"))
                    traceback.print_exc()
            if bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.PRE and callable(bstack11l1llllll1_opy_):
                return bstack11l1llllll1_opy_
            elif bstack11l1lllll11_opy_ == bstack1ll11ll1ll_opy_.POST and bstack11l1llllll1_opy_:
                return bstack11l1llllll1_opy_
    def bstack1ll11l111l1_opy_(
        self, method_name, previous_state: bstack1ll1l1ll11_opy_, *args, **kwargs
    ) -> bstack1ll1l1ll11_opy_:
        if method_name == bstack1ll11_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࠫឤ") or method_name == bstack1ll11_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ឥ") or method_name == bstack1ll11_opy_ (u"࠭࡮ࡦࡹࡢࡴࡦ࡭ࡥࠨឦ"):
            return bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_
        if method_name == bstack1ll11_opy_ (u"ࠧࡥ࡫ࡶࡴࡦࡺࡣࡩࠩឧ"):
            return bstack1ll1l1ll11_opy_.bstack1ll111lll11_opy_
        if method_name == bstack1ll11_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠧឨ"):
            return bstack1ll1l1ll11_opy_.QUIT
        return bstack1ll1l1ll11_opy_.NONE
    @staticmethod
    def bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_]):
        return bstack1ll11_opy_ (u"ࠤ࠽ࠦឩ").join((bstack1ll1l1ll11_opy_(bstack1ll11l11lll_opy_[0]).name, bstack1ll11ll1ll_opy_(bstack1ll11l11lll_opy_[1]).name))
    @staticmethod
    def bstack1l11lll1lll_opy_(bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_], callback: Callable):
        bstack11l1llll111_opy_ = bstack1l111lllll_opy_.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        if not bstack11l1llll111_opy_ in bstack1l111lllll_opy_.bstack11l1llll1ll_opy_:
            bstack1l111lllll_opy_.bstack11l1llll1ll_opy_[bstack11l1llll111_opy_] = []
        bstack1l111lllll_opy_.bstack11l1llll1ll_opy_[bstack11l1llll111_opy_].append(callback)
    @staticmethod
    def bstack1l11l1l1lll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l11ll1l1ll_opy_(method_name: str, *args) -> bool:
        command_name = bstack1l111lllll_opy_.bstack11ll11l1l11_opy_(*args)
        if command_name in [bstack1ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࠡࡤࡵࡳࡼࡹࡥࡳࠤឪ"), bstack1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥࡶࡴࡽࡳࡦࡴࠥឫ")]:
            return True
        return False
    @staticmethod
    def bstack1l1l111111l_opy_(instance: bstack1ll111lllll_opy_, default_value=None):
        return bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1l111lllll_opy_.bstack1lll1l1111_opy_, default_value)
    @staticmethod
    def bstack1l11l111111_opy_(instance: bstack1ll111lllll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l11ll11lll_opy_(instance: bstack1ll111lllll_opy_, default_value=None):
        return bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1l111lllll_opy_.bstack1ll11l1lll_opy_, default_value)
    @staticmethod
    def bstack1l1l111ll11_opy_(*args):
        bstack11l1lll1lll_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11l1lll1lll_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11l1lll1lll_opy_ = args[0]
        if not bstack11l1lll1lll_opy_:
            return None
        return bstack11l1lll1lll_opy_.strip()
    @staticmethod
    def bstack1l11lll11ll_opy_(method_name: str, *args):
        if not bstack1l111lllll_opy_.bstack1l11l1l1lll_opy_(method_name):
            return False
        bstack1l11l1111ll_opy_ = args[0][1]
        if not isinstance(bstack1l11l1111ll_opy_, dict) or bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪឬ") not in bstack1l11l1111ll_opy_:
            return False
        args_list = bstack1l11l1111ll_opy_.get(bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫឭ"), [])
        return any(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠩឮ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l11ll11ll1_opy_(method_name: str, *args):
        if not bstack1l111lllll_opy_.bstack1l11l1l1lll_opy_(method_name):
            return False
        bstack1l11l1111ll_opy_ = args[0][1]
        if not isinstance(bstack1l11l1111ll_opy_, dict) or bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ឯ") not in bstack1l11l1111ll_opy_:
            return False
        args_list = bstack1l11l1111ll_opy_.get(bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧឰ"), [])
        return any(bstack1ll11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࠪࠬࠫឱ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11ll11l1l11_opy_(*args):
        return str(bstack1l111lllll_opy_.bstack1l1l111ll11_opy_(*args)).lower()