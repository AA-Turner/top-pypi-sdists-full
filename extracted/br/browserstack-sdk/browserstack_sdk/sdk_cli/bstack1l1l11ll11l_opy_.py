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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack1l1ll11l1ll_opy_,
    bstack1l1ll1ll11l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lllllll11l_opy_, bstack11111l111l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l11l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack111l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lll1l_opy_ import bstack11llll111ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1111ll11_opy_ import bstack1l11111l11_opy_, bstack11ll1l1111_opy_, bstack1l1llll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1l11ll1l1_opy_(bstack11llll111ll_opy_):
    bstack11l1l1ll111_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥឤ")
    bstack11ll1lllll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦឥ")
    bstack11ll1lll11l_opy_ = bstack1l1111l_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣឦ")
    bstack11l1l1ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢឧ")
    bstack11l1l1l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧឨ")
    bstack11ll1l1lll1_opy_ = bstack1l1111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣឩ")
    bstack11l1l1lll1l_opy_ = bstack1l1111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨឪ")
    bstack11l1l1ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤឫ")
    def __init__(self):
        super().__init__(bstack11llll111l1_opy_=self.bstack11l1l1ll111_opy_, frameworks=[bstack1l1l111l111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l1ll111ll_opy_)
        if bstack11111l111l_opy_():
            TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111111ll_opy_)
        else:
            TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111111ll_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1ll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1l1lllll_opy_ = self.bstack11l1l1l1ll1_opy_(instance.context)
        if not bstack11l1l1lllll_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥឬ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠨࠢឭ"))
            return
        f.bstack111l1llll1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1lllll1_opy_, bstack11l1l1lllll_opy_)
    def bstack11l1l1l1ll1_opy_(self, context: bstack1l1ll1ll11l_opy_, bstack11l1ll11lll_opy_= True):
        if bstack11l1ll11lll_opy_:
            bstack11l1l1lllll_opy_ = self.bstack11lll1ll111_opy_(context, reverse=True)
        else:
            bstack11l1l1lllll_opy_ = self.bstack11llll11111_opy_(context, reverse=True)
        return [f for f in bstack11l1l1lllll_opy_ if f[1].state != bstack1lll11l1l1_opy_.QUIT]
    def bstack1l1111111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll111ll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if not bstack1lllllll11l_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥឮ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠣࠤឯ"))
            return
        bstack11l1l1lllll_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack11l1l1lllll_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧឰ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠥࠦឱ"))
            return
        if len(bstack11l1l1lllll_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l11l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨឲ"))
        bstack11l1ll11l11_opy_, bstack11ll1111111_opy_ = bstack11l1l1lllll_opy_[0]
        page = bstack11l1ll11l11_opy_()
        if not page:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧឳ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢ឴"))
            return
        bstack1l111l111_opy_ = getattr(args[0], bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ឵"), None) or getattr(args[0], bstack1l1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨា"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢិ")).get(bstack1l1111l_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧី")):
            try:
                page.evaluate(bstack1l1111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧឹ"),
                            bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩឺ") + json.dumps(
                                bstack1l111l111_opy_) + bstack1l1111l_opy_ (u"ࠨࡽࡾࠤុ"))
            except Exception as e:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧូ"), e)
    def bstack1l1111ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll111ll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if not bstack1lllllll11l_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦួ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠤࠥើ"))
            return
        bstack11l1l1lllll_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack11l1l1lllll_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨឿ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠦࠧៀ"))
            return
        if len(bstack11l1l1lllll_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l11l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢេ"))
        bstack11l1ll11l11_opy_, bstack11ll1111111_opy_ = bstack11l1l1lllll_opy_[0]
        page = bstack11l1ll11l11_opy_()
        if not page:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨែ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠢࠣៃ"))
            return
        status = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l1ll1111l_opy_, None)
        if not status:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦោ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠤࠥៅ"))
            return
        bstack11l1ll11ll1_opy_ = {bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥំ"): status.lower()}
        bstack11l1ll111l1_opy_ = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_, None)
        if status.lower() == bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫះ") and bstack11l1ll111l1_opy_ is not None:
            bstack11l1ll11ll1_opy_[bstack1l1111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬៈ")] = bstack11l1ll111l1_opy_[0][bstack1l1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ៉")][0] if isinstance(bstack11l1ll111l1_opy_, list) else str(bstack11l1ll111l1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧ៊")).get(bstack1l1111l_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ់")):
            try:
                page.evaluate(
                        bstack1l1111l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ៌"),
                        bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨ៍")
                        + json.dumps(bstack11l1ll11ll1_opy_)
                        + bstack1l1111l_opy_ (u"ࠦࢂࠨ៎")
                    )
            except Exception as e:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧ៏"), e)
    def bstack11ll11l1ll1_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        f: TestFramework,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll111ll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if not bstack1lllllll11l_opy_:
            self.logger.debug(
                bstack1l1ll1l11l1_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢ័"))
            return
        bstack11l1l1lllll_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack11l1l1lllll_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ៑") + str(kwargs) + bstack1l1111l_opy_ (u"ࠣࠤ្"))
            return
        if len(bstack11l1l1lllll_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l11l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦ៓"))
        bstack11l1ll11l11_opy_, bstack11ll1111111_opy_ = bstack11l1l1lllll_opy_[0]
        page = bstack11l1ll11l11_opy_()
        if not page:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ។") + str(kwargs) + bstack1l1111l_opy_ (u"ࠦࠧ៕"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1111l_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥ៖") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢៗ"),
                bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ៘").format(
                    json.dumps(
                        {
                            bstack1l1111l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ៙"): bstack1l1111l_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ៚"),
                            bstack1l1111l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ៛"): {
                                bstack1l1111l_opy_ (u"ࠦࡹࡿࡰࡦࠤៜ"): bstack1l1111l_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤ៝"),
                                bstack1l1111l_opy_ (u"ࠨࡤࡢࡶࡤࠦ៞"): data,
                                bstack1l1111l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ៟"): bstack1l1111l_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢ០")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦ១"), e)
    def bstack11ll1l1l111_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        f: TestFramework,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll111ll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1l1lll1_opy_, False):
            return
        self.bstack1l1111l1ll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1l1111l_opy_ (u"ࠥࠦ២"))
        req.platform_index = int(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_, 0) or 0)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ៣").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l11111l11l_opy_, bstack1l1111l_opy_ (u"ࠧࠨ៤")) or bstack1l1111l_opy_ (u"ࠨࠢ៥"))
        req.test_framework_version = str(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11ll11l1lll_opy_, bstack1l1111l_opy_ (u"ࠢࠣ៦")) or bstack1l1111l_opy_ (u"ࠣࠤ៧"))
        req.test_framework_state = str(bstack1l1ll1ll111_opy_[0].name)
        req.test_hook_state = str(bstack1l1ll1ll111_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_, bstack1l1111l_opy_ (u"ࠤࠥ៨")) or bstack1l1111l_opy_ (u"ࠥࠦ៩"))
        current_test_id = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l1ll11111_opy_, None)
        bstack11l1ll1l111_opy_ = 0
        bstack11l1ll11l1l_opy_ = 0
        for bstack11l1l1l1lll_opy_ in bstack111l1l11l_opy_.bstack1lllll1ll1_opy_.values():
            session_id = bstack111l1l11l_opy_.bstack1ll1111l1l1_opy_(
                bstack11l1l1l1lll_opy_,
                bstack111l1l11l_opy_.bstack1l1lllll1l1_opy_,
                bstack1l1111l_opy_ (u"ࠦࠧ៪")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack111l1l11l_opy_.bstack1ll1111l1l1_opy_(bstack11l1l1l1lll_opy_, bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭៫"), None)
                if instance_test_id != current_test_id:
                    bstack11l1ll11l1l_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1ll11l1l_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧ៬")
                if bstack1lllllll11l_opy_
                else bstack1l1111l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨ៭")
            )
            session.ref = str(bstack11l1l1l1lll_opy_.ref() or bstack1l1111l_opy_ (u"ࠣࠤ៮"))
            session.hub_url = str(bstack111l1l11l_opy_.bstack1ll1111l1l1_opy_(
                bstack11l1l1l1lll_opy_,
                bstack111l1l11l_opy_.bstack11111llll_opy_,
                bstack1l1111l_opy_ (u"ࠤࠥ៯")
            ) or bstack1l1111l_opy_ (u"ࠥࠦ៰"))
            session.framework_name = str(bstack11l1l1l1lll_opy_.framework_name or bstack1l1111l_opy_ (u"ࠦࠧ៱"))
            session.framework_version = str(bstack11l1l1l1lll_opy_.framework_version or bstack1l1111l_opy_ (u"ࠧࠨ៲"))
            session.framework_session_id = str(session_id)
            bstack11l1ll1l111_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1l1lllll_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l11ll1l1_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack11l1l1lllll_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ៳") + str(kwargs) + bstack1l1111l_opy_ (u"ࠢࠣ៴"))
            return
        if len(bstack11l1l1lllll_opy_) > 1:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ៵") + str(kwargs) + bstack1l1111l_opy_ (u"ࠤࠥ៶"))
        bstack11l1ll11l11_opy_, bstack11ll1111111_opy_ = bstack11l1l1lllll_opy_[0]
        page = bstack11l1ll11l11_opy_()
        if not page:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ៷") + str(kwargs) + bstack1l1111l_opy_ (u"ࠦࠧ៸"))
            return
        return page
    def bstack11lllllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l1l1l1l11_opy_ = {}
        for bstack11l1l1l1lll_opy_ in bstack111l1l11l_opy_.bstack1lllll1ll1_opy_.values():
            caps = bstack111l1l11l_opy_.bstack1ll1111l1l1_opy_(bstack11l1l1l1lll_opy_, bstack111l1l11l_opy_.bstack1l111111l_opy_, {})
        bstack11l1l1l1l11_opy_[bstack1l1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ៹")] = caps.get(bstack1l1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ៺"), bstack1l1111l_opy_ (u"ࠢࠣ៻"))
        bstack11l1l1l1l11_opy_[bstack1l1111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ៼")] = caps.get(bstack1l1111l_opy_ (u"ࠤࡲࡷࠧ៽"), bstack1l1111l_opy_ (u"ࠥࠦ៾"))
        bstack11l1l1l1l11_opy_[bstack1l1111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ៿")] = caps.get(bstack1l1111l_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ᠀"), bstack1l1111l_opy_ (u"ࠨࠢ᠁"))
        bstack11l1l1l1l11_opy_[bstack1l1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ᠂")] = caps.get(bstack1l1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥ᠃"), bstack1l1111l_opy_ (u"ࠤࠥ᠄"))
        try:
            bstack11l1lllll1_opy_ = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11l1lllll1_opy_, int):
                bstack11l1lllll1_opy_ = 0
            bstack1llll11l11_opy_ = self.config.get(bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᠅"), [])
            bstack11l1l1lll11_opy_ = bstack1llll11l11_opy_[bstack11l1lllll1_opy_] if bstack11l1lllll1_opy_ < len(bstack1llll11l11_opy_) else self.config
            bstack1ll1lll1l11_opy_ = (
                bstack11l1l1lll11_opy_.get(bstack1l1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᠆"))
                or bstack11l1l1lll11_opy_.get(bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᠇"))
                or self.config.get(bstack1l1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᠈"))
                or self.config.get(bstack1l1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠉"))
            )
            if bstack1ll1lll1l11_opy_:
                bstack11l1l1l1l11_opy_[bstack1l1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᠊")] = bstack1ll1lll1l11_opy_
        except Exception as ex:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡦࡺࡴࡢࡥ࡫ࠤࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶ࠾ࠥࠨ᠋") + str(ex) + bstack1l1111l_opy_ (u"ࠥࠦ᠌"))
        return bstack11l1l1l1l11_opy_
    def bstack1l111111l1l_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack1l1111l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ᠍"), bstack1l1111l_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧ᠎"))
            if is_robot_playwright_installed():
                bstack11l1l1llll1_opy_ = script_code.replace(bstack1l1111l_opy_ (u"ࠨࡷࡪࡰࡧࡳࡼ࠴ࠢ᠏"), bstack1l1111l_opy_ (u"ࠢࡨ࡮ࡲࡦࡦࡲࡔࡩ࡫ࡶ࠲ࠧ᠐"))
                bstack11l1l1llll1_opy_ = bstack11l1l1llll1_opy_.replace(bstack1l1111l_opy_ (u"ࠣࡹ࡬ࡲࡩࡵࡷ࡜ࠤ᠑"), bstack1l1111l_opy_ (u"ࠤࡪࡰࡴࡨࡡ࡭ࡖ࡫࡭ࡸࡡࠢ᠒"))
                bstack11l1l1l11ll_opy_ = bstack1l1111l_opy_ (u"ࠥࠦࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࠬ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢࡴࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠣࡁࠥࡡࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁࠧࠨࠢ᠓").format(fn_body=bstack11l1l1llll1_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1l1111l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫ᠔"),
                    None,
                    bstack11l1l1l11ll_opy_
                )
            else:
                script_template = bstack1l1111l_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥ᠕")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧ᠖") + str(e) + bstack1l1111l_opy_ (u"ࠢࠣ᠗"))