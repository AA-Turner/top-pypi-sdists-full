# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l111l1l1_opy_,
    bstack1l1lll111ll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1ll111_opy_, bstack11llll11ll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack11ll11lll1l_opy_ import bstack11ll1l11111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11111l111_opy_ import bstack1111llll1l_opy_, bstack11ll1l11ll_opy_, bstack111ll111l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1111ll1l1_opy_(bstack11ll1l11111_opy_):
    bstack11l11ll1111_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤ᠚")
    bstack11ll11ll111_opy_ = bstack111l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥ᠛")
    bstack11l1lll11l1_opy_ = bstack111l_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢ᠜")
    bstack11l11llll11_opy_ = bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨ᠝")
    bstack11l1l11111l_opy_ = bstack111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦ᠞")
    bstack11ll11111ll_opy_ = bstack111l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢ᠟")
    bstack11l11lll1l1_opy_ = bstack111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᠠ")
    bstack11l11ll1l11_opy_ = bstack111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᠡ")
    def __init__(self):
        super().__init__(bstack11ll1l11ll1_opy_=self.bstack11l11ll1111_opy_, frameworks=[bstack1l11l11l11l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11ll1ll1_opy_)
        if bstack11llll11ll_opy_():
            TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll1ll_opy_)
        else:
            TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11lll1ll1ll_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l11ll1lll_opy_ = self.bstack11l11lll11l_opy_(instance.context)
        if not bstack11l11ll1lll_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᠢ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠧࠨᠣ"))
            return
        f.bstack1l11l1ll11_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11ll111_opy_, bstack11l11ll1lll_opy_)
    def bstack11l11lll11l_opy_(self, context: bstack1l1lll111ll_opy_, bstack11l11ll11ll_opy_= True):
        if bstack11l11ll11ll_opy_:
            bstack11l11ll1lll_opy_ = self.bstack11ll1l11lll_opy_(context, reverse=True)
        else:
            bstack11l11ll1lll_opy_ = self.bstack11ll11llll1_opy_(context, reverse=True)
        return [f for f in bstack11l11ll1lll_opy_ if f[1].state != bstack11l1ll1l1_opy_.QUIT]
    def bstack11lll1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1ll1_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if not bstack1ll1ll111_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᠤ") + str(kwargs) + bstack111l_opy_ (u"ࠢࠣᠥ"))
            return
        bstack11l11ll1lll_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11ll111_opy_, [])
        if not bstack11l11ll1lll_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᠦ") + str(kwargs) + bstack111l_opy_ (u"ࠤࠥᠧ"))
            return
        if len(bstack11l11ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᠨ"))
        bstack11l11ll11l1_opy_, bstack11l1l1l1lll_opy_ = bstack11l11ll1lll_opy_[0]
        page = bstack11l11ll11l1_opy_()
        if not page:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᠩ") + str(kwargs) + bstack111l_opy_ (u"ࠧࠨᠪ"))
            return
        bstack111l11l1l1_opy_ = getattr(args[0], bstack111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᠫ"), None) or getattr(args[0], bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᠬ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᠭ")).get(bstack111l_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᠮ")):
            try:
                page.evaluate(bstack111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᠯ"),
                            bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨᠰ") + json.dumps(
                                bstack111l11l1l1_opy_) + bstack111l_opy_ (u"ࠧࢃࡽࠣᠱ"))
            except Exception as e:
                self.logger.debug(bstack111l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦᠲ"), e)
    def bstack11lll1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1ll1_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if not bstack1ll1ll111_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᠳ") + str(kwargs) + bstack111l_opy_ (u"ࠣࠤᠴ"))
            return
        bstack11l11ll1lll_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11ll111_opy_, [])
        if not bstack11l11ll1lll_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᠵ") + str(kwargs) + bstack111l_opy_ (u"ࠥࠦᠶ"))
            return
        if len(bstack11l11ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᠷ"))
        bstack11l11ll11l1_opy_, bstack11l1l1l1lll_opy_ = bstack11l11ll1lll_opy_[0]
        page = bstack11l11ll11l1_opy_()
        if not page:
            self.logger.debug(bstack111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᠸ") + str(kwargs) + bstack111l_opy_ (u"ࠨࠢᠹ"))
            return
        status = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, None)
        if not status:
            self.logger.debug(bstack111l_opy_ (u"ࠢ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᠺ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠣࠤᠻ"))
            return
        bstack11l11llll1l_opy_ = {bstack111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᠼ"): status.lower()}
        bstack11l11lll111_opy_ = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_, None)
        if status.lower() == bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᠽ") and bstack11l11lll111_opy_ is not None:
            bstack11l11llll1l_opy_[bstack111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᠾ")] = bstack11l11lll111_opy_[0][bstack111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᠿ")][0] if isinstance(bstack11l11lll111_opy_, list) else str(bstack11l11lll111_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᡀ")).get(bstack111l_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᡁ")):
            try:
                page.evaluate(
                        bstack111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᡂ"),
                        bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧᡃ")
                        + json.dumps(bstack11l11llll1l_opy_)
                        + bstack111l_opy_ (u"ࠥࢁࠧᡄ")
                    )
            except Exception as e:
                self.logger.debug(bstack111l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦᡅ"), e)
    def bstack11ll111l1ll_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        f: TestFramework,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1ll1_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if not bstack1ll1ll111_opy_:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᡆ"))
            return
        bstack11l11ll1lll_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11ll111_opy_, [])
        if not bstack11l11ll1lll_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᡇ") + str(kwargs) + bstack111l_opy_ (u"ࠢࠣᡈ"))
            return
        if len(bstack11l11ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᡉ"))
        bstack11l11ll11l1_opy_, bstack11l1l1l1lll_opy_ = bstack11l11ll1lll_opy_[0]
        page = bstack11l11ll11l1_opy_()
        if not page:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᡊ") + str(kwargs) + bstack111l_opy_ (u"ࠥࠦᡋ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111l_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤᡌ") + str(timestamp)
        try:
            page.evaluate(
                bstack111l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᡍ"),
                bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᡎ").format(
                    json.dumps(
                        {
                            bstack111l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᡏ"): bstack111l_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥᡐ"),
                            bstack111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᡑ"): {
                                bstack111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᡒ"): bstack111l_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣᡓ"),
                                bstack111l_opy_ (u"ࠧࡪࡡࡵࡣࠥᡔ"): data,
                                bstack111l_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧᡕ"): bstack111l_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨᡖ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥᡗ"), e)
    def bstack11l1lll11ll_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        f: TestFramework,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1ll1_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11111ll_opy_, False):
            return
        self.bstack11lllll1111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack111l_opy_ (u"ࠤࠥᡘ"))
        req.platform_index = int(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_, 0) or 0)
        req.client_worker_id = bstack111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᡙ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l11_opy_, bstack111l_opy_ (u"ࠦࠧᡚ")) or bstack111l_opy_ (u"ࠧࠨᡛ"))
        req.test_framework_version = str(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, bstack111l_opy_ (u"ࠨࠢᡜ")) or bstack111l_opy_ (u"ࠢࠣᡝ"))
        req.test_framework_state = str(bstack1l1l1lllll1_opy_[0].name)
        req.test_hook_state = str(bstack1l1l1lllll1_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, bstack111l_opy_ (u"ࠣࠤᡞ")) or bstack111l_opy_ (u"ࠤࠥᡟ"))
        current_test_id = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll111l1l_opy_, None)
        bstack11l11llllll_opy_ = 0
        bstack11l1l111111_opy_ = 0
        for bstack11l11ll1l1l_opy_ in bstack11ll1lllll_opy_.bstack1l111l111_opy_.values():
            session_id = bstack11ll1lllll_opy_.bstack1ll111111ll_opy_(
                bstack11l11ll1l1l_opy_,
                bstack11ll1lllll_opy_.bstack1ll11111111_opy_,
                bstack111l_opy_ (u"ࠥࠦᡠ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack11ll1lllll_opy_.bstack1ll111111ll_opy_(bstack11l11ll1l1l_opy_, bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡬ࡨࠬᡡ"), None)
                if instance_test_id != current_test_id:
                    bstack11l1l111111_opy_ += 1
                    continue
                if not session_id:
                    bstack11l1l111111_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᡢ")
                if bstack1ll1ll111_opy_
                else bstack111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᡣ")
            )
            session.ref = str(bstack11l11ll1l1l_opy_.ref() or bstack111l_opy_ (u"ࠢࠣᡤ"))
            session.hub_url = str(bstack11ll1lllll_opy_.bstack1ll111111ll_opy_(
                bstack11l11ll1l1l_opy_,
                bstack11ll1lllll_opy_.bstack11l1ll111l_opy_,
                bstack111l_opy_ (u"ࠣࠤᡥ")
            ) or bstack111l_opy_ (u"ࠤࠥᡦ"))
            session.framework_name = str(bstack11l11ll1l1l_opy_.framework_name or bstack111l_opy_ (u"ࠥࠦᡧ"))
            session.framework_version = str(bstack11l11ll1l1l_opy_.framework_version or bstack111l_opy_ (u"ࠦࠧᡨ"))
            session.framework_session_id = str(session_id)
            bstack11l11llllll_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11llll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l11ll1lll_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111ll1l1_opy_.bstack11ll11ll111_opy_, [])
        if not bstack11l11ll1lll_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᡩ") + str(kwargs) + bstack111l_opy_ (u"ࠨࠢᡪ"))
            return
        if len(bstack11l11ll1lll_opy_) > 1:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᡫ") + str(kwargs) + bstack111l_opy_ (u"ࠣࠤᡬ"))
        bstack11l11ll11l1_opy_, bstack11l1l1l1lll_opy_ = bstack11l11ll1lll_opy_[0]
        page = bstack11l11ll11l1_opy_()
        if not page:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᡭ") + str(kwargs) + bstack111l_opy_ (u"ࠥࠦᡮ"))
            return
        return page
    def bstack11llll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11l11lllll1_opy_ = {}
        for bstack11l11ll1l1l_opy_ in bstack11ll1lllll_opy_.bstack1l111l111_opy_.values():
            caps = bstack11ll1lllll_opy_.bstack1ll111111ll_opy_(bstack11l11ll1l1l_opy_, bstack11ll1lllll_opy_.bstack1111lll1_opy_, {})
        bstack11l11lllll1_opy_[bstack111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤᡯ")] = caps.get(bstack111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨᡰ"), bstack111l_opy_ (u"ࠨࠢᡱ"))
        bstack11l11lllll1_opy_[bstack111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᡲ")] = caps.get(bstack111l_opy_ (u"ࠣࡱࡶࠦᡳ"), bstack111l_opy_ (u"ࠤࠥᡴ"))
        bstack11l11lllll1_opy_[bstack111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᡵ")] = caps.get(bstack111l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᡶ"), bstack111l_opy_ (u"ࠧࠨᡷ"))
        bstack11l11lllll1_opy_[bstack111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢᡸ")] = caps.get(bstack111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ᡹"), bstack111l_opy_ (u"ࠣࠤ᡺"))
        try:
            bstack11l111lll_opy_ = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11l111lll_opy_, int):
                bstack11l111lll_opy_ = 0
            bstack1ll11ll1_opy_ = self.config.get(bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᡻"), [])
            bstack11l11ll111l_opy_ = bstack1ll11ll1_opy_[bstack11l111lll_opy_] if bstack11l111lll_opy_ < len(bstack1ll11ll1_opy_) else self.config
            bstack1ll1lll1l11_opy_ = (
                bstack11l11ll111l_opy_.get(bstack111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᡼"))
                or bstack11l11ll111l_opy_.get(bstack111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᡽"))
                or self.config.get(bstack111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᡾"))
                or self.config.get(bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᡿"))
            )
            if bstack1ll1lll1l11_opy_:
                bstack11l11lllll1_opy_[bstack111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᢀ")] = bstack1ll1lll1l11_opy_
        except Exception as ex:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡥࡹࡺࡡࡤࡪࠣࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᢁ") + str(ex) + bstack111l_opy_ (u"ࠤࠥᢂ"))
        return bstack11l11lllll1_opy_
    def bstack11lll111ll1_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack111l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᢃ"), bstack111l_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦᢄ"))
            if is_robot_playwright_installed():
                bstack11l11l1llll_opy_ = script_code.replace(bstack111l_opy_ (u"ࠧࡽࡩ࡯ࡦࡲࡻ࠳ࠨᢅ"), bstack111l_opy_ (u"ࠨࡧ࡭ࡱࡥࡥࡱ࡚ࡨࡪࡵ࠱ࠦᢆ"))
                bstack11l11l1llll_opy_ = bstack11l11l1llll_opy_.replace(bstack111l_opy_ (u"ࠢࡸ࡫ࡱࡨࡴࡽ࡛ࠣᢇ"), bstack111l_opy_ (u"ࠣࡩ࡯ࡳࡧࡧ࡬ࡕࡪ࡬ࡷࡠࠨᢈ"))
                bstack11l11lll1ll_opy_ = bstack111l_opy_ (u"ࠤࠥࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࠫ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡࡳࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠢࡀࠤࡠࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾ࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀࠦࠧࠨᢉ").format(fn_body=bstack11l11l1llll_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack111l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡊࡼࡡ࡭ࡷࡤࡸࡪࠦࡊࡢࡸࡤࡗࡨࡸࡩࡱࡶࠪᢊ"),
                    None,
                    bstack11l11lll1ll_opy_
                )
            else:
                script_template = bstack111l_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤᢋ")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮ࠣࠦᢌ") + str(e) + bstack111l_opy_ (u"ࠨࠢᢍ"))