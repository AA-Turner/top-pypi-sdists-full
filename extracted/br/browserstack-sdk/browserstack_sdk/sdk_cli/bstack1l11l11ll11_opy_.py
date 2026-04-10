# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack11l1111ll_opy_,
    bstack1l1ll11ll11_opy_,
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.constants import EVENTS
class bstack1l11ll1llll_opy_(bstack11l1111ll_opy_):
    bstack11l11l11111_opy_ = bstack1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ᫐")
    NAME = bstack1ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ᫑")
    bstack11llll1l11_opy_ = bstack1ll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢ᫒")
    bstack1l1lllll11l_opy_ = bstack1ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ᫓")
    bstack111l1ll1111_opy_ = bstack1ll_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᫔")
    bstack11l1111l1l_opy_ = bstack1ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᫕")
    bstack11l11l1l1l1_opy_ = bstack1ll_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤ᫖")
    bstack111l1l1llll_opy_ = bstack1ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣ᫗")
    bstack111l1ll1l11_opy_ = bstack1ll_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢ᫘")
    bstack1l1111l11l1_opy_ = bstack1ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢ᫙")
    bstack11l1l111l1l_opy_ = bstack1ll_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦ᫚")
    bstack111l1l1ll1l_opy_ = bstack1ll_opy_ (u"ࠣࡩࡨࡸࠧ᫛")
    bstack11ll1lll11l_opy_ = bstack1ll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᫜")
    bstack11l111llll1_opy_ = bstack1ll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨ᫝")
    bstack11l111lll1l_opy_ = bstack1ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧ᫞")
    bstack111l1ll111l_opy_ = bstack1ll_opy_ (u"ࠧࡷࡵࡪࡶࠥ᫟")
    bstack111l1ll1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack11l1l1111l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1l11ll11l_opy_: Any
    bstack11l11l1111l_opy_: Dict
    def __init__(
        self,
        bstack11l1l1111l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1l11ll11l_opy_: Dict[str, Any],
        methods=[bstack1ll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣ᫠"), bstack1ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ᫡"), bstack1ll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤ᫢"), bstack1ll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢ᫣")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l1l1111l1_opy_ = bstack11l1l1111l1_opy_
        self.platform_index = platform_index
        self.bstack1l1ll1ll1l1_opy_(methods)
        self.bstack1l1l11ll11l_opy_ = bstack1l1l11ll11l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11l1111ll_opy_.get_data(bstack1l11ll1llll_opy_.bstack1l1lllll11l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11l1111ll_opy_.get_data(bstack1l11ll1llll_opy_.bstack11llll1l11_opy_, target, strict)
    @staticmethod
    def bstack111l1ll11l1_opy_(target: object, strict=True):
        return bstack11l1111ll_opy_.get_data(bstack1l11ll1llll_opy_.bstack111l1ll1111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11l1111ll_opy_.get_data(bstack1l11ll1llll_opy_.bstack11l1111l1l_opy_, target, strict)
    @staticmethod
    def bstack11llll111l1_opy_(instance: bstack1l1ll11ll11_opy_) -> bool:
        return bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack11l11l1l1l1_opy_, False)
    @staticmethod
    def bstack11lllll11ll_opy_(instance: bstack1l1ll11ll11_opy_, default_value=None):
        return bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack11llll1l11_opy_, default_value)
    @staticmethod
    def bstack1l111l1ll1l_opy_(instance: bstack1l1ll11ll11_opy_, default_value=None):
        return bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack11l1111l1l_opy_, default_value)
    @staticmethod
    def bstack11llll1ll11_opy_(hub_url: str, bstack111l1l1l1ll_opy_=bstack1ll_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢ᫤")):
        try:
            bstack111l1ll1ll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1ll1ll1_opy_.endswith(bstack111l1l1l1ll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l111ll1l1l_opy_(method_name: str):
        return method_name == bstack1ll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧ᫥")
    @staticmethod
    def bstack1l11111l1l1_opy_(method_name: str, *args):
        return (
            bstack1l11ll1llll_opy_.bstack1l111ll1l1l_opy_(method_name)
            and bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args) == bstack1l11ll1llll_opy_.bstack11l1l111l1l_opy_
        )
    @staticmethod
    def bstack1l1111ll111_opy_(method_name: str, *args):
        if not bstack1l11ll1llll_opy_.bstack1l111ll1l1l_opy_(method_name):
            return False
        if not bstack1l11ll1llll_opy_.bstack11l111llll1_opy_ in bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args):
            return False
        bstack11llll1l111_opy_ = bstack1l11ll1llll_opy_.bstack11llll1llll_opy_(*args)
        return bstack11llll1l111_opy_ and bstack1ll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᫦") in bstack11llll1l111_opy_ and bstack1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᫧") in bstack11llll1l111_opy_[bstack1ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᫨")]
    @staticmethod
    def bstack11lllll1lll_opy_(method_name: str, *args):
        if not bstack1l11ll1llll_opy_.bstack1l111ll1l1l_opy_(method_name):
            return False
        if not bstack1l11ll1llll_opy_.bstack11l111llll1_opy_ in bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args):
            return False
        bstack11llll1l111_opy_ = bstack1l11ll1llll_opy_.bstack11llll1llll_opy_(*args)
        return (
            bstack11llll1l111_opy_
            and bstack1ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ᫩") in bstack11llll1l111_opy_
            and bstack1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧ᫪") in bstack11llll1l111_opy_[bstack1ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᫫")]
        )
    @staticmethod
    def bstack11l11lll11l_opy_(*args):
        return str(bstack1l11ll1llll_opy_.bstack11lllllll11_opy_(*args)).lower()
    @staticmethod
    def bstack11lllllll11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11llll1llll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1lll11l111_opy_(driver):
        command_executor = getattr(driver, bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᫬"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1ll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥ᫭"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1ll_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢ᫮"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1ll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧ᫯"), None)
        return hub_url
    def bstack11l11ll11ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᫰"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᫱"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1ll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣ᫲")):
                setattr(command_executor, bstack1ll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤ᫳"), hub_url)
                result = True
        if result:
            self.bstack11l1l1111l1_opy_ = hub_url
            bstack1l11ll1llll_opy_.bstack1l1l1l1l_opy_(instance, bstack1l11ll1llll_opy_.bstack11llll1l11_opy_, hub_url)
            bstack1l11ll1llll_opy_.bstack1l1l1l1l_opy_(
                instance, bstack1l11ll1llll_opy_.bstack11l11l1l1l1_opy_, bstack1l11ll1llll_opy_.bstack11llll1ll11_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_]):
        return bstack1ll_opy_ (u"ࠧࡀࠢ᫴").join((bstack1111ll1l11_opy_(bstack1l1ll1lll11_opy_[0]).name, bstack1llll11lll_opy_(bstack1l1ll1lll11_opy_[1]).name))
    @staticmethod
    def bstack1l1111111l1_opy_(bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_], callback: Callable):
        bstack11l111lllll_opy_ = bstack1l11ll1llll_opy_.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        if not bstack11l111lllll_opy_ in bstack1l11ll1llll_opy_.bstack111l1ll1l1l_opy_:
            bstack1l11ll1llll_opy_.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_] = []
        bstack1l11ll1llll_opy_.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_].append(callback)
    def bstack1l1lll11111_opy_(self, instance: bstack1l1ll11ll11_opy_, method_name: str, bstack1l1lll111l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1ll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨ᫵")):
            return
        cmd = args[0] if method_name == bstack1ll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣ᫶") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l1l1lll1_opy_ = bstack1ll_opy_ (u"ࠣ࠼ࠥ᫷").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥ᫸") + bstack111l1l1lll1_opy_, bstack1l1lll111l1_opy_)
    def bstack1l1l1ll1ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll1l11l1_opy_, bstack11l11l111ll_opy_ = bstack1l1ll1lll11_opy_
        bstack11l111lllll_opy_ = bstack1l11ll1llll_opy_.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᫹") + str(kwargs) + bstack1ll_opy_ (u"ࠦࠧ᫺"))
        if bstack1l1ll1l11l1_opy_ == bstack1111ll1l11_opy_.QUIT:
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.PRE:
                bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111l1l1ll11_opy_.value)
                bstack11l1111ll_opy_.bstack1l1l1l1l_opy_(instance, EVENTS.bstack111l1l1ll11_opy_.value, bstack1lll1lll11_opy_)
                self.logger.debug(bstack1ll_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤ᫻").format(instance, method_name, bstack1l1ll1l11l1_opy_, bstack11l11l111ll_opy_))
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST:
                bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111l1ll11ll_opy_.value)
                bstack11l1111ll_opy_.bstack1l1l1l1l_opy_(instance, EVENTS.bstack111l1ll11ll_opy_.value, bstack1lll1lll11_opy_)
        if bstack1l1ll1l11l1_opy_ == bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_:
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST and not bstack1l11ll1llll_opy_.bstack1l1lllll11l_opy_ in instance.data:
                session_id = getattr(target, bstack1ll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥ᫼"), None)
                if session_id:
                    instance.data[bstack1l11ll1llll_opy_.bstack1l1lllll11l_opy_] = session_id
        elif (
            bstack1l1ll1l11l1_opy_ == bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_
            and bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args) == bstack1l11ll1llll_opy_.bstack11l1l111l1l_opy_
        ):
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.PRE:
                hub_url = bstack1l11ll1llll_opy_.bstack1lll11l111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l11ll1llll_opy_.bstack11llll1l11_opy_: hub_url,
                            bstack1l11ll1llll_opy_.bstack11l11l1l1l1_opy_: bstack1l11ll1llll_opy_.bstack11llll1ll11_opy_(hub_url),
                            bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_: int(
                                os.environ.get(bstack1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢ᫽"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11llll1l111_opy_ = bstack1l11ll1llll_opy_.bstack11llll1llll_opy_(*args)
                bstack111l1ll11l1_opy_ = bstack11llll1l111_opy_.get(bstack1ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᫾"), None) if bstack11llll1l111_opy_ else None
                if isinstance(bstack111l1ll11l1_opy_, dict):
                    instance.data[bstack1l11ll1llll_opy_.bstack111l1ll1111_opy_] = copy.deepcopy(bstack111l1ll11l1_opy_)
                    instance.data[bstack1l11ll1llll_opy_.bstack11l1111l1l_opy_] = bstack111l1ll11l1_opy_
            elif bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣ᫿"), dict()).get(bstack1ll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᬀ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l11ll1llll_opy_.bstack1l1lllll11l_opy_: framework_session_id,
                                bstack1l11ll1llll_opy_.bstack111l1l1llll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1ll1l11l1_opy_ == bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_
            and bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args) == bstack1l11ll1llll_opy_.bstack111l1ll111l_opy_
            and bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST
        ):
            instance.data[bstack1l11ll1llll_opy_.bstack111l1ll1l11_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l111lllll_opy_ in bstack1l11ll1llll_opy_.bstack111l1ll1l1l_opy_:
            bstack11l111ll1l1_opy_ = None
            for callback in bstack1l11ll1llll_opy_.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_]:
                try:
                    bstack11l111lll11_opy_ = callback(self, target, exec, bstack1l1ll1lll11_opy_, result, *args, **kwargs)
                    if bstack11l111ll1l1_opy_ == None:
                        bstack11l111ll1l1_opy_ = bstack11l111lll11_opy_
                except Exception as e:
                    self.logger.error(bstack1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᬁ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᬂ"))
                    traceback.print_exc()
            if bstack1l1ll1l11l1_opy_ == bstack1111ll1l11_opy_.QUIT:
                if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.PRE:
                    bstack1lll1lll11_opy_ = bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, EVENTS.bstack111l1l1ll11_opy_.value)
                    if bstack1lll1lll11_opy_!=None:
                        bstack1l11l1ll11_opy_.end(EVENTS.bstack111l1l1ll11_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᬃ"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᬄ"), True, None)
                if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST:
                    bstack1lll1lll11_opy_ = bstack11l1111ll_opy_.bstack1ll11111l11_opy_(instance, EVENTS.bstack111l1ll11ll_opy_.value)
                    if bstack1lll1lll11_opy_!=None:
                        bstack1l11l1ll11_opy_.end(EVENTS.bstack111l1ll11ll_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᬅ"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᬆ"), True, None)
            if bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.PRE and callable(bstack11l111ll1l1_opy_):
                return bstack11l111ll1l1_opy_
            elif bstack11l11l111ll_opy_ == bstack1llll11lll_opy_.POST and bstack11l111ll1l1_opy_:
                return bstack11l111ll1l1_opy_
    def bstack1l1ll1ll111_opy_(
        self, method_name, previous_state: bstack1111ll1l11_opy_, *args, **kwargs
    ) -> bstack1111ll1l11_opy_:
        if method_name == bstack1ll_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᬇ") or method_name == bstack1ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᬈ"):
            return bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_
        if method_name == bstack1ll_opy_ (u"ࠧࡷࡵࡪࡶࠥᬉ"):
            return bstack1111ll1l11_opy_.QUIT
        if method_name == bstack1ll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᬊ"):
            if previous_state != bstack1111ll1l11_opy_.NONE:
                command_name = bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args)
                if command_name == bstack1l11ll1llll_opy_.bstack11l1l111l1l_opy_:
                    return bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_
            return bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_
        return bstack1111ll1l11_opy_.NONE