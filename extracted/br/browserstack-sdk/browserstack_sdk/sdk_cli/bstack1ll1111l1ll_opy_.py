# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1lll1llll1l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11llll111_opy_, bstack11l111l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_, bstack1ll11111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll1l1111l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1l111l11_opy_ import bstack111l1ll111_opy_, bstack11l1l111l_opy_, bstack1ll11lll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll11lll11l_opy_(bstack1lll1l1111l_opy_):
    bstack1l111ll1l1l_opy_ = bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᐠ")
    bstack1l1l11l1111_opy_ = bstack11lllll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᐡ")
    bstack1l111l1l111_opy_ = bstack11lllll_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᐢ")
    bstack1l111ll11ll_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᐣ")
    bstack1l111ll1ll1_opy_ = bstack11lllll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᐤ")
    bstack1l11l1ll111_opy_ = bstack11lllll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᐥ")
    bstack1l111l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᐦ")
    bstack1l111l1llll_opy_ = bstack11lllll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᐧ")
    def __init__(self):
        super().__init__(bstack1llll111111_opy_=self.bstack1l111ll1l1l_opy_, frameworks=[bstack1lll11lllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.BEFORE_EACH, bstack1ll11l1l11l_opy_.POST), self.bstack1l111l1l11l_opy_)
        if bstack11l111l111_opy_():
            TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1lll1111l_opy_)
        else:
            TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.PRE), self.bstack1l1lll1111l_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1l1l1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l111l11ll1_opy_ = self.bstack1l111l1ll1l_opy_(instance.context)
        if not bstack1l111l11ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᐨ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠤࠥᐩ"))
            return
        f.bstack1lll1ll1lll_opy_(instance, bstack1ll11lll11l_opy_.bstack1l1l11l1111_opy_, bstack1l111l11ll1_opy_)
    def bstack1l111l1ll1l_opy_(self, context: bstack1lll1llll1l_opy_, bstack1l111ll1lll_opy_= True):
        if bstack1l111ll1lll_opy_:
            bstack1l111l11ll1_opy_ = self.bstack1lll1llll11_opy_(context, reverse=True)
        else:
            bstack1l111l11ll1_opy_ = self.bstack1lll1ll1l11_opy_(context, reverse=True)
        return [f for f in bstack1l111l11ll1_opy_ if f[1].state != bstack1lll1l1ll1l_opy_.QUIT]
    def bstack1l1lll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1l11l_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐪ") + str(kwargs) + bstack11lllll_opy_ (u"ࠦࠧᐫ"))
            return
        bstack1l111l11ll1_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11lll11l_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l111l11ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐬ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᐭ"))
            return
        if len(bstack1l111l11ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll11111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᐮ"))
        bstack1l111l1l1ll_opy_, bstack1l11l11l1ll_opy_ = bstack1l111l11ll1_opy_[0]
        page = bstack1l111l1l1ll_opy_()
        if not page:
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐯ") + str(kwargs) + bstack11lllll_opy_ (u"ࠤࠥᐰ"))
            return
        bstack11lll11111_opy_ = getattr(args[0], bstack11lllll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᐱ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᐲ")).get(bstack11lllll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᐳ")):
            try:
                page.evaluate(bstack11lllll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᐴ"),
                            bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᐵ") + json.dumps(
                                bstack11lll11111_opy_) + bstack11lllll_opy_ (u"ࠣࡿࢀࠦᐶ"))
            except Exception as e:
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᐷ"), e)
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1l11l_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐸ") + str(kwargs) + bstack11lllll_opy_ (u"ࠦࠧᐹ"))
            return
        bstack1l111l11ll1_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11lll11l_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l111l11ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐺ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᐻ"))
            return
        if len(bstack1l111l11ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll11111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᐼ"))
        bstack1l111l1l1ll_opy_, bstack1l11l11l1ll_opy_ = bstack1l111l11ll1_opy_[0]
        page = bstack1l111l1l1ll_opy_()
        if not page:
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐽ") + str(kwargs) + bstack11lllll_opy_ (u"ࠤࠥᐾ"))
            return
        status = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, None)
        if not status:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᐿ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠦࠧᑀ"))
            return
        bstack1l111ll1l11_opy_ = {bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᑁ"): status.lower()}
        bstack1l111ll111l_opy_ = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l111ll1111_opy_, None)
        if status.lower() == bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑂ") and bstack1l111ll111l_opy_ is not None:
            bstack1l111ll1l11_opy_[bstack11lllll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᑃ")] = bstack1l111ll111l_opy_[0][bstack11lllll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑄ")][0] if isinstance(bstack1l111ll111l_opy_, list) else str(bstack1l111ll111l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᑅ")).get(bstack11lllll_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᑆ")):
            try:
                page.evaluate(
                        bstack11lllll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᑇ"),
                        bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࠪᑈ")
                        + json.dumps(bstack1l111ll1l11_opy_)
                        + bstack11lllll_opy_ (u"ࠨࡽࠣᑉ")
                    )
            except Exception as e:
                self.logger.debug(bstack11lllll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢᑊ"), e)
    def bstack1l11ll11111_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        f: TestFramework,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1l11l_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if not bstack1l11llll111_opy_:
            self.logger.debug(
                bstack1llll11111l_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᑋ"))
            return
        bstack1l111l11ll1_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11lll11l_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l111l11ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑌ") + str(kwargs) + bstack11lllll_opy_ (u"ࠥࠦᑍ"))
            return
        if len(bstack1l111l11ll1_opy_) > 1:
            self.logger.debug(
                bstack1llll11111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᑎ"))
        bstack1l111l1l1ll_opy_, bstack1l11l11l1ll_opy_ = bstack1l111l11ll1_opy_[0]
        page = bstack1l111l1l1ll_opy_()
        if not page:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑏ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᑐ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11lllll_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧᑑ") + str(timestamp)
        try:
            page.evaluate(
                bstack11lllll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᑒ"),
                bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᑓ").format(
                    json.dumps(
                        {
                            bstack11lllll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᑔ"): bstack11lllll_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨᑕ"),
                            bstack11lllll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᑖ"): {
                                bstack11lllll_opy_ (u"ࠨࡴࡺࡲࡨࠦᑗ"): bstack11lllll_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦᑘ"),
                                bstack11lllll_opy_ (u"ࠣࡦࡤࡸࡦࠨᑙ"): data,
                                bstack11lllll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣᑚ"): bstack11lllll_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤᑛ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡰ࠳࠴ࡽࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡿࢂࠨᑜ"), e)
    def bstack1l11ll111ll_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        f: TestFramework,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1l11l_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll11lll11l_opy_.bstack1l11l1ll111_opy_, False):
            return
        self.bstack1l1ll1l11ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᑝ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1ll111ll1_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        req.test_framework_state = bstack1lll1l11lll_opy_[0].name
        req.test_hook_state = bstack1lll1l11lll_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        for bstack1l111ll11l1_opy_ in bstack1lll1lll11l_opy_.bstack1ll1llll11l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11lllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᑞ")
                if bstack1l11llll111_opy_
                else bstack11lllll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨᑟ")
            )
            session.ref = bstack1l111ll11l1_opy_.ref()
            session.hub_url = bstack1lll1lll11l_opy_.bstack1lll1l1l111_opy_(bstack1l111ll11l1_opy_, bstack1lll1lll11l_opy_.bstack1l111lll111_opy_, bstack11lllll_opy_ (u"ࠣࠤᑠ"))
            session.framework_name = bstack1l111ll11l1_opy_.framework_name
            session.framework_version = bstack1l111ll11l1_opy_.framework_version
            session.framework_session_id = bstack1lll1lll11l_opy_.bstack1lll1l1l111_opy_(bstack1l111ll11l1_opy_, bstack1lll1lll11l_opy_.bstack1l111llll11_opy_, bstack11lllll_opy_ (u"ࠤࠥᑡ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll11l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l111l11ll1_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11lll11l_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l111l11ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑢ") + str(kwargs) + bstack11lllll_opy_ (u"ࠦࠧᑣ"))
            return
        if len(bstack1l111l11ll1_opy_) > 1:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᑤ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᑥ"))
        bstack1l111l1l1ll_opy_, bstack1l11l11l1ll_opy_ = bstack1l111l11ll1_opy_[0]
        page = bstack1l111l1l1ll_opy_()
        if not page:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᑦ") + str(kwargs) + bstack11lllll_opy_ (u"ࠣࠤᑧ"))
            return
        return page
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l111l1lll1_opy_ = {}
        for bstack1l111ll11l1_opy_ in bstack1lll1lll11l_opy_.bstack1ll1llll11l_opy_.values():
            caps = bstack1lll1lll11l_opy_.bstack1lll1l1l111_opy_(bstack1l111ll11l1_opy_, bstack1lll1lll11l_opy_.bstack1l11l1111ll_opy_, bstack11lllll_opy_ (u"ࠤࠥᑨ"))
        bstack1l111l1lll1_opy_[bstack11lllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣᑩ")] = caps.get(bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧᑪ"), bstack11lllll_opy_ (u"ࠧࠨᑫ"))
        bstack1l111l1lll1_opy_[bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᑬ")] = caps.get(bstack11lllll_opy_ (u"ࠢࡰࡵࠥᑭ"), bstack11lllll_opy_ (u"ࠣࠤᑮ"))
        bstack1l111l1lll1_opy_[bstack11lllll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᑯ")] = caps.get(bstack11lllll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᑰ"), bstack11lllll_opy_ (u"ࠦࠧᑱ"))
        bstack1l111l1lll1_opy_[bstack11lllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨᑲ")] = caps.get(bstack11lllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᑳ"), bstack11lllll_opy_ (u"ࠢࠣᑴ"))
        return bstack1l111l1lll1_opy_
    def bstack1l1ll1l1l11_opy_(self, page: object, bstack1l1lll1ll11_opy_, args={}):
        try:
            bstack1l111l11lll_opy_ = bstack11lllll_opy_ (u"ࠣࠤࠥࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨ࠯࠰࠱ࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴ࠰ࡳࡹࡸ࡮ࠨࡳࡧࡶࡳࡱࡼࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡾࡪࡳࡥࡢࡰࡦࡼࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯ࠨࡼࡣࡵ࡫ࡤࡰࡳࡰࡰࢀ࠭ࠧࠨࠢᑵ")
            bstack1l1lll1ll11_opy_ = bstack1l1lll1ll11_opy_.replace(bstack11lllll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᑶ"), bstack11lllll_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵࠥᑷ"))
            script = bstack1l111l11lll_opy_.format(fn_body=bstack1l1lll1ll11_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡦ࠷࠱ࡺࡡࡶࡧࡷ࡯ࡰࡵࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡊࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴ࠭ࠢࠥᑸ") + str(e) + bstack11lllll_opy_ (u"ࠧࠨᑹ"))