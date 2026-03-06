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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1ll1l111_opy_,
    bstack1ll1ll11l11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111l1ll1l_opy_, bstack1l1ll11l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1l1l1_opy_ import bstack1l11ll1llll_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack1l1lllll1l_opy_, bstack11lllll111_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll111l1lll_opy_(bstack1l11ll1llll_opy_):
    bstack11lllll1ll1_opy_ = bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣᕏ")
    bstack1l11l1111l1_opy_ = bstack1111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᕐ")
    bstack1l111l1llll_opy_ = bstack1111_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᕑ")
    bstack11llll1lll1_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᕒ")
    bstack11lllll1l11_opy_ = bstack1111_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥᕓ")
    bstack1l111lll1ll_opy_ = bstack1111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨᕔ")
    bstack11llllll1l1_opy_ = bstack1111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᕕ")
    bstack11llllll1ll_opy_ = bstack1111_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢᕖ")
    def __init__(self):
        super().__init__(bstack1l11lll11ll_opy_=self.bstack11lllll1ll1_opy_, frameworks=[bstack1ll11l11111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11lllll1lll_opy_)
        if bstack1l1ll11l_opy_():
            TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l11ll_opy_)
        else:
            TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l11ll_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lllll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11llllll111_opy_ = self.bstack11lllllll11_opy_(instance.context)
        if not bstack11llllll111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᕗ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠦࠧᕘ"))
            return
        f.bstack1lll1l11l1l_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11l1111l1_opy_, bstack11llllll111_opy_)
    def bstack11lllllll11_opy_(self, context: bstack1ll1ll11l11_opy_, bstack11lllllll1l_opy_= True):
        if bstack11lllllll1l_opy_:
            bstack11llllll111_opy_ = self.bstack1l11ll1ll1l_opy_(context, reverse=True)
        else:
            bstack11llllll111_opy_ = self.bstack1l11lll11l1_opy_(context, reverse=True)
        return [f for f in bstack11llllll111_opy_ if f[1].state != bstack1ll1lll1ll1_opy_.QUIT]
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l111l1ll1l_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᕙ") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢᕚ"))
            return
        bstack11llllll111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack11llllll111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕛ") + str(kwargs) + bstack1111_opy_ (u"ࠣࠤᕜ"))
            return
        if len(bstack11llllll111_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1l11l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᕝ"))
        bstack11lllll1111_opy_, bstack1l1111l1lll_opy_ = bstack11llllll111_opy_[0]
        page = bstack11lllll1111_opy_()
        if not page:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕞ") + str(kwargs) + bstack1111_opy_ (u"ࠦࠧᕟ"))
            return
        bstack11ll1l11l1_opy_ = getattr(args[0], bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᕠ"), None) or getattr(args[0], bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᕡ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᕢ")).get(bstack1111_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᕣ")):
            try:
                page.evaluate(bstack1111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᕤ"),
                            bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧᕥ") + json.dumps(
                                bstack11ll1l11l1_opy_) + bstack1111_opy_ (u"ࠦࢂࢃࠢᕦ"))
            except Exception as e:
                self.logger.debug(bstack1111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥᕧ"), e)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l111l1ll1l_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᕨ") + str(kwargs) + bstack1111_opy_ (u"ࠢࠣᕩ"))
            return
        bstack11llllll111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack11llllll111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᕪ") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥᕫ"))
            return
        if len(bstack11llllll111_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1l11l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᕬ"))
        bstack11lllll1111_opy_, bstack1l1111l1lll_opy_ = bstack11llllll111_opy_[0]
        page = bstack11lllll1111_opy_()
        if not page:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᕭ") + str(kwargs) + bstack1111_opy_ (u"ࠧࠨᕮ"))
            return
        status = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll111l_opy_, None)
        if not status:
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᕯ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠢࠣᕰ"))
            return
        bstack11lllll1l1l_opy_ = {bstack1111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᕱ"): status.lower()}
        bstack11llll1llll_opy_ = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll11l1_opy_, None)
        if status.lower() == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᕲ") and bstack11llll1llll_opy_ is not None:
            bstack11lllll1l1l_opy_[bstack1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᕳ")] = bstack11llll1llll_opy_[0][bstack1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᕴ")][0] if isinstance(bstack11llll1llll_opy_, list) else str(bstack11llll1llll_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᕵ")).get(bstack1111_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᕶ")):
            try:
                page.evaluate(
                        bstack1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᕷ"),
                        bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ᕸ")
                        + json.dumps(bstack11lllll1l1l_opy_)
                        + bstack1111_opy_ (u"ࠤࢀࠦᕹ")
                    )
            except Exception as e:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥᕺ"), e)
    def bstack1l11l1111ll_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l111l1ll1l_opy_:
            self.logger.debug(
                bstack1ll1l1l11l1_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᕻ"))
            return
        bstack11llllll111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack11llllll111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᕼ") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢᕽ"))
            return
        if len(bstack11llllll111_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1l11l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᕾ"))
        bstack11lllll1111_opy_, bstack1l1111l1lll_opy_ = bstack11llllll111_opy_[0]
        page = bstack11lllll1111_opy_()
        if not page:
            self.logger.debug(bstack1111_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᕿ") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥᖀ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1111_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣᖁ") + str(timestamp)
        try:
            page.evaluate(
                bstack1111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᖂ"),
                bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪᖃ").format(
                    json.dumps(
                        {
                            bstack1111_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᖄ"): bstack1111_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤᖅ"),
                            bstack1111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᖆ"): {
                                bstack1111_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᖇ"): bstack1111_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢᖈ"),
                                bstack1111_opy_ (u"ࠦࡩࡧࡴࡢࠤᖉ"): data,
                                bstack1111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦᖊ"): bstack1111_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧᖋ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤᖌ"), e)
    def bstack1l11l111111_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if f.bstack1lll1l11111_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111lll1ll_opy_, False):
            return
        self.bstack1l1l111ll1l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1111_opy_ (u"ࠣࠤᖍ"))
        req.platform_index = int(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1ll1_opy_, 0) or 0)
        req.client_worker_id = bstack1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᖎ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111l11_opy_, bstack1111_opy_ (u"ࠥࠦᖏ")) or bstack1111_opy_ (u"ࠦࠧᖐ"))
        req.test_framework_version = str(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l111llll11_opy_, bstack1111_opy_ (u"ࠧࠨᖑ")) or bstack1111_opy_ (u"ࠨࠢᖒ"))
        req.test_framework_state = str(bstack1ll1ll1ll1l_opy_[0].name)
        req.test_hook_state = str(bstack1ll1ll1ll1l_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_, bstack1111_opy_ (u"ࠢࠣᖓ")) or bstack1111_opy_ (u"ࠣࠤᖔ"))
        current_test_id = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11llll1ll1l_opy_, None)
        bstack1l111111111_opy_ = 0
        bstack11llllll11l_opy_ = 0
        for bstack11lllll11ll_opy_ in bstack1lll11l11ll_opy_.bstack1lll1111lll_opy_.values():
            session_id = bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(
                bstack11lllll11ll_opy_,
                bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_,
                bstack1111_opy_ (u"ࠤࠥᖕ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(bstack11lllll11ll_opy_, bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠ࡫ࡧࠫᖖ"), None)
                if instance_test_id != current_test_id:
                    bstack11llllll11l_opy_ += 1
                    continue
                if not session_id:
                    bstack11llllll11l_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᖗ")
                if bstack1l111l1ll1l_opy_
                else bstack1111_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᖘ")
            )
            session.ref = str(bstack11lllll11ll_opy_.ref() or bstack1111_opy_ (u"ࠨࠢᖙ"))
            session.hub_url = str(bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(
                bstack11lllll11ll_opy_,
                bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_,
                bstack1111_opy_ (u"ࠢࠣᖚ")
            ) or bstack1111_opy_ (u"ࠣࠤᖛ"))
            session.framework_name = str(bstack11lllll11ll_opy_.framework_name or bstack1111_opy_ (u"ࠤࠥᖜ"))
            session.framework_version = str(bstack11lllll11ll_opy_.framework_version or bstack1111_opy_ (u"ࠥࠦᖝ"))
            session.framework_session_id = str(session_id)
            bstack1l111111111_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1l1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11llllll111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack11llllll111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᖞ") + str(kwargs) + bstack1111_opy_ (u"ࠧࠨᖟ"))
            return
        if len(bstack11llllll111_opy_) > 1:
            self.logger.debug(bstack1111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᖠ") + str(kwargs) + bstack1111_opy_ (u"ࠢࠣᖡ"))
        bstack11lllll1111_opy_, bstack1l1111l1lll_opy_ = bstack11llllll111_opy_[0]
        page = bstack11lllll1111_opy_()
        if not page:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᖢ") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥᖣ"))
            return
        return page
    def bstack1l1l1l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11llllllll1_opy_ = {}
        for bstack11lllll11ll_opy_ in bstack1lll11l11ll_opy_.bstack1lll1111lll_opy_.values():
            caps = bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(bstack11lllll11ll_opy_, bstack1lll11l11ll_opy_.bstack1lll1111l11_opy_, {})
        bstack11llllllll1_opy_[bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣᖤ")] = caps.get(bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧᖥ"), bstack1111_opy_ (u"ࠧࠨᖦ"))
        bstack11llllllll1_opy_[bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᖧ")] = caps.get(bstack1111_opy_ (u"ࠢࡰࡵࠥᖨ"), bstack1111_opy_ (u"ࠣࠤᖩ"))
        bstack11llllllll1_opy_[bstack1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᖪ")] = caps.get(bstack1111_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᖫ"), bstack1111_opy_ (u"ࠦࠧᖬ"))
        bstack11llllllll1_opy_[bstack1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨᖭ")] = caps.get(bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᖮ"), bstack1111_opy_ (u"ࠢࠣᖯ"))
        return bstack11llllllll1_opy_
    def bstack1l1l1l1111l_opy_(self, page: object, bstack1l1l11ll1ll_opy_, args={}):
        try:
            bstack11lllllllll_opy_ = bstack1111_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢᖰ")
            bstack1l1l11ll1ll_opy_ = bstack1l1l11ll1ll_opy_.replace(bstack1111_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᖱ"), bstack1111_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥᖲ"))
            script = bstack11lllllllll_opy_.format(fn_body=bstack1l1l11ll1ll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥᖳ") + str(e) + bstack1111_opy_ (u"ࠧࠨᖴ"))