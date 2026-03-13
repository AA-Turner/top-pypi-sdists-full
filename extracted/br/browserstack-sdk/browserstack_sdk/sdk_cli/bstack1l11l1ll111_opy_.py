# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1l1lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll11lll1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11l1l1l1l_opy_(bstack1ll1111l1ll_opy_):
    bstack1l11l1ll1ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1l1lll1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1l1lll1l_opy_]]
    def __init__(self, bstack1l11l1ll1ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11l1l1l11_opy_ = dict()
        self.bstack1l11l1ll1ll_opy_ = bstack1l11l1ll1ll_opy_
        self.frameworks = frameworks
        bstack1ll1llllll1_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll1ll1111l_opy_.POST), self.__1l11l1ll1l1_opy_)
        if any(bstack1ll111ll1ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_(
                (bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.__1l11ll1111l_opy_
            )
            bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_(
                (bstack1ll1l1l1lll_opy_.QUIT, bstack1ll1ll1111l_opy_.POST), self.__1l11l1ll11l_opy_
            )
    def __1l11l1ll1l1_opy_(
        self,
        f: bstack1ll1llllll1_opy_,
        bstack1l11l1llll1_opy_: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1111l_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᔡ"):
                return
            contexts = bstack1l11l1llll1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111l_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᔢ") in page.url:
                                self.logger.debug(bstack1111l_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᔣ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, self.bstack1l11l1ll1ll_opy_, True)
                                self.logger.debug(bstack1111l_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᔤ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠤࠥᔥ"))
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢᔦ"),e)
    def __1l11ll1111l_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, self.bstack1l11l1ll1ll_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll11lll11l_opy_ = None
        if label:
            if bstack1111l_opy_ (u"ࠦࠨࠨᔧ") in label:
                suffix = label.rsplit(bstack1111l_opy_ (u"ࠧࠩࠢᔨ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll11lll11l_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll1l11l1ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᔩ")
                    )
            else:
                self.logger.debug(
                    bstack1ll1l11l1ll_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᔪ")
                )
        if bstack1ll11lll11l_opy_ is not None:
            bstack1ll11lll11l_opy_ = label.split(bstack1111l_opy_ (u"ࠣࠥࠥᔫ"))[-1]
            instance.data[bstack1111l_opy_ (u"ࠤࡵࡥࡳࡱࠢᔬ")] = bstack1ll11lll11l_opy_
        self.logger.debug(bstack1111l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࡀࠦᔭ") + str(instance.data) + bstack1111l_opy_ (u"ࠦࠧᔮ"))
        if not f.bstack1l11ll1l1l1_opy_(f.hub_url(driver)):
            self.bstack1l11l1l1l11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, self.bstack1l11l1ll1ll_opy_, True)
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᔯ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠨࠢᔰ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, self.bstack1l11l1ll1ll_opy_, True)
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᔱ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠣࠤᔲ"))
    def __1l11l1ll11l_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11l1l1ll1_opy_(instance)
        self.logger.debug(bstack1111l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᔳ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠥࠦᔴ"))
    def bstack1l11ll11111_opy_(self, context: bstack1ll11lll1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1lll1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11l1lllll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll111ll1ll_opy_.bstack1l11l1l1lll_opy_(data[1])
                    and data[1].bstack1l11l1lllll_opy_(context)
                    and getattr(data[0](), bstack1111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᔵ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11llllll_opy_, reverse=reverse)
    def bstack1l11l1lll11_opy_(self, context: bstack1ll11lll1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1lll1l_opy_]]:
        matches = []
        for data in self.bstack1l11l1l1l11_opy_.values():
            if (
                data[1].bstack1l11l1lllll_opy_(context)
                and getattr(data[0](), bstack1111l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᔶ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11llllll_opy_, reverse=reverse)
    def bstack1l11l1lll1l_opy_(self, instance: bstack1ll1l1lll1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11l1l1ll1_opy_(self, instance: bstack1ll1l1lll1l_opy_) -> bool:
        if self.bstack1l11l1lll1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, self.bstack1l11l1ll1ll_opy_, False)
            return True
        return False