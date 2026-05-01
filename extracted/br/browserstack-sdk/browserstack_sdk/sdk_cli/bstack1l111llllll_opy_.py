# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack1l1ll111lll_opy_,
    bstack1l1ll1111l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1l11_opy_, bstack11l1ll1l1_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lllll_opy_ import bstack11lll1ll111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11111l1ll1_opy_ import bstack111ll111l_opy_, bstack11ll1l1l1_opy_, bstack1lllll111_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l11l1ll111_opy_(bstack11lll1ll111_opy_):
    bstack11l1l1l1l1l_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦឳ")
    bstack11ll1lll1ll_opy_ = bstack111ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧ឴")
    bstack11ll1l1ll11_opy_ = bstack111ll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ឵")
    bstack11l1ll11l1l_opy_ = bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣា")
    bstack11l1l1l111l_opy_ = bstack111ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨិ")
    bstack11ll11l11ll_opy_ = bstack111ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤី")
    bstack11l1ll11111_opy_ = bstack111ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢឹ")
    bstack11l1l1l11ll_opy_ = bstack111ll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥឺ")
    def __init__(self):
        super().__init__(bstack11lll1llll1_opy_=self.bstack11l1l1l1l1l_opy_, frameworks=[bstack1l11lll111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l1ll1111l_opy_)
        if bstack11l1ll1l1_opy_():
            TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l11ll_opy_)
        else:
            TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111l11ll_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1ll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1l1l1ll1_opy_ = self.bstack11l1l1ll111_opy_(instance.context)
        if not bstack11l1l1l1ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦុ") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠢࠣូ"))
            return
        f.bstack11ll11l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1lll1ll_opy_, bstack11l1l1l1ll1_opy_)
    def bstack11l1l1ll111_opy_(self, context: bstack1l1ll1111l1_opy_, bstack11l1l1lll1l_opy_= True):
        if bstack11l1l1lll1l_opy_:
            bstack11l1l1l1ll1_opy_ = self.bstack11lll1ll1ll_opy_(context, reverse=True)
        else:
            bstack11l1l1l1ll1_opy_ = self.bstack11lll1ll1l1_opy_(context, reverse=True)
        return [f for f in bstack11l1l1l1ll1_opy_ if f[1].state != bstack1ll1l1111l_opy_.QUIT]
    def bstack1l1111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll1111l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if not bstack1l1l1l11_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦួ") + str(kwargs) + bstack111ll_opy_ (u"ࠤࠥើ"))
            return
        bstack11l1l1l1ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack11l1l1l1ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨឿ") + str(kwargs) + bstack111ll_opy_ (u"ࠦࠧៀ"))
            return
        if len(bstack11l1l1l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢេ"))
        bstack11l1ll111l1_opy_, bstack11l1llll11l_opy_ = bstack11l1l1l1ll1_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨែ") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣៃ"))
            return
        bstack1111l11lll_opy_ = getattr(args[0], bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣោ"), None) or getattr(args[0], bstack111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢៅ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣំ")).get(bstack111ll_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨះ")):
            try:
                page.evaluate(bstack111ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨៈ"),
                            bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ៉") + json.dumps(
                                bstack1111l11lll_opy_) + bstack111ll_opy_ (u"ࠢࡾࡿࠥ៊"))
            except Exception as e:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ់"), e)
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll1111l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if not bstack1l1l1l11_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ៌") + str(kwargs) + bstack111ll_opy_ (u"ࠥࠦ៍"))
            return
        bstack11l1l1l1ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack11l1l1l1ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ៎") + str(kwargs) + bstack111ll_opy_ (u"ࠧࠨ៏"))
            return
        if len(bstack11l1l1l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l1111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣ័"))
        bstack11l1ll111l1_opy_, bstack11l1llll11l_opy_ = bstack11l1l1l1ll1_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ៑") + str(kwargs) + bstack111ll_opy_ (u"ࠣࠤ្"))
            return
        status = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1ll11l11_opy_, None)
        if not status:
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧ៓") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠥࠦ។"))
            return
        bstack11l1l1l1111_opy_ = {bstack111ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ៕"): status.lower()}
        bstack11l1l1lll11_opy_ = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1l1ll1ll_opy_, None)
        if status.lower() == bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ៖") and bstack11l1l1lll11_opy_ is not None:
            bstack11l1l1l1111_opy_[bstack111ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ៗ")] = bstack11l1l1lll11_opy_[0][bstack111ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ៘")][0] if isinstance(bstack11l1l1lll11_opy_, list) else str(bstack11l1l1lll11_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ៙")).get(bstack111ll_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ៚")):
            try:
                page.evaluate(
                        bstack111ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ៛"),
                        bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩៜ")
                        + json.dumps(bstack11l1l1l1111_opy_)
                        + bstack111ll_opy_ (u"ࠧࢃࠢ៝")
                    )
            except Exception as e:
                self.logger.debug(bstack111ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ៞"), e)
    def bstack11ll11lll1l_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        f: TestFramework,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll1111l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if not bstack1l1l1l11_opy_:
            self.logger.debug(
                bstack1l1ll1l1111_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣ៟"))
            return
        bstack11l1l1l1ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack11l1l1l1ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ០") + str(kwargs) + bstack111ll_opy_ (u"ࠤࠥ១"))
            return
        if len(bstack11l1l1l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1l1ll1l1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧ២"))
        bstack11l1ll111l1_opy_, bstack11l1llll11l_opy_ = bstack11l1l1l1ll1_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ៣") + str(kwargs) + bstack111ll_opy_ (u"ࠧࠨ៤"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111ll_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦ៥") + str(timestamp)
        try:
            page.evaluate(
                bstack111ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ៦"),
                bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭៧").format(
                    json.dumps(
                        {
                            bstack111ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ៨"): bstack111ll_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ៩"),
                            bstack111ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ៪"): {
                                bstack111ll_opy_ (u"ࠧࡺࡹࡱࡧࠥ៫"): bstack111ll_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥ៬"),
                                bstack111ll_opy_ (u"ࠢࡥࡣࡷࡥࠧ៭"): data,
                                bstack111ll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢ៮"): bstack111ll_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣ៯")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧ៰"), e)
    def bstack11ll111llll_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        f: TestFramework,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l1ll1111l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if f.bstack1l1llll1111_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll11l11ll_opy_, False):
            return
        self.bstack11llllll111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack111ll_opy_ (u"ࠦࠧ៱"))
        req.platform_index = int(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_, 0) or 0)
        req.client_worker_id = bstack111ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ៲").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111l111l_opy_, bstack111ll_opy_ (u"ࠨࠢ៳")) or bstack111ll_opy_ (u"ࠢࠣ៴"))
        req.test_framework_version = str(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l11l1l_opy_, bstack111ll_opy_ (u"ࠣࠤ៵")) or bstack111ll_opy_ (u"ࠤࠥ៶"))
        req.test_framework_state = str(bstack1l1l1lll11l_opy_[0].name)
        req.test_hook_state = str(bstack1l1l1lll11l_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_, bstack111ll_opy_ (u"ࠥࠦ៷")) or bstack111ll_opy_ (u"ࠦࠧ៸"))
        current_test_id = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_, None)
        bstack11l1ll111ll_opy_ = 0
        bstack11l1l1l11l1_opy_ = 0
        for bstack11l1l1l1l11_opy_ in bstack11ll1l1ll_opy_.bstack111l11l1l1_opy_.values():
            session_id = bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(
                bstack11l1l1l1l11_opy_,
                bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_,
                bstack111ll_opy_ (u"ࠧࠨ៹")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(bstack11l1l1l1l11_opy_, bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧ៺"), None)
                if instance_test_id != current_test_id:
                    bstack11l1l1l11l1_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1l1l11l1_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨ៻")
                if bstack1l1l1l11_opy_
                else bstack111ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢ៼")
            )
            session.ref = str(bstack11l1l1l1l11_opy_.ref() or bstack111ll_opy_ (u"ࠤࠥ៽"))
            session.hub_url = str(bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(
                bstack11l1l1l1l11_opy_,
                bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_,
                bstack111ll_opy_ (u"ࠥࠦ៾")
            ) or bstack111ll_opy_ (u"ࠦࠧ៿"))
            session.framework_name = str(bstack11l1l1l1l11_opy_.framework_name or bstack111ll_opy_ (u"ࠧࠨ᠀"))
            session.framework_version = str(bstack11l1l1l1l11_opy_.framework_version or bstack111ll_opy_ (u"ࠨࠢ᠁"))
            session.framework_session_id = str(session_id)
            bstack11l1ll111ll_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l111l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1l1l1ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack11l1l1l1ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᠂") + str(kwargs) + bstack111ll_opy_ (u"ࠣࠤ᠃"))
            return
        if len(bstack11l1l1l1ll1_opy_) > 1:
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᠄") + str(kwargs) + bstack111ll_opy_ (u"ࠥࠦ᠅"))
        bstack11l1ll111l1_opy_, bstack11l1llll11l_opy_ = bstack11l1l1l1ll1_opy_[0]
        page = bstack11l1ll111l1_opy_()
        if not page:
            self.logger.debug(bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᠆") + str(kwargs) + bstack111ll_opy_ (u"ࠧࠨ᠇"))
            return
        return page
    def bstack11llllllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l1l1llll1_opy_ = {}
        for bstack11l1l1l1l11_opy_ in bstack11ll1l1ll_opy_.bstack111l11l1l1_opy_.values():
            caps = bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(bstack11l1l1l1l11_opy_, bstack11ll1l1ll_opy_.bstack1ll111ll_opy_, {})
        bstack11l1l1llll1_opy_[bstack111ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ᠈")] = caps.get(bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ᠉"), bstack111ll_opy_ (u"ࠣࠤ᠊"))
        bstack11l1l1llll1_opy_[bstack111ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ᠋")] = caps.get(bstack111ll_opy_ (u"ࠥࡳࡸࠨ᠌"), bstack111ll_opy_ (u"ࠦࠧ᠍"))
        bstack11l1l1llll1_opy_[bstack111ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ᠎")] = caps.get(bstack111ll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ᠏"), bstack111ll_opy_ (u"ࠢࠣ᠐"))
        bstack11l1l1llll1_opy_[bstack111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ᠑")] = caps.get(bstack111ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ᠒"), bstack111ll_opy_ (u"ࠥࠦ᠓"))
        try:
            bstack1l1l11111_opy_ = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack1l1l11111_opy_, int):
                bstack1l1l11111_opy_ = 0
            bstack11llllllll_opy_ = self.config.get(bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᠔"), [])
            bstack11l1l1ll1l1_opy_ = bstack11llllllll_opy_[bstack1l1l11111_opy_] if bstack1l1l11111_opy_ < len(bstack11llllllll_opy_) else self.config
            bstack1ll1lll1l1l_opy_ = (
                bstack11l1l1ll1l1_opy_.get(bstack111ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᠕"))
                or bstack11l1l1ll1l1_opy_.get(bstack111ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᠖"))
                or self.config.get(bstack111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᠗"))
                or self.config.get(bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᠘"))
            )
            if bstack1ll1lll1l1l_opy_:
                bstack11l1l1llll1_opy_[bstack111ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠙")] = bstack1ll1lll1l1l_opy_
        except Exception as ex:
            self.logger.debug(bstack111ll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡧࡴࡵࡣࡦ࡬ࠥࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ࠿ࠦࠢ᠚") + str(ex) + bstack111ll_opy_ (u"ࠦࠧ᠛"))
        return bstack11l1l1llll1_opy_
    def bstack1l111111ll1_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack111ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᠜"), bstack111ll_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨ᠝"))
            if is_robot_playwright_installed():
                bstack11l1l1lllll_opy_ = script_code.replace(bstack111ll_opy_ (u"ࠢࡸ࡫ࡱࡨࡴࡽ࠮ࠣ᠞"), bstack111ll_opy_ (u"ࠣࡩ࡯ࡳࡧࡧ࡬ࡕࡪ࡬ࡷ࠳ࠨ᠟"))
                bstack11l1l1lllll_opy_ = bstack11l1l1lllll_opy_.replace(bstack111ll_opy_ (u"ࠤࡺ࡭ࡳࡪ࡯ࡸ࡝ࠥᠠ"), bstack111ll_opy_ (u"ࠥ࡫ࡱࡵࡢࡢ࡮ࡗ࡬࡮ࡹ࡛ࠣᠡ"))
                bstack11l1l1l1lll_opy_ = bstack111ll_opy_ (u"ࠦࠧࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽ࠭࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡷࡣࡵࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠤࡂ࡛ࠦࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂࠨࠢࠣᠢ").format(fn_body=bstack11l1l1lllll_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack111ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡅࡷࡣ࡯ࡹࡦࡺࡥࠡࡌࡤࡺࡦ࡙ࡣࡳ࡫ࡳࡸࠬᠣ"),
                    None,
                    bstack11l1l1l1lll_opy_
                )
            else:
                script_template = bstack111ll_opy_ (u"ࠨࠢࠣࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࠴࠮࠯ࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦᠤ")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨᠥ") + str(e) + bstack111ll_opy_ (u"ࠣࠤᠦ"))