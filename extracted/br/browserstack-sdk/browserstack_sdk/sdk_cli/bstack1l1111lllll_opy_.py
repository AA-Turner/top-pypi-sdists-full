# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack1l1l1ll11l_opy_,
    bstack1l1l111l1l1_opy_,
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.constants import EVENTS
class bstack1l11l11l11l_opy_(bstack1l1l1ll11l_opy_):
    bstack111lllll111_opy_ = bstack111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ᭡")
    NAME = bstack111l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧ᭢")
    bstack11l1ll111l_opy_ = bstack111l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧ᭣")
    bstack1ll11111111_opy_ = bstack111l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧ᭤")
    bstack111l1l11111_opy_ = bstack111l_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᭥")
    bstack1111lll1_opy_ = bstack111l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᭦")
    bstack11l11111ll1_opy_ = bstack111l_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢ᭧")
    bstack111l1l11l1l_opy_ = bstack111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᭨")
    bstack111l11llll1_opy_ = bstack111l_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧ᭩")
    bstack1l1l1l11ll1_opy_ = bstack111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧ᭪")
    bstack11l111ll11l_opy_ = bstack111l_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤ᭫")
    bstack111l1l1111l_opy_ = bstack111l_opy_ (u"ࠨࡧࡦࡶ᭬ࠥ")
    bstack11l1llll11l_opy_ = bstack111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᭭")
    bstack111lllll11l_opy_ = bstack111l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦ᭮")
    bstack111llll1l11_opy_ = bstack111l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥ᭯")
    bstack111l1l11l11_opy_ = bstack111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣ᭰")
    bstack111l1l11ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack11l1111llll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l111l11_opy_: Any
    bstack111llllll1l_opy_: Dict
    def __init__(
        self,
        bstack11l1111llll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l11l111l11_opy_: Dict[str, Any],
        methods=[bstack111l_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨ᭱"), bstack111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᭲"), bstack111l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢ᭳"), bstack111l_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ᭴")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l1111llll_opy_ = bstack11l1111llll_opy_
        self.platform_index = platform_index
        self.bstack1l1l111ll11_opy_(methods)
        self.bstack1l11l111l11_opy_ = bstack1l11l111l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1l1l1ll11l_opy_.get_data(bstack1l11l11l11l_opy_.bstack1ll11111111_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1l1l1ll11l_opy_.get_data(bstack1l11l11l11l_opy_.bstack11l1ll111l_opy_, target, strict)
    @staticmethod
    def bstack111l1l111l1_opy_(target: object, strict=True):
        return bstack1l1l1ll11l_opy_.get_data(bstack1l11l11l11l_opy_.bstack111l1l11111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1l1l1ll11l_opy_.get_data(bstack1l11l11l11l_opy_.bstack1111lll1_opy_, target, strict)
    @staticmethod
    def bstack11ll1l11l11_opy_(instance: bstack1l1l111l1l1_opy_) -> bool:
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack11l11111ll1_opy_, False)
    @staticmethod
    def bstack11ll1ll1lll_opy_(instance: bstack1l1l111l1l1_opy_, default_value=None):
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack11l1ll111l_opy_, default_value)
    @staticmethod
    def bstack11lll11111l_opy_(instance: bstack1l1l111l1l1_opy_, default_value=None):
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1111lll1_opy_, default_value)
    @staticmethod
    def bstack11ll1l1lll1_opy_(hub_url: str, bstack111l1l1l11l_opy_=bstack111l_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ᭵")):
        try:
            bstack111l1l11lll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1l11lll_opy_.endswith(bstack111l1l1l11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack11llll111l1_opy_(method_name: str):
        return method_name == bstack111l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᭶")
    @staticmethod
    def bstack11lll1l11l1_opy_(method_name: str, *args):
        return (
            bstack1l11l11l11l_opy_.bstack11llll111l1_opy_(method_name)
            and bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args) == bstack1l11l11l11l_opy_.bstack11l111ll11l_opy_
        )
    @staticmethod
    def bstack11lll111l11_opy_(method_name: str, *args):
        if not bstack1l11l11l11l_opy_.bstack11llll111l1_opy_(method_name):
            return False
        if not bstack1l11l11l11l_opy_.bstack111lllll11l_opy_ in bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args):
            return False
        bstack11ll1l1l1l1_opy_ = bstack1l11l11l11l_opy_.bstack11ll1l1ll11_opy_(*args)
        return bstack11ll1l1l1l1_opy_ and bstack111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᭷") in bstack11ll1l1l1l1_opy_ and bstack111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᭸") in bstack11ll1l1l1l1_opy_[bstack111l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᭹")]
    @staticmethod
    def bstack11lll1l1l1l_opy_(method_name: str, *args):
        if not bstack1l11l11l11l_opy_.bstack11llll111l1_opy_(method_name):
            return False
        if not bstack1l11l11l11l_opy_.bstack111lllll11l_opy_ in bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args):
            return False
        bstack11ll1l1l1l1_opy_ = bstack1l11l11l11l_opy_.bstack11ll1l1ll11_opy_(*args)
        return (
            bstack11ll1l1l1l1_opy_
            and bstack111l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᭺") in bstack11ll1l1l1l1_opy_
            and bstack111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥ᭻") in bstack11ll1l1l1l1_opy_[bstack111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ᭼")]
        )
    @staticmethod
    def bstack11l11l1l11l_opy_(*args):
        return str(bstack1l11l11l11l_opy_.bstack11lll1ll11l_opy_(*args)).lower()
    @staticmethod
    def bstack11lll1ll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11ll1l1ll11_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack111111l111_opy_(driver):
        command_executor = getattr(driver, bstack111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᭽"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack111l_opy_ (u"ࠥࡣࡺࡸ࡬ࠣ᭾"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack111l_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧ᭿"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack111l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᮀ"), None)
        return hub_url
    def bstack11l111l1l1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᮁ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᮂ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack111l_opy_ (u"ࠣࡡࡸࡶࡱࠨᮃ")):
                setattr(command_executor, bstack111l_opy_ (u"ࠤࡢࡹࡷࡲࠢᮄ"), hub_url)
                result = True
        if result:
            self.bstack11l1111llll_opy_ = hub_url
            bstack1l11l11l11l_opy_.bstack1l11l1ll11_opy_(instance, bstack1l11l11l11l_opy_.bstack11l1ll111l_opy_, hub_url)
            bstack1l11l11l11l_opy_.bstack1l11l1ll11_opy_(
                instance, bstack1l11l11l11l_opy_.bstack11l11111ll1_opy_, bstack1l11l11l11l_opy_.bstack11ll1l1lll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_]):
        return bstack111l_opy_ (u"ࠥ࠾ࠧᮅ").join((bstack11l1ll1l1_opy_(bstack1l1l1lllll1_opy_[0]).name, bstack1lll1l11l1_opy_(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack11llll1l1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_], callback: Callable):
        bstack111llllll11_opy_ = bstack1l11l11l11l_opy_.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        if not bstack111llllll11_opy_ in bstack1l11l11l11l_opy_.bstack111l1l11ll1_opy_:
            bstack1l11l11l11l_opy_.bstack111l1l11ll1_opy_[bstack111llllll11_opy_] = []
        bstack1l11l11l11l_opy_.bstack111l1l11ll1_opy_[bstack111llllll11_opy_].append(callback)
    def bstack1l1l11l1111_opy_(self, instance: bstack1l1l111l1l1_opy_, method_name: str, bstack1l1l111lll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack111l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᮆ")):
            return
        cmd = args[0] if method_name == bstack111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᮇ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l11lllll_opy_ = bstack111l_opy_ (u"ࠨ࠺ࠣᮈ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᮉ") + bstack111l11lllll_opy_, bstack1l1l111lll1_opy_)
    def bstack11l11ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1111lll_opy_, bstack111llll11ll_opy_ = bstack1l1l1lllll1_opy_
        bstack111llllll11_opy_ = bstack1l11l11l11l_opy_.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᮊ") + str(kwargs) + bstack111l_opy_ (u"ࠤࠥᮋ"))
        if bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.QUIT:
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.PRE:
                bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1l111ll_opy_.value)
                bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, EVENTS.bstack111l1l111ll_opy_.value, bstack1l1l111lll_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᮌ").format(instance, method_name, bstack1l1l1111lll_opy_, bstack111llll11ll_opy_))
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST:
                bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1l1l111_opy_.value)
                bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, EVENTS.bstack111l1l1l111_opy_.value, bstack1l1l111lll_opy_)
        if bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.bstack11llll111l_opy_:
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST and not bstack1l11l11l11l_opy_.bstack1ll11111111_opy_ in instance.data:
                session_id = getattr(target, bstack111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᮍ"), None)
                if session_id:
                    instance.data[bstack1l11l11l11l_opy_.bstack1ll11111111_opy_] = session_id
        elif (
            bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_
            and bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args) == bstack1l11l11l11l_opy_.bstack11l111ll11l_opy_
        ):
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.PRE:
                hub_url = bstack1l11l11l11l_opy_.bstack111111l111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l11l11l11l_opy_.bstack11l1ll111l_opy_: hub_url,
                            bstack1l11l11l11l_opy_.bstack11l11111ll1_opy_: bstack1l11l11l11l_opy_.bstack11ll1l1lll1_opy_(hub_url),
                            bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_: int(
                                os.environ.get(bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᮎ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11ll1l1l1l1_opy_ = bstack1l11l11l11l_opy_.bstack11ll1l1ll11_opy_(*args)
                bstack111l1l111l1_opy_ = bstack11ll1l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᮏ"), None) if bstack11ll1l1l1l1_opy_ else None
                if isinstance(bstack111l1l111l1_opy_, dict):
                    instance.data[bstack1l11l11l11l_opy_.bstack111l1l11111_opy_] = copy.deepcopy(bstack111l1l111l1_opy_)
                    instance.data[bstack1l11l11l11l_opy_.bstack1111lll1_opy_] = bstack111l1l111l1_opy_
            elif bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack111l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᮐ"), dict()).get(bstack111l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᮑ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l11l11l11l_opy_.bstack1ll11111111_opy_: framework_session_id,
                                bstack1l11l11l11l_opy_.bstack111l1l11l1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_
            and bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args) == bstack1l11l11l11l_opy_.bstack111l1l11l11_opy_
            and bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST
        ):
            instance.data[bstack1l11l11l11l_opy_.bstack111l11llll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack111llllll11_opy_ in bstack1l11l11l11l_opy_.bstack111l1l11ll1_opy_:
            bstack111lllll1ll_opy_ = None
            for callback in bstack1l11l11l11l_opy_.bstack111l1l11ll1_opy_[bstack111llllll11_opy_]:
                try:
                    bstack111lllll1l1_opy_ = callback(self, target, exec, bstack1l1l1lllll1_opy_, result, *args, **kwargs)
                    if bstack111lllll1ll_opy_ == None:
                        bstack111lllll1ll_opy_ = bstack111lllll1l1_opy_
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᮒ") + str(e) + bstack111l_opy_ (u"ࠥࠦᮓ"))
                    traceback.print_exc()
            if bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.QUIT:
                if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.PRE:
                    bstack1l1l111lll_opy_ = bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, EVENTS.bstack111l1l111ll_opy_.value)
                    if bstack1l1l111lll_opy_!=None:
                        bstack11lll11111_opy_.end(EVENTS.bstack111l1l111ll_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᮔ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᮕ"), True, None)
                if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST:
                    bstack1l1l111lll_opy_ = bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, EVENTS.bstack111l1l1l111_opy_.value)
                    if bstack1l1l111lll_opy_!=None:
                        bstack11lll11111_opy_.end(EVENTS.bstack111l1l1l111_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᮖ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᮗ"), True, None)
            if bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.PRE and callable(bstack111lllll1ll_opy_):
                return bstack111lllll1ll_opy_
            elif bstack111llll11ll_opy_ == bstack1lll1l11l1_opy_.POST and bstack111lllll1ll_opy_:
                return bstack111lllll1ll_opy_
    def bstack1l11lll1l11_opy_(
        self, method_name, previous_state: bstack11l1ll1l1_opy_, *args, **kwargs
    ) -> bstack11l1ll1l1_opy_:
        if method_name == bstack111l_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᮘ") or method_name == bstack111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᮙ"):
            return bstack11l1ll1l1_opy_.bstack11llll111l_opy_
        if method_name == bstack111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᮚ"):
            return bstack11l1ll1l1_opy_.QUIT
        if method_name == bstack111l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᮛ"):
            if previous_state != bstack11l1ll1l1_opy_.NONE:
                command_name = bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args)
                if command_name == bstack1l11l11l11l_opy_.bstack11l111ll11l_opy_:
                    return bstack11l1ll1l1_opy_.bstack11llll111l_opy_
            return bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_
        return bstack11l1ll1l1_opy_.NONE