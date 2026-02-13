# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1l1ll1ll_opy_,
    bstack1ll1ll1llll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111lllll1_opy_, bstack11lll1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_, bstack1ll11l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l11lll11ll_opy_ import bstack1l11lll1l1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1ll111l1l1_opy_ import bstack1lll1l1l1l_opy_, bstack1ll1l1l1_opy_, bstack1l11lll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1l1ll1ll111_opy_(bstack1l11lll1l1l_opy_):
    bstack1l11111111l_opy_ = bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᒹ")
    bstack1l11l1l11ll_opy_ = bstack11l11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᒺ")
    bstack11lllllll11_opy_ = bstack11l11_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᒻ")
    bstack11llllll1l1_opy_ = bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᒼ")
    bstack11llllll1ll_opy_ = bstack11l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᒽ")
    bstack1l11l1lllll_opy_ = bstack11l11_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᒾ")
    bstack1l1111111l1_opy_ = bstack11l11_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᒿ")
    bstack11llllll11l_opy_ = bstack11l11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᓀ")
    def __init__(self):
        super().__init__(bstack1l11lll11l1_opy_=self.bstack1l11111111l_opy_, frameworks=[bstack1l1llllllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.BEFORE_EACH, bstack1l1lllll1ll_opy_.POST), self.bstack11lllllll1l_opy_)
        if bstack11lll1111l_opy_():
            TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l11ll111_opy_)
        else:
            TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE), self.bstack1l1l11ll111_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l1llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lllllll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l111111l11_opy_ = self.bstack11llllllll1_opy_(instance.context)
        if not bstack1l111111l11_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᓁ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠣࠤᓂ"))
            return
        f.bstack1ll1lll111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1l11ll_opy_, bstack1l111111l11_opy_)
    def bstack11llllllll1_opy_(self, context: bstack1ll1ll1llll_opy_, bstack1l11111l111_opy_= True):
        if bstack1l11111l111_opy_:
            bstack1l111111l11_opy_ = self.bstack1l11lll1111_opy_(context, reverse=True)
        else:
            bstack1l111111l11_opy_ = self.bstack1l11lll1l11_opy_(context, reverse=True)
        return [f for f in bstack1l111111l11_opy_ if f[1].state != bstack1ll1lllllll_opy_.QUIT]
    def bstack1l1l11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllllll1l_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if not bstack1l111lllll1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓃ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᓄ"))
            return
        bstack1l111111l11_opy_ = f.bstack1lll111111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111111l11_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓅ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᓆ"))
            return
        if len(bstack1l111111l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1lllll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓇ"))
        bstack1l111111lll_opy_, bstack1l1111llll1_opy_ = bstack1l111111l11_opy_[0]
        page = bstack1l111111lll_opy_()
        if not page:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓈ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤᓉ"))
            return
        bstack11l111l11l_opy_ = getattr(args[0], bstack11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᓊ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᓋ")).get(bstack11l11_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᓌ")):
            try:
                page.evaluate(bstack11l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᓍ"),
                            bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᓎ") + json.dumps(
                                bstack11l111l11l_opy_) + bstack11l11_opy_ (u"ࠢࡾࡿࠥᓏ"))
            except Exception as e:
                self.logger.debug(bstack11l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᓐ"), e)
    def bstack1l1l1llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllllll1l_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if not bstack1l111lllll1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓑ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᓒ"))
            return
        bstack1l111111l11_opy_ = f.bstack1lll111111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111111l11_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓓ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᓔ"))
            return
        if len(bstack1l111111l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1lllll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓕ"))
        bstack1l111111lll_opy_, bstack1l1111llll1_opy_ = bstack1l111111l11_opy_[0]
        page = bstack1l111111lll_opy_()
        if not page:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓖ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤᓗ"))
            return
        status = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l111111l1l_opy_, None)
        if not status:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᓘ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠥࠦᓙ"))
            return
        bstack11lllll1lll_opy_ = {bstack11l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᓚ"): status.lower()}
        bstack11lllllllll_opy_ = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l111111111_opy_, None)
        if status.lower() == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓛ") and bstack11lllllllll_opy_ is not None:
            bstack11lllll1lll_opy_[bstack11l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᓜ")] = bstack11lllllllll_opy_[0][bstack11l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᓝ")][0] if isinstance(bstack11lllllllll_opy_, list) else str(bstack11lllllllll_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᓞ")).get(bstack11l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᓟ")):
            try:
                page.evaluate(
                        bstack11l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᓠ"),
                        bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩᓡ")
                        + json.dumps(bstack11lllll1lll_opy_)
                        + bstack11l11_opy_ (u"ࠧࢃࠢᓢ")
                    )
            except Exception as e:
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨᓣ"), e)
    def bstack1l11l1ll1l1_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        f: TestFramework,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllllll1l_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if not bstack1l111lllll1_opy_:
            self.logger.debug(
                bstack1ll1lllll11_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓤ"))
            return
        bstack1l111111l11_opy_ = f.bstack1lll111111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111111l11_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓥ") + str(kwargs) + bstack11l11_opy_ (u"ࠤࠥᓦ"))
            return
        if len(bstack1l111111l11_opy_) > 1:
            self.logger.debug(
                bstack1ll1lllll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᓧ"))
        bstack1l111111lll_opy_, bstack1l1111llll1_opy_ = bstack1l111111l11_opy_[0]
        page = bstack1l111111lll_opy_()
        if not page:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓨ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᓩ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l11_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᓪ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᓫ"),
                bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᓬ").format(
                    json.dumps(
                        {
                            bstack11l11_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᓭ"): bstack11l11_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᓮ"),
                            bstack11l11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᓯ"): {
                                bstack11l11_opy_ (u"ࠧࡺࡹࡱࡧࠥᓰ"): bstack11l11_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᓱ"),
                                bstack11l11_opy_ (u"ࠢࡥࡣࡷࡥࠧᓲ"): data,
                                bstack11l11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᓳ"): bstack11l11_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᓴ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧᓵ"), e)
    def bstack1l11l111l1l_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        f: TestFramework,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllllll1l_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if f.bstack1lll111111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1lllll_opy_, False):
            return
        self.bstack1l1l11l1111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᓶ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l1l11l11_opy_)
        req.test_framework_version = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l11l111l11_opy_)
        req.test_framework_state = bstack1ll1l1lll1l_opy_[0].name
        req.test_hook_state = bstack1ll1l1lll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        for bstack11llllll111_opy_ in bstack1l1lllll11l_opy_.bstack1lll111l1l1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᓷ")
                if bstack1l111lllll1_opy_
                else bstack11l11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᓸ")
            )
            session.ref = bstack11llllll111_opy_.ref()
            session.hub_url = bstack1l1lllll11l_opy_.bstack1lll111111l_opy_(bstack11llllll111_opy_, bstack1l1lllll11l_opy_.bstack1l11111lll1_opy_, bstack11l11_opy_ (u"ࠢࠣᓹ"))
            session.framework_name = bstack11llllll111_opy_.framework_name
            session.framework_version = bstack11llllll111_opy_.framework_version
            session.framework_session_id = bstack1l1lllll11l_opy_.bstack1lll111111l_opy_(bstack11llllll111_opy_, bstack1l1lllll11l_opy_.bstack1l1111ll1ll_opy_, bstack11l11_opy_ (u"ࠣࠤᓺ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l11l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l111111l11_opy_ = f.bstack1lll111111l_opy_(instance, bstack1l1ll1ll111_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111111l11_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓻ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᓼ"))
            return
        if len(bstack1l111111l11_opy_) > 1:
            self.logger.debug(bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᓽ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᓾ"))
        bstack1l111111lll_opy_, bstack1l1111llll1_opy_ = bstack1l111111l11_opy_[0]
        page = bstack1l111111lll_opy_()
        if not page:
            self.logger.debug(bstack11l11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᓿ") + str(kwargs) + bstack11l11_opy_ (u"ࠢࠣᔀ"))
            return
        return page
    def bstack1l1l1ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l111111ll1_opy_ = {}
        for bstack11llllll111_opy_ in bstack1l1lllll11l_opy_.bstack1lll111l1l1_opy_.values():
            caps = bstack1l1lllll11l_opy_.bstack1lll111111l_opy_(bstack11llllll111_opy_, bstack1l1lllll11l_opy_.bstack1l1111l1lll_opy_, bstack11l11_opy_ (u"ࠣࠤᔁ"))
        bstack1l111111ll1_opy_[bstack11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᔂ")] = caps.get(bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᔃ"), bstack11l11_opy_ (u"ࠦࠧᔄ"))
        bstack1l111111ll1_opy_[bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᔅ")] = caps.get(bstack11l11_opy_ (u"ࠨ࡯ࡴࠤᔆ"), bstack11l11_opy_ (u"ࠢࠣᔇ"))
        bstack1l111111ll1_opy_[bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᔈ")] = caps.get(bstack11l11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᔉ"), bstack11l11_opy_ (u"ࠥࠦᔊ"))
        bstack1l111111ll1_opy_[bstack11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᔋ")] = caps.get(bstack11l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᔌ"), bstack11l11_opy_ (u"ࠨࠢᔍ"))
        return bstack1l111111ll1_opy_
    def bstack1l1l1ll11l1_opy_(self, page: object, bstack1l1l1l1l1l1_opy_, args={}):
        try:
            bstack1l1111111ll_opy_ = bstack11l11_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᔎ")
            bstack1l1l1l1l1l1_opy_ = bstack1l1l1l1l1l1_opy_.replace(bstack11l11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᔏ"), bstack11l11_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᔐ"))
            script = bstack1l1111111ll_opy_.format(fn_body=bstack1l1l1l1l1l1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᔑ") + str(e) + bstack11l11_opy_ (u"ࠦࠧᔒ"))