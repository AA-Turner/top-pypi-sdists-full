# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11ll11l1l1_opy_,
    bstack1l1ll1ll111_opy_,
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111ll11111_opy_(bstack11ll11l1l1_opy_):
    bstack11l111lll11_opy_ = bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᣥ")
    bstack1ll11111lll_opy_ = bstack111ll11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᣦ")
    bstack111llll1ll_opy_ = bstack111ll11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᣧ")
    bstack1lllll1l1l_opy_ = bstack111ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᣨ")
    bstack11l11l1111l_opy_ = bstack111ll11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᣩ")
    bstack11l111ll1l1_opy_ = bstack111ll11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᣪ")
    NAME = bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᣫ")
    bstack11l111lllll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l1lllll_opy_: Any
    bstack11l111ll111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111ll11_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᣬ"), bstack111ll11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᣭ"), bstack111ll11_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᣮ"), bstack111ll11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᣯ"), bstack111ll11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᣰ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll1lllll_opy_(methods)
    def bstack1l1ll1ll1l1_opy_(self, instance: bstack1l1ll1ll111_opy_, method_name: str, bstack1l1ll1111l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1lll11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll1lll11_opy_, bstack11l111l1lll_opy_ = bstack1l1ll11l11l_opy_
        bstack11l111ll1ll_opy_ = bstack111ll11111_opy_.bstack11l111lll1l_opy_(bstack1l1ll11l11l_opy_)
        if bstack11l111ll1ll_opy_ in bstack111ll11111_opy_.bstack11l111lllll_opy_:
            bstack11l111ll11l_opy_ = None
            for callback in bstack111ll11111_opy_.bstack11l111lllll_opy_[bstack11l111ll1ll_opy_]:
                try:
                    bstack11l111llll1_opy_ = callback(self, target, exec, bstack1l1ll11l11l_opy_, result, *args, **kwargs)
                    if bstack11l111ll11l_opy_ == None:
                        bstack11l111ll11l_opy_ = bstack11l111llll1_opy_
                except Exception as e:
                    self.logger.error(bstack111ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᣱ") + str(e) + bstack111ll11_opy_ (u"ࠤࠥᣲ"))
                    traceback.print_exc()
            if bstack11l111l1lll_opy_ == bstack1111111ll_opy_.PRE and callable(bstack11l111ll11l_opy_):
                return bstack11l111ll11l_opy_
            elif bstack11l111l1lll_opy_ == bstack1111111ll_opy_.POST and bstack11l111ll11l_opy_:
                return bstack11l111ll11l_opy_
    def bstack1l1ll11ll1l_opy_(
        self, method_name, previous_state: bstack11l111l1l_opy_, *args, **kwargs
    ) -> bstack11l111l1l_opy_:
        if method_name == bstack111ll11_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᣳ") or method_name == bstack111ll11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᣴ") or method_name == bstack111ll11_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᣵ"):
            return bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_
        if method_name == bstack111ll11_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨ᣶"):
            return bstack11l111l1l_opy_.bstack1l1l1llll11_opy_
        if method_name == bstack111ll11_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭᣷"):
            return bstack11l111l1l_opy_.QUIT
        return bstack11l111l1l_opy_.NONE
    @staticmethod
    def bstack11l111lll1l_opy_(bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_]):
        return bstack111ll11_opy_ (u"ࠣ࠼ࠥ᣸").join((bstack11l111l1l_opy_(bstack1l1ll11l11l_opy_[0]).name, bstack1111111ll_opy_(bstack1l1ll11l11l_opy_[1]).name))
    @staticmethod
    def bstack1l1111111ll_opy_(bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_], callback: Callable):
        bstack11l111ll1ll_opy_ = bstack111ll11111_opy_.bstack11l111lll1l_opy_(bstack1l1ll11l11l_opy_)
        if not bstack11l111ll1ll_opy_ in bstack111ll11111_opy_.bstack11l111lllll_opy_:
            bstack111ll11111_opy_.bstack11l111lllll_opy_[bstack11l111ll1ll_opy_] = []
        bstack111ll11111_opy_.bstack11l111lllll_opy_[bstack11l111ll1ll_opy_].append(callback)
    @staticmethod
    def bstack1l11111111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1111111l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack111ll11111_opy_.bstack11l1l11ll1l_opy_(*args)
        if command_name in [bstack111ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠣ᣹"), bstack111ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠤ᣺")]:
            return True
        return False
    @staticmethod
    def bstack1l1111l11ll_opy_(instance: bstack1l1ll1ll111_opy_, default_value=None):
        return bstack11ll11l1l1_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11111_opy_.bstack1lllll1l1l_opy_, default_value)
    @staticmethod
    def bstack11llll111ll_opy_(instance: bstack1l1ll1ll111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l111111lll_opy_(instance: bstack1l1ll1ll111_opy_, default_value=None):
        return bstack11ll11l1l1_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11111_opy_.bstack111llll1ll_opy_, default_value)
    @staticmethod
    def bstack1l111l1l111_opy_(*args):
        bstack11l11l11111_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11l11l11111_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11l11l11111_opy_ = args[0]
        if not bstack11l11l11111_opy_:
            return None
        return bstack11l11l11111_opy_.strip()
    @staticmethod
    def bstack1l111l111ll_opy_(method_name: str, *args):
        if not bstack111ll11111_opy_.bstack1l11111111l_opy_(method_name):
            return False
        bstack11llll11ll1_opy_ = args[0][1]
        if not isinstance(bstack11llll11ll1_opy_, dict) or bstack111ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩ᣻") not in bstack11llll11ll1_opy_:
            return False
        args_list = bstack11llll11ll1_opy_.get(bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ᣼"), [])
        return any(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠨ᣽") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11lllll11l1_opy_(method_name: str, *args):
        if not bstack111ll11111_opy_.bstack1l11111111l_opy_(method_name):
            return False
        bstack11llll11ll1_opy_ = args[0][1]
        if not isinstance(bstack11llll11ll1_opy_, dict) or bstack111ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬ᣾") not in bstack11llll11ll1_opy_:
            return False
        args_list = bstack11llll11ll1_opy_.get(bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᣿"), [])
        return any(bstack111ll11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࠤࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࠩࠫࠪᤀ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l1l11ll1l_opy_(*args):
        return str(bstack111ll11111_opy_.bstack1l111l1l111_opy_(*args)).lower()