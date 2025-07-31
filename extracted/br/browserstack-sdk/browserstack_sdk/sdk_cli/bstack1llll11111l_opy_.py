# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1llll1l1lll_opy_,
    bstack1lllllllll1_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1lllll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1lll111_opy_, bstack1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_, bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1l1l_opy_ import bstack1l1llll11ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1lll1ll1ll_opy_ import bstack1llll11ll1_opy_, bstack1l1l11l1ll_opy_, bstack1l11111l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1l11l1l_opy_(bstack1l1llll11ll_opy_):
    bstack1l1l1111lll_opy_ = bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢጉ")
    bstack1l1lll11111_opy_ = bstack1l11l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጊ")
    bstack1l1l111l11l_opy_ = bstack1l11l11_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጋ")
    bstack1l1l1111ll1_opy_ = bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጌ")
    bstack1l1l111l1l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤግ")
    bstack1l1lll1llll_opy_ = bstack1l11l11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጎ")
    bstack1l11lllll1l_opy_ = bstack1l11l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥጏ")
    bstack1l1l1111l11_opy_ = bstack1l11l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨጐ")
    def __init__(self):
        super().__init__(bstack1l1llll1ll1_opy_=self.bstack1l1l1111lll_opy_, frameworks=[bstack1ll1llll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1lll1llll11_opy_.POST), self.bstack1l11lllllll_opy_)
        if bstack1l1l11ll1_opy_():
            TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.POST), self.bstack1ll111l1l11_opy_)
        else:
            TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.PRE), self.bstack1ll111l1l11_opy_)
        TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.POST), self.bstack1ll1111llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1111111_opy_ = self.bstack1l11llllll1_opy_(instance.context)
        if not bstack1l1l1111111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ጑") + str(bstack1llllll11l1_opy_) + bstack1l11l11_opy_ (u"ࠥࠦጒ"))
            return
        f.bstack1lllll1l11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll11111_opy_, bstack1l1l1111111_opy_)
    def bstack1l11llllll1_opy_(self, context: bstack1llll1lllll_opy_, bstack1l1l11111l1_opy_= True):
        if bstack1l1l11111l1_opy_:
            bstack1l1l1111111_opy_ = self.bstack1l1lllll111_opy_(context, reverse=True)
        else:
            bstack1l1l1111111_opy_ = self.bstack1l1llllll1l_opy_(context, reverse=True)
        return [f for f in bstack1l1l1111111_opy_ if f[1].state != bstack1llll1l1lll_opy_.QUIT]
    def bstack1ll111l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1llllll11l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጓ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠧࠨጔ"))
            return
        bstack1l1l1111111_opy_ = f.bstack1lllllll11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll11111_opy_, [])
        if not bstack1l1l1111111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጕ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠢࠣ጖"))
            return
        if len(bstack1l1l1111111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥ጗"))
        bstack1l11lllll11_opy_, bstack1l1l1l1l11l_opy_ = bstack1l1l1111111_opy_[0]
        page = bstack1l11lllll11_opy_()
        if not page:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጘ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠥࠦጙ"))
            return
        bstack1l1lll11l_opy_ = getattr(args[0], bstack1l11l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦጚ"), None)
        try:
            page.evaluate(bstack1l11l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጛ"),
                        bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪጜ") + json.dumps(
                            bstack1l1lll11l_opy_) + bstack1l11l11_opy_ (u"ࠢࡾࡿࠥጝ"))
        except Exception as e:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨጞ"), e)
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1llllll11l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጟ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠥࠦጠ"))
            return
        bstack1l1l1111111_opy_ = f.bstack1lllllll11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll11111_opy_, [])
        if not bstack1l1l1111111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጡ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠧࠨጢ"))
            return
        if len(bstack1l1l1111111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll111l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጣ"))
        bstack1l11lllll11_opy_, bstack1l1l1l1l11l_opy_ = bstack1l1l1111111_opy_[0]
        page = bstack1l11lllll11_opy_()
        if not page:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጤ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠣࠤጥ"))
            return
        status = f.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l11llll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጦ") + str(bstack1llllll11l1_opy_) + bstack1l11l11_opy_ (u"ࠥࠦጧ"))
            return
        bstack1l1l1111l1l_opy_ = {bstack1l11l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦጨ"): status.lower()}
        bstack1l11llll1ll_opy_ = f.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l1l11111ll_opy_, None)
        if status.lower() == bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬጩ") and bstack1l11llll1ll_opy_ is not None:
            bstack1l1l1111l1l_opy_[bstack1l11l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ጪ")] = bstack1l11llll1ll_opy_[0][bstack1l11l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪጫ")][0] if isinstance(bstack1l11llll1ll_opy_, list) else str(bstack1l11llll1ll_opy_)
        try:
              page.evaluate(
                    bstack1l11l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤጬ"),
                    bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧጭ")
                    + json.dumps(bstack1l1l1111l1l_opy_)
                    + bstack1l11l11_opy_ (u"ࠥࢁࠧጮ")
                )
        except Exception as e:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦጯ"), e)
    def bstack1l1lll1l1l1_opy_(
        self,
        instance: bstack1lll11l1l11_opy_,
        f: TestFramework,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1llllll11l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(
                bstack1ll1ll111l1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጰ"))
            return
        bstack1l1l1111111_opy_ = f.bstack1lllllll11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll11111_opy_, [])
        if not bstack1l1l1111111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጱ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠢࠣጲ"))
            return
        if len(bstack1l1l1111111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll111l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥጳ"))
        bstack1l11lllll11_opy_, bstack1l1l1l1l11l_opy_ = bstack1l1l1111111_opy_[0]
        page = bstack1l11lllll11_opy_()
        if not page:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጴ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠥࠦጵ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l11l11_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤጶ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l11l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጷ"),
                bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫጸ").format(
                    json.dumps(
                        {
                            bstack1l11l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጹ"): bstack1l11l11_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥጺ"),
                            bstack1l11l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጻ"): {
                                bstack1l11l11_opy_ (u"ࠥࡸࡾࡶࡥࠣጼ"): bstack1l11l11_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣጽ"),
                                bstack1l11l11_opy_ (u"ࠧࡪࡡࡵࡣࠥጾ"): data,
                                bstack1l11l11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጿ"): bstack1l11l11_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨፀ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥፁ"), e)
    def bstack1l1l1llllll_opy_(
        self,
        instance: bstack1lll11l1l11_opy_,
        f: TestFramework,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1llllll11l1_opy_, *args, **kwargs)
        if f.bstack1lllllll11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll1llll_opy_, False):
            return
        self.bstack1ll1l111l1l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll11l1l11l_opy_)
        req.test_framework_name = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_)
        req.test_framework_version = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l1ll1ll1ll_opy_)
        req.test_framework_state = bstack1llllll11l1_opy_[0].name
        req.test_hook_state = bstack1llllll11l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
        for bstack1l1l111111l_opy_ in bstack1llll1l11l1_opy_.bstack1llll1ll1ll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣፂ")
                if bstack1l1l1lll111_opy_
                else bstack1l11l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤፃ")
            )
            session.ref = bstack1l1l111111l_opy_.ref()
            session.hub_url = bstack1llll1l11l1_opy_.bstack1lllllll11l_opy_(bstack1l1l111111l_opy_, bstack1llll1l11l1_opy_.bstack1l1l11lll11_opy_, bstack1l11l11_opy_ (u"ࠦࠧፄ"))
            session.framework_name = bstack1l1l111111l_opy_.framework_name
            session.framework_version = bstack1l1l111111l_opy_.framework_version
            session.framework_session_id = bstack1llll1l11l1_opy_.bstack1lllllll11l_opy_(bstack1l1l111111l_opy_, bstack1llll1l11l1_opy_.bstack1l1l11l11ll_opy_, bstack1l11l11_opy_ (u"ࠧࠨፅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1111111_opy_ = f.bstack1lllllll11l_opy_(instance, bstack1lll1l11l1l_opy_.bstack1l1lll11111_opy_, [])
        if not bstack1l1l1111111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፆ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠢࠣፇ"))
            return
        if len(bstack1l1l1111111_opy_) > 1:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፈ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠤࠥፉ"))
        bstack1l11lllll11_opy_, bstack1l1l1l1l11l_opy_ = bstack1l1l1111111_opy_[0]
        page = bstack1l11lllll11_opy_()
        if not page:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፊ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠦࠧፋ"))
            return
        return page
    def bstack1ll111l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111l111_opy_ = {}
        for bstack1l1l111111l_opy_ in bstack1llll1l11l1_opy_.bstack1llll1ll1ll_opy_.values():
            caps = bstack1llll1l11l1_opy_.bstack1lllllll11l_opy_(bstack1l1l111111l_opy_, bstack1llll1l11l1_opy_.bstack1l1l11l1ll1_opy_, bstack1l11l11_opy_ (u"ࠧࠨፌ"))
        bstack1l1l111l111_opy_[bstack1l11l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦፍ")] = caps.get(bstack1l11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣፎ"), bstack1l11l11_opy_ (u"ࠣࠤፏ"))
        bstack1l1l111l111_opy_[bstack1l11l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣፐ")] = caps.get(bstack1l11l11_opy_ (u"ࠥࡳࡸࠨፑ"), bstack1l11l11_opy_ (u"ࠦࠧፒ"))
        bstack1l1l111l111_opy_[bstack1l11l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢፓ")] = caps.get(bstack1l11l11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥፔ"), bstack1l11l11_opy_ (u"ࠢࠣፕ"))
        bstack1l1l111l111_opy_[bstack1l11l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤፖ")] = caps.get(bstack1l11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦፗ"), bstack1l11l11_opy_ (u"ࠥࠦፘ"))
        return bstack1l1l111l111_opy_
    def bstack1ll1l11ll11_opy_(self, page: object, bstack1ll1l111111_opy_, args={}):
        try:
            bstack1l11llll11l_opy_ = bstack1l11l11_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥፙ")
            bstack1ll1l111111_opy_ = bstack1ll1l111111_opy_.replace(bstack1l11l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣፚ"), bstack1l11l11_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨ፛"))
            script = bstack1l11llll11l_opy_.format(fn_body=bstack1ll1l111111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨ፜") + str(e) + bstack1l11l11_opy_ (u"ࠣࠤ፝"))