# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack11ll11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11l1l1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11l1111ll_opy_(bstack1ll111l11ll_opy_):
    bstack1l111lll11l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll11ll1l11_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll11ll1l11_opy_]]
    def __init__(self, bstack1l111lll11l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l111llllll_opy_ = dict()
        self.bstack1l111lll11l_opy_ = bstack1l111lll11l_opy_
        self.frameworks = frameworks
        bstack111l111ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.POST), self.__1l111lll111_opy_)
        if any(bstack1ll111l1111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll111l1111_opy_.bstack1l11ll11111_opy_(
                (bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.__1l111lll1ll_opy_
            )
            bstack1ll111l1111_opy_.bstack1l11ll11111_opy_(
                (bstack11lll111_opy_.QUIT, bstack1l11l11l1_opy_.POST), self.__1l111ll1lll_opy_
            )
    def __1l111lll111_opy_(
        self,
        f: bstack111l111ll_opy_,
        bstack1l111llll1l_opy_: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1ll1lll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᕪ"):
                return
            contexts = bstack1l111llll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1ll1lll_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᕫ") in page.url:
                                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᕬ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, self.bstack1l111lll11l_opy_, True)
                                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡳࡥ࡬࡫࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᕭ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠧࠨᕮ"))
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࠼ࠥᕯ"),e)
    def __1l111lll1ll_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, self.bstack1l111lll11l_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll11ll11ll_opy_ = None
        if label:
            if bstack1ll1lll_opy_ (u"ࠢࠤࠤᕰ") in label:
                suffix = label.rsplit(bstack1ll1lll_opy_ (u"ࠣࠥࠥᕱ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll11ll11ll_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll11l1ll11_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࡶࡹ࡫࡬ࡩࡹࠢࠪࡿࡸࡻࡦࡧ࡫ࡻࢁࠬࠦࡩ࡯ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠ࡯ࡷࡰࡩࡷ࡯ࡣࠡࡴࡤࡲࡰ࠴ࠢᕲ")
                    )
            else:
                self.logger.debug(
                    bstack1ll11l1ll11_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࠡࠩࠦࠫࡀࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡴࡤࡲࡰࠦࡡࡴࡵ࡬࡫ࡳࡳࡥ࡯ࡶ࠱ࠦᕳ")
                )
        if bstack1ll11ll11ll_opy_ is not None:
            bstack1ll11ll11ll_opy_ = label.split(bstack1ll1lll_opy_ (u"ࠦࠨࠨᕴ"))[-1]
            instance.data[bstack1ll1lll_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᕵ")] = bstack1ll11ll11ll_opy_
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡻ࡮ࡺࡨࠡࡦࡤࡸࡦࡃࠢᕶ") + str(instance.data) + bstack1ll1lll_opy_ (u"ࠢࠣᕷ"))
        if not f.bstack1l11l11l1ll_opy_(f.hub_url(driver)):
            self.bstack1l111llllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, self.bstack1l111lll11l_opy_, True)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᕸ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠤࠥᕹ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, self.bstack1l111lll11l_opy_, True)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᕺ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠦࠧᕻ"))
    def __1l111ll1lll_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11l11111l_opy_(instance)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᕼ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠨࠢᕽ"))
    def bstack1l11l1111l1_opy_(self, context: bstack1ll11l1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll11ll1l11_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l111lllll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll111l1111_opy_.bstack1l111lll1l1_opy_(data[1])
                    and data[1].bstack1l111lllll1_opy_(context)
                    and getattr(data[0](), bstack1ll1lll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᕾ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11lll1l1_opy_, reverse=reverse)
    def bstack1l111llll11_opy_(self, context: bstack1ll11l1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll11ll1l11_opy_]]:
        matches = []
        for data in self.bstack1l111llllll_opy_.values():
            if (
                data[1].bstack1l111lllll1_opy_(context)
                and getattr(data[0](), bstack1ll1lll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᕿ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll11lll1l1_opy_, reverse=reverse)
    def bstack1l11l111111_opy_(self, instance: bstack1ll11ll1l11_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11ll1l11_opy_) -> bool:
        if self.bstack1l11l111111_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, self.bstack1l111lll11l_opy_, False)
            return True
        return False