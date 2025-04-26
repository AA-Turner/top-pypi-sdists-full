# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
    bstack1111l11lll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1lllll_opy_, bstack11llllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_, bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1lll111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll11_opy_ import bstack1ll11l11l1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11ll1111l_opy_ import bstack11ll11l111_opy_, bstack11l1111l1_opy_, bstack1lll111l11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lll11llll1_opy_(bstack1ll11l11l1l_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1l11lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦብ")
    bstack1l1llllll1l_opy_ = bstack1l11lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧቦ")
    bstack1l1l1ll1lll_opy_ = bstack1l11lll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤቧ")
    bstack1l1l1l1l1ll_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣቨ")
    bstack1l1l1llll11_opy_ = bstack1l11lll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨቩ")
    bstack1l1llll11ll_opy_ = bstack1l11lll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤቪ")
    bstack1l1l1lll1l1_opy_ = bstack1l11lll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢቫ")
    bstack1l1l1ll1l11_opy_ = bstack1l11lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥቬ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll1l_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1lll1l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.BEFORE_EACH, bstack1lll1l1l11l_opy_.POST), self.bstack1l1l1ll11l1_opy_)
        if bstack11llllll1l_opy_():
            TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST), self.bstack1ll1ll1ll11_opy_)
        else:
            TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.PRE), self.bstack1ll1ll1ll11_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l1ll11_opy_ = self.bstack1l1l1lll11l_opy_(instance.context)
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦቭ") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠢࠣቮ"))
            return
        f.bstack1111l111ll_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llllll1l_opy_, bstack1l1l1l1ll11_opy_)
    def bstack1l1l1lll11l_opy_(self, context: bstack1111l11lll_opy_, bstack1l1l1l1llll_opy_= True):
        if bstack1l1l1l1llll_opy_:
            bstack1l1l1l1ll11_opy_ = self.bstack1ll11l1l11l_opy_(context, reverse=True)
        else:
            bstack1l1l1l1ll11_opy_ = self.bstack1ll11l111l1_opy_(context, reverse=True)
        return [f for f in bstack1l1l1l1ll11_opy_ if f[1].state != bstack111111lll1_opy_.QUIT]
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll11l1_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not bstack1l1ll1lllll_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቯ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠤࠥተ"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1111111111_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቱ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠦࠧቲ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢታ"))
        bstack1l1l1ll111l_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1ll111l_opy_()
        if not page:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቴ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠢࠣት"))
            return
        bstack11lll1llll_opy_ = getattr(args[0], bstack1l11lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣቶ"), None)
        try:
            page.evaluate(bstack1l11lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥቷ"),
                        bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧቸ") + json.dumps(
                            bstack11lll1llll_opy_) + bstack1l11lll_opy_ (u"ࠦࢂࢃࠢቹ"))
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥቺ"), e)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll11l1_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not bstack1l1ll1lllll_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤቻ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠢࠣቼ"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1111111111_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦች") + str(kwargs) + bstack1l11lll_opy_ (u"ࠤࠥቾ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧቿ"))
        bstack1l1l1ll111l_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1ll111l_opy_()
        if not page:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኀ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨኁ"))
            return
        status = f.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, None)
        if not status:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤኂ") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠢࠣኃ"))
            return
        bstack1l1l1l1ll1l_opy_ = {bstack1l11lll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣኄ"): status.lower()}
        bstack1l1l1ll1111_opy_ = f.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1lll1ll_opy_, None)
        if status.lower() == bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩኅ") and bstack1l1l1ll1111_opy_ is not None:
            bstack1l1l1l1ll1l_opy_[bstack1l11lll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪኆ")] = bstack1l1l1ll1111_opy_[0][bstack1l11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧኇ")][0] if isinstance(bstack1l1l1ll1111_opy_, list) else str(bstack1l1l1ll1111_opy_)
        try:
              page.evaluate(
                    bstack1l11lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨኈ"),
                    bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࠫ኉")
                    + json.dumps(bstack1l1l1l1ll1l_opy_)
                    + bstack1l11lll_opy_ (u"ࠢࡾࠤኊ")
                )
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣኋ"), e)
    def bstack1l1lll1l11l_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll11l1_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not bstack1l1ll1lllll_opy_:
            self.logger.debug(
                bstack1lll1l1111l_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥኌ"))
            return
        bstack1l1l1l1ll11_opy_ = f.bstack1111111111_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኍ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠦࠧ኎"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢ኏"))
        bstack1l1l1ll111l_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1ll111l_opy_()
        if not page:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨነ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠢࠣኑ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l11lll_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨኒ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l11lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥና"),
                bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨኔ").format(
                    json.dumps(
                        {
                            bstack1l11lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦን"): bstack1l11lll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢኖ"),
                            bstack1l11lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤኗ"): {
                                bstack1l11lll_opy_ (u"ࠢࡵࡻࡳࡩࠧኘ"): bstack1l11lll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧኙ"),
                                bstack1l11lll_opy_ (u"ࠤࡧࡥࡹࡧࠢኚ"): data,
                                bstack1l11lll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤኛ"): bstack1l11lll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥኜ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡱ࠴࠵ࡾࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࢀࢃࠢኝ"), e)
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll11l1_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if f.bstack1111111111_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llll11ll_opy_, False):
            return
        self.bstack1ll1ll1l11l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        req.test_framework_name = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l1ll111_opy_)
        req.test_framework_version = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_)
        req.test_framework_state = bstack11111l11ll_opy_[0].name
        req.test_hook_state = bstack11111l11ll_opy_[1].name
        req.test_uuid = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1ll11lll_opy_)
        for bstack1l1l1l1lll1_opy_ in bstack1lll111ll11_opy_.bstack11111lllll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧኞ")
                if bstack1l1ll1lllll_opy_
                else bstack1l11lll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨኟ")
            )
            session.ref = bstack1l1l1l1lll1_opy_.ref()
            session.hub_url = bstack1lll111ll11_opy_.bstack1111111111_opy_(bstack1l1l1l1lll1_opy_, bstack1lll111ll11_opy_.bstack1l1ll11l1ll_opy_, bstack1l11lll_opy_ (u"ࠣࠤአ"))
            session.framework_name = bstack1l1l1l1lll1_opy_.framework_name
            session.framework_version = bstack1l1l1l1lll1_opy_.framework_version
            session.framework_session_id = bstack1lll111ll11_opy_.bstack1111111111_opy_(bstack1l1l1l1lll1_opy_, bstack1lll111ll11_opy_.bstack1l1ll111l1l_opy_, bstack1l11lll_opy_ (u"ࠤࠥኡ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1l1ll11_opy_ = f.bstack1111111111_opy_(instance, bstack1lll11llll1_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1l1l1ll11_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኢ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠦࠧኣ"))
            return
        if len(bstack1l1l1l1ll11_opy_) > 1:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኤ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠨࠢእ"))
        bstack1l1l1ll111l_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1l1l1ll11_opy_[0]
        page = bstack1l1l1ll111l_opy_()
        if not page:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኦ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠣࠤኧ"))
            return
        return page
    def bstack1ll1l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1ll1ll1_opy_ = {}
        for bstack1l1l1l1lll1_opy_ in bstack1lll111ll11_opy_.bstack11111lllll_opy_.values():
            caps = bstack1lll111ll11_opy_.bstack1111111111_opy_(bstack1l1l1l1lll1_opy_, bstack1lll111ll11_opy_.bstack1l1ll11llll_opy_, bstack1l11lll_opy_ (u"ࠤࠥከ"))
        bstack1l1l1ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣኩ")] = caps.get(bstack1l11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧኪ"), bstack1l11lll_opy_ (u"ࠧࠨካ"))
        bstack1l1l1ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧኬ")] = caps.get(bstack1l11lll_opy_ (u"ࠢࡰࡵࠥክ"), bstack1l11lll_opy_ (u"ࠣࠤኮ"))
        bstack1l1l1ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦኯ")] = caps.get(bstack1l11lll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢኰ"), bstack1l11lll_opy_ (u"ࠦࠧ኱"))
        bstack1l1l1ll1ll1_opy_[bstack1l11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨኲ")] = caps.get(bstack1l11lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣኳ"), bstack1l11lll_opy_ (u"ࠢࠣኴ"))
        return bstack1l1l1ll1ll1_opy_
    def bstack1ll1l11l1ll_opy_(self, page: object, bstack1ll1l1llll1_opy_, args={}):
        try:
            bstack1l1l1lll111_opy_ = bstack1l11lll_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢኵ")
            bstack1ll1l1llll1_opy_ = bstack1ll1l1llll1_opy_.replace(bstack1l11lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ኶"), bstack1l11lll_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥ኷"))
            script = bstack1l1l1lll111_opy_.format(fn_body=bstack1ll1l1llll1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥኸ") + str(e) + bstack1l11lll_opy_ (u"ࠧࠨኹ"))