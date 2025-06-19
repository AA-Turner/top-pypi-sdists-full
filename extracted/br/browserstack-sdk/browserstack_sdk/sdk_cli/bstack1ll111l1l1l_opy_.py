# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1111111l11_opy_,
    bstack1llllll111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllllll1l_opy_ import bstack1llllllll11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
import weakref
class bstack1ll111l1111_opy_(bstack1lll1l11ll1_opy_):
    bstack1ll111l1l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llllll111l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llllll111l_opy_]]
    def __init__(self, bstack1ll111l1l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll111ll111_opy_ = dict()
        self.bstack1ll111l1l11_opy_ = bstack1ll111l1l11_opy_
        self.frameworks = frameworks
        bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllllll1l1_opy_, bstack11111l1ll1_opy_.POST), self.__1ll111ll1l1_opy_)
        if any(bstack1llll111lll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_(
                (bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.__1ll111ll11l_opy_
            )
            bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_(
                (bstack1111111111_opy_.QUIT, bstack11111l1ll1_opy_.POST), self.__1ll111lll11_opy_
            )
    def __1ll111ll1l1_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        bstack1ll111l11ll_opy_: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack111lll_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᇛ"):
                return
            contexts = bstack1ll111l11ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111lll_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨᇜ") in page.url:
                                self.logger.debug(bstack111lll_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᇝ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111111l11_opy_.bstack11111ll111_opy_(instance, self.bstack1ll111l1l11_opy_, True)
                                self.logger.debug(bstack111lll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᇞ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠦࠧᇟ"))
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤᇠ"),e)
    def __1ll111ll11l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, self.bstack1ll111l1l11_opy_, False):
            return
        if not f.bstack1ll111llll1_opy_(f.hub_url(driver)):
            self.bstack1ll111ll111_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111111l11_opy_.bstack11111ll111_opy_(instance, self.bstack1ll111l1l11_opy_, True)
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᇡ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠢࠣᇢ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111111l11_opy_.bstack11111ll111_opy_(instance, self.bstack1ll111l1l11_opy_, True)
        self.logger.debug(bstack111lll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᇣ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠤࠥᇤ"))
    def __1ll111lll11_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll1111llll_opy_(instance)
        self.logger.debug(bstack111lll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᇥ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠦࠧᇦ"))
    def bstack1ll111l11l1_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll111l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll111l1ll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll111lll_opy_.bstack1ll111l111l_opy_(data[1])
                    and data[1].bstack1ll111l1ll1_opy_(context)
                    and getattr(data[0](), bstack111lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᇧ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll1l_opy_, reverse=reverse)
    def bstack1ll111ll1ll_opy_(self, context: bstack1llllllll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll111l_opy_]]:
        matches = []
        for data in self.bstack1ll111ll111_opy_.values():
            if (
                data[1].bstack1ll111l1ll1_opy_(context)
                and getattr(data[0](), bstack111lll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᇨ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll1l_opy_, reverse=reverse)
    def bstack1ll111l1lll_opy_(self, instance: bstack1llllll111l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll1111llll_opy_(self, instance: bstack1llllll111l_opy_) -> bool:
        if self.bstack1ll111l1lll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111111l11_opy_.bstack11111ll111_opy_(instance, self.bstack1ll111l1l11_opy_, False)
            return True
        return False