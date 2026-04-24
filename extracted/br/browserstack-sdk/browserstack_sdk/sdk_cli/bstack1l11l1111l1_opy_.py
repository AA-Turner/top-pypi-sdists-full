# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack1l1ll1ll111_opy_,
    bstack1l1lll11111_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111llll1_opy_, bstack1ll1l1llll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l111llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lll11_opy_ import bstack11lll1lll1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1lll1lll_opy_ import bstack1lll1l1l11_opy_, bstack11111lll11_opy_, bstack1lll1l1l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l11lll1l11_opy_(bstack11lll1lll1l_opy_):
    bstack11l1ll1l111_opy_ = bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣអ")
    bstack11ll1llllll_opy_ = bstack111ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤឣ")
    bstack11ll111ll11_opy_ = bstack111ll11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨឤ")
    bstack11l1ll111l1_opy_ = bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧឥ")
    bstack11l1l1lll11_opy_ = bstack111ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥឦ")
    bstack11ll1ll1lll_opy_ = bstack111ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨឧ")
    bstack11l1l1lll1l_opy_ = bstack111ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦឨ")
    bstack11l1ll11l1l_opy_ = bstack111ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢឩ")
    def __init__(self):
        super().__init__(bstack11lll1ll1l1_opy_=self.bstack11l1ll1l111_opy_, frameworks=[bstack1l11l11111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l1l1ll11l_opy_)
        if bstack1ll1l1llll_opy_():
            TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11llllll1l1_opy_)
        else:
            TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11llllll1l1_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1ll1l11l_opy_ = self.bstack11l1ll1111l_opy_(instance.context)
        if not bstack11l1ll1l11l_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣឪ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠦࠧឫ"))
            return
        f.bstack11l1ll11ll_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1llllll_opy_, bstack11l1ll1l11l_opy_)
    def bstack11l1ll1111l_opy_(self, context: bstack1l1lll11111_opy_, bstack11l1l1l1ll1_opy_= True):
        if bstack11l1l1l1ll1_opy_:
            bstack11l1ll1l11l_opy_ = self.bstack11llll1111l_opy_(context, reverse=True)
        else:
            bstack11l1ll1l11l_opy_ = self.bstack11llll11111_opy_(context, reverse=True)
        return [f for f in bstack11l1ll1l11l_opy_ if f[1].state != bstack11l111l1l_opy_.QUIT]
    def bstack11llllll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1ll11l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if not bstack1l111llll1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣឬ") + str(kwargs) + bstack111ll11_opy_ (u"ࠨࠢឭ"))
            return
        bstack11l1ll1l11l_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1llllll_opy_, [])
        if not bstack11l1ll1l11l_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥឮ") + str(kwargs) + bstack111ll11_opy_ (u"ࠣࠤឯ"))
            return
        if len(bstack11l1ll1l11l_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦឰ"))
        bstack11l1ll1l1l1_opy_, bstack11ll11111ll_opy_ = bstack11l1ll1l11l_opy_[0]
        page = bstack11l1ll1l1l1_opy_()
        if not page:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥឱ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧឲ"))
            return
        bstack1ll11l1l1_opy_ = getattr(args[0], bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧឳ"), None) or getattr(args[0], bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ឴"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll11_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧ឵")).get(bstack111ll11_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥា")):
            try:
                page.evaluate(bstack111ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥិ"),
                            bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧី") + json.dumps(
                                bstack1ll11l1l1_opy_) + bstack111ll11_opy_ (u"ࠦࢂࢃࠢឹ"))
            except Exception as e:
                self.logger.debug(bstack111ll11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥឺ"), e)
    def bstack1l111l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1ll11l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if not bstack1l111llll1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤុ") + str(kwargs) + bstack111ll11_opy_ (u"ࠢࠣូ"))
            return
        bstack11l1ll1l11l_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1llllll_opy_, [])
        if not bstack11l1ll1l11l_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦួ") + str(kwargs) + bstack111ll11_opy_ (u"ࠤࠥើ"))
            return
        if len(bstack11l1ll1l11l_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧឿ"))
        bstack11l1ll1l1l1_opy_, bstack11ll11111ll_opy_ = bstack11l1ll1l11l_opy_[0]
        page = bstack11l1ll1l1l1_opy_()
        if not page:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦៀ") + str(kwargs) + bstack111ll11_opy_ (u"ࠧࠨេ"))
            return
        status = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1ll11111_opy_, None)
        if not status:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤែ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠢࠣៃ"))
            return
        bstack11l1l1lllll_opy_ = {bstack111ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣោ"): status.lower()}
        bstack11l1l1ll111_opy_ = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1ll111ll_opy_, None)
        if status.lower() == bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩៅ") and bstack11l1l1ll111_opy_ is not None:
            bstack11l1l1lllll_opy_[bstack111ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪំ")] = bstack11l1l1ll111_opy_[0][bstack111ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧះ")][0] if isinstance(bstack11l1l1ll111_opy_, list) else str(bstack11l1l1ll111_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥៈ")).get(bstack111ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ៉")):
            try:
                page.evaluate(
                        bstack111ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ៊"),
                        bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭់")
                        + json.dumps(bstack11l1l1lllll_opy_)
                        + bstack111ll11_opy_ (u"ࠤࢀࠦ៌")
                    )
            except Exception as e:
                self.logger.debug(bstack111ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥ៍"), e)
    def bstack11ll11l11ll_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        f: TestFramework,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1ll11l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if not bstack1l111llll1_opy_:
            self.logger.debug(
                bstack1l1ll1111ll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧ៎"))
            return
        bstack11l1ll1l11l_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1llllll_opy_, [])
        if not bstack11l1ll1l11l_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ៏") + str(kwargs) + bstack111ll11_opy_ (u"ࠨࠢ័"))
            return
        if len(bstack11l1ll1l11l_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1111ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤ៑"))
        bstack11l1ll1l1l1_opy_, bstack11ll11111ll_opy_ = bstack11l1ll1l11l_opy_[0]
        page = bstack11l1ll1l1l1_opy_()
        if not page:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽្ࠣ") + str(kwargs) + bstack111ll11_opy_ (u"ࠤࠥ៓"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111ll11_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣ។") + str(timestamp)
        try:
            page.evaluate(
                bstack111ll11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ៕"),
                bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ៖").format(
                    json.dumps(
                        {
                            bstack111ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨៗ"): bstack111ll11_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ៘"),
                            bstack111ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ៙"): {
                                bstack111ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ៚"): bstack111ll11_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢ៛"),
                                bstack111ll11_opy_ (u"ࠦࡩࡧࡴࡢࠤៜ"): data,
                                bstack111ll11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦ៝"): bstack111ll11_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧ៞")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤ៟"), e)
    def bstack11ll111ll1l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        f: TestFramework,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1l1ll11l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1ll1lll_opy_, False):
            return
        self.bstack1l1111lllll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack111ll11_opy_ (u"ࠣࠤ០"))
        req.platform_index = int(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11llllll1ll_opy_, 0) or 0)
        req.client_worker_id = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ១").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111ll11ll_opy_, bstack111ll11_opy_ (u"ࠥࠦ២")) or bstack111ll11_opy_ (u"ࠦࠧ៣"))
        req.test_framework_version = str(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11111l_opy_, bstack111ll11_opy_ (u"ࠧࠨ៤")) or bstack111ll11_opy_ (u"ࠨࠢ៥"))
        req.test_framework_state = str(bstack1l1ll11l11l_opy_[0].name)
        req.test_hook_state = str(bstack1l1ll11l11l_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_, bstack111ll11_opy_ (u"ࠢࠣ៦")) or bstack111ll11_opy_ (u"ࠣࠤ៧"))
        current_test_id = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1l1l1l1l_opy_, None)
        bstack11l1l1ll1ll_opy_ = 0
        bstack11l1ll11ll1_opy_ = 0
        for bstack11l1l1l1lll_opy_ in bstack111ll11111_opy_.bstack1111l11ll_opy_.values():
            session_id = bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(
                bstack11l1l1l1lll_opy_,
                bstack111ll11111_opy_.bstack1ll11111lll_opy_,
                bstack111ll11_opy_ (u"ࠤࠥ៨")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(bstack11l1l1l1lll_opy_, bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠ࡫ࡧࠫ៩"), None)
                if instance_test_id != current_test_id:
                    bstack11l1ll11ll1_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1ll11ll1_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack111ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥ៪")
                if bstack1l111llll1_opy_
                else bstack111ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦ៫")
            )
            session.ref = str(bstack11l1l1l1lll_opy_.ref() or bstack111ll11_opy_ (u"ࠨࠢ៬"))
            session.hub_url = str(bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(
                bstack11l1l1l1lll_opy_,
                bstack111ll11111_opy_.bstack111llll1ll_opy_,
                bstack111ll11_opy_ (u"ࠢࠣ៭")
            ) or bstack111ll11_opy_ (u"ࠣࠤ៮"))
            session.framework_name = str(bstack11l1l1l1lll_opy_.framework_name or bstack111ll11_opy_ (u"ࠤࠥ៯"))
            session.framework_version = str(bstack11l1l1l1lll_opy_.framework_version or bstack111ll11_opy_ (u"ࠥࠦ៰"))
            session.framework_session_id = str(session_id)
            bstack11l1l1ll1ll_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11lllll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1ll1l11l_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll1l11_opy_.bstack11ll1llllll_opy_, [])
        if not bstack11l1ll1l11l_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ៱") + str(kwargs) + bstack111ll11_opy_ (u"ࠧࠨ៲"))
            return
        if len(bstack11l1ll1l11l_opy_) > 1:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ៳") + str(kwargs) + bstack111ll11_opy_ (u"ࠢࠣ៴"))
        bstack11l1ll1l1l1_opy_, bstack11ll11111ll_opy_ = bstack11l1ll1l11l_opy_[0]
        page = bstack11l1ll1l1l1_opy_()
        if not page:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ៵") + str(kwargs) + bstack111ll11_opy_ (u"ࠤࠥ៶"))
            return
        return page
    def bstack1l11111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l1ll11lll_opy_ = {}
        for bstack11l1l1l1lll_opy_ in bstack111ll11111_opy_.bstack1111l11ll_opy_.values():
            caps = bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(bstack11l1l1l1lll_opy_, bstack111ll11111_opy_.bstack1lllll1l1l_opy_, {})
        bstack11l1ll11lll_opy_[bstack111ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ៷")] = caps.get(bstack111ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ៸"), bstack111ll11_opy_ (u"ࠧࠨ៹"))
        bstack11l1ll11lll_opy_[bstack111ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ៺")] = caps.get(bstack111ll11_opy_ (u"ࠢࡰࡵࠥ៻"), bstack111ll11_opy_ (u"ࠣࠤ៼"))
        bstack11l1ll11lll_opy_[bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ៽")] = caps.get(bstack111ll11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ៾"), bstack111ll11_opy_ (u"ࠦࠧ៿"))
        bstack11l1ll11lll_opy_[bstack111ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ᠀")] = caps.get(bstack111ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᠁"), bstack111ll11_opy_ (u"ࠢࠣ᠂"))
        try:
            bstack1l1ll11l1l_opy_ = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11llllll1ll_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack1l1ll11l1l_opy_, int):
                bstack1l1ll11l1l_opy_ = 0
            bstack11lll1l1ll_opy_ = self.config.get(bstack111ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᠃"), [])
            bstack11l1ll11l11_opy_ = bstack11lll1l1ll_opy_[bstack1l1ll11l1l_opy_] if bstack1l1ll11l1l_opy_ < len(bstack11lll1l1ll_opy_) else self.config
            bstack1ll1ll11lll_opy_ = (
                bstack11l1ll11l11_opy_.get(bstack111ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠄"))
                or bstack11l1ll11l11_opy_.get(bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᠅"))
                or self.config.get(bstack111ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᠆"))
                or self.config.get(bstack111ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᠇"))
            )
            if bstack1ll1ll11lll_opy_:
                bstack11l1ll11lll_opy_[bstack111ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᠈")] = bstack1ll1ll11lll_opy_
        except Exception as ex:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡤࡸࡹࡧࡣࡩࠢࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦ᠉") + str(ex) + bstack111ll11_opy_ (u"ࠣࠤ᠊"))
        return bstack11l1ll11lll_opy_
    def bstack11lllllll11_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack111ll11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ᠋"), bstack111ll11_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥ᠌"))
            if is_robot_playwright_installed():
                bstack11l1l1ll1l1_opy_ = script_code.replace(bstack111ll11_opy_ (u"ࠦࡼ࡯࡮ࡥࡱࡺ࠲ࠧ᠍"), bstack111ll11_opy_ (u"ࠧ࡭࡬ࡰࡤࡤࡰ࡙࡮ࡩࡴ࠰ࠥ᠎"))
                bstack11l1l1ll1l1_opy_ = bstack11l1l1ll1l1_opy_.replace(bstack111ll11_opy_ (u"ࠨࡷࡪࡰࡧࡳࡼࡡࠢ᠏"), bstack111ll11_opy_ (u"ࠢࡨ࡮ࡲࡦࡦࡲࡔࡩ࡫ࡶ࡟ࠧ᠐"))
                bstack11l1l1llll1_opy_ = bstack111ll11_opy_ (u"ࠣࠤࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࠪࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧࡲࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠡ࠿ࠣ࡟ࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽ࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠥࠦࠧ᠑").format(fn_body=bstack11l1l1ll1l1_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack111ll11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴ࠱ࡉࡻࡧ࡬ࡶࡣࡷࡩࠥࡐࡡࡷࡣࡖࡧࡷ࡯ࡰࡵࠩ᠒"),
                    None,
                    bstack11l1l1llll1_opy_
                )
            else:
                script_template = bstack111ll11_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩࠩࡽࡤࡶ࡬ࡥࡪࡴࡱࡱࢁ࠮ࠨࠢࠣ᠓")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥ᠔") + str(e) + bstack111ll11_opy_ (u"ࠧࠨ᠕"))