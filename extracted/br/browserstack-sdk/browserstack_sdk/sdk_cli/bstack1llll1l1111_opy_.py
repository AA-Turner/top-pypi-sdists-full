# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack11111111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1l11l11_opy_(bstack11111111ll_opy_):
    bstack1l11l11lll1_opy_ = bstack111l111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᕯ")
    NAME = bstack111l111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᕰ")
    bstack1l1l11l11l1_opy_ = bstack111l111_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᕱ")
    bstack1l1l111lll1_opy_ = bstack111l111_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᕲ")
    bstack11llll1llll_opy_ = bstack111l111_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᕳ")
    bstack1l1l111ll1l_opy_ = bstack111l111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᕴ")
    bstack1l11l1ll111_opy_ = bstack111l111_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᕵ")
    bstack11llll1lll1_opy_ = bstack111l111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᕶ")
    bstack11llll11ll1_opy_ = bstack111l111_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᕷ")
    bstack1ll11l1lll1_opy_ = bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᕸ")
    bstack1l11llll1l1_opy_ = bstack111l111_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᕹ")
    bstack11llll11lll_opy_ = bstack111l111_opy_ (u"ࠥ࡫ࡪࡺࠢᕺ")
    bstack1l1ll11ll1l_opy_ = bstack111l111_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᕻ")
    bstack1l11l11l111_opy_ = bstack111l111_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᕼ")
    bstack1l11l1l1111_opy_ = bstack111l111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᕽ")
    bstack11llll1ll11_opy_ = bstack111l111_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᕾ")
    bstack11llll1ll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1ll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll1l1l1_opy_: Any
    bstack1l11l11ll11_opy_: Dict
    def __init__(
        self,
        bstack1l11ll1ll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1ll1l1l1_opy_: Dict[str, Any],
        methods=[bstack111l111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᕿ"), bstack111l111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᖀ"), bstack111l111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᖁ"), bstack111l111_opy_ (u"ࠦࡶࡻࡩࡵࠤᖂ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll1ll11_opy_ = bstack1l11ll1ll11_opy_
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111111ll_opy_.get_data(bstack1lll1l11l11_opy_.bstack1l1l111lll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111111ll_opy_.get_data(bstack1lll1l11l11_opy_.bstack1l1l11l11l1_opy_, target, strict)
    @staticmethod
    def bstack11llll1l1ll_opy_(target: object, strict=True):
        return bstack11111111ll_opy_.get_data(bstack1lll1l11l11_opy_.bstack11llll1llll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111111ll_opy_.get_data(bstack1lll1l11l11_opy_.bstack1l1l111ll1l_opy_, target, strict)
    @staticmethod
    def bstack1l1llllll1l_opy_(instance: bstack1lllll1ll1l_opy_) -> bool:
        return bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1l11l1ll111_opy_, False)
    @staticmethod
    def bstack1ll1l111lll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1l1l11l11l1_opy_, default_value)
    @staticmethod
    def bstack1ll111ll1ll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1l1l111ll1l_opy_, default_value)
    @staticmethod
    def bstack1ll11111lll_opy_(hub_url: str, bstack11llll1l111_opy_=bstack111l111_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᖃ")):
        try:
            bstack11llll1l1l1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1l1l1_opy_.endswith(bstack11llll1l111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11l1111l_opy_(method_name: str):
        return method_name == bstack111l111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᖄ")
    @staticmethod
    def bstack1ll1l11l11l_opy_(method_name: str, *args):
        return (
            bstack1lll1l11l11_opy_.bstack1ll11l1111l_opy_(method_name)
            and bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args) == bstack1lll1l11l11_opy_.bstack1l11llll1l1_opy_
        )
    @staticmethod
    def bstack1ll111l1111_opy_(method_name: str, *args):
        if not bstack1lll1l11l11_opy_.bstack1ll11l1111l_opy_(method_name):
            return False
        if not bstack1lll1l11l11_opy_.bstack1l11l11l111_opy_ in bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1lll1l11l11_opy_.bstack1ll111111ll_opy_(*args)
        return bstack1ll1111l1ll_opy_ and bstack111l111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᖅ") in bstack1ll1111l1ll_opy_ and bstack111l111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᖆ") in bstack1ll1111l1ll_opy_[bstack111l111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᖇ")]
    @staticmethod
    def bstack1ll11ll1111_opy_(method_name: str, *args):
        if not bstack1lll1l11l11_opy_.bstack1ll11l1111l_opy_(method_name):
            return False
        if not bstack1lll1l11l11_opy_.bstack1l11l11l111_opy_ in bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args):
            return False
        bstack1ll1111l1ll_opy_ = bstack1lll1l11l11_opy_.bstack1ll111111ll_opy_(*args)
        return (
            bstack1ll1111l1ll_opy_
            and bstack111l111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᖈ") in bstack1ll1111l1ll_opy_
            and bstack111l111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᖉ") in bstack1ll1111l1ll_opy_[bstack111l111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᖊ")]
        )
    @staticmethod
    def bstack1l11llll11l_opy_(*args):
        return str(bstack1lll1l11l11_opy_.bstack1ll11llllll_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11llllll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111111ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l11l11ll1_opy_(driver):
        command_executor = getattr(driver, bstack111l111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᖋ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack111l111_opy_ (u"ࠢࡠࡷࡵࡰࠧᖌ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack111l111_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᖍ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack111l111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᖎ"), None)
        return hub_url
    def bstack1l11ll1l111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack111l111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖏ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack111l111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖐ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack111l111_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᖑ")):
                setattr(command_executor, bstack111l111_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᖒ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll1ll11_opy_ = hub_url
            bstack1lll1l11l11_opy_.bstack1111111111_opy_(instance, bstack1lll1l11l11_opy_.bstack1l1l11l11l1_opy_, hub_url)
            bstack1lll1l11l11_opy_.bstack1111111111_opy_(
                instance, bstack1lll1l11l11_opy_.bstack1l11l1ll111_opy_, bstack1lll1l11l11_opy_.bstack1ll11111lll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_]):
        return bstack111l111_opy_ (u"ࠢ࠻ࠤᖓ").join((bstack1lllllll11l_opy_(bstack1llllll111l_opy_[0]).name, bstack1llllll1111_opy_(bstack1llllll111l_opy_[1]).name))
    @staticmethod
    def bstack1ll11l1l11l_opy_(bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l11l1l1_opy_ = bstack1lll1l11l11_opy_.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        if not bstack1l11l11l1l1_opy_ in bstack1lll1l11l11_opy_.bstack11llll1ll1l_opy_:
            bstack1lll1l11l11_opy_.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_] = []
        bstack1lll1l11l11_opy_.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_].append(callback)
    def bstack1llll1ll1l1_opy_(self, instance: bstack1lllll1ll1l_opy_, method_name: str, bstack1lllllll1l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack111l111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᖔ")):
            return
        cmd = args[0] if method_name == bstack111l111_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᖕ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1l11l_opy_ = bstack111l111_opy_ (u"ࠥ࠾ࠧᖖ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᖗ") + bstack11llll1l11l_opy_, bstack1lllllll1l1_opy_)
    def bstack1lllll11l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll1lll1_opy_, bstack1l11l11l11l_opy_ = bstack1llllll111l_opy_
        bstack1l11l11l1l1_opy_ = bstack1lll1l11l11_opy_.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᖘ") + str(kwargs) + bstack111l111_opy_ (u"ࠨࠢᖙ"))
        if bstack1lllll1lll1_opy_ == bstack1lllllll11l_opy_.QUIT:
            if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack11ll1ll11l_opy_.value)
                bstack11111111ll_opy_.bstack1111111111_opy_(instance, EVENTS.bstack11ll1ll11l_opy_.value, bstack1ll11llll11_opy_)
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᖚ").format(instance, method_name, bstack1lllll1lll1_opy_, bstack1l11l11l11l_opy_))
        if bstack1lllll1lll1_opy_ == bstack1lllllll11l_opy_.bstack1lllll11lll_opy_:
            if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST and not bstack1lll1l11l11_opy_.bstack1l1l111lll1_opy_ in instance.data:
                session_id = getattr(target, bstack111l111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᖛ"), None)
                if session_id:
                    instance.data[bstack1lll1l11l11_opy_.bstack1l1l111lll1_opy_] = session_id
        elif (
            bstack1lllll1lll1_opy_ == bstack1lllllll11l_opy_.bstack1llllll11ll_opy_
            and bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args) == bstack1lll1l11l11_opy_.bstack1l11llll1l1_opy_
        ):
            if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.PRE:
                hub_url = bstack1lll1l11l11_opy_.bstack1l11l11ll1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1l11l11_opy_.bstack1l1l11l11l1_opy_: hub_url,
                            bstack1lll1l11l11_opy_.bstack1l11l1ll111_opy_: bstack1lll1l11l11_opy_.bstack1ll11111lll_opy_(hub_url),
                            bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_: int(
                                os.environ.get(bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᖜ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111l1ll_opy_ = bstack1lll1l11l11_opy_.bstack1ll111111ll_opy_(*args)
                bstack11llll1l1ll_opy_ = bstack1ll1111l1ll_opy_.get(bstack111l111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᖝ"), None) if bstack1ll1111l1ll_opy_ else None
                if isinstance(bstack11llll1l1ll_opy_, dict):
                    instance.data[bstack1lll1l11l11_opy_.bstack11llll1llll_opy_] = copy.deepcopy(bstack11llll1l1ll_opy_)
                    instance.data[bstack1lll1l11l11_opy_.bstack1l1l111ll1l_opy_] = bstack11llll1l1ll_opy_
            elif bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack111l111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᖞ"), dict()).get(bstack111l111_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᖟ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1l11l11_opy_.bstack1l1l111lll1_opy_: framework_session_id,
                                bstack1lll1l11l11_opy_.bstack11llll1lll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllll1lll1_opy_ == bstack1lllllll11l_opy_.bstack1llllll11ll_opy_
            and bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args) == bstack1lll1l11l11_opy_.bstack11llll1ll11_opy_
            and bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST
        ):
            instance.data[bstack1lll1l11l11_opy_.bstack11llll11ll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l11l1l1_opy_ in bstack1lll1l11l11_opy_.bstack11llll1ll1l_opy_:
            bstack1l11l11l1ll_opy_ = None
            for callback in bstack1lll1l11l11_opy_.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_]:
                try:
                    bstack1l11l11llll_opy_ = callback(self, target, exec, bstack1llllll111l_opy_, result, *args, **kwargs)
                    if bstack1l11l11l1ll_opy_ == None:
                        bstack1l11l11l1ll_opy_ = bstack1l11l11llll_opy_
                except Exception as e:
                    self.logger.error(bstack111l111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᖠ") + str(e) + bstack111l111_opy_ (u"ࠢࠣᖡ"))
                    traceback.print_exc()
            if bstack1lllll1lll1_opy_ == bstack1lllllll11l_opy_.QUIT:
                if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST:
                    bstack1ll11llll11_opy_ = bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, EVENTS.bstack11ll1ll11l_opy_.value)
                    if bstack1ll11llll11_opy_!=None:
                        bstack1llll1111l1_opy_.end(EVENTS.bstack11ll1ll11l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᖢ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᖣ"), True, None)
            if bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l11l1ll_opy_):
                return bstack1l11l11l1ll_opy_
            elif bstack1l11l11l11l_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l11l1ll_opy_:
                return bstack1l11l11l1ll_opy_
    def bstack1111111l11_opy_(
        self, method_name, previous_state: bstack1lllllll11l_opy_, *args, **kwargs
    ) -> bstack1lllllll11l_opy_:
        if method_name == bstack111l111_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᖤ") or method_name == bstack111l111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᖥ"):
            return bstack1lllllll11l_opy_.bstack1lllll11lll_opy_
        if method_name == bstack111l111_opy_ (u"ࠧࡷࡵࡪࡶࠥᖦ"):
            return bstack1lllllll11l_opy_.QUIT
        if method_name == bstack111l111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᖧ"):
            if previous_state != bstack1lllllll11l_opy_.NONE:
                bstack1ll1l11l111_opy_ = bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args)
                if bstack1ll1l11l111_opy_ == bstack1lll1l11l11_opy_.bstack1l11llll1l1_opy_:
                    return bstack1lllllll11l_opy_.bstack1lllll11lll_opy_
            return bstack1lllllll11l_opy_.bstack1llllll11ll_opy_
        return bstack1lllllll11l_opy_.NONE