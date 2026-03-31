# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack1ll111lllll_opy_,
    bstack1ll11l11ll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111l1111_opy_, bstack1111l1111l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l111lll111_opy_ import bstack1l11l11111l_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack11l11l111l_opy_, bstack1ll1l11lll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1llll11l1_opy_(bstack1l11l11111l_opy_):
    bstack11ll1llll11_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᙓ")
    bstack1l1111ll1l1_opy_ = bstack1ll11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᙔ")
    bstack1l1111ll111_opy_ = bstack1ll11_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᙕ")
    bstack11lll111lll_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᙖ")
    bstack11lll11111l_opy_ = bstack1ll11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᙗ")
    bstack1l111l11ll1_opy_ = bstack1ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᙘ")
    bstack11lll1111ll_opy_ = bstack1ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᙙ")
    bstack11ll1llllll_opy_ = bstack1ll11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᙚ")
    def __init__(self):
        super().__init__(bstack1l111lll11l_opy_=self.bstack11ll1llll11_opy_, frameworks=[bstack1ll11111111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll1lll11l_opy_)
        if bstack1111l1111l_opy_():
            TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11llll1ll_opy_)
        else:
            TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11llll1ll_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1lll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1lll1l1_opy_ = self.bstack11lll111l11_opy_(instance.context)
        if not bstack11ll1lll1l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᙛ") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠧࠨᙜ"))
            return
        f.bstack1l11lllll_opy_(instance, bstack1l1llll11l1_opy_.bstack1l1111ll1l1_opy_, bstack11ll1lll1l1_opy_)
    def bstack11lll111l11_opy_(self, context: bstack1ll11l11ll1_opy_, bstack11ll1ll1l1l_opy_= True):
        if bstack11ll1ll1l1l_opy_:
            bstack11ll1lll1l1_opy_ = self.bstack1l111llllll_opy_(context, reverse=True)
        else:
            bstack11ll1lll1l1_opy_ = self.bstack1l111llll1l_opy_(context, reverse=True)
        return [f for f in bstack11ll1lll1l1_opy_ if f[1].state != bstack1ll1l1ll11_opy_.QUIT]
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1lll11l_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if not bstack1l111l1111_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᙝ") + str(kwargs) + bstack1ll11_opy_ (u"ࠢࠣᙞ"))
            return
        bstack11ll1lll1l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1llll11l1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11ll1lll1l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙟ") + str(kwargs) + bstack1ll11_opy_ (u"ࠤࠥᙠ"))
            return
        if len(bstack11ll1lll1l1_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᙡ"))
        bstack11lll111l1l_opy_, bstack11llll11l11_opy_ = bstack11ll1lll1l1_opy_[0]
        page = bstack11lll111l1l_opy_()
        if not page:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙢ") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨᙣ"))
            return
        bstack11lll1l111_opy_ = getattr(args[0], bstack1ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᙤ"), None) or getattr(args[0], bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᙥ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᙦ")).get(bstack1ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᙧ")):
            try:
                page.evaluate(bstack1ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᙨ"),
                            bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨᙩ") + json.dumps(
                                bstack11lll1l111_opy_) + bstack1ll11_opy_ (u"ࠧࢃࡽࠣᙪ"))
            except Exception as e:
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦᙫ"), e)
    def bstack1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1lll11l_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if not bstack1l111l1111_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙬ") + str(kwargs) + bstack1ll11_opy_ (u"ࠣࠤ᙭"))
            return
        bstack11ll1lll1l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1llll11l1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11ll1lll1l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᙮") + str(kwargs) + bstack1ll11_opy_ (u"ࠥࠦᙯ"))
            return
        if len(bstack11ll1lll1l1_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᙰ"))
        bstack11lll111l1l_opy_, bstack11llll11l11_opy_ = bstack11ll1lll1l1_opy_[0]
        page = bstack11lll111l1l_opy_()
        if not page:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᙱ") + str(kwargs) + bstack1ll11_opy_ (u"ࠨࠢᙲ"))
            return
        status = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11lll11l111_opy_, None)
        if not status:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᙳ") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠣࠤᙴ"))
            return
        bstack11lll111ll1_opy_ = {bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᙵ"): status.lower()}
        bstack11ll1llll1l_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_, None)
        if status.lower() == bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙶ") and bstack11ll1llll1l_opy_ is not None:
            bstack11lll111ll1_opy_[bstack1ll11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᙷ")] = bstack11ll1llll1l_opy_[0][bstack1ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᙸ")][0] if isinstance(bstack11ll1llll1l_opy_, list) else str(bstack11ll1llll1l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᙹ")).get(bstack1ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᙺ")):
            try:
                page.evaluate(
                        bstack1ll11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᙻ"),
                        bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧᙼ")
                        + json.dumps(bstack11lll111ll1_opy_)
                        + bstack1ll11_opy_ (u"ࠥࢁࠧᙽ")
                    )
            except Exception as e:
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦᙾ"), e)
    def bstack1l11111l1ll_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        f: TestFramework,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1lll11l_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if not bstack1l111l1111_opy_:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᙿ"))
            return
        bstack11ll1lll1l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1llll11l1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11ll1lll1l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ ") + str(kwargs) + bstack1ll11_opy_ (u"ࠢࠣᚁ"))
            return
        if len(bstack11ll1lll1l1_opy_) > 1:
            self.logger.debug(
                bstack1ll11l1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᚂ"))
        bstack11lll111l1l_opy_, bstack11llll11l11_opy_ = bstack11ll1lll1l1_opy_[0]
        page = bstack11lll111l1l_opy_()
        if not page:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᚃ") + str(kwargs) + bstack1ll11_opy_ (u"ࠥࠦᚄ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll11_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤᚅ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᚆ"),
                bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᚇ").format(
                    json.dumps(
                        {
                            bstack1ll11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᚈ"): bstack1ll11_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥᚉ"),
                            bstack1ll11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᚊ"): {
                                bstack1ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣᚋ"): bstack1ll11_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣᚌ"),
                                bstack1ll11_opy_ (u"ࠧࡪࡡࡵࡣࠥᚍ"): data,
                                bstack1ll11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧᚎ"): bstack1ll11_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨᚏ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥᚐ"), e)
    def bstack1l111ll11ll_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        f: TestFramework,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1lll11l_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1llll11l1_opy_.bstack1l111l11ll1_opy_, False):
            return
        self.bstack1l1l1111l11_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1ll11_opy_ (u"ࠤࠥᚑ"))
        req.platform_index = int(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_, 0) or 0)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᚒ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l11llll_opy_, bstack1ll11_opy_ (u"ࠦࠧᚓ")) or bstack1ll11_opy_ (u"ࠧࠨᚔ"))
        req.test_framework_version = str(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11111lll1_opy_, bstack1ll11_opy_ (u"ࠨࠢᚕ")) or bstack1ll11_opy_ (u"ࠢࠣᚖ"))
        req.test_framework_state = str(bstack1ll11l11lll_opy_[0].name)
        req.test_hook_state = str(bstack1ll11l11lll_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_, bstack1ll11_opy_ (u"ࠣࠤᚗ")) or bstack1ll11_opy_ (u"ࠤࠥᚘ"))
        current_test_id = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11lll111111_opy_, None)
        bstack11ll1lll111_opy_ = 0
        bstack11lll11l11l_opy_ = 0
        for bstack11lll11l1l1_opy_ in bstack1l111lllll_opy_.bstack1l1l111l_opy_.values():
            session_id = bstack1l111lllll_opy_.bstack1ll1ll1l1l1_opy_(
                bstack11lll11l1l1_opy_,
                bstack1l111lllll_opy_.bstack1ll1l1l1lll_opy_,
                bstack1ll11_opy_ (u"ࠥࠦᚙ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1l111lllll_opy_.bstack1ll1ll1l1l1_opy_(bstack11lll11l1l1_opy_, bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡬ࡨࠬᚚ"), None)
                if instance_test_id != current_test_id:
                    bstack11lll11l11l_opy_ += 1
                    continue
                if not session_id:
                    bstack11lll11l11l_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦ᚛")
                if bstack1l111l1111_opy_
                else bstack1ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧ᚜")
            )
            session.ref = str(bstack11lll11l1l1_opy_.ref() or bstack1ll11_opy_ (u"ࠢࠣ᚝"))
            session.hub_url = str(bstack1l111lllll_opy_.bstack1ll1ll1l1l1_opy_(
                bstack11lll11l1l1_opy_,
                bstack1l111lllll_opy_.bstack1ll11l1lll_opy_,
                bstack1ll11_opy_ (u"ࠣࠤ᚞")
            ) or bstack1ll11_opy_ (u"ࠤࠥ᚟"))
            session.framework_name = str(bstack11lll11l1l1_opy_.framework_name or bstack1ll11_opy_ (u"ࠥࠦᚠ"))
            session.framework_version = str(bstack11lll11l1l1_opy_.framework_version or bstack1ll11_opy_ (u"ࠦࠧᚡ"))
            session.framework_session_id = str(session_id)
            bstack11ll1lll111_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11lll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1lll1l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1llll11l1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11ll1lll1l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᚢ") + str(kwargs) + bstack1ll11_opy_ (u"ࠨࠢᚣ"))
            return
        if len(bstack11ll1lll1l1_opy_) > 1:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᚤ") + str(kwargs) + bstack1ll11_opy_ (u"ࠣࠤᚥ"))
        bstack11lll111l1l_opy_, bstack11llll11l11_opy_ = bstack11ll1lll1l1_opy_[0]
        page = bstack11lll111l1l_opy_()
        if not page:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᚦ") + str(kwargs) + bstack1ll11_opy_ (u"ࠥࠦᚧ"))
            return
        return page
    def bstack1l11l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11ll1ll1ll1_opy_ = {}
        for bstack11lll11l1l1_opy_ in bstack1l111lllll_opy_.bstack1l1l111l_opy_.values():
            caps = bstack1l111lllll_opy_.bstack1ll1ll1l1l1_opy_(bstack11lll11l1l1_opy_, bstack1l111lllll_opy_.bstack1lll1l1111_opy_, {})
        bstack11ll1ll1ll1_opy_[bstack1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤᚨ")] = caps.get(bstack1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨᚩ"), bstack1ll11_opy_ (u"ࠨࠢᚪ"))
        bstack11ll1ll1ll1_opy_[bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᚫ")] = caps.get(bstack1ll11_opy_ (u"ࠣࡱࡶࠦᚬ"), bstack1ll11_opy_ (u"ࠤࠥᚭ"))
        bstack11ll1ll1ll1_opy_[bstack1ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᚮ")] = caps.get(bstack1ll11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᚯ"), bstack1ll11_opy_ (u"ࠧࠨᚰ"))
        bstack11ll1ll1ll1_opy_[bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢᚱ")] = caps.get(bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᚲ"), bstack1ll11_opy_ (u"ࠣࠤᚳ"))
        try:
            bstack11111lll1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_, 0) if (f and instance) else 0
            if not isinstance(bstack11111lll1_opy_, int):
                bstack11111lll1_opy_ = 0
            bstack111ll1l111_opy_ = self.config.get(bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚴ"), [])
            bstack11ll1ll1lll_opy_ = bstack111ll1l111_opy_[bstack11111lll1_opy_] if bstack11111lll1_opy_ < len(bstack111ll1l111_opy_) else self.config
            bstack11lll1111l1_opy_ = (
                bstack11ll1ll1lll_opy_.get(bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚵ"))
                or bstack11ll1ll1lll_opy_.get(bstack1ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚶ"))
                or self.config.get(bstack1ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚷ"))
                or self.config.get(bstack1ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚸ"))
            )
            if bstack11lll1111l1_opy_:
                bstack11ll1ll1ll1_opy_[bstack1ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚹ")] = bstack11lll1111l1_opy_
        except Exception as ex:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡥࡹࡺࡡࡤࡪࠣࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᚺ") + str(ex) + bstack1ll11_opy_ (u"ࠤࠥᚻ"))
        return bstack11ll1ll1ll1_opy_
    def bstack1l11lllll11_opy_(self, page: object, script_code, args={}):
        try:
            script_code = script_code.replace(bstack1ll11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᚼ"), bstack1ll11_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦᚽ"))
            if is_robot_playwright_installed():
                bstack11ll1ll1l11_opy_ = script_code.replace(bstack1ll11_opy_ (u"ࠧࡽࡩ࡯ࡦࡲࡻ࠳ࠨᚾ"), bstack1ll11_opy_ (u"ࠨࡧ࡭ࡱࡥࡥࡱ࡚ࡨࡪࡵ࠱ࠦᚿ"))
                bstack11ll1ll1l11_opy_ = bstack11ll1ll1l11_opy_.replace(bstack1ll11_opy_ (u"ࠢࡸ࡫ࡱࡨࡴࡽ࡛ࠣᛀ"), bstack1ll11_opy_ (u"ࠣࡩ࡯ࡳࡧࡧ࡬ࡕࡪ࡬ࡷࡠࠨᛁ"))
                bstack11ll1lllll1_opy_ = bstack1ll11_opy_ (u"ࠤࠥࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࠫ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡࡳࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠢࡀࠤࡠࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾ࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀࠦࠧࠨᛂ").format(fn_body=bstack11ll1ll1l11_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1ll11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡊࡼࡡ࡭ࡷࡤࡸࡪࠦࡊࡢࡸࡤࡗࡨࡸࡩࡱࡶࠪᛃ"),
                    None,
                    bstack11ll1lllll1_opy_
                )
            else:
                script_template = bstack1ll11_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤᛄ")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮ࠣࠦᛅ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᛆ"))