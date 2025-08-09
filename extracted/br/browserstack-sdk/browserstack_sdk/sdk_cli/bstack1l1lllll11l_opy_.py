# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll111ll_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1llllll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1llllllll11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llll11l11l_opy_
import weakref
class bstack1ll111111ll_opy_(bstack1llll11l11l_opy_):
    bstack1l1lllll1ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllll1ll1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllll1ll1l_opy_]]
    def __init__(self, bstack1l1lllll1ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llllllll_opy_ = dict()
        self.bstack1l1lllll1ll_opy_ = bstack1l1lllll1ll_opy_
        self.frameworks = frameworks
        bstack1lll1llllll_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll11ll_opy_, bstack1llll1lll11_opy_.POST), self.__1l1lllll111_opy_)
        if any(bstack1llll1l11l1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_(
                (bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.PRE), self.__1l1llll1lll_opy_
            )
            bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_(
                (bstack1llllllllll_opy_.QUIT, bstack1llll1lll11_opy_.POST), self.__1ll11111111_opy_
            )
    def __1l1lllll111_opy_(
        self,
        f: bstack1lll1llllll_opy_,
        bstack1l1llllll11_opy_: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤቄ"):
                return
            contexts = bstack1l1llllll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨቅ") in page.url:
                                self.logger.debug(bstack11l1_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦቆ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lllll111ll_opy_.bstack1111111lll_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
                                self.logger.debug(bstack11l1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣቇ") + str(instance.ref()) + bstack11l1_opy_ (u"ࠦࠧቈ"))
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤ቉"),e)
    def __1l1llll1lll_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lllll111ll_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll1ll_opy_, False):
            return
        if not f.bstack1ll1111l1ll_opy_(f.hub_url(driver)):
            self.bstack1l1llllllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lllll111ll_opy_.bstack1111111lll_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
            self.logger.debug(bstack11l1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦቊ") + str(instance.ref()) + bstack11l1_opy_ (u"ࠢࠣቋ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lllll111ll_opy_.bstack1111111lll_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
        self.logger.debug(bstack11l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥቌ") + str(instance.ref()) + bstack11l1_opy_ (u"ࠤࠥቍ"))
    def __1ll11111111_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1lllll1l1_opy_(instance)
        self.logger.debug(bstack11l1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ቎") + str(instance.ref()) + bstack11l1_opy_ (u"ࠦࠧ቏"))
    def bstack1ll111111l1_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1lllllll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll1l11l1_opy_.bstack1ll11111l11_opy_(data[1])
                    and data[1].bstack1l1lllllll1_opy_(context)
                    and getattr(data[0](), bstack11l1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤቐ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll11ll1_opy_, reverse=reverse)
    def bstack1ll1111111l_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll1l_opy_]]:
        matches = []
        for data in self.bstack1l1llllllll_opy_.values():
            if (
                data[1].bstack1l1lllllll1_opy_(context)
                and getattr(data[0](), bstack11l1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥቑ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll11ll1_opy_, reverse=reverse)
    def bstack1l1llllll1l_opy_(self, instance: bstack1lllll1ll1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1lllll1l1_opy_(self, instance: bstack1lllll1ll1l_opy_) -> bool:
        if self.bstack1l1llllll1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lllll111ll_opy_.bstack1111111lll_opy_(instance, self.bstack1l1lllll1ll_opy_, False)
            return True
        return False