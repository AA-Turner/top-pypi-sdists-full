# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111ll1_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
from bstack_utils.constants import EVENTS
class bstack1llll11l111_opy_(bstack1111111ll1_opy_):
    bstack1l11l1ll1ll_opy_ = bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᔑ")
    NAME = bstack11ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᔒ")
    bstack1l1l1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᔓ")
    bstack1l1l1l11l11_opy_ = bstack11ll11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᔔ")
    bstack11llllll1ll_opy_ = bstack11ll11_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔕ")
    bstack1l1l1l11111_opy_ = bstack11ll11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᔖ")
    bstack1l11ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᔗ")
    bstack11lllll1ll1_opy_ = bstack11ll11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔘ")
    bstack11lllll1lll_opy_ = bstack11ll11_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᔙ")
    bstack1ll1l11111l_opy_ = bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᔚ")
    bstack1l1l111l11l_opy_ = bstack11ll11_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᔛ")
    bstack11llllll11l_opy_ = bstack11ll11_opy_ (u"ࠢࡨࡧࡷࠦᔜ")
    bstack1l1ll1llll1_opy_ = bstack11ll11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᔝ")
    bstack1l11l1ll1l1_opy_ = bstack11ll11_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᔞ")
    bstack1l11l1llll1_opy_ = bstack11ll11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᔟ")
    bstack11llllllll1_opy_ = bstack11ll11_opy_ (u"ࠦࡶࡻࡩࡵࠤᔠ")
    bstack11lllllll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1llll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll111l11l_opy_: Any
    bstack1l11ll11111_opy_: Dict
    def __init__(
        self,
        bstack1l11ll1llll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll111l11l_opy_: Dict[str, Any],
        methods=[bstack11ll11_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᔡ"), bstack11ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᔢ"), bstack11ll11_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᔣ"), bstack11ll11_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᔤ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll1llll_opy_ = bstack1l11ll1llll_opy_
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
        self.bstack1lll111l11l_opy_ = bstack1lll111l11l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1111111ll1_opy_.get_data(bstack1llll11l111_opy_.bstack1l1l1l11l11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1111111ll1_opy_.get_data(bstack1llll11l111_opy_.bstack1l1l1l11l1l_opy_, target, strict)
    @staticmethod
    def bstack11lllll1l1l_opy_(target: object, strict=True):
        return bstack1111111ll1_opy_.get_data(bstack1llll11l111_opy_.bstack11llllll1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1111111ll1_opy_.get_data(bstack1llll11l111_opy_.bstack1l1l1l11111_opy_, target, strict)
    @staticmethod
    def bstack1ll11111ll1_opy_(instance: bstack1llll1ll1ll_opy_) -> bool:
        return bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1l11ll1l11l_opy_, False)
    @staticmethod
    def bstack1ll11lll1ll_opy_(instance: bstack1llll1ll1ll_opy_, default_value=None):
        return bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1l1l1l11l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1llll1ll1ll_opy_, default_value=None):
        return bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1ll111l1l1l_opy_(hub_url: str, bstack11llllll1l1_opy_=bstack11ll11_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᔥ")):
        try:
            bstack11llllll111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llllll111_opy_.endswith(bstack11llllll1l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l11ll1l_opy_(method_name: str):
        return method_name == bstack11ll11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᔦ")
    @staticmethod
    def bstack1ll11lllll1_opy_(method_name: str, *args):
        return (
            bstack1llll11l111_opy_.bstack1ll1l11ll1l_opy_(method_name)
            and bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll11l111_opy_.bstack1l1l111l11l_opy_
        )
    @staticmethod
    def bstack1ll111lll11_opy_(method_name: str, *args):
        if not bstack1llll11l111_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1llll11l111_opy_.bstack1l11l1ll1l1_opy_ in bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1llll11l111_opy_.bstack1ll111l1ll1_opy_(*args)
        return bstack1ll1111lll1_opy_ and bstack11ll11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᔧ") in bstack1ll1111lll1_opy_ and bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔨ") in bstack1ll1111lll1_opy_[bstack11ll11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᔩ")]
    @staticmethod
    def bstack1ll11lll1l1_opy_(method_name: str, *args):
        if not bstack1llll11l111_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1llll11l111_opy_.bstack1l11l1ll1l1_opy_ in bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1llll11l111_opy_.bstack1ll111l1ll1_opy_(*args)
        return (
            bstack1ll1111lll1_opy_
            and bstack11ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᔪ") in bstack1ll1111lll1_opy_
            and bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᔫ") in bstack1ll1111lll1_opy_[bstack11ll11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᔬ")]
        )
    @staticmethod
    def bstack1l1l11111l1_opy_(*args):
        return str(bstack1llll11l111_opy_.bstack1ll11l1ll1l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11l1ll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111l1ll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11ll11l111_opy_(driver):
        command_executor = getattr(driver, bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔭ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11ll11_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᔮ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11ll11_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᔯ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11ll11_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᔰ"), None)
        return hub_url
    def bstack1l11llll1ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔱ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔲ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11ll11_opy_ (u"ࠤࡢࡹࡷࡲࠢᔳ")):
                setattr(command_executor, bstack11ll11_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᔴ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll1llll_opy_ = hub_url
            bstack1llll11l111_opy_.bstack1llllllllll_opy_(instance, bstack1llll11l111_opy_.bstack1l1l1l11l1l_opy_, hub_url)
            bstack1llll11l111_opy_.bstack1llllllllll_opy_(
                instance, bstack1llll11l111_opy_.bstack1l11ll1l11l_opy_, bstack1llll11l111_opy_.bstack1ll111l1l1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l1ll11l_opy_(bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_]):
        return bstack11ll11_opy_ (u"ࠦ࠿ࠨᔵ").join((bstack1111111l11_opy_(bstack111111111l_opy_[0]).name, bstack1llllll1111_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_], callback: Callable):
        bstack1l11l1l1lll_opy_ = bstack1llll11l111_opy_.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        if not bstack1l11l1l1lll_opy_ in bstack1llll11l111_opy_.bstack11lllllll11_opy_:
            bstack1llll11l111_opy_.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_] = []
        bstack1llll11l111_opy_.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_].append(callback)
    def bstack111111l11l_opy_(self, instance: bstack1llll1ll1ll_opy_, method_name: str, bstack11111111ll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11ll11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᔶ")):
            return
        cmd = args[0] if method_name == bstack11ll11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᔷ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11lllllll1l_opy_ = bstack11ll11_opy_ (u"ࠢ࠻ࠤᔸ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᔹ") + bstack11lllllll1l_opy_, bstack11111111ll_opy_)
    def bstack1llll1lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllllll11l_opy_, bstack1l11l1lll11_opy_ = bstack111111111l_opy_
        bstack1l11l1l1lll_opy_ = bstack1llll11l111_opy_.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔺ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦᔻ"))
        if bstack1lllllll11l_opy_ == bstack1111111l11_opy_.QUIT:
            if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.PRE:
                bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l11lll1_opy_.value)
                bstack1111111ll1_opy_.bstack1llllllllll_opy_(instance, EVENTS.bstack1l11lll1_opy_.value, bstack1ll11ll111l_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᔼ").format(instance, method_name, bstack1lllllll11l_opy_, bstack1l11l1lll11_opy_))
        if bstack1lllllll11l_opy_ == bstack1111111l11_opy_.bstack1llllll11l1_opy_:
            if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST and not bstack1llll11l111_opy_.bstack1l1l1l11l11_opy_ in instance.data:
                session_id = getattr(target, bstack11ll11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᔽ"), None)
                if session_id:
                    instance.data[bstack1llll11l111_opy_.bstack1l1l1l11l11_opy_] = session_id
        elif (
            bstack1lllllll11l_opy_ == bstack1111111l11_opy_.bstack1lllll11lll_opy_
            and bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll11l111_opy_.bstack1l1l111l11l_opy_
        ):
            if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.PRE:
                hub_url = bstack1llll11l111_opy_.bstack11ll11l111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll11l111_opy_.bstack1l1l1l11l1l_opy_: hub_url,
                            bstack1llll11l111_opy_.bstack1l11ll1l11l_opy_: bstack1llll11l111_opy_.bstack1ll111l1l1l_opy_(hub_url),
                            bstack1llll11l111_opy_.bstack1ll1l11111l_opy_: int(
                                os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᔾ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111lll1_opy_ = bstack1llll11l111_opy_.bstack1ll111l1ll1_opy_(*args)
                bstack11lllll1l1l_opy_ = bstack1ll1111lll1_opy_.get(bstack11ll11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔿ"), None) if bstack1ll1111lll1_opy_ else None
                if isinstance(bstack11lllll1l1l_opy_, dict):
                    instance.data[bstack1llll11l111_opy_.bstack11llllll1ll_opy_] = copy.deepcopy(bstack11lllll1l1l_opy_)
                    instance.data[bstack1llll11l111_opy_.bstack1l1l1l11111_opy_] = bstack11lllll1l1l_opy_
            elif bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11ll11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᕀ"), dict()).get(bstack11ll11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᕁ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll11l111_opy_.bstack1l1l1l11l11_opy_: framework_session_id,
                                bstack1llll11l111_opy_.bstack11lllll1ll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllllll11l_opy_ == bstack1111111l11_opy_.bstack1lllll11lll_opy_
            and bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll11l111_opy_.bstack11llllllll1_opy_
            and bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST
        ):
            instance.data[bstack1llll11l111_opy_.bstack11lllll1lll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l1l1lll_opy_ in bstack1llll11l111_opy_.bstack11lllllll11_opy_:
            bstack1l11l1lllll_opy_ = None
            for callback in bstack1llll11l111_opy_.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_]:
                try:
                    bstack1l11l1lll1l_opy_ = callback(self, target, exec, bstack111111111l_opy_, result, *args, **kwargs)
                    if bstack1l11l1lllll_opy_ == None:
                        bstack1l11l1lllll_opy_ = bstack1l11l1lll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᕂ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧᕃ"))
                    traceback.print_exc()
            if bstack1lllllll11l_opy_ == bstack1111111l11_opy_.QUIT:
                if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST:
                    bstack1ll11ll111l_opy_ = bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, EVENTS.bstack1l11lll1_opy_.value)
                    if bstack1ll11ll111l_opy_!=None:
                        bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l11lll1_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᕄ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᕅ"), True, None)
            if bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.PRE and callable(bstack1l11l1lllll_opy_):
                return bstack1l11l1lllll_opy_
            elif bstack1l11l1lll11_opy_ == bstack1llllll1111_opy_.POST and bstack1l11l1lllll_opy_:
                return bstack1l11l1lllll_opy_
    def bstack1111111lll_opy_(
        self, method_name, previous_state: bstack1111111l11_opy_, *args, **kwargs
    ) -> bstack1111111l11_opy_:
        if method_name == bstack11ll11_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᕆ") or method_name == bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᕇ"):
            return bstack1111111l11_opy_.bstack1llllll11l1_opy_
        if method_name == bstack11ll11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᕈ"):
            return bstack1111111l11_opy_.QUIT
        if method_name == bstack11ll11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᕉ"):
            if previous_state != bstack1111111l11_opy_.NONE:
                bstack1ll11ll1lll_opy_ = bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args)
                if bstack1ll11ll1lll_opy_ == bstack1llll11l111_opy_.bstack1l1l111l11l_opy_:
                    return bstack1111111l11_opy_.bstack1llllll11l1_opy_
            return bstack1111111l11_opy_.bstack1lllll11lll_opy_
        return bstack1111111l11_opy_.NONE