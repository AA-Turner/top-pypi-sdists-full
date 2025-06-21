# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1llllll1lll_opy_,
    bstack1111111111_opy_,
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.constants import EVENTS
class bstack1llll111lll_opy_(bstack1llllll1lll_opy_):
    bstack1l11l1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᔒ")
    NAME = bstack1l1l1l1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᔓ")
    bstack1l1l11lllll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᔔ")
    bstack1l1l11lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᔕ")
    bstack11llllll111_opy_ = bstack1l1l1l1_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔖ")
    bstack1l1l1l1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᔗ")
    bstack1l11ll11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᔘ")
    bstack11llllllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᔙ")
    bstack11llllll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᔚ")
    bstack1ll111ll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᔛ")
    bstack1l11lll111l_opy_ = bstack1l1l1l1_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᔜ")
    bstack11llllll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࠧᔝ")
    bstack1l1ll1lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᔞ")
    bstack1l11l1ll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᔟ")
    bstack1l11ll11111_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᔠ")
    bstack11llllll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡷࡵࡪࡶࠥᔡ")
    bstack11lllll1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11lll1ll1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l1l_opy_: Any
    bstack1l11l1lll1l_opy_: Dict
    def __init__(
        self,
        bstack1l11lll1ll1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l11l1l_opy_: Dict[str, Any],
        methods=[bstack1l1l1l1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᔢ"), bstack1l1l1l1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᔣ"), bstack1l1l1l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᔤ"), bstack1l1l1l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᔥ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11lll1ll1_opy_ = bstack1l11lll1ll1_opy_
        self.platform_index = platform_index
        self.bstack1llllll1l1l_opy_(methods)
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllll1lll_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l11lll1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllll1lll_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l11lllll_opy_, target, strict)
    @staticmethod
    def bstack11lllll1lll_opy_(target: object, strict=True):
        return bstack1llllll1lll_opy_.get_data(bstack1llll111lll_opy_.bstack11llllll111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllll1lll_opy_.get_data(bstack1llll111lll_opy_.bstack1l1l1l1lll1_opy_, target, strict)
    @staticmethod
    def bstack1ll11111l11_opy_(instance: bstack1111111111_opy_) -> bool:
        return bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1l11ll11lll_opy_, False)
    @staticmethod
    def bstack1ll11ll11ll_opy_(instance: bstack1111111111_opy_, default_value=None):
        return bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1l1l11lllll_opy_, default_value)
    @staticmethod
    def bstack1ll11l1l11l_opy_(instance: bstack1111111111_opy_, default_value=None):
        return bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1l1l1l1lll1_opy_, default_value)
    @staticmethod
    def bstack1ll111l1l1l_opy_(hub_url: str, bstack11lllllll11_opy_=bstack1l1l1l1_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᔦ")):
        try:
            bstack11lllllll1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11lllllll1l_opy_.endswith(bstack11lllllll11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11l111ll_opy_(method_name: str):
        return method_name == bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᔧ")
    @staticmethod
    def bstack1ll111ll11l_opy_(method_name: str, *args):
        return (
            bstack1llll111lll_opy_.bstack1ll11l111ll_opy_(method_name)
            and bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll111lll_opy_.bstack1l11lll111l_opy_
        )
    @staticmethod
    def bstack1ll1l11ll11_opy_(method_name: str, *args):
        if not bstack1llll111lll_opy_.bstack1ll11l111ll_opy_(method_name):
            return False
        if not bstack1llll111lll_opy_.bstack1l11l1ll1l1_opy_ in bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll111l11ll_opy_ = bstack1llll111lll_opy_.bstack1ll111l11l1_opy_(*args)
        return bstack1ll111l11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᔨ") in bstack1ll111l11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᔩ") in bstack1ll111l11ll_opy_[bstack1l1l1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᔪ")]
    @staticmethod
    def bstack1ll1l1l111l_opy_(method_name: str, *args):
        if not bstack1llll111lll_opy_.bstack1ll11l111ll_opy_(method_name):
            return False
        if not bstack1llll111lll_opy_.bstack1l11l1ll1l1_opy_ in bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args):
            return False
        bstack1ll111l11ll_opy_ = bstack1llll111lll_opy_.bstack1ll111l11l1_opy_(*args)
        return (
            bstack1ll111l11ll_opy_
            and bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᔫ") in bstack1ll111l11ll_opy_
            and bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᔬ") in bstack1ll111l11ll_opy_[bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᔭ")]
        )
    @staticmethod
    def bstack1l1l11111l1_opy_(*args):
        return str(bstack1llll111lll_opy_.bstack1ll11l1ll11_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11l1ll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll111l11l1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l111llll_opy_(driver):
        command_executor = getattr(driver, bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᔮ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1l1l1_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᔯ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1l1l1_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢᔰ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧᔱ"), None)
        return hub_url
    def bstack1l11llll1ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᔲ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1l1l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔳ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1l1l1_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᔴ")):
                setattr(command_executor, bstack1l1l1l1_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᔵ"), hub_url)
                result = True
        if result:
            self.bstack1l11lll1ll1_opy_ = hub_url
            bstack1llll111lll_opy_.bstack1lllll1111l_opy_(instance, bstack1llll111lll_opy_.bstack1l1l11lllll_opy_, hub_url)
            bstack1llll111lll_opy_.bstack1lllll1111l_opy_(
                instance, bstack1llll111lll_opy_.bstack1l11ll11lll_opy_, bstack1llll111lll_opy_.bstack1ll111l1l1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_]):
        return bstack1l1l1l1_opy_ (u"ࠧࡀࠢᔶ").join((bstack1lllll1l111_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1lllll1llll_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_], callback: Callable):
        bstack1l11l1ll1ll_opy_ = bstack1llll111lll_opy_.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l1ll1ll_opy_ in bstack1llll111lll_opy_.bstack11lllll1l1l_opy_:
            bstack1llll111lll_opy_.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_] = []
        bstack1llll111lll_opy_.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_].append(callback)
    def bstack1111111l11_opy_(self, instance: bstack1111111111_opy_, method_name: str, bstack1llllllll1l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1l1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᔷ")):
            return
        cmd = args[0] if method_name == bstack1l1l1l1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᔸ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11lllll1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣ࠼ࠥᔹ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥᔺ") + bstack11lllll1ll1_opy_, bstack1llllllll1l_opy_)
    def bstack1lllll1lll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111111l1_opy_, bstack1l11l1l1lll_opy_ = bstack1lllll11ll1_opy_
        bstack1l11l1ll1ll_opy_ = bstack1llll111lll_opy_.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔻ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧᔼ"))
        if bstack11111111l1_opy_ == bstack1lllll1l111_opy_.QUIT:
            if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.PRE:
                bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack11l1111l1l_opy_.value)
                bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, EVENTS.bstack11l1111l1l_opy_.value, bstack1ll111ll1l1_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᔽ").format(instance, method_name, bstack11111111l1_opy_, bstack1l11l1l1lll_opy_))
        if bstack11111111l1_opy_ == bstack1lllll1l111_opy_.bstack1111111lll_opy_:
            if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST and not bstack1llll111lll_opy_.bstack1l1l11lll1l_opy_ in instance.data:
                session_id = getattr(target, bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᔾ"), None)
                if session_id:
                    instance.data[bstack1llll111lll_opy_.bstack1l1l11lll1l_opy_] = session_id
        elif (
            bstack11111111l1_opy_ == bstack1lllll1l111_opy_.bstack1lllll11111_opy_
            and bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll111lll_opy_.bstack1l11lll111l_opy_
        ):
            if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.PRE:
                hub_url = bstack1llll111lll_opy_.bstack11l111llll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll111lll_opy_.bstack1l1l11lllll_opy_: hub_url,
                            bstack1llll111lll_opy_.bstack1l11ll11lll_opy_: bstack1llll111lll_opy_.bstack1ll111l1l1l_opy_(hub_url),
                            bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_: int(
                                os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᔿ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll111l11ll_opy_ = bstack1llll111lll_opy_.bstack1ll111l11l1_opy_(*args)
                bstack11lllll1lll_opy_ = bstack1ll111l11ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᕀ"), None) if bstack1ll111l11ll_opy_ else None
                if isinstance(bstack11lllll1lll_opy_, dict):
                    instance.data[bstack1llll111lll_opy_.bstack11llllll111_opy_] = copy.deepcopy(bstack11lllll1lll_opy_)
                    instance.data[bstack1llll111lll_opy_.bstack1l1l1l1lll1_opy_] = bstack11lllll1lll_opy_
            elif bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1l1l1_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᕁ"), dict()).get(bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᕂ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll111lll_opy_.bstack1l1l11lll1l_opy_: framework_session_id,
                                bstack1llll111lll_opy_.bstack11llllllll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111111l1_opy_ == bstack1lllll1l111_opy_.bstack1lllll11111_opy_
            and bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll111lll_opy_.bstack11llllll11l_opy_
            and bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST
        ):
            instance.data[bstack1llll111lll_opy_.bstack11llllll1ll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l1ll1ll_opy_ in bstack1llll111lll_opy_.bstack11lllll1l1l_opy_:
            bstack1l11l1llll1_opy_ = None
            for callback in bstack1llll111lll_opy_.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_]:
                try:
                    bstack1l11l1ll11l_opy_ = callback(self, target, exec, bstack1lllll11ll1_opy_, result, *args, **kwargs)
                    if bstack1l11l1llll1_opy_ == None:
                        bstack1l11l1llll1_opy_ = bstack1l11l1ll11l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᕃ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨᕄ"))
                    traceback.print_exc()
            if bstack11111111l1_opy_ == bstack1lllll1l111_opy_.QUIT:
                if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST:
                    bstack1ll111ll1l1_opy_ = bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, EVENTS.bstack11l1111l1l_opy_.value)
                    if bstack1ll111ll1l1_opy_!=None:
                        bstack1lll1ll11l1_opy_.end(EVENTS.bstack11l1111l1l_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᕅ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᕆ"), True, None)
            if bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.PRE and callable(bstack1l11l1llll1_opy_):
                return bstack1l11l1llll1_opy_
            elif bstack1l11l1l1lll_opy_ == bstack1lllll1llll_opy_.POST and bstack1l11l1llll1_opy_:
                return bstack1l11l1llll1_opy_
    def bstack111111l11l_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1l1l1l1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᕇ") or method_name == bstack1l1l1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᕈ"):
            return bstack1lllll1l111_opy_.bstack1111111lll_opy_
        if method_name == bstack1l1l1l1_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᕉ"):
            return bstack1lllll1l111_opy_.QUIT
        if method_name == bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᕊ"):
            if previous_state != bstack1lllll1l111_opy_.NONE:
                bstack1ll11lll1l1_opy_ = bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args)
                if bstack1ll11lll1l1_opy_ == bstack1llll111lll_opy_.bstack1l11lll111l_opy_:
                    return bstack1lllll1l111_opy_.bstack1111111lll_opy_
            return bstack1lllll1l111_opy_.bstack1lllll11111_opy_
        return bstack1lllll1l111_opy_.NONE