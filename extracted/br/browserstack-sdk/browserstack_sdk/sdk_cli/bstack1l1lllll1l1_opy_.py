# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
    bstack11111111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1111111l1l_opy_ import bstack1111111ll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
import weakref
class bstack1ll1111111l_opy_(bstack1llll11l111_opy_):
    bstack1l1lllll111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllll1ll11_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllll1ll11_opy_]]
    def __init__(self, bstack1l1lllll111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1lllll1ll_opy_ = dict()
        self.bstack1l1lllll111_opy_ = bstack1l1lllll111_opy_
        self.frameworks = frameworks
        bstack1llll1l1l11_opy_.bstack1ll11l111l1_opy_((bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_, bstack1llllll1111_opy_.POST), self.__1ll111111l1_opy_)
        if any(bstack1lll1lll11l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1lll11l_opy_.bstack1ll11l111l1_opy_(
                (bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_, bstack1llllll1111_opy_.PRE), self.__1l1llll1l1l_opy_
            )
            bstack1lll1lll11l_opy_.bstack1ll11l111l1_opy_(
                (bstack1lllll1lll1_opy_.QUIT, bstack1llllll1111_opy_.POST), self.__1l1llllll1l_opy_
            )
    def __1ll111111l1_opy_(
        self,
        f: bstack1llll1l1l11_opy_,
        bstack1l1llllll11_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1111lll_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣቊ"):
                return
            contexts = bstack1l1llllll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111lll_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧቋ") in page.url:
                                self.logger.debug(bstack1111lll_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥቌ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1l1lllll111_opy_, True)
                                self.logger.debug(bstack1111lll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢቍ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠥࠦ቎"))
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣ቏"),e)
    def __1l1llll1l1l_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, self.bstack1l1lllll111_opy_, False):
            return
        if not f.bstack1ll1111ll1l_opy_(f.hub_url(driver)):
            self.bstack1l1lllll1ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1l1lllll111_opy_, True)
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥቐ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠨࠢቑ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1l1lllll111_opy_, True)
        self.logger.debug(bstack1111lll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤቒ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠣࠤቓ"))
    def __1l1llllll1l_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1llllllll_opy_(instance)
        self.logger.debug(bstack1111lll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦቔ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠥࠦቕ"))
    def bstack1l1llll1lll_opy_(self, context: bstack1111111ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll11_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1lllllll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1lll11l_opy_.bstack1l1lllll11l_opy_(data[1])
                    and data[1].bstack1l1lllllll1_opy_(context)
                    and getattr(data[0](), bstack1111lll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣቖ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllllll1l_opy_, reverse=reverse)
    def bstack1l1llll1ll1_opy_(self, context: bstack1111111ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll11_opy_]]:
        matches = []
        for data in self.bstack1l1lllll1ll_opy_.values():
            if (
                data[1].bstack1l1lllllll1_opy_(context)
                and getattr(data[0](), bstack1111lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤ቗"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llllllll1l_opy_, reverse=reverse)
    def bstack1ll11111111_opy_(self, instance: bstack1lllll1ll11_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1llllllll_opy_(self, instance: bstack1lllll1ll11_opy_) -> bool:
        if self.bstack1ll11111111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1l1lllll111_opy_, False)
            return True
        return False