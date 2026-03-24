# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack1ll11l1l111_opy_,
    bstack1ll11ll1ll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11l1111l_opy_, bstack1l11ll1lll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111l1_opy_ import bstack1l11l111lll_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack1111lll1l1_opy_, bstack11ll11ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1ll111l11_opy_(bstack1l11l111lll_opy_):
    bstack11lll11111l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᘪ")
    bstack11lllll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᘫ")
    bstack1l111ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᘬ")
    bstack11lll1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᘭ")
    bstack11lll111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᘮ")
    bstack1l1111lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᘯ")
    bstack11lll1l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᘰ")
    bstack11lll1l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᘱ")
    def __init__(self):
        super().__init__(bstack1l11l11l1l1_opy_=self.bstack11lll11111l_opy_, frameworks=[bstack1l1llll1111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11lll1l1111_opy_)
        if bstack1l11ll1lll_opy_():
            TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1lll1_opy_)
        else:
            TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11ll1lll1_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1llllll_opy_ = self.bstack11lll11l1l1_opy_(instance.context)
        if not bstack11ll1llllll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᘲ") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢᘳ"))
            return
        f.bstack1l1l11lll_opy_(instance, bstack1l1ll111l11_opy_.bstack11lllll1l11_opy_, bstack11ll1llllll_opy_)
    def bstack11lll11l1l1_opy_(self, context: bstack1ll11ll1ll1_opy_, bstack11lll11llll_opy_= True):
        if bstack11lll11llll_opy_:
            bstack11ll1llllll_opy_ = self.bstack1l11l111l11_opy_(context, reverse=True)
        else:
            bstack11ll1llllll_opy_ = self.bstack1l11l111l1l_opy_(context, reverse=True)
        return [f for f in bstack11ll1llllll_opy_ if f[1].state != bstack111l11ll_opy_.QUIT]
    def bstack1l11ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if not bstack1l11l1111l_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᘴ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠣࠤᘵ"))
            return
        bstack11ll1llllll_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll111l11_opy_.bstack11lllll1l11_opy_, [])
        if not bstack11ll1llllll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᘶ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᘷ"))
            return
        if len(bstack11ll1llllll_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll11l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᘸ"))
        bstack11lll111l11_opy_, bstack11llll1ll11_opy_ = bstack11ll1llllll_opy_[0]
        page = bstack11lll111l11_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᘹ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᘺ"))
            return
        bstack1ll1l11l1l_opy_ = getattr(args[0], bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᘻ"), None) or getattr(args[0], bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᘼ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᘽ")).get(bstack1ll1lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᘾ")):
            try:
                page.evaluate(bstack1ll1lll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᘿ"),
                            bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᙀ") + json.dumps(
                                bstack1ll1l11l1l_opy_) + bstack1ll1lll_opy_ (u"ࠨࡽࡾࠤᙁ"))
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᙂ"), e)
    def bstack1l11lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if not bstack1l11l1111l_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙃ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥᙄ"))
            return
        bstack11ll1llllll_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll111l11_opy_.bstack11lllll1l11_opy_, [])
        if not bstack11ll1llllll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙅ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᙆ"))
            return
        if len(bstack11ll1llllll_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll11l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᙇ"))
        bstack11lll111l11_opy_, bstack11llll1ll11_opy_ = bstack11ll1llllll_opy_[0]
        page = bstack11lll111l11_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙈ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᙉ"))
            return
        status = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11lll11ll11_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᙊ") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᙋ"))
            return
        bstack11lll1l11l1_opy_ = {bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᙌ"): status.lower()}
        bstack11ll1lllll1_opy_ = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11lll11ll1l_opy_, None)
        if status.lower() == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙍ") and bstack11ll1lllll1_opy_ is not None:
            bstack11lll1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙎ")] = bstack11ll1lllll1_opy_[0][bstack1ll1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᙏ")][0] if isinstance(bstack11ll1lllll1_opy_, list) else str(bstack11ll1lllll1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᙐ")).get(bstack1ll1lll_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᙑ")):
            try:
                page.evaluate(
                        bstack1ll1lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᙒ"),
                        bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨᙓ")
                        + json.dumps(bstack11lll1l11l1_opy_)
                        + bstack1ll1lll_opy_ (u"ࠦࢂࠨᙔ")
                    )
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧᙕ"), e)
    def bstack1l11111l1l1_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if not bstack1l11l1111l_opy_:
            self.logger.debug(
                bstack1ll11ll11l1_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᙖ"))
            return
        bstack11ll1llllll_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll111l11_opy_.bstack11lllll1l11_opy_, [])
        if not bstack11ll1llllll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙗ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠣࠤᙘ"))
            return
        if len(bstack11ll1llllll_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll11l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᙙ"))
        bstack11lll111l11_opy_, bstack11llll1ll11_opy_ = bstack11ll1llllll_opy_[0]
        page = bstack11lll111l11_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙚ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᙛ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll1lll_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥᙜ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᙝ"),
                bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᙞ").format(
                    json.dumps(
                        {
                            bstack1ll1lll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᙟ"): bstack1ll1lll_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᙠ"),
                            bstack1ll1lll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᙡ"): {
                                bstack1ll1lll_opy_ (u"ࠦࡹࡿࡰࡦࠤᙢ"): bstack1ll1lll_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᙣ"),
                                bstack1ll1lll_opy_ (u"ࠨࡤࡢࡶࡤࠦᙤ"): data,
                                bstack1ll1lll_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᙥ"): bstack1ll1lll_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᙦ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦᙧ"), e)
    def bstack1l1111ll1ll_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll111l11_opy_.bstack1l1111lll1l_opy_, False):
            return
        self.bstack1l11l1ll111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1ll1lll_opy_ (u"ࠥࠦᙨ"))
        req.platform_index = int(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11llll111_opy_, 0) or 0)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᙩ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11lll111l_opy_, bstack1ll1lll_opy_ (u"ࠧࠨᙪ")) or bstack1ll1lll_opy_ (u"ࠨࠢᙫ"))
        req.test_framework_version = str(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1111l1ll1_opy_, bstack1ll1lll_opy_ (u"ࠢࠣᙬ")) or bstack1ll1lll_opy_ (u"ࠣࠤ᙭"))
        req.test_framework_state = str(bstack1ll11l1ll11_opy_[0].name)
        req.test_hook_state = str(bstack1ll11l1ll11_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_, bstack1ll1lll_opy_ (u"ࠤࠥ᙮")) or bstack1ll1lll_opy_ (u"ࠥࠦᙯ"))
        current_test_id = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11lll111lll_opy_, None)
        bstack11lll11lll1_opy_ = 0
        bstack11lll11l11l_opy_ = 0
        for bstack11lll111ll1_opy_ in bstack11ll1l1l_opy_.bstack111llll1l_opy_.values():
            session_id = bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(
                bstack11lll111ll1_opy_,
                bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_,
                bstack1ll1lll_opy_ (u"ࠦࠧᙰ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(bstack11lll111ll1_opy_, bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭ᙱ"), None)
                if instance_test_id != current_test_id:
                    bstack11lll11l11l_opy_ += 1
                    continue
                if not session_id:
                    bstack11lll11l11l_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᙲ")
                if bstack1l11l1111l_opy_
                else bstack1ll1lll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨᙳ")
            )
            session.ref = str(bstack11lll111ll1_opy_.ref() or bstack1ll1lll_opy_ (u"ࠣࠤᙴ"))
            session.hub_url = str(bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(
                bstack11lll111ll1_opy_,
                bstack11ll1l1l_opy_.bstack1l111ll111_opy_,
                bstack1ll1lll_opy_ (u"ࠤࠥᙵ")
            ) or bstack1ll1lll_opy_ (u"ࠥࠦᙶ"))
            session.framework_name = str(bstack11lll111ll1_opy_.framework_name or bstack1ll1lll_opy_ (u"ࠦࠧᙷ"))
            session.framework_version = str(bstack11lll111ll1_opy_.framework_version or bstack1ll1lll_opy_ (u"ࠧࠨᙸ"))
            session.framework_session_id = str(session_id)
            bstack11lll11lll1_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l11l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1llllll_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll111l11_opy_.bstack11lllll1l11_opy_, [])
        if not bstack11ll1llllll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙹ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᙺ"))
            return
        if len(bstack11ll1llllll_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙻ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥᙼ"))
        bstack11lll111l11_opy_, bstack11llll1ll11_opy_ = bstack11ll1llllll_opy_[0]
        page = bstack11lll111l11_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙽ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᙾ"))
            return
        return page
    def bstack1l11lll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11lll11l111_opy_ = {}
        for bstack11lll111ll1_opy_ in bstack11ll1l1l_opy_.bstack111llll1l_opy_.values():
            caps = bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(bstack11lll111ll1_opy_, bstack11ll1l1l_opy_.bstack11111l11l_opy_, {})
        bstack11lll11l111_opy_[bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥᙿ")] = caps.get(bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ "), bstack1ll1lll_opy_ (u"ࠢࠣᚁ"))
        bstack11lll11l111_opy_[bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᚂ")] = caps.get(bstack1ll1lll_opy_ (u"ࠤࡲࡷࠧᚃ"), bstack1ll1lll_opy_ (u"ࠥࠦᚄ"))
        bstack11lll11l111_opy_[bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᚅ")] = caps.get(bstack1ll1lll_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᚆ"), bstack1ll1lll_opy_ (u"ࠨࠢᚇ"))
        bstack11lll11l111_opy_[bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣᚈ")] = caps.get(bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥᚉ"), bstack1ll1lll_opy_ (u"ࠤࠥᚊ"))
        try:
            bstack111111lll1_opy_ = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11llll111_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack111111lll1_opy_, int):
                bstack111111lll1_opy_ = 0
            bstack111lll1lll_opy_ = self.config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᚋ"), [])
            bstack11lll1l111l_opy_ = bstack111lll1lll_opy_[bstack111111lll1_opy_] if bstack111111lll1_opy_ < len(bstack111lll1lll_opy_) else self.config
            bstack11lll11l1ll_opy_ = (
                bstack11lll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚌ"))
                or bstack11lll1l111l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚍ"))
                or self.config.get(bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚎ"))
                or self.config.get(bstack1ll1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚏ"))
            )
            if bstack11lll11l1ll_opy_:
                bstack11lll11l111_opy_[bstack1ll1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚐ")] = bstack11lll11l1ll_opy_
        except Exception as ex:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡦࡺࡴࡢࡥ࡫ࠤࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᚑ") + str(ex) + bstack1ll1lll_opy_ (u"ࠥࠦᚒ"))
        return bstack11lll11l111_opy_
    def bstack1l1l11111l1_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack1ll1lll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᚓ"), bstack1ll1lll_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧᚔ"))
            if is_robot_playwright_installed():
                bstack11lll1111l1_opy_ = script_code.replace(bstack1ll1lll_opy_ (u"ࠨࡷࡪࡰࡧࡳࡼ࠴ࠢᚕ"), bstack1ll1lll_opy_ (u"ࠢࡨ࡮ࡲࡦࡦࡲࡔࡩ࡫ࡶ࠲ࠧᚖ"))
                bstack11lll1111l1_opy_ = bstack11lll1111l1_opy_.replace(bstack1ll1lll_opy_ (u"ࠣࡹ࡬ࡲࡩࡵࡷ࡜ࠤᚗ"), bstack1ll1lll_opy_ (u"ࠤࡪࡰࡴࡨࡡ࡭ࡖ࡫࡭ࡸࡡࠢᚘ"))
                bstack11lll111111_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࠬ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢࡴࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠣࡁࠥࡡࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁࠧࠨࠢᚙ").format(fn_body=bstack11lll1111l1_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1ll1lll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫᚚ"),
                    None,
                    bstack11lll111111_opy_
                )
            else:
                script_template = bstack1ll1lll_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥ᚛")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧ᚜") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣ᚝"))