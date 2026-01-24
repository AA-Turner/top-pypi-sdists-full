# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1l1111l_opy_,
    bstack1lll11lll11_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1l111l1_opy_, bstack1llllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_, bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1ll1_opy_ import bstack1ll1ll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11l1l_opy_ import bstack1l1l1l111ll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l1l11l1_opy_ import bstack1lll1l1l_opy_, bstack1l111l1ll_opy_, bstack1llll1lll1_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll111lll1l_opy_(bstack1l1l1l111ll_opy_):
    bstack1l111ll11l1_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᐊ")
    bstack1l11llll1ll_opy_ = bstack1l1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᐋ")
    bstack1l111l1llll_opy_ = bstack1l1111_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᐌ")
    bstack1l111lll11l_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᐍ")
    bstack1l111ll1l11_opy_ = bstack1l1111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᐎ")
    bstack1l1l111ll11_opy_ = bstack1l1111_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᐏ")
    bstack1l111ll1111_opy_ = bstack1l1111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᐐ")
    bstack1l111ll1l1l_opy_ = bstack1l1111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᐑ")
    def __init__(self):
        super().__init__(bstack1l1l1l1ll1l_opy_=self.bstack1l111ll11l1_opy_, frameworks=[bstack1ll1l111l1l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.BEFORE_EACH, bstack1ll1l111111_opy_.POST), self.bstack1l111l1ll1l_opy_)
        if bstack1llllll1l_opy_():
            TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), self.bstack1l1llll1l1l_opy_)
        else:
            TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.PRE), self.bstack1l1llll1l1l_opy_)
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), self.bstack1l1ll1ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l111l1lll1_opy_ = self.bstack1l111lll111_opy_(instance.context)
        if not bstack1l111l1lll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᐒ") + str(bstack1lll111llll_opy_) + bstack1l1111_opy_ (u"ࠣࠤᐓ"))
            return
        f.bstack1lll11l1ll1_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11llll1ll_opy_, bstack1l111l1lll1_opy_)
    def bstack1l111lll111_opy_(self, context: bstack1lll11lll11_opy_, bstack1l111ll11ll_opy_= True):
        if bstack1l111ll11ll_opy_:
            bstack1l111l1lll1_opy_ = self.bstack1l1l1l11lll_opy_(context, reverse=True)
        else:
            bstack1l111l1lll1_opy_ = self.bstack1l1l1l1l1ll_opy_(context, reverse=True)
        return [f for f in bstack1l111l1lll1_opy_ if f[1].state != bstack1lll111lll1_opy_.QUIT]
    def bstack1l1llll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1ll1l_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        if not bstack1l1l1l111l1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐔ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᐕ"))
            return
        bstack1l111l1lll1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11llll1ll_opy_, [])
        if not bstack1l111l1lll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐖ") + str(kwargs) + bstack1l1111_opy_ (u"ࠧࠨᐗ"))
            return
        if len(bstack1l111l1lll1_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1l1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᐘ"))
        bstack1l111ll1ll1_opy_, bstack1l11l1l11l1_opy_ = bstack1l111l1lll1_opy_[0]
        page = bstack1l111ll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐙ") + str(kwargs) + bstack1l1111_opy_ (u"ࠣࠤᐚ"))
            return
        bstack1l1l111l_opy_ = getattr(args[0], bstack1l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᐛ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᐜ")).get(bstack1l1111_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᐝ")):
            try:
                page.evaluate(bstack1l1111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᐞ"),
                            bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᐟ") + json.dumps(
                                bstack1l1l111l_opy_) + bstack1l1111_opy_ (u"ࠢࡾࡿࠥᐠ"))
            except Exception as e:
                self.logger.debug(bstack1l1111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᐡ"), e)
    def bstack1l1ll1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1ll1l_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        if not bstack1l1l1l111l1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐢ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᐣ"))
            return
        bstack1l111l1lll1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11llll1ll_opy_, [])
        if not bstack1l111l1lll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐤ") + str(kwargs) + bstack1l1111_opy_ (u"ࠧࠨᐥ"))
            return
        if len(bstack1l111l1lll1_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1l1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᐦ"))
        bstack1l111ll1ll1_opy_, bstack1l11l1l11l1_opy_ = bstack1l111l1lll1_opy_[0]
        page = bstack1l111ll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐧ") + str(kwargs) + bstack1l1111_opy_ (u"ࠣࠤᐨ"))
            return
        status = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l111l1l1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᐩ") + str(bstack1lll111llll_opy_) + bstack1l1111_opy_ (u"ࠥࠦᐪ"))
            return
        bstack1l111l1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᐫ"): status.lower()}
        bstack1l111lll1l1_opy_ = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, None)
        if status.lower() == bstack1l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᐬ") and bstack1l111lll1l1_opy_ is not None:
            bstack1l111l1l1ll_opy_[bstack1l1111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᐭ")] = bstack1l111lll1l1_opy_[0][bstack1l1111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᐮ")][0] if isinstance(bstack1l111lll1l1_opy_, list) else str(bstack1l111lll1l1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᐯ")).get(bstack1l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᐰ")):
            try:
                page.evaluate(
                        bstack1l1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᐱ"),
                        bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࠩᐲ")
                        + json.dumps(bstack1l111l1l1ll_opy_)
                        + bstack1l1111_opy_ (u"ࠧࢃࠢᐳ")
                    )
            except Exception as e:
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨᐴ"), e)
    def bstack1l11l1llll1_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        f: TestFramework,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1ll1l_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        if not bstack1l1l1l111l1_opy_:
            self.logger.debug(
                bstack1ll1ll1l1ll_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᐵ"))
            return
        bstack1l111l1lll1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11llll1ll_opy_, [])
        if not bstack1l111l1lll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐶ") + str(kwargs) + bstack1l1111_opy_ (u"ࠤࠥᐷ"))
            return
        if len(bstack1l111l1lll1_opy_) > 1:
            self.logger.debug(
                bstack1ll1ll1l1ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᐸ"))
        bstack1l111ll1ll1_opy_, bstack1l11l1l11l1_opy_ = bstack1l111l1lll1_opy_[0]
        page = bstack1l111ll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐹ") + str(kwargs) + bstack1l1111_opy_ (u"ࠧࠨᐺ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1111_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᐻ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᐼ"),
                bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᐽ").format(
                    json.dumps(
                        {
                            bstack1l1111_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᐾ"): bstack1l1111_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᐿ"),
                            bstack1l1111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᑀ"): {
                                bstack1l1111_opy_ (u"ࠧࡺࡹࡱࡧࠥᑁ"): bstack1l1111_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᑂ"),
                                bstack1l1111_opy_ (u"ࠢࡥࡣࡷࡥࠧᑃ"): data,
                                bstack1l1111_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᑄ"): bstack1l1111_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᑅ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦ࡯࠲࠳ࡼࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡾࢁࠧᑆ"), e)
    def bstack1l11llllll1_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        f: TestFramework,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111l1ll1l_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        if f.bstack1lll1l11lll_opy_(instance, bstack1ll111lll1l_opy_.bstack1l1l111ll11_opy_, False):
            return
        self.bstack1l1lllllll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
        req.client_worker_id = bstack1l1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᑇ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1l1l1111l_opy_)
        req.test_framework_state = bstack1lll111llll_opy_[0].name
        req.test_hook_state = bstack1lll111llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
        for bstack1l111ll111l_opy_ in bstack1ll1ll11ll1_opy_.bstack1lll11ll1ll_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᑈ")
                if bstack1l1l1l111l1_opy_
                else bstack1l1111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᑉ")
            )
            session.ref = bstack1l111ll111l_opy_.ref()
            session.hub_url = bstack1ll1ll11ll1_opy_.bstack1lll1l11lll_opy_(bstack1l111ll111l_opy_, bstack1ll1ll11ll1_opy_.bstack1l111lllll1_opy_, bstack1l1111_opy_ (u"ࠢࠣᑊ"))
            session.framework_name = bstack1l111ll111l_opy_.framework_name
            session.framework_version = bstack1l111ll111l_opy_.framework_version
            session.framework_session_id = bstack1ll1ll11ll1_opy_.bstack1lll1l11lll_opy_(bstack1l111ll111l_opy_, bstack1ll1ll11ll1_opy_.bstack1l11l1111ll_opy_, bstack1l1111_opy_ (u"ࠣࠤᑋ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1lll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs
    ):
        bstack1l111l1lll1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11llll1ll_opy_, [])
        if not bstack1l111l1lll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᑌ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᑍ"))
            return
        if len(bstack1l111l1lll1_opy_) > 1:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑎ") + str(kwargs) + bstack1l1111_opy_ (u"ࠧࠨᑏ"))
        bstack1l111ll1ll1_opy_, bstack1l11l1l11l1_opy_ = bstack1l111l1lll1_opy_[0]
        page = bstack1l111ll1ll1_opy_()
        if not page:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᑐ") + str(kwargs) + bstack1l1111_opy_ (u"ࠢࠣᑑ"))
            return
        return page
    def bstack1l1llllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l111lll1ll_opy_ = {}
        for bstack1l111ll111l_opy_ in bstack1ll1ll11ll1_opy_.bstack1lll11ll1ll_opy_.values():
            caps = bstack1ll1ll11ll1_opy_.bstack1lll1l11lll_opy_(bstack1l111ll111l_opy_, bstack1ll1ll11ll1_opy_.bstack1l11l111lll_opy_, bstack1l1111_opy_ (u"ࠣࠤᑒ"))
        bstack1l111lll1ll_opy_[bstack1l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢᑓ")] = caps.get(bstack1l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦᑔ"), bstack1l1111_opy_ (u"ࠦࠧᑕ"))
        bstack1l111lll1ll_opy_[bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᑖ")] = caps.get(bstack1l1111_opy_ (u"ࠨ࡯ࡴࠤᑗ"), bstack1l1111_opy_ (u"ࠢࠣᑘ"))
        bstack1l111lll1ll_opy_[bstack1l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᑙ")] = caps.get(bstack1l1111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᑚ"), bstack1l1111_opy_ (u"ࠥࠦᑛ"))
        bstack1l111lll1ll_opy_[bstack1l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧᑜ")] = caps.get(bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᑝ"), bstack1l1111_opy_ (u"ࠨࠢᑞ"))
        return bstack1l111lll1ll_opy_
    def bstack1l1lll1l11l_opy_(self, page: object, bstack1l1ll1l1ll1_opy_, args={}):
        try:
            bstack1l111ll1lll_opy_ = bstack1l1111_opy_ (u"ࠢࠣࠤࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮࠮࠯࠰ࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠫࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡁࡃࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡽࡩࡲࡤࡨ࡯ࡥࡻࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮࠮ࡻࡢࡴࡪࡣ࡯ࡹ࡯࡯ࡿࠬࠦࠧࠨᑟ")
            bstack1l1ll1l1ll1_opy_ = bstack1l1ll1l1ll1_opy_.replace(bstack1l1111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᑠ"), bstack1l1111_opy_ (u"ࠤࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠤᑡ"))
            script = bstack1l111ll1lll_opy_.format(fn_body=bstack1l1ll1l1ll1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠥࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࠬࠡࠤᑢ") + str(e) + bstack1l1111_opy_ (u"ࠦࠧᑣ"))