# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1llllll1111_opy_,
    bstack1llll1ll111_opy_,
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1l1ll111_opy_(bstack1llllll1111_opy_):
    bstack1l11l11l11l_opy_ = bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᕻ")
    NAME = bstack1ll11ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᕼ")
    bstack1l1l11l1ll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᕽ")
    bstack1l1l111l111_opy_ = bstack1ll11ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᕾ")
    bstack11llll111ll_opy_ = bstack1ll11ll_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᕿ")
    bstack1l1l11ll111_opy_ = bstack1ll11ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᖀ")
    bstack1l11l1l1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᖁ")
    bstack11llll111l1_opy_ = bstack1ll11ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᖂ")
    bstack11llll1111l_opy_ = bstack1ll11ll_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᖃ")
    bstack1ll1111lll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᖄ")
    bstack1l11lll1l11_opy_ = bstack1ll11ll_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᖅ")
    bstack11llll11lll_opy_ = bstack1ll11ll_opy_ (u"ࠣࡩࡨࡸࠧᖆ")
    bstack1l1ll111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᖇ")
    bstack1l11l11l111_opy_ = bstack1ll11ll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᖈ")
    bstack1l11l111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᖉ")
    bstack11llll1l111_opy_ = bstack1ll11ll_opy_ (u"ࠧࡷࡵࡪࡶࠥᖊ")
    bstack11llll11ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1l1l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1111l1l_opy_: Any
    bstack1l11l1111ll_opy_: Dict
    def __init__(
        self,
        bstack1l11ll1l1l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1111l1l_opy_: Dict[str, Any],
        methods=[bstack1ll11ll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᖋ"), bstack1ll11ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᖌ"), bstack1ll11ll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᖍ"), bstack1ll11ll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᖎ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll1l1l1_opy_ = bstack1l11ll1l1l1_opy_
        self.platform_index = platform_index
        self.bstack1lllll11l11_opy_(methods)
        self.bstack1lll1111l1l_opy_ = bstack1lll1111l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1l1ll111_opy_.bstack1l1l111l111_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1l1ll111_opy_.bstack1l1l11l1ll1_opy_, target, strict)
    @staticmethod
    def bstack11llll11l11_opy_(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1l1ll111_opy_.bstack11llll111ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1l1ll111_opy_.bstack1l1l11ll111_opy_, target, strict)
    @staticmethod
    def bstack1l1llll11ll_opy_(instance: bstack1llll1ll111_opy_) -> bool:
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1l11l1l1l1l_opy_, False)
    @staticmethod
    def bstack1ll11ll1111_opy_(instance: bstack1llll1ll111_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1l1l11l1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll11ll11ll_opy_(instance: bstack1llll1ll111_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1l1l11ll111_opy_, default_value)
    @staticmethod
    def bstack1l1lllllll1_opy_(hub_url: str, bstack11llll11l1l_opy_=bstack1ll11ll_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᖏ")):
        try:
            bstack11llll1l1l1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1l1l1_opy_.endswith(bstack11llll11l1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str):
        return method_name == bstack1ll11ll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᖐ")
    @staticmethod
    def bstack1ll111lll11_opy_(method_name: str, *args):
        return (
            bstack1ll1l1ll111_opy_.bstack1ll11ll1l1l_opy_(method_name)
            and bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args) == bstack1ll1l1ll111_opy_.bstack1l11lll1l11_opy_
        )
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str, *args):
        if not bstack1ll1l1ll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
            return False
        if not bstack1ll1l1ll111_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args):
            return False
        bstack1ll11111lll_opy_ = bstack1ll1l1ll111_opy_.bstack1ll11111l11_opy_(*args)
        return bstack1ll11111lll_opy_ and bstack1ll11ll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᖑ") in bstack1ll11111lll_opy_ and bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖒ") in bstack1ll11111lll_opy_[bstack1ll11ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᖓ")]
    @staticmethod
    def bstack1ll1111l1ll_opy_(method_name: str, *args):
        if not bstack1ll1l1ll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
            return False
        if not bstack1ll1l1ll111_opy_.bstack1l11l11l111_opy_ in bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args):
            return False
        bstack1ll11111lll_opy_ = bstack1ll1l1ll111_opy_.bstack1ll11111l11_opy_(*args)
        return (
            bstack1ll11111lll_opy_
            and bstack1ll11ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᖔ") in bstack1ll11111lll_opy_
            and bstack1ll11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᖕ") in bstack1ll11111lll_opy_[bstack1ll11ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᖖ")]
        )
    @staticmethod
    def bstack1l11ll111ll_opy_(*args):
        return str(bstack1ll1l1ll111_opy_.bstack1ll111ll1l1_opy_(*args)).lower()
    @staticmethod
    def bstack1ll111ll1l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11111l11_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11lll111l1_opy_(driver):
        command_executor = getattr(driver, bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖗ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll11ll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᖘ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll11ll_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢᖙ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll11ll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧᖚ"), None)
        return hub_url
    def bstack1l11l1llll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll11ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᖛ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll11ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᖜ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll11ll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᖝ")):
                setattr(command_executor, bstack1ll11ll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᖞ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll1l1l1_opy_ = hub_url
            bstack1ll1l1ll111_opy_.bstack1llll1l1lll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1l1l11l1ll1_opy_, hub_url)
            bstack1ll1l1ll111_opy_.bstack1llll1l1lll_opy_(
                instance, bstack1ll1l1ll111_opy_.bstack1l11l1l1l1l_opy_, bstack1ll1l1ll111_opy_.bstack1l1lllllll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_]):
        return bstack1ll11ll_opy_ (u"ࠧࡀࠢᖟ").join((bstack1lllll1l111_opy_(bstack1llll1ll1l1_opy_[0]).name, bstack1lllll111ll_opy_(bstack1llll1ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = bstack1ll1l1ll111_opy_.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        if not bstack1l11l111l11_opy_ in bstack1ll1l1ll111_opy_.bstack11llll11ll1_opy_:
            bstack1ll1l1ll111_opy_.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_] = []
        bstack1ll1l1ll111_opy_.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_].append(callback)
    def bstack1lllllll1ll_opy_(self, instance: bstack1llll1ll111_opy_, method_name: str, bstack1lllll11111_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll11ll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᖠ")):
            return
        cmd = args[0] if method_name == bstack1ll11ll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖡ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠣ࠼ࠥᖢ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥᖣ") + bstack11llll1l11l_opy_, bstack1lllll11111_opy_)
    def bstack1llll1ll11l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll111l1_opy_, bstack1l11l11l1l1_opy_ = bstack1llll1ll1l1_opy_
        bstack1l11l111l11_opy_ = bstack1ll1l1ll111_opy_.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᖤ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠦࠧᖥ"))
        if bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.QUIT:
            if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.PRE:
                bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack11l1l11l1l_opy_.value)
                bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, EVENTS.bstack11l1l11l1l_opy_.value, bstack1ll111ll1ll_opy_)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᖦ").format(instance, method_name, bstack1lllll111l1_opy_, bstack1l11l11l1l1_opy_))
        if bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_:
            if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST and not bstack1ll1l1ll111_opy_.bstack1l1l111l111_opy_ in instance.data:
                session_id = getattr(target, bstack1ll11ll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᖧ"), None)
                if session_id:
                    instance.data[bstack1ll1l1ll111_opy_.bstack1l1l111l111_opy_] = session_id
        elif (
            bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.bstack1llllllllll_opy_
            and bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args) == bstack1ll1l1ll111_opy_.bstack1l11lll1l11_opy_
        ):
            if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.PRE:
                hub_url = bstack1ll1l1ll111_opy_.bstack11lll111l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1l1ll111_opy_.bstack1l1l11l1ll1_opy_: hub_url,
                            bstack1ll1l1ll111_opy_.bstack1l11l1l1l1l_opy_: bstack1ll1l1ll111_opy_.bstack1l1lllllll1_opy_(hub_url),
                            bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_: int(
                                os.environ.get(bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᖨ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11111lll_opy_ = bstack1ll1l1ll111_opy_.bstack1ll11111l11_opy_(*args)
                bstack11llll11l11_opy_ = bstack1ll11111lll_opy_.get(bstack1ll11ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᖩ"), None) if bstack1ll11111lll_opy_ else None
                if isinstance(bstack11llll11l11_opy_, dict):
                    instance.data[bstack1ll1l1ll111_opy_.bstack11llll111ll_opy_] = copy.deepcopy(bstack11llll11l11_opy_)
                    instance.data[bstack1ll1l1ll111_opy_.bstack1l1l11ll111_opy_] = bstack11llll11l11_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll11ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᖪ"), dict()).get(bstack1ll11ll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᖫ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1l1ll111_opy_.bstack1l1l111l111_opy_: framework_session_id,
                                bstack1ll1l1ll111_opy_.bstack11llll111l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.bstack1llllllllll_opy_
            and bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args) == bstack1ll1l1ll111_opy_.bstack11llll1l111_opy_
            and bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST
        ):
            instance.data[bstack1ll1l1ll111_opy_.bstack11llll1111l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l111l11_opy_ in bstack1ll1l1ll111_opy_.bstack11llll11ll1_opy_:
            bstack1l11l111lll_opy_ = None
            for callback in bstack1ll1l1ll111_opy_.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_]:
                try:
                    bstack1l11l11l1ll_opy_ = callback(self, target, exec, bstack1llll1ll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11l111lll_opy_ == None:
                        bstack1l11l111lll_opy_ = bstack1l11l11l1ll_opy_
                except Exception as e:
                    self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᖬ") + str(e) + bstack1ll11ll_opy_ (u"ࠧࠨᖭ"))
                    traceback.print_exc()
            if bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.QUIT:
                if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST:
                    bstack1ll111ll1ll_opy_ = bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, EVENTS.bstack11l1l11l1l_opy_.value)
                    if bstack1ll111ll1ll_opy_!=None:
                        bstack1ll1ll11ll1_opy_.end(EVENTS.bstack11l1l11l1l_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖮ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖯ"), True, None)
            if bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.PRE and callable(bstack1l11l111lll_opy_):
                return bstack1l11l111lll_opy_
            elif bstack1l11l11l1l1_opy_ == bstack1lllll111ll_opy_.POST and bstack1l11l111lll_opy_:
                return bstack1l11l111lll_opy_
    def bstack1lllll11ll1_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1ll11ll_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᖰ") or method_name == bstack1ll11ll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᖱ"):
            return bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_
        if method_name == bstack1ll11ll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᖲ"):
            return bstack1lllll1l111_opy_.QUIT
        if method_name == bstack1ll11ll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᖳ"):
            if previous_state != bstack1lllll1l111_opy_.NONE:
                command_name = bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args)
                if command_name == bstack1ll1l1ll111_opy_.bstack1l11lll1l11_opy_:
                    return bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_
            return bstack1lllll1l111_opy_.bstack1llllllllll_opy_
        return bstack1lllll1l111_opy_.NONE