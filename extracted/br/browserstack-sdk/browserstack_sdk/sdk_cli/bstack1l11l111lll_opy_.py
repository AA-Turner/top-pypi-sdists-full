# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1l1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111_opy_ import (
    bstack1l1111llll_opy_,
    bstack1ll1l11l1_opy_,
    bstack1llllllll1_opy_,
    bstack1ll1l1111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l11l_opy_ import bstack1l1lll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll111_opy_ import bstack11ll11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l111ll_opy_ import bstack1ll11llllll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1l1lllll1_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l111lllll1_opy_(bstack1l1l1lllll1_opy_):
    bstack1l11l111l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1l1111l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1l1111l1_opy_]]
    def __init__(self, bstack1l11l111l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11l11111l_opy_ = dict()
        self.bstack1l11l111l11_opy_ = bstack1l11l111l11_opy_
        self.frameworks = frameworks
        bstack11ll11l1l_opy_.bstack1l1l11ll111_opy_((bstack1l1111llll_opy_.bstack1ll1l1111l_opy_, bstack1ll1l11l1_opy_.POST), self.__1l11l1111ll_opy_)
        if any(bstack1l1lll1l1ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l1lll1l1ll_opy_.bstack1l1l11ll111_opy_(
                (bstack1l1111llll_opy_.bstack1ll1ll1lll1_opy_, bstack1ll1l11l1_opy_.PRE), self.__1l111llllll_opy_
            )
            bstack1l1lll1l1ll_opy_.bstack1l1l11ll111_opy_(
                (bstack1l1111llll_opy_.QUIT, bstack1ll1l11l1_opy_.POST), self.__1l11l1111l1_opy_
            )
    def __1l11l1111ll_opy_(
        self,
        f: bstack11ll11l1l_opy_,
        bstack1l11l111l1l_opy_: object,
        exec: Tuple[bstack1ll1l1111l1_opy_, str],
        bstack1ll11ll1lll_opy_: Tuple[bstack1l1111llll_opy_, bstack1ll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᕒ"):
                return
            contexts = bstack1l11l111l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᕓ") in page.url:
                                self.logger.debug(bstack1l1_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᕔ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllllll1_opy_.bstack1ll1l11lll_opy_(instance, self.bstack1l11l111l11_opy_, True)
                                self.logger.debug(bstack1l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᕕ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠤࠥᕖ"))
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢᕗ"),e)
    def __1l111llllll_opy_(
        self,
        f: bstack1l1lll1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1111l1_opy_, str],
        bstack1ll11ll1lll_opy_: Tuple[bstack1l1111llll_opy_, bstack1ll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllllll1_opy_.bstack1ll1ll11l1l_opy_(instance, self.bstack1l11l111l11_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll11l1ll11_opy_ = None
        if label:
            if bstack1l1_opy_ (u"ࠦࠨࠨᕘ") in label:
                suffix = label.rsplit(bstack1l1_opy_ (u"ࠧࠩࠢᕙ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll11l1ll11_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll11l111l1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᕚ")
                    )
            else:
                self.logger.debug(
                    bstack1ll11l111l1_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᕛ")
                )
        if bstack1ll11l1ll11_opy_ is not None:
            bstack1ll11l1ll11_opy_ = label.split(bstack1l1_opy_ (u"ࠣࠥࠥᕜ"))[-1]
            instance.data[bstack1l1_opy_ (u"ࠤࡵࡥࡳࡱࠢᕝ")] = bstack1ll11l1ll11_opy_
        self.logger.debug(bstack1l1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࡀࠦᕞ") + str(instance.data) + bstack1l1_opy_ (u"ࠦࠧᕟ"))
        if not f.bstack1l11l11ll11_opy_(f.hub_url(driver)):
            self.bstack1l11l11111l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllllll1_opy_.bstack1ll1l11lll_opy_(instance, self.bstack1l11l111l11_opy_, True)
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᕠ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠨࠢᕡ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllllll1_opy_.bstack1ll1l11lll_opy_(instance, self.bstack1l11l111l11_opy_, True)
        self.logger.debug(bstack1l1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᕢ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠣࠤᕣ"))
    def __1l11l1111l1_opy_(
        self,
        f: bstack1l1lll1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1111l1_opy_, str],
        bstack1ll11ll1lll_opy_: Tuple[bstack1l1111llll_opy_, bstack1ll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11l11l11l_opy_(instance)
        self.logger.debug(bstack1l1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᕤ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠥࠦᕥ"))
    def bstack1l11l111ll1_opy_(self, context: bstack1ll11llllll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1111l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11l11l1ll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l1lll1l1ll_opy_.bstack1l11l11l1l1_opy_(data[1])
                    and data[1].bstack1l11l11l1ll_opy_(context)
                    and getattr(data[0](), bstack1l1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᕦ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11ll111l_opy_, reverse=reverse)
    def bstack1l11l11l111_opy_(self, context: bstack1ll11llllll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1111l1_opy_]]:
        matches = []
        for data in self.bstack1l11l11111l_opy_.values():
            if (
                data[1].bstack1l11l11l1ll_opy_(context)
                and getattr(data[0](), bstack1l1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᕧ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11ll111l_opy_, reverse=reverse)
    def bstack1l11l111111_opy_(self, instance: bstack1ll1l1111l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11l11l11l_opy_(self, instance: bstack1ll1l1111l1_opy_) -> bool:
        if self.bstack1l11l111111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllllll1_opy_.bstack1ll1l11lll_opy_(instance, self.bstack1l11l111l11_opy_, False)
            return True
        return False