# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1lll11ll1l1_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.constants import EVENTS
class bstack1l1lllll1l1_opy_(bstack1lll11ll1l1_opy_):
    bstack11lll11l1ll_opy_ = bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ᝞")
    NAME = bstack11l1l11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ᝟")
    bstack1l111l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᝠ")
    bstack1l111l1l111_opy_ = bstack11l1l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᝡ")
    bstack11l1ll1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᝢ")
    bstack1l1111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᝣ")
    bstack11lll1lll11_opy_ = bstack11l1l11_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᝤ")
    bstack11l1ll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᝥ")
    bstack11l1ll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᝦ")
    bstack1l1l1l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᝧ")
    bstack11lllll1lll_opy_ = bstack11l1l11_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᝨ")
    bstack11l1ll1lll1_opy_ = bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࠧᝩ")
    bstack1l11l1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᝪ")
    bstack11lll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᝫ")
    bstack11lll11l11l_opy_ = bstack11l1l11_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᝬ")
    bstack11l1ll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡷࡵࡪࡶࠥ᝭")
    bstack11l1ll1ll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack11llllll1ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll111l1l1l_opy_: Any
    bstack11lll1l11l1_opy_: Dict
    def __init__(
        self,
        bstack11llllll1ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll111l1l1l_opy_: Dict[str, Any],
        methods=[bstack11l1l11_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᝮ"), bstack11l1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᝯ"), bstack11l1l11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᝰ"), bstack11l1l11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢ᝱")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11llllll1ll_opy_ = bstack11llllll1ll_opy_
        self.platform_index = platform_index
        self.bstack1ll1lll11l1_opy_(methods)
        self.bstack1ll111l1l1l_opy_ = bstack1ll111l1l1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lll11ll1l1_opy_.get_data(bstack1l1lllll1l1_opy_.bstack1l111l1l111_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lll11ll1l1_opy_.get_data(bstack1l1lllll1l1_opy_.bstack1l111l1l11l_opy_, target, strict)
    @staticmethod
    def bstack11l1ll11l11_opy_(target: object, strict=True):
        return bstack1lll11ll1l1_opy_.get_data(bstack1l1lllll1l1_opy_.bstack11l1ll1l1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lll11ll1l1_opy_.get_data(bstack1l1lllll1l1_opy_.bstack1l1111ll11l_opy_, target, strict)
    @staticmethod
    def bstack1l1l1111l11_opy_(instance: bstack1ll1llll111_opy_) -> bool:
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack11lll1lll11_opy_, False)
    @staticmethod
    def bstack1l1l11ll1ll_opy_(instance: bstack1ll1llll111_opy_, default_value=None):
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l111l1l11l_opy_, default_value)
    @staticmethod
    def bstack1l1l11ll1l1_opy_(instance: bstack1ll1llll111_opy_, default_value=None):
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1111ll11l_opy_, default_value)
    @staticmethod
    def bstack1l1l11l11l1_opy_(hub_url: str, bstack11l1ll1llll_opy_=bstack11l1l11_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᝲ")):
        try:
            bstack11l1ll11lll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1ll11lll_opy_.endswith(bstack11l1ll1llll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(method_name: str):
        return method_name == bstack11l1l11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᝳ")
    @staticmethod
    def bstack1l1ll1111l1_opy_(method_name: str, *args):
        return (
            bstack1l1lllll1l1_opy_.bstack1l1ll1ll1ll_opy_(method_name)
            and bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args) == bstack1l1lllll1l1_opy_.bstack11lllll1lll_opy_
        )
    @staticmethod
    def bstack1l1l1l1111l_opy_(method_name: str, *args):
        if not bstack1l1lllll1l1_opy_.bstack1l1ll1ll1ll_opy_(method_name):
            return False
        if not bstack1l1lllll1l1_opy_.bstack11lll11ll1l_opy_ in bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111llll_opy_ = bstack1l1lllll1l1_opy_.bstack1l1l11l1l11_opy_(*args)
        return bstack1l1l111llll_opy_ and bstack11l1l11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᝴") in bstack1l1l111llll_opy_ and bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᝵") in bstack1l1l111llll_opy_[bstack11l1l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᝶")]
    @staticmethod
    def bstack1l1l1llll1l_opy_(method_name: str, *args):
        if not bstack1l1lllll1l1_opy_.bstack1l1ll1ll1ll_opy_(method_name):
            return False
        if not bstack1l1lllll1l1_opy_.bstack11lll11ll1l_opy_ in bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111llll_opy_ = bstack1l1lllll1l1_opy_.bstack1l1l11l1l11_opy_(*args)
        return (
            bstack1l1l111llll_opy_
            and bstack11l1l11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ᝷") in bstack1l1l111llll_opy_
            and bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧ᝸") in bstack1l1l111llll_opy_[bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᝹")]
        )
    @staticmethod
    def bstack11llll1l111_opy_(*args):
        return str(bstack1l1lllll1l1_opy_.bstack1l1l1l11lll_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l1l11lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l11l1l11_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l11111111_opy_(driver):
        command_executor = getattr(driver, bstack11l1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᝺"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1l11_opy_ (u"ࠧࡥࡵࡳ࡮ࠥ᝻"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1l11_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢ᝼"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1l11_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧ᝽"), None)
        return hub_url
    def bstack11llll11l1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᝾"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᝿"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1l11_opy_ (u"ࠥࡣࡺࡸ࡬ࠣក")):
                setattr(command_executor, bstack11l1l11_opy_ (u"ࠦࡤࡻࡲ࡭ࠤខ"), hub_url)
                result = True
        if result:
            self.bstack11llllll1ll_opy_ = hub_url
            bstack1l1lllll1l1_opy_.bstack1lll111ll11_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l111l1l11l_opy_, hub_url)
            bstack1l1lllll1l1_opy_.bstack1lll111ll11_opy_(
                instance, bstack1l1lllll1l1_opy_.bstack11lll1lll11_opy_, bstack1l1lllll1l1_opy_.bstack1l1l11l11l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11lll11ll11_opy_(bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_]):
        return bstack11l1l11_opy_ (u"ࠧࡀࠢគ").join((bstack1ll1lll1lll_opy_(bstack1lll11ll111_opy_[0]).name, bstack1lll11l111l_opy_(bstack1lll11ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1l11lll1l_opy_(bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_], callback: Callable):
        bstack11lll11lll1_opy_ = bstack1l1lllll1l1_opy_.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        if not bstack11lll11lll1_opy_ in bstack1l1lllll1l1_opy_.bstack11l1ll1ll1l_opy_:
            bstack1l1lllll1l1_opy_.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_] = []
        bstack1l1lllll1l1_opy_.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_].append(callback)
    def bstack1ll1ll1l1l1_opy_(self, instance: bstack1ll1llll111_opy_, method_name: str, bstack1lll11l1111_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨឃ")):
            return
        cmd = args[0] if method_name == bstack11l1l11_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣង") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1ll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠣ࠼ࠥច").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥឆ") + bstack11l1ll1l11l_opy_, bstack1lll11l1111_opy_)
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll111111l_opy_, bstack11lll1l111l_opy_ = bstack1lll11ll111_opy_
        bstack11lll11lll1_opy_ = bstack1l1lllll1l1_opy_.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥជ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧឈ"))
        if bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.QUIT:
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.PRE:
                bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11l1ll1l111_opy_.value)
                bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, EVENTS.bstack11l1ll1l111_opy_.value, bstack1l1l1l1111_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤញ").format(instance, method_name, bstack1lll111111l_opy_, bstack11lll1l111l_opy_))
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST:
                bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11l1ll1l1l1_opy_.value)
                bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, EVENTS.bstack11l1ll1l1l1_opy_.value, bstack1l1l1l1111_opy_)
        if bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_:
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST and not bstack1l1lllll1l1_opy_.bstack1l111l1l111_opy_ in instance.data:
                session_id = getattr(target, bstack11l1l11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥដ"), None)
                if session_id:
                    instance.data[bstack1l1lllll1l1_opy_.bstack1l111l1l111_opy_] = session_id
        elif (
            bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_
            and bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args) == bstack1l1lllll1l1_opy_.bstack11lllll1lll_opy_
        ):
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.PRE:
                hub_url = bstack1l1lllll1l1_opy_.bstack1l11111111_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l1lllll1l1_opy_.bstack1l111l1l11l_opy_: hub_url,
                            bstack1l1lllll1l1_opy_.bstack11lll1lll11_opy_: bstack1l1lllll1l1_opy_.bstack1l1l11l11l1_opy_(hub_url),
                            bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_: int(
                                os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢឋ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l111llll_opy_ = bstack1l1lllll1l1_opy_.bstack1l1l11l1l11_opy_(*args)
                bstack11l1ll11l11_opy_ = bstack1l1l111llll_opy_.get(bstack11l1l11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢឌ"), None) if bstack1l1l111llll_opy_ else None
                if isinstance(bstack11l1ll11l11_opy_, dict):
                    instance.data[bstack1l1lllll1l1_opy_.bstack11l1ll1l1ll_opy_] = copy.deepcopy(bstack11l1ll11l11_opy_)
                    instance.data[bstack1l1lllll1l1_opy_.bstack1l1111ll11l_opy_] = bstack11l1ll11l11_opy_
            elif bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1l11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣឍ"), dict()).get(bstack11l1l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨណ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l1lllll1l1_opy_.bstack1l111l1l111_opy_: framework_session_id,
                                bstack1l1lllll1l1_opy_.bstack11l1ll11ll1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_
            and bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args) == bstack1l1lllll1l1_opy_.bstack11l1ll11l1l_opy_
            and bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST
        ):
            instance.data[bstack1l1lllll1l1_opy_.bstack11l1ll1ll11_opy_] = datetime.now(tz=timezone.utc)
        if bstack11lll11lll1_opy_ in bstack1l1lllll1l1_opy_.bstack11l1ll1ll1l_opy_:
            bstack11lll11llll_opy_ = None
            for callback in bstack1l1lllll1l1_opy_.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_]:
                try:
                    bstack11lll11l1l1_opy_ = callback(self, target, exec, bstack1lll11ll111_opy_, result, *args, **kwargs)
                    if bstack11lll11llll_opy_ == None:
                        bstack11lll11llll_opy_ = bstack11lll11l1l1_opy_
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤត") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨថ"))
                    traceback.print_exc()
            if bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.QUIT:
                if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.PRE:
                    bstack1l1l1l1111_opy_ = bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, EVENTS.bstack11l1ll1l111_opy_.value)
                    if bstack1l1l1l1111_opy_!=None:
                        bstack11ll1l1l1_opy_.end(EVENTS.bstack11l1ll1l111_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨទ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧធ"), True, None)
                if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST:
                    bstack1l1l1l1111_opy_ = bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, EVENTS.bstack11l1ll1l1l1_opy_.value)
                    if bstack1l1l1l1111_opy_!=None:
                        bstack11ll1l1l1_opy_.end(EVENTS.bstack11l1ll1l1l1_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣន"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢប"), True, None)
            if bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.PRE and callable(bstack11lll11llll_opy_):
                return bstack11lll11llll_opy_
            elif bstack11lll1l111l_opy_ == bstack1lll11l111l_opy_.POST and bstack11lll11llll_opy_:
                return bstack11lll11llll_opy_
    def bstack1lll11l1lll_opy_(
        self, method_name, previous_state: bstack1ll1lll1lll_opy_, *args, **kwargs
    ) -> bstack1ll1lll1lll_opy_:
        if method_name == bstack11l1l11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧផ") or method_name == bstack11l1l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦព"):
            return bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_
        if method_name == bstack11l1l11_opy_ (u"ࠧࡷࡵࡪࡶࠥភ"):
            return bstack1ll1lll1lll_opy_.QUIT
        if method_name == bstack11l1l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢម"):
            if previous_state != bstack1ll1lll1lll_opy_.NONE:
                command_name = bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args)
                if command_name == bstack1l1lllll1l1_opy_.bstack11lllll1lll_opy_:
                    return bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_
            return bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_
        return bstack1ll1lll1lll_opy_.NONE