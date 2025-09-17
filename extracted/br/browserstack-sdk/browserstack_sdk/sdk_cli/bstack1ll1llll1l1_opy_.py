# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1lllllll111_opy_,
    bstack1llll1lllll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11ll1_opy_, bstack1l11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_, bstack1lll11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1ll1l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1111_opy_ import bstack1l1lllll111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l1111111_opy_ import bstack1ll1llllll_opy_, bstack1l1l111l1_opy_, bstack1llllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1lll1l1l_opy_(bstack1l1lllll111_opy_):
    bstack1l11lllll11_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥጓ")
    bstack1l1ll11l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጔ")
    bstack1l1l1111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጕ")
    bstack1l11lll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢ጖")
    bstack1l1l11111ll_opy_ = bstack1l11ll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧ጗")
    bstack1l1lll111l1_opy_ = bstack1l11ll1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣጘ")
    bstack1l11llll11l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨጙ")
    bstack1l11llll111_opy_ = bstack1l11ll1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤጚ")
    def __init__(self):
        super().__init__(bstack1l1llll1l1l_opy_=self.bstack1l11lllll11_opy_, frameworks=[bstack1ll1l1l1lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1lll111l1l1_opy_.POST), self.bstack1l1l1111lll_opy_)
        if bstack1l11llll11_opy_():
            TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11l11ll1_opy_)
        else:
            TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.PRE), self.bstack1ll11l11ll1_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l111111l_opy_ = self.bstack1l11llll1ll_opy_(instance.context)
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጛ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢጜ"))
            return
        f.bstack1llllll1ll1_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll11l1ll_opy_, bstack1l1l111111l_opy_)
    def bstack1l11llll1ll_opy_(self, context: bstack1llll1lllll_opy_, bstack1l1l11111l1_opy_= True):
        if bstack1l1l11111l1_opy_:
            bstack1l1l111111l_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        else:
            bstack1l1l111111l_opy_ = self.bstack1l1lllll11l_opy_(context, reverse=True)
        return [f for f in bstack1l1l111111l_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    def bstack1ll11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጝ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠣࠤጞ"))
            return
        bstack1l1l111111l_opy_ = f.bstack1llllllllll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጟ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠥࠦጠ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(
                bstack1llll111ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጡ"))
        bstack1l11lll1lll_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l111111l_opy_[0]
        page = bstack1l11lll1lll_opy_()
        if not page:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጢ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢጣ"))
            return
        bstack1l11111l1_opy_ = getattr(args[0], bstack1l11ll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢጤ"), None)
        try:
            page.evaluate(bstack1l11ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤጥ"),
                        bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ጦ") + json.dumps(
                            bstack1l11111l1_opy_) + bstack1l11ll1_opy_ (u"ࠥࢁࢂࠨጧ"))
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤጨ"), e)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጩ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢጪ"))
            return
        bstack1l1l111111l_opy_ = f.bstack1llllllllll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጫ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠣࠤጬ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(
                bstack1llll111ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦጭ"))
        bstack1l11lll1lll_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l111111l_opy_[0]
        page = bstack1l11lll1lll_opy_()
        if not page:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጮ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠦࠧጯ"))
            return
        status = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1111ll1_opy_, None)
        if not status:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣጰ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢጱ"))
            return
        bstack1l11llll1l1_opy_ = {bstack1l11ll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢጲ"): status.lower()}
        bstack1l1l1111111_opy_ = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_, None)
        if status.lower() == bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጳ") and bstack1l1l1111111_opy_ is not None:
            bstack1l11llll1l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩጴ")] = bstack1l1l1111111_opy_[0][bstack1l11ll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ጵ")][0] if isinstance(bstack1l1l1111111_opy_, list) else str(bstack1l1l1111111_opy_)
        try:
              page.evaluate(
                    bstack1l11ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧጶ"),
                    bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࠪጷ")
                    + json.dumps(bstack1l11llll1l1_opy_)
                    + bstack1l11ll1_opy_ (u"ࠨࡽࠣጸ")
                )
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢጹ"), e)
    def bstack1l1lll1l111_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        f: TestFramework,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(
                bstack1llll111ll1_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤጺ"))
            return
        bstack1l1l111111l_opy_ = f.bstack1llllllllll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጻ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠥࠦጼ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(
                bstack1llll111ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጽ"))
        bstack1l11lll1lll_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l111111l_opy_[0]
        page = bstack1l11lll1lll_opy_()
        if not page:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጾ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢጿ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l11ll1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧፀ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l11ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤፁ"),
                bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧፂ").format(
                    json.dumps(
                        {
                            bstack1l11ll1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥፃ"): bstack1l11ll1_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨፄ"),
                            bstack1l11ll1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣፅ"): {
                                bstack1l11ll1_opy_ (u"ࠨࡴࡺࡲࡨࠦፆ"): bstack1l11ll1_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦፇ"),
                                bstack1l11ll1_opy_ (u"ࠣࡦࡤࡸࡦࠨፈ"): data,
                                bstack1l11ll1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣፉ"): bstack1l11ll1_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤፊ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡰ࠳࠴ࡽࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡿࢂࠨፋ"), e)
    def bstack1l1ll1ll1l1_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        f: TestFramework,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111lll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if f.bstack1llllllllll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1lll111l1_opy_, False):
            return
        self.bstack1ll11l111l1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_)
        req.test_framework_name = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        req.test_framework_version = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1l1l1ll_opy_)
        req.test_framework_state = bstack1lllll1llll_opy_[0].name
        req.test_hook_state = bstack1lllll1llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        for bstack1l11llllll1_opy_ in bstack1ll1l1lllll_opy_.bstack1llllll1lll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦፌ")
                if bstack1l1lll11ll1_opy_
                else bstack1l11ll1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧፍ")
            )
            session.ref = bstack1l11llllll1_opy_.ref()
            session.hub_url = bstack1ll1l1lllll_opy_.bstack1llllllllll_opy_(bstack1l11llllll1_opy_, bstack1ll1l1lllll_opy_.bstack1l1l11l1ll1_opy_, bstack1l11ll1_opy_ (u"ࠢࠣፎ"))
            session.framework_name = bstack1l11llllll1_opy_.framework_name
            session.framework_version = bstack1l11llllll1_opy_.framework_version
            session.framework_session_id = bstack1ll1l1lllll_opy_.bstack1llllllllll_opy_(bstack1l11llllll1_opy_, bstack1ll1l1lllll_opy_.bstack1l1l11l1l1l_opy_, bstack1l11ll1_opy_ (u"ࠣࠤፏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l111111l_opy_ = f.bstack1llllllllll_opy_(instance, bstack1ll1lll1l1l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፐ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠥࠦፑ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፒ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠧࠨፓ"))
        bstack1l11lll1lll_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l111111l_opy_[0]
        page = bstack1l11lll1lll_opy_()
        if not page:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፔ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠢࠣፕ"))
            return
        return page
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l11lllll1l_opy_ = {}
        for bstack1l11llllll1_opy_ in bstack1ll1l1lllll_opy_.bstack1llllll1lll_opy_.values():
            caps = bstack1ll1l1lllll_opy_.bstack1llllllllll_opy_(bstack1l11llllll1_opy_, bstack1ll1l1lllll_opy_.bstack1l1l111lll1_opy_, bstack1l11ll1_opy_ (u"ࠣࠤፖ"))
        bstack1l11lllll1l_opy_[bstack1l11ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢፗ")] = caps.get(bstack1l11ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦፘ"), bstack1l11ll1_opy_ (u"ࠦࠧፙ"))
        bstack1l11lllll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦፚ")] = caps.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡴࠤ፛"), bstack1l11ll1_opy_ (u"ࠢࠣ፜"))
        bstack1l11lllll1l_opy_[bstack1l11ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ፝")] = caps.get(bstack1l11ll1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ፞"), bstack1l11ll1_opy_ (u"ࠥࠦ፟"))
        bstack1l11lllll1l_opy_[bstack1l11ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ፠")] = caps.get(bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ፡"), bstack1l11ll1_opy_ (u"ࠨࠢ።"))
        return bstack1l11lllll1l_opy_
    def bstack1ll1l11l111_opy_(self, page: object, bstack1ll11llllll_opy_, args={}):
        try:
            bstack1l11lllllll_opy_ = bstack1l11ll1_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨ፣")
            bstack1ll11llllll_opy_ = bstack1ll11llllll_opy_.replace(bstack1l11ll1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ፤"), bstack1l11ll1_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤ፥"))
            script = bstack1l11lllllll_opy_.format(fn_body=bstack1ll11llllll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤ፦") + str(e) + bstack1l11ll1_opy_ (u"ࠦࠧ፧"))