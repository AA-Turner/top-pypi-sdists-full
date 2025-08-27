# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll11_opy_,
    bstack1111111ll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11l1l_opy_, bstack1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll111l_opy_, bstack1lll111111l_opy_, bstack1ll1ll1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1l1_opy_ import bstack1ll1111111l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l1lll111_opy_ import bstack1111ll1ll_opy_, bstack11l1ll1l_opy_, bstack1ll11ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll111l11l_opy_(bstack1ll1111111l_opy_):
    bstack1l1l111ll1l_opy_ = bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢጐ")
    bstack1l1ll1lll1l_opy_ = bstack1111lll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣ጑")
    bstack1l1l1111l11_opy_ = bstack1111lll_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጒ")
    bstack1l1l11111ll_opy_ = bstack1111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጓ")
    bstack1l1l111l1l1_opy_ = bstack1111lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤጔ")
    bstack1l1llll11ll_opy_ = bstack1111lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጕ")
    bstack1l11lllllll_opy_ = bstack1111lll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥ጖")
    bstack1l11lllll11_opy_ = bstack1111lll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨ጗")
    def __init__(self):
        super().__init__(bstack1l1lllll111_opy_=self.bstack1l1l111ll1l_opy_, frameworks=[bstack1lll1lll11l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.BEFORE_EACH, bstack1lll111111l_opy_.POST), self.bstack1l1l111l1ll_opy_)
        if bstack1l111lll_opy_():
            TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST), self.bstack1ll1l11l111_opy_)
        else:
            TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.PRE), self.bstack1ll1l11l111_opy_)
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST), self.bstack1ll1l11ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lllll1l_opy_ = self.bstack1l1l1111lll_opy_(instance.context)
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጘ") + str(bstack1llllll11ll_opy_) + bstack1111lll_opy_ (u"ࠥࠦጙ"))
            return
        f.bstack1llllll1l1l_opy_(instance, bstack1lll111l11l_opy_.bstack1l1ll1lll1l_opy_, bstack1l11lllll1l_opy_)
    def bstack1l1l1111lll_opy_(self, context: bstack1111111ll1_opy_, bstack1l1l1111l1l_opy_= True):
        if bstack1l1l1111l1l_opy_:
            bstack1l11lllll1l_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        else:
            bstack1l11lllll1l_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        return [f for f in bstack1l11lllll1l_opy_ if f[1].state != bstack1lllll1lll1_opy_.QUIT]
    def bstack1ll1l11l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጚ") + str(kwargs) + bstack1111lll_opy_ (u"ࠧࠨጛ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1llllll1l11_opy_(instance, bstack1lll111l11l_opy_.bstack1l1ll1lll1l_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጜ") + str(kwargs) + bstack1111lll_opy_ (u"ࠢࠣጝ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥጞ"))
        bstack1l1l111111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጟ") + str(kwargs) + bstack1111lll_opy_ (u"ࠥࠦጠ"))
            return
        bstack11llllll1_opy_ = getattr(args[0], bstack1111lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦጡ"), None)
        try:
            page.evaluate(bstack1111lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጢ"),
                        bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪጣ") + json.dumps(
                            bstack11llllll1_opy_) + bstack1111lll_opy_ (u"ࠢࡾࡿࠥጤ"))
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨጥ"), e)
    def bstack1ll1l11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጦ") + str(kwargs) + bstack1111lll_opy_ (u"ࠥࠦጧ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1llllll1l11_opy_(instance, bstack1lll111l11l_opy_.bstack1l1ll1lll1l_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጨ") + str(kwargs) + bstack1111lll_opy_ (u"ࠧࠨጩ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጪ"))
        bstack1l1l111111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጫ") + str(kwargs) + bstack1111lll_opy_ (u"ࠣࠤጬ"))
            return
        status = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_, None)
        if not status:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጭ") + str(bstack1llllll11ll_opy_) + bstack1111lll_opy_ (u"ࠥࠦጮ"))
            return
        bstack1l11llllll1_opy_ = {bstack1111lll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦጯ"): status.lower()}
        bstack1l1l1111111_opy_ = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1l111l111_opy_, None)
        if status.lower() == bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬጰ") and bstack1l1l1111111_opy_ is not None:
            bstack1l11llllll1_opy_[bstack1111lll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ጱ")] = bstack1l1l1111111_opy_[0][bstack1111lll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪጲ")][0] if isinstance(bstack1l1l1111111_opy_, list) else str(bstack1l1l1111111_opy_)
        try:
              page.evaluate(
                    bstack1111lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤጳ"),
                    bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧጴ")
                    + json.dumps(bstack1l11llllll1_opy_)
                    + bstack1111lll_opy_ (u"ࠥࢁࠧጵ")
                )
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦጶ"), e)
    def bstack1l1ll1l1l1l_opy_(
        self,
        instance: bstack1ll1ll1l1l1_opy_,
        f: TestFramework,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(
                bstack1llll1l1ll1_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጷ"))
            return
        bstack1l11lllll1l_opy_ = f.bstack1llllll1l11_opy_(instance, bstack1lll111l11l_opy_.bstack1l1ll1lll1l_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጸ") + str(kwargs) + bstack1111lll_opy_ (u"ࠢࠣጹ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(
                bstack1llll1l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥጺ"))
        bstack1l1l111111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጻ") + str(kwargs) + bstack1111lll_opy_ (u"ࠥࠦጼ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1111lll_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤጽ") + str(timestamp)
        try:
            page.evaluate(
                bstack1111lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨጾ"),
                bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫጿ").format(
                    json.dumps(
                        {
                            bstack1111lll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢፀ"): bstack1111lll_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥፁ"),
                            bstack1111lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧፂ"): {
                                bstack1111lll_opy_ (u"ࠥࡸࡾࡶࡥࠣፃ"): bstack1111lll_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣፄ"),
                                bstack1111lll_opy_ (u"ࠧࡪࡡࡵࡣࠥፅ"): data,
                                bstack1111lll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧፆ"): bstack1111lll_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨፇ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥፈ"), e)
    def bstack1l1l1ll1lll_opy_(
        self,
        instance: bstack1ll1ll1l1l1_opy_,
        f: TestFramework,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        if f.bstack1llllll1l11_opy_(instance, bstack1lll111l11l_opy_.bstack1l1llll11ll_opy_, False):
            return
        self.bstack1ll1l111lll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1ll11_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1l1l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        req.test_framework_state = bstack1llllll11ll_opy_[0].name
        req.test_hook_state = bstack1llllll11ll_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
        for bstack1l1l111l11l_opy_ in bstack1llll1l1l11_opy_.bstack1lllllll11l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣፉ")
                if bstack1l1lll11l1l_opy_
                else bstack1111lll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤፊ")
            )
            session.ref = bstack1l1l111l11l_opy_.ref()
            session.hub_url = bstack1llll1l1l11_opy_.bstack1llllll1l11_opy_(bstack1l1l111l11l_opy_, bstack1llll1l1l11_opy_.bstack1l1l11l1l1l_opy_, bstack1111lll_opy_ (u"ࠦࠧፋ"))
            session.framework_name = bstack1l1l111l11l_opy_.framework_name
            session.framework_version = bstack1l1l111l11l_opy_.framework_version
            session.framework_session_id = bstack1llll1l1l11_opy_.bstack1llllll1l11_opy_(bstack1l1l111l11l_opy_, bstack1llll1l1l11_opy_.bstack1l1l11ll1l1_opy_, bstack1111lll_opy_ (u"ࠧࠨፌ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l11lllll1l_opy_ = f.bstack1llllll1l11_opy_(instance, bstack1lll111l11l_opy_.bstack1l1ll1lll1l_opy_, [])
        if not bstack1l11lllll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፍ") + str(kwargs) + bstack1111lll_opy_ (u"ࠢࠣፎ"))
            return
        if len(bstack1l11lllll1l_opy_) > 1:
            self.logger.debug(bstack1111lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፏ") + str(kwargs) + bstack1111lll_opy_ (u"ࠤࠥፐ"))
        bstack1l1l111111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l11lllll1l_opy_[0]
        page = bstack1l1l111111l_opy_()
        if not page:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፑ") + str(kwargs) + bstack1111lll_opy_ (u"ࠦࠧፒ"))
            return
        return page
    def bstack1ll11llll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1111ll1_opy_ = {}
        for bstack1l1l111l11l_opy_ in bstack1llll1l1l11_opy_.bstack1lllllll11l_opy_.values():
            caps = bstack1llll1l1l11_opy_.bstack1llllll1l11_opy_(bstack1l1l111l11l_opy_, bstack1llll1l1l11_opy_.bstack1l1l11llll1_opy_, bstack1111lll_opy_ (u"ࠧࠨፓ"))
        bstack1l1l1111ll1_opy_[bstack1111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦፔ")] = caps.get(bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣፕ"), bstack1111lll_opy_ (u"ࠣࠤፖ"))
        bstack1l1l1111ll1_opy_[bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣፗ")] = caps.get(bstack1111lll_opy_ (u"ࠥࡳࡸࠨፘ"), bstack1111lll_opy_ (u"ࠦࠧፙ"))
        bstack1l1l1111ll1_opy_[bstack1111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢፚ")] = caps.get(bstack1111lll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ፛"), bstack1111lll_opy_ (u"ࠢࠣ፜"))
        bstack1l1l1111ll1_opy_[bstack1111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ፝")] = caps.get(bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ፞"), bstack1111lll_opy_ (u"ࠥࠦ፟"))
        return bstack1l1l1111ll1_opy_
    def bstack1ll1l11l1l1_opy_(self, page: object, bstack1ll1l111l1l_opy_, args={}):
        try:
            bstack1l1l11111l1_opy_ = bstack1111lll_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥ፠")
            bstack1ll1l111l1l_opy_ = bstack1ll1l111l1l_opy_.replace(bstack1111lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ፡"), bstack1111lll_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨ።"))
            script = bstack1l1l11111l1_opy_.format(fn_body=bstack1ll1l111l1l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨ፣") + str(e) + bstack1111lll_opy_ (u"ࠣࠤ፤"))