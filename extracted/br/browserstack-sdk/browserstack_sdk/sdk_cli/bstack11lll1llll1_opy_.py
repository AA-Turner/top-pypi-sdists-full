# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import (
    bstack1l1111l1l1_opy_,
    bstack1ll111111l_opy_,
    bstack1111lll1ll_opy_,
    bstack1l1ll1111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l1l111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11_opy_ import bstack1l1l11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11ll1l_opy_ import bstack1l1ll11lll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11llll11111_opy_(bstack1l11lll1l1l_opy_):
    bstack11lll1lll1l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1l1ll1111l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1l1ll1111l1_opy_]]
    def __init__(self, bstack11lll1lll1l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11llll11l1l_opy_ = dict()
        self.bstack11lll1lll1l_opy_ = bstack11lll1lll1l_opy_
        self.frameworks = frameworks
        bstack1l1l11ll1l_opy_.bstack1l1111ll11l_opy_((bstack1l1111l1l1_opy_.bstack1l111l11ll_opy_, bstack1ll111111l_opy_.POST), self.__11llll11l11_opy_)
        if any(bstack1l1l111l1ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l1l111l1ll_opy_.bstack1l1111ll11l_opy_(
                (bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_, bstack1ll111111l_opy_.PRE), self.__11lll1ll1l1_opy_
            )
            bstack1l1l111l1ll_opy_.bstack1l1111ll11l_opy_(
                (bstack1l1111l1l1_opy_.QUIT, bstack1ll111111l_opy_.POST), self.__11lll1lll11_opy_
            )
    def __11llll11l11_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack11llll111l1_opy_: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll1l11_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᚩ"):
                return
            contexts = bstack11llll111l1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll1l11_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᚪ") in page.url:
                                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᚫ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111lll1ll_opy_.bstack1ll11l1ll_opy_(instance, self.bstack11lll1lll1l_opy_, True)
                                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᚬ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠤࠥᚭ"))
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢᚮ"),e)
    def __11lll1ll1l1_opy_(
        self,
        f: bstack1l1l111l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111lll1ll_opy_.bstack1l1lll1ll11_opy_(instance, self.bstack11lll1lll1l_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l1ll11l11l_opy_ = None
        if label:
            if bstack1ll1l11_opy_ (u"ࠦࠨࠨᚯ") in label:
                suffix = label.rsplit(bstack1ll1l11_opy_ (u"ࠧࠩࠢᚰ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l1ll11l11l_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l1ll1ll11l_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᚱ")
                    )
            else:
                self.logger.debug(
                    bstack1l1ll1ll11l_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᚲ")
                )
        if bstack1l1ll11l11l_opy_ is not None:
            bstack1l1ll11l11l_opy_ = label.split(bstack1ll1l11_opy_ (u"ࠣࠥࠥᚳ"))[-1]
            instance.data[bstack1ll1l11_opy_ (u"ࠤࡵࡥࡳࡱࠢᚴ")] = bstack1l1ll11l11l_opy_
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࡀࠦᚵ") + str(instance.data) + bstack1ll1l11_opy_ (u"ࠦࠧᚶ"))
        if not f.bstack11llll1l1ll_opy_(f.hub_url(driver)):
            self.bstack11llll11l1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111lll1ll_opy_.bstack1ll11l1ll_opy_(instance, self.bstack11lll1lll1l_opy_, True)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᚷ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠨࠢᚸ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111lll1ll_opy_.bstack1ll11l1ll_opy_(instance, self.bstack11lll1lll1l_opy_, True)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᚹ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠣࠤᚺ"))
    def __11lll1lll11_opy_(
        self,
        f: bstack1l1l111l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11llll11ll1_opy_(instance)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᚻ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠥࠦᚼ"))
    def bstack11llll1111l_opy_(self, context: bstack1l1ll11lll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll1111l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11lll1lllll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l1l111l1ll_opy_.bstack11lll1ll1ll_opy_(data[1])
                    and data[1].bstack11lll1lllll_opy_(context)
                    and getattr(data[0](), bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᚽ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll1l1lll_opy_, reverse=reverse)
    def bstack11llll11lll_opy_(self, context: bstack1l1ll11lll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll1111l1_opy_]]:
        matches = []
        for data in self.bstack11llll11l1l_opy_.values():
            if (
                data[1].bstack11lll1lllll_opy_(context)
                and getattr(data[0](), bstack1ll1l11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᚾ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll1l1lll_opy_, reverse=reverse)
    def bstack11llll111ll_opy_(self, instance: bstack1l1ll1111l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11llll11ll1_opy_(self, instance: bstack1l1ll1111l1_opy_) -> bool:
        if self.bstack11llll111ll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111lll1ll_opy_.bstack1ll11l1ll_opy_(instance, self.bstack11lll1lll1l_opy_, False)
            return True
        return False