# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1llllllll1l_opy_,
    bstack1lllllll111_opy_,
    bstack1llll1lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_, bstack1lll11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1111_opy_ import bstack1l1lllll111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll11111l_opy_(bstack1l1lllll111_opy_):
    bstack1l11lllll11_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᎿ")
    bstack1l1ll11l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᏀ")
    bstack1l1l1111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᏁ")
    bstack1l11lll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᏂ")
    bstack1l1l11111ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᏃ")
    bstack1l1lll111l1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᏄ")
    bstack1l11llll11l_opy_ = bstack1l11ll1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᏅ")
    bstack1l11llll111_opy_ = bstack1l11ll1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᏆ")
    def __init__(self):
        super().__init__(bstack1l1llll1l1l_opy_=self.bstack1l11lllll11_opy_, frameworks=[bstack1ll1l1l1lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1lll111l1l1_opy_.POST), self.bstack1l11l11llll_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.PRE), self.bstack1ll11l11ll1_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l11llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l1l111_opy_ = self.bstack1l11l1ll111_opy_(instance.context)
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᏇ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠥࠦᏈ"))
        f.bstack1llllll1ll1_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, bstack1l1l1l1l111_opy_)
        bstack1l11l1ll11l_opy_ = self.bstack1l11l1ll111_opy_(instance.context, bstack1l11l1l11ll_opy_=False)
        f.bstack1llllll1ll1_opy_(instance, bstack1llll11111l_opy_.bstack1l1l1111l1l_opy_, bstack1l11l1ll11l_opy_)
    def bstack1ll11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l11llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if not f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll11l_opy_, False):
            self.__1l11l11ll1l_opy_(f,instance,bstack1lllll1llll_opy_)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l11llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        if not f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll11l_opy_, False):
            self.__1l11l11ll1l_opy_(f, instance, bstack1lllll1llll_opy_)
        if not f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll111_opy_, False):
            self.__1l11l1l1lll_opy_(f, instance, bstack1lllll1llll_opy_)
    def bstack1l11l11lll1_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1lllll1l1_opy_(instance):
            return
        if f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll111_opy_, False):
            return
        driver.execute_script(
            bstack1l11ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᏉ").format(
                json.dumps(
                    {
                        bstack1l11ll1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᏊ"): bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᏋ"),
                        bstack1l11ll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᏌ"): {bstack1l11ll1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᏍ"): result},
                    }
                )
            )
        )
        f.bstack1llllll1ll1_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll111_opy_, True)
    def bstack1l11l1ll111_opy_(self, context: bstack1llll1lllll_opy_, bstack1l11l1l11ll_opy_= True):
        if bstack1l11l1l11ll_opy_:
            bstack1l1l1l1l111_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        else:
            bstack1l1l1l1l111_opy_ = self.bstack1l1lllll11l_opy_(context, reverse=True)
        return [f for f in bstack1l1l1l1l111_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1llll1111_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1l11l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᏎ")).get(bstack1l11ll1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᏏ")):
            bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
            if not bstack1l1l1l1l111_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᏐ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠧࠨᏑ"))
                return
            driver = bstack1l1l1l1l111_opy_[0][0]()
            status = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1111ll1_opy_, None)
            if not status:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᏒ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣᏓ"))
                return
            bstack1l11llll1l1_opy_ = {bstack1l11ll1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᏔ"): status.lower()}
            bstack1l1l1111111_opy_ = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_, None)
            if status.lower() == bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏕ") and bstack1l1l1111111_opy_ is not None:
                bstack1l11llll1l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᏖ")] = bstack1l1l1111111_opy_[0][bstack1l11ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᏗ")][0] if isinstance(bstack1l1l1111111_opy_, list) else str(bstack1l1l1111111_opy_)
            driver.execute_script(
                bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᏘ").format(
                    json.dumps(
                        {
                            bstack1l11ll1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᏙ"): bstack1l11ll1_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᏚ"),
                            bstack1l11ll1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᏛ"): bstack1l11llll1l1_opy_,
                        }
                    )
                )
            )
            f.bstack1llllll1ll1_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll111_opy_, True)
    @measure(event_name=EVENTS.bstack11l1l1l11l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1l11l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᏜ")).get(bstack1l11ll1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᏝ")):
            test_name = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᏞ"))
                return
            bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
            if not bstack1l1l1l1l111_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᏟ") + str(bstack1lllll1llll_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢᏠ"))
                return
            for bstack1l1l11llll1_opy_, bstack1l11l1l1l1l_opy_ in bstack1l1l1l1l111_opy_:
                if not bstack1ll1l1l1lll_opy_.bstack1l1lllll1l1_opy_(bstack1l11l1l1l1l_opy_):
                    continue
                driver = bstack1l1l11llll1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l11ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᏡ").format(
                        json.dumps(
                            {
                                bstack1l11ll1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᏢ"): bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᏣ"),
                                bstack1l11ll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᏤ"): {bstack1l11ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏥ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llllll1ll1_opy_(instance, bstack1llll11111l_opy_.bstack1l11llll11l_opy_, True)
    def bstack1l1lll1l111_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        f: TestFramework,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l11llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        bstack1l1l1l1l111_opy_ = [d for d, _ in f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])]
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᏦ"))
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᏧ"))
            return
        for bstack1l11l1l1ll1_opy_ in bstack1l1l1l1l111_opy_:
            driver = bstack1l11l1l1ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l11ll1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧᏨ") + str(timestamp)
            driver.execute_script(
                bstack1l11ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᏩ").format(
                    json.dumps(
                        {
                            bstack1l11ll1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᏪ"): bstack1l11ll1_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᏫ"),
                            bstack1l11ll1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᏬ"): {
                                bstack1l11ll1_opy_ (u"ࠧࡺࡹࡱࡧࠥᏭ"): bstack1l11ll1_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᏮ"),
                                bstack1l11ll1_opy_ (u"ࠢࡥࡣࡷࡥࠧᏯ"): data,
                                bstack1l11ll1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᏰ"): bstack1l11ll1_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᏱ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll1ll1l1_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        f: TestFramework,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l11llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        keys = [
            bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_,
            bstack1llll11111l_opy_.bstack1l1l1111l1l_opy_,
        ]
        bstack1l1l1l1l111_opy_ = []
        for key in keys:
            bstack1l1l1l1l111_opy_.extend(f.bstack1llllllllll_opy_(instance, key, []))
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᏲ"))
            return
        if f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1lll111l1_opy_, False):
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦᏳ"))
            return
        self.bstack1ll11l111l1_opy_()
        bstack1l11ll1ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_)
        req.test_framework_name = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        req.test_framework_version = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1l1l1ll_opy_)
        req.test_framework_state = bstack1lllll1llll_opy_[0].name
        req.test_hook_state = bstack1lllll1llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        for bstack1l1l11llll1_opy_, driver in bstack1l1l1l1l111_opy_:
            try:
                webdriver = bstack1l1l11llll1_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠧ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠤ࠭ࡸࡥࡧࡧࡵࡩࡳࡩࡥࠡࡧࡻࡴ࡮ࡸࡥࡥࠫࠥᏴ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1l11ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᏵ")
                    if bstack1ll1l1l1lll_opy_.bstack1llllllllll_opy_(driver, bstack1ll1l1l1lll_opy_.bstack1l11l1l1l11_opy_, False)
                    else bstack1l11ll1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨ᏶")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1ll1l1l1lll_opy_.bstack1llllllllll_opy_(driver, bstack1ll1l1l1lll_opy_.bstack1l1l11l1ll1_opy_, bstack1l11ll1_opy_ (u"ࠣࠤ᏷"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1ll1l1l1lll_opy_.bstack1llllllllll_opy_(driver, bstack1ll1l1l1lll_opy_.bstack1l1l11l1l1l_opy_, bstack1l11ll1_opy_ (u"ࠤࠥᏸ"))
                caps = None
                if hasattr(webdriver, bstack1l11ll1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᏹ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡪࡩࡳࡧࡦࡸࡱࡿࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᏺ"))
                    except Exception as e:
                        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᏻ") + str(e) + bstack1l11ll1_opy_ (u"ࠨࠢᏼ"))
                try:
                    bstack1l11l1l1111_opy_ = json.dumps(caps).encode(bstack1l11ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᏽ")) if caps else bstack1l11l1l111l_opy_ (u"ࠣࡽࢀࠦ᏾")
                    req.capabilities = bstack1l11l1l1111_opy_
                except Exception as e:
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸ࡫ࡲࡪࡣ࡯࡭ࡿ࡫ࠠࡤࡣࡳࡷࠥ࡬࡯ࡳࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࠧ᏿") + str(e) + bstack1l11ll1_opy_ (u"ࠥࠦ᐀"))
            except Exception as e:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡶࡨࡱ࠿ࠦࠢᐁ") + str(str(e)) + bstack1l11ll1_opy_ (u"ࠧࠨᐂ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1lll11ll1_opy_() and len(bstack1l1l1l1l111_opy_) == 0:
            bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1l1111l1l_opy_, [])
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐃ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠢࠣᐄ"))
            return {}
        if len(bstack1l1l1l1l111_opy_) > 1:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐅ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠤࠥᐆ"))
            return {}
        bstack1l1l11llll1_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l1l1l111_opy_[0]
        driver = bstack1l1l11llll1_opy_()
        if not driver:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐇ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠦࠧᐈ"))
            return {}
        capabilities = f.bstack1llllllllll_opy_(bstack1l1l1l11lll_opy_, bstack1ll1l1l1lll_opy_.bstack1l1l111lll1_opy_)
        if not capabilities:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐉ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢᐊ"))
            return {}
        return capabilities.get(bstack1l11ll1_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧᐋ"), {})
    def bstack1ll1111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1lll11ll1_opy_() and len(bstack1l1l1l1l111_opy_) == 0:
            bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1l1111l1l_opy_, [])
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐌ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠤࠥᐍ"))
            return
        if len(bstack1l1l1l1l111_opy_) > 1:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐎ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠦࠧᐏ"))
        bstack1l1l11llll1_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l1l1l111_opy_[0]
        driver = bstack1l1l11llll1_opy_()
        if not driver:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐐ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢᐑ"))
            return
        return driver