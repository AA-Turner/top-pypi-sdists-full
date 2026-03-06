# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1lll11l1ll1_opy_,
    bstack1ll1ll1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1ll11l11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11ll1llll_opy_(bstack1ll111l1l1l_opy_):
    bstack1l11lll11ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1ll1l111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1ll1l111_opy_]]
    def __init__(self, bstack1l11lll11ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l11lll1l11_opy_ = dict()
        self.bstack1l11lll11ll_opy_ = bstack1l11lll11ll_opy_
        self.frameworks = frameworks
        bstack1lll11l11ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_.POST), self.__1l11lll111l_opy_)
        if any(bstack1ll11l11111_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_(
                (bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.__1l11ll1l11l_opy_
            )
            bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_(
                (bstack1ll1lll1ll1_opy_.QUIT, bstack1ll1l1lll1l_opy_.POST), self.__1l11ll1ll11_opy_
            )
    def __1l11lll111l_opy_(
        self,
        f: bstack1lll11l11ll_opy_,
        bstack1l11ll1l1ll_opy_: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1111_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᑾ"):
                return
            contexts = bstack1l11ll1l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1111_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᑿ") in page.url:
                                self.logger.debug(bstack1111_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᒀ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, self.bstack1l11lll11ll_opy_, True)
                                self.logger.debug(bstack1111_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᒁ") + str(instance.ref()) + bstack1111_opy_ (u"ࠢࠣᒂ"))
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧᒃ"),e)
    def __1l11ll1l11l_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, self.bstack1l11lll11ll_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1ll1l1l11ll_opy_ = None
        if label:
            if bstack1111_opy_ (u"ࠤࠦࠦᒄ") in label:
                suffix = label.rsplit(bstack1111_opy_ (u"ࠥࠧࠧᒅ"), 1)[-1]
                if suffix.isdigit():
                    bstack1ll1l1l11ll_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1ll1l1l11l1_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࡸࡻࡦࡧ࡫ࡻࠤࠬࢁࡳࡶࡨࡩ࡭ࡽࢃࠧࠡ࡫ࡱࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࡁࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡱࡹࡲ࡫ࡲࡪࡥࠣࡶࡦࡴ࡫࠯ࠤᒆ")
                    )
            else:
                self.logger.debug(
                    bstack1ll1l1l11l1_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࠬࢁ࡬ࡢࡤࡨࡰࢂ࠭ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡦࡳࡳࡺࡡࡪࡰࠣࠫࠨ࠭࠻ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡶࡦࡴ࡫ࠡࡣࡶࡷ࡮࡭࡮࡮ࡧࡱࡸ࠳ࠨᒇ")
                )
        if bstack1ll1l1l11ll_opy_ is not None:
            bstack1ll1l1l11ll_opy_ = label.split(bstack1111_opy_ (u"ࠨࠣࠣᒈ"))[-1]
            instance.data[bstack1111_opy_ (u"ࠢࡳࡣࡱ࡯ࠧᒉ")] = bstack1ll1l1l11ll_opy_
        self.logger.debug(bstack1111_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡ࠾ࠤᒊ") + str(instance.data) + bstack1111_opy_ (u"ࠤࠥᒋ"))
        if not f.bstack1l11llll11l_opy_(f.hub_url(driver)):
            self.bstack1l11lll1l11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, self.bstack1l11lll11ll_opy_, True)
            self.logger.debug(bstack1111_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒌ") + str(instance.ref()) + bstack1111_opy_ (u"ࠦࠧᒍ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, self.bstack1l11lll11ll_opy_, True)
        self.logger.debug(bstack1111_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᒎ") + str(instance.ref()) + bstack1111_opy_ (u"ࠨࠢᒏ"))
    def __1l11ll1ll11_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l11lll1111_opy_(instance)
        self.logger.debug(bstack1111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᒐ") + str(instance.ref()) + bstack1111_opy_ (u"ࠣࠤᒑ"))
    def bstack1l11ll1ll1l_opy_(self, context: bstack1ll1ll11l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1ll1l111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l11lll1l1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll11l11111_opy_.bstack1l11ll1lll1_opy_(data[1])
                    and data[1].bstack1l11lll1l1l_opy_(context)
                    and getattr(data[0](), bstack1111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᒒ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l1llll1_opy_, reverse=reverse)
    def bstack1l11lll11l1_opy_(self, context: bstack1ll1ll11l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1ll1l111_opy_]]:
        matches = []
        for data in self.bstack1l11lll1l11_opy_.values():
            if (
                data[1].bstack1l11lll1l1l_opy_(context)
                and getattr(data[0](), bstack1111_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᒓ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1l1llll1_opy_, reverse=reverse)
    def bstack1l11lll1ll1_opy_(self, instance: bstack1ll1ll1l111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l11lll1111_opy_(self, instance: bstack1ll1ll1l111_opy_) -> bool:
        if self.bstack1l11lll1ll1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, self.bstack1l11lll11ll_opy_, False)
            return True
        return False