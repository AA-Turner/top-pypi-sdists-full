# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lll1llll11_opy_,
    bstack1ll1ll1l11l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1llll1ll1l1_opy_, bstack1ll11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_, bstack1lllll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l11l111ll_opy_ import bstack1l11111ll1_opy_, bstack1111l1l11_opy_, bstack11lllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1l1l1111_opy_(bstack1ll1ll1l1ll_opy_):
    bstack1ll1l11l1ll_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᅱ")
    bstack1lll1l1ll11_opy_ = bstack11l1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᅲ")
    bstack1ll1l111ll1_opy_ = bstack11l1111_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᅳ")
    bstack1ll1l11ll1l_opy_ = bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᅴ")
    bstack1ll1l11lll1_opy_ = bstack11l1111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᅵ")
    bstack1111111ll1_opy_ = bstack11l1111_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᅶ")
    bstack1ll11lll1l1_opy_ = bstack11l1111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᅷ")
    bstack1ll1l11llll_opy_ = bstack11l1111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᅸ")
    def __init__(self):
        super().__init__(bstack1ll1ll1l1l1_opy_=self.bstack1ll1l11l1ll_opy_, frameworks=[bstack1lll1ll1l1l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.BEFORE_EACH, bstack1lll1lll1ll_opy_.POST), self.bstack1ll1l1l111l_opy_)
        if bstack1ll11ll111_opy_():
            TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll1lll1_opy_)
        else:
            TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE), self.bstack1lllll1lll1_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11lll11l_opy_ = self.bstack1ll1l111111_opy_(instance.context)
        if not bstack1ll11lll11l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᅹ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠣࠤᅺ"))
            return
        f.bstack1llll111l11_opy_(instance, bstack1ll1l1l1111_opy_.bstack1lll1l1ll11_opy_, bstack1ll11lll11l_opy_)
    def bstack1ll1l111111_opy_(self, context: bstack1ll1ll1l11l_opy_, bstack1ll11lllll1_opy_= True):
        if bstack1ll11lllll1_opy_:
            bstack1ll11lll11l_opy_ = self.bstack1ll1llll1l1_opy_(context, reverse=True)
        else:
            bstack1ll11lll11l_opy_ = self.bstack1ll1lll1ll1_opy_(context, reverse=True)
        return [f for f in bstack1ll11lll11l_opy_ if f[1].state != bstack1lll1llllll_opy_.QUIT]
    def bstack1lllll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l1l111l_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if not bstack1llll1ll1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᅻ") + str(kwargs) + bstack11l1111_opy_ (u"ࠥࠦᅼ"))
            return
        bstack1ll11lll11l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1l1111_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1ll11lll11l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᅽ") + str(kwargs) + bstack11l1111_opy_ (u"ࠧࠨᅾ"))
            return
        if len(bstack1ll11lll11l_opy_) > 1:
            self.logger.debug(
                bstack1lll1111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᅿ"))
        bstack1ll1l11111l_opy_, bstack1lll11ll11l_opy_ = bstack1ll11lll11l_opy_[0]
        page = bstack1ll1l11111l_opy_()
        if not page:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆀ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤᆁ"))
            return
        bstack1ll1ll11ll_opy_ = getattr(args[0], bstack11l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᆂ"), None)
        try:
            page.evaluate(bstack11l1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᆃ"),
                        bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨᆄ") + json.dumps(
                            bstack1ll1ll11ll_opy_) + bstack11l1111_opy_ (u"ࠧࢃࡽࠣᆅ"))
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦᆆ"), e)
    def bstack1lllll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l1l111l_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if not bstack1llll1ll1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᆇ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤᆈ"))
            return
        bstack1ll11lll11l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1l1111_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1ll11lll11l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᆉ") + str(kwargs) + bstack11l1111_opy_ (u"ࠥࠦᆊ"))
            return
        if len(bstack1ll11lll11l_opy_) > 1:
            self.logger.debug(
                bstack1lll1111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᆋ"))
        bstack1ll1l11111l_opy_, bstack1lll11ll11l_opy_ = bstack1ll11lll11l_opy_[0]
        page = bstack1ll1l11111l_opy_()
        if not page:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᆌ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢᆍ"))
            return
        status = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1l11l111_opy_, None)
        if not status:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᆎ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠣࠤᆏ"))
            return
        bstack1ll1l111lll_opy_ = {bstack11l1111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᆐ"): status.lower()}
        bstack1ll11llll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1l111l11_opy_, None)
        if status.lower() == bstack11l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᆑ") and bstack1ll11llll1l_opy_ is not None:
            bstack1ll1l111lll_opy_[bstack11l1111_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᆒ")] = bstack1ll11llll1l_opy_[0][bstack11l1111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᆓ")][0] if isinstance(bstack1ll11llll1l_opy_, list) else str(bstack1ll11llll1l_opy_)
        try:
              page.evaluate(
                    bstack11l1111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᆔ"),
                    bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬᆕ")
                    + json.dumps(bstack1ll1l111lll_opy_)
                    + bstack11l1111_opy_ (u"ࠣࡿࠥᆖ")
                )
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᆗ"), e)
    def bstack1llllllll11_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        f: TestFramework,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l1l111l_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if not bstack1llll1ll1l1_opy_:
            self.logger.debug(
                bstack1lll1111lll_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᆘ"))
            return
        bstack1ll11lll11l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1l1111_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1ll11lll11l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆙ") + str(kwargs) + bstack11l1111_opy_ (u"ࠧࠨᆚ"))
            return
        if len(bstack1ll11lll11l_opy_) > 1:
            self.logger.debug(
                bstack1lll1111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᆛ"))
        bstack1ll1l11111l_opy_, bstack1lll11ll11l_opy_ = bstack1ll11lll11l_opy_[0]
        page = bstack1ll1l11111l_opy_()
        if not page:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆜ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤᆝ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l1111_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᆞ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᆟ"),
                bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᆠ").format(
                    json.dumps(
                        {
                            bstack11l1111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᆡ"): bstack11l1111_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᆢ"),
                            bstack11l1111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᆣ"): {
                                bstack11l1111_opy_ (u"ࠣࡶࡼࡴࡪࠨᆤ"): bstack11l1111_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᆥ"),
                                bstack11l1111_opy_ (u"ࠥࡨࡦࡺࡡࠣᆦ"): data,
                                bstack11l1111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᆧ"): bstack11l1111_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᆨ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣᆩ"), e)
    def bstack1llllll1111_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        f: TestFramework,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1l1l111l_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1l1111_opy_.bstack1111111ll1_opy_, False):
            return
        self.bstack1lll1lll1l1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1llllll1lll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1ll1l11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l11ll1_opy_)
        req.test_framework_state = bstack1llll11l111_opy_[0].name
        req.test_hook_state = bstack1llll11l111_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
        for bstack1ll1l1111ll_opy_ in bstack1ll1lll1l1l_opy_.bstack1ll11llllll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᆪ")
                if bstack1llll1ll1l1_opy_
                else bstack11l1111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᆫ")
            )
            session.ref = bstack1ll1l1111ll_opy_.ref()
            session.hub_url = bstack1ll1lll1l1l_opy_.bstack1lllll1l11l_opy_(bstack1ll1l1111ll_opy_, bstack1ll1lll1l1l_opy_.bstack1ll1ll1l111_opy_, bstack11l1111_opy_ (u"ࠤࠥᆬ"))
            session.framework_name = bstack1ll1l1111ll_opy_.framework_name
            session.framework_version = bstack1ll1l1111ll_opy_.framework_version
            session.framework_session_id = bstack1ll1lll1l1l_opy_.bstack1lllll1l11l_opy_(bstack1ll1l1111ll_opy_, bstack1ll1lll1l1l_opy_.bstack1ll1l1l1ll1_opy_, bstack11l1111_opy_ (u"ࠥࠦᆭ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1ll11lll11l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1l1111_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1ll11lll11l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᆮ") + str(kwargs) + bstack11l1111_opy_ (u"ࠧࠨᆯ"))
            return
        if len(bstack1ll11lll11l_opy_) > 1:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆰ") + str(kwargs) + bstack11l1111_opy_ (u"ࠢࠣᆱ"))
        bstack1ll1l11111l_opy_, bstack1lll11ll11l_opy_ = bstack1ll11lll11l_opy_[0]
        page = bstack1ll1l11111l_opy_()
        if not page:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᆲ") + str(kwargs) + bstack11l1111_opy_ (u"ࠤࠥᆳ"))
            return
        return page
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1ll11lll1ll_opy_ = {}
        for bstack1ll1l1111ll_opy_ in bstack1ll1lll1l1l_opy_.bstack1ll11llllll_opy_.values():
            caps = bstack1ll1lll1l1l_opy_.bstack1lllll1l11l_opy_(bstack1ll1l1111ll_opy_, bstack1ll1lll1l1l_opy_.bstack1ll1ll11l11_opy_, bstack11l1111_opy_ (u"ࠥࠦᆴ"))
        bstack1ll11lll1ll_opy_[bstack11l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤᆵ")] = caps.get(bstack11l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨᆶ"), bstack11l1111_opy_ (u"ࠨࠢᆷ"))
        bstack1ll11lll1ll_opy_[bstack11l1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᆸ")] = caps.get(bstack11l1111_opy_ (u"ࠣࡱࡶࠦᆹ"), bstack11l1111_opy_ (u"ࠤࠥᆺ"))
        bstack1ll11lll1ll_opy_[bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᆻ")] = caps.get(bstack11l1111_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᆼ"), bstack11l1111_opy_ (u"ࠧࠨᆽ"))
        bstack1ll11lll1ll_opy_[bstack11l1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢᆾ")] = caps.get(bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᆿ"), bstack11l1111_opy_ (u"ࠣࠤᇀ"))
        return bstack1ll11lll1ll_opy_
    def bstack1ll11llll11_opy_(self, page: object, bstack1ll1l11ll11_opy_, args={}):
        try:
            bstack1ll1l1111l1_opy_ = bstack11l1111_opy_ (u"ࠤࠥࠦ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩ࠰࠱࠲ࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩࠩࡽࡤࡶ࡬ࡥࡪࡴࡱࡱࢁ࠮ࠨࠢࠣᇁ")
            bstack1ll1l11ll11_opy_ = bstack1ll1l11ll11_opy_.replace(bstack11l1111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᇂ"), bstack11l1111_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦᇃ"))
            script = bstack1ll1l1111l1_opy_.format(fn_body=bstack1ll1l11ll11_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮ࠣࠦᇄ") + str(e) + bstack11l1111_opy_ (u"ࠨࠢᇅ"))