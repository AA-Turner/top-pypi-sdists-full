# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1ll11l11_opy_,
    bstack1ll1l1ll1ll_opy_,
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from bstack_utils.constants import EVENTS
class bstack1l1llllllll_opy_(bstack1ll1ll11l11_opy_):
    bstack11lll1111l1_opy_ = bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ᝔")
    NAME = bstack11l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᝕")
    bstack1l11111lll1_opy_ = bstack11l11_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦ᝖")
    bstack1l1111ll1ll_opy_ = bstack11l11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ᝗")
    bstack11l1l1lll1l_opy_ = bstack11l11_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᝘")
    bstack1l1111l1lll_opy_ = bstack11l11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᝙")
    bstack11lll11l1ll_opy_ = bstack11l11_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨ᝚")
    bstack11l1l1l1ll1_opy_ = bstack11l11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧ᝛")
    bstack11l1l1lllll_opy_ = bstack11l11_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦ᝜")
    bstack1l1l111l11l_opy_ = bstack11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦ᝝")
    bstack11llll111l1_opy_ = bstack11l11_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᝞")
    bstack11l1l1ll1l1_opy_ = bstack11l11_opy_ (u"ࠧ࡭ࡥࡵࠤ᝟")
    bstack1l11l11111l_opy_ = bstack11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᝠ")
    bstack11ll1lll1ll_opy_ = bstack11l11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᝡ")
    bstack11lll111111_opy_ = bstack11l11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᝢ")
    bstack11l1l1ll111_opy_ = bstack11l11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᝣ")
    bstack11l1l1l1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack11lll1l1l1l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1llll111l_opy_: Any
    bstack11lll11111l_opy_: Dict
    def __init__(
        self,
        bstack11lll1l1l1l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1llll111l_opy_: Dict[str, Any],
        methods=[bstack11l11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᝤ"), bstack11l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᝥ"), bstack11l11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᝦ"), bstack11l11_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᝧ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11lll1l1l1l_opy_ = bstack11lll1l1l1l_opy_
        self.platform_index = platform_index
        self.bstack1ll1llllll1_opy_(methods)
        self.bstack1l1llll111l_opy_ = bstack1l1llll111l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1ll11l11_opy_.get_data(bstack1l1llllllll_opy_.bstack1l1111ll1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1ll11l11_opy_.get_data(bstack1l1llllllll_opy_.bstack1l11111lll1_opy_, target, strict)
    @staticmethod
    def bstack11l1l1l1lll_opy_(target: object, strict=True):
        return bstack1ll1ll11l11_opy_.get_data(bstack1l1llllllll_opy_.bstack11l1l1lll1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1ll11l11_opy_.get_data(bstack1l1llllllll_opy_.bstack1l1111l1lll_opy_, target, strict)
    @staticmethod
    def bstack1l11lllll11_opy_(instance: bstack1ll1l1ll1ll_opy_) -> bool:
        return bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack11lll11l1ll_opy_, False)
    @staticmethod
    def bstack1l1l1ll1l1l_opy_(instance: bstack1ll1l1ll1ll_opy_, default_value=None):
        return bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l11111lll1_opy_, default_value)
    @staticmethod
    def bstack1l1l1l111l1_opy_(instance: bstack1ll1l1ll1ll_opy_, default_value=None):
        return bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1111l1lll_opy_, default_value)
    @staticmethod
    def bstack1l1l1111lll_opy_(hub_url: str, bstack11l1l1llll1_opy_=bstack11l11_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᝨ")):
        try:
            bstack11l1l1lll11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1l1lll11_opy_.endswith(bstack11l1l1llll1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(method_name: str):
        return method_name == bstack11l11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᝩ")
    @staticmethod
    def bstack1l1l11l1lll_opy_(method_name: str, *args):
        return (
            bstack1l1llllllll_opy_.bstack1l1l1l1ll1l_opy_(method_name)
            and bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args) == bstack1l1llllllll_opy_.bstack11llll111l1_opy_
        )
    @staticmethod
    def bstack1l1l1llllll_opy_(method_name: str, *args):
        if not bstack1l1llllllll_opy_.bstack1l1l1l1ll1l_opy_(method_name):
            return False
        if not bstack1l1llllllll_opy_.bstack11ll1lll1ll_opy_ in bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1l1llllllll_opy_.bstack1l1l1111111_opy_(*args)
        return bstack1l11lllllll_opy_ and bstack11l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᝪ") in bstack1l11lllllll_opy_ and bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᝫ") in bstack1l11lllllll_opy_[bstack11l11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᝬ")]
    @staticmethod
    def bstack1l1l1l1lll1_opy_(method_name: str, *args):
        if not bstack1l1llllllll_opy_.bstack1l1l1l1ll1l_opy_(method_name):
            return False
        if not bstack1l1llllllll_opy_.bstack11ll1lll1ll_opy_ in bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args):
            return False
        bstack1l11lllllll_opy_ = bstack1l1llllllll_opy_.bstack1l1l1111111_opy_(*args)
        return (
            bstack1l11lllllll_opy_
            and bstack11l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᝭") in bstack1l11lllllll_opy_
            and bstack11l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᝮ") in bstack1l11lllllll_opy_[bstack11l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᝯ")]
        )
    @staticmethod
    def bstack11lllll1ll1_opy_(*args):
        return str(bstack1l1llllllll_opy_.bstack1l1l11ll11l_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l11ll11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l1111111_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1llll1ll_opy_(driver):
        command_executor = getattr(driver, bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᝰ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l11_opy_ (u"ࠤࡢࡹࡷࡲࠢ᝱"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l11_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᝲ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᝳ"), None)
        return hub_url
    def bstack11lllll111l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᝴"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᝵"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l11_opy_ (u"ࠢࡠࡷࡵࡰࠧ᝶")):
                setattr(command_executor, bstack11l11_opy_ (u"ࠣࡡࡸࡶࡱࠨ᝷"), hub_url)
                result = True
        if result:
            self.bstack11lll1l1l1l_opy_ = hub_url
            bstack1l1llllllll_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l11111lll1_opy_, hub_url)
            bstack1l1llllllll_opy_.bstack1ll1lll111l_opy_(
                instance, bstack1l1llllllll_opy_.bstack11lll11l1ll_opy_, bstack1l1llllllll_opy_.bstack1l1l1111lll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_]):
        return bstack11l11_opy_ (u"ࠤ࠽ࠦ᝸").join((bstack1ll1lllllll_opy_(bstack1ll1l1lll1l_opy_[0]).name, bstack1ll1l1llll1_opy_(bstack1ll1l1lll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1l111ll_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_], callback: Callable):
        bstack11ll1llll11_opy_ = bstack1l1llllllll_opy_.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        if not bstack11ll1llll11_opy_ in bstack1l1llllllll_opy_.bstack11l1l1l1l1l_opy_:
            bstack1l1llllllll_opy_.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_] = []
        bstack1l1llllllll_opy_.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_].append(callback)
    def bstack1ll1lll1ll1_opy_(self, instance: bstack1ll1l1ll1ll_opy_, method_name: str, bstack1ll1ll1l111_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥ᝹")):
            return
        cmd = args[0] if method_name == bstack11l11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧ᝺") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1l1ll11l_opy_ = bstack11l11_opy_ (u"ࠧࡀࠢ᝻").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢ᝼") + bstack11l1l1ll11l_opy_, bstack1ll1ll1l111_opy_)
    def bstack1ll1ll11ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1lll11ll_opy_, bstack11ll1lll1l1_opy_ = bstack1ll1l1lll1l_opy_
        bstack11ll1llll11_opy_ = bstack1l1llllllll_opy_.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᝽") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤ᝾"))
        if bstack1ll1lll11ll_opy_ == bstack1ll1lllllll_opy_.QUIT:
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.PRE:
                bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l1l1l1l11_opy_.value)
                bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, EVENTS.bstack11l1l1l1l11_opy_.value, bstack1l111l111l_opy_)
                self.logger.debug(bstack11l11_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨ᝿").format(instance, method_name, bstack1ll1lll11ll_opy_, bstack11ll1lll1l1_opy_))
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST:
                bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l1l1ll1ll_opy_.value)
                bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, EVENTS.bstack11l1l1ll1ll_opy_.value, bstack1l111l111l_opy_)
        if bstack1ll1lll11ll_opy_ == bstack1ll1lllllll_opy_.bstack1lll1111111_opy_:
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST and not bstack1l1llllllll_opy_.bstack1l1111ll1ll_opy_ in instance.data:
                session_id = getattr(target, bstack11l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢក"), None)
                if session_id:
                    instance.data[bstack1l1llllllll_opy_.bstack1l1111ll1ll_opy_] = session_id
        elif (
            bstack1ll1lll11ll_opy_ == bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_
            and bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args) == bstack1l1llllllll_opy_.bstack11llll111l1_opy_
        ):
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.PRE:
                hub_url = bstack1l1llllllll_opy_.bstack1l1llll1ll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l1llllllll_opy_.bstack1l11111lll1_opy_: hub_url,
                            bstack1l1llllllll_opy_.bstack11lll11l1ll_opy_: bstack1l1llllllll_opy_.bstack1l1l1111lll_opy_(hub_url),
                            bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_: int(
                                os.environ.get(bstack11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦខ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11lllllll_opy_ = bstack1l1llllllll_opy_.bstack1l1l1111111_opy_(*args)
                bstack11l1l1l1lll_opy_ = bstack1l11lllllll_opy_.get(bstack11l11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦគ"), None) if bstack1l11lllllll_opy_ else None
                if isinstance(bstack11l1l1l1lll_opy_, dict):
                    instance.data[bstack1l1llllllll_opy_.bstack11l1l1lll1l_opy_] = copy.deepcopy(bstack11l1l1l1lll_opy_)
                    instance.data[bstack1l1llllllll_opy_.bstack1l1111l1lll_opy_] = bstack11l1l1l1lll_opy_
            elif bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧឃ"), dict()).get(bstack11l11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥង"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l1llllllll_opy_.bstack1l1111ll1ll_opy_: framework_session_id,
                                bstack1l1llllllll_opy_.bstack11l1l1l1ll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1lll11ll_opy_ == bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_
            and bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args) == bstack1l1llllllll_opy_.bstack11l1l1ll111_opy_
            and bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST
        ):
            instance.data[bstack1l1llllllll_opy_.bstack11l1l1lllll_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll1llll11_opy_ in bstack1l1llllllll_opy_.bstack11l1l1l1l1l_opy_:
            bstack11ll1lllll1_opy_ = None
            for callback in bstack1l1llllllll_opy_.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_]:
                try:
                    bstack11lll1111ll_opy_ = callback(self, target, exec, bstack1ll1l1lll1l_opy_, result, *args, **kwargs)
                    if bstack11ll1lllll1_opy_ == None:
                        bstack11ll1lllll1_opy_ = bstack11lll1111ll_opy_
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨច") + str(e) + bstack11l11_opy_ (u"ࠤࠥឆ"))
                    traceback.print_exc()
            if bstack1ll1lll11ll_opy_ == bstack1ll1lllllll_opy_.QUIT:
                if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.PRE:
                    bstack1l111l111l_opy_ = bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, EVENTS.bstack11l1l1l1l11_opy_.value)
                    if bstack1l111l111l_opy_!=None:
                        bstack111l1lllll_opy_.end(EVENTS.bstack11l1l1l1l11_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥជ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤឈ"), True, None)
                if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST:
                    bstack1l111l111l_opy_ = bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, EVENTS.bstack11l1l1ll1ll_opy_.value)
                    if bstack1l111l111l_opy_!=None:
                        bstack111l1lllll_opy_.end(EVENTS.bstack11l1l1ll1ll_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧញ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦដ"), True, None)
            if bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.PRE and callable(bstack11ll1lllll1_opy_):
                return bstack11ll1lllll1_opy_
            elif bstack11ll1lll1l1_opy_ == bstack1ll1l1llll1_opy_.POST and bstack11ll1lllll1_opy_:
                return bstack11ll1lllll1_opy_
    def bstack1ll1ll1lll1_opy_(
        self, method_name, previous_state: bstack1ll1lllllll_opy_, *args, **kwargs
    ) -> bstack1ll1lllllll_opy_:
        if method_name == bstack11l11_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤឋ") or method_name == bstack11l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣឌ"):
            return bstack1ll1lllllll_opy_.bstack1lll1111111_opy_
        if method_name == bstack11l11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢឍ"):
            return bstack1ll1lllllll_opy_.QUIT
        if method_name == bstack11l11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦណ"):
            if previous_state != bstack1ll1lllllll_opy_.NONE:
                command_name = bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args)
                if command_name == bstack1l1llllllll_opy_.bstack11llll111l1_opy_:
                    return bstack1ll1lllllll_opy_.bstack1lll1111111_opy_
            return bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_
        return bstack1ll1lllllll_opy_.NONE