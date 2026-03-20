# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1ll11llllll_opy_,
    bstack1ll11lll1ll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack11l1111l1l_opy_, bstack1ll11lll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l111lllll1_opy_ import bstack1l11l111111_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack11111l11_opy_, bstack1ll11ll1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1ll1ll11l_opy_(bstack1l11l111111_opy_):
    bstack11lll1l1l1l_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᘧ")
    bstack11llllll11l_opy_ = bstack11lll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᘨ")
    bstack1l1111ll11l_opy_ = bstack11lll1_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᘩ")
    bstack11lll11l111_opy_ = bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᘪ")
    bstack11lll111l11_opy_ = bstack11lll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᘫ")
    bstack1l1111111ll_opy_ = bstack11lll1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᘬ")
    bstack11lll111l1l_opy_ = bstack11lll1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᘭ")
    bstack11lll1111ll_opy_ = bstack11lll1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᘮ")
    def __init__(self):
        super().__init__(bstack1l11l1111ll_opy_=self.bstack11lll1l1l1l_opy_, frameworks=[bstack1ll111l11ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11lll11llll_opy_)
        if bstack1ll11lll_opy_():
            TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l111111l_opy_)
        else:
            TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l111111l_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll11llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lll11l11l_opy_ = self.bstack11lll1l11l1_opy_(instance.context)
        if not bstack11lll11l11l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᘯ") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠥࠦᘰ"))
            return
        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll1ll11l_opy_.bstack11llllll11l_opy_, bstack11lll11l11l_opy_)
    def bstack11lll1l11l1_opy_(self, context: bstack1ll11lll1ll_opy_, bstack11lll11l1ll_opy_= True):
        if bstack11lll11l1ll_opy_:
            bstack11lll11l11l_opy_ = self.bstack1l11l111l11_opy_(context, reverse=True)
        else:
            bstack11lll11l11l_opy_ = self.bstack1l11l11l1ll_opy_(context, reverse=True)
        return [f for f in bstack11lll11l11l_opy_ if f[1].state != bstack111ll1lll1_opy_.QUIT]
    def bstack1l1l111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11llll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if not bstack11l1111l1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᘱ") + str(kwargs) + bstack11lll1_opy_ (u"ࠧࠨᘲ"))
            return
        bstack11lll11l11l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1ll11l_opy_.bstack11llllll11l_opy_, [])
        if not bstack11lll11l11l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᘳ") + str(kwargs) + bstack11lll1_opy_ (u"ࠢࠣᘴ"))
            return
        if len(bstack11lll11l11l_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᘵ"))
        bstack11lll1l111l_opy_, bstack11lllll111l_opy_ = bstack11lll11l11l_opy_[0]
        page = bstack11lll1l111l_opy_()
        if not page:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᘶ") + str(kwargs) + bstack11lll1_opy_ (u"ࠥࠦᘷ"))
            return
        bstack1l11ll11l_opy_ = getattr(args[0], bstack11lll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᘸ"), None) or getattr(args[0], bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᘹ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᘺ")).get(bstack11lll1_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᘻ")):
            try:
                page.evaluate(bstack11lll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᘼ"),
                            bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᘽ") + json.dumps(
                                bstack1l11ll11l_opy_) + bstack11lll1_opy_ (u"ࠥࢁࢂࠨᘾ"))
            except Exception as e:
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᘿ"), e)
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11llll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if not bstack11l1111l1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᙀ") + str(kwargs) + bstack11lll1_opy_ (u"ࠨࠢᙁ"))
            return
        bstack11lll11l11l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1ll11l_opy_.bstack11llllll11l_opy_, [])
        if not bstack11lll11l11l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙂ") + str(kwargs) + bstack11lll1_opy_ (u"ࠣࠤᙃ"))
            return
        if len(bstack11lll11l11l_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᙄ"))
        bstack11lll1l111l_opy_, bstack11lllll111l_opy_ = bstack11lll11l11l_opy_[0]
        page = bstack11lll1l111l_opy_()
        if not page:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙅ") + str(kwargs) + bstack11lll1_opy_ (u"ࠦࠧᙆ"))
            return
        status = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11lll11111l_opy_, None)
        if not status:
            self.logger.debug(bstack11lll1_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᙇ") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠨࠢᙈ"))
            return
        bstack11lll1l1ll1_opy_ = {bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᙉ"): status.lower()}
        bstack11lll1l1lll_opy_ = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11lll1l1111_opy_, None)
        if status.lower() == bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᙊ") and bstack11lll1l1lll_opy_ is not None:
            bstack11lll1l1ll1_opy_[bstack11lll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᙋ")] = bstack11lll1l1lll_opy_[0][bstack11lll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᙌ")][0] if isinstance(bstack11lll1l1lll_opy_, list) else str(bstack11lll1l1lll_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᙍ")).get(bstack11lll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᙎ")):
            try:
                page.evaluate(
                        bstack11lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᙏ"),
                        bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬᙐ")
                        + json.dumps(bstack11lll1l1ll1_opy_)
                        + bstack11lll1_opy_ (u"ࠣࡿࠥᙑ")
                    )
            except Exception as e:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᙒ"), e)
    def bstack1l111lll11l_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        f: TestFramework,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11llll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if not bstack11l1111l1l_opy_:
            self.logger.debug(
                bstack1ll11ll1ll1_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᙓ"))
            return
        bstack11lll11l11l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1ll11l_opy_.bstack11llllll11l_opy_, [])
        if not bstack11lll11l11l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙔ") + str(kwargs) + bstack11lll1_opy_ (u"ࠧࠨᙕ"))
            return
        if len(bstack11lll11l11l_opy_) > 1:
            self.logger.debug(
                bstack1ll11ll1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᙖ"))
        bstack11lll1l111l_opy_, bstack11lllll111l_opy_ = bstack11lll11l11l_opy_[0]
        page = bstack11lll1l111l_opy_()
        if not page:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙗ") + str(kwargs) + bstack11lll1_opy_ (u"ࠣࠤᙘ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11lll1_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᙙ") + str(timestamp)
        try:
            page.evaluate(
                bstack11lll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᙚ"),
                bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᙛ").format(
                    json.dumps(
                        {
                            bstack11lll1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᙜ"): bstack11lll1_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᙝ"),
                            bstack11lll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᙞ"): {
                                bstack11lll1_opy_ (u"ࠣࡶࡼࡴࡪࠨᙟ"): bstack11lll1_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᙠ"),
                                bstack11lll1_opy_ (u"ࠥࡨࡦࡺࡡࠣᙡ"): data,
                                bstack11lll1_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᙢ"): bstack11lll1_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᙣ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣᙤ"), e)
    def bstack1l111lll1ll_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        f: TestFramework,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11llll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1ll11l_opy_.bstack1l1111111ll_opy_, False):
            return
        self.bstack1l1l1111l1l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack11lll1_opy_ (u"ࠢࠣᙥ"))
        req.platform_index = int(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll1ll1_opy_, 0) or 0)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᙦ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll111l_opy_, bstack11lll1_opy_ (u"ࠤࠥᙧ")) or bstack11lll1_opy_ (u"ࠥࠦᙨ"))
        req.test_framework_version = str(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l111l11lll_opy_, bstack11lll1_opy_ (u"ࠦࠧᙩ")) or bstack11lll1_opy_ (u"ࠧࠨᙪ"))
        req.test_framework_state = str(bstack1ll1l111111_opy_[0].name)
        req.test_hook_state = str(bstack1ll1l111111_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_, bstack11lll1_opy_ (u"ࠨࠢᙫ")) or bstack11lll1_opy_ (u"ࠢࠣᙬ"))
        current_test_id = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11lll111lll_opy_, None)
        bstack11lll11l1l1_opy_ = 0
        bstack11lll1l1l11_opy_ = 0
        for bstack11lll1111l1_opy_ in bstack1l1l11ll1l_opy_.bstack11l1lll111_opy_.values():
            session_id = bstack1l1l11ll1l_opy_.bstack1ll1l1l1111_opy_(
                bstack11lll1111l1_opy_,
                bstack1l1l11ll1l_opy_.bstack1ll1ll1ll1l_opy_,
                bstack11lll1_opy_ (u"ࠣࠤ᙭")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1l1l11ll1l_opy_.bstack1ll1l1l1111_opy_(bstack11lll1111l1_opy_, bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪ᙮"), None)
                if instance_test_id != current_test_id:
                    bstack11lll1l1l11_opy_ += 1
                    continue
                if not session_id:
                    bstack11lll1l1l11_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack11lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᙯ")
                if bstack11l1111l1l_opy_
                else bstack11lll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᙰ")
            )
            session.ref = str(bstack11lll1111l1_opy_.ref() or bstack11lll1_opy_ (u"ࠧࠨᙱ"))
            session.hub_url = str(bstack1l1l11ll1l_opy_.bstack1ll1l1l1111_opy_(
                bstack11lll1111l1_opy_,
                bstack1l1l11ll1l_opy_.bstack11l1111lll_opy_,
                bstack11lll1_opy_ (u"ࠨࠢᙲ")
            ) or bstack11lll1_opy_ (u"ࠢࠣᙳ"))
            session.framework_name = str(bstack11lll1111l1_opy_.framework_name or bstack11lll1_opy_ (u"ࠣࠤᙴ"))
            session.framework_version = str(bstack11lll1111l1_opy_.framework_version or bstack11lll1_opy_ (u"ࠤࠥᙵ"))
            session.framework_session_id = str(session_id)
            bstack11lll11l1l1_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l11l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll11l11l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1ll11l_opy_.bstack11llllll11l_opy_, [])
        if not bstack11lll11l11l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙶ") + str(kwargs) + bstack11lll1_opy_ (u"ࠦࠧᙷ"))
            return
        if len(bstack11lll11l11l_opy_) > 1:
            self.logger.debug(bstack11lll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙸ") + str(kwargs) + bstack11lll1_opy_ (u"ࠨࠢᙹ"))
        bstack11lll1l111l_opy_, bstack11lllll111l_opy_ = bstack11lll11l11l_opy_[0]
        page = bstack11lll1l111l_opy_()
        if not page:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙺ") + str(kwargs) + bstack11lll1_opy_ (u"ࠣࠤᙻ"))
            return
        return page
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11lll11lll1_opy_ = {}
        for bstack11lll1111l1_opy_ in bstack1l1l11ll1l_opy_.bstack11l1lll111_opy_.values():
            caps = bstack1l1l11ll1l_opy_.bstack1ll1l1l1111_opy_(bstack11lll1111l1_opy_, bstack1l1l11ll1l_opy_.bstack1l1l111l11_opy_, {})
        bstack11lll11lll1_opy_[bstack11lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᙼ")] = caps.get(bstack11lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᙽ"), bstack11lll1_opy_ (u"ࠦࠧᙾ"))
        bstack11lll11lll1_opy_[bstack11lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᙿ")] = caps.get(bstack11lll1_opy_ (u"ࠨ࡯ࡴࠤ "), bstack11lll1_opy_ (u"ࠢࠣᚁ"))
        bstack11lll11lll1_opy_[bstack11lll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᚂ")] = caps.get(bstack11lll1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᚃ"), bstack11lll1_opy_ (u"ࠥࠦᚄ"))
        bstack11lll11lll1_opy_[bstack11lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᚅ")] = caps.get(bstack11lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᚆ"), bstack11lll1_opy_ (u"ࠨࠢᚇ"))
        try:
            bstack11l111lll1_opy_ = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll1ll1_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11l111lll1_opy_, int):
                bstack11l111lll1_opy_ = 0
            bstack11l1l1ll11_opy_ = self.config.get(bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᚈ"), [])
            bstack11lll11ll11_opy_ = bstack11l1l1ll11_opy_[bstack11l111lll1_opy_] if bstack11l111lll1_opy_ < len(bstack11l1l1ll11_opy_) else self.config
            bstack11lll1l11ll_opy_ = (
                bstack11lll11ll11_opy_.get(bstack11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚉ"))
                or bstack11lll11ll11_opy_.get(bstack11lll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚊ"))
                or self.config.get(bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚋ"))
                or self.config.get(bstack11lll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚌ"))
            )
            if bstack11lll1l11ll_opy_:
                bstack11lll11lll1_opy_[bstack11lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚍ")] = bstack11lll1l11ll_opy_
        except Exception as ex:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡣࡷࡸࡦࡩࡨࠡࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠥᚎ") + str(ex) + bstack11lll1_opy_ (u"ࠢࠣᚏ"))
        return bstack11lll11lll1_opy_
    def bstack1l1l11ll1l1_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack11lll1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᚐ"), bstack11lll1_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᚑ"))
            if is_robot_playwright_installed():
                bstack11lll111ll1_opy_ = script_code.replace(bstack11lll1_opy_ (u"ࠥࡻ࡮ࡴࡤࡰࡹ࠱ࠦᚒ"), bstack11lll1_opy_ (u"ࠦ࡬ࡲ࡯ࡣࡣ࡯ࡘ࡭࡯ࡳ࠯ࠤᚓ"))
                bstack11lll111ll1_opy_ = bstack11lll111ll1_opy_.replace(bstack11lll1_opy_ (u"ࠧࡽࡩ࡯ࡦࡲࡻࡠࠨᚔ"), bstack11lll1_opy_ (u"ࠨࡧ࡭ࡱࡥࡥࡱ࡚ࡨࡪࡵ࡞ࠦᚕ"))
                bstack11lll11ll1l_opy_ = bstack11lll1_opy_ (u"ࠢࠣࠤࡩࡹࡳࡩࡴࡪࡱࡱࠤࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࠩࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡺࡦࡸࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠠ࠾ࠢ࡞ࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃ࡝࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠤࠥࠦᚖ").format(fn_body=bstack11lll111ll1_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack11lll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳ࠰ࡈࡺࡦࡲࡵࡢࡶࡨࠤࡏࡧࡶࡢࡕࡦࡶ࡮ࡶࡴࠨᚗ"),
                    None,
                    bstack11lll11ll1l_opy_
                )
            else:
                script_template = bstack11lll1_opy_ (u"ࠤࠥࠦ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩ࠰࠱࠲ࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠲ࡵࡻࡳࡩࠪࡵࡩࡸࡵ࡬ࡷࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢᚘ")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᚙ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᚚ"))