# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1l1lll1111_opy_,
    bstack1ll11llllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11lll1ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11l111111_opy_(bstack1l1lllllll1_opy_):
    bstack1l11l1111ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll11llllll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll11llllll_opy_]]
    def __init__(self, bstack1l11l1111ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l111llllll_opy_ = dict()
        self.bstack1l11l1111ll_opy_ = bstack1l11l1111ll_opy_
        self.frameworks = frameworks
        bstack1l1l11ll1l_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.POST), self.__1l11l11l1l1_opy_)
        if any(bstack1ll111l11ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_(
                (bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.__1l11l1111l1_opy_
            )
            bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_(
                (bstack111ll1lll1_opy_.QUIT, bstack11lllll11l_opy_.POST), self.__1l11l11111l_opy_
            )
    def __1l11l11l1l1_opy_(
        self,
        f: bstack1l1l11ll1l_opy_,
        bstack1l11l111lll_opy_: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11lll1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦᕖ"):
                return
            contexts = bstack1l11l111lll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11lll1_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣᕗ") in page.url:
                                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᕘ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, self.bstack1l11l1111ll_opy_, True)
                                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᕙ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠨࠢᕚ"))
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦᕛ"),e)
    def __1l11l1111l1_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, self.bstack1l11l1111ll_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll11l11ll1_opy_ = None
        if label:
            if bstack11lll1_opy_ (u"ࠣࠥࠥᕜ") in label:
                suffix = label.rsplit(bstack11lll1_opy_ (u"ࠤࠦࠦᕝ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll11l11ll1_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll11ll1ll1_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣᕞ")
                    )
            else:
                self.logger.debug(
                    bstack1ll11ll1ll1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧᕟ")
                )
        if bstack1ll11l11ll1_opy_ is not None:
            bstack1ll11l11ll1_opy_ = label.split(bstack11lll1_opy_ (u"ࠧࠩࠢᕠ"))[-1]
            instance.data[bstack11lll1_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᕡ")] = bstack1ll11l11ll1_opy_
        self.logger.debug(bstack11lll1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡼ࡯ࡴࡩࠢࡧࡥࡹࡧ࠽ࠣᕢ") + str(instance.data) + bstack11lll1_opy_ (u"ࠣࠤᕣ"))
        if not f.bstack1l11l11ll1l_opy_(f.hub_url(driver)):
            self.bstack1l111llllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, self.bstack1l11l1111ll_opy_, True)
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᕤ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠥࠦᕥ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, self.bstack1l11l1111ll_opy_, True)
        self.logger.debug(bstack11lll1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᕦ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠧࠨᕧ"))
    def __1l11l11111l_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11l11l11l_opy_(instance)
        self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᕨ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠢࠣᕩ"))
    def bstack1l11l111l11_opy_(self, context: bstack1ll11lll1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll11llllll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11l111ll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll111l11ll_opy_.bstack1l11l111l1l_opy_(data[1])
                    and data[1].bstack1l11l111ll1_opy_(context)
                    and getattr(data[0](), bstack11lll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᕪ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l111l1l_opy_, reverse=reverse)
    def bstack1l11l11l1ll_opy_(self, context: bstack1ll11lll1ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll11llllll_opy_]]:
        matches = []
        for data in self.bstack1l111llllll_opy_.values():
            if (
                data[1].bstack1l11l111ll1_opy_(context)
                and getattr(data[0](), bstack11lll1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᕫ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l111l1l_opy_, reverse=reverse)
    def bstack1l11l11l111_opy_(self, instance: bstack1ll11llllll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11l11l11l_opy_(self, instance: bstack1ll11llllll_opy_) -> bool:
        if self.bstack1l11l11l111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, self.bstack1l11l1111ll_opy_, False)
            return True
        return False