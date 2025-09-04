# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll1l_opy_,
    bstack1llll1l1ll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1l1l1l_opy_, bstack1ll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1l1_opy_ import bstack1l1llll1lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1ll1l11l11_opy_ import bstack1ll1l1l1l_opy_, bstack1l11111l1l_opy_, bstack1l11l11l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll11111l1_opy_(bstack1l1llll1lll_opy_):
    bstack1l1l111111l_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧጕ")
    bstack1l1lll1l1l1_opy_ = bstack1111l1l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨ጖")
    bstack1l1l1111111_opy_ = bstack1111l1l_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥ጗")
    bstack1l1l1111ll1_opy_ = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤጘ")
    bstack1l1l11111ll_opy_ = bstack1111l1l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢጙ")
    bstack1l1ll1ll111_opy_ = bstack1111l1l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥጚ")
    bstack1l11llll1l1_opy_ = bstack1111l1l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣጛ")
    bstack1l11llll1ll_opy_ = bstack1111l1l_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦጜ")
    def __init__(self):
        super().__init__(bstack1l1lllll11l_opy_=self.bstack1l1l111111l_opy_, frameworks=[bstack1lll1l111ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.BEFORE_EACH, bstack1ll1llll1ll_opy_.POST), self.bstack1l11lllllll_opy_)
        if bstack1ll1l1l1l1_opy_():
            TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll1111l1l1_opy_)
        else:
            TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE), self.bstack1ll1111l1l1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll11llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lllll1l_opy_ = self.bstack1l11llllll1_opy_(instance.context)
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጝ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠣࠤጞ"))
            return
        f.bstack1lllllllll1_opy_(instance, bstack1lll11111l1_opy_.bstack1l1lll1l1l1_opy_, bstack1l11lllll1l_opy_)
    def bstack1l11llllll1_opy_(self, context: bstack1llll1l1ll1_opy_, bstack1l11lllll11_opy_= True):
        if bstack1l11lllll11_opy_:
            bstack1l11lllll1l_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        else:
            bstack1l11lllll1l_opy_ = self.bstack1l1llll111l_opy_(context, reverse=True)
        return [f for f in bstack1l11lllll1l_opy_ if f[1].state != bstack1lllll11111_opy_.QUIT]
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1ll1l1l1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጟ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠥࠦጠ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll11111l1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጡ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠧࠨጢ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1lll11lll1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጣ"))
        bstack1l1l1111lll_opy_, bstack1l1l11lllll_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l1111lll_opy_()
        if not page:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጤ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤጥ"))
            return
        bstack1ll1l1ll_opy_ = getattr(args[0], bstack1111l1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤጦ"), None)
        try:
            page.evaluate(bstack1111l1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦጧ"),
                        bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨጨ") + json.dumps(
                            bstack1ll1l1ll_opy_) + bstack1111l1l_opy_ (u"ࠧࢃࡽࠣጩ"))
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦጪ"), e)
    def bstack1ll11llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1ll1l1l1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጫ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤጬ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll11111l1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጭ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠥࠦጮ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1lll11lll1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጯ"))
        bstack1l1l1111lll_opy_, bstack1l1l11lllll_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l1111lll_opy_()
        if not page:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጰ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠨࠢጱ"))
            return
        status = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_, None)
        if not status:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጲ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠣࠤጳ"))
            return
        bstack1l1l111l111_opy_ = {bstack1111l1l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤጴ"): status.lower()}
        bstack1l11llll111_opy_ = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l11111l1_opy_, None)
        if status.lower() == bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪጵ") and bstack1l11llll111_opy_ is not None:
            bstack1l1l111l111_opy_[bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫጶ")] = bstack1l11llll111_opy_[0][bstack1111l1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨጷ")][0] if isinstance(bstack1l11llll111_opy_, list) else str(bstack1l11llll111_opy_)
        try:
              page.evaluate(
                    bstack1111l1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢጸ"),
                    bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬጹ")
                    + json.dumps(bstack1l1l111l111_opy_)
                    + bstack1111l1l_opy_ (u"ࠣࡿࠥጺ")
                )
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤጻ"), e)
    def bstack1l1ll111111_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not bstack1l1ll1l1l1l_opy_:
            self.logger.debug(
                bstack1lll11lll1l_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦጼ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll11111l1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጽ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠧࠨጾ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1lll11lll1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጿ"))
        bstack1l1l1111lll_opy_, bstack1l1l11lllll_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l1111lll_opy_()
        if not page:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፀ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤፁ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1111l1l_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢፂ") + str(timestamp)
        try:
            page.evaluate(
                bstack1111l1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦፃ"),
                bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩፄ").format(
                    json.dumps(
                        {
                            bstack1111l1l_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧፅ"): bstack1111l1l_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣፆ"),
                            bstack1111l1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥፇ"): {
                                bstack1111l1l_opy_ (u"ࠣࡶࡼࡴࡪࠨፈ"): bstack1111l1l_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨፉ"),
                                bstack1111l1l_opy_ (u"ࠥࡨࡦࡺࡡࠣፊ"): data,
                                bstack1111l1l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥፋ"): bstack1111l1l_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦፌ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣፍ"), e)
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lllllll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll11111l1_opy_.bstack1l1ll1ll111_opy_, False):
            return
        self.bstack1ll1l1111ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        for bstack1l1l1111l11_opy_ in bstack1ll1lll1lll_opy_.bstack1111111111_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨፎ")
                if bstack1l1ll1l1l1l_opy_
                else bstack1111l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢፏ")
            )
            session.ref = bstack1l1l1111l11_opy_.ref()
            session.hub_url = bstack1ll1lll1lll_opy_.bstack1lllll1l11l_opy_(bstack1l1l1111l11_opy_, bstack1ll1lll1lll_opy_.bstack1l1l111ll11_opy_, bstack1111l1l_opy_ (u"ࠤࠥፐ"))
            session.framework_name = bstack1l1l1111l11_opy_.framework_name
            session.framework_version = bstack1l1l1111l11_opy_.framework_version
            session.framework_session_id = bstack1ll1lll1lll_opy_.bstack1lllll1l11l_opy_(bstack1l1l1111l11_opy_, bstack1ll1lll1lll_opy_.bstack1l1l111llll_opy_, bstack1111l1l_opy_ (u"ࠥࠦፑ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11lllll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll11111l1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፒ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠧࠨፓ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፔ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠢࠣፕ"))
        bstack1l1l1111lll_opy_, bstack1l1l11lllll_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l1111lll_opy_()
        if not page:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፖ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠤࠥፗ"))
            return
        return page
    def bstack1ll11l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l11lll1lll_opy_ = {}
        for bstack1l1l1111l11_opy_ in bstack1ll1lll1lll_opy_.bstack1111111111_opy_.values():
            caps = bstack1ll1lll1lll_opy_.bstack1lllll1l11l_opy_(bstack1l1l1111l11_opy_, bstack1ll1lll1lll_opy_.bstack1l1l111ll1l_opy_, bstack1111l1l_opy_ (u"ࠥࠦፘ"))
        bstack1l11lll1lll_opy_[bstack1111l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤፙ")] = caps.get(bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨፚ"), bstack1111l1l_opy_ (u"ࠨࠢ፛"))
        bstack1l11lll1lll_opy_[bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ፜")] = caps.get(bstack1111l1l_opy_ (u"ࠣࡱࡶࠦ፝"), bstack1111l1l_opy_ (u"ࠤࠥ፞"))
        bstack1l11lll1lll_opy_[bstack1111l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ፟")] = caps.get(bstack1111l1l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ፠"), bstack1111l1l_opy_ (u"ࠧࠨ፡"))
        bstack1l11lll1lll_opy_[bstack1111l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ።")] = caps.get(bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ፣"), bstack1111l1l_opy_ (u"ࠣࠤ፤"))
        return bstack1l11lll1lll_opy_
    def bstack1ll11llllll_opy_(self, page: object, bstack1ll11ll1lll_opy_, args={}):
        try:
            bstack1l11llll11l_opy_ = bstack1111l1l_opy_ (u"ࠤࠥࠦ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩ࠰࠱࠲ࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩࠩࡽࡤࡶ࡬ࡥࡪࡴࡱࡱࢁ࠮ࠨࠢࠣ፥")
            bstack1ll11ll1lll_opy_ = bstack1ll11ll1lll_opy_.replace(bstack1111l1l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ፦"), bstack1111l1l_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦ፧"))
            script = bstack1l11llll11l_opy_.format(fn_body=bstack1ll11ll1lll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮ࠣࠦ፨") + str(e) + bstack1111l1l_opy_ (u"ࠨࠢ፩"))