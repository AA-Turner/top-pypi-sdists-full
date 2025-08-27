# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack11111111l1_opy_,
    bstack1lllll1ll11_opy_,
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1lll11l_opy_(bstack11111111l1_opy_):
    bstack1l11l11llll_opy_ = bstack1111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᕷ")
    NAME = bstack1111lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᕸ")
    bstack1l1l11l1l1l_opy_ = bstack1111lll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᕹ")
    bstack1l1l11ll1l1_opy_ = bstack1111lll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᕺ")
    bstack11llll1l1ll_opy_ = bstack1111lll_opy_ (u"ࠦ࡮ࡴࡰࡶࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᕻ")
    bstack1l1l11llll1_opy_ = bstack1111lll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᕼ")
    bstack1l11l1l1ll1_opy_ = bstack1111lll_opy_ (u"ࠨࡩࡴࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡪࡸࡦࠧᕽ")
    bstack11llll1l1l1_opy_ = bstack1111lll_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᕾ")
    bstack11llll1lll1_opy_ = bstack1111lll_opy_ (u"ࠣࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᕿ")
    bstack1ll11l1ll11_opy_ = bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᖀ")
    bstack1l11lll111l_opy_ = bstack1111lll_opy_ (u"ࠥࡲࡪࡽࡳࡦࡵࡶ࡭ࡴࡴࠢᖁ")
    bstack11llll11lll_opy_ = bstack1111lll_opy_ (u"ࠦ࡬࡫ࡴࠣᖂ")
    bstack1l1ll1111ll_opy_ = bstack1111lll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᖃ")
    bstack1l11l11l1l1_opy_ = bstack1111lll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᖄ")
    bstack1l11l11ll11_opy_ = bstack1111lll_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᖅ")
    bstack11lllll1111_opy_ = bstack1111lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᖆ")
    bstack11llll1llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll11111_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l111l1_opy_: Any
    bstack1l11l1l1111_opy_: Dict
    def __init__(
        self,
        bstack1l11ll11111_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l111l1_opy_: Dict[str, Any],
        methods=[bstack1111lll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᖇ"), bstack1111lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᖈ"), bstack1111lll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᖉ"), bstack1111lll_opy_ (u"ࠧࡷࡵࡪࡶࠥᖊ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll11111_opy_ = bstack1l11ll11111_opy_
        self.platform_index = platform_index
        self.bstack1lllll1l1l1_opy_(methods)
        self.bstack1lll1l111l1_opy_ = bstack1lll1l111l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111111l1_opy_.get_data(bstack1lll1lll11l_opy_.bstack1l1l11ll1l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111111l1_opy_.get_data(bstack1lll1lll11l_opy_.bstack1l1l11l1l1l_opy_, target, strict)
    @staticmethod
    def bstack11llll1ll1l_opy_(target: object, strict=True):
        return bstack11111111l1_opy_.get_data(bstack1lll1lll11l_opy_.bstack11llll1l1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111111l1_opy_.get_data(bstack1lll1lll11l_opy_.bstack1l1l11llll1_opy_, target, strict)
    @staticmethod
    def bstack1l1lllll11l_opy_(instance: bstack1lllll1ll11_opy_) -> bool:
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1lll1lll11l_opy_.bstack1l11l1l1ll1_opy_, False)
    @staticmethod
    def bstack1ll11l11111_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1l11l1l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1l1l_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1l11llll1_opy_, default_value)
    @staticmethod
    def bstack1ll1111ll1l_opy_(hub_url: str, bstack11llll1l111_opy_=bstack1111lll_opy_ (u"ࠨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᖋ")):
        try:
            bstack11llll1ll11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1ll11_opy_.endswith(bstack11llll1l111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11llllll_opy_(method_name: str):
        return method_name == bstack1111lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖌ")
    @staticmethod
    def bstack1ll11ll1l11_opy_(method_name: str, *args):
        return (
            bstack1lll1lll11l_opy_.bstack1ll11llllll_opy_(method_name)
            and bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args) == bstack1lll1lll11l_opy_.bstack1l11lll111l_opy_
        )
    @staticmethod
    def bstack1ll11lllll1_opy_(method_name: str, *args):
        if not bstack1lll1lll11l_opy_.bstack1ll11llllll_opy_(method_name):
            return False
        if not bstack1lll1lll11l_opy_.bstack1l11l11l1l1_opy_ in bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args):
            return False
        bstack1ll111111ll_opy_ = bstack1lll1lll11l_opy_.bstack1ll1111l1ll_opy_(*args)
        return bstack1ll111111ll_opy_ and bstack1111lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᖍ") in bstack1ll111111ll_opy_ and bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖎ") in bstack1ll111111ll_opy_[bstack1111lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᖏ")]
    @staticmethod
    def bstack1ll111l11l1_opy_(method_name: str, *args):
        if not bstack1lll1lll11l_opy_.bstack1ll11llllll_opy_(method_name):
            return False
        if not bstack1lll1lll11l_opy_.bstack1l11l11l1l1_opy_ in bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args):
            return False
        bstack1ll111111ll_opy_ = bstack1lll1lll11l_opy_.bstack1ll1111l1ll_opy_(*args)
        return (
            bstack1ll111111ll_opy_
            and bstack1111lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᖐ") in bstack1ll111111ll_opy_
            and bstack1111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᖑ") in bstack1ll111111ll_opy_[bstack1111lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᖒ")]
        )
    @staticmethod
    def bstack1l11lll1l1l_opy_(*args):
        return str(bstack1lll1lll11l_opy_.bstack1ll11lll11l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11lll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1111l1ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11ll11llll_opy_(driver):
        command_executor = getattr(driver, bstack1111lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖓ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1111lll_opy_ (u"ࠣࡡࡸࡶࡱࠨᖔ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1111lll_opy_ (u"ࠤࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠥᖕ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1111lll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡢࡷࡪࡸࡶࡦࡴࡢࡥࡩࡪࡲࠣᖖ"), None)
        return hub_url
    def bstack1l11llll11l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1111lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖗ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1111lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖘ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1111lll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᖙ")):
                setattr(command_executor, bstack1111lll_opy_ (u"ࠢࡠࡷࡵࡰࠧᖚ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll11111_opy_ = hub_url
            bstack1lll1lll11l_opy_.bstack1llllll1l1l_opy_(instance, bstack1lll1lll11l_opy_.bstack1l1l11l1l1l_opy_, hub_url)
            bstack1lll1lll11l_opy_.bstack1llllll1l1l_opy_(
                instance, bstack1lll1lll11l_opy_.bstack1l11l1l1ll1_opy_, bstack1lll1lll11l_opy_.bstack1ll1111ll1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_]):
        return bstack1111lll_opy_ (u"ࠣ࠼ࠥᖛ").join((bstack1lllll1lll1_opy_(bstack1llllll11ll_opy_[0]).name, bstack1llllll1111_opy_(bstack1llllll11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll11l111l1_opy_(bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l11l11l_opy_ = bstack1lll1lll11l_opy_.bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_)
        if not bstack1l11l11l11l_opy_ in bstack1lll1lll11l_opy_.bstack11llll1llll_opy_:
            bstack1lll1lll11l_opy_.bstack11llll1llll_opy_[bstack1l11l11l11l_opy_] = []
        bstack1lll1lll11l_opy_.bstack11llll1llll_opy_[bstack1l11l11l11l_opy_].append(callback)
    def bstack1111111111_opy_(self, instance: bstack1lllll1ll11_opy_, method_name: str, bstack1llll1lllll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1111lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᖜ")):
            return
        cmd = args[0] if method_name == bstack1111lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᖝ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1l11l_opy_ = bstack1111lll_opy_ (u"ࠦ࠿ࠨᖞ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠨᖟ") + bstack11llll1l11l_opy_, bstack1llll1lllll_opy_)
    def bstack1llllll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1ll111_opy_, bstack1l11l1l11l1_opy_ = bstack1llllll11ll_opy_
        bstack1l11l11l11l_opy_ = bstack1lll1lll11l_opy_.bstack1l11l11lll1_opy_(bstack1llllll11ll_opy_)
        self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡯࡯ࡡ࡫ࡳࡴࡱ࠺ࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᖠ") + str(kwargs) + bstack1111lll_opy_ (u"ࠢࠣᖡ"))
        if bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.QUIT:
            if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.PRE:
                bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack1ll111llll1_opy_(EVENTS.bstack111l1ll1l_opy_.value)
                bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, EVENTS.bstack111l1ll1l_opy_.value, bstack1ll11l1l11l_opy_)
                self.logger.debug(bstack1111lll_opy_ (u"ࠣ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᖢ").format(instance, method_name, bstack1llll1ll111_opy_, bstack1l11l1l11l1_opy_))
        if bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_:
            if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST and not bstack1lll1lll11l_opy_.bstack1l1l11ll1l1_opy_ in instance.data:
                session_id = getattr(target, bstack1111lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᖣ"), None)
                if session_id:
                    instance.data[bstack1lll1lll11l_opy_.bstack1l1l11ll1l1_opy_] = session_id
        elif (
            bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_
            and bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args) == bstack1lll1lll11l_opy_.bstack1l11lll111l_opy_
        ):
            if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.PRE:
                hub_url = bstack1lll1lll11l_opy_.bstack11ll11llll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1lll11l_opy_.bstack1l1l11l1l1l_opy_: hub_url,
                            bstack1lll1lll11l_opy_.bstack1l11l1l1ll1_opy_: bstack1lll1lll11l_opy_.bstack1ll1111ll1l_opy_(hub_url),
                            bstack1lll1lll11l_opy_.bstack1ll11l1ll11_opy_: int(
                                os.environ.get(bstack1111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᖤ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll111111ll_opy_ = bstack1lll1lll11l_opy_.bstack1ll1111l1ll_opy_(*args)
                bstack11llll1ll1l_opy_ = bstack1ll111111ll_opy_.get(bstack1111lll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᖥ"), None) if bstack1ll111111ll_opy_ else None
                if isinstance(bstack11llll1ll1l_opy_, dict):
                    instance.data[bstack1lll1lll11l_opy_.bstack11llll1l1ll_opy_] = copy.deepcopy(bstack11llll1ll1l_opy_)
                    instance.data[bstack1lll1lll11l_opy_.bstack1l1l11llll1_opy_] = bstack11llll1ll1l_opy_
            elif bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1111lll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᖦ"), dict()).get(bstack1111lll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᖧ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1lll11l_opy_.bstack1l1l11ll1l1_opy_: framework_session_id,
                                bstack1lll1lll11l_opy_.bstack11llll1l1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_
            and bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args) == bstack1lll1lll11l_opy_.bstack11lllll1111_opy_
            and bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST
        ):
            instance.data[bstack1lll1lll11l_opy_.bstack11llll1lll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l11l11l_opy_ in bstack1lll1lll11l_opy_.bstack11llll1llll_opy_:
            bstack1l11l1l111l_opy_ = None
            for callback in bstack1lll1lll11l_opy_.bstack11llll1llll_opy_[bstack1l11l11l11l_opy_]:
                try:
                    bstack1l11l11ll1l_opy_ = callback(self, target, exec, bstack1llllll11ll_opy_, result, *args, **kwargs)
                    if bstack1l11l1l111l_opy_ == None:
                        bstack1l11l1l111l_opy_ = bstack1l11l11ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack1111lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᖨ") + str(e) + bstack1111lll_opy_ (u"ࠣࠤᖩ"))
                    traceback.print_exc()
            if bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.QUIT:
                if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST:
                    bstack1ll11l1l11l_opy_ = bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, EVENTS.bstack111l1ll1l_opy_.value)
                    if bstack1ll11l1l11l_opy_!=None:
                        bstack1ll1llll11l_opy_.end(EVENTS.bstack111l1ll1l_opy_.value, bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᖪ"), bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᖫ"), True, None)
            if bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l1l111l_opy_):
                return bstack1l11l1l111l_opy_
            elif bstack1l11l1l11l1_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l1l111l_opy_:
                return bstack1l11l1l111l_opy_
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1lllll1lll1_opy_, *args, **kwargs
    ) -> bstack1lllll1lll1_opy_:
        if method_name == bstack1111lll_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᖬ") or method_name == bstack1111lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᖭ"):
            return bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_
        if method_name == bstack1111lll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᖮ"):
            return bstack1lllll1lll1_opy_.QUIT
        if method_name == bstack1111lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖯ"):
            if previous_state != bstack1lllll1lll1_opy_.NONE:
                command_name = bstack1lll1lll11l_opy_.bstack1l11lll1l1l_opy_(*args)
                if command_name == bstack1lll1lll11l_opy_.bstack1l11lll111l_opy_:
                    return bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_
            return bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_
        return bstack1lllll1lll1_opy_.NONE