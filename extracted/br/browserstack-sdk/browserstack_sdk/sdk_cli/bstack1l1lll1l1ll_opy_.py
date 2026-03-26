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
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll111l1111_opy_(bstack11ll11l1_opy_):
    bstack11ll111111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᦉ")
    NAME = bstack1ll1lll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᦊ")
    bstack1lll111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᦋ")
    bstack1ll1ll111ll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᦌ")
    bstack11l1111l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᦍ")
    bstack11l11l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᦎ")
    bstack11ll111l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᦏ")
    bstack11l111l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᦐ")
    bstack11l111l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᦑ")
    bstack1l11l1ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᦒ")
    bstack11ll11l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᦓ")
    bstack11l1111l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺࠢᦔ")
    bstack1l1111l1111_opy_ = bstack1ll1lll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᦕ")
    bstack11l1llllll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᦖ")
    bstack11l1llll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᦗ")
    bstack11l1111ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᦘ")
    bstack11l1111llll_opy_: Dict[str, List[Callable]] = dict()
    bstack11ll1ll11ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l1ll1ll1_opy_: Any
    bstack11l1lllll1l_opy_: Dict
    def __init__(
        self,
        bstack11ll1ll11ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1l1ll1ll1_opy_: Dict[str, Any],
        methods=[bstack1ll1lll_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᦙ"), bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᦚ"), bstack1ll1lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᦛ"), bstack1ll1lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᦜ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11ll1ll11ll_opy_ = bstack11ll1ll11ll_opy_
        self.platform_index = platform_index
        self.bstack1ll111lll1l_opy_(methods)
        self.bstack1l1l1ll1ll1_opy_ = bstack1l1l1ll1ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11ll11l1_opy_.get_data(bstack1ll111l1111_opy_.bstack1ll1ll111ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11ll11l1_opy_.get_data(bstack1ll111l1111_opy_.bstack1lll111l_opy_, target, strict)
    @staticmethod
    def bstack11l111l111l_opy_(target: object, strict=True):
        return bstack11ll11l1_opy_.get_data(bstack1ll111l1111_opy_.bstack11l1111l1l1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11ll11l1_opy_.get_data(bstack1ll111l1111_opy_.bstack11l11l11_opy_, target, strict)
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1ll11ll1l11_opy_) -> bool:
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack11ll111l1ll_opy_, False)
    @staticmethod
    def bstack1l1l11l1111_opy_(instance: bstack1ll11ll1l11_opy_, default_value=None):
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1lll111l_opy_, default_value)
    @staticmethod
    def bstack1l11lll1lll_opy_(instance: bstack1ll11ll1l11_opy_, default_value=None):
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack11l11l11_opy_, default_value)
    @staticmethod
    def bstack1l11l11l1ll_opy_(hub_url: str, bstack11l1111lll1_opy_=bstack1ll1lll_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᦝ")):
        try:
            bstack11l111l11ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l111l11ll_opy_.endswith(bstack11l1111lll1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l11111ll_opy_(method_name: str):
        return method_name == bstack1ll1lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᦞ")
    @staticmethod
    def bstack1l11l1l11l1_opy_(method_name: str, *args):
        return (
            bstack1ll111l1111_opy_.bstack1l1l11111ll_opy_(method_name)
            and bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args) == bstack1ll111l1111_opy_.bstack11ll11l1l11_opy_
        )
    @staticmethod
    def bstack1l11l11llll_opy_(method_name: str, *args):
        if not bstack1ll111l1111_opy_.bstack1l1l11111ll_opy_(method_name):
            return False
        if not bstack1ll111l1111_opy_.bstack11l1llllll1_opy_ in bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args):
            return False
        bstack1l11l111l1l_opy_ = bstack1ll111l1111_opy_.bstack1l11l11l11l_opy_(*args)
        return bstack1l11l111l1l_opy_ and bstack1ll1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᦟ") in bstack1l11l111l1l_opy_ and bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᦠ") in bstack1l11l111l1l_opy_[bstack1ll1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᦡ")]
    @staticmethod
    def bstack1l1l11111l1_opy_(method_name: str, *args):
        if not bstack1ll111l1111_opy_.bstack1l1l11111ll_opy_(method_name):
            return False
        if not bstack1ll111l1111_opy_.bstack11l1llllll1_opy_ in bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args):
            return False
        bstack1l11l111l1l_opy_ = bstack1ll111l1111_opy_.bstack1l11l11l11l_opy_(*args)
        return (
            bstack1l11l111l1l_opy_
            and bstack1ll1lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᦢ") in bstack1l11l111l1l_opy_
            and bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᦣ") in bstack1l11l111l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᦤ")]
        )
    @staticmethod
    def bstack11ll11l11ll_opy_(*args):
        return str(bstack1ll111l1111_opy_.bstack1l11llll11l_opy_(*args)).lower()
    @staticmethod
    def bstack1l11llll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11l11l11l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11llll1l1l_opy_(driver):
        command_executor = getattr(driver, bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᦥ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll1lll_opy_ (u"ࠢࡠࡷࡵࡰࠧᦦ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll1lll_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᦧ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll1lll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᦨ"), None)
        return hub_url
    def bstack11ll11l1l1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᦩ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᦪ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll1lll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᦫ")):
                setattr(command_executor, bstack1ll1lll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦ᦬"), hub_url)
                result = True
        if result:
            self.bstack11ll1ll11ll_opy_ = hub_url
            bstack1ll111l1111_opy_.bstack1lll1111ll_opy_(instance, bstack1ll111l1111_opy_.bstack1lll111l_opy_, hub_url)
            bstack1ll111l1111_opy_.bstack1lll1111ll_opy_(
                instance, bstack1ll111l1111_opy_.bstack11ll111l1ll_opy_, bstack1ll111l1111_opy_.bstack1l11l11l1ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_]):
        return bstack1ll1lll_opy_ (u"ࠢ࠻ࠤ᦭").join((bstack11lll111_opy_(bstack1ll11l1l111_opy_[0]).name, bstack1l11l11l1_opy_(bstack1ll11l1l111_opy_[1]).name))
    @staticmethod
    def bstack1l11ll11111_opy_(bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_], callback: Callable):
        bstack11l1llll111_opy_ = bstack1ll111l1111_opy_.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        if not bstack11l1llll111_opy_ in bstack1ll111l1111_opy_.bstack11l1111llll_opy_:
            bstack1ll111l1111_opy_.bstack11l1111llll_opy_[bstack11l1llll111_opy_] = []
        bstack1ll111l1111_opy_.bstack11l1111llll_opy_[bstack11l1llll111_opy_].append(callback)
    def bstack1ll11l11l11_opy_(self, instance: bstack1ll11ll1l11_opy_, method_name: str, bstack1ll111ll1l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll1lll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᦮")):
            return
        cmd = args[0] if method_name == bstack1ll1lll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᦯") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠥ࠾ࠧᦰ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᦱ") + bstack11l1111ll11_opy_, bstack1ll111ll1l1_opy_)
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
        bstack11l1llll111_opy_ = bstack1ll111l1111_opy_.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᦲ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᦳ"))
        if bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.QUIT:
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.PRE:
                bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l111l1111_opy_.value)
                bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, EVENTS.bstack11l111l1111_opy_.value, bstack111l1l1l1_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᦴ").format(instance, method_name, bstack1ll11l1lll1_opy_, bstack11l1lllllll_opy_))
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST:
                bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l111l1l1l_opy_.value)
                bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, EVENTS.bstack11l111l1l1l_opy_.value, bstack111l1l1l1_opy_)
        if bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.bstack1l111ll1l1_opy_:
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST and not bstack1ll111l1111_opy_.bstack1ll1ll111ll_opy_ in instance.data:
                session_id = getattr(target, bstack1ll1lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᦵ"), None)
                if session_id:
                    instance.data[bstack1ll111l1111_opy_.bstack1ll1ll111ll_opy_] = session_id
        elif (
            bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.bstack1ll1l1lllll_opy_
            and bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args) == bstack1ll111l1111_opy_.bstack11ll11l1l11_opy_
        ):
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.PRE:
                hub_url = bstack1ll111l1111_opy_.bstack11llll1l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll111l1111_opy_.bstack1lll111l_opy_: hub_url,
                            bstack1ll111l1111_opy_.bstack11ll111l1ll_opy_: bstack1ll111l1111_opy_.bstack1l11l11l1ll_opy_(hub_url),
                            bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_: int(
                                os.environ.get(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᦶ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11l111l1l_opy_ = bstack1ll111l1111_opy_.bstack1l11l11l11l_opy_(*args)
                bstack11l111l111l_opy_ = bstack1l11l111l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᦷ"), None) if bstack1l11l111l1l_opy_ else None
                if isinstance(bstack11l111l111l_opy_, dict):
                    instance.data[bstack1ll111l1111_opy_.bstack11l1111l1l1_opy_] = copy.deepcopy(bstack11l111l111l_opy_)
                    instance.data[bstack1ll111l1111_opy_.bstack11l11l11_opy_] = bstack11l111l111l_opy_
            elif bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll1lll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᦸ"), dict()).get(bstack1ll1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᦹ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll111l1111_opy_.bstack1ll1ll111ll_opy_: framework_session_id,
                                bstack1ll111l1111_opy_.bstack11l111l1l11_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.bstack1ll1l1lllll_opy_
            and bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args) == bstack1ll111l1111_opy_.bstack11l1111ll1l_opy_
            and bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST
        ):
            instance.data[bstack1ll111l1111_opy_.bstack11l111l11l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l1llll111_opy_ in bstack1ll111l1111_opy_.bstack11l1111llll_opy_:
            bstack11l1lllll11_opy_ = None
            for callback in bstack1ll111l1111_opy_.bstack11l1111llll_opy_[bstack11l1llll111_opy_]:
                try:
                    bstack11l1llll11l_opy_ = callback(self, target, exec, bstack1ll11l1l111_opy_, result, *args, **kwargs)
                    if bstack11l1lllll11_opy_ == None:
                        bstack11l1lllll11_opy_ = bstack11l1llll11l_opy_
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᦺ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᦻ"))
                    traceback.print_exc()
            if bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.QUIT:
                if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.PRE:
                    bstack111l1l1l1_opy_ = bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, EVENTS.bstack11l111l1111_opy_.value)
                    if bstack111l1l1l1_opy_!=None:
                        bstack1l1l11ll1_opy_.end(EVENTS.bstack11l111l1111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᦼ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᦽ"), True, None)
                if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST:
                    bstack111l1l1l1_opy_ = bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, EVENTS.bstack11l111l1l1l_opy_.value)
                    if bstack111l1l1l1_opy_!=None:
                        bstack1l1l11ll1_opy_.end(EVENTS.bstack11l111l1l1l_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᦾ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᦿ"), True, None)
            if bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.PRE and callable(bstack11l1lllll11_opy_):
                return bstack11l1lllll11_opy_
            elif bstack11l1lllllll_opy_ == bstack1l11l11l1_opy_.POST and bstack11l1lllll11_opy_:
                return bstack11l1lllll11_opy_
    def bstack1ll11llll11_opy_(
        self, method_name, previous_state: bstack11lll111_opy_, *args, **kwargs
    ) -> bstack11lll111_opy_:
        if method_name == bstack1ll1lll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᧀ") or method_name == bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᧁ"):
            return bstack11lll111_opy_.bstack1l111ll1l1_opy_
        if method_name == bstack1ll1lll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᧂ"):
            return bstack11lll111_opy_.QUIT
        if method_name == bstack1ll1lll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᧃ"):
            if previous_state != bstack11lll111_opy_.NONE:
                command_name = bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args)
                if command_name == bstack1ll111l1111_opy_.bstack11ll11l1l11_opy_:
                    return bstack11lll111_opy_.bstack1l111ll1l1_opy_
            return bstack11lll111_opy_.bstack1ll1l1lllll_opy_
        return bstack11lll111_opy_.NONE