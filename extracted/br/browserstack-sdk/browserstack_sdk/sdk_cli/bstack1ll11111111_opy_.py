# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack11111111ll_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1ll1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll11_opy_ import bstack1llll1ll11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
import weakref
class bstack1l1llll1lll_opy_(bstack1llll1l1l11_opy_):
    bstack1ll1111111l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllll1ll1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllll1ll1l_opy_]]
    def __init__(self, bstack1ll1111111l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1lllll1l1_opy_ = dict()
        self.bstack1ll1111111l_opy_ = bstack1ll1111111l_opy_
        self.frameworks = frameworks
        bstack1ll1llll11l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.POST), self.__1l1lllll111_opy_)
        if any(bstack1lll1l11l11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_(
                (bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.__1l1llll1l1l_opy_
            )
            bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_(
                (bstack1lllllll11l_opy_.QUIT, bstack1llllll1111_opy_.POST), self.__1l1llllllll_opy_
            )
    def __1l1lllll111_opy_(
        self,
        f: bstack1ll1llll11l_opy_,
        bstack1l1lllll11l_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack111l111_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣቃ"):
                return
            contexts = bstack1l1lllll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111l111_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧቄ") in page.url:
                                self.logger.debug(bstack111l111_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥቅ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111111ll_opy_.bstack1111111111_opy_(instance, self.bstack1ll1111111l_opy_, True)
                                self.logger.debug(bstack111l111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢቆ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠥࠦቇ"))
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣቈ"),e)
    def __1l1llll1l1l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, self.bstack1ll1111111l_opy_, False):
            return
        if not f.bstack1ll11111lll_opy_(f.hub_url(driver)):
            self.bstack1l1lllll1l1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111111ll_opy_.bstack1111111111_opy_(instance, self.bstack1ll1111111l_opy_, True)
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ቉") + str(instance.ref()) + bstack111l111_opy_ (u"ࠨࠢቊ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111111ll_opy_.bstack1111111111_opy_(instance, self.bstack1ll1111111l_opy_, True)
        self.logger.debug(bstack111l111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤቋ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠣࠤቌ"))
    def __1l1llllllll_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1llll1l11_opy_(instance)
        self.logger.debug(bstack111l111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦቍ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠥࠦ቎"))
    def bstack1l1lllllll1_opy_(self, context: bstack1llll1ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1llllll11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1l11l11_opy_.bstack1l1llllll1l_opy_(data[1])
                    and data[1].bstack1l1llllll11_opy_(context)
                    and getattr(data[0](), bstack111l111_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣ቏"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll111ll_opy_, reverse=reverse)
    def bstack1l1llll1ll1_opy_(self, context: bstack1llll1ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll1l_opy_]]:
        matches = []
        for data in self.bstack1l1lllll1l1_opy_.values():
            if (
                data[1].bstack1l1llllll11_opy_(context)
                and getattr(data[0](), bstack111l111_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤቐ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll111ll_opy_, reverse=reverse)
    def bstack1l1lllll1ll_opy_(self, instance: bstack1lllll1ll1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1llll1l11_opy_(self, instance: bstack1lllll1ll1l_opy_) -> bool:
        if self.bstack1l1lllll1ll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111111ll_opy_.bstack1111111111_opy_(instance, self.bstack1ll1111111l_opy_, False)
            return True
        return False