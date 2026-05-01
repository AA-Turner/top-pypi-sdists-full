# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack11l1l1l1_opy_,
    bstack1l1ll111lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1lll_opy_ import bstack1l1ll1111l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11lll1ll111_opy_(bstack1l11l1l11ll_opy_):
    bstack11lll1llll1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1l1ll111lll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1l1ll111lll_opy_]]
    def __init__(self, bstack11lll1llll1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11lll1lll1l_opy_ = dict()
        self.bstack11lll1llll1_opy_ = bstack11lll1llll1_opy_
        self.frameworks = frameworks
        bstack11ll1l1ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.POST), self.__11lll1l11ll_opy_)
        if any(bstack1l11lll111l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l11lll111l_opy_.bstack1l111l1111l_opy_(
                (bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.__11lll1l1l1l_opy_
            )
            bstack1l11lll111l_opy_.bstack1l111l1111l_opy_(
                (bstack1ll1l1111l_opy_.QUIT, bstack1l1l111lll_opy_.POST), self.__11llll11111_opy_
            )
    def __11lll1l11ll_opy_(
        self,
        f: bstack11ll1l1ll_opy_,
        bstack11lll1lll11_opy_: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack111ll_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢᛓ"):
                return
            contexts = bstack11lll1lll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111ll_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᛔ") in page.url:
                                self.logger.debug(bstack111ll_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᛕ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, self.bstack11lll1llll1_opy_, True)
                                self.logger.debug(bstack111ll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᛖ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠤࠥᛗ"))
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢᛘ"),e)
    def __11lll1l1l1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, self.bstack11lll1llll1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l1ll1l11l1_opy_ = None
        if label:
            if bstack111ll_opy_ (u"ࠦࠨࠨᛙ") in label:
                suffix = label.rsplit(bstack111ll_opy_ (u"ࠧࠩࠢᛚ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l1ll1l11l1_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l1ll1l1111_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᛛ")
                    )
            else:
                self.logger.debug(
                    bstack1l1ll1l1111_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᛜ")
                )
        if bstack1l1ll1l11l1_opy_ is not None:
            bstack1l1ll1l11l1_opy_ = label.split(bstack111ll_opy_ (u"ࠣࠥࠥᛝ"))[-1]
            instance.data[bstack111ll_opy_ (u"ࠤࡵࡥࡳࡱࠢᛞ")] = bstack1l1ll1l11l1_opy_
        self.logger.debug(bstack111ll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࡀࠦᛟ") + str(instance.data) + bstack111ll_opy_ (u"ࠦࠧᛠ"))
        if not f.bstack11llll11ll1_opy_(f.hub_url(driver)):
            self.bstack11lll1lll1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, self.bstack11lll1llll1_opy_, True)
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᛡ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠨࠢᛢ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, self.bstack11lll1llll1_opy_, True)
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᛣ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠣࠤᛤ"))
    def __11llll11111_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11lll1l1lll_opy_(instance)
        self.logger.debug(bstack111ll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᛥ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠥࠦᛦ"))
    def bstack11lll1ll1ll_opy_(self, context: bstack1l1ll1111l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll111lll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11lll1l1l11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l11lll111l_opy_.bstack11lll1ll11l_opy_(data[1])
                    and data[1].bstack11lll1l1l11_opy_(context)
                    and getattr(data[0](), bstack111ll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᛧ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll1111ll_opy_, reverse=reverse)
    def bstack11lll1ll1l1_opy_(self, context: bstack1l1ll1111l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll111lll_opy_]]:
        matches = []
        for data in self.bstack11lll1lll1l_opy_.values():
            if (
                data[1].bstack11lll1l1l11_opy_(context)
                and getattr(data[0](), bstack111ll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᛨ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll1111ll_opy_, reverse=reverse)
    def bstack11lll1l1ll1_opy_(self, instance: bstack1l1ll111lll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11lll1l1lll_opy_(self, instance: bstack1l1ll111lll_opy_) -> bool:
        if self.bstack11lll1l1ll1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, self.bstack11lll1llll1_opy_, False)
            return True
        return False