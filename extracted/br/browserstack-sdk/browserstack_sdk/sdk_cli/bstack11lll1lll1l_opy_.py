# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack11l1l1ll11_opy_,
    bstack1l1ll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack111l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1ll1ll11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11llll111ll_opy_(bstack1l1l1111111_opy_):
    bstack11llll111l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1l1ll11l1ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1l1ll11l1ll_opy_]]
    def __init__(self, bstack11llll111l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11lll1l1lll_opy_ = dict()
        self.bstack11llll111l1_opy_ = bstack11llll111l1_opy_
        self.frameworks = frameworks
        bstack111l1l11l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.POST), self.__11llll1111l_opy_)
        if any(bstack1l1l111l111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l1l111l111_opy_.bstack1l1111lllll_opy_(
                (bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.__11lll1llll1_opy_
            )
            bstack1l1l111l111_opy_.bstack1l1111lllll_opy_(
                (bstack1lll11l1l1_opy_.QUIT, bstack1111llll1l_opy_.POST), self.__11lll1ll11l_opy_
            )
    def __11llll1111l_opy_(
        self,
        f: bstack111l1l11l_opy_,
        bstack11lll1ll1ll_opy_: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1111l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᛄ"):
                return
            contexts = bstack11lll1ll1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1111l_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᛅ") in page.url:
                                self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᛆ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, self.bstack11llll111l1_opy_, True)
                                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᛇ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠣࠤᛈ"))
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨᛉ"),e)
    def __11lll1llll1_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, self.bstack11llll111l1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l1ll11l111_opy_ = None
        if label:
            if bstack1l1111l_opy_ (u"ࠥࠧࠧᛊ") in label:
                suffix = label.rsplit(bstack1l1111l_opy_ (u"ࠦࠨࠨᛋ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l1ll11l111_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l1ll1l11l1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡤࡳ࡫ࡹࡩࡷࠦ࡬ࡢࡤࡨࡰࠥࡹࡵࡧࡨ࡬ࡼࠥ࠭ࡻࡴࡷࡩࡪ࡮ࡾࡽࠨࠢ࡬ࡲࠥࡲࡡࡣࡧ࡯ࠤࠬࢁ࡬ࡢࡤࡨࡰࢂ࠭࠻ࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡲࡺࡳࡥࡳ࡫ࡦࠤࡷࡧ࡮࡬࠰ࠥᛌ")
                    )
            else:
                self.logger.debug(
                    bstack1l1ll1l11l1_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡧࡴࡴࡴࡢ࡫ࡱࠤࠬࠩࠧ࠼ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡷࡧ࡮࡬ࠢࡤࡷࡸ࡯ࡧ࡯࡯ࡨࡲࡹ࠴ࠢᛍ")
                )
        if bstack1l1ll11l111_opy_ is not None:
            bstack1l1ll11l111_opy_ = label.split(bstack1l1111l_opy_ (u"ࠢࠤࠤᛎ"))[-1]
            instance.data[bstack1l1111l_opy_ (u"ࠣࡴࡤࡲࡰࠨᛏ")] = bstack1l1ll11l111_opy_
        self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢ࠿ࠥᛐ") + str(instance.data) + bstack1l1111l_opy_ (u"ࠥࠦᛑ"))
        if not f.bstack11llll1lll1_opy_(f.hub_url(driver)):
            self.bstack11lll1l1lll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, self.bstack11llll111l1_opy_, True)
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᛒ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠧࠨᛓ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, self.bstack11llll111l1_opy_, True)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᛔ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠢࠣᛕ"))
    def __11lll1ll11l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11lll1lllll_opy_(instance)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡳࡸ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᛖ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠤࠥᛗ"))
    def bstack11lll1ll111_opy_(self, context: bstack1l1ll1ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll11l1ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11lll1ll1l1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l1l111l111_opy_.bstack11lll1l1ll1_opy_(data[1])
                    and data[1].bstack11lll1ll1l1_opy_(context)
                    and getattr(data[0](), bstack1l1111l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᛘ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1lll11111_opy_, reverse=reverse)
    def bstack11llll11111_opy_(self, context: bstack1l1ll1ll11l_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll11l1ll_opy_]]:
        matches = []
        for data in self.bstack11lll1l1lll_opy_.values():
            if (
                data[1].bstack11lll1ll1l1_opy_(context)
                and getattr(data[0](), bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᛙ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1lll11111_opy_, reverse=reverse)
    def bstack11lll1lll11_opy_(self, instance: bstack1l1ll11l1ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11lll1lllll_opy_(self, instance: bstack1l1ll11l1ll_opy_) -> bool:
        if self.bstack11lll1lll11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, self.bstack11llll111l1_opy_, False)
            return True
        return False