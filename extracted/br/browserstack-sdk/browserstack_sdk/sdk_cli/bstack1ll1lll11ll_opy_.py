# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1ll1lllll11_opy_,
    bstack1lll1llll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1lll_opy_ import bstack1ll1ll1l11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
import weakref
class bstack1ll1ll1l1ll_opy_(bstack1lll1lllll1_opy_):
    bstack1ll1ll1l1l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lll1llll11_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lll1llll11_opy_]]
    def __init__(self, bstack1ll1ll1l1l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll1llll1ll_opy_ = dict()
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
        self.frameworks = frameworks
        bstack1ll1lll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_, bstack1llllll1l1l_opy_.POST), self.__1ll1lll111l_opy_)
        if any(bstack1lll1ll1l1l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_(
                (bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.__1ll1llll111_opy_
            )
            bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_(
                (bstack1lll1llllll_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.__1ll1llll11l_opy_
            )
    def __1ll1lll111l_opy_(
        self,
        f: bstack1ll1lll1l1l_opy_,
        bstack1ll1lll11l1_opy_: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1111_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᅄ"):
                return
            contexts = bstack1ll1lll11l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1111_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᅅ") in page.url:
                                self.logger.debug(bstack11l1111_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᅆ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, self.bstack1ll1ll1l1l1_opy_, True)
                                self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᅇ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠢࠣᅈ"))
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧᅉ"),e)
    def __1ll1llll111_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, self.bstack1ll1ll1l1l1_opy_, False):
            return
        if not f.bstack1lll1111l11_opy_(f.hub_url(driver)):
            self.bstack1ll1llll1ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, self.bstack1ll1ll1l1l1_opy_, True)
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᅊ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠥࠦᅋ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, self.bstack1ll1ll1l1l1_opy_, True)
        self.logger.debug(bstack11l1111_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᅌ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠧࠨᅍ"))
    def __1ll1llll11l_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll1ll1ll11_opy_(instance)
        self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᅎ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠢࠣᅏ"))
    def bstack1ll1llll1l1_opy_(self, context: bstack1ll1ll1l11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1llll11_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll1ll1lll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1ll1l1l_opy_.bstack1ll1lllll1l_opy_(data[1])
                    and data[1].bstack1ll1ll1lll1_opy_(context)
                    and getattr(data[0](), bstack11l1111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᅐ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1l11_opy_, reverse=reverse)
    def bstack1ll1lll1ll1_opy_(self, context: bstack1ll1ll1l11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll1llll11_opy_]]:
        matches = []
        for data in self.bstack1ll1llll1ll_opy_.values():
            if (
                data[1].bstack1ll1ll1lll1_opy_(context)
                and getattr(data[0](), bstack11l1111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᅑ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1l11_opy_, reverse=reverse)
    def bstack1ll1lll1111_opy_(self, instance: bstack1lll1llll11_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll1ll1ll11_opy_(self, instance: bstack1lll1llll11_opy_) -> bool:
        if self.bstack1ll1lll1111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, self.bstack1ll1ll1l1l1_opy_, False)
            return True
        return False