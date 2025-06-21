# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1llllll1lll_opy_,
    bstack1111111111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1lllll1ll1l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
import weakref
class bstack1ll11111lll_opy_(bstack1llll11l1ll_opy_):
    bstack1ll1111l111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111111111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111111111_opy_]]
    def __init__(self, bstack1ll1111l111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll1111ll1l_opy_ = dict()
        self.bstack1ll1111l111_opy_ = bstack1ll1111l111_opy_
        self.frameworks = frameworks
        bstack1ll1lllllll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1111111lll_opy_, bstack1lllll1llll_opy_.POST), self.__1ll11111ll1_opy_)
        if any(bstack1llll111lll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll111lll_opy_.bstack1ll111lll1l_opy_(
                (bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.__1ll1111l11l_opy_
            )
            bstack1llll111lll_opy_.bstack1ll111lll1l_opy_(
                (bstack1lllll1l111_opy_.QUIT, bstack1lllll1llll_opy_.POST), self.__1ll111111ll_opy_
            )
    def __1ll11111ll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        bstack1ll1111ll11_opy_: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1l1l1_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᇪ"):
                return
            contexts = bstack1ll1111ll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1l1l1_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᇫ") in page.url:
                                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᇬ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, self.bstack1ll1111l111_opy_, True)
                                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡳࡥ࡬࡫࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᇭ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠧࠨᇮ"))
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࠼ࠥᇯ"),e)
    def __1ll1111l11l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, self.bstack1ll1111l111_opy_, False):
            return
        if not f.bstack1ll111l1l1l_opy_(f.hub_url(driver)):
            self.bstack1ll1111ll1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, self.bstack1ll1111l111_opy_, True)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᇰ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠣࠤᇱ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, self.bstack1ll1111l111_opy_, True)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᇲ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠥࠦᇳ"))
    def __1ll111111ll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll1111111l_opy_(instance)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᇴ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠧࠨᇵ"))
    def bstack1ll1111l1l1_opy_(self, context: bstack1lllll1ll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll111111l1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll111lll_opy_.bstack1ll11111l11_opy_(data[1])
                    and data[1].bstack1ll111111l1_opy_(context)
                    and getattr(data[0](), bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᇶ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll111ll_opy_, reverse=reverse)
    def bstack1ll11111l1l_opy_(self, context: bstack1lllll1ll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111111_opy_]]:
        matches = []
        for data in self.bstack1ll1111ll1l_opy_.values():
            if (
                data[1].bstack1ll111111l1_opy_(context)
                and getattr(data[0](), bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᇷ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lllll111ll_opy_, reverse=reverse)
    def bstack1ll11111111_opy_(self, instance: bstack1111111111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll1111111l_opy_(self, instance: bstack1111111111_opy_) -> bool:
        if self.bstack1ll11111111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, self.bstack1ll1111l111_opy_, False)
            return True
        return False