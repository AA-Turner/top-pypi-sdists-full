# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1llll111_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from bstack_utils.constants import EVENTS
class bstack1ll111ll1ll_opy_(bstack1ll1llll111_opy_):
    bstack11ll11llll1_opy_ = bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᤱ")
    NAME = bstack1111l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᤲ")
    bstack1lll1111ll1_opy_ = bstack1111l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᤳ")
    bstack1ll1llll1l1_opy_ = bstack1111l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᤴ")
    bstack11l11ll1l1l_opy_ = bstack1111l_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᤵ")
    bstack1ll1lll1lll_opy_ = bstack1111l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᤶ")
    bstack11ll1ll1111_opy_ = bstack1111l_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᤷ")
    bstack11l11ll11l1_opy_ = bstack1111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᤸ")
    bstack11l11ll1l11_opy_ = bstack1111l_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸ᤹ࠧ")
    bstack1l1l1l111ll_opy_ = bstack1111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧ᤺")
    bstack11lll1l11l1_opy_ = bstack1111l_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤ᤻")
    bstack11l11l1lll1_opy_ = bstack1111l_opy_ (u"ࠨࡧࡦࡶࠥ᤼")
    bstack1l111l1llll_opy_ = bstack1111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᤽")
    bstack11ll1l11l11_opy_ = bstack1111l_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦ᤾")
    bstack11ll1l111l1_opy_ = bstack1111l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥ᤿")
    bstack11l11ll111l_opy_ = bstack1111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣ᥀")
    bstack11l11lll111_opy_: Dict[str, List[Callable]] = dict()
    bstack11lll1l111l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l1ll111l11_opy_: Any
    bstack11ll11lll11_opy_: Dict
    def __init__(
        self,
        bstack11lll1l111l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l1ll111l11_opy_: Dict[str, Any],
        methods=[bstack1111l_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨ᥁"), bstack1111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᥂"), bstack1111l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢ᥃"), bstack1111l_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ᥄")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11lll1l111l_opy_ = bstack11lll1l111l_opy_
        self.platform_index = platform_index
        self.bstack1ll1ll11111_opy_(methods)
        self.bstack1l1ll111l11_opy_ = bstack1l1ll111l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1llll111_opy_.get_data(bstack1ll111ll1ll_opy_.bstack1ll1llll1l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1llll111_opy_.get_data(bstack1ll111ll1ll_opy_.bstack1lll1111ll1_opy_, target, strict)
    @staticmethod
    def bstack11l11ll11ll_opy_(target: object, strict=True):
        return bstack1ll1llll111_opy_.get_data(bstack1ll111ll1ll_opy_.bstack11l11ll1l1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1llll111_opy_.get_data(bstack1ll111ll1ll_opy_.bstack1ll1lll1lll_opy_, target, strict)
    @staticmethod
    def bstack1l11l1l1lll_opy_(instance: bstack1ll1l1lll1l_opy_) -> bool:
        return bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack11ll1ll1111_opy_, False)
    @staticmethod
    def bstack1l1l11lll11_opy_(instance: bstack1ll1l1lll1l_opy_, default_value=None):
        return bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1lll1111ll1_opy_, default_value)
    @staticmethod
    def bstack1l1l1ll1111_opy_(instance: bstack1ll1l1lll1l_opy_, default_value=None):
        return bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1ll1lll1lll_opy_, default_value)
    @staticmethod
    def bstack1l11ll1l1l1_opy_(hub_url: str, bstack11l11lll11l_opy_=bstack1111l_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ᥅")):
        try:
            bstack11l11l1llll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l11l1llll_opy_.endswith(bstack11l11lll11l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l1111111_opy_(method_name: str):
        return method_name == bstack1111l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥ᥆")
    @staticmethod
    def bstack1l1l11l11ll_opy_(method_name: str, *args):
        return (
            bstack1ll111ll1ll_opy_.bstack1l1l1111111_opy_(method_name)
            and bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args) == bstack1ll111ll1ll_opy_.bstack11lll1l11l1_opy_
        )
    @staticmethod
    def bstack1l11lll1l1l_opy_(method_name: str, *args):
        if not bstack1ll111ll1ll_opy_.bstack1l1l1111111_opy_(method_name):
            return False
        if not bstack1ll111ll1ll_opy_.bstack11ll1l11l11_opy_ in bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args):
            return False
        bstack1l11ll11l1l_opy_ = bstack1ll111ll1ll_opy_.bstack1l11ll11lll_opy_(*args)
        return bstack1l11ll11l1l_opy_ and bstack1111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ᥇") in bstack1l11ll11l1l_opy_ and bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᥈") in bstack1l11ll11l1l_opy_[bstack1111l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᥉")]
    @staticmethod
    def bstack1l1l1l11l1l_opy_(method_name: str, *args):
        if not bstack1ll111ll1ll_opy_.bstack1l1l1111111_opy_(method_name):
            return False
        if not bstack1ll111ll1ll_opy_.bstack11ll1l11l11_opy_ in bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args):
            return False
        bstack1l11ll11l1l_opy_ = bstack1ll111ll1ll_opy_.bstack1l11ll11lll_opy_(*args)
        return (
            bstack1l11ll11l1l_opy_
            and bstack1111l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ᥊") in bstack1l11ll11l1l_opy_
            and bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥ᥋") in bstack1l11ll11l1l_opy_[bstack1111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ᥌")]
        )
    @staticmethod
    def bstack11lll1l1lll_opy_(*args):
        return str(bstack1ll111ll1ll_opy_.bstack1l11llll1ll_opy_(*args)).lower()
    @staticmethod
    def bstack1l11llll1ll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l11ll11lll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1ll11l111l_opy_(driver):
        command_executor = getattr(driver, bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᥍"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1111l_opy_ (u"ࠥࡣࡺࡸ࡬ࠣ᥎"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1111l_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧ᥏"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1111l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᥐ"), None)
        return hub_url
    def bstack11lll111ll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᥑ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᥒ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1111l_opy_ (u"ࠣࡡࡸࡶࡱࠨᥓ")):
                setattr(command_executor, bstack1111l_opy_ (u"ࠤࡢࡹࡷࡲࠢᥔ"), hub_url)
                result = True
        if result:
            self.bstack11lll1l111l_opy_ = hub_url
            bstack1ll111ll1ll_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1lll1111ll1_opy_, hub_url)
            bstack1ll111ll1ll_opy_.bstack1ll1lllll11_opy_(
                instance, bstack1ll111ll1ll_opy_.bstack11ll1ll1111_opy_, bstack1ll111ll1ll_opy_.bstack1l11ll1l1l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_]):
        return bstack1111l_opy_ (u"ࠥ࠾ࠧᥕ").join((bstack1ll1l1l1lll_opy_(bstack1ll1l111l11_opy_[0]).name, bstack1ll1ll1111l_opy_(bstack1ll1l111l11_opy_[1]).name))
    @staticmethod
    def bstack1l1l11llll1_opy_(bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_], callback: Callable):
        bstack11ll11lllll_opy_ = bstack1ll111ll1ll_opy_.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        if not bstack11ll11lllll_opy_ in bstack1ll111ll1ll_opy_.bstack11l11lll111_opy_:
            bstack1ll111ll1ll_opy_.bstack11l11lll111_opy_[bstack11ll11lllll_opy_] = []
        bstack1ll111ll1ll_opy_.bstack11l11lll111_opy_[bstack11ll11lllll_opy_].append(callback)
    def bstack1ll11llll11_opy_(self, instance: bstack1ll1l1lll1l_opy_, method_name: str, bstack1ll1l11111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1111l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᥖ")):
            return
        cmd = args[0] if method_name == bstack1111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᥗ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l11ll1lll_opy_ = bstack1111l_opy_ (u"ࠨ࠺ࠣᥘ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᥙ") + bstack11l11ll1lll_opy_, bstack1ll1l11111l_opy_)
    def bstack1ll1l111111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll1ll111l1_opy_, bstack11ll1l1111l_opy_ = bstack1ll1l111l11_opy_
        bstack11ll11lllll_opy_ = bstack1ll111ll1ll_opy_.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᥚ") + str(kwargs) + bstack1111l_opy_ (u"ࠤࠥᥛ"))
        if bstack1ll1ll111l1_opy_ == bstack1ll1l1l1lll_opy_.QUIT:
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.PRE:
                bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l11ll1111_opy_.value)
                bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, EVENTS.bstack11l11ll1111_opy_.value, bstack1l1llll1_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᥜ").format(instance, method_name, bstack1ll1ll111l1_opy_, bstack11ll1l1111l_opy_))
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST:
                bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l11ll1ll1_opy_.value)
                bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, EVENTS.bstack11l11ll1ll1_opy_.value, bstack1l1llll1_opy_)
        if bstack1ll1ll111l1_opy_ == bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_:
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST and not bstack1ll111ll1ll_opy_.bstack1ll1llll1l1_opy_ in instance.data:
                session_id = getattr(target, bstack1111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᥝ"), None)
                if session_id:
                    instance.data[bstack1ll111ll1ll_opy_.bstack1ll1llll1l1_opy_] = session_id
        elif (
            bstack1ll1ll111l1_opy_ == bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_
            and bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args) == bstack1ll111ll1ll_opy_.bstack11lll1l11l1_opy_
        ):
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.PRE:
                hub_url = bstack1ll111ll1ll_opy_.bstack1ll11l111l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll111ll1ll_opy_.bstack1lll1111ll1_opy_: hub_url,
                            bstack1ll111ll1ll_opy_.bstack11ll1ll1111_opy_: bstack1ll111ll1ll_opy_.bstack1l11ll1l1l1_opy_(hub_url),
                            bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_: int(
                                os.environ.get(bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᥞ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l11ll11l1l_opy_ = bstack1ll111ll1ll_opy_.bstack1l11ll11lll_opy_(*args)
                bstack11l11ll11ll_opy_ = bstack1l11ll11l1l_opy_.get(bstack1111l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᥟ"), None) if bstack1l11ll11l1l_opy_ else None
                if isinstance(bstack11l11ll11ll_opy_, dict):
                    instance.data[bstack1ll111ll1ll_opy_.bstack11l11ll1l1l_opy_] = copy.deepcopy(bstack11l11ll11ll_opy_)
                    instance.data[bstack1ll111ll1ll_opy_.bstack1ll1lll1lll_opy_] = bstack11l11ll11ll_opy_
            elif bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1111l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᥠ"), dict()).get(bstack1111l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᥡ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll111ll1ll_opy_.bstack1ll1llll1l1_opy_: framework_session_id,
                                bstack1ll111ll1ll_opy_.bstack11l11ll11l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll1ll111l1_opy_ == bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_
            and bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args) == bstack1ll111ll1ll_opy_.bstack11l11ll111l_opy_
            and bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST
        ):
            instance.data[bstack1ll111ll1ll_opy_.bstack11l11ll1l11_opy_] = datetime.now(tz=timezone.utc)
        if bstack11ll11lllll_opy_ in bstack1ll111ll1ll_opy_.bstack11l11lll111_opy_:
            bstack11ll11lll1l_opy_ = None
            for callback in bstack1ll111ll1ll_opy_.bstack11l11lll111_opy_[bstack11ll11lllll_opy_]:
                try:
                    bstack11ll1l11111_opy_ = callback(self, target, exec, bstack1ll1l111l11_opy_, result, *args, **kwargs)
                    if bstack11ll11lll1l_opy_ == None:
                        bstack11ll11lll1l_opy_ = bstack11ll1l11111_opy_
                except Exception as e:
                    self.logger.error(bstack1111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᥢ") + str(e) + bstack1111l_opy_ (u"ࠥࠦᥣ"))
                    traceback.print_exc()
            if bstack1ll1ll111l1_opy_ == bstack1ll1l1l1lll_opy_.QUIT:
                if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.PRE:
                    bstack1l1llll1_opy_ = bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, EVENTS.bstack11l11ll1111_opy_.value)
                    if bstack1l1llll1_opy_!=None:
                        bstack1l11ll1l1_opy_.end(EVENTS.bstack11l11ll1111_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᥤ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᥥ"), True, None)
                if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST:
                    bstack1l1llll1_opy_ = bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, EVENTS.bstack11l11ll1ll1_opy_.value)
                    if bstack1l1llll1_opy_!=None:
                        bstack1l11ll1l1_opy_.end(EVENTS.bstack11l11ll1ll1_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᥦ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᥧ"), True, None)
            if bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.PRE and callable(bstack11ll11lll1l_opy_):
                return bstack11ll11lll1l_opy_
            elif bstack11ll1l1111l_opy_ == bstack1ll1ll1111l_opy_.POST and bstack11ll11lll1l_opy_:
                return bstack11ll11lll1l_opy_
    def bstack1ll1l11l1l1_opy_(
        self, method_name, previous_state: bstack1ll1l1l1lll_opy_, *args, **kwargs
    ) -> bstack1ll1l1l1lll_opy_:
        if method_name == bstack1111l_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᥨ") or method_name == bstack1111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᥩ"):
            return bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_
        if method_name == bstack1111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᥪ"):
            return bstack1ll1l1l1lll_opy_.QUIT
        if method_name == bstack1111l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᥫ"):
            if previous_state != bstack1ll1l1l1lll_opy_.NONE:
                command_name = bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args)
                if command_name == bstack1ll111ll1ll_opy_.bstack11lll1l11l1_opy_:
                    return bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_
            return bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_
        return bstack1ll1l1l1lll_opy_.NONE