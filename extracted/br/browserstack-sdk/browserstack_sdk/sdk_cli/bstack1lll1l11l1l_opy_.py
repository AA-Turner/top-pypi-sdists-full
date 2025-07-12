# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1ll1lllll11_opy_,
    bstack1lll1llll11_opy_,
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1ll1l1l_opy_(bstack1ll1lllll11_opy_):
    bstack1l1llllllll_opy_ = bstack11l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᏙ")
    NAME = bstack11l1111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᏚ")
    bstack1ll1ll1l111_opy_ = bstack11l1111_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᏛ")
    bstack1ll1l1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᏜ")
    bstack1l1l11l1lll_opy_ = bstack11l1111_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᏝ")
    bstack1ll1ll11l11_opy_ = bstack11l1111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᏞ")
    bstack1ll1111l1ll_opy_ = bstack11l1111_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᏟ")
    bstack1l1l111lll1_opy_ = bstack11l1111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᏠ")
    bstack1l1l11l1l1l_opy_ = bstack11l1111_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᏡ")
    bstack1llllll1lll_opy_ = bstack11l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᏢ")
    bstack1ll11ll1111_opy_ = bstack11l1111_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᏣ")
    bstack1l1l111llll_opy_ = bstack11l1111_opy_ (u"ࠥ࡫ࡪࡺࠢᏤ")
    bstack1lll1ll1ll1_opy_ = bstack11l1111_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᏥ")
    bstack1ll11111lll_opy_ = bstack11l1111_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᏦ")
    bstack1ll1111l111_opy_ = bstack11l1111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᏧ")
    bstack1l1l11l1ll1_opy_ = bstack11l1111_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᏨ")
    bstack1l1l11l11ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll111ll11l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll11l11l11_opy_: Any
    bstack1ll111111ll_opy_: Dict
    def __init__(
        self,
        bstack1ll111ll11l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll11l11l11_opy_: Dict[str, Any],
        methods=[bstack11l1111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᏩ"), bstack11l1111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᏪ"), bstack11l1111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᏫ"), bstack11l1111_opy_ (u"ࠦࡶࡻࡩࡵࠤᏬ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1ll111ll11l_opy_ = bstack1ll111ll11l_opy_
        self.platform_index = platform_index
        self.bstack1l1lllllll1_opy_(methods)
        self.bstack1ll11l11l11_opy_ = bstack1ll11l11l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1lllll11_opy_.get_data(bstack1lll1ll1l1l_opy_.bstack1ll1l1l1ll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1lllll11_opy_.get_data(bstack1lll1ll1l1l_opy_.bstack1ll1ll1l111_opy_, target, strict)
    @staticmethod
    def bstack1l1l11l111l_opy_(target: object, strict=True):
        return bstack1ll1lllll11_opy_.get_data(bstack1lll1ll1l1l_opy_.bstack1l1l11l1lll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1lllll11_opy_.get_data(bstack1lll1ll1l1l_opy_.bstack1ll1ll11l11_opy_, target, strict)
    @staticmethod
    def bstack1ll1lllll1l_opy_(instance: bstack1lll1llll11_opy_) -> bool:
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1ll1111l1ll_opy_, False)
    @staticmethod
    def bstack1l1lllll111_opy_(instance: bstack1lll1llll11_opy_, default_value=None):
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1ll1ll1l111_opy_, default_value)
    @staticmethod
    def bstack1l1llllll11_opy_(instance: bstack1lll1llll11_opy_, default_value=None):
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1ll1ll11l11_opy_, default_value)
    @staticmethod
    def bstack1lll1111l11_opy_(hub_url: str, bstack1l1l11l11l1_opy_=bstack11l1111_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᏭ")):
        try:
            bstack1l1l11l1111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1l11l1111_opy_.endswith(bstack1l1l11l11l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1lllll11ll1_opy_(method_name: str):
        return method_name == bstack11l1111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᏮ")
    @staticmethod
    def bstack1ll11l11111_opy_(method_name: str, *args):
        return (
            bstack1lll1ll1l1l_opy_.bstack1lllll11ll1_opy_(method_name)
            and bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args) == bstack1lll1ll1l1l_opy_.bstack1ll11ll1111_opy_
        )
    @staticmethod
    def bstack1ll111111l1_opy_(method_name: str, *args):
        if not bstack1lll1ll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
            return False
        if not bstack1lll1ll1l1l_opy_.bstack1ll11111lll_opy_ in bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args):
            return False
        bstack1lll1111111_opy_ = bstack1lll1ll1l1l_opy_.bstack1lll111llll_opy_(*args)
        return bstack1lll1111111_opy_ and bstack11l1111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᏯ") in bstack1lll1111111_opy_ and bstack11l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᏰ") in bstack1lll1111111_opy_[bstack11l1111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᏱ")]
    @staticmethod
    def bstack1ll11111l11_opy_(method_name: str, *args):
        if not bstack1lll1ll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
            return False
        if not bstack1lll1ll1l1l_opy_.bstack1ll11111lll_opy_ in bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args):
            return False
        bstack1lll1111111_opy_ = bstack1lll1ll1l1l_opy_.bstack1lll111llll_opy_(*args)
        return (
            bstack1lll1111111_opy_
            and bstack11l1111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᏲ") in bstack1lll1111111_opy_
            and bstack11l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᏳ") in bstack1lll1111111_opy_[bstack11l1111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᏴ")]
        )
    @staticmethod
    def bstack1ll11l1l1ll_opy_(*args):
        return str(bstack1lll1ll1l1l_opy_.bstack1lllll1ll11_opy_(*args)).lower()
    @staticmethod
    def bstack1lllll1ll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1lll111llll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l111l1l1_opy_(driver):
        command_executor = getattr(driver, bstack11l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᏵ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1111_opy_ (u"ࠢࡠࡷࡵࡰࠧ᏶"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1111_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤ᏷"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᏸ"), None)
        return hub_url
    def bstack1ll11l11ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᏹ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᏺ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1111_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᏻ")):
                setattr(command_executor, bstack11l1111_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᏼ"), hub_url)
                result = True
        if result:
            self.bstack1ll111ll11l_opy_ = hub_url
            bstack1lll1ll1l1l_opy_.bstack1llll111l11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1ll1ll1l111_opy_, hub_url)
            bstack1lll1ll1l1l_opy_.bstack1llll111l11_opy_(
                instance, bstack1lll1ll1l1l_opy_.bstack1ll1111l1ll_opy_, bstack1lll1ll1l1l_opy_.bstack1lll1111l11_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_]):
        return bstack11l1111_opy_ (u"ࠢ࠻ࠤᏽ").join((bstack1lll1llllll_opy_(bstack1llll11l111_opy_[0]).name, bstack1llllll1l1l_opy_(bstack1llll11l111_opy_[1]).name))
    @staticmethod
    def bstack1lllll1llll_opy_(bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1ll11111111_opy_ = bstack1lll1ll1l1l_opy_.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        if not bstack1ll11111111_opy_ in bstack1lll1ll1l1l_opy_.bstack1l1l11l11ll_opy_:
            bstack1lll1ll1l1l_opy_.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_] = []
        bstack1lll1ll1l1l_opy_.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_].append(callback)
    def bstack1ll1111l11l_opy_(self, instance: bstack1lll1llll11_opy_, method_name: str, bstack1ll11111l1l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᏾")):
            return
        cmd = args[0] if method_name == bstack11l1111_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᏿") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1l11l1l11_opy_ = bstack11l1111_opy_ (u"ࠥ࠾ࠧ᐀").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᐁ") + bstack1l1l11l1l11_opy_, bstack1ll11111l1l_opy_)
    def bstack1ll11111ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1lllll1ll_opy_, bstack1l1llll1lll_opy_ = bstack1llll11l111_opy_
        bstack1ll11111111_opy_ = bstack1lll1ll1l1l_opy_.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐂ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢᐃ"))
        if bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.QUIT:
            if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.PRE:
                bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack1l11l1l1ll_opy_.value)
                bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, EVENTS.bstack1l11l1l1ll_opy_.value, bstack1lll1lll11l_opy_)
                self.logger.debug(bstack11l1111_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᐄ").format(instance, method_name, bstack1l1lllll1ll_opy_, bstack1l1llll1lll_opy_))
        if bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_:
            if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST and not bstack1lll1ll1l1l_opy_.bstack1ll1l1l1ll1_opy_ in instance.data:
                session_id = getattr(target, bstack11l1111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᐅ"), None)
                if session_id:
                    instance.data[bstack1lll1ll1l1l_opy_.bstack1ll1l1l1ll1_opy_] = session_id
        elif (
            bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.bstack1llll1lll11_opy_
            and bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args) == bstack1lll1ll1l1l_opy_.bstack1ll11ll1111_opy_
        ):
            if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.PRE:
                hub_url = bstack1lll1ll1l1l_opy_.bstack11l111l1l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1ll1l1l_opy_.bstack1ll1ll1l111_opy_: hub_url,
                            bstack1lll1ll1l1l_opy_.bstack1ll1111l1ll_opy_: bstack1lll1ll1l1l_opy_.bstack1lll1111l11_opy_(hub_url),
                            bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_: int(
                                os.environ.get(bstack11l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᐆ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1lll1111111_opy_ = bstack1lll1ll1l1l_opy_.bstack1lll111llll_opy_(*args)
                bstack1l1l11l111l_opy_ = bstack1lll1111111_opy_.get(bstack11l1111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᐇ"), None) if bstack1lll1111111_opy_ else None
                if isinstance(bstack1l1l11l111l_opy_, dict):
                    instance.data[bstack1lll1ll1l1l_opy_.bstack1l1l11l1lll_opy_] = copy.deepcopy(bstack1l1l11l111l_opy_)
                    instance.data[bstack1lll1ll1l1l_opy_.bstack1ll1ll11l11_opy_] = bstack1l1l11l111l_opy_
            elif bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᐈ"), dict()).get(bstack11l1111_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᐉ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1ll1l1l_opy_.bstack1ll1l1l1ll1_opy_: framework_session_id,
                                bstack1lll1ll1l1l_opy_.bstack1l1l111lll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.bstack1llll1lll11_opy_
            and bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args) == bstack1lll1ll1l1l_opy_.bstack1l1l11l1ll1_opy_
            and bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST
        ):
            instance.data[bstack1lll1ll1l1l_opy_.bstack1l1l11l1l1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1ll11111111_opy_ in bstack1lll1ll1l1l_opy_.bstack1l1l11l11ll_opy_:
            bstack1l1lllll11l_opy_ = None
            for callback in bstack1lll1ll1l1l_opy_.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_]:
                try:
                    bstack1l1llllll1l_opy_ = callback(self, target, exec, bstack1llll11l111_opy_, result, *args, **kwargs)
                    if bstack1l1lllll11l_opy_ == None:
                        bstack1l1lllll11l_opy_ = bstack1l1llllll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᐊ") + str(e) + bstack11l1111_opy_ (u"ࠢࠣᐋ"))
                    traceback.print_exc()
            if bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.QUIT:
                if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST:
                    bstack1lll1lll11l_opy_ = bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, EVENTS.bstack1l11l1l1ll_opy_.value)
                    if bstack1lll1lll11l_opy_!=None:
                        bstack1lll1l1l11l_opy_.end(EVENTS.bstack1l11l1l1ll_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᐌ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᐍ"), True, None)
            if bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l1lllll11l_opy_):
                return bstack1l1lllll11l_opy_
            elif bstack1l1llll1lll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l1lllll11l_opy_:
                return bstack1l1lllll11l_opy_
    def bstack1ll1111111l_opy_(
        self, method_name, previous_state: bstack1lll1llllll_opy_, *args, **kwargs
    ) -> bstack1lll1llllll_opy_:
        if method_name == bstack11l1111_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᐎ") or method_name == bstack11l1111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᐏ"):
            return bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_
        if method_name == bstack11l1111_opy_ (u"ࠧࡷࡵࡪࡶࠥᐐ"):
            return bstack1lll1llllll_opy_.QUIT
        if method_name == bstack11l1111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᐑ"):
            if previous_state != bstack1lll1llllll_opy_.NONE:
                bstack1lll1111ll1_opy_ = bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args)
                if bstack1lll1111ll1_opy_ == bstack1lll1ll1l1l_opy_.bstack1ll11ll1111_opy_:
                    return bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_
            return bstack1lll1llllll_opy_.bstack1llll1lll11_opy_
        return bstack1lll1llllll_opy_.NONE