# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1lllllll1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll111ll1_opy_, bstack111ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_, bstack1llll111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll1l_opy_ import bstack1ll1111ll11_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1l11l11l_opy_ import bstack11l1lll11_opy_, bstack11l1l1l11l_opy_, bstack11lll1l11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll111111_opy_(bstack1ll1111ll11_opy_):
    bstack1l1l111lll1_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤኩ")
    bstack1l1ll11ll11_opy_ = bstack11ll11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥኪ")
    bstack1l1l11l1l1l_opy_ = bstack11ll11_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢካ")
    bstack1l1l11ll11l_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨኬ")
    bstack1l1l11l1111_opy_ = bstack11ll11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦክ")
    bstack1l1llllll11_opy_ = bstack11ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢኮ")
    bstack1l1l11ll1l1_opy_ = bstack11ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧኯ")
    bstack1l1l111l1ll_opy_ = bstack11ll11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣኰ")
    def __init__(self):
        super().__init__(bstack1ll111111ll_opy_=self.bstack1l1l111lll1_opy_, frameworks=[bstack1llll11l111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.BEFORE_EACH, bstack1ll1l1lll11_opy_.POST), self.bstack1l1l11l111l_opy_)
        if bstack111ll11l_opy_():
            TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll11ll1l1l_opy_)
        else:
            TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE), self.bstack1ll11ll1l1l_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll1l111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11ll1ll_opy_ = self.bstack1l1l111l1l1_opy_(instance.context)
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤ኱") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠧࠨኲ"))
            return
        f.bstack1llllllllll_opy_(instance, bstack1llll111111_opy_.bstack1l1ll11ll11_opy_, bstack1l1l11ll1ll_opy_)
    def bstack1l1l111l1l1_opy_(self, context: bstack1lllllll1l1_opy_, bstack1l1l111ll11_opy_= True):
        if bstack1l1l111ll11_opy_:
            bstack1l1l11ll1ll_opy_ = self.bstack1ll11111lll_opy_(context, reverse=True)
        else:
            bstack1l1l11ll1ll_opy_ = self.bstack1ll1111111l_opy_(context, reverse=True)
        return [f for f in bstack1l1l11ll1ll_opy_ if f[1].state != bstack1111111l11_opy_.QUIT]
    def bstack1ll11ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l111l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1l1ll111ll1_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኳ") + str(kwargs) + bstack11ll11_opy_ (u"ࠢࠣኴ"))
            return
        bstack1l1l11ll1ll_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1llll111111_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኵ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥ኶"))
            return
        if len(bstack1l1l11ll1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧ኷"))
        bstack1l1l11l11ll_opy_, bstack1l1l1lll111_opy_ = bstack1l1l11ll1ll_opy_[0]
        page = bstack1l1l11l11ll_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኸ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨኹ"))
            return
        bstack1111llll_opy_ = getattr(args[0], bstack11ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨኺ"), None)
        try:
            page.evaluate(bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣኻ"),
                        bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬኼ") + json.dumps(
                            bstack1111llll_opy_) + bstack11ll11_opy_ (u"ࠤࢀࢁࠧኽ"))
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣኾ"), e)
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l111l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1l1ll111ll1_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ኿") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨዀ"))
            return
        bstack1l1l11ll1ll_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1llll111111_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ዁") + str(kwargs) + bstack11ll11_opy_ (u"ࠢࠣዂ"))
            return
        if len(bstack1l1l11ll1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11ll111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥዃ"))
        bstack1l1l11l11ll_opy_, bstack1l1l1lll111_opy_ = bstack1l1l11ll1ll_opy_[0]
        page = bstack1l1l11l11ll_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዄ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦዅ"))
            return
        status = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_, None)
        if not status:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ዆") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠧࠨ዇"))
            return
        bstack1l1l111llll_opy_ = {bstack11ll11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨወ"): status.lower()}
        bstack1l1l11ll111_opy_ = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1l11l1lll_opy_, None)
        if status.lower() == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዉ") and bstack1l1l11ll111_opy_ is not None:
            bstack1l1l111llll_opy_[bstack11ll11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨዊ")] = bstack1l1l11ll111_opy_[0][bstack11ll11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬዋ")][0] if isinstance(bstack1l1l11ll111_opy_, list) else str(bstack1l1l11ll111_opy_)
        try:
              page.evaluate(
                    bstack11ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦዌ"),
                    bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩው")
                    + json.dumps(bstack1l1l111llll_opy_)
                    + bstack11ll11_opy_ (u"ࠧࢃࠢዎ")
                )
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨዏ"), e)
    def bstack1l1ll11llll_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l111l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not bstack1l1ll111ll1_opy_:
            self.logger.debug(
                bstack1lll11ll111_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣዐ"))
            return
        bstack1l1l11ll1ll_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1llll111111_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዑ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥዒ"))
            return
        if len(bstack1l1l11ll1ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧዓ"))
        bstack1l1l11l11ll_opy_, bstack1l1l1lll111_opy_ = bstack1l1l11ll1ll_opy_[0]
        page = bstack1l1l11l11ll_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዔ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨዕ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11ll11_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦዖ") + str(timestamp)
        try:
            page.evaluate(
                bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ዗"),
                bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ዘ").format(
                    json.dumps(
                        {
                            bstack11ll11_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤዙ"): bstack11ll11_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧዚ"),
                            bstack11ll11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢዛ"): {
                                bstack11ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥዜ"): bstack11ll11_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥዝ"),
                                bstack11ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧዞ"): data,
                                bstack11ll11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢዟ"): bstack11ll11_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣዠ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧዡ"), e)
    def bstack1l1ll11l11l_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l111l_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if f.bstack1lllll1l1ll_opy_(instance, bstack1llll111111_opy_.bstack1l1llllll11_opy_, False):
            return
        self.bstack1ll1l1l1111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11111l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11ll11_opy_)
        for bstack1l1l11l1l11_opy_ in bstack1lll1lll1l1_opy_.bstack1lllllll111_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥዢ")
                if bstack1l1ll111ll1_opy_
                else bstack11ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦዣ")
            )
            session.ref = bstack1l1l11l1l11_opy_.ref()
            session.hub_url = bstack1lll1lll1l1_opy_.bstack1lllll1l1ll_opy_(bstack1l1l11l1l11_opy_, bstack1lll1lll1l1_opy_.bstack1l1l1l11l1l_opy_, bstack11ll11_opy_ (u"ࠨࠢዤ"))
            session.framework_name = bstack1l1l11l1l11_opy_.framework_name
            session.framework_version = bstack1l1l11l1l11_opy_.framework_version
            session.framework_session_id = bstack1lll1lll1l1_opy_.bstack1lllll1l1ll_opy_(bstack1l1l11l1l11_opy_, bstack1lll1lll1l1_opy_.bstack1l1l1l11l11_opy_, bstack11ll11_opy_ (u"ࠢࠣዥ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11ll1ll_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1llll111111_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዦ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥዧ"))
            return
        if len(bstack1l1l11ll1ll_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦየ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧዩ"))
        bstack1l1l11l11ll_opy_, bstack1l1l1lll111_opy_ = bstack1l1l11ll1ll_opy_[0]
        page = bstack1l1l11l11ll_opy_()
        if not page:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዪ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢያ"))
            return
        return page
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111ll1l_opy_ = {}
        for bstack1l1l11l1l11_opy_ in bstack1lll1lll1l1_opy_.bstack1lllllll111_opy_.values():
            caps = bstack1lll1lll1l1_opy_.bstack1lllll1l1ll_opy_(bstack1l1l11l1l11_opy_, bstack1lll1lll1l1_opy_.bstack1l1l1l11111_opy_, bstack11ll11_opy_ (u"ࠢࠣዬ"))
        bstack1l1l111ll1l_opy_[bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨይ")] = caps.get(bstack11ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥዮ"), bstack11ll11_opy_ (u"ࠥࠦዯ"))
        bstack1l1l111ll1l_opy_[bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥደ")] = caps.get(bstack11ll11_opy_ (u"ࠧࡵࡳࠣዱ"), bstack11ll11_opy_ (u"ࠨࠢዲ"))
        bstack1l1l111ll1l_opy_[bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤዳ")] = caps.get(bstack11ll11_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧዴ"), bstack11ll11_opy_ (u"ࠤࠥድ"))
        bstack1l1l111ll1l_opy_[bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦዶ")] = caps.get(bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨዷ"), bstack11ll11_opy_ (u"ࠧࠨዸ"))
        return bstack1l1l111ll1l_opy_
    def bstack1ll1l11llll_opy_(self, page: object, bstack1ll1l11l11l_opy_, args={}):
        try:
            bstack1l1l11l1ll1_opy_ = bstack11ll11_opy_ (u"ࠨࠢࠣࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࠴࠮࠯ࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡼࡨࡱࡣࡧࡵࡤࡺࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭࠭ࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾࠫࠥࠦࠧዹ")
            bstack1ll1l11l11l_opy_ = bstack1ll1l11l11l_opy_.replace(bstack11ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥዺ"), bstack11ll11_opy_ (u"ࠣࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠣዻ"))
            script = bstack1l1l11l1ll1_opy_.format(fn_body=bstack1ll1l11l11l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺ࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡈࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠣዼ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦዽ"))