# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1llllll1111_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll111111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1lllllll1ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
import weakref
class bstack1ll111111l1_opy_(bstack1lll1ll1l1l_opy_):
    bstack1l1lllll1ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    def __init__(self, bstack1l1lllll1ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llllllll_opy_ = dict()
        self.bstack1l1lllll1ll_opy_ = bstack1l1lllll1ll_opy_
        self.frameworks = frameworks
        bstack1lll111111l_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack11111111l1_opy_, bstack1llllll1ll1_opy_.POST), self.__1l1llll1lll_opy_)
        if any(bstack1ll1lllllll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_(
                (bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.__1l1lllllll1_opy_
            )
            bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_(
                (bstack1lllll1ll11_opy_.QUIT, bstack1llllll1ll1_opy_.POST), self.__1l1llllll11_opy_
            )
    def __1l1llll1lll_opy_(
        self,
        f: bstack1lll111111l_opy_,
        bstack1ll1111111l_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11ll1l1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢሊ"):
                return
            contexts = bstack1ll1111111l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11ll1l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦላ") in page.url:
                                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤሌ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
                                self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨል") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠤࠥሎ"))
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢሏ"),e)
    def __1l1lllllll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, self.bstack1l1lllll1ll_opy_, False):
            return
        if not f.bstack1ll11111ll1_opy_(f.hub_url(driver)):
            self.bstack1l1llllllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤሐ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠧࠨሑ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣሒ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠢࠣሓ"))
    def __1l1llllll11_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11111l11_opy_(instance)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡳࡸ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥሔ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠤࠥሕ"))
    def bstack1ll11111111_opy_(self, context: bstack1lllllll1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1lllll1l1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1lllllll_opy_.bstack1l1lllll11l_opy_(data[1])
                    and data[1].bstack1l1lllll1l1_opy_(context)
                    and getattr(data[0](), bstack11ll1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢሖ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1ll1ll_opy_, reverse=reverse)
    def bstack1l1llllll1l_opy_(self, context: bstack1lllllll1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        for data in self.bstack1l1llllllll_opy_.values():
            if (
                data[1].bstack1l1lllll1l1_opy_(context)
                and getattr(data[0](), bstack11ll1l1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣሗ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1ll1ll_opy_, reverse=reverse)
    def bstack1l1lllll111_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11111l11_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        if self.bstack1l1lllll111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, self.bstack1l1lllll1ll_opy_, False)
            return True
        return False