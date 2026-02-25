# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1ll1llll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1lllll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1lll11l1l11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack1l11lllllll_opy_(bstack1ll11llll11_opy_):
    bstack1l1l1111111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1ll1llll111_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1ll1llll111_opy_]]
    def __init__(self, bstack1l1l1111111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1l111l111_opy_ = dict()
        self.bstack1l1l1111111_opy_ = bstack1l1l1111111_opy_
        self.frameworks = frameworks
        bstack1l1lllll1ll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_, bstack1lll11l111l_opy_.POST), self.__1l1l111l1l1_opy_)
        if any(bstack1l1lllll1l1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_(
                (bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.__1l1l1111ll1_opy_
            )
            bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_(
                (bstack1ll1lll1lll_opy_.QUIT, bstack1lll11l111l_opy_.POST), self.__1l1l111ll11_opy_
            )
    def __1l1l111l1l1_opy_(
        self,
        f: bstack1l1lllll1ll_opy_,
        bstack1l1l11111ll_opy_: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11l1l11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᏲ"):
                return
            contexts = bstack1l1l11111ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11l1l11_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᏳ") in page.url:
                                self.logger.debug(bstack11l1l11_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᏴ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, self.bstack1l1l1111111_opy_, True)
                                self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏵ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠢࠣ᏶"))
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧ᏷"),e)
    def __1l1l1111ll1_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, self.bstack1l1l1111111_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1lll1111l11_opy_ = None
        if label:
            if bstack11l1l11_opy_ (u"ࠤࠦࠦᏸ") in label:
                suffix = label.rsplit(bstack11l1l11_opy_ (u"ࠥࠧࠧᏹ"), 1)[-1]
                if suffix.isdigit():
                    bstack1lll1111l11_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1lll11l11ll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࡸࡻࡦࡧ࡫ࡻࠤࠬࢁࡳࡶࡨࡩ࡭ࡽࢃࠧࠡ࡫ࡱࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࡁࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡱࡹࡲ࡫ࡲࡪࡥࠣࡶࡦࡴ࡫࠯ࠤᏺ")
                    )
            else:
                self.logger.debug(
                    bstack1lll11l11ll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࠬࢁ࡬ࡢࡤࡨࡰࢂ࠭ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡦࡳࡳࡺࡡࡪࡰࠣࠫࠨ࠭࠻ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡶࡦࡴ࡫ࠡࡣࡶࡷ࡮࡭࡮࡮ࡧࡱࡸ࠳ࠨᏻ")
                )
        if bstack1lll1111l11_opy_ is not None:
            bstack1lll1111l11_opy_ = label.split(bstack11l1l11_opy_ (u"ࠨࠣࠣᏼ"))[-1]
            instance.data[bstack11l1l11_opy_ (u"ࠢࡳࡣࡱ࡯ࠧᏽ")] = bstack1lll1111l11_opy_
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡ࠾ࠤ᏾") + str(instance.data) + bstack11l1l11_opy_ (u"ࠤࠥ᏿"))
        if not f.bstack1l1l11l11l1_opy_(f.hub_url(driver)):
            self.bstack1l1l111l111_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, self.bstack1l1l1111111_opy_, True)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᐀") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠦࠧᐁ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, self.bstack1l1l1111111_opy_, True)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᐂ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠨࠢᐃ"))
    def __1l1l111ll11_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1l111l1ll_opy_(instance)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᐄ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠣࠤᐅ"))
    def bstack1l1l1111lll_opy_(self, context: bstack1lll11l1l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1llll111_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1l111111l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1l1lllll1l1_opy_.bstack1l1l1111l11_opy_(data[1])
                    and data[1].bstack1l1l111111l_opy_(context)
                    and getattr(data[0](), bstack11l1l11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᐆ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1ll1_opy_, reverse=reverse)
    def bstack1l1l11111l1_opy_(self, context: bstack1lll11l1l11_opy_, reverse=True) -> List[Tuple[Callable, bstack1ll1llll111_opy_]]:
        matches = []
        for data in self.bstack1l1l111l111_opy_.values():
            if (
                data[1].bstack1l1l111111l_opy_(context)
                and getattr(data[0](), bstack11l1l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᐇ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1ll1lll1ll1_opy_, reverse=reverse)
    def bstack1l1l1111l1l_opy_(self, instance: bstack1ll1llll111_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1l111l1ll_opy_(self, instance: bstack1ll1llll111_opy_) -> bool:
        if self.bstack1l1l1111l1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, self.bstack1l1l1111111_opy_, False)
            return True
        return False