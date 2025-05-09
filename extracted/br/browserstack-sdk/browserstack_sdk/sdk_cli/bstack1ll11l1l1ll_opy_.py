# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack1llllllll1l_opy_,
    bstack11111l1ll1_opy_,
    bstack111111l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack111111ll1l_opy_ import bstack1111l111ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1lll1_opy_
import weakref
class bstack1ll11l111ll_opy_(bstack1lll1l1lll1_opy_):
    bstack1ll11l11l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack111111l1ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack111111l1ll_opy_]]
    def __init__(self, bstack1ll11l11l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l111l1_opy_ = dict()
        self.bstack1ll11l11l11_opy_ = bstack1ll11l11l11_opy_
        self.frameworks = frameworks
        bstack1lll1lll111_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111ll11l_opy_, bstack1llllllll1l_opy_.POST), self.__1ll11l11lll_opy_)
        if any(bstack1lll1ll1lll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_(
                (bstack1lllllll1l1_opy_.bstack11111lll1l_opy_, bstack1llllllll1l_opy_.PRE), self.__1ll11l1111l_opy_
            )
            bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_(
                (bstack1lllllll1l1_opy_.QUIT, bstack1llllllll1l_opy_.POST), self.__1ll11l1l11l_opy_
            )
    def __1ll11l11lll_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1ll11l11l1l_opy_: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11lll_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᆥ"):
                return
            contexts = bstack1ll11l11l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11lll_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᆦ") in page.url:
                                self.logger.debug(bstack11lll_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᆧ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111l1ll1_opy_.bstack11111llll1_opy_(instance, self.bstack1ll11l11l11_opy_, True)
                                self.logger.debug(bstack11lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᆨ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠨࠢᆩ"))
        except Exception as e:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᆪ"),e)
    def __1ll11l1111l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111l1ll1_opy_.bstack111111l1l1_opy_(instance, self.bstack1ll11l11l11_opy_, False):
            return
        if not f.bstack1ll11l1llll_opy_(f.hub_url(driver)):
            self.bstack1ll11l111l1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111l1ll1_opy_.bstack11111llll1_opy_(instance, self.bstack1ll11l11l11_opy_, True)
            self.logger.debug(bstack11lll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᆫ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠤࠥᆬ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111l1ll1_opy_.bstack11111llll1_opy_(instance, self.bstack1ll11l11l11_opy_, True)
        self.logger.debug(bstack11lll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᆭ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠦࠧᆮ"))
    def __1ll11l1l11l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll111lllll_opy_(instance)
        self.logger.debug(bstack11lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆯ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠨࠢᆰ"))
    def bstack1ll11l11111_opy_(self, context: bstack1111l111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack111111l1ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l1l1l1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(data[1])
                    and data[1].bstack1ll11l1l1l1_opy_(context)
                    and getattr(data[0](), bstack11lll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᆱ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll11_opy_, reverse=reverse)
    def bstack1ll11l11ll1_opy_(self, context: bstack1111l111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack111111l1ll_opy_]]:
        matches = []
        for data in self.bstack1ll11l111l1_opy_.values():
            if (
                data[1].bstack1ll11l1l1l1_opy_(context)
                and getattr(data[0](), bstack11lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᆲ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll11_opy_, reverse=reverse)
    def bstack1ll11l1l111_opy_(self, instance: bstack111111l1ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll111lllll_opy_(self, instance: bstack111111l1ll_opy_) -> bool:
        if self.bstack1ll11l1l111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111l1ll1_opy_.bstack11111llll1_opy_(instance, self.bstack1ll11l11l11_opy_, False)
            return True
        return False