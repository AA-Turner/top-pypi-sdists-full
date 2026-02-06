# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1llll1l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1lll1l1111l_opy_(bstack1lll1l1l1l1_opy_):
    bstack1llll111111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lll1l1l11l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lll1l1l11l_opy_]]
    def __init__(self, bstack1llll111111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1lll1lll1ll_opy_ = dict()
        self.bstack1llll111111_opy_ = bstack1llll111111_opy_
        self.frameworks = frameworks
        bstack1lll1lll11l_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_, bstack1lll1ll11ll_opy_.POST), self.__1lll1ll1l1l_opy_)
        if any(bstack1lll11lllll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_(
                (bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.__1lll1lllll1_opy_
            )
            bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_(
                (bstack1lll1l1ll1l_opy_.QUIT, bstack1lll1ll11ll_opy_.POST), self.__1lll1lll111_opy_
            )
    def __1lll1ll1l1l_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        bstack1lll11lll1l_opy_: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11lllll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᄻ"):
                return
            contexts = bstack1lll11lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11lllll_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᄼ") in page.url:
                                self.logger.debug(bstack11lllll_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᄽ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, self.bstack1llll111111_opy_, True)
                                self.logger.debug(bstack11lllll_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡳࡥ࡬࡫࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᄾ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠧࠨᄿ"))
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࠼ࠥᅀ"),e)
    def __1lll1lllll1_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, self.bstack1llll111111_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1lll1l111ll_opy_ = None
        if label:
            if bstack11lllll_opy_ (u"ࠢࠤࠤᅁ") in label:
                suffix = label.rsplit(bstack11lllll_opy_ (u"ࠣࠥࠥᅂ"), 1)[-1]
                if suffix.isdigit():
                    bstack1lll1l111ll_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1llll11111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࡶࡹ࡫࡬ࡩࡹࠢࠪࡿࡸࡻࡦࡧ࡫ࡻࢁࠬࠦࡩ࡯ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠ࡯ࡷࡰࡩࡷ࡯ࡣࠡࡴࡤࡲࡰ࠴ࠢᅃ")
                    )
            else:
                self.logger.debug(
                    bstack1llll11111l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࠡࠩࠦࠫࡀࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡴࡤࡲࡰࠦࡡࡴࡵ࡬࡫ࡳࡳࡥ࡯ࡶ࠱ࠦᅄ")
                )
        if bstack1lll1l111ll_opy_ is not None:
            bstack1lll1l111ll_opy_ = label.split(bstack11lllll_opy_ (u"ࠦࠨࠨᅅ"))[-1]
            instance.data[bstack11lllll_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᅆ")] = bstack1lll1l111ll_opy_
        self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࡃࠢᅇ") + str(instance.data) + bstack11lllll_opy_ (u"ࠢࠣᅈ"))
        if not f.bstack1lll1ll11l1_opy_(f.hub_url(driver)):
            self.bstack1lll1lll1ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, self.bstack1llll111111_opy_, True)
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᅉ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠤࠥᅊ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, self.bstack1llll111111_opy_, True)
        self.logger.debug(bstack11lllll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᅋ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠦࠧᅌ"))
    def __1lll1lll111_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1lll1l11l11_opy_(instance)
        self.logger.debug(bstack11lllll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᅍ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠨࠢᅎ"))
    def bstack1lll1llll11_opy_(self, context: bstack1lll1llll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1l1l11l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1lll1ll1111_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll11lllll_opy_.bstack1lll1l1llll_opy_(data[1])
                    and data[1].bstack1lll1ll1111_opy_(context)
                    and getattr(data[0](), bstack11lllll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᅏ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll11llll1_opy_, reverse=reverse)
    def bstack1lll1ll1l11_opy_(self, context: bstack1lll1llll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1l1l11l_opy_]]:
        matches = []
        for data in self.bstack1lll1lll1ll_opy_.values():
            if (
                data[1].bstack1lll1ll1111_opy_(context)
                and getattr(data[0](), bstack11lllll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᅐ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll11llll1_opy_, reverse=reverse)
    def bstack1lll1l11111_opy_(self, instance: bstack1lll1l1l11l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1lll1l11l11_opy_(self, instance: bstack1lll1l1l11l_opy_) -> bool:
        if self.bstack1lll1l11111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, self.bstack1llll111111_opy_, False)
            return True
        return False