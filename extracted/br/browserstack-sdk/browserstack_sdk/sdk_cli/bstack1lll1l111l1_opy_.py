# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1llllll1111_opy_,
    bstack1111111l1l_opy_,
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1lllllll_opy_(bstack1llllll1111_opy_):
    bstack1l11l1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᔲ")
    NAME = bstack11ll1l1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᔳ")
    bstack1l1l11lllll_opy_ = bstack11ll1l1_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᔴ")
    bstack1l1l11l11ll_opy_ = bstack11ll1l1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᔵ")
    bstack11lllll11ll_opy_ = bstack11ll1l1_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᔶ")
    bstack1l1l1l11111_opy_ = bstack11ll1l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔷ")
    bstack1l11l1lllll_opy_ = bstack11ll1l1_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨᔸ")
    bstack11llll1llll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᔹ")
    bstack11lllll111l_opy_ = bstack11ll1l1_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᔺ")
    bstack1ll111ll11l_opy_ = bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᔻ")
    bstack1l11ll1l111_opy_ = bstack11ll1l1_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣᔼ")
    bstack11lllll1111_opy_ = bstack11ll1l1_opy_ (u"ࠧ࡭ࡥࡵࠤᔽ")
    bstack1l1lll111ll_opy_ = bstack11ll1l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᔾ")
    bstack1l11l1l1l11_opy_ = bstack11ll1l1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᔿ")
    bstack1l11l1l1lll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᕀ")
    bstack11llll1ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᕁ")
    bstack11lllll1l11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1ll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1llll1l1_opy_: Any
    bstack1l11l11lll1_opy_: Dict
    def __init__(
        self,
        bstack1l11ll1ll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1llll1l1_opy_: Dict[str, Any],
        methods=[bstack11ll1l1_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᕂ"), bstack11ll1l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᕃ"), bstack11ll1l1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᕄ"), bstack11ll1l1_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᕅ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll1ll11_opy_ = bstack1l11ll1ll11_opy_
        self.platform_index = platform_index
        self.bstack1lllll1lll1_opy_(methods)
        self.bstack1ll1llll1l1_opy_ = bstack1ll1llll1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1lllllll_opy_.bstack1l1l11l11ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, target, strict)
    @staticmethod
    def bstack11llll1lll1_opy_(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1lllllll_opy_.bstack11lllll11ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllll1111_opy_.get_data(bstack1ll1lllllll_opy_.bstack1l1l1l11111_opy_, target, strict)
    @staticmethod
    def bstack1l1lllll11l_opy_(instance: bstack1111111l1l_opy_) -> bool:
        return bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1l11l1lllll_opy_, False)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, default_value)
    @staticmethod
    def bstack1ll11l1llll_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1ll11111ll1_opy_(hub_url: str, bstack11llll1ll11_opy_=bstack11ll1l1_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᕆ")):
        try:
            bstack11lllll11l1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11lllll11l1_opy_.endswith(bstack11llll1ll11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11l1lll1_opy_(method_name: str):
        return method_name == bstack11ll1l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᕇ")
    @staticmethod
    def bstack1ll11l1111l_opy_(method_name: str, *args):
        return (
            bstack1ll1lllllll_opy_.bstack1ll11l1lll1_opy_(method_name)
            and bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1lllllll_opy_.bstack1l11ll1l111_opy_
        )
    @staticmethod
    def bstack1ll1l111l1l_opy_(method_name: str, *args):
        if not bstack1ll1lllllll_opy_.bstack1ll11l1lll1_opy_(method_name):
            return False
        if not bstack1ll1lllllll_opy_.bstack1l11l1l1l11_opy_ in bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1ll1lllllll_opy_.bstack1ll1111ll11_opy_(*args)
        return bstack1ll1111lll1_opy_ and bstack11ll1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᕈ") in bstack1ll1111lll1_opy_ and bstack11ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᕉ") in bstack1ll1111lll1_opy_[bstack11ll1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᕊ")]
    @staticmethod
    def bstack1ll11llll1l_opy_(method_name: str, *args):
        if not bstack1ll1lllllll_opy_.bstack1ll11l1lll1_opy_(method_name):
            return False
        if not bstack1ll1lllllll_opy_.bstack1l11l1l1l11_opy_ in bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args):
            return False
        bstack1ll1111lll1_opy_ = bstack1ll1lllllll_opy_.bstack1ll1111ll11_opy_(*args)
        return (
            bstack1ll1111lll1_opy_
            and bstack11ll1l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᕋ") in bstack1ll1111lll1_opy_
            and bstack11ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᕌ") in bstack1ll1111lll1_opy_[bstack11ll1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᕍ")]
        )
    @staticmethod
    def bstack1l11ll1l11l_opy_(*args):
        return str(bstack1ll1lllllll_opy_.bstack1ll1l111ll1_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111ll1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1111ll11_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll11l11_opy_(driver):
        command_executor = getattr(driver, bstack11ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᕎ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11ll1l1_opy_ (u"ࠤࡢࡹࡷࡲࠢᕏ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11ll1l1_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᕐ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11ll1l1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᕑ"), None)
        return hub_url
    def bstack1l11llll1l1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11ll1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᕒ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11ll1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᕓ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11ll1l1_opy_ (u"ࠢࡠࡷࡵࡰࠧᕔ")):
                setattr(command_executor, bstack11ll1l1_opy_ (u"ࠣࡡࡸࡶࡱࠨᕕ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll1ll11_opy_ = hub_url
            bstack1ll1lllllll_opy_.bstack1lllll1ll1l_opy_(instance, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, hub_url)
            bstack1ll1lllllll_opy_.bstack1lllll1ll1l_opy_(
                instance, bstack1ll1lllllll_opy_.bstack1l11l1lllll_opy_, bstack1ll1lllllll_opy_.bstack1ll11111ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l11llll_opy_(bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_]):
        return bstack11ll1l1_opy_ (u"ࠤ࠽ࠦᕖ").join((bstack1lllll1ll11_opy_(bstack1llllllllll_opy_[0]).name, bstack1llllll1ll1_opy_(bstack1llllllllll_opy_[1]).name))
    @staticmethod
    def bstack1ll11l11lll_opy_(bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_], callback: Callable):
        bstack1l11l1l111l_opy_ = bstack1ll1lllllll_opy_.bstack1l11l11llll_opy_(bstack1llllllllll_opy_)
        if not bstack1l11l1l111l_opy_ in bstack1ll1lllllll_opy_.bstack11lllll1l11_opy_:
            bstack1ll1lllllll_opy_.bstack11lllll1l11_opy_[bstack1l11l1l111l_opy_] = []
        bstack1ll1lllllll_opy_.bstack11lllll1l11_opy_[bstack1l11l1l111l_opy_].append(callback)
    def bstack111111l111_opy_(self, instance: bstack1111111l1l_opy_, method_name: str, bstack1llll1llll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11ll1l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᕗ")):
            return
        cmd = args[0] if method_name == bstack11ll1l1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᕘ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11lllll1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠧࡀࠢᕙ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢᕚ") + bstack11lllll1l1l_opy_, bstack1llll1llll1_opy_)
    def bstack1llllll1l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111111lll_opy_, bstack1l11l1l11ll_opy_ = bstack1llllllllll_opy_
        bstack1l11l1l111l_opy_ = bstack1ll1lllllll_opy_.bstack1l11l11llll_opy_(bstack1llllllllll_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᕛ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠣࠤᕜ"))
        if bstack1111111lll_opy_ == bstack1lllll1ll11_opy_.QUIT:
            if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.PRE:
                bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1l1l111lll_opy_.value)
                bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, EVENTS.bstack1l1l111lll_opy_.value, bstack1ll11l111ll_opy_)
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᕝ").format(instance, method_name, bstack1111111lll_opy_, bstack1l11l1l11ll_opy_))
        if bstack1111111lll_opy_ == bstack1lllll1ll11_opy_.bstack11111111l1_opy_:
            if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST and not bstack1ll1lllllll_opy_.bstack1l1l11l11ll_opy_ in instance.data:
                session_id = getattr(target, bstack11ll1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᕞ"), None)
                if session_id:
                    instance.data[bstack1ll1lllllll_opy_.bstack1l1l11l11ll_opy_] = session_id
        elif (
            bstack1111111lll_opy_ == bstack1lllll1ll11_opy_.bstack1llllllll11_opy_
            and bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1lllllll_opy_.bstack1l11ll1l111_opy_
        ):
            if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.PRE:
                hub_url = bstack1ll1lllllll_opy_.bstack1ll11l11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_: hub_url,
                            bstack1ll1lllllll_opy_.bstack1l11l1lllll_opy_: bstack1ll1lllllll_opy_.bstack1ll11111ll1_opy_(hub_url),
                            bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_: int(
                                os.environ.get(bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᕟ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111lll1_opy_ = bstack1ll1lllllll_opy_.bstack1ll1111ll11_opy_(*args)
                bstack11llll1lll1_opy_ = bstack1ll1111lll1_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᕠ"), None) if bstack1ll1111lll1_opy_ else None
                if isinstance(bstack11llll1lll1_opy_, dict):
                    instance.data[bstack1ll1lllllll_opy_.bstack11lllll11ll_opy_] = copy.deepcopy(bstack11llll1lll1_opy_)
                    instance.data[bstack1ll1lllllll_opy_.bstack1l1l1l11111_opy_] = bstack11llll1lll1_opy_
            elif bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11ll1l1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᕡ"), dict()).get(bstack11ll1l1_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᕢ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1lllllll_opy_.bstack1l1l11l11ll_opy_: framework_session_id,
                                bstack1ll1lllllll_opy_.bstack11llll1llll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111111lll_opy_ == bstack1lllll1ll11_opy_.bstack1llllllll11_opy_
            and bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1lllllll_opy_.bstack11llll1ll1l_opy_
            and bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST
        ):
            instance.data[bstack1ll1lllllll_opy_.bstack11lllll111l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l1l111l_opy_ in bstack1ll1lllllll_opy_.bstack11lllll1l11_opy_:
            bstack1l11l1l11l1_opy_ = None
            for callback in bstack1ll1lllllll_opy_.bstack11lllll1l11_opy_[bstack1l11l1l111l_opy_]:
                try:
                    bstack1l11l1l1ll1_opy_ = callback(self, target, exec, bstack1llllllllll_opy_, result, *args, **kwargs)
                    if bstack1l11l1l11l1_opy_ == None:
                        bstack1l11l1l11l1_opy_ = bstack1l11l1l1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᕣ") + str(e) + bstack11ll1l1_opy_ (u"ࠤࠥᕤ"))
                    traceback.print_exc()
            if bstack1111111lll_opy_ == bstack1lllll1ll11_opy_.QUIT:
                if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST:
                    bstack1ll11l111ll_opy_ = bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, EVENTS.bstack1l1l111lll_opy_.value)
                    if bstack1ll11l111ll_opy_!=None:
                        bstack1llll11lll1_opy_.end(EVENTS.bstack1l1l111lll_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᕥ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᕦ"), True, None)
            if bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.PRE and callable(bstack1l11l1l11l1_opy_):
                return bstack1l11l1l11l1_opy_
            elif bstack1l11l1l11ll_opy_ == bstack1llllll1ll1_opy_.POST and bstack1l11l1l11l1_opy_:
                return bstack1l11l1l11l1_opy_
    def bstack1lllll1l1l1_opy_(
        self, method_name, previous_state: bstack1lllll1ll11_opy_, *args, **kwargs
    ) -> bstack1lllll1ll11_opy_:
        if method_name == bstack11ll1l1_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᕧ") or method_name == bstack11ll1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᕨ"):
            return bstack1lllll1ll11_opy_.bstack11111111l1_opy_
        if method_name == bstack11ll1l1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᕩ"):
            return bstack1lllll1ll11_opy_.QUIT
        if method_name == bstack11ll1l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᕪ"):
            if previous_state != bstack1lllll1ll11_opy_.NONE:
                bstack1ll1l11lll1_opy_ = bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args)
                if bstack1ll1l11lll1_opy_ == bstack1ll1lllllll_opy_.bstack1l11ll1l111_opy_:
                    return bstack1lllll1ll11_opy_.bstack11111111l1_opy_
            return bstack1lllll1ll11_opy_.bstack1llllllll11_opy_
        return bstack1lllll1ll11_opy_.NONE