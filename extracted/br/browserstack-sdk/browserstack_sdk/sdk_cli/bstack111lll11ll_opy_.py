# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack11l1111ll_opy_,
    bstack1l1ll11ll11_opy_,
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack11ll1l111l_opy_(bstack11l1111ll_opy_):
    bstack11l11l11111_opy_ = bstack1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᣌ")
    bstack1l1lllll11l_opy_ = bstack1ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᣍ")
    bstack11llll1l11_opy_ = bstack1ll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᣎ")
    bstack11l1111l1l_opy_ = bstack1ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᣏ")
    bstack11l111llll1_opy_ = bstack1ll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᣐ")
    bstack11l111lll1l_opy_ = bstack1ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᣑ")
    NAME = bstack1ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᣒ")
    bstack11l111ll1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l11ll11l_opy_: Any
    bstack11l11l1111l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᣓ"), bstack1ll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣᣔ"), bstack1ll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᣕ"), bstack1ll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᣖ"), bstack1ll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᣗ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll1ll1l1_opy_(methods)
    def bstack1l1lll11111_opy_(self, instance: bstack1l1ll11ll11_opy_, method_name: str, bstack1l1lll111l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1l1l1ll1ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll1l11l1_opy_, bstack11l11l111ll_opy_ = bstack1l1ll1lll11_opy_
        bstack11l111lllll_opy_ = bstack11ll1l111l_opy_.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        if bstack11l111lllll_opy_ in bstack11ll1l111l_opy_.bstack11l111ll1ll_opy_:
            bstack11l111ll1l1_opy_ = None
            for callback in bstack11ll1l111l_opy_.bstack11l111ll1ll_opy_[bstack11l111lllll_opy_]:
                try:
                    bstack11l111lll11_opy_ = callback(self, target, exec, bstack1l1ll1lll11_opy_, result, *args, **kwargs)
                    if bstack11l111ll1l1_opy_ == None:
                        bstack11l111ll1l1_opy_ = bstack11l111lll11_opy_
                except Exception as e:
                    self.logger.error(bstack1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᣘ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᣙ"))
                    traceback.print_exc()
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.PRE and callable(bstack11l111ll1l1_opy_):
                return bstack11l111ll1l1_opy_
            elif bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST and bstack11l111ll1l1_opy_:
                return bstack11l111ll1l1_opy_
    def bstack1l1ll1ll111_opy_(
        self, method_name, previous_state: bstack1111ll1l11_opy_, *args, **kwargs
    ) -> bstack1111ll1l11_opy_:
        if method_name == bstack1ll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭ᣚ") or method_name == bstack1ll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᣛ") or method_name == bstack1ll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪᣜ"):
            return bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_
        if method_name == bstack1ll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫᣝ"):
            return bstack1111ll1l11_opy_.bstack1l1ll1l1111_opy_
        if method_name == bstack1ll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᣞ"):
            return bstack1111ll1l11_opy_.QUIT
        return bstack1111ll1l11_opy_.NONE
    @staticmethod
    def bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_]):
        return bstack1ll_opy_ (u"ࠦ࠿ࠨᣟ").join((bstack1111ll1l11_opy_(bstack1l1ll1lll11_opy_[0]).name, bstack1llll11lll_opy_(bstack1l1ll1lll11_opy_[1]).name))
    @staticmethod
    def bstack1l1111111l1_opy_(bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_], callback: Callable):
        bstack11l111lllll_opy_ = bstack11ll1l111l_opy_.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        if not bstack11l111lllll_opy_ in bstack11ll1l111l_opy_.bstack11l111ll1ll_opy_:
            bstack11ll1l111l_opy_.bstack11l111ll1ll_opy_[bstack11l111lllll_opy_] = []
        bstack11ll1l111l_opy_.bstack11l111ll1ll_opy_[bstack11l111lllll_opy_].append(callback)
    @staticmethod
    def bstack1l111ll1l1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l11111l1l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack11ll1l111l_opy_.bstack11l11lll11l_opy_(*args)
        if command_name in [bstack1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࠴࡮ࡦࡹࠣࡦࡷࡵࡷࡴࡧࡵࠦᣠ"), bstack1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡲࡪࡩࡴࠡࡶࡲࠤࡧࡸ࡯ࡸࡵࡨࡶࠧᣡ")]:
            return True
        return False
    @staticmethod
    def bstack1l111l1ll1l_opy_(instance: bstack1l1ll11ll11_opy_, default_value=None):
        return bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, bstack11ll1l111l_opy_.bstack11l1111l1l_opy_, default_value)
    @staticmethod
    def bstack11llll111l1_opy_(instance: bstack1l1ll11ll11_opy_) -> bool:
        return True
    @staticmethod
    def bstack11lllll11ll_opy_(instance: bstack1l1ll11ll11_opy_, default_value=None):
        return bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, bstack11ll1l111l_opy_.bstack11llll1l11_opy_, default_value)
    @staticmethod
    def bstack11lllllll11_opy_(*args):
        bstack11l11l111l1_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11l11l111l1_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11l11l111l1_opy_ = args[0]
        if not bstack11l11l111l1_opy_:
            return None
        return bstack11l11l111l1_opy_.strip()
    @staticmethod
    def bstack1l1111ll111_opy_(method_name: str, *args):
        if not bstack11ll1l111l_opy_.bstack1l111ll1l1l_opy_(method_name):
            return False
        bstack11llll1l111_opy_ = args[0][1]
        if not isinstance(bstack11llll1l111_opy_, dict) or bstack1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬᣢ") not in bstack11llll1l111_opy_:
            return False
        args_list = bstack11llll1l111_opy_.get(bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᣣ"), [])
        return any(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠫᣤ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11lllll1lll_opy_(method_name: str, *args):
        if not bstack11ll1l111l_opy_.bstack1l111ll1l1l_opy_(method_name):
            return False
        bstack11llll1l111_opy_ = args[0][1]
        if not isinstance(bstack11llll1l111_opy_, dict) or bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᣥ") not in bstack11llll1l111_opy_:
            return False
        args_list = bstack11llll1l111_opy_.get(bstack1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᣦ"), [])
        return any(bstack1ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࠬ࠮࠭ᣧ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l11lll11l_opy_(*args):
        return str(bstack11ll1l111l_opy_.bstack11lllllll11_opy_(*args)).lower()