# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1lll11l1ll1_opy_,
    bstack1ll1ll1l111_opy_,
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from bstack_utils.constants import EVENTS
class bstack1ll11l11111_opy_(bstack1lll11l1ll1_opy_):
    bstack11ll1lll11l_opy_ = bstack1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᢆ")
    NAME = bstack1111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᢇ")
    bstack1lll11lll1l_opy_ = bstack1111_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᢈ")
    bstack1lll1l1l1l1_opy_ = bstack1111_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᢉ")
    bstack11l1l111ll1_opy_ = bstack1111_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᢊ")
    bstack1lll1111l11_opy_ = bstack1111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᢋ")
    bstack11lll111lll_opy_ = bstack1111_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᢌ")
    bstack11l1l1111ll_opy_ = bstack1111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᢍ")
    bstack11l1l1111l1_opy_ = bstack1111_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᢎ")
    bstack1l1l11l1ll1_opy_ = bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᢏ")
    bstack11lll1ll111_opy_ = bstack1111_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᢐ")
    bstack11l1l11l1l1_opy_ = bstack1111_opy_ (u"ࠥ࡫ࡪࡺࠢᢑ")
    bstack1l111ll1l1l_opy_ = bstack1111_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᢒ")
    bstack11ll1ll1ll1_opy_ = bstack1111_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᢓ")
    bstack11ll1lll111_opy_ = bstack1111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᢔ")
    bstack11l1l11l1ll_opy_ = bstack1111_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᢕ")
    bstack11l1l111l11_opy_: Dict[str, List[Callable]] = dict()
    bstack11lll11l1ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llll111l_opy_: Any
    bstack11ll1ll1l1l_opy_: Dict
    def __init__(
        self,
        bstack11lll11l1ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1llll111l_opy_: Dict[str, Any],
        methods=[bstack1111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᢖ"), bstack1111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᢗ"), bstack1111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᢘ"), bstack1111_opy_ (u"ࠦࡶࡻࡩࡵࠤᢙ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11lll11l1ll_opy_ = bstack11lll11l1ll_opy_
        self.platform_index = platform_index
        self.bstack1ll1llll111_opy_(methods)
        self.bstack1l1llll111l_opy_ = bstack1l1llll111l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll11l1ll1_opy_.get_data(bstack1ll11l11111_opy_.bstack1lll1l1l1l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll11l1ll1_opy_.get_data(bstack1ll11l11111_opy_.bstack1lll11lll1l_opy_, target, strict)
    @staticmethod
    def bstack11l1l11ll11_opy_(target: object, strict=True):
        return bstack1lll11l1ll1_opy_.get_data(bstack1ll11l11111_opy_.bstack11l1l111ll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll11l1ll1_opy_.get_data(bstack1ll11l11111_opy_.bstack1lll1111l11_opy_, target, strict)
    @staticmethod
    def bstack1l11ll1lll1_opy_(instance: bstack1ll1ll1l111_opy_) -> bool:
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack11lll111lll_opy_, False)
    @staticmethod
    def bstack1l1ll111111_opy_(instance: bstack1ll1ll1l111_opy_, default_value=None):
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1lll11lll1l_opy_, default_value)
    @staticmethod
    def bstack1l1l1ll1ll1_opy_(instance: bstack1ll1ll1l111_opy_, default_value=None):
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1lll1111l11_opy_, default_value)
    @staticmethod
    def bstack1l11llll11l_opy_(hub_url: str, bstack11l1l11l11l_opy_=bstack1111_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᢚ")):
        try:
            bstack11l1l111l1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1l111l1l_opy_.endswith(bstack11l1l11l11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l111l1ll_opy_(method_name: str):
        return method_name == bstack1111_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᢛ")
    @staticmethod
    def bstack1l1l1lllll1_opy_(method_name: str, *args):
        return (
            bstack1ll11l11111_opy_.bstack1l1l111l1ll_opy_(method_name)
            and bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args) == bstack1ll11l11111_opy_.bstack11lll1ll111_opy_
        )
    @staticmethod
    def bstack1l1l11l1111_opy_(method_name: str, *args):
        if not bstack1ll11l11111_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1ll11l11111_opy_.bstack11ll1ll1ll1_opy_ in bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args):
            return False
        bstack1l1l1111111_opy_ = bstack1ll11l11111_opy_.bstack1l11lllllll_opy_(*args)
        return bstack1l1l1111111_opy_ and bstack1111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᢜ") in bstack1l1l1111111_opy_ and bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᢝ") in bstack1l1l1111111_opy_[bstack1111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᢞ")]
    @staticmethod
    def bstack1l1l1lll11l_opy_(method_name: str, *args):
        if not bstack1ll11l11111_opy_.bstack1l1l111l1ll_opy_(method_name):
            return False
        if not bstack1ll11l11111_opy_.bstack11ll1ll1ll1_opy_ in bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args):
            return False
        bstack1l1l1111111_opy_ = bstack1ll11l11111_opy_.bstack1l11lllllll_opy_(*args)
        return (
            bstack1l1l1111111_opy_
            and bstack1111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᢟ") in bstack1l1l1111111_opy_
            and bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᢠ") in bstack1l1l1111111_opy_[bstack1111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᢡ")]
        )
    @staticmethod
    def bstack11lll1ll1ll_opy_(*args):
        return str(bstack1ll11l11111_opy_.bstack1l1l1l11lll_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l1l11lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11lllllll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1111l111l_opy_(driver):
        command_executor = getattr(driver, bstack1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᢢ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1111_opy_ (u"ࠢࡠࡷࡵࡰࠧᢣ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1111_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᢤ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᢥ"), None)
        return hub_url
    def bstack11llll1111l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᢦ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᢧ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1111_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᢨ")):
                setattr(command_executor, bstack1111_opy_ (u"ࠨ࡟ࡶࡴ࡯ᢩࠦ"), hub_url)
                result = True
        if result:
            self.bstack11lll11l1ll_opy_ = hub_url
            bstack1ll11l11111_opy_.bstack1lll1l11l1l_opy_(instance, bstack1ll11l11111_opy_.bstack1lll11lll1l_opy_, hub_url)
            bstack1ll11l11111_opy_.bstack1lll1l11l1l_opy_(
                instance, bstack1ll11l11111_opy_.bstack11lll111lll_opy_, bstack1ll11l11111_opy_.bstack1l11llll11l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_]):
        return bstack1111_opy_ (u"ࠢ࠻ࠤᢪ").join((bstack1ll1lll1ll1_opy_(bstack1ll1ll1ll1l_opy_[0]).name, bstack1ll1l1lll1l_opy_(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1ll1111ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_], callback: Callable):
        bstack11ll1ll11ll_opy_ = bstack1ll11l11111_opy_.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1ll11ll_opy_ in bstack1ll11l11111_opy_.bstack11l1l111l11_opy_:
            bstack1ll11l11111_opy_.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_] = []
        bstack1ll11l11111_opy_.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_].append(callback)
    def bstack1ll1ll1111l_opy_(self, instance: bstack1ll1ll1l111_opy_, method_name: str, bstack1ll1ll11ll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᢫")):
            return
        cmd = args[0] if method_name == bstack1111_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᢬") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1l111lll_opy_ = bstack1111_opy_ (u"ࠥ࠾ࠧ᢭").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧ᢮") + bstack11l1l111lll_opy_, bstack1ll1ll11ll1_opy_)
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1l11llll_opy_, bstack11ll1ll11l1_opy_ = bstack1ll1ll1ll1l_opy_
        bstack11ll1ll11ll_opy_ = bstack1ll11l11111_opy_.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᢯") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢᢰ"))
        if bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.QUIT:
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.PRE:
                bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1l11ll1l_opy_.value)
                bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, EVENTS.bstack11l1l11ll1l_opy_.value, bstack1l1l1llll1_opy_)
                self.logger.debug(bstack1111_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᢱ").format(instance, method_name, bstack1ll1l11llll_opy_, bstack11ll1ll11l1_opy_))
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST:
                bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1l11l111_opy_.value)
                bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, EVENTS.bstack11l1l11l111_opy_.value, bstack1l1l1llll1_opy_)
        if bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_:
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST and not bstack1ll11l11111_opy_.bstack1lll1l1l1l1_opy_ in instance.data:
                session_id = getattr(target, bstack1111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᢲ"), None)
                if session_id:
                    instance.data[bstack1ll11l11111_opy_.bstack1lll1l1l1l1_opy_] = session_id
        elif (
            bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_
            and bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args) == bstack1ll11l11111_opy_.bstack11lll1ll111_opy_
        ):
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.PRE:
                hub_url = bstack1ll11l11111_opy_.bstack1111l111l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll11l11111_opy_.bstack1lll11lll1l_opy_: hub_url,
                            bstack1ll11l11111_opy_.bstack11lll111lll_opy_: bstack1ll11l11111_opy_.bstack1l11llll11l_opy_(hub_url),
                            bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_: int(
                                os.environ.get(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᢳ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l1111111_opy_ = bstack1ll11l11111_opy_.bstack1l11lllllll_opy_(*args)
                bstack11l1l11ll11_opy_ = bstack1l1l1111111_opy_.get(bstack1111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᢴ"), None) if bstack1l1l1111111_opy_ else None
                if isinstance(bstack11l1l11ll11_opy_, dict):
                    instance.data[bstack1ll11l11111_opy_.bstack11l1l111ll1_opy_] = copy.deepcopy(bstack11l1l11ll11_opy_)
                    instance.data[bstack1ll11l11111_opy_.bstack1lll1111l11_opy_] = bstack11l1l11ll11_opy_
            elif bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᢵ"), dict()).get(bstack1111_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᢶ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll11l11111_opy_.bstack1lll1l1l1l1_opy_: framework_session_id,
                                bstack1ll11l11111_opy_.bstack11l1l1111ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_
            and bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args) == bstack1ll11l11111_opy_.bstack11l1l11l1ll_opy_
            and bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST
        ):
            instance.data[bstack1ll11l11111_opy_.bstack11l1l1111l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll1ll11ll_opy_ in bstack1ll11l11111_opy_.bstack11l1l111l11_opy_:
            bstack11ll1ll1lll_opy_ = None
            for callback in bstack1ll11l11111_opy_.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_]:
                try:
                    bstack11ll1ll111l_opy_ = callback(self, target, exec, bstack1ll1ll1ll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1ll1lll_opy_ == None:
                        bstack11ll1ll1lll_opy_ = bstack11ll1ll111l_opy_
                except Exception as e:
                    self.logger.error(bstack1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᢷ") + str(e) + bstack1111_opy_ (u"ࠢࠣᢸ"))
                    traceback.print_exc()
            if bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.QUIT:
                if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.PRE:
                    bstack1l1l1llll1_opy_ = bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, EVENTS.bstack11l1l11ll1l_opy_.value)
                    if bstack1l1l1llll1_opy_!=None:
                        bstack1l11l1ll_opy_.end(EVENTS.bstack11l1l11ll1l_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᢹ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᢺ"), True, None)
                if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST:
                    bstack1l1l1llll1_opy_ = bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, EVENTS.bstack11l1l11l111_opy_.value)
                    if bstack1l1l1llll1_opy_!=None:
                        bstack1l11l1ll_opy_.end(EVENTS.bstack11l1l11l111_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᢻ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᢼ"), True, None)
            if bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.PRE and callable(bstack11ll1ll1lll_opy_):
                return bstack11ll1ll1lll_opy_
            elif bstack11ll1ll11l1_opy_ == bstack1ll1l1lll1l_opy_.POST and bstack11ll1ll1lll_opy_:
                return bstack11ll1ll1lll_opy_
    def bstack1ll1l1ll1l1_opy_(
        self, method_name, previous_state: bstack1ll1lll1ll1_opy_, *args, **kwargs
    ) -> bstack1ll1lll1ll1_opy_:
        if method_name == bstack1111_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᢽ") or method_name == bstack1111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᢾ"):
            return bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_
        if method_name == bstack1111_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᢿ"):
            return bstack1ll1lll1ll1_opy_.QUIT
        if method_name == bstack1111_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᣀ"):
            if previous_state != bstack1ll1lll1ll1_opy_.NONE:
                command_name = bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args)
                if command_name == bstack1ll11l11111_opy_.bstack11lll1ll111_opy_:
                    return bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_
            return bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_
        return bstack1ll1lll1ll1_opy_.NONE