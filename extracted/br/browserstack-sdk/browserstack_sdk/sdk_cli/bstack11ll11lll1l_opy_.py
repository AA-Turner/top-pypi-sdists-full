# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l1ll11l_opy_,
    bstack1l1l111l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1lll111ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11ll1l11111_opy_(bstack1l111111l1l_opy_):
    bstack11ll1l11ll1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1l1l111l1l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1l1l111l1l1_opy_]]
    def __init__(self, bstack11ll1l11ll1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11ll1l11l1l_opy_ = dict()
        self.bstack11ll1l11ll1_opy_ = bstack11ll1l11ll1_opy_
        self.frameworks = frameworks
        bstack11ll1lllll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.POST), self.__11ll1l111ll_opy_)
        if any(bstack1l11l11l11l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_(
                (bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.__11ll11ll1ll_opy_
            )
            bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_(
                (bstack11l1ll1l1_opy_.QUIT, bstack1lll1l11l1_opy_.POST), self.__11ll1l1111l_opy_
            )
    def __11ll1l111ll_opy_(
        self,
        f: bstack11ll1lllll_opy_,
        bstack11ll11lllll_opy_: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack111l_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣ᜽"):
                return
            contexts = bstack11ll11lllll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack111l_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧ᜾") in page.url:
                                self.logger.debug(bstack111l_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥ᜿"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, self.bstack11ll1l11ll1_opy_, True)
                                self.logger.debug(bstack111l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᝀ") + str(instance.ref()) + bstack111l_opy_ (u"ࠥࠦᝁ"))
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣᝂ"),e)
    def __11ll11ll1ll_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, self.bstack11ll1l11ll1_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l11llll111_opy_ = None
        if label:
            if bstack111l_opy_ (u"ࠧࠩࠢᝃ") in label:
                suffix = label.rsplit(bstack111l_opy_ (u"ࠨࠣࠣᝄ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l11llll111_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l11lll11ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࡴࡷࡩࡪ࡮ࡾࠠࠨࡽࡶࡹ࡫࡬ࡩࡹࡿࠪࠤ࡮ࡴࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡴࡵ࡮ࡧࡵ࡭ࡨࠦࡲࡢࡰ࡮࠲ࠧᝅ")
                    )
            else:
                self.logger.debug(
                    bstack1l11lll11ll_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳࠦࠧࠤࠩ࠾ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡲࡢࡰ࡮ࠤࡦࡹࡳࡪࡩࡱࡱࡪࡴࡴ࠯ࠤᝆ")
                )
        if bstack1l11llll111_opy_ is not None:
            bstack1l11llll111_opy_ = label.split(bstack111l_opy_ (u"ࠤࠦࠦᝇ"))[-1]
            instance.data[bstack111l_opy_ (u"ࠥࡶࡦࡴ࡫ࠣᝈ")] = bstack1l11llll111_opy_
        self.logger.debug(bstack111l_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡹ࡬ࡸ࡭ࠦࡤࡢࡶࡤࡁࠧᝉ") + str(instance.data) + bstack111l_opy_ (u"ࠧࠨᝊ"))
        if not f.bstack11ll1l1lll1_opy_(f.hub_url(driver)):
            self.bstack11ll1l11l1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, self.bstack11ll1l11ll1_opy_, True)
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᝋ") + str(instance.ref()) + bstack111l_opy_ (u"ࠢࠣᝌ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, self.bstack11ll1l11ll1_opy_, True)
        self.logger.debug(bstack111l_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᝍ") + str(instance.ref()) + bstack111l_opy_ (u"ࠤࠥᝎ"))
    def __11ll1l1111l_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11ll11ll1l1_opy_(instance)
        self.logger.debug(bstack111l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᝏ") + str(instance.ref()) + bstack111l_opy_ (u"ࠦࠧᝐ"))
    def bstack11ll1l11lll_opy_(self, context: bstack1l1lll111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1l111l1l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11ll11lll11_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l11l11l11l_opy_.bstack11ll1l11l11_opy_(data[1])
                    and data[1].bstack11ll11lll11_opy_(context)
                    and getattr(data[0](), bstack111l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᝑ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l11lll1l1l_opy_, reverse=reverse)
    def bstack11ll11llll1_opy_(self, context: bstack1l1lll111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1l1l111l1l1_opy_]]:
        matches = []
        for data in self.bstack11ll1l11l1l_opy_.values():
            if (
                data[1].bstack11ll11lll11_opy_(context)
                and getattr(data[0](), bstack111l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᝒ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l11lll1l1l_opy_, reverse=reverse)
    def bstack11ll1l111l1_opy_(self, instance: bstack1l1l111l1l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11ll11ll1l1_opy_(self, instance: bstack1l1l111l1l1_opy_) -> bool:
        if self.bstack11ll1l111l1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, self.bstack11ll1l11ll1_opy_, False)
            return True
        return False