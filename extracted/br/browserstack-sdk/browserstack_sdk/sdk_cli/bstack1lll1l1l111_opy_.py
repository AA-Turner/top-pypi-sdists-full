# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1ll111_opy_,
    bstack1llllll111l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1lll111_opy_, bstack1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_, bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1111_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1l1l_opy_ import bstack1l1lllll111_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l1111111_opy_ import bstack1ll1ll1ll_opy_, bstack1l11lllll1_opy_, bstack1l11ll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll1l1111l_opy_(bstack1l1lllll111_opy_):
    bstack1l1l1111111_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦጔ")
    bstack1l1lll111l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጕ")
    bstack1l1l1111lll_opy_ = bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ጖")
    bstack1l11lllll11_opy_ = bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣ጗")
    bstack1l1l1111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨጘ")
    bstack1l1lll1111l_opy_ = bstack1ll11ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤጙ")
    bstack1l11llll1ll_opy_ = bstack1ll11ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢጚ")
    bstack1l1l11111ll_opy_ = bstack1ll11ll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥጛ")
    def __init__(self):
        super().__init__(bstack1l1llll1l11_opy_=self.bstack1l1l1111111_opy_, frameworks=[bstack1ll1l1ll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.BEFORE_EACH, bstack1ll1lllll11_opy_.POST), self.bstack1l11lllll1l_opy_)
        if bstack1llll1l11_opy_():
            TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll11ll1l11_opy_)
        else:
            TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.PRE), self.bstack1ll11ll1l11_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll1l1111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lll1lll_opy_ = self.bstack1l11llll1l1_opy_(instance.context)
        if not bstack1l11lll1lll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጜ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣጝ"))
            return
        f.bstack1llll1l1lll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll111l1_opy_, bstack1l11lll1lll_opy_)
    def bstack1l11llll1l1_opy_(self, context: bstack1llllll111l_opy_, bstack1l11llllll1_opy_= True):
        if bstack1l11llllll1_opy_:
            bstack1l11lll1lll_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        else:
            bstack1l11lll1lll_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        return [f for f in bstack1l11lll1lll_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    def bstack1ll11ll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllll1l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጞ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠤࠥጟ"))
            return
        bstack1l11lll1lll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l11lll1lll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጠ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠦࠧጡ"))
            return
        if len(bstack1l11lll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lll111ll1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢጢ"))
        bstack1l11lll1ll1_opy_, bstack1l1l11lllll_opy_ = bstack1l11lll1lll_opy_[0]
        page = bstack1l11lll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጣ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣጤ"))
            return
        bstack11ll1l1l_opy_ = getattr(args[0], bstack1ll11ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣጥ"), None)
        try:
            page.evaluate(bstack1ll11ll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥጦ"),
                        bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧጧ") + json.dumps(
                            bstack11ll1l1l_opy_) + bstack1ll11ll_opy_ (u"ࠦࢂࢃࠢጨ"))
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥጩ"), e)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllll1l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጪ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣጫ"))
            return
        bstack1l11lll1lll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l11lll1lll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጬ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠤࠥጭ"))
            return
        if len(bstack1l11lll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lll111ll1l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧጮ"))
        bstack1l11lll1ll1_opy_, bstack1l1l11lllll_opy_ = bstack1l11lll1lll_opy_[0]
        page = bstack1l11lll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጯ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠧࠨጰ"))
            return
        status = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1l11111l1_opy_, None)
        if not status:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤጱ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣጲ"))
            return
        bstack1l1l1111l11_opy_ = {bstack1ll11ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣጳ"): status.lower()}
        bstack1l11llll11l_opy_ = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1l111111l_opy_, None)
        if status.lower() == bstack1ll11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩጴ") and bstack1l11llll11l_opy_ is not None:
            bstack1l1l1111l11_opy_[bstack1ll11ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪጵ")] = bstack1l11llll11l_opy_[0][bstack1ll11ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧጶ")][0] if isinstance(bstack1l11llll11l_opy_, list) else str(bstack1l11llll11l_opy_)
        try:
              page.evaluate(
                    bstack1ll11ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጷ"),
                    bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࠫጸ")
                    + json.dumps(bstack1l1l1111l11_opy_)
                    + bstack1ll11ll_opy_ (u"ࠢࡾࠤጹ")
                )
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣጺ"), e)
    def bstack1l1l1llll11_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        f: TestFramework,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllll1l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if not bstack1l1l1lll111_opy_:
            self.logger.debug(
                bstack1lll111ll1l_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥጻ"))
            return
        bstack1l11lll1lll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l11lll1lll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጼ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠦࠧጽ"))
            return
        if len(bstack1l11lll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lll111ll1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢጾ"))
        bstack1l11lll1ll1_opy_, bstack1l1l11lllll_opy_ = bstack1l11lll1lll_opy_[0]
        page = bstack1l11lll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጿ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣፀ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1ll11ll_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨፁ") + str(timestamp)
        try:
            page.evaluate(
                bstack1ll11ll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥፂ"),
                bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨፃ").format(
                    json.dumps(
                        {
                            bstack1ll11ll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦፄ"): bstack1ll11ll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢፅ"),
                            bstack1ll11ll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤፆ"): {
                                bstack1ll11ll_opy_ (u"ࠢࡵࡻࡳࡩࠧፇ"): bstack1ll11ll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧፈ"),
                                bstack1ll11ll_opy_ (u"ࠤࡧࡥࡹࡧࠢፉ"): data,
                                bstack1ll11ll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤፊ"): bstack1ll11ll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥፋ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡱ࠴࠵ࡾࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࢀࢃࠢፌ"), e)
    def bstack1l1l1ll111l_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        f: TestFramework,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllll1l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if f.bstack1llll1lllll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll1111l_opy_, False):
            return
        self.bstack1ll11l11lll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll1111lll1_opy_)
        req.test_framework_name = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11ll111l_opy_)
        req.test_framework_version = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1ll1l1111_opy_)
        req.test_framework_state = bstack1llll1ll1l1_opy_[0].name
        req.test_hook_state = bstack1llll1ll1l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
        for bstack1l11lllllll_opy_ in bstack1lll1lll111_opy_.bstack1lllllll111_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧፍ")
                if bstack1l1l1lll111_opy_
                else bstack1ll11ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨፎ")
            )
            session.ref = bstack1l11lllllll_opy_.ref()
            session.hub_url = bstack1lll1lll111_opy_.bstack1llll1lllll_opy_(bstack1l11lllllll_opy_, bstack1lll1lll111_opy_.bstack1l1l11l1ll1_opy_, bstack1ll11ll_opy_ (u"ࠣࠤፏ"))
            session.framework_name = bstack1l11lllllll_opy_.framework_name
            session.framework_version = bstack1l11lllllll_opy_.framework_version
            session.framework_session_id = bstack1lll1lll111_opy_.bstack1llll1lllll_opy_(bstack1l11lllllll_opy_, bstack1lll1lll111_opy_.bstack1l1l111l111_opy_, bstack1ll11ll_opy_ (u"ࠤࠥፐ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l11lll1lll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l11lll1lll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፑ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠦࠧፒ"))
            return
        if len(bstack1l11lll1lll_opy_) > 1:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፓ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠨࠢፔ"))
        bstack1l11lll1ll1_opy_, bstack1l1l11lllll_opy_ = bstack1l11lll1lll_opy_[0]
        page = bstack1l11lll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፕ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠣࠤፖ"))
            return
        return page
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l11llll111_opy_ = {}
        for bstack1l11lllllll_opy_ in bstack1lll1lll111_opy_.bstack1lllllll111_opy_.values():
            caps = bstack1lll1lll111_opy_.bstack1llll1lllll_opy_(bstack1l11lllllll_opy_, bstack1lll1lll111_opy_.bstack1l1l11ll111_opy_, bstack1ll11ll_opy_ (u"ࠤࠥፗ"))
        bstack1l11llll111_opy_[bstack1ll11ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣፘ")] = caps.get(bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧፙ"), bstack1ll11ll_opy_ (u"ࠧࠨፚ"))
        bstack1l11llll111_opy_[bstack1ll11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ፛")] = caps.get(bstack1ll11ll_opy_ (u"ࠢࡰࡵࠥ፜"), bstack1ll11ll_opy_ (u"ࠣࠤ፝"))
        bstack1l11llll111_opy_[bstack1ll11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ፞")] = caps.get(bstack1ll11ll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ፟"), bstack1ll11ll_opy_ (u"ࠦࠧ፠"))
        bstack1l11llll111_opy_[bstack1ll11ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ፡")] = caps.get(bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ።"), bstack1ll11ll_opy_ (u"ࠢࠣ፣"))
        return bstack1l11llll111_opy_
    def bstack1ll111l111l_opy_(self, page: object, bstack1ll11ll1ll1_opy_, args={}):
        try:
            bstack1l1l1111l1l_opy_ = bstack1ll11ll_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢ፤")
            bstack1ll11ll1ll1_opy_ = bstack1ll11ll1ll1_opy_.replace(bstack1ll11ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ፥"), bstack1ll11ll_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥ፦"))
            script = bstack1l1l1111l1l_opy_.format(fn_body=bstack1ll11ll1ll1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥ፧") + str(e) + bstack1ll11ll_opy_ (u"ࠧࠨ፨"))