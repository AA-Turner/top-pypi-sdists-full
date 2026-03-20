# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack1l1lll1111_opy_,
    bstack1ll11llllll_opy_,
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1l1l11ll1l_opy_(bstack1l1lll1111_opy_):
    bstack11ll1111l1l_opy_ = bstack11lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᝪ")
    bstack1ll1ll1ll1l_opy_ = bstack11lll1_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᝫ")
    bstack11l1111lll_opy_ = bstack11lll1_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᝬ")
    bstack1l1l111l11_opy_ = bstack11lll1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᝭")
    bstack11ll111l11l_opy_ = bstack11lll1_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᝮ")
    bstack11ll111l111_opy_ = bstack11lll1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᝯ")
    NAME = bstack11lll1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᝰ")
    bstack11ll111ll1l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1ll11l1l1_opy_: Any
    bstack11ll1111lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11lll1_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤ᝱"), bstack11lll1_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᝲ"), bstack11lll1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᝳ"), bstack11lll1_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦ᝴"), bstack11lll1_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣ᝵")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1ll11ll11l1_opy_(methods)
    def bstack1ll11l1lll1_opy_(self, instance: bstack1ll11llllll_opy_, method_name: str, bstack1ll11ll111l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1ll1ll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11l1111l_opy_, bstack11ll1111ll1_opy_ = bstack1ll1l111111_opy_
        bstack11ll11111ll_opy_ = bstack1l1l11ll1l_opy_.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        if bstack11ll11111ll_opy_ in bstack1l1l11ll1l_opy_.bstack11ll111ll1l_opy_:
            bstack11ll111l1ll_opy_ = None
            for callback in bstack1l1l11ll1l_opy_.bstack11ll111ll1l_opy_[bstack11ll11111ll_opy_]:
                try:
                    bstack11ll111l1l1_opy_ = callback(self, target, exec, bstack1ll1l111111_opy_, result, *args, **kwargs)
                    if bstack11ll111l1ll_opy_ == None:
                        bstack11ll111l1ll_opy_ = bstack11ll111l1l1_opy_
                except Exception as e:
                    self.logger.error(bstack11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧ᝶") + str(e) + bstack11lll1_opy_ (u"ࠣࠤ᝷"))
                    traceback.print_exc()
            if bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.PRE and callable(bstack11ll111l1ll_opy_):
                return bstack11ll111l1ll_opy_
            elif bstack11ll1111ll1_opy_ == bstack11lllll11l_opy_.POST and bstack11ll111l1ll_opy_:
                return bstack11ll111l1ll_opy_
    def bstack1ll1l1111ll_opy_(
        self, method_name, previous_state: bstack111ll1lll1_opy_, *args, **kwargs
    ) -> bstack111ll1lll1_opy_:
        if method_name == bstack11lll1_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩ᝸") or method_name == bstack11lll1_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫ᝹") or method_name == bstack11lll1_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭᝺"):
            return bstack111ll1lll1_opy_.bstack1l1111ll11_opy_
        if method_name == bstack11lll1_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧ᝻"):
            return bstack111ll1lll1_opy_.bstack1ll11llll11_opy_
        if method_name == bstack11lll1_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬ᝼"):
            return bstack111ll1lll1_opy_.QUIT
        return bstack111ll1lll1_opy_.NONE
    @staticmethod
    def bstack11ll1111l11_opy_(bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_]):
        return bstack11lll1_opy_ (u"ࠢ࠻ࠤ᝽").join((bstack111ll1lll1_opy_(bstack1ll1l111111_opy_[0]).name, bstack11lllll11l_opy_(bstack1ll1l111111_opy_[1]).name))
    @staticmethod
    def bstack1l1l111lll1_opy_(bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_], callback: Callable):
        bstack11ll11111ll_opy_ = bstack1l1l11ll1l_opy_.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        if not bstack11ll11111ll_opy_ in bstack1l1l11ll1l_opy_.bstack11ll111ll1l_opy_:
            bstack1l1l11ll1l_opy_.bstack11ll111ll1l_opy_[bstack11ll11111ll_opy_] = []
        bstack1l1l11ll1l_opy_.bstack11ll111ll1l_opy_[bstack11ll11111ll_opy_].append(callback)
    @staticmethod
    def bstack1l11ll1ll11_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1l11lll11l1_opy_(method_name: str, *args) -> bool:
        command_name = bstack1l1l11ll1l_opy_.bstack11ll1ll1l11_opy_(*args)
        if command_name in [bstack11lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠢ᝾"), bstack11lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠣ᝿")]:
            return True
        return False
    @staticmethod
    def bstack1l1l1111lll_opy_(instance: bstack1ll11llllll_opy_, default_value=None):
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1l111l11_opy_, default_value)
    @staticmethod
    def bstack1l11l111l1l_opy_(instance: bstack1ll11llllll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1l1l111ll11_opy_(instance: bstack1ll11llllll_opy_, default_value=None):
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1l1l11ll1l_opy_.bstack11l1111lll_opy_, default_value)
    @staticmethod
    def bstack1l11l1lll11_opy_(*args):
        bstack11ll111ll11_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack11ll111ll11_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack11ll111ll11_opy_ = args[0]
        if not bstack11ll111ll11_opy_:
            return None
        return bstack11ll111ll11_opy_.strip()
    @staticmethod
    def bstack1l11ll1l111_opy_(method_name: str, *args):
        if not bstack1l1l11ll1l_opy_.bstack1l11ll1ll11_opy_(method_name):
            return False
        bstack1l11l1l1l11_opy_ = args[0][1]
        if not isinstance(bstack1l11l1l1l11_opy_, dict) or bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨក") not in bstack1l11l1l1l11_opy_:
            return False
        args_list = bstack1l11l1l1l11_opy_.get(bstack11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩខ"), [])
        return any(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠧគ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack1l11ll11l1l_opy_(method_name: str, *args):
        if not bstack1l1l11ll1l_opy_.bstack1l11ll1ll11_opy_(method_name):
            return False
        bstack1l11l1l1l11_opy_ = args[0][1]
        if not isinstance(bstack1l11l1l1l11_opy_, dict) or bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫឃ") not in bstack1l11l1l1l11_opy_:
            return False
        args_list = bstack1l11l1l1l11_opy_.get(bstack11lll1_opy_ (u"ࠧࡢࡴࡪࡷࠬង"), [])
        return any(bstack11lll1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࠣࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࠨࠪࠩច") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11ll1ll1l11_opy_(*args):
        return str(bstack1l1l11ll1l_opy_.bstack1l11l1lll11_opy_(*args)).lower()