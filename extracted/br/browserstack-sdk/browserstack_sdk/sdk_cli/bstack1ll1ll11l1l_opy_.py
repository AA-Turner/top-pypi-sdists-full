# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1111111111_opy_,
    bstack1lllll1ll1l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11ll1_opy_, bstack11lll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1ll11111lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1111ll1l_opy_ import bstack11l11ll1_opy_, bstack1111ll1ll_opy_, bstack11llll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1ll1l1l_opy_(bstack1ll11111lll_opy_):
    bstack1l1l11l1111_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥኪ")
    bstack1l1ll1l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦካ")
    bstack1l1l11l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣኬ")
    bstack1l1l11l1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢክ")
    bstack1l1l111lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧኮ")
    bstack1l1ll1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣኯ")
    bstack1l1l11l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨኰ")
    bstack1l1l11ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤ኱")
    def __init__(self):
        super().__init__(bstack1ll1111l111_opy_=self.bstack1l1l11l1111_opy_, frameworks=[bstack1llll111lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.BEFORE_EACH, bstack1lll1lll111_opy_.POST), self.bstack1l1l111l1ll_opy_)
        if bstack11lll111l1_opy_():
            TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll11l1l111_opy_)
        else:
            TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE), self.bstack1ll11l1l111_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll1l11ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11l1ll1_opy_ = self.bstack1l1l11l1l1l_opy_(instance.context)
        if not bstack1l1l11l1ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥኲ") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢኳ"))
            return
        f.bstack1lllll1111l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1l111l_opy_, bstack1l1l11l1ll1_opy_)
    def bstack1l1l11l1l1l_opy_(self, context: bstack1lllll1ll1l_opy_, bstack1l1l11ll11l_opy_= True):
        if bstack1l1l11ll11l_opy_:
            bstack1l1l11l1ll1_opy_ = self.bstack1ll1111l1l1_opy_(context, reverse=True)
        else:
            bstack1l1l11l1ll1_opy_ = self.bstack1ll11111l1l_opy_(context, reverse=True)
        return [f for f in bstack1l1l11l1ll1_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    def bstack1ll11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኴ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠣࠤኵ"))
            return
        bstack1l1l11l1ll1_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1l11l1ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ኶") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠥࠦ኷"))
            return
        if len(bstack1l1l11l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll1l11l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨኸ"))
        bstack1l1l11ll1ll_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1l11l1ll1_opy_[0]
        page = bstack1l1l11ll1ll_opy_()
        if not page:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧኹ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢኺ"))
            return
        bstack1l11l1l11l_opy_ = getattr(args[0], bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢኻ"), None)
        try:
            page.evaluate(bstack1l1l1l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤኼ"),
                        bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ኽ") + json.dumps(
                            bstack1l11l1l11l_opy_) + bstack1l1l1l1_opy_ (u"ࠥࢁࢂࠨኾ"))
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ኿"), e)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዀ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢ዁"))
            return
        bstack1l1l11l1ll1_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1l11l1ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዂ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠣࠤዃ"))
            return
        if len(bstack1l1l11l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll1l11l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦዄ"))
        bstack1l1l11ll1ll_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1l11l1ll1_opy_[0]
        page = bstack1l1l11ll1ll_opy_()
        if not page:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዅ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧ዆"))
            return
        status = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_, None)
        if not status:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣ዇") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢወ"))
            return
        bstack1l1l111llll_opy_ = {bstack1l1l1l1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢዉ"): status.lower()}
        bstack1l1l11l11l1_opy_ = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1l111l1l1_opy_, None)
        if status.lower() == bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዊ") and bstack1l1l11l11l1_opy_ is not None:
            bstack1l1l111llll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩዋ")] = bstack1l1l11l11l1_opy_[0][bstack1l1l1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ዌ")][0] if isinstance(bstack1l1l11l11l1_opy_, list) else str(bstack1l1l11l11l1_opy_)
        try:
              page.evaluate(
                    bstack1l1l1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧው"),
                    bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࠪዎ")
                    + json.dumps(bstack1l1l111llll_opy_)
                    + bstack1l1l1l1_opy_ (u"ࠨࡽࠣዏ")
                )
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢዐ"), e)
    def bstack1l1ll1l11l1_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(
                bstack1llll1l11l1_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤዑ"))
            return
        bstack1l1l11l1ll1_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1l11l1ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዒ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠥࠦዓ"))
            return
        if len(bstack1l1l11l1ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll1l11l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨዔ"))
        bstack1l1l11ll1ll_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1l11l1ll1_opy_[0]
        page = bstack1l1l11ll1ll_opy_()
        if not page:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዕ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢዖ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1l1l1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧ዗") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1l1l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤዘ"),
                bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧዙ").format(
                    json.dumps(
                        {
                            bstack1l1l1l1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥዚ"): bstack1l1l1l1_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨዛ"),
                            bstack1l1l1l1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣዜ"): {
                                bstack1l1l1l1_opy_ (u"ࠨࡴࡺࡲࡨࠦዝ"): bstack1l1l1l1_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦዞ"),
                                bstack1l1l1l1_opy_ (u"ࠣࡦࡤࡸࡦࠨዟ"): data,
                                bstack1l1l1l1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣዠ"): bstack1l1l1l1_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤዡ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡰ࠳࠴ࡽࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡿࢂࠨዢ"), e)
    def bstack1l1lll1llll_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1ll111_opy_, False):
            return
        self.bstack1ll11l1l1ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
        for bstack1l1l111ll1l_opy_ in bstack1ll1lllllll_opy_.bstack1llllllll11_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦዣ")
                if bstack1l1lll11ll1_opy_
                else bstack1l1l1l1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧዤ")
            )
            session.ref = bstack1l1l111ll1l_opy_.ref()
            session.hub_url = bstack1ll1lllllll_opy_.bstack1lllll1ll11_opy_(bstack1l1l111ll1l_opy_, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, bstack1l1l1l1_opy_ (u"ࠢࠣዥ"))
            session.framework_name = bstack1l1l111ll1l_opy_.framework_name
            session.framework_version = bstack1l1l111ll1l_opy_.framework_version
            session.framework_session_id = bstack1ll1lllllll_opy_.bstack1lllll1ll11_opy_(bstack1l1l111ll1l_opy_, bstack1ll1lllllll_opy_.bstack1l1l11lll1l_opy_, bstack1l1l1l1_opy_ (u"ࠣࠤዦ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11l1ll1_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1l11l1ll1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዧ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠥࠦየ"))
            return
        if len(bstack1l1l11l1ll1_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዩ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠧࠨዪ"))
        bstack1l1l11ll1ll_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1l11l1ll1_opy_[0]
        page = bstack1l1l11ll1ll_opy_()
        if not page:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨያ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠢࠣዬ"))
            return
        return page
    def bstack1ll11ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l11l1lll_opy_ = {}
        for bstack1l1l111ll1l_opy_ in bstack1ll1lllllll_opy_.bstack1llllllll11_opy_.values():
            caps = bstack1ll1lllllll_opy_.bstack1lllll1ll11_opy_(bstack1l1l111ll1l_opy_, bstack1ll1lllllll_opy_.bstack1l1l1l1lll1_opy_, bstack1l1l1l1_opy_ (u"ࠣࠤይ"))
        bstack1l1l11l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢዮ")] = caps.get(bstack1l1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦዯ"), bstack1l1l1l1_opy_ (u"ࠦࠧደ"))
        bstack1l1l11l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦዱ")] = caps.get(bstack1l1l1l1_opy_ (u"ࠨ࡯ࡴࠤዲ"), bstack1l1l1l1_opy_ (u"ࠢࠣዳ"))
        bstack1l1l11l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥዴ")] = caps.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨድ"), bstack1l1l1l1_opy_ (u"ࠥࠦዶ"))
        bstack1l1l11l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧዷ")] = caps.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢዸ"), bstack1l1l1l1_opy_ (u"ࠨࠢዹ"))
        return bstack1l1l11l1lll_opy_
    def bstack1ll1l1l1111_opy_(self, page: object, bstack1ll11l111l1_opy_, args={}):
        try:
            bstack1l1l11ll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨዺ")
            bstack1ll11l111l1_opy_ = bstack1ll11l111l1_opy_.replace(bstack1l1l1l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦዻ"), bstack1l1l1l1_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤዼ"))
            script = bstack1l1l11ll1l1_opy_.format(fn_body=bstack1ll11l111l1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤዽ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧዾ"))