# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1ll1llll111_opy_,
    bstack1lll11l1l11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111lll111_opy_, bstack1llll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_, bstack1l1llll111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1lllll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l11l_opy_ import bstack1l11lllllll_opy_
from typing import Tuple, List, Any
from bstack_utils.session_utils import browserstack_executor_helper, bstack11lll1l11l_opy_, bstack1l111l11l1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1l11l11l_opy_(bstack1l11lllllll_opy_):
    bstack1l1111l1l11_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣᓃ")
    bstack1l11lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᓄ")
    bstack1l11111lll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᓅ")
    bstack1l11111llll_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᓆ")
    bstack1l1111l1lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥᓇ")
    bstack1l11l1111l1_opy_ = bstack11l1l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨᓈ")
    bstack1l11111ll11_opy_ = bstack11l1l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᓉ")
    bstack1l11111l1ll_opy_ = bstack11l1l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢᓊ")
    def __init__(self):
        super().__init__(bstack1l1l1111111_opy_=self.bstack1l1111l1l11_opy_, frameworks=[bstack1l1lllll1l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.BEFORE_EACH, bstack1ll11lll1ll_opy_.POST), self.bstack1l1111l1111_opy_)
        if bstack1llll1ll1_opy_():
            TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1ll11111l_opy_)
        else:
            TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE), self.bstack1l1ll11111l_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1l1ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11111l11l_opy_ = self.bstack1l1111l11ll_opy_(instance.context)
        if not bstack1l11111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᓋ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠦࠧᓌ"))
            return
        f.bstack1lll111ll11_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11lll11l1_opy_, bstack1l11111l11l_opy_)
    def bstack1l1111l11ll_opy_(self, context: bstack1lll11l1l11_opy_, bstack1l1111l111l_opy_= True):
        if bstack1l1111l111l_opy_:
            bstack1l11111l11l_opy_ = self.bstack1l1l1111lll_opy_(context, reverse=True)
        else:
            bstack1l11111l11l_opy_ = self.bstack1l1l11111l1_opy_(context, reverse=True)
        return [f for f in bstack1l11111l11l_opy_ if f[1].state != bstack1ll1lll1lll_opy_.QUIT]
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1111l1111_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᓍ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᓎ"))
            return
        bstack1l11111l11l_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l11111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓏ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᓐ"))
            return
        if len(bstack1l11111l11l_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᓑ"))
        bstack1l11111l111_opy_, bstack1l111l1ll1l_opy_ = bstack1l11111l11l_opy_[0]
        page = bstack1l11111l111_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓒ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧᓓ"))
            return
        bstack1l111l11l_opy_ = getattr(args[0], bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᓔ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᓕ")).get(bstack11l1l11_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᓖ")):
            try:
                page.evaluate(bstack11l1l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᓗ"),
                            bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᓘ") + json.dumps(
                                bstack1l111l11l_opy_) + bstack11l1l11_opy_ (u"ࠥࢁࢂࠨᓙ"))
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᓚ"), e)
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1111l1111_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᓛ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᓜ"))
            return
        bstack1l11111l11l_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l11111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓝ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᓞ"))
            return
        if len(bstack1l11111l11l_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᓟ"))
        bstack1l11111l111_opy_, bstack1l111l1ll1l_opy_ = bstack1l11111l11l_opy_[0]
        page = bstack1l11111l111_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓠ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧᓡ"))
            return
        status = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1111l11l1_opy_, None)
        if not status:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᓢ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᓣ"))
            return
        bstack1l11111l1l1_opy_ = {bstack11l1l11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᓤ"): status.lower()}
        bstack1l11111ll1l_opy_ = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111111lll_opy_, None)
        if status.lower() == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᓥ") and bstack1l11111ll1l_opy_ is not None:
            bstack1l11111l1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᓦ")] = bstack1l11111ll1l_opy_[0][bstack11l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᓧ")][0] if isinstance(bstack1l11111ll1l_opy_, list) else str(bstack1l11111ll1l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᓨ")).get(bstack11l1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᓩ")):
            try:
                page.evaluate(
                        bstack11l1l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᓪ"),
                        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬᓫ")
                        + json.dumps(bstack1l11111l1l1_opy_)
                        + bstack11l1l11_opy_ (u"ࠣࡿࠥᓬ")
                    )
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᓭ"), e)
    def bstack1l11l1l11l1_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        f: TestFramework,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1111l1111_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if not bstack1l111lll111_opy_:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᓮ"))
            return
        bstack1l11111l11l_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l11111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓯ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠧࠨᓰ"))
            return
        if len(bstack1l11111l11l_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᓱ"))
        bstack1l11111l111_opy_, bstack1l111l1ll1l_opy_ = bstack1l11111l11l_opy_[0]
        page = bstack1l11111l111_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓲ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᓳ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l1l11_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᓴ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l1l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᓵ"),
                bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᓶ").format(
                    json.dumps(
                        {
                            bstack11l1l11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᓷ"): bstack11l1l11_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᓸ"),
                            bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᓹ"): {
                                bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࠨᓺ"): bstack11l1l11_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᓻ"),
                                bstack11l1l11_opy_ (u"ࠥࡨࡦࡺࡡࠣᓼ"): data,
                                bstack11l1l11_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᓽ"): bstack11l1l11_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᓾ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣᓿ"), e)
    def bstack1l111llll1l_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        f: TestFramework,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1111l1111_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11l1111l1_opy_, False):
            return
        self.bstack1l1l1ll1111_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᔀ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1ll1l1lll_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_)
        req.test_framework_state = bstack1lll11ll111_opy_[0].name
        req.test_hook_state = bstack1lll11ll111_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
        for bstack1l1111l1l1l_opy_ in bstack1l1lllll1ll_opy_.bstack1ll1ll1ll1l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢᔁ")
                if bstack1l111lll111_opy_
                else bstack11l1l11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣᔂ")
            )
            session.ref = bstack1l1111l1l1l_opy_.ref()
            session.hub_url = bstack1l1lllll1ll_opy_.bstack1ll1lll111l_opy_(bstack1l1111l1l1l_opy_, bstack1l1lllll1ll_opy_.bstack1l111l1l11l_opy_, bstack11l1l11_opy_ (u"ࠥࠦᔃ"))
            session.framework_name = bstack1l1111l1l1l_opy_.framework_name
            session.framework_version = bstack1l1111l1l1l_opy_.framework_version
            session.framework_session_id = bstack1l1lllll1ll_opy_.bstack1ll1lll111l_opy_(bstack1l1111l1l1l_opy_, bstack1l1lllll1ll_opy_.bstack1l111l1l111_opy_, bstack11l1l11_opy_ (u"ࠦࠧᔄ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11111l11l_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l11111l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᔅ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᔆ"))
            return
        if len(bstack1l11111l11l_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔇ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᔈ"))
        bstack1l11111l111_opy_, bstack1l111l1ll1l_opy_ = bstack1l11111l11l_opy_[0]
        page = bstack1l11111l111_opy_()
        if not page:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔉ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦᔊ"))
            return
        return page
    def bstack1l1ll1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1111l1ll1_opy_ = {}
        for bstack1l1111l1l1l_opy_ in bstack1l1lllll1ll_opy_.bstack1ll1ll1ll1l_opy_.values():
            caps = bstack1l1lllll1ll_opy_.bstack1ll1lll111l_opy_(bstack1l1111l1l1l_opy_, bstack1l1lllll1ll_opy_.bstack1l1111ll11l_opy_, bstack11l1l11_opy_ (u"ࠦࠧᔋ"))
        bstack1l1111l1ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥᔌ")] = caps.get(bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢᔍ"), bstack11l1l11_opy_ (u"ࠢࠣᔎ"))
        bstack1l1111l1ll1_opy_[bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᔏ")] = caps.get(bstack11l1l11_opy_ (u"ࠤࡲࡷࠧᔐ"), bstack11l1l11_opy_ (u"ࠥࠦᔑ"))
        bstack1l1111l1ll1_opy_[bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᔒ")] = caps.get(bstack11l1l11_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᔓ"), bstack11l1l11_opy_ (u"ࠨࠢᔔ"))
        bstack1l1111l1ll1_opy_[bstack11l1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣᔕ")] = caps.get(bstack11l1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥᔖ"), bstack11l1l11_opy_ (u"ࠤࠥᔗ"))
        return bstack1l1111l1ll1_opy_
    def bstack1l1l1ll1l11_opy_(self, page: object, bstack1l1ll11l11l_opy_, args={}):
        try:
            bstack1l111111ll1_opy_ = bstack11l1l11_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠲ࡵࡻࡳࡩࠪࡵࡩࡸࡵ࡬ࡷࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤᔘ")
            bstack1l1ll11l11l_opy_ = bstack1l1ll11l11l_opy_.replace(bstack11l1l11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᔙ"), bstack11l1l11_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧᔚ"))
            script = bstack1l111111ll1_opy_.format(fn_body=bstack1l1ll11l11l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧᔛ") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣᔜ"))