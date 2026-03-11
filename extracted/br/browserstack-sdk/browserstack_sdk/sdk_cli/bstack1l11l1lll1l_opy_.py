# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1lllllll_opy_,
    bstack1ll1l1l111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11llll1l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11l1llll1_opy_(bstack1ll11111l11_opy_):
    bstack1l11l1l1ll1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1l1l111l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1l1l111l_opy_]]
    def __init__(self, bstack1l11l1l1ll1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11l1lllll_opy_ = dict()
        self.bstack1l11l1l1ll1_opy_ = bstack1l11l1l1ll1_opy_
        self.frameworks = frameworks
        bstack1lll111l1l1_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_, bstack1ll1l11ll1l_opy_.POST), self.__1l11ll1111l_opy_)
        if any(bstack1ll11lll111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll11lll111_opy_.bstack1l1l1111111_opy_(
                (bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.__1l11l1ll1l1_opy_
            )
            bstack1ll11lll111_opy_.bstack1l1l1111111_opy_(
                (bstack1ll1l1l11l1_opy_.QUIT, bstack1ll1l11ll1l_opy_.POST), self.__1l11ll111l1_opy_
            )
    def __1l11ll1111l_opy_(
        self,
        f: bstack1lll111l1l1_opy_,
        bstack1l11l1ll11l_opy_: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll111_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᓦ"):
                return
            contexts = bstack1l11l1ll11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll111_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᓧ") in page.url:
                                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᓨ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, self.bstack1l11l1l1ll1_opy_, True)
                                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᓩ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠨࠢᓪ"))
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᓫ"),e)
    def __1l11l1ll1l1_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, self.bstack1l11l1l1ll1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll1l11111l_opy_ = None
        if label:
            if bstack1ll111_opy_ (u"ࠣࠥࠥᓬ") in label:
                suffix = label.rsplit(bstack1ll111_opy_ (u"ࠤࠦࠦᓭ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll1l11111l_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll1l11llll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣᓮ")
                    )
            else:
                self.logger.debug(
                    bstack1ll1l11llll_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧᓯ")
                )
        if bstack1ll1l11111l_opy_ is not None:
            bstack1ll1l11111l_opy_ = label.split(bstack1ll111_opy_ (u"ࠧࠩࠢᓰ"))[-1]
            instance.data[bstack1ll111_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᓱ")] = bstack1ll1l11111l_opy_
        self.logger.debug(bstack1ll111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧ࠽ࠣᓲ") + str(instance.data) + bstack1ll111_opy_ (u"ࠣࠤᓳ"))
        if not f.bstack1l11ll1l1l1_opy_(f.hub_url(driver)):
            self.bstack1l11l1lllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, self.bstack1l11l1l1ll1_opy_, True)
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᓴ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠥࠦᓵ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, self.bstack1l11l1l1ll1_opy_, True)
        self.logger.debug(bstack1ll111_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᓶ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠧࠨᓷ"))
    def __1l11ll111l1_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11ll11111_opy_(instance)
        self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᓸ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠢࠣᓹ"))
    def bstack1l11l1ll1ll_opy_(self, context: bstack1ll11llll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1l111l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11l1l1l1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll11lll111_opy_.bstack1l11l1l1lll_opy_(data[1])
                    and data[1].bstack1l11l1l1l1l_opy_(context)
                    and getattr(data[0](), bstack1ll111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᓺ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l1l1ll1_opy_, reverse=reverse)
    def bstack1l11l1ll111_opy_(self, context: bstack1ll11llll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1l1l111l_opy_]]:
        matches = []
        for data in self.bstack1l11l1lllll_opy_.values():
            if (
                data[1].bstack1l11l1l1l1l_opy_(context)
                and getattr(data[0](), bstack1ll111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᓻ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l1l1ll1_opy_, reverse=reverse)
    def bstack1l11l1lll11_opy_(self, instance: bstack1ll1l1l111l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11ll11111_opy_(self, instance: bstack1ll1l1l111l_opy_) -> bool:
        if self.bstack1l11l1lll11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, self.bstack1l11l1l1ll1_opy_, False)
            return True
        return False