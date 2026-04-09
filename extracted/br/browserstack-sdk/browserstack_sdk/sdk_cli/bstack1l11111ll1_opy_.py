# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack1lll1111ll_opy_,
    bstack1l1lll111ll_opy_,
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1111l11l1l_opy_(bstack1lll1111ll_opy_):
    bstack11l11l11111_opy_ = bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᣉ")
    bstack1ll111l11l1_opy_ = bstack11ll11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᣊ")
    bstack1111l1l11_opy_ = bstack11ll11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᣋ")
    bstack11ll1l111l_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᣌ")
    bstack11l111llll1_opy_ = bstack11ll11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᣍ")
    bstack11l11l1111l_opy_ = bstack11ll11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᣎ")
    NAME = bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᣏ")
    bstack11l11l11l1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l111l11_opy_: Any
    bstack11l11l111l1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11ll11_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᣐ"), bstack11ll11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᣑ"), bstack11ll11_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᣒ"), bstack11ll11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᣓ"), bstack11ll11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᣔ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll1l111l_opy_(methods)
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1l1lll111ll_opy_, method_name: str, bstack1l1ll111l11_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1l1lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll111lll_opy_, bstack11l11l111ll_opy_ = bstack1l1ll1l11l1_opy_
        bstack11l11l11l11_opy_ = bstack1111l11l1l_opy_.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        if bstack11l11l11l11_opy_ in bstack1111l11l1l_opy_.bstack11l11l11l1l_opy_:
            bstack11l11l11ll1_opy_ = None
            for callback in bstack1111l11l1l_opy_.bstack11l11l11l1l_opy_[bstack11l11l11l11_opy_]:
                try:
                    bstack11l11l1l111_opy_ = callback(self, target, exec, bstack1l1ll1l11l1_opy_, result, *args, **kwargs)
                    if bstack11l11l11ll1_opy_ == None:
                        bstack11l11l11ll1_opy_ = bstack11l11l1l111_opy_
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᣕ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᣖ"))
                    traceback.print_exc()
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.PRE and callable(bstack11l11l11ll1_opy_):
                return bstack11l11l11ll1_opy_
            elif bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST and bstack11l11l11ll1_opy_:
                return bstack11l11l11ll1_opy_
    def bstack1l1lll111l1_opy_(
        self, method_name, previous_state: bstack11111l1ll_opy_, *args, **kwargs
    ) -> bstack11111l1ll_opy_:
        if method_name == bstack11ll11_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᣗ") or method_name == bstack11ll11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᣘ") or method_name == bstack11ll11_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᣙ"):
            return bstack11111l1ll_opy_.bstack1ll11lll1_opy_
        if method_name == bstack11ll11_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨᣚ"):
            return bstack11111l1ll_opy_.bstack1l1ll111l1l_opy_
        if method_name == bstack11ll11_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ᣛ"):
            return bstack11111l1ll_opy_.QUIT
        return bstack11111l1ll_opy_.NONE
    @staticmethod
    def bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_]):
        return bstack11ll11_opy_ (u"ࠣ࠼ࠥᣜ").join((bstack11111l1ll_opy_(bstack1l1ll1l11l1_opy_[0]).name, bstack111llll1ll_opy_(bstack1l1ll1l11l1_opy_[1]).name))
    @staticmethod
    def bstack1l111l11l11_opy_(bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_], callback: Callable):
        bstack11l11l11l11_opy_ = bstack1111l11l1l_opy_.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        if not bstack11l11l11l11_opy_ in bstack1111l11l1l_opy_.bstack11l11l11l1l_opy_:
            bstack1111l11l1l_opy_.bstack11l11l11l1l_opy_[bstack11l11l11l11_opy_] = []
        bstack1111l11l1l_opy_.bstack11l11l11l1l_opy_[bstack11l11l11l11_opy_].append(callback)
    @staticmethod
    def bstack1l111l1l1l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l111111ll1_opy_(method_name: str, *args) -> bool:
        command_name = bstack1111l11l1l_opy_.bstack11l11llll11_opy_(*args)
        if command_name in [bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠣᣝ"), bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠤᣞ")]:
            return True
        return False
    @staticmethod
    def bstack11lllllll1l_opy_(instance: bstack1l1lll111ll_opy_, default_value=None):
        return bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1111l11l1l_opy_.bstack11ll1l111l_opy_, default_value)
    @staticmethod
    def bstack11lll1llll1_opy_(instance: bstack1l1lll111ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack11llllll1l1_opy_(instance: bstack1l1lll111ll_opy_, default_value=None):
        return bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1111l11l1l_opy_.bstack1111l1l11_opy_, default_value)
    @staticmethod
    def bstack1l111ll11ll_opy_(*args):
        bstack11l111lllll_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11l111lllll_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11l111lllll_opy_ = args[0]
        if not bstack11l111lllll_opy_:
            return None
        return bstack11l111lllll_opy_.strip()
    @staticmethod
    def bstack1l11111111l_opy_(method_name: str, *args):
        if not bstack1111l11l1l_opy_.bstack1l111l1l1l1_opy_(method_name):
            return False
        bstack11llll1l11l_opy_ = args[0][1]
        if not isinstance(bstack11llll1l11l_opy_, dict) or bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩᣟ") not in bstack11llll1l11l_opy_:
            return False
        args_list = bstack11llll1l11l_opy_.get(bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᣠ"), [])
        return any(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠨᣡ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l111111lll_opy_(method_name: str, *args):
        if not bstack1111l11l1l_opy_.bstack1l111l1l1l1_opy_(method_name):
            return False
        bstack11llll1l11l_opy_ = args[0][1]
        if not isinstance(bstack11llll1l11l_opy_, dict) or bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᣢ") not in bstack11llll1l11l_opy_:
            return False
        args_list = bstack11llll1l11l_opy_.get(bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᣣ"), [])
        return any(bstack11ll11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࠤࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࠩࠫࠪᣤ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l11llll11_opy_(*args):
        return str(bstack1111l11l1l_opy_.bstack1l111ll11ll_opy_(*args)).lower()