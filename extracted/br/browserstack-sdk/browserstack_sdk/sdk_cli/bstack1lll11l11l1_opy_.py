# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llllllll11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll111l1l_opy_, bstack1l1l11l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1llllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll11l_opy_ import bstack1ll111111ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1lll111l1_opy_ import bstack11l1lll11l_opy_, bstack11ll1l111_opy_, bstack11ll11ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll111lll_opy_(bstack1ll111111ll_opy_):
    bstack1l1l111l1ll_opy_ = bstack11l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣጊ")
    bstack1l1ll11l111_opy_ = bstack11l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤጋ")
    bstack1l1l1111l1l_opy_ = bstack11l1_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጌ")
    bstack1l11lllllll_opy_ = bstack11l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧግ")
    bstack1l11llllll1_opy_ = bstack11l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥጎ")
    bstack1l1lll11l11_opy_ = bstack11l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨጏ")
    bstack1l1l111llll_opy_ = bstack11l1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦጐ")
    bstack1l1l111ll1l_opy_ = bstack11l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢ጑")
    def __init__(self):
        super().__init__(bstack1l1lllll1ll_opy_=self.bstack1l1l111l1ll_opy_, frameworks=[bstack1llll1l11l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1lll1ll1l1l_opy_.POST), self.bstack1l1l111l1l1_opy_)
        if bstack1l1l11l111_opy_():
            TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.POST), self.bstack1ll11l11l11_opy_)
        else:
            TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.POST), self.bstack1ll11l1l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11111l1_opy_ = self.bstack1l1l1111lll_opy_(instance.context)
        if not bstack1l1l11111l1_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣጒ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠦࠧጓ"))
            return
        f.bstack1111111lll_opy_(instance, bstack1llll111lll_opy_.bstack1l1ll11l111_opy_, bstack1l1l11111l1_opy_)
    def bstack1l1l1111lll_opy_(self, context: bstack1llllllll11_opy_, bstack1l1l1111l11_opy_= True):
        if bstack1l1l1111l11_opy_:
            bstack1l1l11111l1_opy_ = self.bstack1ll111111l1_opy_(context, reverse=True)
        else:
            bstack1l1l11111l1_opy_ = self.bstack1ll1111111l_opy_(context, reverse=True)
        return [f for f in bstack1l1l11111l1_opy_ if f[1].state != bstack1llllllllll_opy_.QUIT]
    def bstack1ll11l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if not bstack1l1ll111l1l_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጔ") + str(kwargs) + bstack11l1_opy_ (u"ࠨࠢጕ"))
            return
        bstack1l1l11111l1_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1llll111lll_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1l11111l1_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ጖") + str(kwargs) + bstack11l1_opy_ (u"ࠣࠤ጗"))
            return
        if len(bstack1l1l11111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1lll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦጘ"))
        bstack1l1l111l11l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1l11111l1_opy_[0]
        page = bstack1l1l111l11l_opy_()
        if not page:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጙ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧጚ"))
            return
        bstack11ll11ll1_opy_ = getattr(args[0], bstack11l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧጛ"), None)
        try:
            page.evaluate(bstack11l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢጜ"),
                        bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫጝ") + json.dumps(
                            bstack11ll11ll1_opy_) + bstack11l1_opy_ (u"ࠣࡿࢀࠦጞ"))
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢጟ"), e)
    def bstack1ll11l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if not bstack1l1ll111l1l_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጠ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧጡ"))
            return
        bstack1l1l11111l1_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1llll111lll_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1l11111l1_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጢ") + str(kwargs) + bstack11l1_opy_ (u"ࠨࠢጣ"))
            return
        if len(bstack1l1l11111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1lll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤጤ"))
        bstack1l1l111l11l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1l11111l1_opy_[0]
        page = bstack1l1l111l11l_opy_()
        if not page:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጥ") + str(kwargs) + bstack11l1_opy_ (u"ࠤࠥጦ"))
            return
        status = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l111lll1_opy_, None)
        if not status:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጧ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠦࠧጨ"))
            return
        bstack1l1l11111ll_opy_ = {bstack11l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧጩ"): status.lower()}
        bstack1l1l1111ll1_opy_ = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l111111l_opy_, None)
        if status.lower() == bstack11l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጪ") and bstack1l1l1111ll1_opy_ is not None:
            bstack1l1l11111ll_opy_[bstack11l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧጫ")] = bstack1l1l1111ll1_opy_[0][bstack11l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫጬ")][0] if isinstance(bstack1l1l1111ll1_opy_, list) else str(bstack1l1l1111ll1_opy_)
        try:
              page.evaluate(
                    bstack11l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥጭ"),
                    bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨጮ")
                    + json.dumps(bstack1l1l11111ll_opy_)
                    + bstack11l1_opy_ (u"ࠦࢂࠨጯ")
                )
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧጰ"), e)
    def bstack1l1l1lll11l_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if not bstack1l1ll111l1l_opy_:
            self.logger.debug(
                bstack1lll1lll111_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢጱ"))
            return
        bstack1l1l11111l1_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1llll111lll_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1l11111l1_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጲ") + str(kwargs) + bstack11l1_opy_ (u"ࠣࠤጳ"))
            return
        if len(bstack1l1l11111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1lll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦጴ"))
        bstack1l1l111l11l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1l11111l1_opy_[0]
        page = bstack1l1l111l11l_opy_()
        if not page:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጵ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧጶ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l1_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥጷ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢጸ"),
                bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬጹ").format(
                    json.dumps(
                        {
                            bstack11l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣጺ"): bstack11l1_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦጻ"),
                            bstack11l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨጼ"): {
                                bstack11l1_opy_ (u"ࠦࡹࡿࡰࡦࠤጽ"): bstack11l1_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤጾ"),
                                bstack11l1_opy_ (u"ࠨࡤࡢࡶࡤࠦጿ"): data,
                                bstack11l1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨፀ"): bstack11l1_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢፁ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦፂ"), e)
    def bstack1l1ll1l11l1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1l1_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if f.bstack1lllllllll1_opy_(instance, bstack1llll111lll_opy_.bstack1l1lll11l11_opy_, False):
            return
        self.bstack1ll11llllll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll111lll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_)
        req.test_framework_state = bstack1lllllll11l_opy_[0].name
        req.test_hook_state = bstack1lllllll11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        for bstack1l1l1111111_opy_ in bstack1lll1llllll_opy_.bstack1lllll1llll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤፃ")
                if bstack1l1ll111l1l_opy_
                else bstack11l1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥፄ")
            )
            session.ref = bstack1l1l1111111_opy_.ref()
            session.hub_url = bstack1lll1llllll_opy_.bstack1lllllllll1_opy_(bstack1l1l1111111_opy_, bstack1lll1llllll_opy_.bstack1l1l1l11111_opy_, bstack11l1_opy_ (u"ࠧࠨፅ"))
            session.framework_name = bstack1l1l1111111_opy_.framework_name
            session.framework_version = bstack1l1l1111111_opy_.framework_version
            session.framework_session_id = bstack1lll1llllll_opy_.bstack1lllllllll1_opy_(bstack1l1l1111111_opy_, bstack1lll1llllll_opy_.bstack1l1l11l1l11_opy_, bstack11l1_opy_ (u"ࠨࠢፆ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11111l1_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1llll111lll_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1l11111l1_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፇ") + str(kwargs) + bstack11l1_opy_ (u"ࠣࠤፈ"))
            return
        if len(bstack1l1l11111l1_opy_) > 1:
            self.logger.debug(bstack11l1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፉ") + str(kwargs) + bstack11l1_opy_ (u"ࠥࠦፊ"))
        bstack1l1l111l11l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1l11111l1_opy_[0]
        page = bstack1l1l111l11l_opy_()
        if not page:
            self.logger.debug(bstack11l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፋ") + str(kwargs) + bstack11l1_opy_ (u"ࠧࠨፌ"))
            return
        return page
    def bstack1ll11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111ll11_opy_ = {}
        for bstack1l1l1111111_opy_ in bstack1lll1llllll_opy_.bstack1lllll1llll_opy_.values():
            caps = bstack1lll1llllll_opy_.bstack1lllllllll1_opy_(bstack1l1l1111111_opy_, bstack1lll1llllll_opy_.bstack1l1l11l1lll_opy_, bstack11l1_opy_ (u"ࠨࠢፍ"))
        bstack1l1l111ll11_opy_[bstack11l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧፎ")] = caps.get(bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤፏ"), bstack11l1_opy_ (u"ࠤࠥፐ"))
        bstack1l1l111ll11_opy_[bstack11l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤፑ")] = caps.get(bstack11l1_opy_ (u"ࠦࡴࡹࠢፒ"), bstack11l1_opy_ (u"ࠧࠨፓ"))
        bstack1l1l111ll11_opy_[bstack11l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣፔ")] = caps.get(bstack11l1_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦፕ"), bstack11l1_opy_ (u"ࠣࠤፖ"))
        bstack1l1l111ll11_opy_[bstack11l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥፗ")] = caps.get(bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧፘ"), bstack11l1_opy_ (u"ࠦࠧፙ"))
        return bstack1l1l111ll11_opy_
    def bstack1ll111l11ll_opy_(self, page: object, bstack1ll111lllll_opy_, args={}):
        try:
            bstack1l1l111l111_opy_ = bstack11l1_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡻࡧࡰࡢࡦࡴࡪࡹࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦፚ")
            bstack1ll111lllll_opy_ = bstack1ll111lllll_opy_.replace(bstack11l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ፛"), bstack11l1_opy_ (u"ࠢࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠢ፜"))
            script = bstack1l1l111l111_opy_.format(fn_body=bstack1ll111lllll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡇࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸ࠱ࠦࠢ፝") + str(e) + bstack11l1_opy_ (u"ࠤࠥ፞"))