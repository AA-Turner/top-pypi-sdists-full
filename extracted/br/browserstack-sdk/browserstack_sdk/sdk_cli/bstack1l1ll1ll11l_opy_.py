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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1l1l111l_opy_,
    bstack1ll11llll1l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lll111l1_opy_, bstack11l11l1111_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1lll1l_opy_ import bstack1l11l1llll1_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack111lll11_opy_, bstack1llll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll11111ll1_opy_(bstack1l11l1llll1_opy_):
    bstack11llll111ll_opy_ = bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᖷ")
    bstack1l111l1l1l1_opy_ = bstack1ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᖸ")
    bstack1l111l1l11l_opy_ = bstack1ll111_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᖹ")
    bstack11lll1lll1l_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᖺ")
    bstack11llll11ll1_opy_ = bstack1ll111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᖻ")
    bstack1l111l1l111_opy_ = bstack1ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᖼ")
    bstack11llll1l111_opy_ = bstack1ll111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᖽ")
    bstack11llll1l1l1_opy_ = bstack1ll111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᖾ")
    def __init__(self):
        super().__init__(bstack1l11l1l1ll1_opy_=self.bstack11llll111ll_opy_, frameworks=[bstack1ll11lll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11llll1l1ll_opy_)
        if bstack11l11l1111_opy_():
            TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11ll1ll_opy_)
        else:
            TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11ll1ll_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11llll11l11_opy_ = self.bstack11lll1lll11_opy_(instance.context)
        if not bstack11llll11l11_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᖿ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠥࠦᗀ"))
            return
        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l1l1_opy_, bstack11llll11l11_opy_)
    def bstack11lll1lll11_opy_(self, context: bstack1ll11llll1l_opy_, bstack11llll11lll_opy_= True):
        if bstack11llll11lll_opy_:
            bstack11llll11l11_opy_ = self.bstack1l11l1ll1ll_opy_(context, reverse=True)
        else:
            bstack11llll11l11_opy_ = self.bstack1l11l1ll111_opy_(context, reverse=True)
        return [f for f in bstack11llll11l11_opy_ if f[1].state != bstack1ll1l1l11l1_opy_.QUIT]
    def bstack1l1l11ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll1l1ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if not bstack1lll111l1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗁ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᗂ"))
            return
        bstack11llll11l11_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack11llll11l11_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᗃ") + str(kwargs) + bstack1ll111_opy_ (u"ࠢࠣᗄ"))
            return
        if len(bstack11llll11l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᗅ"))
        bstack11lll1lllll_opy_, bstack11lllllllll_opy_ = bstack11llll11l11_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᗆ") + str(kwargs) + bstack1ll111_opy_ (u"ࠥࠦᗇ"))
            return
        bstack11l11l111_opy_ = getattr(args[0], bstack1ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᗈ"), None) or getattr(args[0], bstack1ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᗉ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᗊ")).get(bstack1ll111_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᗋ")):
            try:
                page.evaluate(bstack1ll111_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᗌ"),
                            bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᗍ") + json.dumps(
                                bstack11l11l111_opy_) + bstack1ll111_opy_ (u"ࠥࢁࢂࠨᗎ"))
            except Exception as e:
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᗏ"), e)
    def bstack1l11lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll1l1ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if not bstack1lll111l1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᗐ") + str(kwargs) + bstack1ll111_opy_ (u"ࠨࠢᗑ"))
            return
        bstack11llll11l11_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack11llll11l11_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗒ") + str(kwargs) + bstack1ll111_opy_ (u"ࠣࠤᗓ"))
            return
        if len(bstack11llll11l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11llll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᗔ"))
        bstack11lll1lllll_opy_, bstack11lllllllll_opy_ = bstack11llll11l11_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗕ") + str(kwargs) + bstack1ll111_opy_ (u"ࠦࠧᗖ"))
            return
        status = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack11lll1llll1_opy_, None)
        if not status:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᗗ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠨࠢᗘ"))
            return
        bstack11llll1ll1l_opy_ = {bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᗙ"): status.lower()}
        bstack11llll111l1_opy_ = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack11llll11111_opy_, None)
        if status.lower() == bstack1ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᗚ") and bstack11llll111l1_opy_ is not None:
            bstack11llll1ll1l_opy_[bstack1ll111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᗛ")] = bstack11llll111l1_opy_[0][bstack1ll111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᗜ")][0] if isinstance(bstack11llll111l1_opy_, list) else str(bstack11llll111l1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᗝ")).get(bstack1ll111_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᗞ")):
            try:
                page.evaluate(
                        bstack1ll111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗟ"),
                        bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬᗠ")
                        + json.dumps(bstack11llll1ll1l_opy_)
                        + bstack1ll111_opy_ (u"ࠣࡿࠥᗡ")
                    )
            except Exception as e:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᗢ"), e)
    def bstack1l111lll1l1_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        f: TestFramework,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll1l1ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if not bstack1lll111l1_opy_:
            self.logger.debug(
                bstack1ll1l11llll_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᗣ"))
            return
        bstack11llll11l11_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack11llll11l11_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗤ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᗥ"))
            return
        if len(bstack11llll11l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1l11llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᗦ"))
        bstack11lll1lllll_opy_, bstack11lllllllll_opy_ = bstack11llll11l11_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗧ") + str(kwargs) + bstack1ll111_opy_ (u"ࠣࠤᗨ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll111_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᗩ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᗪ"),
                bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᗫ").format(
                    json.dumps(
                        {
                            bstack1ll111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᗬ"): bstack1ll111_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᗭ"),
                            bstack1ll111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᗮ"): {
                                bstack1ll111_opy_ (u"ࠣࡶࡼࡴࡪࠨᗯ"): bstack1ll111_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᗰ"),
                                bstack1ll111_opy_ (u"ࠥࡨࡦࡺࡡࠣᗱ"): data,
                                bstack1ll111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᗲ"): bstack1ll111_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᗳ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣᗴ"), e)
    def bstack1l111llll1l_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        f: TestFramework,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llll1l1ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if f.bstack1lll111lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l111_opy_, False):
            return
        self.bstack1l11ll1llll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1ll111_opy_ (u"ࠢࠣᗵ"))
        req.platform_index = int(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_, 0) or 0)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᗶ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l11llllll1_opy_, bstack1ll111_opy_ (u"ࠤࠥᗷ")) or bstack1ll111_opy_ (u"ࠥࠦᗸ"))
        req.test_framework_version = str(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l111l111ll_opy_, bstack1ll111_opy_ (u"ࠦࠧᗹ")) or bstack1ll111_opy_ (u"ࠧࠨᗺ"))
        req.test_framework_state = str(bstack1ll1l1l1l1l_opy_[0].name)
        req.test_hook_state = str(bstack1ll1l1l1l1l_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, bstack1ll111_opy_ (u"ࠨࠢᗻ")) or bstack1ll111_opy_ (u"ࠢࠣᗼ"))
        current_test_id = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11llll1lll1_opy_, None)
        bstack11llll1111l_opy_ = 0
        bstack11llll1ll11_opy_ = 0
        for bstack11llll11l1l_opy_ in bstack1lll111l1l1_opy_.bstack1ll1llllll1_opy_.values():
            session_id = bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(
                bstack11llll11l1l_opy_,
                bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_,
                bstack1ll111_opy_ (u"ࠣࠤᗽ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(bstack11llll11l1l_opy_, bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪᗾ"), None)
                if instance_test_id != current_test_id:
                    bstack11llll1ll11_opy_ += 1
                    continue
                if not session_id:
                    bstack11llll1ll11_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᗿ")
                if bstack1lll111l1_opy_
                else bstack1ll111_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᘀ")
            )
            session.ref = str(bstack11llll11l1l_opy_.ref() or bstack1ll111_opy_ (u"ࠧࠨᘁ"))
            session.hub_url = str(bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(
                bstack11llll11l1l_opy_,
                bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_,
                bstack1ll111_opy_ (u"ࠨࠢᘂ")
            ) or bstack1ll111_opy_ (u"ࠢࠣᘃ"))
            session.framework_name = str(bstack11llll11l1l_opy_.framework_name or bstack1ll111_opy_ (u"ࠣࠤᘄ"))
            session.framework_version = str(bstack11llll11l1l_opy_.framework_version or bstack1ll111_opy_ (u"ࠤࠥᘅ"))
            session.framework_session_id = str(session_id)
            bstack11llll1111l_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11llll11l11_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll11111ll1_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack11llll11l11_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᘆ") + str(kwargs) + bstack1ll111_opy_ (u"ࠦࠧᘇ"))
            return
        if len(bstack11llll11l11_opy_) > 1:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᘈ") + str(kwargs) + bstack1ll111_opy_ (u"ࠨࠢᘉ"))
        bstack11lll1lllll_opy_, bstack11lllllllll_opy_ = bstack11llll11l11_opy_[0]
        page = bstack11lll1lllll_opy_()
        if not page:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᘊ") + str(kwargs) + bstack1ll111_opy_ (u"ࠣࠤᘋ"))
            return
        return page
    def bstack1l11ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11llll1l11l_opy_ = {}
        for bstack11llll11l1l_opy_ in bstack1lll111l1l1_opy_.bstack1ll1llllll1_opy_.values():
            caps = bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(bstack11llll11l1l_opy_, bstack1lll111l1l1_opy_.bstack1ll1lll1l1l_opy_, {})
        bstack11llll1l11l_opy_[bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᘌ")] = caps.get(bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᘍ"), bstack1ll111_opy_ (u"ࠦࠧᘎ"))
        bstack11llll1l11l_opy_[bstack1ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᘏ")] = caps.get(bstack1ll111_opy_ (u"ࠨ࡯ࡴࠤᘐ"), bstack1ll111_opy_ (u"ࠢࠣᘑ"))
        bstack11llll1l11l_opy_[bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᘒ")] = caps.get(bstack1ll111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᘓ"), bstack1ll111_opy_ (u"ࠥࠦᘔ"))
        bstack11llll1l11l_opy_[bstack1ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘕ")] = caps.get(bstack1ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᘖ"), bstack1ll111_opy_ (u"ࠨࠢᘗ"))
        return bstack11llll1l11l_opy_
    def bstack1l11lll1lll_opy_(self, page: object, bstack1l1l1ll11l1_opy_, args={}):
        try:
            script_template = bstack1ll111_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᘘ")
            bstack1l1l1ll11l1_opy_ = bstack1l1l1ll11l1_opy_.replace(bstack1ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᘙ"), bstack1ll111_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᘚ"))
            script = script_template.format(fn_body=bstack1l1l1ll11l1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᘛ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧᘜ"))