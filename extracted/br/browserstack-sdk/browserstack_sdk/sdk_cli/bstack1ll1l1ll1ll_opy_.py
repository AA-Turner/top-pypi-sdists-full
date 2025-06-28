# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1111111ll1_opy_,
    bstack1111111l1l_opy_,
    bstack1lllll1l1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11111_opy_, bstack1ll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_, bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l11l_opy_ import bstack1lll1lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1llll1111l_opy_ import bstack111111ll1_opy_, bstack1l1ll1lll1_opy_, bstack1ll1111l11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1l1l1l1_opy_(bstack1ll11111111_opy_):
    bstack1l1l11111l1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢዊ")
    bstack1l1ll11ll11_opy_ = bstack1l1ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣዋ")
    bstack1l1l111llll_opy_ = bstack1l1ll1_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧዌ")
    bstack1l1l1111l1l_opy_ = bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦው")
    bstack1l1l1111lll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤዎ")
    bstack1l1l1ll1ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧዏ")
    bstack1l1l11l11ll_opy_ = bstack1l1ll1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥዐ")
    bstack1l1l111lll1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨዑ")
    def __init__(self):
        super().__init__(bstack1ll111111ll_opy_=self.bstack1l1l11111l1_opy_, frameworks=[bstack1lll1l1l1ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.BEFORE_EACH, bstack1ll1lllll1l_opy_.POST), self.bstack1l1l1111l11_opy_)
        if bstack1ll11l111l_opy_():
            TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST), self.bstack1ll11ll111l_opy_)
        else:
            TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.PRE), self.bstack1ll11ll111l_opy_)
        TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST), self.bstack1ll11l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11111ll_opy_ = self.bstack1l1l11l111l_opy_(instance.context)
        if not bstack1l1l11111ll_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢዒ") + str(bstack1llllll1111_opy_) + bstack1l1ll1_opy_ (u"ࠥࠦዓ"))
            return
        f.bstack1lllllll1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, bstack1l1l11111ll_opy_)
    def bstack1l1l11l111l_opy_(self, context: bstack1lllll1l1l1_opy_, bstack1l1l111l1l1_opy_= True):
        if bstack1l1l111l1l1_opy_:
            bstack1l1l11111ll_opy_ = self.bstack1l1lllll111_opy_(context, reverse=True)
        else:
            bstack1l1l11111ll_opy_ = self.bstack1l1llllll11_opy_(context, reverse=True)
        return [f for f in bstack1l1l11111ll_opy_ if f[1].state != bstack1lllll1lll1_opy_.QUIT]
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዔ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠧࠨዕ"))
            return
        bstack1l1l11111ll_opy_ = f.bstack111111l111_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11111ll_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዖ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠢࠣ዗"))
            return
        if len(bstack1l1l11111ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥዘ"))
        bstack1l1l111l111_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l11111ll_opy_[0]
        page = bstack1l1l111l111_opy_()
        if not page:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዙ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠥࠦዚ"))
            return
        bstack1llll1ll1l_opy_ = getattr(args[0], bstack1l1ll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦዛ"), None)
        try:
            page.evaluate(bstack1l1ll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨዜ"),
                        bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪዝ") + json.dumps(
                            bstack1llll1ll1l_opy_) + bstack1l1ll1_opy_ (u"ࠢࡾࡿࠥዞ"))
        except Exception as e:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨዟ"), e)
    def bstack1ll11l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዠ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠥࠦዡ"))
            return
        bstack1l1l11111ll_opy_ = f.bstack111111l111_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11111ll_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዢ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠧࠨዣ"))
            return
        if len(bstack1l1l11111ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣዤ"))
        bstack1l1l111l111_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l11111ll_opy_[0]
        page = bstack1l1l111l111_opy_()
        if not page:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዥ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠣࠤዦ"))
            return
        status = f.bstack111111l111_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, None)
        if not status:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧዧ") + str(bstack1llllll1111_opy_) + bstack1l1ll1_opy_ (u"ࠥࠦየ"))
            return
        bstack1l1l11l11l1_opy_ = {bstack1l1ll1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦዩ"): status.lower()}
        bstack1l1l111l1ll_opy_ = f.bstack111111l111_opy_(instance, TestFramework.bstack1l1l11l1111_opy_, None)
        if status.lower() == bstack1l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዪ") and bstack1l1l111l1ll_opy_ is not None:
            bstack1l1l11l11l1_opy_[bstack1l1ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ያ")] = bstack1l1l111l1ll_opy_[0][bstack1l1ll1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪዬ")][0] if isinstance(bstack1l1l111l1ll_opy_, list) else str(bstack1l1l111l1ll_opy_)
        try:
              page.evaluate(
                    bstack1l1ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤይ"),
                    bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧዮ")
                    + json.dumps(bstack1l1l11l11l1_opy_)
                    + bstack1l1ll1_opy_ (u"ࠥࢁࠧዯ")
                )
        except Exception as e:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦደ"), e)
    def bstack1l1llll1ll1_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        f: TestFramework,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll11111_opy_:
            self.logger.debug(
                bstack1lll1l11ll1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨዱ"))
            return
        bstack1l1l11111ll_opy_ = f.bstack111111l111_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11111ll_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዲ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠢࠣዳ"))
            return
        if len(bstack1l1l11111ll_opy_) > 1:
            self.logger.debug(
                bstack1lll1l11ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥዴ"))
        bstack1l1l111l111_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l11111ll_opy_[0]
        page = bstack1l1l111l111_opy_()
        if not page:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤድ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠥࠦዶ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1ll1_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤዷ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1ll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨዸ"),
                bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫዹ").format(
                    json.dumps(
                        {
                            bstack1l1ll1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢዺ"): bstack1l1ll1_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥዻ"),
                            bstack1l1ll1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧዼ"): {
                                bstack1l1ll1_opy_ (u"ࠥࡸࡾࡶࡥࠣዽ"): bstack1l1ll1_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣዾ"),
                                bstack1l1ll1_opy_ (u"ࠧࡪࡡࡵࡣࠥዿ"): data,
                                bstack1l1ll1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጀ"): bstack1l1ll1_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨጁ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥጂ"), e)
    def bstack1l1lll11l1l_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        f: TestFramework,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if f.bstack111111l111_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l1ll1ll1_opy_, False):
            return
        self.bstack1ll111ll1ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll11l1l111_opy_)
        req.test_framework_name = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll1l11l1ll_opy_)
        req.test_framework_version = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_state = bstack1llllll1111_opy_[0].name
        req.test_hook_state = bstack1llllll1111_opy_[1].name
        req.test_uuid = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
        for bstack1l1l111ll1l_opy_ in bstack1lll1lll1ll_opy_.bstack1llllll1ll1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣጃ")
                if bstack1l1lll11111_opy_
                else bstack1l1ll1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤጄ")
            )
            session.ref = bstack1l1l111ll1l_opy_.ref()
            session.hub_url = bstack1lll1lll1ll_opy_.bstack111111l111_opy_(bstack1l1l111ll1l_opy_, bstack1lll1lll1ll_opy_.bstack1l1l11ll11l_opy_, bstack1l1ll1_opy_ (u"ࠦࠧጅ"))
            session.framework_name = bstack1l1l111ll1l_opy_.framework_name
            session.framework_version = bstack1l1l111ll1l_opy_.framework_version
            session.framework_session_id = bstack1lll1lll1ll_opy_.bstack111111l111_opy_(bstack1l1l111ll1l_opy_, bstack1lll1lll1ll_opy_.bstack1l1l11l1ll1_opy_, bstack1l1ll1_opy_ (u"ࠧࠨጆ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11111ll_opy_ = f.bstack111111l111_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11111ll_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጇ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠢࠣገ"))
            return
        if len(bstack1l1l11111ll_opy_) > 1:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጉ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠤࠥጊ"))
        bstack1l1l111l111_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l11111ll_opy_[0]
        page = bstack1l1l111l111_opy_()
        if not page:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጋ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠦࠧጌ"))
            return
        return page
    def bstack1ll11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111ll11_opy_ = {}
        for bstack1l1l111ll1l_opy_ in bstack1lll1lll1ll_opy_.bstack1llllll1ll1_opy_.values():
            caps = bstack1lll1lll1ll_opy_.bstack111111l111_opy_(bstack1l1l111ll1l_opy_, bstack1lll1lll1ll_opy_.bstack1l1l11llll1_opy_, bstack1l1ll1_opy_ (u"ࠧࠨግ"))
        bstack1l1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦጎ")] = caps.get(bstack1l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣጏ"), bstack1l1ll1_opy_ (u"ࠣࠤጐ"))
        bstack1l1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ጑")] = caps.get(bstack1l1ll1_opy_ (u"ࠥࡳࡸࠨጒ"), bstack1l1ll1_opy_ (u"ࠦࠧጓ"))
        bstack1l1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢጔ")] = caps.get(bstack1l1ll1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥጕ"), bstack1l1ll1_opy_ (u"ࠢࠣ጖"))
        bstack1l1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ጗")] = caps.get(bstack1l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦጘ"), bstack1l1ll1_opy_ (u"ࠥࠦጙ"))
        return bstack1l1l111ll11_opy_
    def bstack1ll11l11111_opy_(self, page: object, bstack1ll11lll1ll_opy_, args={}):
        try:
            bstack1l1l1111ll1_opy_ = bstack1l1ll1_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥጚ")
            bstack1ll11lll1ll_opy_ = bstack1ll11lll1ll_opy_.replace(bstack1l1ll1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጛ"), bstack1l1ll1_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨጜ"))
            script = bstack1l1l1111ll1_opy_.format(fn_body=bstack1ll11lll1ll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨጝ") + str(e) + bstack1l1ll1_opy_ (u"ࠣࠤጞ"))