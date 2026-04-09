# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1l1lll111ll_opy_,
    bstack1l1ll1l1l1l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1ll1l_opy_, bstack1lll1l111_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll1_opy_ import bstack1111l11l1l_opy_
from browserstack_sdk.sdk_cli.bstack11lll1ll1l1_opy_ import bstack11lll1lll1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11ll11ll11_opy_ import bstack1l1l1l11l_opy_, bstack111ll1l1_opy_, bstack11l1l11lll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l11l11llll_opy_(bstack11lll1lll1l_opy_):
    bstack11l1ll11lll_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣឆ")
    bstack11ll1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤជ")
    bstack11lll1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨឈ")
    bstack11l1ll1l1ll_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧញ")
    bstack11l1ll111ll_opy_ = bstack11ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥដ")
    bstack11lll11l11l_opy_ = bstack11ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨឋ")
    bstack11l1ll1ll1l_opy_ = bstack11ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦឌ")
    bstack11l1ll11ll1_opy_ = bstack11ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢឍ")
    def __init__(self):
        super().__init__(bstack11llll11ll1_opy_=self.bstack11l1ll11lll_opy_, frameworks=[bstack1l1l1ll11ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l1lll1111_opy_)
        if bstack1lll1l111_opy_():
            TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111lll11_opy_)
        else:
            TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111lll11_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1lll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1ll1l111_opy_ = self.bstack11l1ll11l1l_opy_(instance.context)
        if not bstack11l1ll1l111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣណ") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠦࠧត"))
            return
        f.bstack1l1l1111l1_opy_(instance, bstack1l11l11llll_opy_.bstack11ll1l1l11l_opy_, bstack11l1ll1l111_opy_)
    def bstack11l1ll11l1l_opy_(self, context: bstack1l1ll1l1l1l_opy_, bstack11l1ll1l11l_opy_= True):
        if bstack11l1ll1l11l_opy_:
            bstack11l1ll1l111_opy_ = self.bstack11llll11l1l_opy_(context, reverse=True)
        else:
            bstack11l1ll1l111_opy_ = self.bstack11lll1lll11_opy_(context, reverse=True)
        return [f for f in bstack11l1ll1l111_opy_ if f[1].state != bstack11111l1ll_opy_.QUIT]
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1lll1111_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣថ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢទ"))
            return
        bstack11l1ll1l111_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l11l11llll_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11l1ll1l111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥធ") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤន"))
            return
        if len(bstack11l1ll1l111_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1lll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦប"))
        bstack11l1ll111l1_opy_, bstack11ll1111ll1_opy_ = bstack11l1ll1l111_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥផ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧព"))
            return
        bstack1l111l1111_opy_ = getattr(args[0], bstack11ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧភ"), None) or getattr(args[0], bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦម"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧយ")).get(bstack11ll11_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥរ")):
            try:
                page.evaluate(bstack11ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥល"),
                            bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧវ") + json.dumps(
                                bstack1l111l1111_opy_) + bstack11ll11_opy_ (u"ࠦࢂࢃࠢឝ"))
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥឞ"), e)
    def bstack1l1111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1lll1111_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤស") + str(kwargs) + bstack11ll11_opy_ (u"ࠢࠣហ"))
            return
        bstack11l1ll1l111_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l11l11llll_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11l1ll1l111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦឡ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥអ"))
            return
        if len(bstack11l1ll1l111_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1lll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧឣ"))
        bstack11l1ll111l1_opy_, bstack11ll1111ll1_opy_ = bstack11l1ll1l111_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦឤ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨឥ"))
            return
        status = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1l1lll1l_opy_, None)
        if not status:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤឦ") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠢࠣឧ"))
            return
        bstack11l1ll1l1l1_opy_ = {bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣឨ"): status.lower()}
        bstack11l1ll1ll11_opy_ = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1ll1lll1_opy_, None)
        if status.lower() == bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩឩ") and bstack11l1ll1ll11_opy_ is not None:
            bstack11l1ll1l1l1_opy_[bstack11ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪឪ")] = bstack11l1ll1ll11_opy_[0][bstack11ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧឫ")][0] if isinstance(bstack11l1ll1ll11_opy_, list) else str(bstack11l1ll1ll11_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥឬ")).get(bstack11ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥឭ")):
            try:
                page.evaluate(
                        bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣឮ"),
                        bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ឯ")
                        + json.dumps(bstack11l1ll1l1l1_opy_)
                        + bstack11ll11_opy_ (u"ࠤࢀࠦឰ")
                    )
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥឱ"), e)
    def bstack11ll1ll1111_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        f: TestFramework,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1lll1111_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l_opy_:
            self.logger.debug(
                bstack1l1ll1lll11_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧឲ"))
            return
        bstack11l1ll1l111_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l11l11llll_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11l1ll1l111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣឳ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢ឴"))
            return
        if len(bstack11l1ll1l111_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1lll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤ឵"))
        bstack11l1ll111l1_opy_, bstack11ll1111ll1_opy_ = bstack11l1ll1l111_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣា") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥិ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11ll11_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣី") + str(timestamp)
        try:
            page.evaluate(
                bstack11ll11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧឹ"),
                bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪឺ").format(
                    json.dumps(
                        {
                            bstack11ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨុ"): bstack11ll11_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤូ"),
                            bstack11ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦួ"): {
                                bstack11ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢើ"): bstack11ll11_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢឿ"),
                                bstack11ll11_opy_ (u"ࠦࡩࡧࡴࡢࠤៀ"): data,
                                bstack11ll11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦេ"): bstack11ll11_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧែ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤៃ"), e)
    def bstack11ll11ll111_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        f: TestFramework,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1lll1111_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if f.bstack1ll111l1111_opy_(instance, bstack1l11l11llll_opy_.bstack11lll11l11l_opy_, False):
            return
        self.bstack1l11111l1l1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack11ll11_opy_ (u"ࠣࠤោ"))
        req.platform_index = int(TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, 0) or 0)
        req.client_worker_id = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣៅ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111ll1111_opy_, bstack11ll11_opy_ (u"ࠥࠦំ")) or bstack11ll11_opy_ (u"ࠦࠧះ"))
        req.test_framework_version = str(TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11lll1l111l_opy_, bstack11ll11_opy_ (u"ࠧࠨៈ")) or bstack11ll11_opy_ (u"ࠨࠢ៉"))
        req.test_framework_state = str(bstack1l1ll1l11l1_opy_[0].name)
        req.test_hook_state = str(bstack1l1ll1l11l1_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, bstack11ll11_opy_ (u"ࠢࠣ៊")) or bstack11ll11_opy_ (u"ࠣࠤ់"))
        current_test_id = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1ll1llll_opy_, None)
        bstack11l1ll11111_opy_ = 0
        bstack11l1ll11l11_opy_ = 0
        for bstack11l1l1lll11_opy_ in bstack1111l11l1l_opy_.bstack11111l111l_opy_.values():
            session_id = bstack1111l11l1l_opy_.bstack1ll111l1111_opy_(
                bstack11l1l1lll11_opy_,
                bstack1111l11l1l_opy_.bstack1ll111l11l1_opy_,
                bstack11ll11_opy_ (u"ࠤࠥ៌")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1111l11l1l_opy_.bstack1ll111l1111_opy_(bstack11l1l1lll11_opy_, bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠ࡫ࡧࠫ៍"), None)
                if instance_test_id != current_test_id:
                    bstack11l1ll11l11_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1ll11l11_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥ៎")
                if bstack1l1ll1ll1l_opy_
                else bstack11ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦ៏")
            )
            session.ref = str(bstack11l1l1lll11_opy_.ref() or bstack11ll11_opy_ (u"ࠨࠢ័"))
            session.hub_url = str(bstack1111l11l1l_opy_.bstack1ll111l1111_opy_(
                bstack11l1l1lll11_opy_,
                bstack1111l11l1l_opy_.bstack1111l1l11_opy_,
                bstack11ll11_opy_ (u"ࠢࠣ៑")
            ) or bstack11ll11_opy_ (u"ࠣࠤ្"))
            session.framework_name = str(bstack11l1l1lll11_opy_.framework_name or bstack11ll11_opy_ (u"ࠤࠥ៓"))
            session.framework_version = str(bstack11l1l1lll11_opy_.framework_version or bstack11ll11_opy_ (u"ࠥࠦ។"))
            session.framework_session_id = str(session_id)
            bstack11l1ll11111_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1111ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1ll1l111_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l11l11llll_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11l1ll1l111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ៕") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨ៖"))
            return
        if len(bstack11l1ll1l111_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢៗ") + str(kwargs) + bstack11ll11_opy_ (u"ࠢࠣ៘"))
        bstack11l1ll111l1_opy_, bstack11ll1111ll1_opy_ = bstack11l1ll1l111_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ៙") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥ៚"))
            return
        return page
    def bstack1l11111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l1l1lllll_opy_ = {}
        for bstack11l1l1lll11_opy_ in bstack1111l11l1l_opy_.bstack11111l111l_opy_.values():
            caps = bstack1111l11l1l_opy_.bstack1ll111l1111_opy_(bstack11l1l1lll11_opy_, bstack1111l11l1l_opy_.bstack11ll1l111l_opy_, {})
        bstack11l1l1lllll_opy_[bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ៛")] = caps.get(bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧៜ"), bstack11ll11_opy_ (u"ࠧࠨ៝"))
        bstack11l1l1lllll_opy_[bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ៞")] = caps.get(bstack11ll11_opy_ (u"ࠢࡰࡵࠥ៟"), bstack11ll11_opy_ (u"ࠣࠤ០"))
        bstack11l1l1lllll_opy_[bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ១")] = caps.get(bstack11ll11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ២"), bstack11ll11_opy_ (u"ࠦࠧ៣"))
        bstack11l1l1lllll_opy_[bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ៤")] = caps.get(bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ៥"), bstack11ll11_opy_ (u"ࠢࠣ៦"))
        try:
            bstack1l11l11ll_opy_ = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack1l11l11ll_opy_, int):
                bstack1l11l11ll_opy_ = 0
            bstack1l1ll1111_opy_ = self.config.get(bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ៧"), [])
            bstack11l1l1llll1_opy_ = bstack1l1ll1111_opy_[bstack1l11l11ll_opy_] if bstack1l11l11ll_opy_ < len(bstack1l1ll1111_opy_) else self.config
            bstack1ll1ll111ll_opy_ = (
                bstack11l1l1llll1_opy_.get(bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៨"))
                or bstack11l1l1llll1_opy_.get(bstack11ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៩"))
                or self.config.get(bstack11ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៪"))
                or self.config.get(bstack11ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៫"))
            )
            if bstack1ll1ll111ll_opy_:
                bstack11l1l1lllll_opy_[bstack11ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ៬")] = bstack1ll1ll111ll_opy_
        except Exception as ex:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡤࡸࡹࡧࡣࡩࠢࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦ៭") + str(ex) + bstack11ll11_opy_ (u"ࠣࠤ៮"))
        return bstack11l1l1lllll_opy_
    def bstack1l111l111ll_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack11ll11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ៯"), bstack11ll11_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥ៰"))
            if is_robot_playwright_installed():
                bstack11l1lll111l_opy_ = script_code.replace(bstack11ll11_opy_ (u"ࠦࡼ࡯࡮ࡥࡱࡺ࠲ࠧ៱"), bstack11ll11_opy_ (u"ࠧ࡭࡬ࡰࡤࡤࡰ࡙࡮ࡩࡴ࠰ࠥ៲"))
                bstack11l1lll111l_opy_ = bstack11l1lll111l_opy_.replace(bstack11ll11_opy_ (u"ࠨࡷࡪࡰࡧࡳࡼࡡࠢ៳"), bstack11ll11_opy_ (u"ࠢࡨ࡮ࡲࡦࡦࡲࡔࡩ࡫ࡶ࡟ࠧ៴"))
                bstack11l1ll1111l_opy_ = bstack11ll11_opy_ (u"ࠣࠤࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࠪࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧࡲࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠡ࠿ࠣ࡟ࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽ࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠥࠦࠧ៵").format(fn_body=bstack11l1lll111l_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack11ll11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴ࠱ࡉࡻࡧ࡬ࡶࡣࡷࡩࠥࡐࡡࡷࡣࡖࡧࡷ࡯ࡰࡵࠩ៶"),
                    None,
                    bstack11l1ll1111l_opy_
                )
            else:
                script_template = bstack11ll11_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩࠩࡽࡤࡶ࡬ࡥࡪࡴࡱࡱࢁ࠮ࠨࠢࠣ៷")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥ៸") + str(e) + bstack11ll11_opy_ (u"ࠧࠨ៹"))