# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llll1lll11_opy_,
    bstack11111111l1_opy_,
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1l1lll11_opy_(bstack1llll1lll11_opy_):
    bstack1l11l11l111_opy_ = bstackl_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᕰ")
    NAME = bstackl_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᕱ")
    bstack1l1l11ll1l1_opy_ = bstackl_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᕲ")
    bstack1l1l11ll1ll_opy_ = bstackl_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᕳ")
    bstack11llll1lll1_opy_ = bstackl_opy_ (u"ࠦ࡮ࡴࡰࡶࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᕴ")
    bstack1l1l11l1l1l_opy_ = bstackl_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᕵ")
    bstack1l11l1ll111_opy_ = bstackl_opy_ (u"ࠨࡩࡴࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡪࡸࡦࠧᕶ")
    bstack11llll1ll11_opy_ = bstackl_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᕷ")
    bstack11llll1l1ll_opy_ = bstackl_opy_ (u"ࠣࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᕸ")
    bstack1ll111ll1l1_opy_ = bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᕹ")
    bstack1l11ll1llll_opy_ = bstackl_opy_ (u"ࠥࡲࡪࡽࡳࡦࡵࡶ࡭ࡴࡴࠢᕺ")
    bstack11llll1l1l1_opy_ = bstackl_opy_ (u"ࠦ࡬࡫ࡴࠣᕻ")
    bstack1l1l1ll11l1_opy_ = bstackl_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᕼ")
    bstack1l11l11l11l_opy_ = bstackl_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᕽ")
    bstack1l11l11l1l1_opy_ = bstackl_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᕾ")
    bstack11llll1l11l_opy_ = bstackl_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᕿ")
    bstack11llll11ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll11l11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1111ll1_opy_: Any
    bstack1l11l11ll1l_opy_: Dict
    def __init__(
        self,
        bstack1l11ll11l11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1111ll1_opy_: Dict[str, Any],
        methods=[bstackl_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᖀ"), bstackl_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᖁ"), bstackl_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᖂ"), bstackl_opy_ (u"ࠧࡷࡵࡪࡶࠥᖃ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll11l11_opy_ = bstack1l11ll11l11_opy_
        self.platform_index = platform_index
        self.bstack1lllllll111_opy_(methods)
        self.bstack1lll1111ll1_opy_ = bstack1lll1111ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llll1lll11_opy_.get_data(bstack1ll1l1lll11_opy_.bstack1l1l11ll1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llll1lll11_opy_.get_data(bstack1ll1l1lll11_opy_.bstack1l1l11ll1l1_opy_, target, strict)
    @staticmethod
    def bstack11llll11lll_opy_(target: object, strict=True):
        return bstack1llll1lll11_opy_.get_data(bstack1ll1l1lll11_opy_.bstack11llll1lll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llll1lll11_opy_.get_data(bstack1ll1l1lll11_opy_.bstack1l1l11l1l1l_opy_, target, strict)
    @staticmethod
    def bstack1l1llll11ll_opy_(instance: bstack11111111l1_opy_) -> bool:
        return bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11l1ll111_opy_, False)
    @staticmethod
    def bstack1ll1l111l11_opy_(instance: bstack11111111l1_opy_, default_value=None):
        return bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l1l11ll1l1_opy_, default_value)
    @staticmethod
    def bstack1ll111l111l_opy_(instance: bstack11111111l1_opy_, default_value=None):
        return bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l1l11l1l1l_opy_, default_value)
    @staticmethod
    def bstack1ll111111l1_opy_(hub_url: str, bstack11llll11l1l_opy_=bstackl_opy_ (u"ࠨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᖄ")):
        try:
            bstack11llll1l111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1l111_opy_.endswith(bstack11llll11l1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll111l1111_opy_(method_name: str):
        return method_name == bstackl_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖅ")
    @staticmethod
    def bstack1ll1111ll1l_opy_(method_name: str, *args):
        return (
            bstack1ll1l1lll11_opy_.bstack1ll111l1111_opy_(method_name)
            and bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args) == bstack1ll1l1lll11_opy_.bstack1l11ll1llll_opy_
        )
    @staticmethod
    def bstack1ll11l1l11l_opy_(method_name: str, *args):
        if not bstack1ll1l1lll11_opy_.bstack1ll111l1111_opy_(method_name):
            return False
        if not bstack1ll1l1lll11_opy_.bstack1l11l11l11l_opy_ in bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args):
            return False
        bstack1ll1111l11l_opy_ = bstack1ll1l1lll11_opy_.bstack1ll1111111l_opy_(*args)
        return bstack1ll1111l11l_opy_ and bstackl_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᖆ") in bstack1ll1111l11l_opy_ and bstackl_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖇ") in bstack1ll1111l11l_opy_[bstackl_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᖈ")]
    @staticmethod
    def bstack1ll1111llll_opy_(method_name: str, *args):
        if not bstack1ll1l1lll11_opy_.bstack1ll111l1111_opy_(method_name):
            return False
        if not bstack1ll1l1lll11_opy_.bstack1l11l11l11l_opy_ in bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args):
            return False
        bstack1ll1111l11l_opy_ = bstack1ll1l1lll11_opy_.bstack1ll1111111l_opy_(*args)
        return (
            bstack1ll1111l11l_opy_
            and bstackl_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᖉ") in bstack1ll1111l11l_opy_
            and bstackl_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᖊ") in bstack1ll1111l11l_opy_[bstackl_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᖋ")]
        )
    @staticmethod
    def bstack1l11llll111_opy_(*args):
        return str(bstack1ll1l1lll11_opy_.bstack1ll11l1ll1l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11l1ll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1111111l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1111l1111_opy_(driver):
        command_executor = getattr(driver, bstackl_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖌ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstackl_opy_ (u"ࠣࡡࡸࡶࡱࠨᖍ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstackl_opy_ (u"ࠤࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠥᖎ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstackl_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡢࡷࡪࡸࡶࡦࡴࡢࡥࡩࡪࡲࠣᖏ"), None)
        return hub_url
    def bstack1l11lll11l1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstackl_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖐ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstackl_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖑ"), hub_url)
                result = True
            elif hasattr(command_executor, bstackl_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᖒ")):
                setattr(command_executor, bstackl_opy_ (u"ࠢࡠࡷࡵࡰࠧᖓ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll11l11_opy_ = hub_url
            bstack1ll1l1lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l1l11ll1l1_opy_, hub_url)
            bstack1ll1l1lll11_opy_.bstack1lllllllll1_opy_(
                instance, bstack1ll1l1lll11_opy_.bstack1l11l1ll111_opy_, bstack1ll1l1lll11_opy_.bstack1ll111111l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l11ll11_opy_(bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_]):
        return bstackl_opy_ (u"ࠣ࠼ࠥᖔ").join((bstack1llllllllll_opy_(bstack1lllll1l1ll_opy_[0]).name, bstack1llllllll1l_opy_(bstack1lllll1l1ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11ll1l_opy_(bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_], callback: Callable):
        bstack1l11l111lll_opy_ = bstack1ll1l1lll11_opy_.bstack1l11l11ll11_opy_(bstack1lllll1l1ll_opy_)
        if not bstack1l11l111lll_opy_ in bstack1ll1l1lll11_opy_.bstack11llll11ll1_opy_:
            bstack1ll1l1lll11_opy_.bstack11llll11ll1_opy_[bstack1l11l111lll_opy_] = []
        bstack1ll1l1lll11_opy_.bstack11llll11ll1_opy_[bstack1l11l111lll_opy_].append(callback)
    def bstack1lllll1l111_opy_(self, instance: bstack11111111l1_opy_, method_name: str, bstack111111111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstackl_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᖕ")):
            return
        cmd = args[0] if method_name == bstackl_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᖖ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1ll1l_opy_ = bstackl_opy_ (u"ࠦ࠿ࠨᖗ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠨᖘ") + bstack11llll1ll1l_opy_, bstack111111111l_opy_)
    def bstack1lllll1ll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1ll1l1_opy_, bstack1l11l11lll1_opy_ = bstack1lllll1l1ll_opy_
        bstack1l11l111lll_opy_ = bstack1ll1l1lll11_opy_.bstack1l11l11ll11_opy_(bstack1lllll1l1ll_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠨ࡯࡯ࡡ࡫ࡳࡴࡱ࠺ࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᖙ") + str(kwargs) + bstackl_opy_ (u"ࠢࠣᖚ"))
        if bstack1llll1ll1l1_opy_ == bstack1llllllllll_opy_.QUIT:
            if bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.PRE:
                bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack11ll11ll11_opy_.value)
                bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, EVENTS.bstack11ll11ll11_opy_.value, bstack1ll11lll11l_opy_)
                self.logger.debug(bstackl_opy_ (u"ࠣ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᖛ").format(instance, method_name, bstack1llll1ll1l1_opy_, bstack1l11l11lll1_opy_))
        if bstack1llll1ll1l1_opy_ == bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_:
            if bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.POST and not bstack1ll1l1lll11_opy_.bstack1l1l11ll1ll_opy_ in instance.data:
                session_id = getattr(target, bstackl_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᖜ"), None)
                if session_id:
                    instance.data[bstack1ll1l1lll11_opy_.bstack1l1l11ll1ll_opy_] = session_id
        elif (
            bstack1llll1ll1l1_opy_ == bstack1llllllllll_opy_.bstack1llllll1l11_opy_
            and bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args) == bstack1ll1l1lll11_opy_.bstack1l11ll1llll_opy_
        ):
            if bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.PRE:
                hub_url = bstack1ll1l1lll11_opy_.bstack1111l1111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1l1lll11_opy_.bstack1l1l11ll1l1_opy_: hub_url,
                            bstack1ll1l1lll11_opy_.bstack1l11l1ll111_opy_: bstack1ll1l1lll11_opy_.bstack1ll111111l1_opy_(hub_url),
                            bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_: int(
                                os.environ.get(bstackl_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᖝ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111l11l_opy_ = bstack1ll1l1lll11_opy_.bstack1ll1111111l_opy_(*args)
                bstack11llll11lll_opy_ = bstack1ll1111l11l_opy_.get(bstackl_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᖞ"), None) if bstack1ll1111l11l_opy_ else None
                if isinstance(bstack11llll11lll_opy_, dict):
                    instance.data[bstack1ll1l1lll11_opy_.bstack11llll1lll1_opy_] = copy.deepcopy(bstack11llll11lll_opy_)
                    instance.data[bstack1ll1l1lll11_opy_.bstack1l1l11l1l1l_opy_] = bstack11llll11lll_opy_
            elif bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstackl_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᖟ"), dict()).get(bstackl_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᖠ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1l1lll11_opy_.bstack1l1l11ll1ll_opy_: framework_session_id,
                                bstack1ll1l1lll11_opy_.bstack11llll1ll11_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1llll1ll1l1_opy_ == bstack1llllllllll_opy_.bstack1llllll1l11_opy_
            and bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args) == bstack1ll1l1lll11_opy_.bstack11llll1l11l_opy_
            and bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.POST
        ):
            instance.data[bstack1ll1l1lll11_opy_.bstack11llll1l1ll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l111lll_opy_ in bstack1ll1l1lll11_opy_.bstack11llll11ll1_opy_:
            bstack1l11l1l1111_opy_ = None
            for callback in bstack1ll1l1lll11_opy_.bstack11llll11ll1_opy_[bstack1l11l111lll_opy_]:
                try:
                    bstack1l11l11llll_opy_ = callback(self, target, exec, bstack1lllll1l1ll_opy_, result, *args, **kwargs)
                    if bstack1l11l1l1111_opy_ == None:
                        bstack1l11l1l1111_opy_ = bstack1l11l11llll_opy_
                except Exception as e:
                    self.logger.error(bstackl_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᖡ") + str(e) + bstackl_opy_ (u"ࠣࠤᖢ"))
                    traceback.print_exc()
            if bstack1llll1ll1l1_opy_ == bstack1llllllllll_opy_.QUIT:
                if bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.POST:
                    bstack1ll11lll11l_opy_ = bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, EVENTS.bstack11ll11ll11_opy_.value)
                    if bstack1ll11lll11l_opy_!=None:
                        bstack1lll11lll1l_opy_.end(EVENTS.bstack11ll11ll11_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᖣ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᖤ"), True, None)
            if bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.PRE and callable(bstack1l11l1l1111_opy_):
                return bstack1l11l1l1111_opy_
            elif bstack1l11l11lll1_opy_ == bstack1llllllll1l_opy_.POST and bstack1l11l1l1111_opy_:
                return bstack1l11l1l1111_opy_
    def bstack1lllll1111l_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        if method_name == bstackl_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᖥ") or method_name == bstackl_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᖦ"):
            return bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_
        if method_name == bstackl_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᖧ"):
            return bstack1llllllllll_opy_.QUIT
        if method_name == bstackl_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᖨ"):
            if previous_state != bstack1llllllllll_opy_.NONE:
                bstack1ll11l1llll_opy_ = bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args)
                if bstack1ll11l1llll_opy_ == bstack1ll1l1lll11_opy_.bstack1l11ll1llll_opy_:
                    return bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_
            return bstack1llllllllll_opy_.bstack1llllll1l11_opy_
        return bstack1llllllllll_opy_.NONE