# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1111111ll1_opy_,
    bstack111111l1l1_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11l_opy_ import bstack1lll1lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1lllll1l1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
import weakref
class bstack1ll11111111_opy_(bstack1llll1111ll_opy_):
    bstack1ll111111ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    def __init__(self, bstack1ll111111ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1lllllll1_opy_ = dict()
        self.bstack1ll111111ll_opy_ = bstack1ll111111ll_opy_
        self.frameworks = frameworks
        bstack1lll1lll1ll_opy_.bstack1ll11llll11_opy_((bstack1lllll1lll1_opy_.bstack1lllll1l111_opy_, bstack1111111ll1_opy_.POST), self.__1l1lllll1ll_opy_)
        if any(bstack1lll1l1l1ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1l1l1ll_opy_.bstack1ll11llll11_opy_(
                (bstack1lllll1lll1_opy_.bstack1llllllll11_opy_, bstack1111111ll1_opy_.PRE), self.__1ll1111111l_opy_
            )
            bstack1lll1l1l1ll_opy_.bstack1ll11llll11_opy_(
                (bstack1lllll1lll1_opy_.QUIT, bstack1111111ll1_opy_.POST), self.__1l1llllllll_opy_
            )
    def __1l1lllll1ll_opy_(
        self,
        f: bstack1lll1lll1ll_opy_,
        bstack1l1llllll1l_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1ll1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢሊ"):
                return
            contexts = bstack1l1llllll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1ll1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦላ") in page.url:
                                self.logger.debug(bstack1l1ll1_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤሌ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack111111l1l1_opy_.bstack1lllllll1ll_opy_(instance, self.bstack1ll111111ll_opy_, True)
                                self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨል") + str(instance.ref()) + bstack1l1ll1_opy_ (u"ࠤࠥሎ"))
        except Exception as e:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢሏ"),e)
    def __1ll1111111l_opy_(
        self,
        f: bstack1lll1l1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack111111l1l1_opy_.bstack111111l111_opy_(instance, self.bstack1ll111111ll_opy_, False):
            return
        if not f.bstack1ll1111lll1_opy_(f.hub_url(driver)):
            self.bstack1l1lllllll1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack111111l1l1_opy_.bstack1lllllll1ll_opy_(instance, self.bstack1ll111111ll_opy_, True)
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤሐ") + str(instance.ref()) + bstack1l1ll1_opy_ (u"ࠧࠨሑ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack111111l1l1_opy_.bstack1lllllll1ll_opy_(instance, self.bstack1ll111111ll_opy_, True)
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣሒ") + str(instance.ref()) + bstack1l1ll1_opy_ (u"ࠢࠣሓ"))
    def __1l1llllllll_opy_(
        self,
        f: bstack1lll1l1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11111l1l_opy_(instance)
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡳࡸ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥሔ") + str(instance.ref()) + bstack1l1ll1_opy_ (u"ࠤࠥሕ"))
    def bstack1l1lllll111_opy_(self, context: bstack1lllll1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11111l11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1l1l1ll_opy_.bstack1l1lllll1l1_opy_(data[1])
                    and data[1].bstack1ll11111l11_opy_(context)
                    and getattr(data[0](), bstack1l1ll1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢሖ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllllllll_opy_, reverse=reverse)
    def bstack1l1llllll11_opy_(self, context: bstack1lllll1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        for data in self.bstack1l1lllllll1_opy_.values():
            if (
                data[1].bstack1ll11111l11_opy_(context)
                and getattr(data[0](), bstack1l1ll1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣሗ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllllllll_opy_, reverse=reverse)
    def bstack1l1lllll11l_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11111l1l_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        if self.bstack1l1lllll11l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack111111l1l1_opy_.bstack1lllllll1ll_opy_(instance, self.bstack1ll111111ll_opy_, False)
            return True
        return False