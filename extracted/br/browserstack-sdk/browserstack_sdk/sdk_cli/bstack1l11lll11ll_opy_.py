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
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1ll11l11_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1ll1llll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11lll1l1l_opy_(bstack1l1ll1lll11_opy_):
    bstack1l11lll11l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1l1ll1ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1l1ll1ll_opy_]]
    def __init__(self, bstack1l11lll11l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11lll1lll_opy_ = dict()
        self.bstack1l11lll11l1_opy_ = bstack1l11lll11l1_opy_
        self.frameworks = frameworks
        bstack1l1lllll11l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1lll1111111_opy_, bstack1ll1l1llll1_opy_.POST), self.__1l11llll1l1_opy_)
        if any(bstack1l1llllllll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_(
                (bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.__1l11lll1ll1_opy_
            )
            bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_(
                (bstack1ll1lllllll_opy_.QUIT, bstack1ll1l1llll1_opy_.POST), self.__1l11llll11l_opy_
            )
    def __1l11llll1l1_opy_(
        self,
        f: bstack1l1lllll11l_opy_,
        bstack1l11llll1ll_opy_: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l11_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᏨ"):
                return
            contexts = bstack1l11llll1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l11_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨᏩ") in page.url:
                                self.logger.debug(bstack11l11_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᏪ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, self.bstack1l11lll11l1_opy_, True)
                                self.logger.debug(bstack11l11_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᏫ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠦࠧᏬ"))
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤᏭ"),e)
    def __1l11lll1ll1_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, self.bstack1l11lll11l1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll1llll1l1_opy_ = None
        if label:
            if bstack11l11_opy_ (u"ࠨࠣࠣᏮ") in label:
                suffix = label.rsplit(bstack11l11_opy_ (u"ࠢࠤࠤᏯ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll1llll1l1_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll1lllll11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࡵࡸࡪ࡫࡯ࡸࠡࠩࡾࡷࡺ࡬ࡦࡪࡺࢀࠫࠥ࡯࡮ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦ࡮ࡶ࡯ࡨࡶ࡮ࡩࠠࡳࡣࡱ࡯࠳ࠨᏰ")
                    )
            else:
                self.logger.debug(
                    bstack1ll1lllll11_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࠠࠨࠥࠪ࠿ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡳࡣࡱ࡯ࠥࡧࡳࡴ࡫ࡪࡲࡲ࡫࡮ࡵ࠰ࠥᏱ")
                )
        if bstack1ll1llll1l1_opy_ is not None:
            bstack1ll1llll1l1_opy_ = label.split(bstack11l11_opy_ (u"ࠥࠧࠧᏲ"))[-1]
            instance.data[bstack11l11_opy_ (u"ࠦࡷࡧ࡮࡬ࠤᏳ")] = bstack1ll1llll1l1_opy_
        self.logger.debug(bstack11l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࡂࠨᏴ") + str(instance.data) + bstack11l11_opy_ (u"ࠨࠢᏵ"))
        if not f.bstack1l1l1111lll_opy_(f.hub_url(driver)):
            self.bstack1l11lll1lll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, self.bstack1l11lll11l1_opy_, True)
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ᏶") + str(instance.ref()) + bstack11l11_opy_ (u"ࠣࠤ᏷"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, self.bstack1l11lll11l1_opy_, True)
        self.logger.debug(bstack11l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏸ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠥࠦᏹ"))
    def __1l11llll11l_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11llll111_opy_(instance)
        self.logger.debug(bstack11l11_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᏺ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠧࠨᏻ"))
    def bstack1l11lll1111_opy_(self, context: bstack1ll1ll1llll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1ll1ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11lll111l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l1llllllll_opy_.bstack1l11lllll11_opy_(data[1])
                    and data[1].bstack1l11lll111l_opy_(context)
                    and getattr(data[0](), bstack11l11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᏼ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1llll11l_opy_, reverse=reverse)
    def bstack1l11lll1l11_opy_(self, context: bstack1ll1ll1llll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1ll1ll_opy_]]:
        matches = []
        for data in self.bstack1l11lll1lll_opy_.values():
            if (
                data[1].bstack1l11lll111l_opy_(context)
                and getattr(data[0](), bstack11l11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᏽ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1llll11l_opy_, reverse=reverse)
    def bstack1l11lllll1l_opy_(self, instance: bstack1ll1l1ll1ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11llll111_opy_(self, instance: bstack1ll1l1ll1ll_opy_) -> bool:
        if self.bstack1l11lllll1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, self.bstack1l11lll11l1_opy_, False)
            return True
        return False