# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll11lll1l_opy_,
    bstack1lll1lll11l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1111ll1_opy_, bstack1l1l1l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_, bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l1l1l1111l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack111lllll1_opy_ import bstack1111l11l_opy_, bstack1lllll1l1_opy_, bstack11111l11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1l1lllll_opy_(bstack1l1l1l1111l_opy_):
    bstack1l111l11lll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦᐐ")
    bstack1l1l11l111l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᐑ")
    bstack1l111ll11l1_opy_ = bstack11l1ll1_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᐒ")
    bstack1l111ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᐓ")
    bstack1l111lll111_opy_ = bstack11l1ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨᐔ")
    bstack1l1l1111l11_opy_ = bstack11l1ll1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᐕ")
    bstack1l111l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᐖ")
    bstack1l111ll11ll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥᐗ")
    def __init__(self):
        super().__init__(bstack1l1l1l11l11_opy_=self.bstack1l111l11lll_opy_, frameworks=[bstack1ll1ll1lll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.BEFORE_EACH, bstack1ll1111llll_opy_.POST), self.bstack1l111ll1ll1_opy_)
        if bstack1l1l1l1l1l_opy_():
            TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1ll11ll11_opy_)
        else:
            TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1llll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l111l1l111_opy_ = self.bstack1l111l1lll1_opy_(instance.context)
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᐘ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠢࠣᐙ"))
            return
        f.bstack1lll1l1111l_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l111l_opy_, bstack1l111l1l111_opy_)
    def bstack1l111l1lll1_opy_(self, context: bstack1lll1lll11l_opy_, bstack1l111ll1111_opy_= True):
        if bstack1l111ll1111_opy_:
            bstack1l111l1l111_opy_ = self.bstack1l1l1l1l111_opy_(context, reverse=True)
        else:
            bstack1l111l1l111_opy_ = self.bstack1l1l1l1l1ll_opy_(context, reverse=True)
        return [f for f in bstack1l111l1l111_opy_ if f[1].state != bstack1lll111lll1_opy_.QUIT]
    def bstack1l1ll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111ll1ll1_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐚ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᐛ"))
            return
        bstack1l111l1l111_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐜ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠦࠧᐝ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll11l1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᐞ"))
        bstack1l111l1llll_opy_, bstack1l11l1l111l_opy_ = bstack1l111l1l111_opy_[0]
        page = bstack1l111l1llll_opy_()
        if not page:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐟ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠢࠣᐠ"))
            return
        bstack1ll1l111l_opy_ = getattr(args[0], bstack11l1ll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᐡ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᐢ")).get(bstack11l1ll1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᐣ")):
            try:
                page.evaluate(bstack11l1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᐤ"),
                            bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᐥ") + json.dumps(
                                bstack1ll1l111l_opy_) + bstack11l1ll1_opy_ (u"ࠨࡽࡾࠤᐦ"))
            except Exception as e:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᐧ"), e)
    def bstack1l1llll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111ll1ll1_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐨ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᐩ"))
            return
        bstack1l111l1l111_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐪ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠦࠧᐫ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll11l1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᐬ"))
        bstack1l111l1llll_opy_, bstack1l11l1l111l_opy_ = bstack1l111l1l111_opy_[0]
        page = bstack1l111l1llll_opy_()
        if not page:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐭ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠢࠣᐮ"))
            return
        status = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, None)
        if not status:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᐯ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠤࠥᐰ"))
            return
        bstack1l111ll1lll_opy_ = {bstack11l1ll1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᐱ"): status.lower()}
        bstack1l111ll1l1l_opy_ = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l111ll111l_opy_, None)
        if status.lower() == bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐲ") and bstack1l111ll1l1l_opy_ is not None:
            bstack1l111ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᐳ")] = bstack1l111ll1l1l_opy_[0][bstack11l1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᐴ")][0] if isinstance(bstack1l111ll1l1l_opy_, list) else str(bstack1l111ll1l1l_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᐵ")).get(bstack11l1ll1_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᐶ")):
            try:
                page.evaluate(
                        bstack11l1ll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᐷ"),
                        bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨᐸ")
                        + json.dumps(bstack1l111ll1lll_opy_)
                        + bstack11l1ll1_opy_ (u"ࠦࢂࠨᐹ")
                    )
            except Exception as e:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧᐺ"), e)
    def bstack1l1l1111l1l_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        f: TestFramework,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111ll1ll1_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(
                bstack1ll1ll11l1l_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢᐻ"))
            return
        bstack1l111l1l111_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐼ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠣࠤᐽ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll11l1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᐾ"))
        bstack1l111l1llll_opy_, bstack1l11l1l111l_opy_ = bstack1l111l1l111_opy_[0]
        page = bstack1l111l1llll_opy_()
        if not page:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐿ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠦࠧᑀ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11l1ll1_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥᑁ") + str(timestamp)
        try:
            page.evaluate(
                bstack11l1ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᑂ"),
                bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᑃ").format(
                    json.dumps(
                        {
                            bstack11l1ll1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᑄ"): bstack11l1ll1_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᑅ"),
                            bstack11l1ll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᑆ"): {
                                bstack11l1ll1_opy_ (u"ࠦࡹࡿࡰࡦࠤᑇ"): bstack11l1ll1_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᑈ"),
                                bstack11l1ll1_opy_ (u"ࠨࡤࡢࡶࡤࠦᑉ"): data,
                                bstack11l1ll1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᑊ"): bstack11l1ll1_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᑋ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦᑌ"), e)
    def bstack1l11ll111l1_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        f: TestFramework,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111ll1ll1_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l1111l11_opy_, False):
            return
        self.bstack1l1lll1ll1l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑍ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llllll11_opy_)
        req.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l111llll_opy_)
        req.test_framework_state = bstack1lll1l1ll11_opy_[0].name
        req.test_hook_state = bstack1lll1l1ll11_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
        for bstack1l111l1l11l_opy_ in bstack1ll111ll1l1_opy_.bstack1lll1ll11ll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᑎ")
                if bstack1l1l1111ll1_opy_
                else bstack11l1ll1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᑏ")
            )
            session.ref = bstack1l111l1l11l_opy_.ref()
            session.hub_url = bstack1ll111ll1l1_opy_.bstack1lll1ll11l1_opy_(bstack1l111l1l11l_opy_, bstack1ll111ll1l1_opy_.bstack1l111llll11_opy_, bstack11l1ll1_opy_ (u"ࠨࠢᑐ"))
            session.framework_name = bstack1l111l1l11l_opy_.framework_name
            session.framework_version = bstack1l111l1l11l_opy_.framework_version
            session.framework_session_id = bstack1ll111ll1l1_opy_.bstack1lll1ll11l1_opy_(bstack1l111l1l11l_opy_, bstack1ll111ll1l1_opy_.bstack1l111lll1ll_opy_, bstack11l1ll1_opy_ (u"ࠢࠣᑑ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l111l1l111_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᑒ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᑓ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑔ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠦࠧᑕ"))
        bstack1l111l1llll_opy_, bstack1l11l1l111l_opy_ = bstack1l111l1l111_opy_[0]
        page = bstack1l111l1llll_opy_()
        if not page:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑖ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠨࠢᑗ"))
            return
        return page
    def bstack1l1ll1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l111l1l1l1_opy_ = {}
        for bstack1l111l1l11l_opy_ in bstack1ll111ll1l1_opy_.bstack1lll1ll11ll_opy_.values():
            caps = bstack1ll111ll1l1_opy_.bstack1lll1ll11l1_opy_(bstack1l111l1l11l_opy_, bstack1ll111ll1l1_opy_.bstack1l11l111lll_opy_, bstack11l1ll1_opy_ (u"ࠢࠣᑘ"))
        bstack1l111l1l1l1_opy_[bstack11l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨᑙ")] = caps.get(bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥᑚ"), bstack11l1ll1_opy_ (u"ࠥࠦᑛ"))
        bstack1l111l1l1l1_opy_[bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᑜ")] = caps.get(bstack11l1ll1_opy_ (u"ࠧࡵࡳࠣᑝ"), bstack11l1ll1_opy_ (u"ࠨࠢᑞ"))
        bstack1l111l1l1l1_opy_[bstack11l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᑟ")] = caps.get(bstack11l1ll1_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᑠ"), bstack11l1ll1_opy_ (u"ࠤࠥᑡ"))
        bstack1l111l1l1l1_opy_[bstack11l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦᑢ")] = caps.get(bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᑣ"), bstack11l1ll1_opy_ (u"ࠧࠨᑤ"))
        return bstack1l111l1l1l1_opy_
    def bstack1l1ll1111ll_opy_(self, page: object, bstack1l1lll11l1l_opy_, args={}):
        try:
            bstack1l111l1ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࠢࠣࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࠴࠮࠯ࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠪࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹ࠮ࡱࡷࡶ࡬࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡼࡨࡱࡣࡧࡵࡤࡺࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭࠭ࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾࠫࠥࠦࠧᑥ")
            bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_.replace(bstack11l1ll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᑦ"), bstack11l1ll1_opy_ (u"ࠣࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳࠣᑧ"))
            script = bstack1l111l1ll1l_opy_.format(fn_body=bstack1l1lll11l1l_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺ࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡈࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹ࠲ࠠࠣᑨ") + str(e) + bstack11l1ll1_opy_ (u"ࠥࠦᑩ"))