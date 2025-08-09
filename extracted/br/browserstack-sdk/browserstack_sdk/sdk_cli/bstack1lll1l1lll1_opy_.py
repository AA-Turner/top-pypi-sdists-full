# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1lllll111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
from bstack_utils.constants import EVENTS
class bstack1llll1l11l1_opy_(bstack1lllll111ll_opy_):
    bstack1l11l11lll1_opy_ = bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᕱ")
    NAME = bstack11l1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᕲ")
    bstack1l1l1l11111_opy_ = bstack11l1_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᕳ")
    bstack1l1l11l1l11_opy_ = bstack11l1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᕴ")
    bstack11llll1ll11_opy_ = bstack11l1_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᕵ")
    bstack1l1l11l1lll_opy_ = bstack11l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕶ")
    bstack1l11l1lllll_opy_ = bstack11l1_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨᕷ")
    bstack11llll1l11l_opy_ = bstack11l1_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᕸ")
    bstack11llll1llll_opy_ = bstack11l1_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᕹ")
    bstack1ll11l1ll1l_opy_ = bstack11l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᕺ")
    bstack1l11ll1llll_opy_ = bstack11l1_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣᕻ")
    bstack11llll1ll1l_opy_ = bstack11l1_opy_ (u"ࠧ࡭ࡥࡵࠤᕼ")
    bstack1l1ll1ll1ll_opy_ = bstack11l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᕽ")
    bstack1l11l1l11ll_opy_ = bstack11l1_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᕾ")
    bstack1l11l1l1l11_opy_ = bstack11l1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᕿ")
    bstack11lllll111l_opy_ = bstack11l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᖀ")
    bstack11llll1l1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll111ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l1ll1l_opy_: Any
    bstack1l11l1l111l_opy_: Dict
    def __init__(
        self,
        bstack1l11ll111ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l1ll1l_opy_: Dict[str, Any],
        methods=[bstack11l1_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᖁ"), bstack11l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᖂ"), bstack11l1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᖃ"), bstack11l1_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᖄ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11ll111ll_opy_ = bstack1l11ll111ll_opy_
        self.platform_index = platform_index
        self.bstack1111111111_opy_(methods)
        self.bstack1lll1l1ll1l_opy_ = bstack1lll1l1ll1l_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lllll111ll_opy_.get_data(bstack1llll1l11l1_opy_.bstack1l1l11l1l11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lllll111ll_opy_.get_data(bstack1llll1l11l1_opy_.bstack1l1l1l11111_opy_, target, strict)
    @staticmethod
    def bstack11lllll11l1_opy_(target: object, strict=True):
        return bstack1lllll111ll_opy_.get_data(bstack1llll1l11l1_opy_.bstack11llll1ll11_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lllll111ll_opy_.get_data(bstack1llll1l11l1_opy_.bstack1l1l11l1lll_opy_, target, strict)
    @staticmethod
    def bstack1ll11111l11_opy_(instance: bstack1lllll1ll1l_opy_) -> bool:
        return bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1l11l1lllll_opy_, False)
    @staticmethod
    def bstack1ll111ll1ll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1l1l1l11111_opy_, default_value)
    @staticmethod
    def bstack1ll11l1llll_opy_(instance: bstack1lllll1ll1l_opy_, default_value=None):
        return bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1l1l11l1lll_opy_, default_value)
    @staticmethod
    def bstack1ll1111l1ll_opy_(hub_url: str, bstack11lllll1111_opy_=bstack11l1_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᖅ")):
        try:
            bstack11llll1l1ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11llll1l1ll_opy_.endswith(bstack11lllll1111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str):
        return method_name == bstack11l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᖆ")
    @staticmethod
    def bstack1ll111l1111_opy_(method_name: str, *args):
        return (
            bstack1llll1l11l1_opy_.bstack1ll11ll111l_opy_(method_name)
            and bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args) == bstack1llll1l11l1_opy_.bstack1l11ll1llll_opy_
        )
    @staticmethod
    def bstack1ll11ll11ll_opy_(method_name: str, *args):
        if not bstack1llll1l11l1_opy_.bstack1ll11ll111l_opy_(method_name):
            return False
        if not bstack1llll1l11l1_opy_.bstack1l11l1l11ll_opy_ in bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args):
            return False
        bstack1ll1111llll_opy_ = bstack1llll1l11l1_opy_.bstack1ll11111lll_opy_(*args)
        return bstack1ll1111llll_opy_ and bstack11l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᖇ") in bstack1ll1111llll_opy_ and bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᖈ") in bstack1ll1111llll_opy_[bstack11l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᖉ")]
    @staticmethod
    def bstack1ll1l1111l1_opy_(method_name: str, *args):
        if not bstack1llll1l11l1_opy_.bstack1ll11ll111l_opy_(method_name):
            return False
        if not bstack1llll1l11l1_opy_.bstack1l11l1l11ll_opy_ in bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args):
            return False
        bstack1ll1111llll_opy_ = bstack1llll1l11l1_opy_.bstack1ll11111lll_opy_(*args)
        return (
            bstack1ll1111llll_opy_
            and bstack11l1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᖊ") in bstack1ll1111llll_opy_
            and bstack11l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᖋ") in bstack1ll1111llll_opy_[bstack11l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᖌ")]
        )
    @staticmethod
    def bstack1l11lllll11_opy_(*args):
        return str(bstack1llll1l11l1_opy_.bstack1ll1l11l11l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l11l11l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11111lll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1llll1l11_opy_(driver):
        command_executor = getattr(driver, bstack11l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᖍ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11l1_opy_ (u"ࠤࡢࡹࡷࡲࠢᖎ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11l1_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᖏ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11l1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᖐ"), None)
        return hub_url
    def bstack1l11lll1ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖑ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᖒ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11l1_opy_ (u"ࠢࡠࡷࡵࡰࠧᖓ")):
                setattr(command_executor, bstack11l1_opy_ (u"ࠣࡡࡸࡶࡱࠨᖔ"), hub_url)
                result = True
        if result:
            self.bstack1l11ll111ll_opy_ = hub_url
            bstack1llll1l11l1_opy_.bstack1111111lll_opy_(instance, bstack1llll1l11l1_opy_.bstack1l1l1l11111_opy_, hub_url)
            bstack1llll1l11l1_opy_.bstack1111111lll_opy_(
                instance, bstack1llll1l11l1_opy_.bstack1l11l1lllll_opy_, bstack1llll1l11l1_opy_.bstack1ll1111l1ll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_]):
        return bstack11l1_opy_ (u"ࠤ࠽ࠦᖕ").join((bstack1llllllllll_opy_(bstack1lllllll11l_opy_[0]).name, bstack1llll1lll11_opy_(bstack1lllllll11l_opy_[1]).name))
    @staticmethod
    def bstack1ll11lll111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_], callback: Callable):
        bstack1l11l1l11l1_opy_ = bstack1llll1l11l1_opy_.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        if not bstack1l11l1l11l1_opy_ in bstack1llll1l11l1_opy_.bstack11llll1l1l1_opy_:
            bstack1llll1l11l1_opy_.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_] = []
        bstack1llll1l11l1_opy_.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_].append(callback)
    def bstack1111111ll1_opy_(self, instance: bstack1lllll1ll1l_opy_, method_name: str, bstack1llllll11l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᖖ")):
            return
        cmd = args[0] if method_name == bstack11l1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᖗ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11llll1lll1_opy_ = bstack11l1_opy_ (u"ࠧࡀࠢᖘ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll11lll11_opy_(bstack11l1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢᖙ") + bstack11llll1lll1_opy_, bstack1llllll11l1_opy_)
    def bstack1111111l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1llll1lll1l_opy_, bstack1l11l11llll_opy_ = bstack1lllllll11l_opy_
        bstack1l11l1l11l1_opy_ = bstack1llll1l11l1_opy_.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        self.logger.debug(bstack11l1_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᖚ") + str(kwargs) + bstack11l1_opy_ (u"ࠣࠤᖛ"))
        if bstack1llll1lll1l_opy_ == bstack1llllllllll_opy_.QUIT:
            if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.PRE:
                bstack1ll111llll1_opy_ = bstack1ll1ll11111_opy_.bstack1ll11lll11l_opy_(EVENTS.bstack1l1l11lll1_opy_.value)
                bstack1lllll111ll_opy_.bstack1111111lll_opy_(instance, EVENTS.bstack1l1l11lll1_opy_.value, bstack1ll111llll1_opy_)
                self.logger.debug(bstack11l1_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᖜ").format(instance, method_name, bstack1llll1lll1l_opy_, bstack1l11l11llll_opy_))
        if bstack1llll1lll1l_opy_ == bstack1llllllllll_opy_.bstack1llllll11ll_opy_:
            if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST and not bstack1llll1l11l1_opy_.bstack1l1l11l1l11_opy_ in instance.data:
                session_id = getattr(target, bstack11l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᖝ"), None)
                if session_id:
                    instance.data[bstack1llll1l11l1_opy_.bstack1l1l11l1l11_opy_] = session_id
        elif (
            bstack1llll1lll1l_opy_ == bstack1llllllllll_opy_.bstack1llllll111l_opy_
            and bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args) == bstack1llll1l11l1_opy_.bstack1l11ll1llll_opy_
        ):
            if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.PRE:
                hub_url = bstack1llll1l11l1_opy_.bstack1llll1l11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll1l11l1_opy_.bstack1l1l1l11111_opy_: hub_url,
                            bstack1llll1l11l1_opy_.bstack1l11l1lllll_opy_: bstack1llll1l11l1_opy_.bstack1ll1111l1ll_opy_(hub_url),
                            bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_: int(
                                os.environ.get(bstack11l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᖞ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1111llll_opy_ = bstack1llll1l11l1_opy_.bstack1ll11111lll_opy_(*args)
                bstack11lllll11l1_opy_ = bstack1ll1111llll_opy_.get(bstack11l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᖟ"), None) if bstack1ll1111llll_opy_ else None
                if isinstance(bstack11lllll11l1_opy_, dict):
                    instance.data[bstack1llll1l11l1_opy_.bstack11llll1ll11_opy_] = copy.deepcopy(bstack11lllll11l1_opy_)
                    instance.data[bstack1llll1l11l1_opy_.bstack1l1l11l1lll_opy_] = bstack11lllll11l1_opy_
            elif bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11l1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᖠ"), dict()).get(bstack11l1_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᖡ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll1l11l1_opy_.bstack1l1l11l1l11_opy_: framework_session_id,
                                bstack1llll1l11l1_opy_.bstack11llll1l11l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1llll1lll1l_opy_ == bstack1llllllllll_opy_.bstack1llllll111l_opy_
            and bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args) == bstack1llll1l11l1_opy_.bstack11lllll111l_opy_
            and bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST
        ):
            instance.data[bstack1llll1l11l1_opy_.bstack11llll1llll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11l1l11l1_opy_ in bstack1llll1l11l1_opy_.bstack11llll1l1l1_opy_:
            bstack1l11l11ll11_opy_ = None
            for callback in bstack1llll1l11l1_opy_.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_]:
                try:
                    bstack1l11l11ll1l_opy_ = callback(self, target, exec, bstack1lllllll11l_opy_, result, *args, **kwargs)
                    if bstack1l11l11ll11_opy_ == None:
                        bstack1l11l11ll11_opy_ = bstack1l11l11ll1l_opy_
                except Exception as e:
                    self.logger.error(bstack11l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᖢ") + str(e) + bstack11l1_opy_ (u"ࠤࠥᖣ"))
                    traceback.print_exc()
            if bstack1llll1lll1l_opy_ == bstack1llllllllll_opy_.QUIT:
                if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST:
                    bstack1ll111llll1_opy_ = bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, EVENTS.bstack1l1l11lll1_opy_.value)
                    if bstack1ll111llll1_opy_!=None:
                        bstack1ll1ll11111_opy_.end(EVENTS.bstack1l1l11lll1_opy_.value, bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᖤ"), bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᖥ"), True, None)
            if bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.PRE and callable(bstack1l11l11ll11_opy_):
                return bstack1l11l11ll11_opy_
            elif bstack1l11l11llll_opy_ == bstack1llll1lll11_opy_.POST and bstack1l11l11ll11_opy_:
                return bstack1l11l11ll11_opy_
    def bstack111111111l_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        if method_name == bstack11l1_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᖦ") or method_name == bstack11l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᖧ"):
            return bstack1llllllllll_opy_.bstack1llllll11ll_opy_
        if method_name == bstack11l1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᖨ"):
            return bstack1llllllllll_opy_.QUIT
        if method_name == bstack11l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᖩ"):
            if previous_state != bstack1llllllllll_opy_.NONE:
                command_name = bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args)
                if command_name == bstack1llll1l11l1_opy_.bstack1l11ll1llll_opy_:
                    return bstack1llllllllll_opy_.bstack1llllll11ll_opy_
            return bstack1llllllllll_opy_.bstack1llllll111l_opy_
        return bstack1llllllllll_opy_.NONE