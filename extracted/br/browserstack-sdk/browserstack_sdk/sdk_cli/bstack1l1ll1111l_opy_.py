# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11ll11l1_opy_,
    bstack1ll11ll1l11_opy_,
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111l111ll_opy_(bstack11ll11l1_opy_):
    bstack11ll111111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣច")
    bstack1ll1ll111ll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤឆ")
    bstack1lll111l_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦជ")
    bstack11l11l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥឈ")
    bstack11l1llllll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣញ")
    bstack11l1llll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢដ")
    NAME = bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦឋ")
    bstack11ll1111111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1ll1ll1_opy_: Any
    bstack11l1lllll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1ll1lll_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣឌ"), bstack1ll1lll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥឍ"), bstack1ll1lll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧណ"), bstack1ll1lll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥត"), bstack1ll1lll_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢថ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll111lll1l_opy_(methods)
    def bstack1ll11l11l11_opy_(self, instance: bstack1ll11ll1l11_opy_, method_name: str, bstack1ll111ll1l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1l1lll1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11l1lll1_opy_, bstack11l1lllllll_opy_ = bstack1ll11l1l111_opy_
        bstack11l1llll111_opy_ = bstack111l111ll_opy_.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        if bstack11l1llll111_opy_ in bstack111l111ll_opy_.bstack11ll1111111_opy_:
            bstack11l1lllll11_opy_ = None
            for callback in bstack111l111ll_opy_.bstack11ll1111111_opy_[bstack11l1llll111_opy_]:
                try:
                    bstack11l1llll11l_opy_ = callback(self, target, exec, bstack1ll11l1l111_opy_, result, *args, **kwargs)
                    if bstack11l1lllll11_opy_ == None:
                        bstack11l1lllll11_opy_ = bstack11l1llll11l_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦទ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣធ"))
                    traceback.print_exc()
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.PRE and callable(bstack11l1lllll11_opy_):
                return bstack11l1lllll11_opy_
            elif bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST and bstack11l1lllll11_opy_:
                return bstack11l1lllll11_opy_
    def bstack1ll11llll11_opy_(
        self, method_name, previous_state: bstack11lll111_opy_, *args, **kwargs
    ) -> bstack11lll111_opy_:
        if method_name == bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࠨន") or method_name == bstack1ll1lll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪប") or method_name == bstack1ll1lll_opy_ (u"ࠪࡲࡪࡽ࡟ࡱࡣࡪࡩࠬផ"):
            return bstack11lll111_opy_.bstack1l111ll1l1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠫࡩ࡯ࡳࡱࡣࡷࡧ࡭࠭ព"):
            return bstack11lll111_opy_.bstack1ll11l11ll1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫភ"):
            return bstack11lll111_opy_.QUIT
        return bstack11lll111_opy_.NONE
    @staticmethod
    def bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_]):
        return bstack1ll1lll_opy_ (u"ࠨ࠺ࠣម").join((bstack11lll111_opy_(bstack1ll11l1l111_opy_[0]).name, bstack1l11l11l1_opy_(bstack1ll11l1l111_opy_[1]).name))
    @staticmethod
    def bstack1l11ll11111_opy_(bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_], callback: Callable):
        bstack11l1llll111_opy_ = bstack111l111ll_opy_.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        if not bstack11l1llll111_opy_ in bstack111l111ll_opy_.bstack11ll1111111_opy_:
            bstack111l111ll_opy_.bstack11ll1111111_opy_[bstack11l1llll111_opy_] = []
        bstack111l111ll_opy_.bstack11ll1111111_opy_[bstack11l1llll111_opy_].append(callback)
    @staticmethod
    def bstack1l1l11111ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l11l1l11l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack111l111ll_opy_.bstack11ll11l11ll_opy_(*args)
        if command_name in [bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡰࡨࡻࠥࡨࡲࡰࡹࡶࡩࡷࠨយ"), bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦࡢࡳࡱࡺࡷࡪࡸࠢរ")]:
            return True
        return False
    @staticmethod
    def bstack1l11lll1lll_opy_(instance: bstack1ll11ll1l11_opy_, default_value=None):
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack111l111ll_opy_.bstack11l11l11_opy_, default_value)
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1ll11ll1l11_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l11l1111_opy_(instance: bstack1ll11ll1l11_opy_, default_value=None):
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, default_value)
    @staticmethod
    def bstack1l11llll11l_opy_(*args):
        bstack11ll11111l1_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11ll11111l1_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11ll11111l1_opy_ = args[0]
        if not bstack11ll11111l1_opy_:
            return None
        return bstack11ll11111l1_opy_.strip()
    @staticmethod
    def bstack1l11l11llll_opy_(method_name: str, *args):
        if not bstack111l111ll_opy_.bstack1l1l11111ll_opy_(method_name):
            return False
        bstack1l11l111l1l_opy_ = args[0][1]
        if not isinstance(bstack1l11l111l1l_opy_, dict) or bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧល") not in bstack1l11l111l1l_opy_:
            return False
        args_list = bstack1l11l111l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨវ"), [])
        return any(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿࠭ឝ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l1l11111l1_opy_(method_name: str, *args):
        if not bstack111l111ll_opy_.bstack1l1l11111ll_opy_(method_name):
            return False
        bstack1l11l111l1l_opy_ = args[0][1]
        if not isinstance(bstack1l11l111l1l_opy_, dict) or bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪឞ") not in bstack1l11l111l1l_opy_:
            return False
        args_list = bstack1l11l111l1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫស"), [])
        return any(bstack1ll1lll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࠮ࠩࠨហ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11ll11l11ll_opy_(*args):
        return str(bstack111l111ll_opy_.bstack1l11llll11l_opy_(*args)).lower()