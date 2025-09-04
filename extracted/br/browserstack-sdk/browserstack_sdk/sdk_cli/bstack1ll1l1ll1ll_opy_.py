# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1llllllll11_opy_,
    bstack1llllllll1l_opy_,
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1l111ll_opy_(bstack1llllllll11_opy_):
    bstack1l11l11l1l1_opy_ = bstack1111l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᕼ")
    NAME = bstack1111l1l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᕽ")
    bstack1l1l111ll11_opy_ = bstack1111l1l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᕾ")
    bstack1l1l111llll_opy_ = bstack1111l1l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᕿ")
    bstack11llll11ll1_opy_ = bstack1111l1l_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᖀ")
    bstack1l1l111ll1l_opy_ = bstack1111l1l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᖁ")
    bstack1l11l1ll111_opy_ = bstack1111l1l_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᖂ")
    bstack11llll11l1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᖃ")
    bstack11llll1l1l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᖄ")
    bstack1ll11l1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᖅ")
    bstack1l11ll1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᖆ")
    bstack11llll111ll_opy_ = bstack1111l1l_opy_ (u"ࠤࡪࡩࡹࠨᖇ")
    bstack1l1lll1ll11_opy_ = bstack1111l1l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᖈ")
    bstack1l11l11l1ll_opy_ = bstack1111l1l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᖉ")
    bstack1l11l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᖊ")
    bstack11llll1l11l_opy_ = bstack1111l1l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᖋ")
    bstack11llll1l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll111ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l1l_opy_: Any
    bstack1l11l11ll1l_opy_: Dict
    def __init__(
        self,
        bstack1l11ll111ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l11l1l_opy_: Dict[str, Any],
        methods=[bstack1111l1l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᖌ"), bstack1111l1l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᖍ"), bstack1111l1l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᖎ"), bstack1111l1l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᖏ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll111ll_opy_ = bstack1l11ll111ll_opy_
        self.platform_index = platform_index
        self.bstack1lllll111ll_opy_(methods)
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllllll11_opy_.get_data(bstack1lll1l111ll_opy_.bstack1l1l111llll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllllll11_opy_.get_data(bstack1lll1l111ll_opy_.bstack1l1l111ll11_opy_, target, strict)
    @staticmethod
    def bstack11llll11l11_opy_(target: object, strict=True):
        return bstack1llllllll11_opy_.get_data(bstack1lll1l111ll_opy_.bstack11llll11ll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllllll11_opy_.get_data(bstack1lll1l111ll_opy_.bstack1l1l111ll1l_opy_, target, strict)
    @staticmethod
    def bstack1l1lllll111_opy_(instance: bstack1llllllll1l_opy_) -> bool:
        return bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l1ll111_opy_, False)
    @staticmethod
    def bstack1ll11l11l1l_opy_(instance: bstack1llllllll1l_opy_, default_value=None):
        return bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l111ll11_opy_, default_value)
    @staticmethod
    def bstack1ll1111l1ll_opy_(instance: bstack1llllllll1l_opy_, default_value=None):
        return bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l111ll1l_opy_, default_value)
    @staticmethod
    def bstack1l1lllllll1_opy_(hub_url: str, bstack11llll111l1_opy_=bstack1111l1l_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᖐ")):
        try:
            bstack11llll11lll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll11lll_opy_.endswith(bstack11llll111l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll111l111l_opy_(method_name: str):
        return method_name == bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᖑ")
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str, *args):
        return (
            bstack1lll1l111ll_opy_.bstack1ll111l111l_opy_(method_name)
            and bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args) == bstack1lll1l111ll_opy_.bstack1l11ll1ll1l_opy_
        )
    @staticmethod
    def bstack1ll1l111ll1_opy_(method_name: str, *args):
        if not bstack1lll1l111ll_opy_.bstack1ll111l111l_opy_(method_name):
            return False
        if not bstack1lll1l111ll_opy_.bstack1l11l11l1ll_opy_ in bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args):
            return False
        bstack1ll1111l111_opy_ = bstack1lll1l111ll_opy_.bstack1ll111111l1_opy_(*args)
        return bstack1ll1111l111_opy_ and bstack1111l1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᖒ") in bstack1ll1111l111_opy_ and bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖓ") in bstack1ll1111l111_opy_[bstack1111l1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᖔ")]
    @staticmethod
    def bstack1ll1l111lll_opy_(method_name: str, *args):
        if not bstack1lll1l111ll_opy_.bstack1ll111l111l_opy_(method_name):
            return False
        if not bstack1lll1l111ll_opy_.bstack1l11l11l1ll_opy_ in bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args):
            return False
        bstack1ll1111l111_opy_ = bstack1lll1l111ll_opy_.bstack1ll111111l1_opy_(*args)
        return (
            bstack1ll1111l111_opy_
            and bstack1111l1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᖕ") in bstack1ll1111l111_opy_
            and bstack1111l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᖖ") in bstack1ll1111l111_opy_[bstack1111l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᖗ")]
        )
    @staticmethod
    def bstack1l11ll111l1_opy_(*args):
        return str(bstack1lll1l111ll_opy_.bstack1ll111llll1_opy_(*args)).lower()
    @staticmethod
    def bstack1ll111llll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111111l1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack111llllll1_opy_(driver):
        command_executor = getattr(driver, bstack1111l1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖘ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1111l1l_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᖙ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1111l1l_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᖚ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1111l1l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᖛ"), None)
        return hub_url
    def bstack1l11ll11lll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1111l1l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᖜ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1111l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖝ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1111l1l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᖞ")):
                setattr(command_executor, bstack1111l1l_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᖟ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll111ll_opy_ = hub_url
            bstack1lll1l111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l111ll11_opy_, hub_url)
            bstack1lll1l111ll_opy_.bstack1lllllllll1_opy_(
                instance, bstack1lll1l111ll_opy_.bstack1l11l1ll111_opy_, bstack1lll1l111ll_opy_.bstack1l1lllllll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_]):
        return bstack1111l1l_opy_ (u"ࠨ࠺ࠣᖠ").join((bstack1lllll11111_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1llll1lllll_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1lll1l111ll_opy_.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l111l11_opy_ in bstack1lll1l111ll_opy_.bstack11llll1l1ll_opy_:
            bstack1lll1l111ll_opy_.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_] = []
        bstack1lll1l111ll_opy_.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_].append(callback)
    def bstack1lllllll1l1_opy_(self, instance: bstack1llllllll1l_opy_, method_name: str, bstack1lllll1l1l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1111l1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᖡ")):
            return
        cmd = args[0] if method_name == bstack1111l1l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᖢ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1l111_opy_ = bstack1111l1l_opy_ (u"ࠤ࠽ࠦᖣ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᖤ") + bstack11llll1l111_opy_, bstack1lllll1l1l1_opy_)
    def bstack1llllll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1llll1_opy_, bstack1l11l111ll1_opy_ = bstack1lllll11ll1_opy_
        bstack1l11l111l11_opy_ = bstack1lll1l111ll_opy_.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᖥ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠧࠨᖦ"))
        if bstack1llll1llll1_opy_ == bstack1lllll11111_opy_.QUIT:
            if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.PRE:
                bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11ll1lll1l_opy_.value)
                bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, EVENTS.bstack11ll1lll1l_opy_.value, bstack1ll111l1ll1_opy_)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᖧ").format(instance, method_name, bstack1llll1llll1_opy_, bstack1l11l111ll1_opy_))
        if bstack1llll1llll1_opy_ == bstack1lllll11111_opy_.bstack1lllll1ll11_opy_:
            if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST and not bstack1lll1l111ll_opy_.bstack1l1l111llll_opy_ in instance.data:
                session_id = getattr(target, bstack1111l1l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᖨ"), None)
                if session_id:
                    instance.data[bstack1lll1l111ll_opy_.bstack1l1l111llll_opy_] = session_id
        elif (
            bstack1llll1llll1_opy_ == bstack1lllll11111_opy_.bstack1llll1lll11_opy_
            and bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args) == bstack1lll1l111ll_opy_.bstack1l11ll1ll1l_opy_
        ):
            if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.PRE:
                hub_url = bstack1lll1l111ll_opy_.bstack111llllll1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1l111ll_opy_.bstack1l1l111ll11_opy_: hub_url,
                            bstack1lll1l111ll_opy_.bstack1l11l1ll111_opy_: bstack1lll1l111ll_opy_.bstack1l1lllllll1_opy_(hub_url),
                            bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_: int(
                                os.environ.get(bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᖩ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111l111_opy_ = bstack1lll1l111ll_opy_.bstack1ll111111l1_opy_(*args)
                bstack11llll11l11_opy_ = bstack1ll1111l111_opy_.get(bstack1111l1l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᖪ"), None) if bstack1ll1111l111_opy_ else None
                if isinstance(bstack11llll11l11_opy_, dict):
                    instance.data[bstack1lll1l111ll_opy_.bstack11llll11ll1_opy_] = copy.deepcopy(bstack11llll11l11_opy_)
                    instance.data[bstack1lll1l111ll_opy_.bstack1l1l111ll1l_opy_] = bstack11llll11l11_opy_
            elif bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1111l1l_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᖫ"), dict()).get(bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᖬ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1l111ll_opy_.bstack1l1l111llll_opy_: framework_session_id,
                                bstack1lll1l111ll_opy_.bstack11llll11l1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1llll1llll1_opy_ == bstack1lllll11111_opy_.bstack1llll1lll11_opy_
            and bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args) == bstack1lll1l111ll_opy_.bstack11llll1l11l_opy_
            and bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST
        ):
            instance.data[bstack1lll1l111ll_opy_.bstack11llll1l1l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l111l11_opy_ in bstack1lll1l111ll_opy_.bstack11llll1l1ll_opy_:
            bstack1l11l111l1l_opy_ = None
            for callback in bstack1lll1l111ll_opy_.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11l11l_opy_ = callback(self, target, exec, bstack1lllll11ll1_opy_, result, *args, **kwargs)
                    if bstack1l11l111l1l_opy_ == None:
                        bstack1l11l111l1l_opy_ = bstack1l11l11l11l_opy_
                except Exception as e:
                    self.logger.error(bstack1111l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᖭ") + str(e) + bstack1111l1l_opy_ (u"ࠨࠢᖮ"))
                    traceback.print_exc()
            if bstack1llll1llll1_opy_ == bstack1lllll11111_opy_.QUIT:
                if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST:
                    bstack1ll111l1ll1_opy_ = bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, EVENTS.bstack11ll1lll1l_opy_.value)
                    if bstack1ll111l1ll1_opy_!=None:
                        bstack1lll11111ll_opy_.end(EVENTS.bstack11ll1lll1l_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᖯ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᖰ"), True, None)
            if bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.PRE and callable(bstack1l11l111l1l_opy_):
                return bstack1l11l111l1l_opy_
            elif bstack1l11l111ll1_opy_ == bstack1llll1lllll_opy_.POST and bstack1l11l111l1l_opy_:
                return bstack1l11l111l1l_opy_
    def bstack1lllll11l11_opy_(
        self, method_name, previous_state: bstack1lllll11111_opy_, *args, **kwargs
    ) -> bstack1lllll11111_opy_:
        if method_name == bstack1111l1l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᖱ") or method_name == bstack1111l1l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᖲ"):
            return bstack1lllll11111_opy_.bstack1lllll1ll11_opy_
        if method_name == bstack1111l1l_opy_ (u"ࠦࡶࡻࡩࡵࠤᖳ"):
            return bstack1lllll11111_opy_.QUIT
        if method_name == bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᖴ"):
            if previous_state != bstack1lllll11111_opy_.NONE:
                command_name = bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args)
                if command_name == bstack1lll1l111ll_opy_.bstack1l11ll1ll1l_opy_:
                    return bstack1lllll11111_opy_.bstack1lllll1ll11_opy_
            return bstack1lllll11111_opy_.bstack1llll1lll11_opy_
        return bstack1lllll11111_opy_.NONE