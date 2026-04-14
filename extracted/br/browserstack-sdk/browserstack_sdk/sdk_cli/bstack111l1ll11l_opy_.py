# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack111l1ll1ll_opy_,
    bstack1l1ll1lllll_opy_,
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack11ll1llll_opy_(bstack111l1ll1ll_opy_):
    bstack11l111lllll_opy_ = bstack1l111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᣥ")
    bstack1ll1111lll1_opy_ = bstack1l111l_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᣦ")
    bstack11llll1l11_opy_ = bstack1l111l_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᣧ")
    bstack11lll111l_opy_ = bstack1l111l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᣨ")
    bstack11l111ll111_opy_ = bstack1l111l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᣩ")
    bstack11l111lll11_opy_ = bstack1l111l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᣪ")
    NAME = bstack1l111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᣫ")
    bstack11l111ll11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1lll1l1_opy_: Any
    bstack11l11l11111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l111l_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥᣬ"), bstack1l111l_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᣭ"), bstack1l111l_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᣮ"), bstack1l111l_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᣯ"), bstack1l111l_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤᣰ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll1llll1_opy_(methods)
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1l1ll1lllll_opy_, method_name: str, bstack1l1ll1l11l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1l1l1llll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll1l111l_opy_, bstack11l111ll1ll_opy_ = bstack1l1l1lllll1_opy_
        bstack11l11l1111l_opy_ = bstack11ll1llll_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        if bstack11l11l1111l_opy_ in bstack11ll1llll_opy_.bstack11l111ll11l_opy_:
            bstack11l111lll1l_opy_ = None
            for callback in bstack11ll1llll_opy_.bstack11l111ll11l_opy_[bstack11l11l1111l_opy_]:
                try:
                    bstack11l111llll1_opy_ = callback(self, target, exec, bstack1l1l1lllll1_opy_, result, *args, **kwargs)
                    if bstack11l111lll1l_opy_ == None:
                        bstack11l111lll1l_opy_ = bstack11l111llll1_opy_
                except Exception as e:
                    self.logger.error(bstack1l111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᣱ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᣲ"))
                    traceback.print_exc()
            if bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.PRE and callable(bstack11l111lll1l_opy_):
                return bstack11l111lll1l_opy_
            elif bstack11l111ll1ll_opy_ == bstack1ll1llll1l_opy_.POST and bstack11l111lll1l_opy_:
                return bstack11l111lll1l_opy_
    def bstack1l1l1llll1l_opy_(
        self, method_name, previous_state: bstack1l1l11ll1l_opy_, *args, **kwargs
    ) -> bstack1l1l11ll1l_opy_:
        if method_name == bstack1l111l_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪᣳ") or method_name == bstack1l111l_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᣴ") or method_name == bstack1l111l_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧᣵ"):
            return bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_
        if method_name == bstack1l111l_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨ᣶"):
            return bstack1l1l11ll1l_opy_.bstack1l1ll1l1l11_opy_
        if method_name == bstack1l111l_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭᣷"):
            return bstack1l1l11ll1l_opy_.QUIT
        return bstack1l1l11ll1l_opy_.NONE
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_]):
        return bstack1l111l_opy_ (u"ࠣ࠼ࠥ᣸").join((bstack1l1l11ll1l_opy_(bstack1l1l1lllll1_opy_[0]).name, bstack1ll1llll1l_opy_(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack1l11111ll11_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_], callback: Callable):
        bstack11l11l1111l_opy_ = bstack11ll1llll_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        if not bstack11l11l1111l_opy_ in bstack11ll1llll_opy_.bstack11l111ll11l_opy_:
            bstack11ll1llll_opy_.bstack11l111ll11l_opy_[bstack11l11l1111l_opy_] = []
        bstack11ll1llll_opy_.bstack11l111ll11l_opy_[bstack11l11l1111l_opy_].append(callback)
    @staticmethod
    def bstack11lllll1ll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l111l111l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack11ll1llll_opy_.bstack11l1l1l1111_opy_(*args)
        if command_name in [bstack1l111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠣ᣹"), bstack1l111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠤ᣺")]:
            return True
        return False
    @staticmethod
    def bstack1l111ll11l1_opy_(instance: bstack1l1ll1lllll_opy_, default_value=None):
        return bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, bstack11ll1llll_opy_.bstack11lll111l_opy_, default_value)
    @staticmethod
    def bstack11lll1lllll_opy_(instance: bstack1l1ll1lllll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1111l1l11_opy_(instance: bstack1l1ll1lllll_opy_, default_value=None):
        return bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, bstack11ll1llll_opy_.bstack11llll1l11_opy_, default_value)
    @staticmethod
    def bstack1l111111l11_opy_(*args):
        bstack11l111l1lll_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11l111l1lll_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11l111l1lll_opy_ = args[0]
        if not bstack11l111l1lll_opy_:
            return None
        return bstack11l111l1lll_opy_.strip()
    @staticmethod
    def bstack1l111l1l111_opy_(method_name: str, *args):
        if not bstack11ll1llll_opy_.bstack11lllll1ll1_opy_(method_name):
            return False
        bstack11llll1ll11_opy_ = args[0][1]
        if not isinstance(bstack11llll1ll11_opy_, dict) or bstack1l111l_opy_ (u"ࠫࡦࡸࡧࡴࠩ᣻") not in bstack11llll1ll11_opy_:
            return False
        args_list = bstack11llll1ll11_opy_.get(bstack1l111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ᣼"), [])
        return any(bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠨ᣽") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11lllll111l_opy_(method_name: str, *args):
        if not bstack11ll1llll_opy_.bstack11lllll1ll1_opy_(method_name):
            return False
        bstack11llll1ll11_opy_ = args[0][1]
        if not isinstance(bstack11llll1ll11_opy_, dict) or bstack1l111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ᣾") not in bstack11llll1ll11_opy_:
            return False
        args_list = bstack11llll1ll11_opy_.get(bstack1l111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᣿"), [])
        return any(bstack1l111l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࠤࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࠩࠫࠪᤀ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l1l1l1111_opy_(*args):
        return str(bstack11ll1llll_opy_.bstack1l111111l11_opy_(*args)).lower()