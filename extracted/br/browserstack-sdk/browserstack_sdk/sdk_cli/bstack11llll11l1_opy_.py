# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111lll11l_opy_,
    bstack1ll11l1l111_opy_,
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack11ll1l1l_opy_(bstack111lll11l_opy_):
    bstack11ll1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧ᝭")
    bstack1ll1l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᝮ")
    bstack1l111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᝯ")
    bstack11111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᝰ")
    bstack11ll11111l1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧ᝱")
    bstack11ll11111ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᝲ")
    NAME = bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᝳ")
    bstack11ll111l1l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1lll111ll_opy_: Any
    bstack11ll1111lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll1lll_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧ᝴"), bstack1ll1lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢ᝵"), bstack1ll1lll_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤ᝶"), bstack1ll1lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢ᝷"), bstack1ll1lll_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦ᝸")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll11l11lll_opy_(methods)
    def bstack1ll11l11l1l_opy_(self, instance: bstack1ll11l1l111_opy_, method_name: str, bstack1ll11lll11l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111lll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11ll11ll_opy_, bstack11ll111111l_opy_ = bstack1ll11l1ll11_opy_
        bstack11ll111l11l_opy_ = bstack11ll1l1l_opy_.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        if bstack11ll111l11l_opy_ in bstack11ll1l1l_opy_.bstack11ll111l1l1_opy_:
            bstack11ll111l111_opy_ = None
            for callback in bstack11ll1l1l_opy_.bstack11ll111l1l1_opy_[bstack11ll111l11l_opy_]:
                try:
                    bstack11ll1111111_opy_ = callback(self, target, exec, bstack1ll11l1ll11_opy_, result, *args, **kwargs)
                    if bstack11ll111l111_opy_ == None:
                        bstack11ll111l111_opy_ = bstack11ll1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣ᝹") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧ᝺"))
                    traceback.print_exc()
            if bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.PRE and callable(bstack11ll111l111_opy_):
                return bstack11ll111l111_opy_
            elif bstack11ll111111l_opy_ == bstack1lll1ll11_opy_.POST and bstack11ll111l111_opy_:
                return bstack11ll111l111_opy_
    def bstack1ll1l111111_opy_(
        self, method_name, previous_state: bstack111l11ll_opy_, *args, **kwargs
    ) -> bstack111l11ll_opy_:
        if method_name == bstack1ll1lll_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬ᝻") or method_name == bstack1ll1lll_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧ᝼") or method_name == bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩ᝽"):
            return bstack111l11ll_opy_.bstack11ll1lll1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪ᝾"):
            return bstack111l11ll_opy_.bstack1ll11l1lll1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨ᝿"):
            return bstack111l11ll_opy_.QUIT
        return bstack111l11ll_opy_.NONE
    @staticmethod
    def bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_]):
        return bstack1ll1lll_opy_ (u"ࠥ࠾ࠧក").join((bstack111l11ll_opy_(bstack1ll11l1ll11_opy_[0]).name, bstack1lll1ll11_opy_(bstack1ll11l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_], callback: Callable):
        bstack11ll111l11l_opy_ = bstack11ll1l1l_opy_.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        if not bstack11ll111l11l_opy_ in bstack11ll1l1l_opy_.bstack11ll111l1l1_opy_:
            bstack11ll1l1l_opy_.bstack11ll111l1l1_opy_[bstack11ll111l11l_opy_] = []
        bstack11ll1l1l_opy_.bstack11ll111l1l1_opy_[bstack11ll111l11l_opy_].append(callback)
    @staticmethod
    def bstack1l1l111l1ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l1l111l11l_opy_(method_name: str, *args) -> bool:
        command_name = bstack11ll1l1l_opy_.bstack11ll1l11ll1_opy_(*args)
        if command_name in [bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠥខ"), bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠦគ")]:
            return True
        return False
    @staticmethod
    def bstack1l11ll11l1l_opy_(instance: bstack1ll11l1l111_opy_, default_value=None):
        return bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack11ll1l1l_opy_.bstack11111l11l_opy_, default_value)
    @staticmethod
    def bstack1l111lllll1_opy_(instance: bstack1ll11l1l111_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l11ll111ll_opy_(instance: bstack1ll11l1l111_opy_, default_value=None):
        return bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, default_value)
    @staticmethod
    def bstack1l1l1111l1l_opy_(*args):
        bstack11ll1111l1l_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11ll1111l1l_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11ll1111l1l_opy_ = args[0]
        if not bstack11ll1111l1l_opy_:
            return None
        return bstack11ll1111l1l_opy_.strip()
    @staticmethod
    def bstack1l1l111l1l1_opy_(method_name: str, *args):
        if not bstack11ll1l1l_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        bstack1l11l1l11ll_opy_ = args[0][1]
        if not isinstance(bstack1l11l1l11ll_opy_, dict) or bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫឃ") not in bstack1l11l1l11ll_opy_:
            return False
        args_list = bstack1l11l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬង"), [])
        return any(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠪច") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l11ll1111l_opy_(method_name: str, *args):
        if not bstack11ll1l1l_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        bstack1l11l1l11ll_opy_ = args[0][1]
        if not isinstance(bstack1l11l1l11ll_opy_, dict) or bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧឆ") not in bstack1l11l1l11ll_opy_:
            return False
        args_list = bstack1l11l1l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨជ"), [])
        return any(bstack1ll1lll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࠫ࠭ࠬឈ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11ll1l11ll1_opy_(*args):
        return str(bstack11ll1l1l_opy_.bstack1l1l1111l1l_opy_(*args)).lower()