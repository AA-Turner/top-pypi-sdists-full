# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1llllllll1l_opy_,
    bstack1lllllll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1ll1l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll111l_opy_ import bstack1llll1lllll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
import weakref
class bstack1l1lllll111_opy_(bstack1ll1l1llll1_opy_):
    bstack1l1llll1l1l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllllll111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllllll111_opy_]]
    def __init__(self, bstack1l1llll1l1l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llll1ll1_opy_ = dict()
        self.bstack1l1llll1l1l_opy_ = bstack1l1llll1l1l_opy_
        self.frameworks = frameworks
        bstack1ll1l1lllll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_, bstack1llll1l11ll_opy_.POST), self.__1l1lll1llll_opy_)
        if any(bstack1ll1l1l1lll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_(
                (bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.__1l1lllll1ll_opy_
            )
            bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_(
                (bstack1lllll1l111_opy_.QUIT, bstack1llll1l11ll_opy_.POST), self.__1l1llll11l1_opy_
            )
    def __1l1lll1llll_opy_(
        self,
        f: bstack1ll1l1lllll_opy_,
        bstack1l1llll11ll_opy_: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l11ll1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦቍ"):
                return
            contexts = bstack1l1llll11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l11ll1_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣ቎") in page.url:
                                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨ቏"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, self.bstack1l1llll1l1l_opy_, True)
                                self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥቐ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠨࠢቑ"))
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦቒ"),e)
    def __1l1lllll1ll_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, self.bstack1l1llll1l1l_opy_, False):
            return
        if not f.bstack1ll11111ll1_opy_(f.hub_url(driver)):
            self.bstack1l1llll1ll1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, self.bstack1l1llll1l1l_opy_, True)
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨቓ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠤࠥቔ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, self.bstack1l1llll1l1l_opy_, True)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧቕ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠦࠧቖ"))
    def __1l1llll11l1_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1llll1l11_opy_(instance)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ቗") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠨࠢቘ"))
    def bstack1l1llll1lll_opy_(self, context: bstack1llll1lllll_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllllll111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1llll111l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1l1l1lll_opy_.bstack1l1lllll1l1_opy_(data[1])
                    and data[1].bstack1l1llll111l_opy_(context)
                    and getattr(data[0](), bstack1l11ll1_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ቙"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll1l1ll_opy_, reverse=reverse)
    def bstack1l1lllll11l_opy_(self, context: bstack1llll1lllll_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllllll111_opy_]]:
        matches = []
        for data in self.bstack1l1llll1ll1_opy_.values():
            if (
                data[1].bstack1l1llll111l_opy_(context)
                and getattr(data[0](), bstack1l11ll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧቚ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll1l1ll_opy_, reverse=reverse)
    def bstack1l1llllll11_opy_(self, instance: bstack1lllllll111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1llll1l11_opy_(self, instance: bstack1lllllll111_opy_) -> bool:
        if self.bstack1l1llllll11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, self.bstack1l1llll1l1l_opy_, False)
            return True
        return False