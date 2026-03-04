# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1llll11l_opy_,
    bstack1ll1ll11lll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11ll1l1l1_opy_, bstack1l111lll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11lll1lll_opy_ import bstack1l11lll1111_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack111ll1l1_opy_, bstack111l1111l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1l1111l1_opy_(bstack1l11lll1111_opy_):
    bstack11lllll1l11_opy_ = bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᕎ")
    bstack1l111lllll1_opy_ = bstack1lll1l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᕏ")
    bstack1l11ll111ll_opy_ = bstack1lll1l_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᕐ")
    bstack1l111111111_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᕑ")
    bstack11lllll1ll1_opy_ = bstack1lll1l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᕒ")
    bstack1l11l11l1l1_opy_ = bstack1lll1l_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᕓ")
    bstack11lllllll11_opy_ = bstack1lll1l_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᕔ")
    bstack11llll1llll_opy_ = bstack1lll1l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᕕ")
    def __init__(self):
        super().__init__(bstack1l11lll1ll1_opy_=self.bstack11lllll1l11_opy_, frameworks=[bstack1ll11l11l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11llllll1ll_opy_)
        if bstack1l111lll_opy_():
            TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1lll1_opy_)
        else:
            TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l1l1lll1_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llllll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lllll111l_opy_ = self.bstack11lllll11ll_opy_(instance.context)
        if not bstack11lllll111l_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᕖ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠥࠦᕗ"))
            return
        f.bstack1lll1l11lll_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111lllll1_opy_, bstack11lllll111l_opy_)
    def bstack11lllll11ll_opy_(self, context: bstack1ll1ll11lll_opy_, bstack11lllll1l1l_opy_= True):
        if bstack11lllll1l1l_opy_:
            bstack11lllll111l_opy_ = self.bstack1l11ll1l1ll_opy_(context, reverse=True)
        else:
            bstack11lllll111l_opy_ = self.bstack1l11lll11ll_opy_(context, reverse=True)
        return [f for f in bstack11lllll111l_opy_ if f[1].state != bstack1ll1l1l11ll_opy_.QUIT]
    def bstack1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llllll1ll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l11ll1l1l1_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᕘ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨᕙ"))
            return
        bstack11lllll111l_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111lllll1_opy_, [])
        if not bstack11lllll111l_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᕚ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠢࠣᕛ"))
            return
        if len(bstack11lllll111l_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1ll11l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥᕜ"))
        bstack11lllll11l1_opy_, bstack1l1111ll111_opy_ = bstack11lllll111l_opy_[0]
        page = bstack11lllll11l1_opy_()
        if not page:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᕝ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠥࠦᕞ"))
            return
        bstack1l11111ll1_opy_ = getattr(args[0], bstack1lll1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᕟ"), None) or getattr(args[0], bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᕠ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᕡ")).get(bstack1lll1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᕢ")):
            try:
                page.evaluate(bstack1lll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᕣ"),
                            bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᕤ") + json.dumps(
                                bstack1l11111ll1_opy_) + bstack1lll1l_opy_ (u"ࠥࢁࢂࠨᕥ"))
            except Exception as e:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᕦ"), e)
    def bstack1l1l1l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llllll1ll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l11ll1l1l1_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᕧ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠨࠢᕨ"))
            return
        bstack11lllll111l_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111lllll1_opy_, [])
        if not bstack11lllll111l_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕩ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤᕪ"))
            return
        if len(bstack11lllll111l_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1ll11l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᕫ"))
        bstack11lllll11l1_opy_, bstack1l1111ll111_opy_ = bstack11lllll111l_opy_[0]
        page = bstack11lllll11l1_opy_()
        if not page:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕬ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠦࠧᕭ"))
            return
        status = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1111111l1_opy_, None)
        if not status:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᕮ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠨࠢᕯ"))
            return
        bstack11llllllll1_opy_ = {bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᕰ"): status.lower()}
        bstack11llllll11l_opy_ = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11llllll1l1_opy_, None)
        if status.lower() == bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᕱ") and bstack11llllll11l_opy_ is not None:
            bstack11llllllll1_opy_[bstack1lll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᕲ")] = bstack11llllll11l_opy_[0][bstack1lll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᕳ")][0] if isinstance(bstack11llllll11l_opy_, list) else str(bstack11llllll11l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᕴ")).get(bstack1lll1l_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᕵ")):
            try:
                page.evaluate(
                        bstack1lll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᕶ"),
                        bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬᕷ")
                        + json.dumps(bstack11llllllll1_opy_)
                        + bstack1lll1l_opy_ (u"ࠣࡿࠥᕸ")
                    )
            except Exception as e:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᕹ"), e)
    def bstack1l11l1l1l11_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llllll1ll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not bstack1l11ll1l1l1_opy_:
            self.logger.debug(
                bstack1ll1l1ll11l_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᕺ"))
            return
        bstack11lllll111l_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111lllll1_opy_, [])
        if not bstack11lllll111l_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᕻ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨᕼ"))
            return
        if len(bstack11lllll111l_opy_) > 1:
            self.logger.debug(
                bstack1ll1l1ll11l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᕽ"))
        bstack11lllll11l1_opy_, bstack1l1111ll111_opy_ = bstack11lllll111l_opy_[0]
        page = bstack11lllll11l1_opy_()
        if not page:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᕾ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤᕿ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1lll1l_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᖀ") + str(timestamp)
        try:
            page.evaluate(
                bstack1lll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᖁ"),
                bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᖂ").format(
                    json.dumps(
                        {
                            bstack1lll1l_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᖃ"): bstack1lll1l_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᖄ"),
                            bstack1lll1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᖅ"): {
                                bstack1lll1l_opy_ (u"ࠣࡶࡼࡴࡪࠨᖆ"): bstack1lll1l_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᖇ"),
                                bstack1lll1l_opy_ (u"ࠥࡨࡦࡺࡡࠣᖈ"): data,
                                bstack1lll1l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᖉ"): bstack1lll1l_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᖊ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣᖋ"), e)
    def bstack1l11l1l111l_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11llllll1ll_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l11l11l1l1_opy_, False):
            return
        self.bstack1l1l1111ll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1lll1l_opy_ (u"ࠢࠣᖌ"))
        req.platform_index = int(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, 0) or 0)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᖍ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_, bstack1lll1l_opy_ (u"ࠤࠥᖎ")) or bstack1lll1l_opy_ (u"ࠥࠦᖏ"))
        req.test_framework_version = str(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l11l11l1ll_opy_, bstack1lll1l_opy_ (u"ࠦࠧᖐ")) or bstack1lll1l_opy_ (u"ࠧࠨᖑ"))
        req.test_framework_state = str(bstack1ll1ll1ll1l_opy_[0].name)
        req.test_hook_state = str(bstack1ll1ll1ll1l_opy_[1].name)
        req.test_uuid = str(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_, bstack1lll1l_opy_ (u"ࠨࠢᖒ")) or bstack1lll1l_opy_ (u"ࠢࠣᖓ"))
        current_test_id = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11lllll1111_opy_, None)
        bstack1l11111111l_opy_ = 0
        bstack11lllll1lll_opy_ = 0
        for bstack11lllllll1l_opy_ in bstack1lll111l1ll_opy_.bstack1lll1l1111l_opy_.values():
            session_id = bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(
                bstack11lllllll1l_opy_,
                bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_,
                bstack1lll1l_opy_ (u"ࠣࠤᖔ")
            )
            if is_robot_playwright_installed():
                instance_test_id = bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(bstack11lllllll1l_opy_, bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪᖕ"), None)
                if instance_test_id != current_test_id:
                    bstack11lllll1lll_opy_ += 1
                    continue
                if not session_id:
                    bstack11lllll1lll_opy_ += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᖖ")
                if bstack1l11ll1l1l1_opy_
                else bstack1lll1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᖗ")
            )
            session.ref = str(bstack11lllllll1l_opy_.ref() or bstack1lll1l_opy_ (u"ࠧࠨᖘ"))
            session.hub_url = str(bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(
                bstack11lllllll1l_opy_,
                bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_,
                bstack1lll1l_opy_ (u"ࠨࠢᖙ")
            ) or bstack1lll1l_opy_ (u"ࠢࠣᖚ"))
            session.framework_name = str(bstack11lllllll1l_opy_.framework_name or bstack1lll1l_opy_ (u"ࠣࠤᖛ"))
            session.framework_version = str(bstack11lllllll1l_opy_.framework_version or bstack1lll1l_opy_ (u"ࠤࠥᖜ"))
            session.framework_session_id = str(session_id)
            bstack1l11111111l_opy_ += 1
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lllll111l_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111lllll1_opy_, [])
        if not bstack11lllll111l_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᖝ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠦࠧᖞ"))
            return
        if len(bstack11lllll111l_opy_) > 1:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᖟ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠨࠢᖠ"))
        bstack11lllll11l1_opy_, bstack1l1111ll111_opy_ = bstack11lllll111l_opy_[0]
        page = bstack11lllll11l1_opy_()
        if not page:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᖡ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤᖢ"))
            return
        return page
    def bstack1l1l11ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        bstack11lllllllll_opy_ = {}
        for bstack11lllllll1l_opy_ in bstack1lll111l1ll_opy_.bstack1lll1l1111l_opy_.values():
            caps = bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(bstack11lllllll1l_opy_, bstack1lll111l1ll_opy_.bstack1lll11ll1l1_opy_, {})
        bstack11lllllllll_opy_[bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᖣ")] = caps.get(bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᖤ"), bstack1lll1l_opy_ (u"ࠦࠧᖥ"))
        bstack11lllllllll_opy_[bstack1lll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᖦ")] = caps.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡴࠤᖧ"), bstack1lll1l_opy_ (u"ࠢࠣᖨ"))
        bstack11lllllllll_opy_[bstack1lll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᖩ")] = caps.get(bstack1lll1l_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᖪ"), bstack1lll1l_opy_ (u"ࠥࠦᖫ"))
        bstack11lllllllll_opy_[bstack1lll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᖬ")] = caps.get(bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᖭ"), bstack1lll1l_opy_ (u"ࠨࠢᖮ"))
        return bstack11lllllllll_opy_
    def bstack1l1l1llll11_opy_(self, page: object, bstack1l1l11ll111_opy_, args={}):
        try:
            bstack11llllll111_opy_ = bstack1lll1l_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᖯ")
            bstack1l1l11ll111_opy_ = bstack1l1l11ll111_opy_.replace(bstack1lll1l_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᖰ"), bstack1lll1l_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᖱ"))
            script = bstack11llllll111_opy_.format(fn_body=bstack1l1l11ll111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᖲ") + str(e) + bstack1lll1l_opy_ (u"ࠦࠧᖳ"))