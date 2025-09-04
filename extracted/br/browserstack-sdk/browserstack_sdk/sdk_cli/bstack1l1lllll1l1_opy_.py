# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll11_opy_,
    bstack1llllllll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack1llll1l1ll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
import weakref
class bstack1l1llll1lll_opy_(bstack1lll1lll111_opy_):
    bstack1l1lllll11l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llllllll1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llllllll1l_opy_]]
    def __init__(self, bstack1l1lllll11l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llll1l11_opy_ = dict()
        self.bstack1l1lllll11l_opy_ = bstack1l1lllll11l_opy_
        self.frameworks = frameworks
        bstack1ll1lll1lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1ll11_opy_, bstack1llll1lllll_opy_.POST), self.__1l1llllll1l_opy_)
        if any(bstack1lll1l111ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_(
                (bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.__1l1llll11l1_opy_
            )
            bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_(
                (bstack1lllll11111_opy_.QUIT, bstack1llll1lllll_opy_.POST), self.__1l1lllll1ll_opy_
            )
    def __1l1llllll1l_opy_(
        self,
        f: bstack1ll1lll1lll_opy_,
        bstack1l1llll11ll_opy_: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1111l1l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨ቏"):
                return
            contexts = bstack1l1llll11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111l1l_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥቐ") in page.url:
                                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣቑ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll11l_opy_, True)
                                self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧቒ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠣࠤቓ"))
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨቔ"),e)
    def __1l1llll11l1_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, self.bstack1l1lllll11l_opy_, False):
            return
        if not f.bstack1l1lllllll1_opy_(f.hub_url(driver)):
            self.bstack1l1llll1l11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll11l_opy_, True)
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣቕ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠦࠧቖ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll11l_opy_, True)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ቗") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠨࠢቘ"))
    def __1l1lllll1ll_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1llllll11_opy_(instance)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ቙") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠣࠤቚ"))
    def bstack1l1llll1ll1_opy_(self, context: bstack1llll1l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllllll1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1llll1l1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1l111ll_opy_.bstack1l1lllll111_opy_(data[1])
                    and data[1].bstack1l1llll1l1l_opy_(context)
                    and getattr(data[0](), bstack1111l1l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨቛ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1l1l11_opy_, reverse=reverse)
    def bstack1l1llll111l_opy_(self, context: bstack1llll1l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllllll1l_opy_]]:
        matches = []
        for data in self.bstack1l1llll1l11_opy_.values():
            if (
                data[1].bstack1l1llll1l1l_opy_(context)
                and getattr(data[0](), bstack1111l1l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢቜ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1l1l11_opy_, reverse=reverse)
    def bstack1l1llll1111_opy_(self, instance: bstack1llllllll1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1llllll11_opy_(self, instance: bstack1llllllll1l_opy_) -> bool:
        if self.bstack1l1llll1111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll11l_opy_, False)
            return True
        return False