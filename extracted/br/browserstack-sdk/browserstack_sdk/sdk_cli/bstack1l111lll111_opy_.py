# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack111l1ll111_opy_,
    bstack1ll111lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11ll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11l11111l_opy_(bstack1ll111l11ll_opy_):
    bstack1l111lll11l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll111lllll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll111lllll_opy_]]
    def __init__(self, bstack1l111lll11l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l111ll1lll_opy_ = dict()
        self.bstack1l111lll11l_opy_ = bstack1l111lll11l_opy_
        self.frameworks = frameworks
        bstack1l111lllll_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.POST), self.__1l111lllll1_opy_)
        if any(bstack1ll11111111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll11111111_opy_.bstack1l11lll1lll_opy_(
                (bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.__1l111ll1ll1_opy_
            )
            bstack1ll11111111_opy_.bstack1l11lll1lll_opy_(
                (bstack1ll1l1ll11_opy_.QUIT, bstack1ll11ll1ll_opy_.POST), self.__1l111ll1l11_opy_
            )
    def __1l111lllll1_opy_(
        self,
        f: bstack1l111lllll_opy_,
        bstack1l111lll1l1_opy_: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᕻ"):
                return
            contexts = bstack1l111lll1l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll11_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᕼ") in page.url:
                                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᕽ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, self.bstack1l111lll11l_opy_, True)
                                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᕾ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠣࠤᕿ"))
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨᖀ"),e)
    def __1l111ll1ll1_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, self.bstack1l111lll11l_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll11ll1l1l_opy_ = None
        if label:
            if bstack1ll11_opy_ (u"ࠥࠧࠧᖁ") in label:
                suffix = label.rsplit(bstack1ll11_opy_ (u"ࠦࠨࠨᖂ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll11ll1l1l_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll11l1ll11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡤࡳ࡫ࡹࡩࡷࠦ࡬ࡢࡤࡨࡰࠥࡹࡵࡧࡨ࡬ࡼࠥ࠭ࡻࡴࡷࡩࡪ࡮ࡾࡽࠨࠢ࡬ࡲࠥࡲࡡࡣࡧ࡯ࠤࠬࢁ࡬ࡢࡤࡨࡰࢂ࠭࠻ࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡲࡺࡳࡥࡳ࡫ࡦࠤࡷࡧ࡮࡬࠰ࠥᖃ")
                    )
            else:
                self.logger.debug(
                    bstack1ll11l1ll11_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡧࡴࡴࡴࡢ࡫ࡱࠤࠬࠩࠧ࠼ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡷࡧ࡮࡬ࠢࡤࡷࡸ࡯ࡧ࡯࡯ࡨࡲࡹ࠴ࠢᖄ")
                )
        if bstack1ll11ll1l1l_opy_ is not None:
            bstack1ll11ll1l1l_opy_ = label.split(bstack1ll11_opy_ (u"ࠢࠤࠤᖅ"))[-1]
            instance.data[bstack1ll11_opy_ (u"ࠣࡴࡤࡲࡰࠨᖆ")] = bstack1ll11ll1l1l_opy_
        self.logger.debug(bstack1ll11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢ࠿ࠥᖇ") + str(instance.data) + bstack1ll11_opy_ (u"ࠥࠦᖈ"))
        if not f.bstack1l11l1111l1_opy_(f.hub_url(driver)):
            self.bstack1l111ll1lll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, self.bstack1l111lll11l_opy_, True)
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᖉ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠧࠨᖊ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, self.bstack1l111lll11l_opy_, True)
        self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᖋ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠢࠣᖌ"))
    def __1l111ll1l11_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l111lll1ll_opy_(instance)
        self.logger.debug(bstack1ll11_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡳࡸ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᖍ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠤࠥᖎ"))
    def bstack1l111llllll_opy_(self, context: bstack1ll11l11ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll111lllll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l111llll11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll11111111_opy_.bstack1l11l111111_opy_(data[1])
                    and data[1].bstack1l111llll11_opy_(context)
                    and getattr(data[0](), bstack1ll11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᖏ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11l1l1ll_opy_, reverse=reverse)
    def bstack1l111llll1l_opy_(self, context: bstack1ll11l11ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll111lllll_opy_]]:
        matches = []
        for data in self.bstack1l111ll1lll_opy_.values():
            if (
                data[1].bstack1l111llll11_opy_(context)
                and getattr(data[0](), bstack1ll11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᖐ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11l1l1ll_opy_, reverse=reverse)
    def bstack1l111ll1l1l_opy_(self, instance: bstack1ll111lllll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l111lll1ll_opy_(self, instance: bstack1ll111lllll_opy_) -> bool:
        if self.bstack1l111ll1l1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, self.bstack1l111lll11l_opy_, False)
            return True
        return False