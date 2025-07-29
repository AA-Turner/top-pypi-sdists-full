# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
    bstack1llll1lll11_opy_,
    bstack11111111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11l1l_opy_ import bstack1llllllll11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
import weakref
class bstack1l1lllll1l1_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1lllll1ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111111l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111111l1_opy_]]
    def __init__(self, bstack1l1lllll1ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1llll1ll1_opy_ = dict()
        self.bstack1l1lllll1ll_opy_ = bstack1l1lllll1ll_opy_
        self.frameworks = frameworks
        bstack1ll1lllll1l_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_, bstack1llllllll1l_opy_.POST), self.__1l1llll1l1l_opy_)
        if any(bstack1ll1l1lll11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_(
                (bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.PRE), self.__1l1llll1l11_opy_
            )
            bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_(
                (bstack1llllllllll_opy_.QUIT, bstack1llllllll1l_opy_.POST), self.__1ll11111111_opy_
            )
    def __1l1llll1l1l_opy_(
        self,
        f: bstack1ll1lllll1l_opy_,
        bstack1l1llllllll_opy_: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstackl_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤቄ"):
                return
            contexts = bstack1l1llllllll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstackl_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨቅ") in page.url:
                                self.logger.debug(bstackl_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦቆ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
                                self.logger.debug(bstackl_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣቇ") + str(instance.ref()) + bstackl_opy_ (u"ࠦࠧቈ"))
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤ቉"),e)
    def __1l1llll1l11_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1l1lllll1ll_opy_, False):
            return
        if not f.bstack1ll111111l1_opy_(f.hub_url(driver)):
            self.bstack1l1llll1ll1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
            self.logger.debug(bstackl_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦቊ") + str(instance.ref()) + bstackl_opy_ (u"ࠢࠣቋ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll1ll_opy_, True)
        self.logger.debug(bstackl_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥቌ") + str(instance.ref()) + bstackl_opy_ (u"ࠤࠥቍ"))
    def __1ll11111111_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1lllllll1_opy_(instance)
        self.logger.debug(bstackl_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ቎") + str(instance.ref()) + bstackl_opy_ (u"ࠦࠧ቏"))
    def bstack1l1llllll1l_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack11111111l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1llll1lll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1l1lll11_opy_.bstack1l1llll11ll_opy_(data[1])
                    and data[1].bstack1l1llll1lll_opy_(context)
                    and getattr(data[0](), bstackl_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤቐ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1l1lll_opy_, reverse=reverse)
    def bstack1l1lllll11l_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack11111111l1_opy_]]:
        matches = []
        for data in self.bstack1l1llll1ll1_opy_.values():
            if (
                data[1].bstack1l1llll1lll_opy_(context)
                and getattr(data[0](), bstackl_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥቑ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll1l1lll_opy_, reverse=reverse)
    def bstack1l1llllll11_opy_(self, instance: bstack11111111l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1lllllll1_opy_(self, instance: bstack11111111l1_opy_) -> bool:
        if self.bstack1l1llllll11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, self.bstack1l1lllll1ll_opy_, False)
            return True
        return False