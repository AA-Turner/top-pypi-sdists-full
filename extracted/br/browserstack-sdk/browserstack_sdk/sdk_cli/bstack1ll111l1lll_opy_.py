# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1lll1111_opy_,
    bstack1ll1lll11l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11l1111ll_opy_, bstack111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l111111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1ll11l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l1ll_opy_ import bstack1l1l1111111_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack1l11l1ll11_opy_, bstack111l1l1lll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1l1ll1ll_opy_(bstack1l1l1111111_opy_):
    bstack1l111111ll1_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᓀ")
    bstack1l11l11l111_opy_ = bstack11ll111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᓁ")
    bstack1l11l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᓂ")
    bstack1l11111ll11_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᓃ")
    bstack1l1111l1l11_opy_ = bstack11ll111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᓄ")
    bstack1l11l1ll11l_opy_ = bstack11ll111_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᓅ")
    bstack1l11111llll_opy_ = bstack11ll111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᓆ")
    bstack1l1111l11l1_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᓇ")
    def __init__(self):
        super().__init__(bstack1l1l11111l1_opy_=self.bstack1l111111ll1_opy_, frameworks=[bstack1ll1111ll11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1l1llll1l1l_opy_.POST), self.bstack1l111111l1l_opy_)
        if bstack111l1lll_opy_():
            TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll1111ll_opy_)
        else:
            TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE), self.bstack1l1ll1111ll_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1111l11ll_opy_ = self.bstack1l11111l11l_opy_(instance.context)
        if not bstack1l1111l11ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᓈ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠣࠤᓉ"))
            return
        f.bstack1lll11l1111_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l11l111_opy_, bstack1l1111l11ll_opy_)
    def bstack1l11111l11l_opy_(self, context: bstack1ll1lll11l1_opy_, bstack1l11111l1ll_opy_= True):
        if bstack1l11111l1ll_opy_:
            bstack1l1111l11ll_opy_ = self.bstack1l1l111l11l_opy_(context, reverse=True)
        else:
            bstack1l1111l11ll_opy_ = self.bstack1l1l111l111_opy_(context, reverse=True)
        return [f for f in bstack1l1111l11ll_opy_ if f[1].state != bstack1ll1ll1l1l1_opy_.QUIT]
    def bstack1l1ll1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111111l1l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if not bstack1l11l1111ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓊ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᓋ"))
            return
        bstack1l1111l11ll_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l1111l11ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓌ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᓍ"))
            return
        if len(bstack1l1111l11ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11111l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓎ"))
        bstack1l11111ll1l_opy_, bstack1l111ll1l1l_opy_ = bstack1l1111l11ll_opy_[0]
        page = bstack1l11111ll1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓏ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤᓐ"))
            return
        bstack11ll11ll11_opy_ = getattr(args[0], bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᓑ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᓒ")).get(bstack11ll111_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᓓ")):
            try:
                page.evaluate(bstack11ll111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᓔ"),
                            bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᓕ") + json.dumps(
                                bstack11ll11ll11_opy_) + bstack11ll111_opy_ (u"ࠢࡾࡿࠥᓖ"))
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᓗ"), e)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111111l1l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if not bstack1l11l1111ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓘ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᓙ"))
            return
        bstack1l1111l11ll_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l1111l11ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓚ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᓛ"))
            return
        if len(bstack1l1111l11ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11111l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓜ"))
        bstack1l11111ll1l_opy_, bstack1l111ll1l1l_opy_ = bstack1l1111l11ll_opy_[0]
        page = bstack1l11111ll1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓝ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤᓞ"))
            return
        status = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11111l1l1_opy_, None)
        if not status:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᓟ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠥࠦᓠ"))
            return
        bstack1l1111l111l_opy_ = {bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᓡ"): status.lower()}
        bstack1l111111lll_opy_ = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1111l1l1l_opy_, None)
        if status.lower() == bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓢ") and bstack1l111111lll_opy_ is not None:
            bstack1l1111l111l_opy_[bstack11ll111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᓣ")] = bstack1l111111lll_opy_[0][bstack11ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᓤ")][0] if isinstance(bstack1l111111lll_opy_, list) else str(bstack1l111111lll_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᓥ")).get(bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᓦ")):
            try:
                page.evaluate(
                        bstack11ll111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᓧ"),
                        bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩᓨ")
                        + json.dumps(bstack1l1111l111l_opy_)
                        + bstack11ll111_opy_ (u"ࠧࢃࠢᓩ")
                    )
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨᓪ"), e)
    def bstack1l11l1111l1_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        f: TestFramework,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111111l1l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if not bstack1l11l1111ll_opy_:
            self.logger.debug(
                bstack1lll11111l1_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓫ"))
            return
        bstack1l1111l11ll_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l1111l11ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓬ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥᓭ"))
            return
        if len(bstack1l1111l11ll_opy_) > 1:
            self.logger.debug(
                bstack1lll11111l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᓮ"))
        bstack1l11111ll1l_opy_, bstack1l111ll1l1l_opy_ = bstack1l1111l11ll_opy_[0]
        page = bstack1l11111ll1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓯ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᓰ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11ll111_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᓱ") + str(timestamp)
        try:
            page.evaluate(
                bstack11ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᓲ"),
                bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᓳ").format(
                    json.dumps(
                        {
                            bstack11ll111_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᓴ"): bstack11ll111_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᓵ"),
                            bstack11ll111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᓶ"): {
                                bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥᓷ"): bstack11ll111_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᓸ"),
                                bstack11ll111_opy_ (u"ࠢࡥࡣࡷࡥࠧᓹ"): data,
                                bstack11ll111_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᓺ"): bstack11ll111_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᓻ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧᓼ"), e)
    def bstack1l11l11l1ll_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        f: TestFramework,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111111l1l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l1ll11l_opy_, False):
            return
        self.bstack1l1l11llll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᓽ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_)
        req.test_framework_state = bstack1ll1ll1llll_opy_[0].name
        req.test_hook_state = bstack1ll1ll1llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
        for bstack1l11111l111_opy_ in bstack1ll11l1111l_opy_.bstack1ll1lll1ll1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᓾ")
                if bstack1l11l1111ll_opy_
                else bstack11ll111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᓿ")
            )
            session.ref = bstack1l11111l111_opy_.ref()
            session.hub_url = bstack1ll11l1111l_opy_.bstack1ll1lllll11_opy_(bstack1l11111l111_opy_, bstack1ll11l1111l_opy_.bstack1l111l11ll1_opy_, bstack11ll111_opy_ (u"ࠢࠣᔀ"))
            session.framework_name = bstack1l11111l111_opy_.framework_name
            session.framework_version = bstack1l11111l111_opy_.framework_version
            session.framework_session_id = bstack1ll11l1111l_opy_.bstack1ll1lllll11_opy_(bstack1l11111l111_opy_, bstack1ll11l1111l_opy_.bstack1l111l111l1_opy_, bstack11ll111_opy_ (u"ࠣࠤᔁ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1111l11ll_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll1l1ll1ll_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l1111l11ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔂ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᔃ"))
            return
        if len(bstack1l1111l11ll_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᔄ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᔅ"))
        bstack1l11111ll1l_opy_, bstack1l111ll1l1l_opy_ = bstack1l1111l11ll_opy_[0]
        page = bstack1l11111ll1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᔆ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣᔇ"))
            return
        return page
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l11111lll1_opy_ = {}
        for bstack1l11111l111_opy_ in bstack1ll11l1111l_opy_.bstack1ll1lll1ll1_opy_.values():
            caps = bstack1ll11l1111l_opy_.bstack1ll1lllll11_opy_(bstack1l11111l111_opy_, bstack1ll11l1111l_opy_.bstack1l111l11111_opy_, bstack11ll111_opy_ (u"ࠣࠤᔈ"))
        bstack1l11111lll1_opy_[bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᔉ")] = caps.get(bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᔊ"), bstack11ll111_opy_ (u"ࠦࠧᔋ"))
        bstack1l11111lll1_opy_[bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᔌ")] = caps.get(bstack11ll111_opy_ (u"ࠨ࡯ࡴࠤᔍ"), bstack11ll111_opy_ (u"ࠢࠣᔎ"))
        bstack1l11111lll1_opy_[bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᔏ")] = caps.get(bstack11ll111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᔐ"), bstack11ll111_opy_ (u"ࠥࠦᔑ"))
        bstack1l11111lll1_opy_[bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᔒ")] = caps.get(bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᔓ"), bstack11ll111_opy_ (u"ࠨࠢᔔ"))
        return bstack1l11111lll1_opy_
    def bstack1l1ll1ll111_opy_(self, page: object, bstack1l1l1lll1l1_opy_, args={}):
        try:
            bstack1l1111l1111_opy_ = bstack11ll111_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᔕ")
            bstack1l1l1lll1l1_opy_ = bstack1l1l1lll1l1_opy_.replace(bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᔖ"), bstack11ll111_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᔗ"))
            script = bstack1l1111l1111_opy_.format(fn_body=bstack1l1l1lll1l1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᔘ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧᔙ"))