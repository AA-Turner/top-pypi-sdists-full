# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llll1ll11l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll11llll_opy_, bstack11l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_, bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1ll1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1l1llll1lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1lllllll_opy_ import bstack1llll1111l_opy_, bstack1l11ll11ll_opy_, bstack1lllllll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1lll111l_opy_(bstack1l1llll1lll_opy_):
    bstack1l1l111ll11_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨገ")
    bstack1l1llll111l_opy_ = bstack111l111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢጉ")
    bstack1l1l111l1ll_opy_ = bstack111l111_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጊ")
    bstack1l1l1111l1l_opy_ = bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጋ")
    bstack1l11lllllll_opy_ = bstack111l111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣጌ")
    bstack1l1l1llll11_opy_ = bstack111l111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦግ")
    bstack1l11lllll1l_opy_ = bstack111l111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤጎ")
    bstack1l1l1111lll_opy_ = bstack111l111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧጏ")
    def __init__(self):
        super().__init__(bstack1ll1111111l_opy_=self.bstack1l1l111ll11_opy_, frameworks=[bstack1lll1l11l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.BEFORE_EACH, bstack1lll111llll_opy_.POST), self.bstack1l11llllll1_opy_)
        if bstack11l1l11l_opy_():
            TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll1l111l1l_opy_)
        else:
            TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll111lll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1111ll1_opy_ = self.bstack1l1l1111l11_opy_(instance.context)
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጐ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠤࠥ጑"))
            return
        f.bstack1111111111_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1llll111l_opy_, bstack1l1l1111ll1_opy_)
    def bstack1l1l1111l11_opy_(self, context: bstack1llll1ll11l_opy_, bstack1l1l11111l1_opy_= True):
        if bstack1l1l11111l1_opy_:
            bstack1l1l1111ll1_opy_ = self.bstack1l1lllllll1_opy_(context, reverse=True)
        else:
            bstack1l1l1111ll1_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        return [f for f in bstack1l1l1111ll1_opy_ if f[1].state != bstack1lllllll11l_opy_.QUIT]
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if not bstack1l1ll11llll_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጒ") + str(kwargs) + bstack111l111_opy_ (u"ࠦࠧጓ"))
            return
        bstack1l1l1111ll1_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጔ") + str(kwargs) + bstack111l111_opy_ (u"ࠨࠢጕ"))
            return
        if len(bstack1l1l1111ll1_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤ጖"))
        bstack1l1l11111ll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l1111ll1_opy_[0]
        page = bstack1l1l11111ll_opy_()
        if not page:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ጗") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥጘ"))
            return
        bstack11llll1lll_opy_ = getattr(args[0], bstack111l111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥጙ"), None)
        try:
            page.evaluate(bstack111l111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧጚ"),
                        bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩጛ") + json.dumps(
                            bstack11llll1lll_opy_) + bstack111l111_opy_ (u"ࠨࡽࡾࠤጜ"))
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧጝ"), e)
    def bstack1ll111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if not bstack1l1ll11llll_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጞ") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥጟ"))
            return
        bstack1l1l1111ll1_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጠ") + str(kwargs) + bstack111l111_opy_ (u"ࠦࠧጡ"))
            return
        if len(bstack1l1l1111ll1_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢጢ"))
        bstack1l1l11111ll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l1111ll1_opy_[0]
        page = bstack1l1l11111ll_opy_()
        if not page:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጣ") + str(kwargs) + bstack111l111_opy_ (u"ࠢࠣጤ"))
            return
        status = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1111111_opy_, None)
        if not status:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጥ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠤࠥጦ"))
            return
        bstack1l11llll1ll_opy_ = {bstack111l111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥጧ"): status.lower()}
        bstack1l1l111l1l1_opy_ = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1l11lllll11_opy_, None)
        if status.lower() == bstack111l111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጨ") and bstack1l1l111l1l1_opy_ is not None:
            bstack1l11llll1ll_opy_[bstack111l111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬጩ")] = bstack1l1l111l1l1_opy_[0][bstack111l111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩጪ")][0] if isinstance(bstack1l1l111l1l1_opy_, list) else str(bstack1l1l111l1l1_opy_)
        try:
              page.evaluate(
                    bstack111l111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣጫ"),
                    bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ጬ")
                    + json.dumps(bstack1l11llll1ll_opy_)
                    + bstack111l111_opy_ (u"ࠤࢀࠦጭ")
                )
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥጮ"), e)
    def bstack1l1lll1l1ll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if not bstack1l1ll11llll_opy_:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧጯ"))
            return
        bstack1l1l1111ll1_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጰ") + str(kwargs) + bstack111l111_opy_ (u"ࠨࠢጱ"))
            return
        if len(bstack1l1l1111ll1_opy_) > 1:
            self.logger.debug(
                bstack1lll11l11ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤጲ"))
        bstack1l1l11111ll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l1111ll1_opy_[0]
        page = bstack1l1l11111ll_opy_()
        if not page:
            self.logger.debug(bstack111l111_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጳ") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥጴ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack111l111_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣጵ") + str(timestamp)
        try:
            page.evaluate(
                bstack111l111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧጶ"),
                bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪጷ").format(
                    json.dumps(
                        {
                            bstack111l111_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጸ"): bstack111l111_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤጹ"),
                            bstack111l111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጺ"): {
                                bstack111l111_opy_ (u"ࠤࡷࡽࡵ࡫ࠢጻ"): bstack111l111_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢጼ"),
                                bstack111l111_opy_ (u"ࠦࡩࡧࡴࡢࠤጽ"): data,
                                bstack111l111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦጾ"): bstack111l111_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧጿ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤፀ"), e)
    def bstack1l1ll111111_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11llllll1_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if f.bstack1111111l1l_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1l1llll11_opy_, False):
            return
        self.bstack1ll111l1l11_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
        req.test_framework_name = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_)
        req.test_framework_state = bstack1llllll111l_opy_[0].name
        req.test_hook_state = bstack1llllll111l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
        for bstack1l1l111l111_opy_ in bstack1ll1llll11l_opy_.bstack1lllll1llll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack111l111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢፁ")
                if bstack1l1ll11llll_opy_
                else bstack111l111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣፂ")
            )
            session.ref = bstack1l1l111l111_opy_.ref()
            session.hub_url = bstack1ll1llll11l_opy_.bstack1111111l1l_opy_(bstack1l1l111l111_opy_, bstack1ll1llll11l_opy_.bstack1l1l11l11l1_opy_, bstack111l111_opy_ (u"ࠥࠦፃ"))
            session.framework_name = bstack1l1l111l111_opy_.framework_name
            session.framework_version = bstack1l1l111l111_opy_.framework_version
            session.framework_session_id = bstack1ll1llll11l_opy_.bstack1111111l1l_opy_(bstack1l1l111l111_opy_, bstack1ll1llll11l_opy_.bstack1l1l111lll1_opy_, bstack111l111_opy_ (u"ࠦࠧፄ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11lll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1111ll1_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1lll111l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1l1111ll1_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፅ") + str(kwargs) + bstack111l111_opy_ (u"ࠨࠢፆ"))
            return
        if len(bstack1l1l1111ll1_opy_) > 1:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፇ") + str(kwargs) + bstack111l111_opy_ (u"ࠣࠤፈ"))
        bstack1l1l11111ll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1l1111ll1_opy_[0]
        page = bstack1l1l11111ll_opy_()
        if not page:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፉ") + str(kwargs) + bstack111l111_opy_ (u"ࠥࠦፊ"))
            return
        return page
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l111l11l_opy_ = {}
        for bstack1l1l111l111_opy_ in bstack1ll1llll11l_opy_.bstack1lllll1llll_opy_.values():
            caps = bstack1ll1llll11l_opy_.bstack1111111l1l_opy_(bstack1l1l111l111_opy_, bstack1ll1llll11l_opy_.bstack1l1l111ll1l_opy_, bstack111l111_opy_ (u"ࠦࠧፋ"))
        bstack1l1l111l11l_opy_[bstack111l111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥፌ")] = caps.get(bstack111l111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢፍ"), bstack111l111_opy_ (u"ࠢࠣፎ"))
        bstack1l1l111l11l_opy_[bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢፏ")] = caps.get(bstack111l111_opy_ (u"ࠤࡲࡷࠧፐ"), bstack111l111_opy_ (u"ࠥࠦፑ"))
        bstack1l1l111l11l_opy_[bstack111l111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨፒ")] = caps.get(bstack111l111_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤፓ"), bstack111l111_opy_ (u"ࠨࠢፔ"))
        bstack1l1l111l11l_opy_[bstack111l111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣፕ")] = caps.get(bstack111l111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥፖ"), bstack111l111_opy_ (u"ࠤࠥፗ"))
        return bstack1l1l111l11l_opy_
    def bstack1ll111l1lll_opy_(self, page: object, bstack1ll11ll1l11_opy_, args={}):
        try:
            bstack1l1l111111l_opy_ = bstack111l111_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠲ࡵࡻࡳࡩࠪࡵࡩࡸࡵ࡬ࡷࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤፘ")
            bstack1ll11ll1l11_opy_ = bstack1ll11ll1l11_opy_.replace(bstack111l111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢፙ"), bstack111l111_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧፚ"))
            script = bstack1l1l111111l_opy_.format(fn_body=bstack1ll11ll1l11_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧ፛") + str(e) + bstack111l111_opy_ (u"ࠢࠣ፜"))