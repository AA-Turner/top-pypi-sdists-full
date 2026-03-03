# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1lll1_opy_,
    bstack1ll1lll1111_opy_,
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from bstack_utils.constants import EVENTS
class bstack1ll1111ll11_opy_(bstack1ll1ll1lll1_opy_):
    bstack11lll11l1l1_opy_ = bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ᝛")
    NAME = bstack11ll111_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᝜")
    bstack1l111l11ll1_opy_ = bstack11ll111_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦ᝝")
    bstack1l111l111l1_opy_ = bstack11ll111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ᝞")
    bstack11l1ll1l11l_opy_ = bstack11ll111_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᝟")
    bstack1l111l11111_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᝠ")
    bstack11lll1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨᝡ")
    bstack11l1ll1l1l1_opy_ = bstack11ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᝢ")
    bstack11l1ll1l111_opy_ = bstack11ll111_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᝣ")
    bstack1l1ll1lll11_opy_ = bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᝤ")
    bstack11lllll111l_opy_ = bstack11ll111_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣᝥ")
    bstack11l1ll1l1ll_opy_ = bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࠤᝦ")
    bstack1l11ll1l111_opy_ = bstack11ll111_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᝧ")
    bstack11lll11ll11_opy_ = bstack11ll111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᝨ")
    bstack11lll11ll1l_opy_ = bstack11ll111_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᝩ")
    bstack11l1ll1lll1_opy_ = bstack11ll111_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᝪ")
    bstack11l1ll111ll_opy_: Dict[str, List[Callable]] = dict()
    bstack11llll11ll1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1l1l1111_opy_: Any
    bstack11lll11lll1_opy_: Dict
    def __init__(
        self,
        bstack11llll11ll1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1l1l1111_opy_: Dict[str, Any],
        methods=[bstack11ll111_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᝫ"), bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᝬ"), bstack11ll111_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨ᝭"), bstack11ll111_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᝮ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack11llll11ll1_opy_ = bstack11llll11ll1_opy_
        self.platform_index = platform_index
        self.bstack1lll111ll1l_opy_(methods)
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1ll1ll1lll1_opy_.get_data(bstack1ll1111ll11_opy_.bstack1l111l111l1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1ll1ll1lll1_opy_.get_data(bstack1ll1111ll11_opy_.bstack1l111l11ll1_opy_, target, strict)
    @staticmethod
    def bstack11l1ll1ll11_opy_(target: object, strict=True):
        return bstack1ll1ll1lll1_opy_.get_data(bstack1ll1111ll11_opy_.bstack11l1ll1l11l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1ll1ll1lll1_opy_.get_data(bstack1ll1111ll11_opy_.bstack1l111l11111_opy_, target, strict)
    @staticmethod
    def bstack1l1l1111l1l_opy_(instance: bstack1ll1lll1111_opy_) -> bool:
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack11lll1l1l1l_opy_, False)
    @staticmethod
    def bstack1l1ll1l1111_opy_(instance: bstack1ll1lll1111_opy_, default_value=None):
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l111l11ll1_opy_, default_value)
    @staticmethod
    def bstack1l1ll1l11ll_opy_(instance: bstack1ll1lll1111_opy_, default_value=None):
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l111l11111_opy_, default_value)
    @staticmethod
    def bstack1l1l11l111l_opy_(hub_url: str, bstack11l1ll11l11_opy_=bstack11ll111_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᝯ")):
        try:
            bstack11l1ll11l1l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11l1ll11l1l_opy_.endswith(bstack11l1ll11l11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1l1l1l11111_opy_(method_name: str):
        return method_name == bstack11ll111_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᝰ")
    @staticmethod
    def bstack1l1l11lll1l_opy_(method_name: str, *args):
        return (
            bstack1ll1111ll11_opy_.bstack1l1l1l11111_opy_(method_name)
            and bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args) == bstack1ll1111ll11_opy_.bstack11lllll111l_opy_
        )
    @staticmethod
    def bstack1l1ll111l1l_opy_(method_name: str, *args):
        if not bstack1ll1111ll11_opy_.bstack1l1l1l11111_opy_(method_name):
            return False
        if not bstack1ll1111ll11_opy_.bstack11lll11ll11_opy_ in bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111lll1_opy_ = bstack1ll1111ll11_opy_.bstack1l1l111llll_opy_(*args)
        return bstack1l1l111lll1_opy_ and bstack11ll111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ᝱") in bstack1l1l111lll1_opy_ and bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᝲ") in bstack1l1l111lll1_opy_[bstack11ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᝳ")]
    @staticmethod
    def bstack1l1l1llll11_opy_(method_name: str, *args):
        if not bstack1ll1111ll11_opy_.bstack1l1l1l11111_opy_(method_name):
            return False
        if not bstack1ll1111ll11_opy_.bstack11lll11ll11_opy_ in bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args):
            return False
        bstack1l1l111lll1_opy_ = bstack1ll1111ll11_opy_.bstack1l1l111llll_opy_(*args)
        return (
            bstack1l1l111lll1_opy_
            and bstack11ll111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ᝴") in bstack1l1l111lll1_opy_
            and bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤ᝵") in bstack1l1l111lll1_opy_[bstack11ll111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ᝶")]
        )
    @staticmethod
    def bstack11llll1l111_opy_(*args):
        return str(bstack1ll1111ll11_opy_.bstack1l1l11ll111_opy_(*args)).lower()
    @staticmethod
    def bstack1l1l11ll111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1l111llll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l111lll11_opy_(driver):
        command_executor = getattr(driver, bstack11ll111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᝷"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11ll111_opy_ (u"ࠤࡢࡹࡷࡲࠢ᝸"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11ll111_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦ᝹"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11ll111_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤ᝺"), None)
        return hub_url
    def bstack11lllll1l1l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᝻"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᝼"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11ll111_opy_ (u"ࠢࡠࡷࡵࡰࠧ᝽")):
                setattr(command_executor, bstack11ll111_opy_ (u"ࠣࡡࡸࡶࡱࠨ᝾"), hub_url)
                result = True
        if result:
            self.bstack11llll11ll1_opy_ = hub_url
            bstack1ll1111ll11_opy_.bstack1lll11l1111_opy_(instance, bstack1ll1111ll11_opy_.bstack1l111l11ll1_opy_, hub_url)
            bstack1ll1111ll11_opy_.bstack1lll11l1111_opy_(
                instance, bstack1ll1111ll11_opy_.bstack11lll1l1l1l_opy_, bstack1ll1111ll11_opy_.bstack1l1l11l111l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_]):
        return bstack11ll111_opy_ (u"ࠤ࠽ࠦ᝿").join((bstack1ll1ll1l1l1_opy_(bstack1ll1ll1llll_opy_[0]).name, bstack1lll111l1l1_opy_(bstack1ll1ll1llll_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll11l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_], callback: Callable):
        bstack11lll11l1ll_opy_ = bstack1ll1111ll11_opy_.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        if not bstack11lll11l1ll_opy_ in bstack1ll1111ll11_opy_.bstack11l1ll111ll_opy_:
            bstack1ll1111ll11_opy_.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_] = []
        bstack1ll1111ll11_opy_.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_].append(callback)
    def bstack1lll11l1l11_opy_(self, instance: bstack1ll1lll1111_opy_, method_name: str, bstack1lll11l111l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11ll111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥក")):
            return
        cmd = args[0] if method_name == bstack11ll111_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧខ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11l1ll1ll1l_opy_ = bstack11ll111_opy_ (u"ࠧࡀࠢគ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢឃ") + bstack11l1ll1ll1l_opy_, bstack1lll11l111l_opy_)
    def bstack1ll1lll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lll111111l_opy_, bstack11lll11l111_opy_ = bstack1ll1ll1llll_opy_
        bstack11lll11l1ll_opy_ = bstack1ll1111ll11_opy_.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢង") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤច"))
        if bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.QUIT:
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.PRE:
                bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11l1ll11ll1_opy_.value)
                bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, EVENTS.bstack11l1ll11ll1_opy_.value, bstack11llllllll_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨឆ").format(instance, method_name, bstack1lll111111l_opy_, bstack11lll11l111_opy_))
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST:
                bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11l1ll11lll_opy_.value)
                bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, EVENTS.bstack11l1ll11lll_opy_.value, bstack11llllllll_opy_)
        if bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_:
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST and not bstack1ll1111ll11_opy_.bstack1l111l111l1_opy_ in instance.data:
                session_id = getattr(target, bstack11ll111_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢជ"), None)
                if session_id:
                    instance.data[bstack1ll1111ll11_opy_.bstack1l111l111l1_opy_] = session_id
        elif (
            bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_
            and bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args) == bstack1ll1111ll11_opy_.bstack11lllll111l_opy_
        ):
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.PRE:
                hub_url = bstack1ll1111ll11_opy_.bstack1l111lll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1ll1111ll11_opy_.bstack1l111l11ll1_opy_: hub_url,
                            bstack1ll1111ll11_opy_.bstack11lll1l1l1l_opy_: bstack1ll1111ll11_opy_.bstack1l1l11l111l_opy_(hub_url),
                            bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_: int(
                                os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦឈ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1l111lll1_opy_ = bstack1ll1111ll11_opy_.bstack1l1l111llll_opy_(*args)
                bstack11l1ll1ll11_opy_ = bstack1l1l111lll1_opy_.get(bstack11ll111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦញ"), None) if bstack1l1l111lll1_opy_ else None
                if isinstance(bstack11l1ll1ll11_opy_, dict):
                    instance.data[bstack1ll1111ll11_opy_.bstack11l1ll1l11l_opy_] = copy.deepcopy(bstack11l1ll1ll11_opy_)
                    instance.data[bstack1ll1111ll11_opy_.bstack1l111l11111_opy_] = bstack11l1ll1ll11_opy_
            elif bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11ll111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧដ"), dict()).get(bstack11ll111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥឋ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1ll1111ll11_opy_.bstack1l111l111l1_opy_: framework_session_id,
                                bstack1ll1111ll11_opy_.bstack11l1ll1l1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_
            and bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args) == bstack1ll1111ll11_opy_.bstack11l1ll1lll1_opy_
            and bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST
        ):
            instance.data[bstack1ll1111ll11_opy_.bstack11l1ll1l111_opy_] = datetime.now(tz=timezone.utc)
        if bstack11lll11l1ll_opy_ in bstack1ll1111ll11_opy_.bstack11l1ll111ll_opy_:
            bstack11lll11llll_opy_ = None
            for callback in bstack1ll1111ll11_opy_.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_]:
                try:
                    bstack11lll11l11l_opy_ = callback(self, target, exec, bstack1ll1ll1llll_opy_, result, *args, **kwargs)
                    if bstack11lll11llll_opy_ == None:
                        bstack11lll11llll_opy_ = bstack11lll11l11l_opy_
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨឌ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥឍ"))
                    traceback.print_exc()
            if bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.QUIT:
                if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.PRE:
                    bstack11llllllll_opy_ = bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, EVENTS.bstack11l1ll11ll1_opy_.value)
                    if bstack11llllllll_opy_!=None:
                        bstack1111l1l1l_opy_.end(EVENTS.bstack11l1ll11ll1_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥណ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤត"), True, None)
                if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST:
                    bstack11llllllll_opy_ = bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, EVENTS.bstack11l1ll11lll_opy_.value)
                    if bstack11llllllll_opy_!=None:
                        bstack1111l1l1l_opy_.end(EVENTS.bstack11l1ll11lll_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧថ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦទ"), True, None)
            if bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.PRE and callable(bstack11lll11llll_opy_):
                return bstack11lll11llll_opy_
            elif bstack11lll11l111_opy_ == bstack1lll111l1l1_opy_.POST and bstack11lll11llll_opy_:
                return bstack11lll11llll_opy_
    def bstack1lll1111lll_opy_(
        self, method_name, previous_state: bstack1ll1ll1l1l1_opy_, *args, **kwargs
    ) -> bstack1ll1ll1l1l1_opy_:
        if method_name == bstack11ll111_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤធ") or method_name == bstack11ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣន"):
            return bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_
        if method_name == bstack11ll111_opy_ (u"ࠤࡴࡹ࡮ࡺࠢប"):
            return bstack1ll1ll1l1l1_opy_.QUIT
        if method_name == bstack11ll111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦផ"):
            if previous_state != bstack1ll1ll1l1l1_opy_.NONE:
                command_name = bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args)
                if command_name == bstack1ll1111ll11_opy_.bstack11lllll111l_opy_:
                    return bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_
            return bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_
        return bstack1ll1ll1l1l1_opy_.NONE