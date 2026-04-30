# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack11l1l1ll11_opy_,
    bstack1l1ll11l1ll_opy_,
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111l1l11l_opy_(bstack11l1l1ll11_opy_):
    bstack11l111lll11_opy_ = bstack1l1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᣧ")
    bstack1l1lllll1l1_opy_ = bstack1l1111l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᣨ")
    bstack11111llll_opy_ = bstack1l1111l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᣩ")
    bstack1l111111l_opy_ = bstack1l1111l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᣪ")
    bstack11l111ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᣫ")
    bstack11l111l1ll1_opy_ = bstack1l1111l_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᣬ")
    NAME = bstack1l1111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᣭ")
    bstack11l111ll11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11lll1l11_opy_: Any
    bstack11l111lllll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1111l_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧᣮ"), bstack1l1111l_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᣯ"), bstack1l1111l_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᣰ"), bstack1l1111l_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᣱ"), bstack1l1111l_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦᣲ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll111l11_opy_(methods)
    def bstack1l1l1lllll1_opy_(self, instance: bstack1l1ll11l1ll_opy_, method_name: str, bstack1l1l1llll11_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llll111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1llll1l_opy_, bstack11l111lll1l_opy_ = bstack1l1ll1ll111_opy_
        bstack11l111ll111_opy_ = bstack111l1l11l_opy_.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        if bstack11l111ll111_opy_ in bstack111l1l11l_opy_.bstack11l111ll11l_opy_:
            bstack11l111l1l1l_opy_ = None
            for callback in bstack111l1l11l_opy_.bstack11l111ll11l_opy_[bstack11l111ll111_opy_]:
                try:
                    bstack11l111ll1l1_opy_ = callback(self, target, exec, bstack1l1ll1ll111_opy_, result, *args, **kwargs)
                    if bstack11l111l1l1l_opy_ == None:
                        bstack11l111l1l1l_opy_ = bstack11l111ll1l1_opy_
                except Exception as e:
                    self.logger.error(bstack1l1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᣳ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᣴ"))
                    traceback.print_exc()
            if bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.PRE and callable(bstack11l111l1l1l_opy_):
                return bstack11l111l1l1l_opy_
            elif bstack11l111lll1l_opy_ == bstack1111llll1l_opy_.POST and bstack11l111l1l1l_opy_:
                return bstack11l111l1l1l_opy_
    def bstack1l1ll11ll11_opy_(
        self, method_name, previous_state: bstack1lll11l1l1_opy_, *args, **kwargs
    ) -> bstack1lll11l1l1_opy_:
        if method_name == bstack1l1111l_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬᣵ") or method_name == bstack1l1111l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧ᣶") or method_name == bstack1l1111l_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩ᣷"):
            return bstack1lll11l1l1_opy_.bstack1lll1l111_opy_
        if method_name == bstack1l1111l_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪ᣸"):
            return bstack1lll11l1l1_opy_.bstack1l1ll11llll_opy_
        if method_name == bstack1l1111l_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨ᣹"):
            return bstack1lll11l1l1_opy_.QUIT
        return bstack1lll11l1l1_opy_.NONE
    @staticmethod
    def bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_]):
        return bstack1l1111l_opy_ (u"ࠥ࠾ࠧ᣺").join((bstack1lll11l1l1_opy_(bstack1l1ll1ll111_opy_[0]).name, bstack1111llll1l_opy_(bstack1l1ll1ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1111lllll_opy_(bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_], callback: Callable):
        bstack11l111ll111_opy_ = bstack111l1l11l_opy_.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        if not bstack11l111ll111_opy_ in bstack111l1l11l_opy_.bstack11l111ll11l_opy_:
            bstack111l1l11l_opy_.bstack11l111ll11l_opy_[bstack11l111ll111_opy_] = []
        bstack111l1l11l_opy_.bstack11l111ll11l_opy_[bstack11l111ll111_opy_].append(callback)
    @staticmethod
    def bstack1l1111l111l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l111l1llll_opy_(method_name: str, *args) -> bool:
        command_name = bstack111l1l11l_opy_.bstack11l1l11l1ll_opy_(*args)
        if command_name in [bstack1l1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠥ᣻"), bstack1l1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠦ᣼")]:
            return True
        return False
    @staticmethod
    def bstack1l111l11l11_opy_(instance: bstack1l1ll11l1ll_opy_, default_value=None):
        return bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack111l1l11l_opy_.bstack1l111111l_opy_, default_value)
    @staticmethod
    def bstack11lll1l1ll1_opy_(instance: bstack1l1ll11l1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack11lllll1l1l_opy_(instance: bstack1l1ll11l1ll_opy_, default_value=None):
        return bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack111l1l11l_opy_.bstack11111llll_opy_, default_value)
    @staticmethod
    def bstack1l1111l11l1_opy_(*args):
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
    def bstack11lllll1111_opy_(method_name: str, *args):
        if not bstack111l1l11l_opy_.bstack1l1111l111l_opy_(method_name):
            return False
        bstack11llll1l1l1_opy_ = args[0][1]
        if not isinstance(bstack11llll1l1l1_opy_, dict) or bstack1l1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫ᣽") not in bstack11llll1l1l1_opy_:
            return False
        args_list = bstack11llll1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ᣾"), [])
        return any(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠪ᣿") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l1111111l1_opy_(method_name: str, *args):
        if not bstack111l1l11l_opy_.bstack1l1111l111l_opy_(method_name):
            return False
        bstack11llll1l1l1_opy_ = args[0][1]
        if not isinstance(bstack11llll1l1l1_opy_, dict) or bstack1l1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᤀ") not in bstack11llll1l1l1_opy_:
            return False
        args_list = bstack11llll1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤁ"), [])
        return any(bstack1l1111l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࠫ࠭ࠬᤂ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l1l11l1ll_opy_(*args):
        return str(bstack111l1l11l_opy_.bstack1l1111l11l1_opy_(*args)).lower()