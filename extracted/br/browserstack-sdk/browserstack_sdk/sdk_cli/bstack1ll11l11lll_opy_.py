# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1ll_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import (
    bstack1llllllllll_opy_,
    bstack11111lll1l_opy_,
    bstack111111ll11_opy_,
    bstack11111ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11111_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack11111l1ll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1l1l1ll_opy_ import bstack1ll1llll1ll_opy_
import weakref
class bstack1ll11l11l1l_opy_(bstack1ll1llll1ll_opy_):
    bstack1ll11l11l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111ll111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111ll111_opy_]]
    def __init__(self, bstack1ll11l11l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l1l1ll_opy_ = dict()
        self.bstack1ll11l11l11_opy_ = bstack1ll11l11l11_opy_
        self.frameworks = frameworks
        bstack1llll11l111_opy_.bstack1ll1ll1l111_opy_((bstack1llllllllll_opy_.bstack1111l11lll_opy_, bstack11111lll1l_opy_.POST), self.__1ll11l111l1_opy_)
        if any(bstack1lll11lllll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll11lllll_opy_.bstack1ll1ll1l111_opy_(
                (bstack1llllllllll_opy_.bstack1111l11111_opy_, bstack11111lll1l_opy_.PRE), self.__1ll11l1l1l1_opy_
            )
            bstack1lll11lllll_opy_.bstack1ll1ll1l111_opy_(
                (bstack1llllllllll_opy_.QUIT, bstack11111lll1l_opy_.POST), self.__1ll11l1111l_opy_
            )
    def __1ll11l111l1_opy_(
        self,
        f: bstack1llll11l111_opy_,
        bstack1ll11l1ll11_opy_: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1lll_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᆥ"):
                return
            contexts = bstack1ll11l1ll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1lll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᆦ") in page.url:
                                self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᆧ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack111111ll11_opy_.bstack1111l11l1l_opy_(instance, self.bstack1ll11l11l11_opy_, True)
                                self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᆨ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠨࠢᆩ"))
        except Exception as e:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᆪ"),e)
    def __1ll11l1l1l1_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, self.bstack1ll11l11l11_opy_, False):
            return
        if not f.bstack1ll11ll11l1_opy_(f.hub_url(driver)):
            self.bstack1ll11l1l1ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack111111ll11_opy_.bstack1111l11l1l_opy_(instance, self.bstack1ll11l11l11_opy_, True)
            self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᆫ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠤࠥᆬ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack111111ll11_opy_.bstack1111l11l1l_opy_(instance, self.bstack1ll11l11l11_opy_, True)
        self.logger.debug(bstack1l1lll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᆭ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠦࠧᆮ"))
    def __1ll11l1111l_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l111ll_opy_(instance)
        self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆯ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠨࠢᆰ"))
    def bstack1ll11l1l11l_opy_(self, context: bstack11111l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111ll111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l1l111_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll11lllll_opy_.bstack1ll11llllll_opy_(data[1])
                    and data[1].bstack1ll11l1l111_opy_(context)
                    and getattr(data[0](), bstack1l1lll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᆱ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l11l11_opy_, reverse=reverse)
    def bstack1ll11l11ll1_opy_(self, context: bstack11111l1ll1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111ll111_opy_]]:
        matches = []
        for data in self.bstack1ll11l1l1ll_opy_.values():
            if (
                data[1].bstack1ll11l1l111_opy_(context)
                and getattr(data[0](), bstack1l1lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᆲ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l11l11_opy_, reverse=reverse)
    def bstack1ll11l1ll1l_opy_(self, instance: bstack11111ll111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l111ll_opy_(self, instance: bstack11111ll111_opy_) -> bool:
        if self.bstack1ll11l1ll1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack111111ll11_opy_.bstack1111l11l1l_opy_(instance, self.bstack1ll11l11l11_opy_, False)
            return True
        return False