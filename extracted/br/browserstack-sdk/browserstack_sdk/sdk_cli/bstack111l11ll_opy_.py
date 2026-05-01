# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack11l1l1l1_opy_,
    bstack1l1ll111lll_opy_,
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack11ll1l1ll_opy_(bstack11l1l1l1_opy_):
    bstack11l111lll11_opy_ = bstack111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ᣶")
    bstack1ll1111ll11_opy_ = bstack111ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ᣷")
    bstack1ll1llll1_opy_ = bstack111ll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤ᣸")
    bstack1ll111ll_opy_ = bstack111ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᣹")
    bstack11l111l11ll_opy_ = bstack111ll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨ᣺")
    bstack11l111l1l1l_opy_ = bstack111ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧ᣻")
    NAME = bstack111ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᣼")
    bstack11l111ll1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l11lll1_opy_: Any
    bstack11l111l11l1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack111ll_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨ᣽"), bstack111ll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ᣾"), bstack111ll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥ᣿"), bstack111ll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᤀ"), bstack111ll_opy_ (u"ࠥࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠧᤁ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l1ll1ll11l_opy_(methods)
    def bstack1l1ll1ll111_opy_(self, instance: bstack1l1ll111lll_opy_, method_name: str, bstack1l1ll11lll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1ll111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1llll1l_opy_, bstack11l111ll111_opy_ = bstack1l1l1lll11l_opy_
        bstack11l111l1l11_opy_ = bstack11ll1l1ll_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        if bstack11l111l1l11_opy_ in bstack11ll1l1ll_opy_.bstack11l111ll1ll_opy_:
            bstack11l111ll11l_opy_ = None
            for callback in bstack11ll1l1ll_opy_.bstack11l111ll1ll_opy_[bstack11l111l1l11_opy_]:
                try:
                    bstack11l111l1ll1_opy_ = callback(self, target, exec, bstack1l1l1lll11l_opy_, result, *args, **kwargs)
                    if bstack11l111ll11l_opy_ == None:
                        bstack11l111ll11l_opy_ = bstack11l111l1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᤂ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᤃ"))
                    traceback.print_exc()
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.PRE and callable(bstack11l111ll11l_opy_):
                return bstack11l111ll11l_opy_
            elif bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST and bstack11l111ll11l_opy_:
                return bstack11l111ll11l_opy_
    def bstack1l1ll1l111l_opy_(
        self, method_name, previous_state: bstack1ll1l1111l_opy_, *args, **kwargs
    ) -> bstack1ll1l1111l_opy_:
        if method_name == bstack111ll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࠭ᤄ") or method_name == bstack111ll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᤅ") or method_name == bstack111ll_opy_ (u"ࠨࡰࡨࡻࡤࡶࡡࡨࡧࠪᤆ"):
            return bstack1ll1l1111l_opy_.bstack111l1ll111_opy_
        if method_name == bstack111ll_opy_ (u"ࠩࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠫᤇ"):
            return bstack1ll1l1111l_opy_.bstack1l1ll1lll11_opy_
        if method_name == bstack111ll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠩᤈ"):
            return bstack1ll1l1111l_opy_.QUIT
        return bstack1ll1l1111l_opy_.NONE
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_]):
        return bstack111ll_opy_ (u"ࠦ࠿ࠨᤉ").join((bstack1ll1l1111l_opy_(bstack1l1l1lll11l_opy_[0]).name, bstack1l1l111lll_opy_(bstack1l1l1lll11l_opy_[1]).name))
    @staticmethod
    def bstack1l111l1111l_opy_(bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_], callback: Callable):
        bstack11l111l1l11_opy_ = bstack11ll1l1ll_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        if not bstack11l111l1l11_opy_ in bstack11ll1l1ll_opy_.bstack11l111ll1ll_opy_:
            bstack11ll1l1ll_opy_.bstack11l111ll1ll_opy_[bstack11l111l1l11_opy_] = []
        bstack11ll1l1ll_opy_.bstack11l111ll1ll_opy_[bstack11l111l1l11_opy_].append(callback)
    @staticmethod
    def bstack1l1111llll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack11lllll111l_opy_(method_name: str, *args) -> bool:
        command_name = bstack11ll1l1ll_opy_.bstack11l11ll1l1l_opy_(*args)
        if command_name in [bstack111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࠴࡮ࡦࡹࠣࡦࡷࡵࡷࡴࡧࡵࠦᤊ"), bstack111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡲࡪࡩࡴࠡࡶࡲࠤࡧࡸ࡯ࡸࡵࡨࡶࠧᤋ")]:
            return True
        return False
    @staticmethod
    def bstack1l1111ll1l1_opy_(instance: bstack1l1ll111lll_opy_, default_value=None):
        return bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll111ll_opy_, default_value)
    @staticmethod
    def bstack11lll1ll11l_opy_(instance: bstack1l1ll111lll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l11111l111_opy_(instance: bstack1l1ll111lll_opy_, default_value=None):
        return bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, default_value)
    @staticmethod
    def bstack1l111l1l1l1_opy_(*args):
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
    def bstack11llll1ll11_opy_(method_name: str, *args):
        if not bstack11ll1l1ll_opy_.bstack1l1111llll1_opy_(method_name):
            return False
        bstack11llll1111l_opy_ = args[0][1]
        if not isinstance(bstack11llll1111l_opy_, dict) or bstack111ll_opy_ (u"ࠧࡢࡴࡪࡷࠬᤌ") not in bstack11llll1111l_opy_:
            return False
        args_list = bstack11llll1111l_opy_.get(bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᤍ"), [])
        return any(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠫᤎ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l1111l1ll1_opy_(method_name: str, *args):
        if not bstack11ll1l1ll_opy_.bstack1l1111llll1_opy_(method_name):
            return False
        bstack11llll1111l_opy_ = args[0][1]
        if not isinstance(bstack11llll1111l_opy_, dict) or bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᤏ") not in bstack11llll1111l_opy_:
            return False
        args_list = bstack11llll1111l_opy_.get(bstack111ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᤐ"), [])
        return any(bstack111ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࠬ࠮࠭ᤑ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11l11ll1l1l_opy_(*args):
        return str(bstack11ll1l1ll_opy_.bstack1l111l1l1l1_opy_(*args)).lower()