# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll111l_opy_,
    bstack1lllllll111_opy_,
    bstack1lllll1l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll1l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11l11_opy_ import bstack1111111111_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll11l1111_opy_
import weakref
class bstack1l1lllll111_opy_(bstack1lll11l1111_opy_):
    bstack1l1llllll11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllll1l1l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllll1l1l1_opy_]]
    def __init__(self, bstack1l1llllll11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llll1l11_opy_ = dict()
        self.bstack1l1llllll11_opy_ = bstack1l1llllll11_opy_
        self.frameworks = frameworks
        bstack1llll11lll1_opy_.bstack1ll111lllll_opy_((bstack1lllll1ll11_opy_.bstack1llll1l1lll_opy_, bstack1llllll111l_opy_.POST), self.__1l1llll1lll_opy_)
        if any(bstack1ll1ll111l1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1ll111l1_opy_.bstack1ll111lllll_opy_(
                (bstack1lllll1ll11_opy_.bstack1111111l11_opy_, bstack1llllll111l_opy_.PRE), self.__1l1lllll1l1_opy_
            )
            bstack1ll1ll111l1_opy_.bstack1ll111lllll_opy_(
                (bstack1lllll1ll11_opy_.QUIT, bstack1llllll111l_opy_.POST), self.__1l1lllllll1_opy_
            )
    def __1l1llll1lll_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1l1llll1l1l_opy_: object,
        exec: Tuple[bstack1lllll1l1l1_opy_, str],
        bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨቁ"):
                return
            contexts = bstack1l1llll1l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥቂ") in page.url:
                                self.logger.debug(bstack1l1_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣቃ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lllllll111_opy_.bstack1llll1ll1ll_opy_(instance, self.bstack1l1llllll11_opy_, True)
                                self.logger.debug(bstack1l1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧቄ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠣࠤቅ"))
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨቆ"),e)
    def __1l1lllll1l1_opy_(
        self,
        f: bstack1ll1ll111l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1l1l1_opy_, str],
        bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lllllll111_opy_.bstack1lllll1l11l_opy_(instance, self.bstack1l1llllll11_opy_, False):
            return
        if not f.bstack1ll1111l111_opy_(f.hub_url(driver)):
            self.bstack1l1llll1l11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lllllll111_opy_.bstack1llll1ll1ll_opy_(instance, self.bstack1l1llllll11_opy_, True)
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣቇ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠦࠧቈ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lllllll111_opy_.bstack1llll1ll1ll_opy_(instance, self.bstack1l1llllll11_opy_, True)
        self.logger.debug(bstack1l1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ቉") + str(instance.ref()) + bstack1l1_opy_ (u"ࠨࠢቊ"))
    def __1l1lllllll1_opy_(
        self,
        f: bstack1ll1ll111l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1l1l1_opy_, str],
        bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11111111_opy_(instance)
        self.logger.debug(bstack1l1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤቋ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠣࠤቌ"))
    def bstack1l1llll11ll_opy_(self, context: bstack1111111111_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1l1l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1lllll11l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1ll111l1_opy_.bstack1l1llll1ll1_opy_(data[1])
                    and data[1].bstack1l1lllll11l_opy_(context)
                    and getattr(data[0](), bstack1l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨቍ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111111l_opy_, reverse=reverse)
    def bstack1l1llllll1l_opy_(self, context: bstack1111111111_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1l1l1_opy_]]:
        matches = []
        for data in self.bstack1l1llll1l11_opy_.values():
            if (
                data[1].bstack1l1lllll11l_opy_(context)
                and getattr(data[0](), bstack1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢ቎"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111111l_opy_, reverse=reverse)
    def bstack1l1llllllll_opy_(self, instance: bstack1lllll1l1l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11111111_opy_(self, instance: bstack1lllll1l1l1_opy_) -> bool:
        if self.bstack1l1llllllll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lllllll111_opy_.bstack1llll1ll1ll_opy_(instance, self.bstack1l1llllll11_opy_, False)
            return True
        return False