# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1llllll111l_opy_,
    bstack1llllllll11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll11l1ll_opy_, bstack111ll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lllll1111l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l1l_opy_ import bstack1ll111l1111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack111ll1ll_opy_ import bstack1lll1ll11_opy_, bstack1lll11l1ll_opy_, bstack1l1ll1ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1lllll1_opy_(bstack1ll111l1111_opy_):
    bstack1l1l1l11l1l_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤኛ")
    bstack1ll1111lll1_opy_ = bstack111lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥኜ")
    bstack1l1l11lll11_opy_ = bstack111lll_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢኝ")
    bstack1l1l11lll1l_opy_ = bstack111lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨኞ")
    bstack1l1l1l11111_opy_ = bstack111lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦኟ")
    bstack1ll111111ll_opy_ = bstack111lll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢአ")
    bstack1l1l1l111ll_opy_ = bstack111lll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧኡ")
    bstack1l1l1l111l1_opy_ = bstack111lll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣኢ")
    def __init__(self):
        super().__init__(bstack1ll111l1l11_opy_=self.bstack1l1l1l11l1l_opy_, frameworks=[bstack1llll111lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.BEFORE_EACH, bstack1lllll1111l_opy_.POST), self.bstack1l1l11ll1l1_opy_)
        if bstack111ll111_opy_():
            TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll1ll11111_opy_)
        else:
            TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE), self.bstack1ll1ll11111_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11lllll_opy_ = self.bstack1l1l1l11l11_opy_(instance.context)
        if not bstack1l1l11lllll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤኣ") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠧࠨኤ"))
            return
        f.bstack11111ll111_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll1111lll1_opy_, bstack1l1l11lllll_opy_)
    def bstack1l1l1l11l11_opy_(self, context: bstack1llllllll11_opy_, bstack1l1l1l1l11l_opy_= True):
        if bstack1l1l1l1l11l_opy_:
            bstack1l1l11lllll_opy_ = self.bstack1ll111l11l1_opy_(context, reverse=True)
        else:
            bstack1l1l11lllll_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        return [f for f in bstack1l1l11lllll_opy_ if f[1].state != bstack1111111111_opy_.QUIT]
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1l1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤእ") + str(kwargs) + bstack111lll_opy_ (u"ࠢࠣኦ"))
            return
        bstack1l1l11lllll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1l11lllll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኧ") + str(kwargs) + bstack111lll_opy_ (u"ࠤࠥከ"))
            return
        if len(bstack1l1l11lllll_opy_) > 1:
            self.logger.debug(
                bstack1lllll111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧኩ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1lllll1_opy_ = bstack1l1l11lllll_opy_[0]
        page = bstack1l1l1l11lll_opy_()
        if not page:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኪ") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨካ"))
            return
        bstack11l11l11l_opy_ = getattr(args[0], bstack111lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨኬ"), None)
        try:
            page.evaluate(bstack111lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣክ"),
                        bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬኮ") + json.dumps(
                            bstack11l11l11l_opy_) + bstack111lll_opy_ (u"ࠤࢀࢁࠧኯ"))
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣኰ"), e)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1l1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ኱") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨኲ"))
            return
        bstack1l1l11lllll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1l11lllll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኳ") + str(kwargs) + bstack111lll_opy_ (u"ࠢࠣኴ"))
            return
        if len(bstack1l1l11lllll_opy_) > 1:
            self.logger.debug(
                bstack1lllll111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥኵ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1lllll1_opy_ = bstack1l1l11lllll_opy_[0]
        page = bstack1l1l1l11lll_opy_()
        if not page:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ኶") + str(kwargs) + bstack111lll_opy_ (u"ࠥࠦ኷"))
            return
        status = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l1l1l1l1_opy_, None)
        if not status:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢኸ") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠧࠨኹ"))
            return
        bstack1l1l1l1111l_opy_ = {bstack111lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨኺ"): status.lower()}
        bstack1l1l11ll11l_opy_ = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_, None)
        if status.lower() == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኻ") and bstack1l1l11ll11l_opy_ is not None:
            bstack1l1l1l1111l_opy_[bstack111lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨኼ")] = bstack1l1l11ll11l_opy_[0][bstack111lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬኽ")][0] if isinstance(bstack1l1l11ll11l_opy_, list) else str(bstack1l1l11ll11l_opy_)
        try:
              page.evaluate(
                    bstack111lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦኾ"),
                    bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩ኿")
                    + json.dumps(bstack1l1l1l1111l_opy_)
                    + bstack111lll_opy_ (u"ࠧࢃࠢዀ")
                )
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ዁"), e)
    def bstack1l1lll1lll1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1l1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if not bstack1l1ll11l1ll_opy_:
            self.logger.debug(
                bstack1lllll111l1_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣዂ"))
            return
        bstack1l1l11lllll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1l11lllll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዃ") + str(kwargs) + bstack111lll_opy_ (u"ࠤࠥዄ"))
            return
        if len(bstack1l1l11lllll_opy_) > 1:
            self.logger.debug(
                bstack1lllll111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧዅ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1lllll1_opy_ = bstack1l1l11lllll_opy_[0]
        page = bstack1l1l1l11lll_opy_()
        if not page:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ዆") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨ዇"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111lll_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦወ") + str(timestamp)
        try:
            page.evaluate(
                bstack111lll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣዉ"),
                bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ዊ").format(
                    json.dumps(
                        {
                            bstack111lll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤዋ"): bstack111lll_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧዌ"),
                            bstack111lll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢው"): {
                                bstack111lll_opy_ (u"ࠧࡺࡹࡱࡧࠥዎ"): bstack111lll_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥዏ"),
                                bstack111lll_opy_ (u"ࠢࡥࡣࡷࡥࠧዐ"): data,
                                bstack111lll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢዑ"): bstack111lll_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣዒ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧዓ"), e)
    def bstack1l1llll1lll_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11ll1l1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if f.bstack1llllll1l1l_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll111111ll_opy_, False):
            return
        self.bstack1ll11ll1l11_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l11ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11ll11ll_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_)
        req.test_framework_state = bstack11111l1l11_opy_[0].name
        req.test_hook_state = bstack11111l1l11_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        for bstack1l1l1l1l111_opy_ in bstack1llll11lll1_opy_.bstack1lllll1ll11_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥዔ")
                if bstack1l1ll11l1ll_opy_
                else bstack111lll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦዕ")
            )
            session.ref = bstack1l1l1l1l111_opy_.ref()
            session.hub_url = bstack1llll11lll1_opy_.bstack1llllll1l1l_opy_(bstack1l1l1l1l111_opy_, bstack1llll11lll1_opy_.bstack1l1l1lll1l1_opy_, bstack111lll_opy_ (u"ࠨࠢዖ"))
            session.framework_name = bstack1l1l1l1l111_opy_.framework_name
            session.framework_version = bstack1l1l1l1l111_opy_.framework_version
            session.framework_session_id = bstack1llll11lll1_opy_.bstack1llllll1l1l_opy_(bstack1l1l1l1l111_opy_, bstack1llll11lll1_opy_.bstack1l1l1llll11_opy_, bstack111lll_opy_ (u"ࠢࠣ዗"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11lllll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1lllll1_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1l11lllll_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዘ") + str(kwargs) + bstack111lll_opy_ (u"ࠤࠥዙ"))
            return
        if len(bstack1l1l11lllll_opy_) > 1:
            self.logger.debug(bstack111lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዚ") + str(kwargs) + bstack111lll_opy_ (u"ࠦࠧዛ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1lllll1_opy_ = bstack1l1l11lllll_opy_[0]
        page = bstack1l1l1l11lll_opy_()
        if not page:
            self.logger.debug(bstack111lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዜ") + str(kwargs) + bstack111lll_opy_ (u"ࠨࠢዝ"))
            return
        return page
    def bstack1ll11llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l11llll1_opy_ = {}
        for bstack1l1l1l1l111_opy_ in bstack1llll11lll1_opy_.bstack1lllll1ll11_opy_.values():
            caps = bstack1llll11lll1_opy_.bstack1llllll1l1l_opy_(bstack1l1l1l1l111_opy_, bstack1llll11lll1_opy_.bstack1l1l1l1l1ll_opy_, bstack111lll_opy_ (u"ࠢࠣዞ"))
        bstack1l1l11llll1_opy_[bstack111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨዟ")] = caps.get(bstack111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥዠ"), bstack111lll_opy_ (u"ࠥࠦዡ"))
        bstack1l1l11llll1_opy_[bstack111lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥዢ")] = caps.get(bstack111lll_opy_ (u"ࠧࡵࡳࠣዣ"), bstack111lll_opy_ (u"ࠨࠢዤ"))
        bstack1l1l11llll1_opy_[bstack111lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤዥ")] = caps.get(bstack111lll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧዦ"), bstack111lll_opy_ (u"ࠤࠥዧ"))
        bstack1l1l11llll1_opy_[bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦየ")] = caps.get(bstack111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨዩ"), bstack111lll_opy_ (u"ࠧࠨዪ"))
        return bstack1l1l11llll1_opy_
    def bstack1ll11ll11l1_opy_(self, page: object, bstack1ll11ll1111_opy_, args={}):
        try:
            bstack1l1l1l11ll1_opy_ = bstack111lll_opy_ (u"ࠨࠢࠣࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࠴࠮࠯ࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡼࡨࡱࡣࡧࡵࡤࡺࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭࠭ࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾࠫࠥࠦࠧያ")
            bstack1ll11ll1111_opy_ = bstack1ll11ll1111_opy_.replace(bstack111lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥዬ"), bstack111lll_opy_ (u"ࠣࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠣይ"))
            script = bstack1l1l1l11ll1_opy_.format(fn_body=bstack1ll11ll1111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠤࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺ࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡈࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠣዮ") + str(e) + bstack111lll_opy_ (u"ࠥࠦዯ"))