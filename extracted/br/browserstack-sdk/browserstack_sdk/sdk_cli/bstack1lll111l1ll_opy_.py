# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllll1l1l1_opy_,
    bstack1llllllllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllllll1_opy_,
    bstack1lllll11111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_, bstack1ll1ll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1ll_opy_ import bstack1ll11111111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1llll11ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1lll1111_opy_(bstack1ll11111111_opy_):
    bstack1l1l1111ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦᎼ")
    bstack1l1ll1lllll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᎽ")
    bstack1l1l1111111_opy_ = bstack1l1l1ll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᎾ")
    bstack1l1l111l111_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᎿ")
    bstack1l1l11111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨᏀ")
    bstack1l1lll111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᏁ")
    bstack1l1l11111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᏂ")
    bstack1l1l111ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥᏃ")
    def __init__(self):
        super().__init__(bstack1l1lllll11l_opy_=self.bstack1l1l1111ll1_opy_, frameworks=[bstack1ll1lllllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11lll1_opy_((bstack1lll111l111_opy_.BEFORE_EACH, bstack1lll1ll1ll1_opy_.POST), self.bstack1l11l1l1lll_opy_)
        TestFramework.bstack1ll1l11lll1_opy_((bstack1lll111l111_opy_.TEST, bstack1lll1ll1ll1_opy_.PRE), self.bstack1ll1l11l1l1_opy_)
        TestFramework.bstack1ll1l11lll1_opy_((bstack1lll111l111_opy_.TEST, bstack1lll1ll1ll1_opy_.POST), self.bstack1ll11l11lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1llll1_opy_ = self.bstack1l11l1l1l11_opy_(instance.context)
        if not bstack1l1ll1llll1_opy_:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᏄ") + str(bstack111111111l_opy_) + bstack1l1l1ll_opy_ (u"ࠢࠣᏅ"))
        f.bstack1lllllll111_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, bstack1l1ll1llll1_opy_)
        bstack1l11l1l1ll1_opy_ = self.bstack1l11l1l1l11_opy_(instance.context, bstack1l11l1ll11l_opy_=False)
        f.bstack1lllllll111_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l1111111_opy_, bstack1l11l1l1ll1_opy_)
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1lll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l11111l1_opy_, False):
            self.__1l11l1l1l1l_opy_(f,instance,bstack111111111l_opy_)
    def bstack1ll11l11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1lll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l11111l1_opy_, False):
            self.__1l11l1l1l1l_opy_(f, instance, bstack111111111l_opy_)
        if not f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l111ll1l_opy_, False):
            self.__1l11l1llll1_opy_(f, instance, bstack111111111l_opy_)
    def bstack1l11l1lll11_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1111111l_opy_(instance):
            return
        if f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l111ll1l_opy_, False):
            return
        driver.execute_script(
            bstack1l1l1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᏆ").format(
                json.dumps(
                    {
                        bstack1l1l1ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᏇ"): bstack1l1l1ll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᏈ"),
                        bstack1l1l1ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᏉ"): {bstack1l1l1ll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᏊ"): result},
                    }
                )
            )
        )
        f.bstack1lllllll111_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l111ll1l_opy_, True)
    def bstack1l11l1l1l11_opy_(self, context: bstack1lllll11111_opy_, bstack1l11l1ll11l_opy_= True):
        if bstack1l11l1ll11l_opy_:
            bstack1l1ll1llll1_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        else:
            bstack1l1ll1llll1_opy_ = self.bstack1l1lllll1l1_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1llll1_opy_ if f[1].state != bstack1lllll1l1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def __1l11l1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᏋ")).get(bstack1l1l1ll_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᏌ")):
            bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, [])
            if not bstack1l1ll1llll1_opy_:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᏍ") + str(bstack111111111l_opy_) + bstack1l1l1ll_opy_ (u"ࠤࠥᏎ"))
                return
            driver = bstack1l1ll1llll1_opy_[0][0]()
            status = f.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l11lllll11_opy_, None)
            if not status:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᏏ") + str(bstack111111111l_opy_) + bstack1l1l1ll_opy_ (u"ࠦࠧᏐ"))
                return
            bstack1l1l111ll11_opy_ = {bstack1l1l1ll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᏑ"): status.lower()}
            bstack1l1l111l1l1_opy_ = f.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l1l111111l_opy_, None)
            if status.lower() == bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮢ") and bstack1l1l111l1l1_opy_ is not None:
                bstack1l1l111ll11_opy_[bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᏓ")] = bstack1l1l111l1l1_opy_[0][bstack1l1l1ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᏔ")][0] if isinstance(bstack1l1l111l1l1_opy_, list) else str(bstack1l1l111l1l1_opy_)
            driver.execute_script(
                bstack1l1l1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᏕ").format(
                    json.dumps(
                        {
                            bstack1l1l1ll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᏖ"): bstack1l1l1ll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᏗ"),
                            bstack1l1l1ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᏘ"): bstack1l1l111ll11_opy_,
                        }
                    )
                )
            )
            f.bstack1lllllll111_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l111ll1l_opy_, True)
    @measure(event_name=EVENTS.bstack11lllll1l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def __1l11l1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᏙ")).get(bstack1l1l1ll_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᏚ")):
            test_name = f.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l11l1ll111_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᏛ"))
                return
            bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, [])
            if not bstack1l1ll1llll1_opy_:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᏜ") + str(bstack111111111l_opy_) + bstack1l1l1ll_opy_ (u"ࠥࠦᏝ"))
                return
            for bstack1l1l1l1111l_opy_, bstack1l11l1l11ll_opy_ in bstack1l1ll1llll1_opy_:
                if not bstack1ll1lllllll_opy_.bstack1ll1111111l_opy_(bstack1l11l1l11ll_opy_):
                    continue
                driver = bstack1l1l1l1111l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1l1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᏞ").format(
                        json.dumps(
                            {
                                bstack1l1l1ll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᏟ"): bstack1l1l1ll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᏠ"),
                                bstack1l1l1ll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᏡ"): {bstack1l1l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᏢ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lllllll111_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l11111l1_opy_, True)
    def bstack1l1l1ll11ll_opy_(
        self,
        instance: bstack1ll1ll111ll_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1lll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        bstack1l1ll1llll1_opy_ = [d for d, _ in f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, [])]
        if not bstack1l1ll1llll1_opy_:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᏣ"))
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᏤ"))
            return
        for bstack1l11l1ll1l1_opy_ in bstack1l1ll1llll1_opy_:
            driver = bstack1l11l1ll1l1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1l1ll_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤᏥ") + str(timestamp)
            driver.execute_script(
                bstack1l1l1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᏦ").format(
                    json.dumps(
                        {
                            bstack1l1l1ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᏧ"): bstack1l1l1ll_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤᏨ"),
                            bstack1l1l1ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᏩ"): {
                                bstack1l1l1ll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᏪ"): bstack1l1l1ll_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢᏫ"),
                                bstack1l1l1ll_opy_ (u"ࠦࡩࡧࡴࡢࠤᏬ"): data,
                                bstack1l1l1ll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦᏭ"): bstack1l1l1ll_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧᏮ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1l11l_opy_(
        self,
        instance: bstack1ll1ll111ll_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1lll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        keys = [
            bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_,
            bstack1ll1lll1111_opy_.bstack1l1l1111111_opy_,
        ]
        bstack1l1ll1llll1_opy_ = []
        for key in keys:
            bstack1l1ll1llll1_opy_.extend(f.bstack1llll1llll1_opy_(instance, key, []))
        if not bstack1l1ll1llll1_opy_:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡲࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᏯ"))
            return
        if f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1lll111l1_opy_, False):
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡆࡆ࡙ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡤࡴࡨࡥࡹ࡫ࡤࠣᏰ"))
            return
        self.bstack1ll1l111ll1_opy_()
        bstack1lll111ll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1ll1l11l1ll_opy_)
        req.test_framework_name = TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1ll11ll1ll1_opy_)
        req.test_framework_version = TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        req.test_uuid = TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1ll11ll1lll_opy_)
        for bstack1l1l1l1111l_opy_, driver in bstack1l1ll1llll1_opy_:
            try:
                webdriver = bstack1l1l1l1111l_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢᏱ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1l1l1ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᏲ")
                    if bstack1ll1lllllll_opy_.bstack1llll1llll1_opy_(driver, bstack1ll1lllllll_opy_.bstack1l11l1lll1l_opy_, False)
                    else bstack1l1l1ll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᏳ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1ll1lllllll_opy_.bstack1llll1llll1_opy_(driver, bstack1ll1lllllll_opy_.bstack1l1l11lllll_opy_, bstack1l1l1ll_opy_ (u"ࠧࠨᏴ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1ll1lllllll_opy_.bstack1llll1llll1_opy_(driver, bstack1ll1lllllll_opy_.bstack1l1l11ll1ll_opy_, bstack1l1l1ll_opy_ (u"ࠨࠢᏵ"))
                caps = None
                if hasattr(webdriver, bstack1l1l1ll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᏶")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡧ࡭ࡷ࡫ࡣࡵ࡮ࡼࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᏷"))
                    except Exception as e:
                        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᏸ") + str(e) + bstack1l1l1ll_opy_ (u"ࠥࠦᏹ"))
                try:
                    bstack1l11l1lllll_opy_ = json.dumps(caps).encode(bstack1l1l1ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏺ")) if caps else bstack1l11l1ll1ll_opy_ (u"ࠧࢁࡽࠣᏻ")
                    req.capabilities = bstack1l11l1lllll_opy_
                except Exception as e:
                    self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡵࡨࡶ࡮ࡧ࡬ࡪࡼࡨࠤࡨࡧࡰࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࠤᏼ") + str(e) + bstack1l1l1ll_opy_ (u"ࠢࠣᏽ"))
            except Exception as e:
                self.logger.error(bstack1l1l1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡺࡥ࡮࠼ࠣࠦ᏾") + str(str(e)) + bstack1l1l1ll_opy_ (u"ࠤࠥ᏿"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, [])
        if not bstack1l1llll11ll_opy_() and len(bstack1l1ll1llll1_opy_) == 0:
            bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l1111111_opy_, [])
        if not bstack1l1ll1llll1_opy_:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᐀") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠦࠧᐁ"))
            return {}
        if len(bstack1l1ll1llll1_opy_) > 1:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐂ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠨࠢᐃ"))
            return {}
        bstack1l1l1l1111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l1ll1llll1_opy_[0]
        driver = bstack1l1l1l1111l_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐄ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠣࠤᐅ"))
            return {}
        capabilities = f.bstack1llll1llll1_opy_(bstack1l1l1l11l1l_opy_, bstack1ll1lllllll_opy_.bstack1l1l111lll1_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐆ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠥࠦᐇ"))
            return {}
        return capabilities.get(bstack1l1l1ll_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᐈ"), {})
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1ll1lllll_opy_, [])
        if not bstack1l1llll11ll_opy_() and len(bstack1l1ll1llll1_opy_) == 0:
            bstack1l1ll1llll1_opy_ = f.bstack1llll1llll1_opy_(instance, bstack1ll1lll1111_opy_.bstack1l1l1111111_opy_, [])
        if not bstack1l1ll1llll1_opy_:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐉ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠨࠢᐊ"))
            return
        if len(bstack1l1ll1llll1_opy_) > 1:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐋ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠣࠤᐌ"))
        bstack1l1l1l1111l_opy_, bstack1l1l1l11l1l_opy_ = bstack1l1ll1llll1_opy_[0]
        driver = bstack1l1l1l1111l_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐍ") + str(kwargs) + bstack1l1l1ll_opy_ (u"ࠥࠦᐎ"))
            return
        return driver