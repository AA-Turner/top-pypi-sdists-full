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
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1ll1lll1_opy_,
    bstack1ll1lll1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1ll11l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1ll1lll11l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l1l1111111_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l1l11111l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1lll1111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1lll1111_opy_]]
    def __init__(self, bstack1l1l11111l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1l1111ll1_opy_ = dict()
        self.bstack1l1l11111l1_opy_ = bstack1l1l11111l1_opy_
        self.frameworks = frameworks
        bstack1ll11l1111l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_, bstack1lll111l1l1_opy_.POST), self.__1l1l1111l11_opy_)
        if any(bstack1ll1111ll11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_(
                (bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.__1l11lllllll_opy_
            )
            bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_(
                (bstack1ll1ll1l1l1_opy_.QUIT, bstack1lll111l1l1_opy_.POST), self.__1l1l111l1l1_opy_
            )
    def __1l1l1111l11_opy_(
        self,
        f: bstack1ll11l1111l_opy_,
        bstack1l11llllll1_opy_: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11ll111_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᏯ"):
                return
            contexts = bstack1l11llllll1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11ll111_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨᏰ") in page.url:
                                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᏱ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, self.bstack1l1l11111l1_opy_, True)
                                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᏲ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠦࠧᏳ"))
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤᏴ"),e)
    def __1l11lllllll_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, self.bstack1l1l11111l1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll1llll111_opy_ = None
        if label:
            if bstack11ll111_opy_ (u"ࠨࠣࠣᏵ") in label:
                suffix = label.rsplit(bstack11ll111_opy_ (u"ࠢࠤࠤ᏶"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll1llll111_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1lll11111l1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࡵࡸࡪ࡫࡯ࡸࠡࠩࡾࡷࡺ࡬ࡦࡪࡺࢀࠫࠥ࡯࡮ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦ࡮ࡶ࡯ࡨࡶ࡮ࡩࠠࡳࡣࡱ࡯࠳ࠨ᏷")
                    )
            else:
                self.logger.debug(
                    bstack1lll11111l1_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࠠࠨࠥࠪ࠿ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡳࡣࡱ࡯ࠥࡧࡳࡴ࡫ࡪࡲࡲ࡫࡮ࡵ࠰ࠥᏸ")
                )
        if bstack1ll1llll111_opy_ is not None:
            bstack1ll1llll111_opy_ = label.split(bstack11ll111_opy_ (u"ࠥࠧࠧᏹ"))[-1]
            instance.data[bstack11ll111_opy_ (u"ࠦࡷࡧ࡮࡬ࠤᏺ")] = bstack1ll1llll111_opy_
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡺ࡭ࡹ࡮ࠠࡥࡣࡷࡥࡂࠨᏻ") + str(instance.data) + bstack11ll111_opy_ (u"ࠨࠢᏼ"))
        if not f.bstack1l1l11l111l_opy_(f.hub_url(driver)):
            self.bstack1l1l1111ll1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, self.bstack1l1l11111l1_opy_, True)
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᏽ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠣࠤ᏾"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, self.bstack1l1l11111l1_opy_, True)
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦ᏿") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠥࠦ᐀"))
    def __1l1l111l1l1_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1l1111lll_opy_(instance)
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᐁ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠧࠨᐂ"))
    def bstack1l1l111l11l_opy_(self, context: bstack1ll1lll11l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1lll1111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1l11111ll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1111ll11_opy_.bstack1l1l1111l1l_opy_(data[1])
                    and data[1].bstack1l1l11111ll_opy_(context)
                    and getattr(data[0](), bstack11ll111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᐃ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1l1l_opy_, reverse=reverse)
    def bstack1l1l111l111_opy_(self, context: bstack1ll1lll11l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1lll1111_opy_]]:
        matches = []
        for data in self.bstack1l1l1111ll1_opy_.values():
            if (
                data[1].bstack1l1l11111ll_opy_(context)
                and getattr(data[0](), bstack11ll111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᐄ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1l1l_opy_, reverse=reverse)
    def bstack1l1l111111l_opy_(self, instance: bstack1ll1lll1111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1l1111lll_opy_(self, instance: bstack1ll1lll1111_opy_) -> bool:
        if self.bstack1l1l111111l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, self.bstack1l1l11111l1_opy_, False)
            return True
        return False