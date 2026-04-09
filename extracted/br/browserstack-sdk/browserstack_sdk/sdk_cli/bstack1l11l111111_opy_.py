# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack1lll1111ll_opy_,
    bstack1l1lll111ll_opy_,
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from bstack_utils.constants import EVENTS
class bstack1l1l1ll11ll_opy_(bstack1lll1111ll_opy_):
    bstack11l11l11111_opy_ = bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᫍ")
    NAME = bstack11ll11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᫎ")
    bstack1111l1l11_opy_ = bstack11ll11_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦ᫏")
    bstack1ll111l11l1_opy_ = bstack11ll11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ᫐")
    bstack111l1ll1111_opy_ = bstack11ll11_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᫑")
    bstack11ll1l111l_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᫒")
    bstack11l11l1l1ll_opy_ = bstack11ll11_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨ᫓")
    bstack111l1ll11l1_opy_ = bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧ᫔")
    bstack111l1lll111_opy_ = bstack11ll11_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦ᫕")
    bstack1l111l1lll1_opy_ = bstack11ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦ᫖")
    bstack11l1l1l1lll_opy_ = bstack11ll11_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᫗")
    bstack111l1ll1lll_opy_ = bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࠤ᫘")
    bstack11lll1ll111_opy_ = bstack11ll11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᫙")
    bstack11l111llll1_opy_ = bstack11ll11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥ᫚")
    bstack11l11l1111l_opy_ = bstack11ll11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤ᫛")
    bstack111l1lll1ll_opy_ = bstack11ll11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢ᫜")
    bstack111l1ll1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack11l1l11ll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l111l11_opy_: Any
    bstack11l11l111l1_opy_: Dict
    def __init__(
        self,
        bstack11l1l11ll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l11l111l11_opy_: Dict[str, Any],
        methods=[bstack11ll11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧ᫝"), bstack11ll11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦ᫞"), bstack11ll11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨ᫟"), bstack11ll11_opy_ (u"ࠨࡱࡶ࡫ࡷࠦ᫠")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l1l11ll11_opy_ = bstack11l1l11ll11_opy_
        self.platform_index = platform_index
        self.bstack1l1ll1l111l_opy_(methods)
        self.bstack1l11l111l11_opy_ = bstack1l11l111l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll1111ll_opy_.get_data(bstack1l1l1ll11ll_opy_.bstack1ll111l11l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll1111ll_opy_.get_data(bstack1l1l1ll11ll_opy_.bstack1111l1l11_opy_, target, strict)
    @staticmethod
    def bstack111l1ll111l_opy_(target: object, strict=True):
        return bstack1lll1111ll_opy_.get_data(bstack1l1l1ll11ll_opy_.bstack111l1ll1111_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll1111ll_opy_.get_data(bstack1l1l1ll11ll_opy_.bstack11ll1l111l_opy_, target, strict)
    @staticmethod
    def bstack11lll1llll1_opy_(instance: bstack1l1lll111ll_opy_) -> bool:
        return bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11l11l1l1ll_opy_, False)
    @staticmethod
    def bstack11llllll1l1_opy_(instance: bstack1l1lll111ll_opy_, default_value=None):
        return bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1111l1l11_opy_, default_value)
    @staticmethod
    def bstack11lllllll1l_opy_(instance: bstack1l1lll111ll_opy_, default_value=None):
        return bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11ll1l111l_opy_, default_value)
    @staticmethod
    def bstack11llll1l1l1_opy_(hub_url: str, bstack111l1ll1l1l_opy_=bstack11ll11_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᫡")):
        try:
            bstack111l1lll11l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1lll11l_opy_.endswith(bstack111l1ll1l1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l111l1l1l1_opy_(method_name: str):
        return method_name == bstack11ll11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤ᫢")
    @staticmethod
    def bstack1l111111ll1_opy_(method_name: str, *args):
        return (
            bstack1l1l1ll11ll_opy_.bstack1l111l1l1l1_opy_(method_name)
            and bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args) == bstack1l1l1ll11ll_opy_.bstack11l1l1l1lll_opy_
        )
    @staticmethod
    def bstack1l11111111l_opy_(method_name: str, *args):
        if not bstack1l1l1ll11ll_opy_.bstack1l111l1l1l1_opy_(method_name):
            return False
        if not bstack1l1l1ll11ll_opy_.bstack11l111llll1_opy_ in bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args):
            return False
        bstack11llll1l11l_opy_ = bstack1l1l1ll11ll_opy_.bstack11llll1lll1_opy_(*args)
        return bstack11llll1l11l_opy_ and bstack11ll11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ᫣") in bstack11llll1l11l_opy_ and bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᫤") in bstack11llll1l11l_opy_[bstack11ll11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ᫥")]
    @staticmethod
    def bstack1l111111lll_opy_(method_name: str, *args):
        if not bstack1l1l1ll11ll_opy_.bstack1l111l1l1l1_opy_(method_name):
            return False
        if not bstack1l1l1ll11ll_opy_.bstack11l111llll1_opy_ in bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args):
            return False
        bstack11llll1l11l_opy_ = bstack1l1l1ll11ll_opy_.bstack11llll1lll1_opy_(*args)
        return (
            bstack11llll1l11l_opy_
            and bstack11ll11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᫦") in bstack11llll1l11l_opy_
            and bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤ᫧") in bstack11llll1l11l_opy_[bstack11ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᫨")]
        )
    @staticmethod
    def bstack11l11llll11_opy_(*args):
        return str(bstack1l1l1ll11ll_opy_.bstack1l111ll11ll_opy_(*args)).lower()
    @staticmethod
    def bstack1l111ll11ll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11llll1lll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack111ll11l11_opy_(driver):
        command_executor = getattr(driver, bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᫩"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11ll11_opy_ (u"ࠤࡢࡹࡷࡲࠢ᫪"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11ll11_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦ᫫"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11ll11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤ᫬"), None)
        return hub_url
    def bstack11l1l1l1l11_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᫭"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᫮"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11ll11_opy_ (u"ࠢࡠࡷࡵࡰࠧ᫯")):
                setattr(command_executor, bstack11ll11_opy_ (u"ࠣࡡࡸࡶࡱࠨ᫰"), hub_url)
                result = True
        if result:
            self.bstack11l1l11ll11_opy_ = hub_url
            bstack1l1l1ll11ll_opy_.bstack1l1l1111l1_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1111l1l11_opy_, hub_url)
            bstack1l1l1ll11ll_opy_.bstack1l1l1111l1_opy_(
                instance, bstack1l1l1ll11ll_opy_.bstack11l11l1l1ll_opy_, bstack1l1l1ll11ll_opy_.bstack11llll1l1l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_]):
        return bstack11ll11_opy_ (u"ࠤ࠽ࠦ᫱").join((bstack11111l1ll_opy_(bstack1l1ll1l11l1_opy_[0]).name, bstack111llll1ll_opy_(bstack1l1ll1l11l1_opy_[1]).name))
    @staticmethod
    def bstack1l111l11l11_opy_(bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_], callback: Callable):
        bstack11l11l11l11_opy_ = bstack1l1l1ll11ll_opy_.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        if not bstack11l11l11l11_opy_ in bstack1l1l1ll11ll_opy_.bstack111l1ll1ll1_opy_:
            bstack1l1l1ll11ll_opy_.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_] = []
        bstack1l1l1ll11ll_opy_.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_].append(callback)
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1l1lll111ll_opy_, method_name: str, bstack1l1ll111l11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11ll11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥ᫲")):
            return
        cmd = args[0] if method_name == bstack11ll11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧ᫳") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l1ll1l11_opy_ = bstack11ll11_opy_ (u"ࠧࡀࠢ᫴").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢ᫵") + bstack111l1ll1l11_opy_, bstack1l1ll111l11_opy_)
    def bstack1l1lll11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1ll111lll_opy_, bstack11l11l111ll_opy_ = bstack1l1ll1l11l1_opy_
        bstack11l11l11l11_opy_ = bstack1l1l1ll11ll_opy_.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᫶") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤ᫷"))
        if bstack1l1ll111lll_opy_ == bstack11111l1ll_opy_.QUIT:
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.PRE:
                bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack111l1ll11ll_opy_.value)
                bstack1lll1111ll_opy_.bstack1l1l1111l1_opy_(instance, EVENTS.bstack111l1ll11ll_opy_.value, bstack1111l1ll1l_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨ᫸").format(instance, method_name, bstack1l1ll111lll_opy_, bstack11l11l111ll_opy_))
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST:
                bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack111l1lll1l1_opy_.value)
                bstack1lll1111ll_opy_.bstack1l1l1111l1_opy_(instance, EVENTS.bstack111l1lll1l1_opy_.value, bstack1111l1ll1l_opy_)
        if bstack1l1ll111lll_opy_ == bstack11111l1ll_opy_.bstack1ll11lll1_opy_:
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST and not bstack1l1l1ll11ll_opy_.bstack1ll111l11l1_opy_ in instance.data:
                session_id = getattr(target, bstack11ll11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ᫹"), None)
                if session_id:
                    instance.data[bstack1l1l1ll11ll_opy_.bstack1ll111l11l1_opy_] = session_id
        elif (
            bstack1l1ll111lll_opy_ == bstack11111l1ll_opy_.bstack1ll1111lll1_opy_
            and bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args) == bstack1l1l1ll11ll_opy_.bstack11l1l1l1lll_opy_
        ):
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.PRE:
                hub_url = bstack1l1l1ll11ll_opy_.bstack111ll11l11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l1l1ll11ll_opy_.bstack1111l1l11_opy_: hub_url,
                            bstack1l1l1ll11ll_opy_.bstack11l11l1l1ll_opy_: bstack1l1l1ll11ll_opy_.bstack11llll1l1l1_opy_(hub_url),
                            bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_: int(
                                os.environ.get(bstack11ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ᫺"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11llll1l11l_opy_ = bstack1l1l1ll11ll_opy_.bstack11llll1lll1_opy_(*args)
                bstack111l1ll111l_opy_ = bstack11llll1l11l_opy_.get(bstack11ll11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᫻"), None) if bstack11llll1l11l_opy_ else None
                if isinstance(bstack111l1ll111l_opy_, dict):
                    instance.data[bstack1l1l1ll11ll_opy_.bstack111l1ll1111_opy_] = copy.deepcopy(bstack111l1ll111l_opy_)
                    instance.data[bstack1l1l1ll11ll_opy_.bstack11ll1l111l_opy_] = bstack111l1ll111l_opy_
            elif bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11ll11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧ᫼"), dict()).get(bstack11ll11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥ᫽"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l1l1ll11ll_opy_.bstack1ll111l11l1_opy_: framework_session_id,
                                bstack1l1l1ll11ll_opy_.bstack111l1ll11l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1ll111lll_opy_ == bstack11111l1ll_opy_.bstack1ll1111lll1_opy_
            and bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args) == bstack1l1l1ll11ll_opy_.bstack111l1lll1ll_opy_
            and bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST
        ):
            instance.data[bstack1l1l1ll11ll_opy_.bstack111l1lll111_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l11l11l11_opy_ in bstack1l1l1ll11ll_opy_.bstack111l1ll1ll1_opy_:
            bstack11l11l11ll1_opy_ = None
            for callback in bstack1l1l1ll11ll_opy_.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_]:
                try:
                    bstack11l11l1l111_opy_ = callback(self, target, exec, bstack1l1ll1l11l1_opy_, result, *args, **kwargs)
                    if bstack11l11l11ll1_opy_ == None:
                        bstack11l11l11ll1_opy_ = bstack11l11l1l111_opy_
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨ᫾") + str(e) + bstack11ll11_opy_ (u"ࠤࠥ᫿"))
                    traceback.print_exc()
            if bstack1l1ll111lll_opy_ == bstack11111l1ll_opy_.QUIT:
                if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.PRE:
                    bstack1111l1ll1l_opy_ = bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, EVENTS.bstack111l1ll11ll_opy_.value)
                    if bstack1111l1ll1l_opy_!=None:
                        bstack1ll111lll_opy_.end(EVENTS.bstack111l1ll11ll_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᬀ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᬁ"), True, None)
                if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST:
                    bstack1111l1ll1l_opy_ = bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, EVENTS.bstack111l1lll1l1_opy_.value)
                    if bstack1111l1ll1l_opy_!=None:
                        bstack1ll111lll_opy_.end(EVENTS.bstack111l1lll1l1_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᬂ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᬃ"), True, None)
            if bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.PRE and callable(bstack11l11l11ll1_opy_):
                return bstack11l11l11ll1_opy_
            elif bstack11l11l111ll_opy_ == bstack111llll1ll_opy_.POST and bstack11l11l11ll1_opy_:
                return bstack11l11l11ll1_opy_
    def bstack1l1lll111l1_opy_(
        self, method_name, previous_state: bstack11111l1ll_opy_, *args, **kwargs
    ) -> bstack11111l1ll_opy_:
        if method_name == bstack11ll11_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᬄ") or method_name == bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᬅ"):
            return bstack11111l1ll_opy_.bstack1ll11lll1_opy_
        if method_name == bstack11ll11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᬆ"):
            return bstack11111l1ll_opy_.QUIT
        if method_name == bstack11ll11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᬇ"):
            if previous_state != bstack11111l1ll_opy_.NONE:
                command_name = bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args)
                if command_name == bstack1l1l1ll11ll_opy_.bstack11l1l1l1lll_opy_:
                    return bstack11111l1ll_opy_.bstack1ll11lll1_opy_
            return bstack11111l1ll_opy_.bstack1ll1111lll1_opy_
        return bstack11111l1ll_opy_.NONE