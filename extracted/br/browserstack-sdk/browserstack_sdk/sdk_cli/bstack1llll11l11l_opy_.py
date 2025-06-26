# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1111111l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11111_opy_, bstack1lll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_, bstack1ll1l1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll111111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111ll_opy_ import bstack1ll111111l1_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l1l111_opy_ import bstack1l11llll_opy_, bstack1l1ll11lll_opy_, bstack1lllll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1l111ll_opy_(bstack1ll111111l1_opy_):
    bstack1l1l1111l11_opy_ = bstack11ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢዊ")
    bstack1l1l1ll1lll_opy_ = bstack11ll1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣዋ")
    bstack1l1l111l111_opy_ = bstack11ll1l1_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧዌ")
    bstack1l1l1111lll_opy_ = bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦው")
    bstack1l1l11111ll_opy_ = bstack11ll1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤዎ")
    bstack1l1ll1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧዏ")
    bstack1l1l11l11l1_opy_ = bstack11ll1l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥዐ")
    bstack1l1l111llll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨዑ")
    def __init__(self):
        super().__init__(bstack1l1lllll1ll_opy_=self.bstack1l1l1111l11_opy_, frameworks=[bstack1ll1lllllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.BEFORE_EACH, bstack1lll1111l1l_opy_.POST), self.bstack1l1l111ll11_opy_)
        if bstack1lll111l_opy_():
            TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), self.bstack1ll111l11ll_opy_)
        else:
            TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.PRE), self.bstack1ll111l11ll_opy_)
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1111l1l_opy_ = self.bstack1l1l111l1l1_opy_(instance.context)
        if not bstack1l1l1111l1l_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢዒ") + str(bstack1llllllllll_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦዓ"))
            return
        f.bstack1lllll1ll1l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, bstack1l1l1111l1l_opy_)
    def bstack1l1l111l1l1_opy_(self, context: bstack1lllllll1ll_opy_, bstack1l1l1111ll1_opy_= True):
        if bstack1l1l1111ll1_opy_:
            bstack1l1l1111l1l_opy_ = self.bstack1ll11111111_opy_(context, reverse=True)
        else:
            bstack1l1l1111l1l_opy_ = self.bstack1l1llllll1l_opy_(context, reverse=True)
        return [f for f in bstack1l1l1111l1l_opy_ if f[1].state != bstack1lllll1ll11_opy_.QUIT]
    def bstack1ll111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll11_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዔ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠧࠨዕ"))
            return
        bstack1l1l1111l1l_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, [])
        if not bstack1l1l1111l1l_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዖ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠢࠣ዗"))
            return
        if len(bstack1l1l1111l1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥዘ"))
        bstack1l1l11l111l_opy_, bstack1l1l1l1ll1l_opy_ = bstack1l1l1111l1l_opy_[0]
        page = bstack1l1l11l111l_opy_()
        if not page:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዙ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦዚ"))
            return
        bstack11llll111l_opy_ = getattr(args[0], bstack11ll1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦዛ"), None)
        try:
            page.evaluate(bstack11ll1l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨዜ"),
                        bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪዝ") + json.dumps(
                            bstack11llll111l_opy_) + bstack11ll1l1_opy_ (u"ࠢࡾࡿࠥዞ"))
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨዟ"), e)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll11_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዠ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦዡ"))
            return
        bstack1l1l1111l1l_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, [])
        if not bstack1l1l1111l1l_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዢ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠧࠨዣ"))
            return
        if len(bstack1l1l1111l1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1111l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣዤ"))
        bstack1l1l11l111l_opy_, bstack1l1l1l1ll1l_opy_ = bstack1l1l1111l1l_opy_[0]
        page = bstack1l1l11l111l_opy_()
        if not page:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዥ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠣࠤዦ"))
            return
        status = f.bstack11111111ll_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_, None)
        if not status:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧዧ") + str(bstack1llllllllll_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦየ"))
            return
        bstack1l1l11111l1_opy_ = {bstack11ll1l1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦዩ"): status.lower()}
        bstack1l1l111lll1_opy_ = f.bstack11111111ll_opy_(instance, TestFramework.bstack1l1l111l1ll_opy_, None)
        if status.lower() == bstack11ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዪ") and bstack1l1l111lll1_opy_ is not None:
            bstack1l1l11111l1_opy_[bstack11ll1l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ያ")] = bstack1l1l111lll1_opy_[0][bstack11ll1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪዬ")][0] if isinstance(bstack1l1l111lll1_opy_, list) else str(bstack1l1l111lll1_opy_)
        try:
              page.evaluate(
                    bstack11ll1l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤይ"),
                    bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧዮ")
                    + json.dumps(bstack1l1l11111l1_opy_)
                    + bstack11ll1l1_opy_ (u"ࠥࢁࠧዯ")
                )
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦደ"), e)
    def bstack1l1ll1l1ll1_opy_(
        self,
        instance: bstack1ll1l1lll1l_opy_,
        f: TestFramework,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll11_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(
                bstack1llll1111l1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨዱ"))
            return
        bstack1l1l1111l1l_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, [])
        if not bstack1l1l1111l1l_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዲ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠢࠣዳ"))
            return
        if len(bstack1l1l1111l1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥዴ"))
        bstack1l1l11l111l_opy_, bstack1l1l1l1ll1l_opy_ = bstack1l1l1111l1l_opy_[0]
        page = bstack1l1l11l111l_opy_()
        if not page:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤድ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦዶ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11ll1l1_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤዷ") + str(timestamp)
        try:
            page.evaluate(
                bstack11ll1l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨዸ"),
                bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫዹ").format(
                    json.dumps(
                        {
                            bstack11ll1l1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢዺ"): bstack11ll1l1_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥዻ"),
                            bstack11ll1l1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧዼ"): {
                                bstack11ll1l1_opy_ (u"ࠥࡸࡾࡶࡥࠣዽ"): bstack11ll1l1_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣዾ"),
                                bstack11ll1l1_opy_ (u"ࠧࡪࡡࡵࡣࠥዿ"): data,
                                bstack11ll1l1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጀ"): bstack11ll1l1_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨጁ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥጂ"), e)
    def bstack1l1ll1lll11_opy_(
        self,
        instance: bstack1ll1l1lll1l_opy_,
        f: TestFramework,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll11_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        if f.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1ll1l1111_opy_, False):
            return
        self.bstack1ll11llllll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111ll11l_opy_)
        req.test_framework_name = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11lll111_opy_)
        req.test_framework_version = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_)
        req.test_framework_state = bstack1llllllllll_opy_[0].name
        req.test_hook_state = bstack1llllllllll_opy_[1].name
        req.test_uuid = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11l11l11_opy_)
        for bstack1l1l111l11l_opy_ in bstack1lll111111l_opy_.bstack1llllll11l1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣጃ")
                if bstack1l1lll11111_opy_
                else bstack11ll1l1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤጄ")
            )
            session.ref = bstack1l1l111l11l_opy_.ref()
            session.hub_url = bstack1lll111111l_opy_.bstack11111111ll_opy_(bstack1l1l111l11l_opy_, bstack1lll111111l_opy_.bstack1l1l11lllll_opy_, bstack11ll1l1_opy_ (u"ࠦࠧጅ"))
            session.framework_name = bstack1l1l111l11l_opy_.framework_name
            session.framework_version = bstack1l1l111l11l_opy_.framework_version
            session.framework_session_id = bstack1lll111111l_opy_.bstack11111111ll_opy_(bstack1l1l111l11l_opy_, bstack1lll111111l_opy_.bstack1l1l11l11ll_opy_, bstack11ll1l1_opy_ (u"ࠧࠨጆ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1111l1l_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, [])
        if not bstack1l1l1111l1l_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጇ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠢࠣገ"))
            return
        if len(bstack1l1l1111l1l_opy_) > 1:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጉ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠤࠥጊ"))
        bstack1l1l11l111l_opy_, bstack1l1l1l1ll1l_opy_ = bstack1l1l1111l1l_opy_[0]
        page = bstack1l1l11l111l_opy_()
        if not page:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጋ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠦࠧጌ"))
            return
        return page
    def bstack1ll11ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l11l1111_opy_ = {}
        for bstack1l1l111l11l_opy_ in bstack1lll111111l_opy_.bstack1llllll11l1_opy_.values():
            caps = bstack1lll111111l_opy_.bstack11111111ll_opy_(bstack1l1l111l11l_opy_, bstack1lll111111l_opy_.bstack1l1l1l11111_opy_, bstack11ll1l1_opy_ (u"ࠧࠨግ"))
        bstack1l1l11l1111_opy_[bstack11ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦጎ")] = caps.get(bstack11ll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣጏ"), bstack11ll1l1_opy_ (u"ࠣࠤጐ"))
        bstack1l1l11l1111_opy_[bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ጑")] = caps.get(bstack11ll1l1_opy_ (u"ࠥࡳࡸࠨጒ"), bstack11ll1l1_opy_ (u"ࠦࠧጓ"))
        bstack1l1l11l1111_opy_[bstack11ll1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢጔ")] = caps.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥጕ"), bstack11ll1l1_opy_ (u"ࠢࠣ጖"))
        bstack1l1l11l1111_opy_[bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ጗")] = caps.get(bstack11ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦጘ"), bstack11ll1l1_opy_ (u"ࠥࠦጙ"))
        return bstack1l1l11l1111_opy_
    def bstack1ll111llll1_opy_(self, page: object, bstack1ll1l111111_opy_, args={}):
        try:
            bstack1l1l111111l_opy_ = bstack11ll1l1_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥጚ")
            bstack1ll1l111111_opy_ = bstack1ll1l111111_opy_.replace(bstack11ll1l1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጛ"), bstack11ll1l1_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨጜ"))
            script = bstack1l1l111111l_opy_.format(fn_body=bstack1ll1l111111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨጝ") + str(e) + bstack11ll1l1_opy_ (u"ࠣࠤጞ"))