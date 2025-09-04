# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll11_opy_,
    bstack1llllllll1l_opy_,
    bstack1llll1l1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1l1_opy_ import bstack1l1llll1lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1l1l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll11lll1_opy_(bstack1l1llll1lll_opy_):
    bstack1l1l111111l_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᏁ")
    bstack1l1lll1l1l1_opy_ = bstack1111l1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᏂ")
    bstack1l1l1111111_opy_ = bstack1111l1l_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᏃ")
    bstack1l1l1111ll1_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᏄ")
    bstack1l1l11111ll_opy_ = bstack1111l1l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᏅ")
    bstack1l1ll1ll111_opy_ = bstack1111l1l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᏆ")
    bstack1l11llll1l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᏇ")
    bstack1l11llll1ll_opy_ = bstack1111l1l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᏈ")
    def __init__(self):
        super().__init__(bstack1l1lllll11l_opy_=self.bstack1l1l111111l_opy_, frameworks=[bstack1lll1l111ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.BEFORE_EACH, bstack1ll1llll1ll_opy_.POST), self.bstack1l11l1l1ll1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE), self.bstack1ll1111l1l1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll11llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1lll11_opy_ = self.bstack1l11l1l1l11_opy_(instance.context)
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᏉ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠧࠨᏊ"))
        f.bstack1lllllllll1_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, bstack1l1ll1lll11_opy_)
        bstack1l11l1ll1l1_opy_ = self.bstack1l11l1l1l11_opy_(instance.context, bstack1l11l11lll1_opy_=False)
        f.bstack1lllllllll1_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1111111_opy_, bstack1l11l1ll1l1_opy_)
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1l1_opy_, False):
            self.__1l11l1l11ll_opy_(f,instance,bstack1lllll11ll1_opy_)
    def bstack1ll11llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1l1_opy_, False):
            self.__1l11l1l11ll_opy_(f, instance, bstack1lllll11ll1_opy_)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1ll_opy_, False):
            self.__1l11l1l11l1_opy_(f, instance, bstack1lllll11ll1_opy_)
    def bstack1l11l1l1111_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1lllll111_opy_(instance):
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1ll_opy_, False):
            return
        driver.execute_script(
            bstack1111l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᏋ").format(
                json.dumps(
                    {
                        bstack1111l1l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᏌ"): bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᏍ"),
                        bstack1111l1l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᏎ"): {bstack1111l1l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᏏ"): result},
                    }
                )
            )
        )
        f.bstack1lllllllll1_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1ll_opy_, True)
    def bstack1l11l1l1l11_opy_(self, context: bstack1llll1l1ll1_opy_, bstack1l11l11lll1_opy_= True):
        if bstack1l11l11lll1_opy_:
            bstack1l1ll1lll11_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        else:
            bstack1l1ll1lll11_opy_ = self.bstack1l1llll111l_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1lll11_opy_ if f[1].state != bstack1lllll11111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1l11l1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᏐ")).get(bstack1111l1l_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᏑ")):
            bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
            if not bstack1l1ll1lll11_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᏒ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠢࠣᏓ"))
                return
            driver = bstack1l1ll1lll11_opy_[0][0]()
            status = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_, None)
            if not status:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᏔ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠤࠥᏕ"))
                return
            bstack1l1l111l111_opy_ = {bstack1111l1l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᏖ"): status.lower()}
            bstack1l11llll111_opy_ = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l11111l1_opy_, None)
            if status.lower() == bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᏗ") and bstack1l11llll111_opy_ is not None:
                bstack1l1l111l111_opy_[bstack1111l1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᏘ")] = bstack1l11llll111_opy_[0][bstack1111l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᏙ")][0] if isinstance(bstack1l11llll111_opy_, list) else str(bstack1l11llll111_opy_)
            driver.execute_script(
                bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᏚ").format(
                    json.dumps(
                        {
                            bstack1111l1l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᏛ"): bstack1111l1l_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᏜ"),
                            bstack1111l1l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᏝ"): bstack1l1l111l111_opy_,
                        }
                    )
                )
            )
            f.bstack1lllllllll1_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1111lll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1l11l1l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᏞ")).get(bstack1111l1l_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᏟ")):
            test_name = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, None)
            if not test_name:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᏠ"))
                return
            bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
            if not bstack1l1ll1lll11_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᏡ") + str(bstack1lllll11ll1_opy_) + bstack1111l1l_opy_ (u"ࠣࠤᏢ"))
                return
            for bstack1l1l1l11111_opy_, bstack1l11l11llll_opy_ in bstack1l1ll1lll11_opy_:
                if not bstack1lll1l111ll_opy_.bstack1l1lllll111_opy_(bstack1l11l11llll_opy_):
                    continue
                driver = bstack1l1l1l11111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1111l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᏣ").format(
                        json.dumps(
                            {
                                bstack1111l1l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᏤ"): bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᏥ"),
                                bstack1111l1l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᏦ"): {bstack1111l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏧ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lllllllll1_opy_(instance, bstack1llll11lll1_opy_.bstack1l11llll1l1_opy_, True)
    def bstack1l1ll111111_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        bstack1l1ll1lll11_opy_ = [d for d, _ in f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])]
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᏨ"))
            return
        if not bstack1l1ll1l1l1l_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᏩ"))
            return
        for bstack1l11l1ll11l_opy_ in bstack1l1ll1lll11_opy_:
            driver = bstack1l11l1ll11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1111l1l_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᏪ") + str(timestamp)
            driver.execute_script(
                bstack1111l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᏫ").format(
                    json.dumps(
                        {
                            bstack1111l1l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᏬ"): bstack1111l1l_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢᏭ"),
                            bstack1111l1l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᏮ"): {
                                bstack1111l1l_opy_ (u"ࠢࡵࡻࡳࡩࠧᏯ"): bstack1111l1l_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧᏰ"),
                                bstack1111l1l_opy_ (u"ࠤࡧࡥࡹࡧࠢᏱ"): data,
                                bstack1111l1l_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᏲ"): bstack1111l1l_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᏳ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        keys = [
            bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_,
            bstack1llll11lll1_opy_.bstack1l1l1111111_opy_,
        ]
        bstack1l1ll1lll11_opy_ = []
        for key in keys:
            bstack1l1ll1lll11_opy_.extend(f.bstack1lllll1l11l_opy_(instance, key, []))
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᏴ"))
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1ll1ll111_opy_, False):
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨᏵ"))
            return
        self.bstack1ll1l1111ll_opy_()
        bstack1ll1l1lll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        for bstack1l1l1l11111_opy_, driver in bstack1l1ll1lll11_opy_:
            try:
                webdriver = bstack1l1l1l11111_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧ᏶"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1111l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢ᏷")
                    if bstack1lll1l111ll_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1l111ll_opy_.bstack1l11l1ll111_opy_, False)
                    else bstack1111l1l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣᏸ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1lll1l111ll_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1l111ll_opy_.bstack1l1l111ll11_opy_, bstack1111l1l_opy_ (u"ࠥࠦᏹ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1lll1l111ll_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1l111ll_opy_.bstack1l1l111llll_opy_, bstack1111l1l_opy_ (u"ࠦࠧᏺ"))
                caps = None
                if hasattr(webdriver, bstack1111l1l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᏻ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᏼ"))
                    except Exception as e:
                        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧᏽ") + str(e) + bstack1111l1l_opy_ (u"ࠣࠤ᏾"))
                try:
                    bstack1l11l1l1l1l_opy_ = json.dumps(caps).encode(bstack1111l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᏿")) if caps else bstack1l11l1l1lll_opy_ (u"ࠥࡿࢂࠨ᐀")
                    req.capabilities = bstack1l11l1l1l1l_opy_
                except Exception as e:
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢᐁ") + str(e) + bstack1111l1l_opy_ (u"ࠧࠨᐂ"))
            except Exception as e:
                self.logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤᐃ") + str(str(e)) + bstack1111l1l_opy_ (u"ࠢࠣᐄ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1ll1l1l1l_opy_() and len(bstack1l1ll1lll11_opy_) == 0:
            bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1111111_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐅ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠤࠥᐆ"))
            return {}
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐇ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠦࠧᐈ"))
            return {}
        bstack1l1l1l11111_opy_, bstack1l1l11lllll_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11111_opy_()
        if not driver:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐉ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠨࠢᐊ"))
            return {}
        capabilities = f.bstack1lllll1l11l_opy_(bstack1l1l11lllll_opy_, bstack1lll1l111ll_opy_.bstack1l1l111ll1l_opy_)
        if not capabilities:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐋ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤᐌ"))
            return {}
        return capabilities.get(bstack1111l1l_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᐍ"), {})
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1ll1l1l1l_opy_() and len(bstack1l1ll1lll11_opy_) == 0:
            bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1111111_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐎ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠦࠧᐏ"))
            return
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐐ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠨࠢᐑ"))
        bstack1l1l1l11111_opy_, bstack1l1l11lllll_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11111_opy_()
        if not driver:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐒ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤᐓ"))
            return
        return driver