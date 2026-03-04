# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1lll1111l11_opy_,
    bstack1ll1llll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll11lll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11lll1111_opy_(bstack1ll11l1ll11_opy_):
    bstack1l11lll1ll1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1llll11l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1llll11l_opy_]]
    def __init__(self, bstack1l11lll1ll1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11ll1ll1l_opy_ = dict()
        self.bstack1l11lll1ll1_opy_ = bstack1l11lll1ll1_opy_
        self.frameworks = frameworks
        bstack1lll111l1ll_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_, bstack1ll1llll111_opy_.POST), self.__1l11lll11l1_opy_)
        if any(bstack1ll11l11l11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_(
                (bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.__1l11llll111_opy_
            )
            bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_(
                (bstack1ll1l1l11ll_opy_.QUIT, bstack1ll1llll111_opy_.POST), self.__1l11ll1llll_opy_
            )
    def __1l11lll11l1_opy_(
        self,
        f: bstack1lll111l1ll_opy_,
        bstack1l11ll1ll11_opy_: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1lll1l_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᑽ"):
                return
            contexts = bstack1l11ll1ll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1lll1l_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᑾ") in page.url:
                                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᑿ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, self.bstack1l11lll1ll1_opy_, True)
                                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᒀ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠨࠢᒁ"))
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᒂ"),e)
    def __1l11llll111_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, self.bstack1l11lll1ll1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll1l1l1lll_opy_ = None
        if label:
            if bstack1lll1l_opy_ (u"ࠣࠥࠥᒃ") in label:
                suffix = label.rsplit(bstack1lll1l_opy_ (u"ࠤࠦࠦᒄ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll1l1l1lll_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll1l1ll11l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣᒅ")
                    )
            else:
                self.logger.debug(
                    bstack1ll1l1ll11l_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧᒆ")
                )
        if bstack1ll1l1l1lll_opy_ is not None:
            bstack1ll1l1l1lll_opy_ = label.split(bstack1lll1l_opy_ (u"ࠧࠩࠢᒇ"))[-1]
            instance.data[bstack1lll1l_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᒈ")] = bstack1ll1l1l1lll_opy_
        self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧ࠽ࠣᒉ") + str(instance.data) + bstack1lll1l_opy_ (u"ࠣࠤᒊ"))
        if not f.bstack1l1l111111l_opy_(f.hub_url(driver)):
            self.bstack1l11ll1ll1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, self.bstack1l11lll1ll1_opy_, True)
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᒋ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠥࠦᒌ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, self.bstack1l11lll1ll1_opy_, True)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᒍ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠧࠨᒎ"))
    def __1l11ll1llll_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11lll1l1l_opy_(instance)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒏ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠢࠣᒐ"))
    def bstack1l11ll1l1ll_opy_(self, context: bstack1ll1ll11lll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1llll11l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11lll1l11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll11l11l11_opy_.bstack1l11lll111l_opy_(data[1])
                    and data[1].bstack1l11lll1l11_opy_(context)
                    and getattr(data[0](), bstack1lll1l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᒑ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1111_opy_, reverse=reverse)
    def bstack1l11lll11ll_opy_(self, context: bstack1ll1ll11lll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1llll11l_opy_]]:
        matches = []
        for data in self.bstack1l11ll1ll1l_opy_.values():
            if (
                data[1].bstack1l11lll1l11_opy_(context)
                and getattr(data[0](), bstack1lll1l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᒒ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1111_opy_, reverse=reverse)
    def bstack1l11ll1lll1_opy_(self, instance: bstack1ll1llll11l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11lll1l1l_opy_(self, instance: bstack1ll1llll11l_opy_) -> bool:
        if self.bstack1l11ll1lll1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, self.bstack1l11lll1ll1_opy_, False)
            return True
        return False