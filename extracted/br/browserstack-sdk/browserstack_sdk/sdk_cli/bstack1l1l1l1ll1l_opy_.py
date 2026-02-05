# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll111llll_opy_,
    bstack1lll11lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1lll11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
import weakref
class bstack1l1l1l1111l_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l1l1l11l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lll11lll1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lll11lll1l_opy_]]
    def __init__(self, bstack1l1l1l11l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1l1l1l11l_opy_ = dict()
        self.bstack1l1l1l11l11_opy_ = bstack1l1l1l11l11_opy_
        self.frameworks = frameworks
        bstack1ll111ll1l1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_, bstack1lll1ll1l11_opy_.POST), self.__1l1l1l11l1l_opy_)
        if any(bstack1ll1ll1lll1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_(
                (bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.__1l1l1l11lll_opy_
            )
            bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_(
                (bstack1lll111lll1_opy_.QUIT, bstack1lll1ll1l11_opy_.POST), self.__1l1l1l1l1l1_opy_
            )
    def __1l1l1l11l1l_opy_(
        self,
        f: bstack1ll111ll1l1_opy_,
        bstack1l1l1l111ll_opy_: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1ll1_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤፇ"):
                return
            contexts = bstack1l1l1l111ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1ll1_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨፈ") in page.url:
                                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦፉ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, self.bstack1l1l1l11l11_opy_, True)
                                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣፊ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠦࠧፋ"))
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤፌ"),e)
    def __1l1l1l11lll_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, self.bstack1l1l1l11l11_opy_, False):
            return
        if not f.bstack1l1l1ll11l1_opy_(f.hub_url(driver)):
            self.bstack1l1l1l1l11l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, self.bstack1l1l1l11l11_opy_, True)
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦፍ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠢࠣፎ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, self.bstack1l1l1l11l11_opy_, True)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥፏ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠤࠥፐ"))
    def __1l1l1l1l1l1_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1l1l1ll11_opy_(instance)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧፑ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠦࠧፒ"))
    def bstack1l1l1l1l111_opy_(self, context: bstack1lll1lll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll11lll1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1l1l11111_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll1ll1lll1_opy_.bstack1l1l1l11ll1_opy_(data[1])
                    and data[1].bstack1l1l1l11111_opy_(context)
                    and getattr(data[0](), bstack11l1ll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤፓ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll1l1l1ll_opy_, reverse=reverse)
    def bstack1l1l1l1l1ll_opy_(self, context: bstack1lll1lll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1lll11lll1l_opy_]]:
        matches = []
        for data in self.bstack1l1l1l1l11l_opy_.values():
            if (
                data[1].bstack1l1l1l11111_opy_(context)
                and getattr(data[0](), bstack11l1ll1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥፔ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1lll1l1l1ll_opy_, reverse=reverse)
    def bstack1l1l1l111l1_opy_(self, instance: bstack1lll11lll1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1l1l1ll11_opy_(self, instance: bstack1lll11lll1l_opy_) -> bool:
        if self.bstack1l1l1l111l1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, self.bstack1l1l1l11l11_opy_, False)
            return True
        return False