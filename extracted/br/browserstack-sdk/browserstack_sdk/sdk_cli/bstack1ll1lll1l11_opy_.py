# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll111l_opy_,
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.constants import EVENTS
class bstack1llll111lll_opy_(bstack1111111l11_opy_):
    bstack1l11ll1ll11_opy_ = bstack111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᔃ")
    NAME = bstack111lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᔄ")
    bstack1l1l1lll1l1_opy_ = bstack111lll_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᔅ")
    bstack1l1l1llll11_opy_ = bstack111lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᔆ")
    bstack1l11111l1ll_opy_ = bstack111lll_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔇ")
    bstack1l1l1l1l1ll_opy_ = bstack111lll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᔈ")
    bstack1l11lll11ll_opy_ = bstack111lll_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᔉ")
    bstack1l11111ll1l_opy_ = bstack111lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔊ")
    bstack1l11111l11l_opy_ = bstack111lll_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᔋ")
    bstack1ll1l11ll1l_opy_ = bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᔌ")
    bstack1l1l111l1ll_opy_ = bstack111lll_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᔍ")
    bstack1l111111ll1_opy_ = bstack111lll_opy_ (u"ࠢࡨࡧࡷࠦᔎ")
    bstack1l1lll1l1l1_opy_ = bstack111lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᔏ")
    bstack1l11ll1l111_opy_ = bstack111lll_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᔐ")
    bstack1l11ll1lll1_opy_ = bstack111lll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᔑ")
    bstack1l11111ll11_opy_ = bstack111lll_opy_ (u"ࠦࡶࡻࡩࡵࠤᔒ")
    bstack1l11111l111_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11111ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1l1ll1_opy_: Any
    bstack1l11ll1llll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11111ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll1l1ll1_opy_: Dict[str, Any],
        methods=[bstack111lll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᔓ"), bstack111lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᔔ"), bstack111lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᔕ"), bstack111lll_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᔖ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11111ll_opy_ = bstack1l1l11111ll_opy_
        self.platform_index = platform_index
        self.bstack1lllll1l1ll_opy_(methods)
        self.bstack1llll1l1ll1_opy_ = bstack1llll1l1ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1111111l11_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l1llll11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1111111l11_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l1lll1l1_opy_, target, strict)
    @staticmethod
    def bstack1l111111lll_opy_(target: object, strict=True):
        return bstack1111111l11_opy_.get_data(bstack1llll111lll_opy_.bstack1l11111l1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1111111l11_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l1l1l1ll_opy_, target, strict)
    @staticmethod
    def bstack1ll111l111l_opy_(instance: bstack1llllll111l_opy_) -> bool:
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1l11lll11ll_opy_, False)
    @staticmethod
    def bstack1ll1l1l11l1_opy_(instance: bstack1llllll111l_opy_, default_value=None):
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1l1l1lll1l1_opy_, default_value)
    @staticmethod
    def bstack1ll1l11l11l_opy_(instance: bstack1llllll111l_opy_, default_value=None):
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1l1l1l1l1ll_opy_, default_value)
    @staticmethod
    def bstack1ll111llll1_opy_(hub_url: str, bstack1l111111l11_opy_=bstack111lll_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᔗ")):
        try:
            bstack1l111111l1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l111111l1l_opy_.endswith(bstack1l111111l11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11l1l1l1_opy_(method_name: str):
        return method_name == bstack111lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᔘ")
    @staticmethod
    def bstack1ll1l11l111_opy_(method_name: str, *args):
        return (
            bstack1llll111lll_opy_.bstack1ll11l1l1l1_opy_(method_name)
            and bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args) == bstack1llll111lll_opy_.bstack1l1l111l1ll_opy_
        )
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1llll111lll_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll111lll_opy_.bstack1l11ll1l111_opy_ in bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args):
            return False
        bstack1ll11l11ll1_opy_ = bstack1llll111lll_opy_.bstack1ll11l11lll_opy_(*args)
        return bstack1ll11l11ll1_opy_ and bstack111lll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᔙ") in bstack1ll11l11ll1_opy_ and bstack111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔚ") in bstack1ll11l11ll1_opy_[bstack111lll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᔛ")]
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str, *args):
        if not bstack1llll111lll_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return False
        if not bstack1llll111lll_opy_.bstack1l11ll1l111_opy_ in bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args):
            return False
        bstack1ll11l11ll1_opy_ = bstack1llll111lll_opy_.bstack1ll11l11lll_opy_(*args)
        return (
            bstack1ll11l11ll1_opy_
            and bstack111lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᔜ") in bstack1ll11l11ll1_opy_
            and bstack111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᔝ") in bstack1ll11l11ll1_opy_[bstack111lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᔞ")]
        )
    @staticmethod
    def bstack1l1l111l11l_opy_(*args):
        return str(bstack1llll111lll_opy_.bstack1ll1l111lll_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l11lll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11llll1l1l_opy_(driver):
        command_executor = getattr(driver, bstack111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔟ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack111lll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᔠ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack111lll_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᔡ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack111lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᔢ"), None)
        return hub_url
    def bstack1l1l1111ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack111lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔣ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack111lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔤ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack111lll_opy_ (u"ࠤࡢࡹࡷࡲࠢᔥ")):
                setattr(command_executor, bstack111lll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᔦ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11111ll_opy_ = hub_url
            bstack1llll111lll_opy_.bstack11111ll111_opy_(instance, bstack1llll111lll_opy_.bstack1l1l1lll1l1_opy_, hub_url)
            bstack1llll111lll_opy_.bstack11111ll111_opy_(
                instance, bstack1llll111lll_opy_.bstack1l11lll11ll_opy_, bstack1llll111lll_opy_.bstack1ll111llll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_]):
        return bstack111lll_opy_ (u"ࠦ࠿ࠨᔧ").join((bstack1111111111_opy_(bstack11111l1l11_opy_[0]).name, bstack11111l1ll1_opy_(bstack11111l1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll1l1l_opy_(bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_], callback: Callable):
        bstack1l11ll1ll1l_opy_ = bstack1llll111lll_opy_.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        if not bstack1l11ll1ll1l_opy_ in bstack1llll111lll_opy_.bstack1l11111l111_opy_:
            bstack1llll111lll_opy_.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_] = []
        bstack1llll111lll_opy_.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_].append(callback)
    def bstack11111111l1_opy_(self, instance: bstack1llllll111l_opy_, method_name: str, bstack111111111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack111lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᔨ")):
            return
        cmd = args[0] if method_name == bstack111lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᔩ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11111l1l1_opy_ = bstack111lll_opy_ (u"ࠢ࠻ࠤᔪ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᔫ") + bstack1l11111l1l1_opy_, bstack111111111l_opy_)
    def bstack1llllll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll1llll_opy_, bstack1l11ll1l1l1_opy_ = bstack11111l1l11_opy_
        bstack1l11ll1ll1l_opy_ = bstack1llll111lll_opy_.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔬ") + str(kwargs) + bstack111lll_opy_ (u"ࠥࠦᔭ"))
        if bstack1lllll1llll_opy_ == bstack1111111111_opy_.QUIT:
            if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack111l11ll_opy_.value)
                bstack1111111l11_opy_.bstack11111ll111_opy_(instance, EVENTS.bstack111l11ll_opy_.value, bstack1ll11llll11_opy_)
                self.logger.debug(bstack111lll_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᔮ").format(instance, method_name, bstack1lllll1llll_opy_, bstack1l11ll1l1l1_opy_))
        if bstack1lllll1llll_opy_ == bstack1111111111_opy_.bstack1lllllll1l1_opy_:
            if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST and not bstack1llll111lll_opy_.bstack1l1l1llll11_opy_ in instance.data:
                session_id = getattr(target, bstack111lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᔯ"), None)
                if session_id:
                    instance.data[bstack1llll111lll_opy_.bstack1l1l1llll11_opy_] = session_id
        elif (
            bstack1lllll1llll_opy_ == bstack1111111111_opy_.bstack111111lll1_opy_
            and bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args) == bstack1llll111lll_opy_.bstack1l1l111l1ll_opy_
        ):
            if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.PRE:
                hub_url = bstack1llll111lll_opy_.bstack11llll1l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll111lll_opy_.bstack1l1l1lll1l1_opy_: hub_url,
                            bstack1llll111lll_opy_.bstack1l11lll11ll_opy_: bstack1llll111lll_opy_.bstack1ll111llll1_opy_(hub_url),
                            bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_: int(
                                os.environ.get(bstack111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᔰ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l11ll1_opy_ = bstack1llll111lll_opy_.bstack1ll11l11lll_opy_(*args)
                bstack1l111111lll_opy_ = bstack1ll11l11ll1_opy_.get(bstack111lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔱ"), None) if bstack1ll11l11ll1_opy_ else None
                if isinstance(bstack1l111111lll_opy_, dict):
                    instance.data[bstack1llll111lll_opy_.bstack1l11111l1ll_opy_] = copy.deepcopy(bstack1l111111lll_opy_)
                    instance.data[bstack1llll111lll_opy_.bstack1l1l1l1l1ll_opy_] = bstack1l111111lll_opy_
            elif bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack111lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᔲ"), dict()).get(bstack111lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᔳ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll111lll_opy_.bstack1l1l1llll11_opy_: framework_session_id,
                                bstack1llll111lll_opy_.bstack1l11111ll1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllll1llll_opy_ == bstack1111111111_opy_.bstack111111lll1_opy_
            and bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args) == bstack1llll111lll_opy_.bstack1l11111ll11_opy_
            and bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST
        ):
            instance.data[bstack1llll111lll_opy_.bstack1l11111l11l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11ll1ll1l_opy_ in bstack1llll111lll_opy_.bstack1l11111l111_opy_:
            bstack1l11ll1l1ll_opy_ = None
            for callback in bstack1llll111lll_opy_.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_]:
                try:
                    bstack1l11ll11lll_opy_ = callback(self, target, exec, bstack11111l1l11_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l1ll_opy_ == None:
                        bstack1l11ll1l1ll_opy_ = bstack1l11ll11lll_opy_
                except Exception as e:
                    self.logger.error(bstack111lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᔴ") + str(e) + bstack111lll_opy_ (u"ࠦࠧᔵ"))
                    traceback.print_exc()
            if bstack1lllll1llll_opy_ == bstack1111111111_opy_.QUIT:
                if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST:
                    bstack1ll11llll11_opy_ = bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, EVENTS.bstack111l11ll_opy_.value)
                    if bstack1ll11llll11_opy_!=None:
                        bstack1llll1l1l11_opy_.end(EVENTS.bstack111l11ll_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔶ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔷ"), True, None)
            if bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.PRE and callable(bstack1l11ll1l1ll_opy_):
                return bstack1l11ll1l1ll_opy_
            elif bstack1l11ll1l1l1_opy_ == bstack11111l1ll1_opy_.POST and bstack1l11ll1l1ll_opy_:
                return bstack1l11ll1l1ll_opy_
    def bstack1llllll1ll1_opy_(
        self, method_name, previous_state: bstack1111111111_opy_, *args, **kwargs
    ) -> bstack1111111111_opy_:
        if method_name == bstack111lll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᔸ") or method_name == bstack111lll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᔹ"):
            return bstack1111111111_opy_.bstack1lllllll1l1_opy_
        if method_name == bstack111lll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᔺ"):
            return bstack1111111111_opy_.QUIT
        if method_name == bstack111lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᔻ"):
            if previous_state != bstack1111111111_opy_.NONE:
                bstack1ll1l11111l_opy_ = bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args)
                if bstack1ll1l11111l_opy_ == bstack1llll111lll_opy_.bstack1l1l111l1ll_opy_:
                    return bstack1111111111_opy_.bstack1lllllll1l1_opy_
            return bstack1111111111_opy_.bstack111111lll1_opy_
        return bstack1111111111_opy_.NONE