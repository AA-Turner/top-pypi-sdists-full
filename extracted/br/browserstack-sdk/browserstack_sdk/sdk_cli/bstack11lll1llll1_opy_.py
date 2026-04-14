# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
    bstack111l1ll1ll_opy_,
    bstack1l1ll1lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11l1l1_opy_ import bstack1l11l1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack111l1ll11l_opy_ import bstack11ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1111_opy_ import bstack1l1ll111l11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11llll11l1l_opy_(bstack1l11ll1l11l_opy_):
    bstack11lll1ll111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1l1ll1lllll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1l1ll1lllll_opy_]]
    def __init__(self, bstack11lll1ll111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11lll1ll1ll_opy_ = dict()
        self.bstack11lll1ll111_opy_ = bstack11lll1ll111_opy_
        self.frameworks = frameworks
        bstack11ll1llll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_, bstack1ll1llll1l_opy_.POST), self.__11lll1ll1l1_opy_)
        if any(bstack1l11l1ll1l1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_(
                (bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.PRE), self.__11llll11111_opy_
            )
            bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_(
                (bstack1l1l11ll1l_opy_.QUIT, bstack1ll1llll1l_opy_.POST), self.__11llll11l11_opy_
            )
    def __11lll1ll1l1_opy_(
        self,
        f: bstack11ll1llll_opy_,
        bstack11lll1ll11l_opy_: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l111l_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᛂ"):
                return
            contexts = bstack11lll1ll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l111l_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᛃ") in page.url:
                                self.logger.debug(bstack1l111l_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᛄ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, self.bstack11lll1ll111_opy_, True)
                                self.logger.debug(bstack1l111l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᛅ") + str(instance.ref()) + bstack1l111l_opy_ (u"ࠨࠢᛆ"))
        except Exception as e:
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᛇ"),e)
    def __11llll11111_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack111l1ll1ll_opy_.bstack1ll111111ll_opy_(instance, self.bstack11lll1ll111_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l1ll1lll11_opy_ = None
        if label:
            if bstack1l111l_opy_ (u"ࠣࠥࠥᛈ") in label:
                suffix = label.rsplit(bstack1l111l_opy_ (u"ࠤࠦࠦᛉ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l1ll1lll11_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l1l1llll11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣᛊ")
                    )
            else:
                self.logger.debug(
                    bstack1l1l1llll11_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧᛋ")
                )
        if bstack1l1ll1lll11_opy_ is not None:
            bstack1l1ll1lll11_opy_ = label.split(bstack1l111l_opy_ (u"ࠧࠩࠢᛌ"))[-1]
            instance.data[bstack1l111l_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᛍ")] = bstack1l1ll1lll11_opy_
        self.logger.debug(bstack1l111l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧ࠽ࠣᛎ") + str(instance.data) + bstack1l111l_opy_ (u"ࠣࠤᛏ"))
        if not f.bstack11llll11ll1_opy_(f.hub_url(driver)):
            self.bstack11lll1ll1ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, self.bstack11lll1ll111_opy_, True)
            self.logger.debug(bstack1l111l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᛐ") + str(instance.ref()) + bstack1l111l_opy_ (u"ࠥࠦᛑ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, self.bstack11lll1ll111_opy_, True)
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᛒ") + str(instance.ref()) + bstack1l111l_opy_ (u"ࠧࠨᛓ"))
    def __11llll11l11_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11llll111ll_opy_(instance)
        self.logger.debug(bstack1l111l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᛔ") + str(instance.ref()) + bstack1l111l_opy_ (u"ࠢࠣᛕ"))
    def bstack11llll1111l_opy_(self, context: bstack1l1ll111l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll1lllll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11lll1lll1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l11l1ll1l1_opy_.bstack11lll1lllll_opy_(data[1])
                    and data[1].bstack11lll1lll1l_opy_(context)
                    and getattr(data[0](), bstack1l111l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᛖ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll11ll1l_opy_, reverse=reverse)
    def bstack11lll1lll11_opy_(self, context: bstack1l1ll111l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1ll1lllll_opy_]]:
        matches = []
        for data in self.bstack11lll1ll1ll_opy_.values():
            if (
                data[1].bstack11lll1lll1l_opy_(context)
                and getattr(data[0](), bstack1l111l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᛗ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l1ll11ll1l_opy_, reverse=reverse)
    def bstack11llll111l1_opy_(self, instance: bstack1l1ll1lllll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11llll111ll_opy_(self, instance: bstack1l1ll1lllll_opy_) -> bool:
        if self.bstack11llll111l1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack111l1ll1ll_opy_.bstack11111ll11l_opy_(instance, self.bstack11lll1ll111_opy_, False)
            return True
        return False