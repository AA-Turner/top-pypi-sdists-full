# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll1l1l_opy_,
    bstack1lll1l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1ll1_opy_ import bstack1ll1ll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll11lll11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
import weakref
class bstack1l1l1l111ll_opy_(bstack1ll1ll111l1_opy_):
    bstack1l1l1l1ll1l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lll1l1111l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lll1l1111l_opy_]]
    def __init__(self, bstack1l1l1l1ll1l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1l1ll1111_opy_ = dict()
        self.bstack1l1l1l1ll1l_opy_ = bstack1l1l1l1ll1l_opy_
        self.frameworks = frameworks
        bstack1ll1ll11ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_, bstack1lll1l1ll1l_opy_.POST), self.__1l1l1l1l11l_opy_)
        if any(bstack1ll1l111l1l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_(
                (bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.__1l1l1l1lll1_opy_
            )
            bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_(
                (bstack1lll111lll1_opy_.QUIT, bstack1lll1l1ll1l_opy_.POST), self.__1l1l1l11ll1_opy_
            )
    def __1l1l1l1l11l_opy_(
        self,
        f: bstack1ll1ll11ll1_opy_,
        bstack1l1l1l1l111_opy_: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1111_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥፁ"):
                return
            contexts = bstack1l1l1l1l111_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1111_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢፂ") in page.url:
                                self.logger.debug(bstack1l1111_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧፃ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, self.bstack1l1l1l1ll1l_opy_, True)
                                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡳࡥ࡬࡫࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤፄ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠧࠨፅ"))
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࠼ࠥፆ"),e)
    def __1l1l1l1lll1_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, self.bstack1l1l1l1ll1l_opy_, False):
            return
        if not f.bstack1l1l1ll1lll_opy_(f.hub_url(driver)):
            self.bstack1l1l1ll1111_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, self.bstack1l1l1l1ll1l_opy_, True)
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧፇ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠣࠤፈ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, self.bstack1l1l1l1ll1l_opy_, True)
        self.logger.debug(bstack1l1111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦፉ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠥࠦፊ"))
    def __1l1l1l11ll1_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1l1l1ll11_opy_(instance)
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨፋ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠧࠨፌ"))
    def bstack1l1l1l11lll_opy_(self, context: bstack1lll11lll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1l1111l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1l1l11l11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1l111l1l_opy_.bstack1l1l1l1l1l1_opy_(data[1])
                    and data[1].bstack1l1l1l11l11_opy_(context)
                    and getattr(data[0](), bstack1l1111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥፍ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll1lll111_opy_, reverse=reverse)
    def bstack1l1l1l1l1ll_opy_(self, context: bstack1lll11lll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1l1111l_opy_]]:
        matches = []
        for data in self.bstack1l1l1ll1111_opy_.values():
            if (
                data[1].bstack1l1l1l11l11_opy_(context)
                and getattr(data[0](), bstack1l1111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦፎ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll1lll111_opy_, reverse=reverse)
    def bstack1l1l1l1llll_opy_(self, instance: bstack1lll1l1111l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1l1l1ll11_opy_(self, instance: bstack1lll1l1111l_opy_) -> bool:
        if self.bstack1l1l1l1llll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, self.bstack1l1l1l1ll1l_opy_, False)
            return True
        return False