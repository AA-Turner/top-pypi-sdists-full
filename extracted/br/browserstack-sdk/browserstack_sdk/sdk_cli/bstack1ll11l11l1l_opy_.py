# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll11lll1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack111l1ll11l_opy_, bstack111ll11ll1_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1ll111_opy_ import bstack1l11l1l1l1l_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack1ll1111l1l_opy_, bstack1l111l11ll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll11l1lll1_opy_(bstack1l11l1l1l1l_opy_):
    bstack11llll11111_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᗲ")
    bstack1l111ll1l1l_opy_ = bstack1111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᗳ")
    bstack1l111l11lll_opy_ = bstack1111l_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᗴ")
    bstack11llll1l111_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᗵ")
    bstack11llll11lll_opy_ = bstack1111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᗶ")
    bstack1l1111lll1l_opy_ = bstack1111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᗷ")
    bstack11llll1l11l_opy_ = bstack1111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᗸ")
    bstack11llll1ll1l_opy_ = bstack1111l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᗹ")
    def __init__(self):
        super().__init__(bstack1l11l1ll1ll_opy_=self.bstack11llll11111_opy_, frameworks=[bstack1ll111ll1ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11llll111ll_opy_)
        if bstack111ll11ll1_opy_():
            TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1lll_opy_)
        else:
            TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l1lll_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11llll111l1_opy_ = self.bstack11lll1ll1ll_opy_(instance.context)
        if not bstack11llll111l1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᗺ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠨࠢᗻ"))
            return
        f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l111ll1l1l_opy_, bstack11llll111l1_opy_)
    def bstack11lll1ll1ll_opy_(self, context: bstack1ll11lll1l1_opy_, bstack11lll1lll11_opy_= True):
        if bstack11lll1lll11_opy_:
            bstack11llll111l1_opy_ = self.bstack1l11ll11111_opy_(context, reverse=True)
        else:
            bstack11llll111l1_opy_ = self.bstack1l11l1lll11_opy_(context, reverse=True)
        return [f for f in bstack11llll111l1_opy_ if f[1].state != bstack1ll1l1l1lll_opy_.QUIT]
    def bstack1l1l11l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll111ll_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if not bstack111l1ll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗼ") + str(kwargs) + bstack1111l_opy_ (u"ࠣࠤᗽ"))
            return
        bstack11llll111l1_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack11llll111l1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᗾ") + str(kwargs) + bstack1111l_opy_ (u"ࠥࠦᗿ"))
            return
        if len(bstack11llll111l1_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11l1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᘀ"))
        bstack11lll1lllll_opy_, bstack1l111111ll1_opy_ = bstack11llll111l1_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᘁ") + str(kwargs) + bstack1111l_opy_ (u"ࠨࠢᘂ"))
            return
        bstack11lll111_opy_ = getattr(args[0], bstack1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᘃ"), None) or getattr(args[0], bstack1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᘄ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᘅ")).get(bstack1111l_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᘆ")):
            try:
                page.evaluate(bstack1111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᘇ"),
                            bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᘈ") + json.dumps(
                                bstack11lll111_opy_) + bstack1111l_opy_ (u"ࠨࡽࡾࠤᘉ"))
            except Exception as e:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᘊ"), e)
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll111ll_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if not bstack111l1ll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᘋ") + str(kwargs) + bstack1111l_opy_ (u"ࠤࠥᘌ"))
            return
        bstack11llll111l1_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack11llll111l1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᘍ") + str(kwargs) + bstack1111l_opy_ (u"ࠦࠧᘎ"))
            return
        if len(bstack11llll111l1_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11l1ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᘏ"))
        bstack11lll1lllll_opy_, bstack1l111111ll1_opy_ = bstack11llll111l1_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᘐ") + str(kwargs) + bstack1111l_opy_ (u"ࠢࠣᘑ"))
            return
        status = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11lll1ll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᘒ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠤࠥᘓ"))
            return
        bstack11llll1ll11_opy_ = {bstack1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᘔ"): status.lower()}
        bstack11llll11l1l_opy_ = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11llll11l11_opy_, None)
        if status.lower() == bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘕ") and bstack11llll11l1l_opy_ is not None:
            bstack11llll1ll11_opy_[bstack1111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᘖ")] = bstack11llll11l1l_opy_[0][bstack1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᘗ")][0] if isinstance(bstack11llll11l1l_opy_, list) else str(bstack11llll11l1l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᘘ")).get(bstack1111l_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᘙ")):
            try:
                page.evaluate(
                        bstack1111l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᘚ"),
                        bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨᘛ")
                        + json.dumps(bstack11llll1ll11_opy_)
                        + bstack1111l_opy_ (u"ࠦࢂࠨᘜ")
                    )
            except Exception as e:
                self.logger.debug(bstack1111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧᘝ"), e)
    def bstack1l111l111l1_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll111ll_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if not bstack111l1ll11l_opy_:
            self.logger.debug(
                bstack1ll1l11l1ll_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᘞ"))
            return
        bstack11llll111l1_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack11llll111l1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᘟ") + str(kwargs) + bstack1111l_opy_ (u"ࠣࠤᘠ"))
            return
        if len(bstack11llll111l1_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11l1ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᘡ"))
        bstack11lll1lllll_opy_, bstack1l111111ll1_opy_ = bstack11llll111l1_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᘢ") + str(kwargs) + bstack1111l_opy_ (u"ࠦࠧᘣ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1111l_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥᘤ") + str(timestamp)
        try:
            page.evaluate(
                bstack1111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᘥ"),
                bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᘦ").format(
                    json.dumps(
                        {
                            bstack1111l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᘧ"): bstack1111l_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᘨ"),
                            bstack1111l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᘩ"): {
                                bstack1111l_opy_ (u"ࠦࡹࡿࡰࡦࠤᘪ"): bstack1111l_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᘫ"),
                                bstack1111l_opy_ (u"ࠨࡤࡢࡶࡤࠦᘬ"): data,
                                bstack1111l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᘭ"): bstack1111l_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᘮ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦᘯ"), e)
    def bstack1l11l1111ll_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll111ll_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l1111lll1l_opy_, False):
            return
        self.bstack1l1l111l1ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1111l_opy_ (u"ࠥࠦᘰ"))
        req.platform_index = int(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_, 0) or 0)
        req.client_worker_id = bstack1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᘱ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_, bstack1111l_opy_ (u"ࠧࠨᘲ")) or bstack1111l_opy_ (u"ࠨࠢᘳ"))
        req.test_framework_version = str(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_, bstack1111l_opy_ (u"ࠢࠣᘴ")) or bstack1111l_opy_ (u"ࠣࠤᘵ"))
        req.test_framework_state = str(bstack1ll1l111l11_opy_[0].name)
        req.test_hook_state = str(bstack1ll1l111l11_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, bstack1111l_opy_ (u"ࠤࠥᘶ")) or bstack1111l_opy_ (u"ࠥࠦᘷ"))
        current_test_id = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11llll1l1l1_opy_, None)
        bstack11lll1llll1_opy_ = 0
        bstack11llll1111l_opy_ = 0
        for bstack11lll1ll11l_opy_ in bstack1ll1llllll1_opy_.bstack1ll1lll111l_opy_.values():
            session_id = bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(
                bstack11lll1ll11l_opy_,
                bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_,
                bstack1111l_opy_ (u"ࠦࠧᘸ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(bstack11lll1ll11l_opy_, bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭ᘹ"), None)
                if instance_test_id != current_test_id:
                    bstack11llll1111l_opy_ += 1
                    continue
                if not session_id:
                    bstack11llll1111l_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᘺ")
                if bstack111l1ll11l_opy_
                else bstack1111l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨᘻ")
            )
            session.ref = str(bstack11lll1ll11l_opy_.ref() or bstack1111l_opy_ (u"ࠣࠤᘼ"))
            session.hub_url = str(bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(
                bstack11lll1ll11l_opy_,
                bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_,
                bstack1111l_opy_ (u"ࠤࠥᘽ")
            ) or bstack1111l_opy_ (u"ࠥࠦᘾ"))
            session.framework_name = str(bstack11lll1ll11l_opy_.framework_name or bstack1111l_opy_ (u"ࠦࠧᘿ"))
            session.framework_version = str(bstack11lll1ll11l_opy_.framework_version or bstack1111l_opy_ (u"ࠧࠨᙀ"))
            session.framework_session_id = str(session_id)
            bstack11lll1llll1_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11llll111l1_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1lll1_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack11llll111l1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙁ") + str(kwargs) + bstack1111l_opy_ (u"ࠢࠣᙂ"))
            return
        if len(bstack11llll111l1_opy_) > 1:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙃ") + str(kwargs) + bstack1111l_opy_ (u"ࠤࠥᙄ"))
        bstack11lll1lllll_opy_, bstack1l111111ll1_opy_ = bstack11llll111l1_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙅ") + str(kwargs) + bstack1111l_opy_ (u"ࠦࠧᙆ"))
            return
        return page
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11lll1lll1l_opy_ = {}
        for bstack11lll1ll11l_opy_ in bstack1ll1llllll1_opy_.bstack1ll1lll111l_opy_.values():
            caps = bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(bstack11lll1ll11l_opy_, bstack1ll1llllll1_opy_.bstack1ll1lll1lll_opy_, {})
        bstack11lll1lll1l_opy_[bstack1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥᙇ")] = caps.get(bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢᙈ"), bstack1111l_opy_ (u"ࠢࠣᙉ"))
        bstack11lll1lll1l_opy_[bstack1111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᙊ")] = caps.get(bstack1111l_opy_ (u"ࠤࡲࡷࠧᙋ"), bstack1111l_opy_ (u"ࠥࠦᙌ"))
        bstack11lll1lll1l_opy_[bstack1111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᙍ")] = caps.get(bstack1111l_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᙎ"), bstack1111l_opy_ (u"ࠨࠢᙏ"))
        bstack11lll1lll1l_opy_[bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣᙐ")] = caps.get(bstack1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥᙑ"), bstack1111l_opy_ (u"ࠤࠥᙒ"))
        try:
            bstack111l11l1ll_opy_ = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack111l11l1ll_opy_, int):
                bstack111l11l1ll_opy_ = 0
            bstack1111l11l11_opy_ = self.config.get(bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᙓ"), [])
            bstack11llll11ll1_opy_ = bstack1111l11l11_opy_[bstack111l11l1ll_opy_] if bstack111l11l1ll_opy_ < len(bstack1111l11l11_opy_) else self.config
            bstack11llll1l1ll_opy_ = (
                bstack11llll11ll1_opy_.get(bstack1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙔ"))
                or bstack11llll11ll1_opy_.get(bstack1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᙕ"))
                or self.config.get(bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙖ"))
                or self.config.get(bstack1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᙗ"))
            )
            if bstack11llll1l1ll_opy_:
                bstack11lll1lll1l_opy_[bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙘ")] = bstack11llll1l1ll_opy_
        except Exception as ex:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡦࡺࡴࡢࡥ࡫ࠤࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᙙ") + str(ex) + bstack1111l_opy_ (u"ࠥࠦᙚ"))
        return bstack11lll1lll1l_opy_
    def bstack1l1l1111l1l_opy_(self, page: object, script_code, args={}):
        try:
            script_template = bstack1111l_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥᙛ")
            script_code = script_code.replace(bstack1111l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᙜ"), bstack1111l_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨᙝ"))
            script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨᙞ") + str(e) + bstack1111l_opy_ (u"ࠣࠤᙟ"))