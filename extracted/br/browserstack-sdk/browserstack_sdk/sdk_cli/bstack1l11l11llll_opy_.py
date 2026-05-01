# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack11l1l1l1_opy_,
    bstack1l1ll111lll_opy_,
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils.constants import EVENTS
class bstack1l11lll111l_opy_(bstack11l1l1l1_opy_):
    bstack11l111lll11_opy_ = bstack111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ᫺")
    NAME = bstack111ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ᫻")
    bstack1ll1llll1_opy_ = bstack111ll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢ᫼")
    bstack1ll1111ll11_opy_ = bstack111ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ᫽")
    bstack111l1l1l1l1_opy_ = bstack111ll_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᫾")
    bstack1ll111ll_opy_ = bstack111ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᫿")
    bstack11l111lllll_opy_ = bstack111ll_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᬀ")
    bstack111l1l11l1l_opy_ = bstack111ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᬁ")
    bstack111l1l1l11l_opy_ = bstack111ll_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᬂ")
    bstack1l111111111_opy_ = bstack111ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᬃ")
    bstack11l11ll1lll_opy_ = bstack111ll_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᬄ")
    bstack111l1l1lll1_opy_ = bstack111ll_opy_ (u"ࠣࡩࡨࡸࠧᬅ")
    bstack11ll111l111_opy_ = bstack111ll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᬆ")
    bstack11l111l11ll_opy_ = bstack111ll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᬇ")
    bstack11l111l1l1l_opy_ = bstack111ll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᬈ")
    bstack111l1l11ll1_opy_ = bstack111ll_opy_ (u"ࠧࡷࡵࡪࡶࠥᬉ")
    bstack111l1l1ll11_opy_: Dict[str, List[Callable]] = dict()
    bstack11l1l11llll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l11lll1_opy_: Any
    bstack11l111l11l1_opy_: Dict
    def __init__(
        self,
        bstack11l1l11llll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l11l11lll1_opy_: Dict[str, Any],
        methods=[bstack111ll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᬊ"), bstack111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᬋ"), bstack111ll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᬌ"), bstack111ll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᬍ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11l1l11llll_opy_ = bstack11l1l11llll_opy_
        self.platform_index = platform_index
        self.bstack1l1ll1ll11l_opy_(methods)
        self.bstack1l11l11lll1_opy_ = bstack1l11l11lll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11l1l1l1_opy_.get_data(bstack1l11lll111l_opy_.bstack1ll1111ll11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11l1l1l1_opy_.get_data(bstack1l11lll111l_opy_.bstack1ll1llll1_opy_, target, strict)
    @staticmethod
    def bstack111l1l11lll_opy_(target: object, strict=True):
        return bstack11l1l1l1_opy_.get_data(bstack1l11lll111l_opy_.bstack111l1l1l1l1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11l1l1l1_opy_.get_data(bstack1l11lll111l_opy_.bstack1ll111ll_opy_, target, strict)
    @staticmethod
    def bstack11lll1ll11l_opy_(instance: bstack1l1ll111lll_opy_) -> bool:
        return bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack11l111lllll_opy_, False)
    @staticmethod
    def bstack1l11111l111_opy_(instance: bstack1l1ll111lll_opy_, default_value=None):
        return bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1ll1llll1_opy_, default_value)
    @staticmethod
    def bstack1l1111ll1l1_opy_(instance: bstack1l1ll111lll_opy_, default_value=None):
        return bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1ll111ll_opy_, default_value)
    @staticmethod
    def bstack11llll11ll1_opy_(hub_url: str, bstack111l1l1l1ll_opy_=bstack111ll_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᬎ")):
        try:
            bstack111l1l11l11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l1l11l11_opy_.endswith(bstack111l1l1l1ll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1111llll1_opy_(method_name: str):
        return method_name == bstack111ll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᬏ")
    @staticmethod
    def bstack11lllll111l_opy_(method_name: str, *args):
        return (
            bstack1l11lll111l_opy_.bstack1l1111llll1_opy_(method_name)
            and bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args) == bstack1l11lll111l_opy_.bstack11l11ll1lll_opy_
        )
    @staticmethod
    def bstack11llll1ll11_opy_(method_name: str, *args):
        if not bstack1l11lll111l_opy_.bstack1l1111llll1_opy_(method_name):
            return False
        if not bstack1l11lll111l_opy_.bstack11l111l11ll_opy_ in bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args):
            return False
        bstack11llll1111l_opy_ = bstack1l11lll111l_opy_.bstack11llll1l1ll_opy_(*args)
        return bstack11llll1111l_opy_ and bstack111ll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᬐ") in bstack11llll1111l_opy_ and bstack111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᬑ") in bstack11llll1111l_opy_[bstack111ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᬒ")]
    @staticmethod
    def bstack1l1111l1ll1_opy_(method_name: str, *args):
        if not bstack1l11lll111l_opy_.bstack1l1111llll1_opy_(method_name):
            return False
        if not bstack1l11lll111l_opy_.bstack11l111l11ll_opy_ in bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args):
            return False
        bstack11llll1111l_opy_ = bstack1l11lll111l_opy_.bstack11llll1l1ll_opy_(*args)
        return (
            bstack11llll1111l_opy_
            and bstack111ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᬓ") in bstack11llll1111l_opy_
            and bstack111ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᬔ") in bstack11llll1111l_opy_[bstack111ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᬕ")]
        )
    @staticmethod
    def bstack11l11ll1l1l_opy_(*args):
        return str(bstack1l11lll111l_opy_.bstack1l111l1l1l1_opy_(*args)).lower()
    @staticmethod
    def bstack1l111l1l1l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11llll1l1ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1lllll1l1ll_opy_(driver):
        command_executor = getattr(driver, bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᬖ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack111ll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᬗ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack111ll_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢᬘ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack111ll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧᬙ"), None)
        return hub_url
    def bstack11l1l11l111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack111ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᬚ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack111ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᬛ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack111ll_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᬜ")):
                setattr(command_executor, bstack111ll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᬝ"), hub_url)
                result = True
        if result:
            self.bstack11l1l11llll_opy_ = hub_url
            bstack1l11lll111l_opy_.bstack11ll11l1_opy_(instance, bstack1l11lll111l_opy_.bstack1ll1llll1_opy_, hub_url)
            bstack1l11lll111l_opy_.bstack11ll11l1_opy_(
                instance, bstack1l11lll111l_opy_.bstack11l111lllll_opy_, bstack1l11lll111l_opy_.bstack11llll11ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_]):
        return bstack111ll_opy_ (u"ࠧࡀࠢᬞ").join((bstack1ll1l1111l_opy_(bstack1l1l1lll11l_opy_[0]).name, bstack1l1l111lll_opy_(bstack1l1l1lll11l_opy_[1]).name))
    @staticmethod
    def bstack1l111l1111l_opy_(bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_], callback: Callable):
        bstack11l111l1l11_opy_ = bstack1l11lll111l_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        if not bstack11l111l1l11_opy_ in bstack1l11lll111l_opy_.bstack111l1l1ll11_opy_:
            bstack1l11lll111l_opy_.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_] = []
        bstack1l11lll111l_opy_.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_].append(callback)
    def bstack1l1ll1ll111_opy_(self, instance: bstack1l1ll111lll_opy_, method_name: str, bstack1l1ll11lll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack111ll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᬟ")):
            return
        cmd = args[0] if method_name == bstack111ll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᬠ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l1l1llll_opy_ = bstack111ll_opy_ (u"ࠣ࠼ࠥᬡ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥᬢ") + bstack111l1l1llll_opy_, bstack1l1ll11lll1_opy_)
    def bstack1ll1ll111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l1l1llll1l_opy_, bstack11l111ll111_opy_ = bstack1l1l1lll11l_opy_
        bstack11l111l1l11_opy_ = bstack1l11lll111l_opy_.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᬣ") + str(kwargs) + bstack111ll_opy_ (u"ࠦࠧᬤ"))
        if bstack1l1l1llll1l_opy_ == bstack1ll1l1111l_opy_.QUIT:
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.PRE:
                bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111l1l1ll1l_opy_.value)
                bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, EVENTS.bstack111l1l1ll1l_opy_.value, bstack11111l11l_opy_)
                self.logger.debug(bstack111ll_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᬥ").format(instance, method_name, bstack1l1l1llll1l_opy_, bstack11l111ll111_opy_))
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST:
                bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111l1l1l111_opy_.value)
                bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, EVENTS.bstack111l1l1l111_opy_.value, bstack11111l11l_opy_)
        if bstack1l1l1llll1l_opy_ == bstack1ll1l1111l_opy_.bstack111l1ll111_opy_:
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST and not bstack1l11lll111l_opy_.bstack1ll1111ll11_opy_ in instance.data:
                session_id = getattr(target, bstack111ll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᬦ"), None)
                if session_id:
                    instance.data[bstack1l11lll111l_opy_.bstack1ll1111ll11_opy_] = session_id
        elif (
            bstack1l1l1llll1l_opy_ == bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_
            and bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args) == bstack1l11lll111l_opy_.bstack11l11ll1lll_opy_
        ):
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.PRE:
                hub_url = bstack1l11lll111l_opy_.bstack1lllll1l1ll_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1l11lll111l_opy_.bstack1ll1llll1_opy_: hub_url,
                            bstack1l11lll111l_opy_.bstack11l111lllll_opy_: bstack1l11lll111l_opy_.bstack11llll11ll1_opy_(hub_url),
                            bstack1l11lll111l_opy_.bstack1l111111111_opy_: int(
                                os.environ.get(bstack111ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᬧ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11llll1111l_opy_ = bstack1l11lll111l_opy_.bstack11llll1l1ll_opy_(*args)
                bstack111l1l11lll_opy_ = bstack11llll1111l_opy_.get(bstack111ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᬨ"), None) if bstack11llll1111l_opy_ else None
                if isinstance(bstack111l1l11lll_opy_, dict):
                    instance.data[bstack1l11lll111l_opy_.bstack111l1l1l1l1_opy_] = copy.deepcopy(bstack111l1l11lll_opy_)
                    instance.data[bstack1l11lll111l_opy_.bstack1ll111ll_opy_] = bstack111l1l11lll_opy_
            elif bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack111ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᬩ"), dict()).get(bstack111ll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᬪ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1l11lll111l_opy_.bstack1ll1111ll11_opy_: framework_session_id,
                                bstack1l11lll111l_opy_.bstack111l1l11l1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l1l1llll1l_opy_ == bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_
            and bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args) == bstack1l11lll111l_opy_.bstack111l1l11ll1_opy_
            and bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST
        ):
            instance.data[bstack1l11lll111l_opy_.bstack111l1l1l11l_opy_] = datetime.now(tz=timezone.utc)
        if bstack11l111l1l11_opy_ in bstack1l11lll111l_opy_.bstack111l1l1ll11_opy_:
            bstack11l111ll11l_opy_ = None
            for callback in bstack1l11lll111l_opy_.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_]:
                try:
                    bstack11l111l1ll1_opy_ = callback(self, target, exec, bstack1l1l1lll11l_opy_, result, *args, **kwargs)
                    if bstack11l111ll11l_opy_ == None:
                        bstack11l111ll11l_opy_ = bstack11l111l1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᬫ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᬬ"))
                    traceback.print_exc()
            if bstack1l1l1llll1l_opy_ == bstack1ll1l1111l_opy_.QUIT:
                if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.PRE:
                    bstack11111l11l_opy_ = bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, EVENTS.bstack111l1l1ll1l_opy_.value)
                    if bstack11111l11l_opy_!=None:
                        bstack111l1l1l_opy_.end(EVENTS.bstack111l1l1ll1l_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᬭ"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᬮ"), True, None)
                if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST:
                    bstack11111l11l_opy_ = bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, EVENTS.bstack111l1l1l111_opy_.value)
                    if bstack11111l11l_opy_!=None:
                        bstack111l1l1l_opy_.end(EVENTS.bstack111l1l1l111_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᬯ"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᬰ"), True, None)
            if bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.PRE and callable(bstack11l111ll11l_opy_):
                return bstack11l111ll11l_opy_
            elif bstack11l111ll111_opy_ == bstack1l1l111lll_opy_.POST and bstack11l111ll11l_opy_:
                return bstack11l111ll11l_opy_
    def bstack1l1ll1l111l_opy_(
        self, method_name, previous_state: bstack1ll1l1111l_opy_, *args, **kwargs
    ) -> bstack1ll1l1111l_opy_:
        if method_name == bstack111ll_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᬱ") or method_name == bstack111ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᬲ"):
            return bstack1ll1l1111l_opy_.bstack111l1ll111_opy_
        if method_name == bstack111ll_opy_ (u"ࠧࡷࡵࡪࡶࠥᬳ"):
            return bstack1ll1l1111l_opy_.QUIT
        if method_name == bstack111ll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫᬴ࠢ"):
            if previous_state != bstack1ll1l1111l_opy_.NONE:
                command_name = bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args)
                if command_name == bstack1l11lll111l_opy_.bstack11l11ll1lll_opy_:
                    return bstack1ll1l1111l_opy_.bstack111l1ll111_opy_
            return bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_
        return bstack1ll1l1111l_opy_.NONE