# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1111_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1llllll111l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
import weakref
class bstack1l1lllll111_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l1llll1l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llll1ll111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llll1ll111_opy_]]
    def __init__(self, bstack1l1llll1l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1lll1llll_opy_ = dict()
        self.bstack1l1llll1l11_opy_ = bstack1l1llll1l11_opy_
        self.frameworks = frameworks
        bstack1lll1lll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_, bstack1lllll111ll_opy_.POST), self.__1l1llll1111_opy_)
        if any(bstack1ll1l1ll111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_(
                (bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.__1l1lllll1l1_opy_
            )
            bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_(
                (bstack1lllll1l111_opy_.QUIT, bstack1lllll111ll_opy_.POST), self.__1l1llllll11_opy_
            )
    def __1l1llll1111_opy_(
        self,
        f: bstack1lll1lll111_opy_,
        bstack1l1lllll11l_opy_: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll11ll_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧ቎"):
                return
            contexts = bstack1l1lllll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll11ll_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤ቏") in page.url:
                                self.logger.debug(bstack1ll11ll_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢቐ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, self.bstack1l1llll1l11_opy_, True)
                                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦቑ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠢࠣቒ"))
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧቓ"),e)
    def __1l1lllll1l1_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, self.bstack1l1llll1l11_opy_, False):
            return
        if not f.bstack1l1lllllll1_opy_(f.hub_url(driver)):
            self.bstack1l1lll1llll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, self.bstack1l1llll1l11_opy_, True)
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢቔ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠥࠦቕ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, self.bstack1l1llll1l11_opy_, True)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨቖ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠧࠨ቗"))
    def __1l1llllll11_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1llll11l1_opy_(instance)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣቘ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠢࠣ቙"))
    def bstack1l1llll1ll1_opy_(self, context: bstack1llllll111l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llll1ll111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1llll111l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1l1ll111_opy_.bstack1l1llll11ll_opy_(data[1])
                    and data[1].bstack1l1llll111l_opy_(context)
                    and getattr(data[0](), bstack1ll11ll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧቚ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll11lll_opy_, reverse=reverse)
    def bstack1l1llll1lll_opy_(self, context: bstack1llllll111l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llll1ll111_opy_]]:
        matches = []
        for data in self.bstack1l1lll1llll_opy_.values():
            if (
                data[1].bstack1l1llll111l_opy_(context)
                and getattr(data[0](), bstack1ll11ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨቛ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll11lll_opy_, reverse=reverse)
    def bstack1l1lllll1ll_opy_(self, instance: bstack1llll1ll111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1llll11l1_opy_(self, instance: bstack1llll1ll111_opy_) -> bool:
        if self.bstack1l1lllll1ll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, self.bstack1l1llll1l11_opy_, False)
            return True
        return False