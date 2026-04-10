# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
    bstack1l1ll11ll11_opy_,
    bstack1l1ll1llll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lll1ll1ll_opy_, bstack11lll11ll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11ll1llll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111lll11ll_opy_ import bstack11ll1l111l_opy_
from browserstack_sdk.sdk_cli.bstack11llll11111_opy_ import bstack11llll11lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack111l1l1l1l_opy_ import bstack1l1lll1lll_opy_, bstack1l111l1l1l_opy_, bstack11lllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1l111lll1_opy_(bstack11llll11lll_opy_):
    bstack11l1l1llll1_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦញ")
    bstack11ll11l1111_opy_ = bstack1ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧដ")
    bstack11ll111ll1l_opy_ = bstack1ll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤឋ")
    bstack11l1l1lll11_opy_ = bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣឌ")
    bstack11l1l1lllll_opy_ = bstack1ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨឍ")
    bstack11ll11lll11_opy_ = bstack1ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤណ")
    bstack11l1ll1l111_opy_ = bstack1ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢត")
    bstack11l1l1ll1ll_opy_ = bstack1ll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥថ")
    def __init__(self):
        super().__init__(bstack11llll11ll1_opy_=self.bstack11l1l1llll1_opy_, frameworks=[bstack1l11ll1llll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l1l1lll1l_opy_)
        if bstack11lll11ll_opy_():
            TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111lll11_opy_)
        else:
            TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111lll11_opy_)
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1l1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1ll11ll1_opy_ = self.bstack11l1ll1l1l1_opy_(instance.context)
        if not bstack11l1ll11ll1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦទ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠢࠣធ"))
            return
        f.bstack1l1l1l1l_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11l1111_opy_, bstack11l1ll11ll1_opy_)
    def bstack11l1ll1l1l1_opy_(self, context: bstack1l1ll1llll1_opy_, bstack11l1ll11l1l_opy_= True):
        if bstack11l1ll11l1l_opy_:
            bstack11l1ll11ll1_opy_ = self.bstack11lll1lll11_opy_(context, reverse=True)
        else:
            bstack11l1ll11ll1_opy_ = self.bstack11lll1lll1l_opy_(context, reverse=True)
        return [f for f in bstack11l1ll11ll1_opy_ if f[1].state != bstack1111ll1l11_opy_.QUIT]
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1lll1l_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if not bstack1lll1ll1ll_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦន") + str(kwargs) + bstack1ll_opy_ (u"ࠤࠥប"))
            return
        bstack11l1ll11ll1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11l1111_opy_, [])
        if not bstack11l1ll11ll1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨផ") + str(kwargs) + bstack1ll_opy_ (u"ࠦࠧព"))
            return
        if len(bstack11l1ll11ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢភ"))
        bstack11l1ll1l1ll_opy_, bstack11ll111l1l1_opy_ = bstack11l1ll11ll1_opy_[0]
        page = bstack11l1ll1l1ll_opy_()
        if not page:
            self.logger.debug(bstack1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨម") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣយ"))
            return
        bstack111l11111_opy_ = getattr(args[0], bstack1ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣរ"), None) or getattr(args[0], bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢល"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣវ")).get(bstack1ll_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨឝ")):
            try:
                page.evaluate(bstack1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨឞ"),
                            bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪស") + json.dumps(
                                bstack111l11111_opy_) + bstack1ll_opy_ (u"ࠢࡾࡿࠥហ"))
            except Exception as e:
                self.logger.debug(bstack1ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨឡ"), e)
    def bstack1l1111l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1lll1l_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if not bstack1lll1ll1ll_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧអ") + str(kwargs) + bstack1ll_opy_ (u"ࠥࠦឣ"))
            return
        bstack11l1ll11ll1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11l1111_opy_, [])
        if not bstack11l1ll11ll1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢឤ") + str(kwargs) + bstack1ll_opy_ (u"ࠧࠨឥ"))
            return
        if len(bstack11l1ll11ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣឦ"))
        bstack11l1ll1l1ll_opy_, bstack11ll111l1l1_opy_ = bstack11l1ll11ll1_opy_[0]
        page = bstack11l1ll1l1ll_opy_()
        if not page:
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢឧ") + str(kwargs) + bstack1ll_opy_ (u"ࠣࠤឨ"))
            return
        status = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l1ll11lll_opy_, None)
        if not status:
            self.logger.debug(bstack1ll_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧឩ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠥࠦឪ"))
            return
        bstack11l1ll1l11l_opy_ = {bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦឫ"): status.lower()}
        bstack11l1l1ll111_opy_ = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l1ll11l11_opy_, None)
        if status.lower() == bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬឬ") and bstack11l1l1ll111_opy_ is not None:
            bstack11l1ll1l11l_opy_[bstack1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ឭ")] = bstack11l1l1ll111_opy_[0][bstack1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪឮ")][0] if isinstance(bstack11l1l1ll111_opy_, list) else str(bstack11l1l1ll111_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨឯ")).get(bstack1ll_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨឰ")):
            try:
                page.evaluate(
                        bstack1ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦឱ"),
                        bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩឲ")
                        + json.dumps(bstack11l1ll1l11l_opy_)
                        + bstack1ll_opy_ (u"ࠧࢃࠢឳ")
                    )
            except Exception as e:
                self.logger.debug(bstack1ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ឴"), e)
    def bstack11lll1l1l11_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        f: TestFramework,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1lll1l_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if not bstack1lll1ll1ll_opy_:
            self.logger.debug(
                bstack1l1ll1111l1_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣ឵"))
            return
        bstack11l1ll11ll1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11l1111_opy_, [])
        if not bstack11l1ll11ll1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦា") + str(kwargs) + bstack1ll_opy_ (u"ࠤࠥិ"))
            return
        if len(bstack11l1ll11ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧី"))
        bstack11l1ll1l1ll_opy_, bstack11ll111l1l1_opy_ = bstack11l1ll11ll1_opy_[0]
        page = bstack11l1ll1l1ll_opy_()
        if not page:
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦឹ") + str(kwargs) + bstack1ll_opy_ (u"ࠧࠨឺ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦុ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣូ"),
                bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ួ").format(
                    json.dumps(
                        {
                            bstack1ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤើ"): bstack1ll_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧឿ"),
                            bstack1ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢៀ"): {
                                bstack1ll_opy_ (u"ࠧࡺࡹࡱࡧࠥេ"): bstack1ll_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥែ"),
                                bstack1ll_opy_ (u"ࠢࡥࡣࡷࡥࠧៃ"): data,
                                bstack1ll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢោ"): bstack1ll_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣៅ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧំ"), e)
    def bstack11ll1l1llll_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        f: TestFramework,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1lll1l_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if f.bstack1ll11111l11_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11lll11_opy_, False):
            return
        self.bstack1l111l1ll11_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1ll_opy_ (u"ࠦࠧះ"))
        req.platform_index = int(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111l11l1_opy_, 0) or 0)
        req.client_worker_id = bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦៈ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l11111111l_opy_, bstack1ll_opy_ (u"ࠨࠢ៉")) or bstack1ll_opy_ (u"ࠢࠣ៊"))
        req.test_framework_version = str(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack11ll11l11ll_opy_, bstack1ll_opy_ (u"ࠣࠤ់")) or bstack1ll_opy_ (u"ࠤࠥ៌"))
        req.test_framework_state = str(bstack1l1ll1lll11_opy_[0].name)
        req.test_hook_state = str(bstack1l1ll1lll11_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, bstack1ll_opy_ (u"ࠥࠦ៍")) or bstack1ll_opy_ (u"ࠦࠧ៎"))
        current_test_id = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l1ll11111_opy_, None)
        bstack11l1l1ll1l1_opy_ = 0
        bstack11l1ll111l1_opy_ = 0
        for bstack11l1ll1ll11_opy_ in bstack11ll1l111l_opy_.bstack1l111l11l_opy_.values():
            session_id = bstack11ll1l111l_opy_.bstack1ll11111l11_opy_(
                bstack11l1ll1ll11_opy_,
                bstack11ll1l111l_opy_.bstack1l1lllll11l_opy_,
                bstack1ll_opy_ (u"ࠧࠨ៏")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack11ll1l111l_opy_.bstack1ll11111l11_opy_(bstack11l1ll1ll11_opy_, bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧ័"), None)
                if instance_test_id != current_test_id:
                    bstack11l1ll111l1_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1ll111l1_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨ៑")
                if bstack1lll1ll1ll_opy_
                else bstack1ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪ្ࠢ")
            )
            session.ref = str(bstack11l1ll1ll11_opy_.ref() or bstack1ll_opy_ (u"ࠤࠥ៓"))
            session.hub_url = str(bstack11ll1l111l_opy_.bstack1ll11111l11_opy_(
                bstack11l1ll1ll11_opy_,
                bstack11ll1l111l_opy_.bstack11llll1l11_opy_,
                bstack1ll_opy_ (u"ࠥࠦ។")
            ) or bstack1ll_opy_ (u"ࠦࠧ៕"))
            session.framework_name = str(bstack11l1ll1ll11_opy_.framework_name or bstack1ll_opy_ (u"ࠧࠨ៖"))
            session.framework_version = str(bstack11l1ll1ll11_opy_.framework_version or bstack1ll_opy_ (u"ࠨࠢៗ"))
            session.framework_session_id = str(session_id)
            bstack11l1l1ll1l1_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l111l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1ll11ll1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l111lll1_opy_.bstack11ll11l1111_opy_, [])
        if not bstack11l1ll11ll1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ៘") + str(kwargs) + bstack1ll_opy_ (u"ࠣࠤ៙"))
            return
        if len(bstack11l1ll11ll1_opy_) > 1:
            self.logger.debug(bstack1ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ៚") + str(kwargs) + bstack1ll_opy_ (u"ࠥࠦ៛"))
        bstack11l1ll1l1ll_opy_, bstack11ll111l1l1_opy_ = bstack11l1ll11ll1_opy_[0]
        page = bstack11l1ll1l1ll_opy_()
        if not page:
            self.logger.debug(bstack1ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦៜ") + str(kwargs) + bstack1ll_opy_ (u"ࠧࠨ៝"))
            return
        return page
    def bstack11lllll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l1ll1111l_opy_ = {}
        for bstack11l1ll1ll11_opy_ in bstack11ll1l111l_opy_.bstack1l111l11l_opy_.values():
            caps = bstack11ll1l111l_opy_.bstack1ll11111l11_opy_(bstack11l1ll1ll11_opy_, bstack11ll1l111l_opy_.bstack11l1111l1l_opy_, {})
        bstack11l1ll1111l_opy_[bstack1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ៞")] = caps.get(bstack1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ៟"), bstack1ll_opy_ (u"ࠣࠤ០"))
        bstack11l1ll1111l_opy_[bstack1ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ១")] = caps.get(bstack1ll_opy_ (u"ࠥࡳࡸࠨ២"), bstack1ll_opy_ (u"ࠦࠧ៣"))
        bstack11l1ll1111l_opy_[bstack1ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ៤")] = caps.get(bstack1ll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ៥"), bstack1ll_opy_ (u"ࠢࠣ៦"))
        bstack11l1ll1111l_opy_[bstack1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ៧")] = caps.get(bstack1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ៨"), bstack1ll_opy_ (u"ࠥࠦ៩"))
        try:
            bstack11l11ll1_opy_ = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111l11l1_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11l11ll1_opy_, int):
                bstack11l11ll1_opy_ = 0
            bstack1lll1lll1_opy_ = self.config.get(bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ៪"), [])
            bstack11l1l1l1lll_opy_ = bstack1lll1lll1_opy_[bstack11l11ll1_opy_] if bstack11l11ll1_opy_ < len(bstack1lll1lll1_opy_) else self.config
            bstack1lll1111lll_opy_ = (
                bstack11l1l1l1lll_opy_.get(bstack1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៫"))
                or bstack11l1l1l1lll_opy_.get(bstack1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭៬"))
                or self.config.get(bstack1ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៭"))
                or self.config.get(bstack1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៮"))
            )
            if bstack1lll1111lll_opy_:
                bstack11l1ll1111l_opy_[bstack1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៯")] = bstack1lll1111lll_opy_
        except Exception as ex:
            self.logger.debug(bstack1ll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡧࡴࡵࡣࡦ࡬ࠥࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ࠿ࠦࠢ៰") + str(ex) + bstack1ll_opy_ (u"ࠦࠧ៱"))
        return bstack11l1ll1111l_opy_
    def bstack1l1111l1l1l_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack1ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ៲"), bstack1ll_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨ៳"))
            if is_robot_playwright_installed():
                bstack11l1l1ll11l_opy_ = script_code.replace(bstack1ll_opy_ (u"ࠢࡸ࡫ࡱࡨࡴࡽ࠮ࠣ៴"), bstack1ll_opy_ (u"ࠣࡩ࡯ࡳࡧࡧ࡬ࡕࡪ࡬ࡷ࠳ࠨ៵"))
                bstack11l1l1ll11l_opy_ = bstack11l1l1ll11l_opy_.replace(bstack1ll_opy_ (u"ࠤࡺ࡭ࡳࡪ࡯ࡸ࡝ࠥ៶"), bstack1ll_opy_ (u"ࠥ࡫ࡱࡵࡢࡢ࡮ࡗ࡬࡮ࡹ࡛ࠣ៷"))
                bstack11l1ll111ll_opy_ = bstack1ll_opy_ (u"ࠦࠧࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽ࠭࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡷࡣࡵࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠤࡂ࡛ࠦࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂࠨࠢࠣ៸").format(fn_body=bstack11l1l1ll11l_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡅࡷࡣ࡯ࡹࡦࡺࡥࠡࡌࡤࡺࡦ࡙ࡣࡳ࡫ࡳࡸࠬ៹"),
                    None,
                    bstack11l1ll111ll_opy_
                )
            else:
                script_template = bstack1ll_opy_ (u"ࠨࠢࠣࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࠴࠮࠯ࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦ៺")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨ៻") + str(e) + bstack1ll_opy_ (u"ࠣࠤ៼"))