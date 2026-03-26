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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack1ll11ll1l11_opy_,
    bstack1ll11l1l1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack11lll11l1_opy_, bstack1111ll11_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l111ll1ll1_opy_ import bstack1l11l1111ll_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack1ll1lll1l_opy_, bstack1ll1l1lll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1l1ll1l1l_opy_(bstack1l11l1111ll_opy_):
    bstack11lll111l11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᙂ")
    bstack1l1111ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᙃ")
    bstack11lllllll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᙄ")
    bstack11ll1ll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᙅ")
    bstack11lll11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᙆ")
    bstack11lllll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᙇ")
    bstack11lll11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᙈ")
    bstack11lll11l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᙉ")
    def __init__(self):
        super().__init__(bstack1l111lll11l_opy_=self.bstack11lll111l11_opy_, frameworks=[bstack1ll111l1111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11lll11111l_opy_)
        if bstack1111ll11_opy_():
            TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lllll11_opy_)
        else:
            TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11lllll11_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lll111111_opy_ = self.bstack11lll111l1l_opy_(instance.context)
        if not bstack11lll111111_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᙊ") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᙋ"))
            return
        f.bstack1lll1111ll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack1l1111ll1l1_opy_, bstack11lll111111_opy_)
    def bstack11lll111l1l_opy_(self, context: bstack1ll11l1l1l1_opy_, bstack11ll1lll11l_opy_= True):
        if bstack11ll1lll11l_opy_:
            bstack11lll111111_opy_ = self.bstack1l11l1111l1_opy_(context, reverse=True)
        else:
            bstack11lll111111_opy_ = self.bstack1l111llll11_opy_(context, reverse=True)
        return [f for f in bstack11lll111111_opy_ if f[1].state != bstack11lll111_opy_.QUIT]
    def bstack1l11lllll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if not bstack11lll11l1_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙌ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᙍ"))
            return
        bstack11lll111111_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll111111_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᙎ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᙏ"))
            return
        if len(bstack11lll111111_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᙐ"))
        bstack11ll1lll1l1_opy_, bstack11llll11l1l_opy_ = bstack11lll111111_opy_[0]
        page = bstack11ll1lll1l1_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᙑ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥᙒ"))
            return
        bstack1l1l1l11_opy_ = getattr(args[0], bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᙓ"), None) or getattr(args[0], bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᙔ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᙕ")).get(bstack1ll1lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᙖ")):
            try:
                page.evaluate(bstack1ll1lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᙗ"),
                            bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᙘ") + json.dumps(
                                bstack1l1l1l11_opy_) + bstack1ll1lll_opy_ (u"ࠤࢀࢁࠧᙙ"))
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᙚ"), e)
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if not bstack11lll11l1_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙛ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠧࠨᙜ"))
            return
        bstack11lll111111_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll111111_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙝ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᙞ"))
            return
        if len(bstack11lll111111_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᙟ"))
        bstack11ll1lll1l1_opy_, bstack11llll11l1l_opy_ = bstack11lll111111_opy_[0]
        page = bstack11ll1lll1l1_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙠ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᙡ"))
            return
        status = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11lll1111ll_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᙢ") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠧࠨᙣ"))
            return
        bstack11lll1111l1_opy_ = {bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᙤ"): status.lower()}
        bstack11lll111ll1_opy_ = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11ll1llll11_opy_, None)
        if status.lower() == bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᙥ") and bstack11lll111ll1_opy_ is not None:
            bstack11lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᙦ")] = bstack11lll111ll1_opy_[0][bstack1ll1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᙧ")][0] if isinstance(bstack11lll111ll1_opy_, list) else str(bstack11lll111ll1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᙨ")).get(bstack1ll1lll_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᙩ")):
            try:
                page.evaluate(
                        bstack1ll1lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᙪ"),
                        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࠫᙫ")
                        + json.dumps(bstack11lll1111l1_opy_)
                        + bstack1ll1lll_opy_ (u"ࠢࡾࠤᙬ")
                    )
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣ᙭"), e)
    def bstack1l1111l11ll_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        f: TestFramework,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if not bstack11lll11l1_opy_:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥ᙮"))
            return
        bstack11lll111111_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll111111_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙯ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᙰ"))
            return
        if len(bstack11lll111111_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᙱ"))
        bstack11ll1lll1l1_opy_, bstack11llll11l1l_opy_ = bstack11lll111111_opy_[0]
        page = bstack11ll1lll1l1_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙲ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᙳ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll1lll_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨᙴ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll1lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᙵ"),
                bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᙶ").format(
                    json.dumps(
                        {
                            bstack1ll1lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᙷ"): bstack1ll1lll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢᙸ"),
                            bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᙹ"): {
                                bstack1ll1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧᙺ"): bstack1ll1lll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧᙻ"),
                                bstack1ll1lll_opy_ (u"ࠤࡧࡥࡹࡧࠢᙼ"): data,
                                bstack1ll1lll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᙽ"): bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᙾ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡱ࠴࠵ࡾࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࢀࢃࠢᙿ"), e)
    def bstack1l1111l1l11_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        f: TestFramework,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if f.bstack1ll1l11llll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack11lllll1ll1_opy_, False):
            return
        self.bstack1l11l1l111l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1ll1lll_opy_ (u"ࠨࠢ "))
        req.platform_index = int(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, 0) or 0)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᚁ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll1l111_opy_, bstack1ll1lll_opy_ (u"ࠣࠤᚂ")) or bstack1ll1lll_opy_ (u"ࠤࠥᚃ"))
        req.test_framework_version = str(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11111111l_opy_, bstack1ll1lll_opy_ (u"ࠥࠦᚄ")) or bstack1ll1lll_opy_ (u"ࠦࠧᚅ"))
        req.test_framework_state = str(bstack1ll11l1l111_opy_[0].name)
        req.test_hook_state = str(bstack1ll11l1l111_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, bstack1ll1lll_opy_ (u"ࠧࠨᚆ")) or bstack1ll1lll_opy_ (u"ࠨࠢᚇ"))
        current_test_id = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11ll1lll111_opy_, None)
        bstack11ll1ll1lll_opy_ = 0
        bstack11lll11l111_opy_ = 0
        for bstack11lll111lll_opy_ in bstack111l111ll_opy_.bstack1111l1ll1l_opy_.values():
            session_id = bstack111l111ll_opy_.bstack1ll1l11llll_opy_(
                bstack11lll111lll_opy_,
                bstack111l111ll_opy_.bstack1ll1ll111ll_opy_,
                bstack1ll1lll_opy_ (u"ࠢࠣᚈ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack111l111ll_opy_.bstack1ll1l11llll_opy_(bstack11lll111lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡩࡥࠩᚉ"), None)
                if instance_test_id != current_test_id:
                    bstack11lll11l111_opy_ += 1
                    continue
                if not session_id:
                    bstack11lll11l111_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣᚊ")
                if bstack11lll11l1_opy_
                else bstack1ll1lll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤᚋ")
            )
            session.ref = str(bstack11lll111lll_opy_.ref() or bstack1ll1lll_opy_ (u"ࠦࠧᚌ"))
            session.hub_url = str(bstack111l111ll_opy_.bstack1ll1l11llll_opy_(
                bstack11lll111lll_opy_,
                bstack111l111ll_opy_.bstack1lll111l_opy_,
                bstack1ll1lll_opy_ (u"ࠧࠨᚍ")
            ) or bstack1ll1lll_opy_ (u"ࠨࠢᚎ"))
            session.framework_name = str(bstack11lll111lll_opy_.framework_name or bstack1ll1lll_opy_ (u"ࠢࠣᚏ"))
            session.framework_version = str(bstack11lll111lll_opy_.framework_version or bstack1ll1lll_opy_ (u"ࠣࠤᚐ"))
            session.framework_session_id = str(session_id)
            bstack11ll1ll1lll_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll111111_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll111111_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᚑ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᚒ"))
            return
        if len(bstack11lll111111_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᚓ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠧࠨᚔ"))
        bstack11ll1lll1l1_opy_, bstack11llll11l1l_opy_ = bstack11lll111111_opy_[0]
        page = bstack11ll1lll1l1_opy_()
        if not page:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᚕ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᚖ"))
            return
        return page
    def bstack1l11ll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11ll1lllll1_opy_ = {}
        for bstack11lll111lll_opy_ in bstack111l111ll_opy_.bstack1111l1ll1l_opy_.values():
            caps = bstack111l111ll_opy_.bstack1ll1l11llll_opy_(bstack11lll111lll_opy_, bstack111l111ll_opy_.bstack11l11l11_opy_, {})
        bstack11ll1lllll1_opy_[bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨᚗ")] = caps.get(bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥᚘ"), bstack1ll1lll_opy_ (u"ࠥࠦᚙ"))
        bstack11ll1lllll1_opy_[bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᚚ")] = caps.get(bstack1ll1lll_opy_ (u"ࠧࡵࡳࠣ᚛"), bstack1ll1lll_opy_ (u"ࠨࠢ᚜"))
        bstack11ll1lllll1_opy_[bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ᚝")] = caps.get(bstack1ll1lll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᚞"), bstack1ll1lll_opy_ (u"ࠤࠥ᚟"))
        bstack11ll1lllll1_opy_[bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦᚠ")] = caps.get(bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᚡ"), bstack1ll1lll_opy_ (u"ࠧࠨᚢ"))
        try:
            bstack11111lll_opy_ = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11111lll_opy_, int):
                bstack11111lll_opy_ = 0
            bstack111l11l111_opy_ = self.config.get(bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᚣ"), [])
            bstack11ll1llll1l_opy_ = bstack111l11l111_opy_[bstack11111lll_opy_] if bstack11111lll_opy_ < len(bstack111l11l111_opy_) else self.config
            bstack11ll1llllll_opy_ = (
                bstack11ll1llll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚤ"))
                or bstack11ll1llll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚥ"))
                or self.config.get(bstack1ll1lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚦ"))
                or self.config.get(bstack1ll1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚧ"))
            )
            if bstack11ll1llllll_opy_:
                bstack11ll1lllll1_opy_[bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚨ")] = bstack11ll1llllll_opy_
        except Exception as ex:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡢࡶࡷࡥࡨ࡮ࠠࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᚩ") + str(ex) + bstack1ll1lll_opy_ (u"ࠨࠢᚪ"))
        return bstack11ll1lllll1_opy_
    def bstack1l11ll1ll1l_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack1ll1lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᚫ"), bstack1ll1lll_opy_ (u"ࠣࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠣᚬ"))
            if is_robot_playwright_installed():
                bstack11ll1lll1ll_opy_ = script_code.replace(bstack1ll1lll_opy_ (u"ࠤࡺ࡭ࡳࡪ࡯ࡸ࠰ࠥᚭ"), bstack1ll1lll_opy_ (u"ࠥ࡫ࡱࡵࡢࡢ࡮ࡗ࡬࡮ࡹ࠮ࠣᚮ"))
                bstack11ll1lll1ll_opy_ = bstack11ll1lll1ll_opy_.replace(bstack1ll1lll_opy_ (u"ࠦࡼ࡯࡮ࡥࡱࡺ࡟ࠧᚯ"), bstack1ll1lll_opy_ (u"ࠧ࡭࡬ࡰࡤࡤࡰ࡙࡮ࡩࡴ࡝ࠥᚰ"))
                bstack11lll11ll11_opy_ = bstack1ll1lll_opy_ (u"ࠨࠢࠣࡨࡸࡲࡨࡺࡩࡰࡰࠣࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࠨࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡹࡥࡷࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠦ࠽ࠡ࡝ࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂࡣ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࡪࡺࡴࡣࡵ࡫ࡲࡲ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡼࡨࡱࡣࡧࡵࡤࡺࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠣࠤࠥᚱ").format(fn_body=bstack11ll1lll1ll_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1ll1lll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡇࡹࡥࡱࡻࡡࡵࡧࠣࡎࡦࡼࡡࡔࡥࡵ࡭ࡵࡺࠧᚲ"),
                    None,
                    bstack11lll11ll11_opy_
                )
            else:
                script_template = bstack1ll1lll_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡼࡨࡱࡣࡧࡵࡤࡺࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᚳ")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺ࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡈࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠣᚴ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᚵ"))