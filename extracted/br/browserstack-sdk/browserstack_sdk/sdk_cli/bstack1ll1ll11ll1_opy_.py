# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllll1l1l1_opy_ import (
    bstack1llllllll1l_opy_,
    bstack1lllll1l11l_opy_,
    bstack111111l111_opy_,
    bstack1llllllll11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll1111l_opy_, bstack111l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1lll11ll111_opy_, bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll1l_opy_ import bstack1ll1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1llll1lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1l1l11_opy_ import bstack11ll111l11_opy_, bstack1lllll1l11_opy_, bstack1lll11l111_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1lll1l1l_opy_(bstack1l1llll1lll_opy_):
    bstack1l1l111l111_opy_ = bstack1ll1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢጉ")
    bstack1l1ll111l11_opy_ = bstack1ll1ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጊ")
    bstack1l1l1111ll1_opy_ = bstack1ll1ll_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጋ")
    bstack1l1l111ll11_opy_ = bstack1ll1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጌ")
    bstack1l11lllllll_opy_ = bstack1ll1ll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤግ")
    bstack1l1l1ll1l1l_opy_ = bstack1ll1ll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጎ")
    bstack1l1l111l11l_opy_ = bstack1ll1ll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥጏ")
    bstack1l1l11111l1_opy_ = bstack1ll1ll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨጐ")
    def __init__(self):
        super().__init__(bstack1l1llllll1l_opy_=self.bstack1l1l111l111_opy_, frameworks=[bstack1llll11l111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11l1l111_opy_((bstack1llll1111ll_opy_.BEFORE_EACH, bstack1lll11ll111_opy_.POST), self.bstack1l1l1111lll_opy_)
        if bstack111l11l11_opy_():
            TestFramework.bstack1ll11l1l111_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll11ll111_opy_.POST), self.bstack1ll11l11lll_opy_)
        else:
            TestFramework.bstack1ll11l1l111_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll11ll111_opy_.PRE), self.bstack1ll11l11lll_opy_)
        TestFramework.bstack1ll11l1l111_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll11ll111_opy_.POST), self.bstack1ll111l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l111lll1_opy_ = self.bstack1l1l1111l1l_opy_(instance.context)
        if not bstack1l1l111lll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ጑") + str(bstack1llllll1111_opy_) + bstack1ll1ll_opy_ (u"ࠥࠦጒ"))
            return
        f.bstack1lllll1ll1l_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll111l11_opy_, bstack1l1l111lll1_opy_)
    def bstack1l1l1111l1l_opy_(self, context: bstack1llllllll11_opy_, bstack1l1l1111111_opy_= True):
        if bstack1l1l1111111_opy_:
            bstack1l1l111lll1_opy_ = self.bstack1l1llllll11_opy_(context, reverse=True)
        else:
            bstack1l1l111lll1_opy_ = self.bstack1ll111111ll_opy_(context, reverse=True)
        return [f for f in bstack1l1l111lll1_opy_ if f[1].state != bstack1llllllll1l_opy_.QUIT]
    def bstack1ll11l11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll1111l_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጓ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠧࠨጔ"))
            return
        bstack1l1l111lll1_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll111l11_opy_, [])
        if not bstack1l1l111lll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጕ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠢࠣ጖"))
            return
        if len(bstack1l1l111lll1_opy_) > 1:
            self.logger.debug(
                bstack1lll1111l1l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥ጗"))
        bstack1l1l111111l_opy_, bstack1l1l1l1lll1_opy_ = bstack1l1l111lll1_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጘ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠥࠦጙ"))
            return
        bstack11lll11111_opy_ = getattr(args[0], bstack1ll1ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦጚ"), None)
        try:
            page.evaluate(bstack1ll1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጛ"),
                        bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪጜ") + json.dumps(
                            bstack11lll11111_opy_) + bstack1ll1ll_opy_ (u"ࠢࡾࡿࠥጝ"))
        except Exception as e:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨጞ"), e)
    def bstack1ll111l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll1111l_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጟ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠥࠦጠ"))
            return
        bstack1l1l111lll1_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll111l11_opy_, [])
        if not bstack1l1l111lll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጡ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠧࠨጢ"))
            return
        if len(bstack1l1l111lll1_opy_) > 1:
            self.logger.debug(
                bstack1lll1111l1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጣ"))
        bstack1l1l111111l_opy_, bstack1l1l1l1lll1_opy_ = bstack1l1l111lll1_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጤ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠣࠤጥ"))
            return
        status = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l11111ll_opy_, None)
        if not status:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጦ") + str(bstack1llllll1111_opy_) + bstack1ll1ll_opy_ (u"ࠥࠦጧ"))
            return
        bstack1l1l1111l11_opy_ = {bstack1ll1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦጨ"): status.lower()}
        bstack1l11llllll1_opy_ = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_, None)
        if status.lower() == bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬጩ") and bstack1l11llllll1_opy_ is not None:
            bstack1l1l1111l11_opy_[bstack1ll1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ጪ")] = bstack1l11llllll1_opy_[0][bstack1ll1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪጫ")][0] if isinstance(bstack1l11llllll1_opy_, list) else str(bstack1l11llllll1_opy_)
        try:
              page.evaluate(
                    bstack1ll1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤጬ"),
                    bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧጭ")
                    + json.dumps(bstack1l1l1111l11_opy_)
                    + bstack1ll1ll_opy_ (u"ࠥࢁࠧጮ")
                )
        except Exception as e:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦጯ"), e)
    def bstack1l1lll11lll_opy_(
        self,
        instance: bstack1ll1lll1l11_opy_,
        f: TestFramework,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if not bstack1l1lll1111l_opy_:
            self.logger.debug(
                bstack1lll1111l1l_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጰ"))
            return
        bstack1l1l111lll1_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll111l11_opy_, [])
        if not bstack1l1l111lll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጱ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠢࠣጲ"))
            return
        if len(bstack1l1l111lll1_opy_) > 1:
            self.logger.debug(
                bstack1lll1111l1l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥጳ"))
        bstack1l1l111111l_opy_, bstack1l1l1l1lll1_opy_ = bstack1l1l111lll1_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጴ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠥࠦጵ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll1ll_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤጶ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጷ"),
                bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫጸ").format(
                    json.dumps(
                        {
                            bstack1ll1ll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጹ"): bstack1ll1ll_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥጺ"),
                            bstack1ll1ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጻ"): {
                                bstack1ll1ll_opy_ (u"ࠥࡸࡾࡶࡥࠣጼ"): bstack1ll1ll_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣጽ"),
                                bstack1ll1ll_opy_ (u"ࠧࡪࡡࡵࡣࠥጾ"): data,
                                bstack1ll1ll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጿ"): bstack1ll1ll_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨፀ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥፁ"), e)
    def bstack1l1ll1l11l1_opy_(
        self,
        instance: bstack1ll1lll1l11_opy_,
        f: TestFramework,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1llllll1111_opy_, *args, **kwargs)
        if f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1l1ll1l1l_opy_, False):
            return
        self.bstack1ll111llll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll11ll1l11_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll11lllll1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_)
        req.test_framework_state = bstack1llllll1111_opy_[0].name
        req.test_hook_state = bstack1llllll1111_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1111ll_opy_)
        for bstack1l1l111llll_opy_ in bstack1ll1ll1ll1l_opy_.bstack1111111l11_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣፂ")
                if bstack1l1lll1111l_opy_
                else bstack1ll1ll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤፃ")
            )
            session.ref = bstack1l1l111llll_opy_.ref()
            session.hub_url = bstack1ll1ll1ll1l_opy_.bstack1llllll1lll_opy_(bstack1l1l111llll_opy_, bstack1ll1ll1ll1l_opy_.bstack1l1l1l111l1_opy_, bstack1ll1ll_opy_ (u"ࠦࠧፄ"))
            session.framework_name = bstack1l1l111llll_opy_.framework_name
            session.framework_version = bstack1l1l111llll_opy_.framework_version
            session.framework_session_id = bstack1ll1ll1ll1l_opy_.bstack1llllll1lll_opy_(bstack1l1l111llll_opy_, bstack1ll1ll1ll1l_opy_.bstack1l1l11ll1ll_opy_, bstack1ll1ll_opy_ (u"ࠧࠨፅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l111lll1_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll111l11_opy_, [])
        if not bstack1l1l111lll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፆ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠢࠣፇ"))
            return
        if len(bstack1l1l111lll1_opy_) > 1:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፈ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠤࠥፉ"))
        bstack1l1l111111l_opy_, bstack1l1l1l1lll1_opy_ = bstack1l1l111lll1_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፊ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠦࠧፋ"))
            return
        return page
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111l1ll_opy_ = {}
        for bstack1l1l111llll_opy_ in bstack1ll1ll1ll1l_opy_.bstack1111111l11_opy_.values():
            caps = bstack1ll1ll1ll1l_opy_.bstack1llllll1lll_opy_(bstack1l1l111llll_opy_, bstack1ll1ll1ll1l_opy_.bstack1l1l11lllll_opy_, bstack1ll1ll_opy_ (u"ࠧࠨፌ"))
        bstack1l1l111l1ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦፍ")] = caps.get(bstack1ll1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣፎ"), bstack1ll1ll_opy_ (u"ࠣࠤፏ"))
        bstack1l1l111l1ll_opy_[bstack1ll1ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣፐ")] = caps.get(bstack1ll1ll_opy_ (u"ࠥࡳࡸࠨፑ"), bstack1ll1ll_opy_ (u"ࠦࠧፒ"))
        bstack1l1l111l1ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢፓ")] = caps.get(bstack1ll1ll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥፔ"), bstack1ll1ll_opy_ (u"ࠢࠣፕ"))
        bstack1l1l111l1ll_opy_[bstack1ll1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤፖ")] = caps.get(bstack1ll1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦፗ"), bstack1ll1ll_opy_ (u"ࠥࠦፘ"))
        return bstack1l1l111l1ll_opy_
    def bstack1ll1l11l1l1_opy_(self, page: object, bstack1ll11llllll_opy_, args={}):
        try:
            bstack1l1l111l1l1_opy_ = bstack1ll1ll_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥፙ")
            bstack1ll11llllll_opy_ = bstack1ll11llllll_opy_.replace(bstack1ll1ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣፚ"), bstack1ll1ll_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨ፛"))
            script = bstack1l1l111l1l1_opy_.format(fn_body=bstack1ll11llllll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll1ll_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨ፜") + str(e) + bstack1ll1ll_opy_ (u"ࠣࠤ፝"))