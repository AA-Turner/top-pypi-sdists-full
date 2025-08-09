# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llllllll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll11l_opy_ import bstack1ll111111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll111l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1l1l1l1_opy_(bstack1ll111111ll_opy_):
    bstack1l1l111l1ll_opy_ = bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᎶ")
    bstack1l1ll11l111_opy_ = bstack11l1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᎷ")
    bstack1l1l1111l1l_opy_ = bstack11l1_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᎸ")
    bstack1l11lllllll_opy_ = bstack11l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᎹ")
    bstack1l11llllll1_opy_ = bstack11l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᎺ")
    bstack1l1lll11l11_opy_ = bstack11l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᎻ")
    bstack1l1l111llll_opy_ = bstack11l1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᎼ")
    bstack1l1l111ll1l_opy_ = bstack11l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᎽ")
    def __init__(self):
        super().__init__(bstack1l1lllll1ll_opy_=self.bstack1l1l111l1ll_opy_, frameworks=[bstack1llll1l11l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.BEFORE_EACH, bstack1lll1ll1l1l_opy_.POST), self.bstack1l11l1ll111_opy_)
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.POST), self.bstack1ll11l1l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1ll111_opy_ = self.bstack1l11l1lll11_opy_(instance.context)
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᎾ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠣࠤᎿ"))
        f.bstack1111111lll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, bstack1l1ll1ll111_opy_)
        bstack1l11l1lll1l_opy_ = self.bstack1l11l1lll11_opy_(instance.context, bstack1l11l1ll1ll_opy_=False)
        f.bstack1111111lll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l1111l1l_opy_, bstack1l11l1lll1l_opy_)
    def bstack1ll11l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll111_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if not f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111llll_opy_, False):
            self.__1l11l1l1lll_opy_(f,instance,bstack1lllllll11l_opy_)
    def bstack1ll11l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll111_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        if not f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111llll_opy_, False):
            self.__1l11l1l1lll_opy_(f, instance, bstack1lllllll11l_opy_)
        if not f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111ll1l_opy_, False):
            self.__1l11l1ll1l1_opy_(f, instance, bstack1lllllll11l_opy_)
    def bstack1l11l1llll1_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll11111l11_opy_(instance):
            return
        if f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111ll1l_opy_, False):
            return
        driver.execute_script(
            bstack11l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᏀ").format(
                json.dumps(
                    {
                        bstack11l1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᏁ"): bstack11l1_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᏂ"),
                        bstack11l1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᏃ"): {bstack11l1_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᏄ"): result},
                    }
                )
            )
        )
        f.bstack1111111lll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111ll1l_opy_, True)
    def bstack1l11l1lll11_opy_(self, context: bstack1llllllll11_opy_, bstack1l11l1ll1ll_opy_= True):
        if bstack1l11l1ll1ll_opy_:
            bstack1l1ll1ll111_opy_ = self.bstack1ll111111l1_opy_(context, reverse=True)
        else:
            bstack1l1ll1ll111_opy_ = self.bstack1ll1111111l_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1ll111_opy_ if f[1].state != bstack1llllllllll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def __1l11l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᏅ")).get(bstack11l1_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᏆ")):
            bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
            if not bstack1l1ll1ll111_opy_:
                self.logger.debug(bstack11l1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᏇ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠥࠦᏈ"))
                return
            driver = bstack1l1ll1ll111_opy_[0][0]()
            status = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l111lll1_opy_, None)
            if not status:
                self.logger.debug(bstack11l1_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᏉ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠧࠨᏊ"))
                return
            bstack1l1l11111ll_opy_ = {bstack11l1_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᏋ"): status.lower()}
            bstack1l1l1111ll1_opy_ = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l111111l_opy_, None)
            if status.lower() == bstack11l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᏌ") and bstack1l1l1111ll1_opy_ is not None:
                bstack1l1l11111ll_opy_[bstack11l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᏍ")] = bstack1l1l1111ll1_opy_[0][bstack11l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᏎ")][0] if isinstance(bstack1l1l1111ll1_opy_, list) else str(bstack1l1l1111ll1_opy_)
            driver.execute_script(
                bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᏏ").format(
                    json.dumps(
                        {
                            bstack11l1_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᏐ"): bstack11l1_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᏑ"),
                            bstack11l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᏒ"): bstack1l1l11111ll_opy_,
                        }
                    )
                )
            )
            f.bstack1111111lll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111ll1l_opy_, True)
    @measure(event_name=EVENTS.bstack11l1111l1_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def __1l11l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᏓ")).get(bstack11l1_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᏔ")):
            test_name = f.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l11l1l1l1l_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᏕ"))
                return
            bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
            if not bstack1l1ll1ll111_opy_:
                self.logger.debug(bstack11l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᏖ") + str(bstack1lllllll11l_opy_) + bstack11l1_opy_ (u"ࠦࠧᏗ"))
                return
            for bstack1l1l1l11lll_opy_, bstack1l11l1l1ll1_opy_ in bstack1l1ll1ll111_opy_:
                if not bstack1llll1l11l1_opy_.bstack1ll11111l11_opy_(bstack1l11l1l1ll1_opy_):
                    continue
                driver = bstack1l1l1l11lll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᏘ").format(
                        json.dumps(
                            {
                                bstack11l1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᏙ"): bstack11l1_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᏚ"),
                                bstack11l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᏛ"): {bstack11l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏜ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1111111lll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111llll_opy_, True)
    def bstack1l1l1lll11l_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll111_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        bstack1l1ll1ll111_opy_ = [d for d, _ in f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])]
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥᏝ"))
            return
        if not bstack1l1ll111l1l_opy_():
            self.logger.debug(bstack11l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᏞ"))
            return
        for bstack1l11ll11111_opy_ in bstack1l1ll1ll111_opy_:
            driver = bstack1l11ll11111_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥᏟ") + str(timestamp)
            driver.execute_script(
                bstack11l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᏠ").format(
                    json.dumps(
                        {
                            bstack11l1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᏡ"): bstack11l1_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥᏢ"),
                            bstack11l1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᏣ"): {
                                bstack11l1_opy_ (u"ࠥࡸࡾࡶࡥࠣᏤ"): bstack11l1_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣᏥ"),
                                bstack11l1_opy_ (u"ࠧࡪࡡࡵࡣࠥᏦ"): data,
                                bstack11l1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧᏧ"): bstack11l1_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨᏨ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll1l11l1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll111_opy_(f, instance, bstack1lllllll11l_opy_, *args, **kwargs)
        keys = [
            bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_,
            bstack1lll1l1l1l1_opy_.bstack1l1l1111l1l_opy_,
        ]
        bstack1l1ll1ll111_opy_ = []
        for key in keys:
            bstack1l1ll1ll111_opy_.extend(f.bstack1lllllllll1_opy_(instance, key, []))
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡳࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥᏩ"))
            return
        if f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1lll11l11_opy_, False):
            self.logger.debug(bstack11l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡇࡇ࡚ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡥࡵࡩࡦࡺࡥࡥࠤᏪ"))
            return
        self.bstack1ll11llllll_opy_()
        bstack11ll111l1l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll111lll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_)
        req.test_framework_state = bstack1lllllll11l_opy_[0].name
        req.test_hook_state = bstack1lllllll11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        for bstack1l1l1l11lll_opy_, driver in bstack1l1ll1ll111_opy_:
            try:
                webdriver = bstack1l1l1l11lll_opy_()
                if webdriver is None:
                    self.logger.debug(bstack11l1_opy_ (u"࡛ࠥࡪࡨࡄࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࠫࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࠦࡥࡹࡲ࡬ࡶࡪࡪࠩࠣᏫ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack11l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᏬ")
                    if bstack1llll1l11l1_opy_.bstack1lllllllll1_opy_(driver, bstack1llll1l11l1_opy_.bstack1l11l1lllll_opy_, False)
                    else bstack11l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᏭ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1llll1l11l1_opy_.bstack1lllllllll1_opy_(driver, bstack1llll1l11l1_opy_.bstack1l1l1l11111_opy_, bstack11l1_opy_ (u"ࠨࠢᏮ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1llll1l11l1_opy_.bstack1lllllllll1_opy_(driver, bstack1llll1l11l1_opy_.bstack1l1l11l1l11_opy_, bstack11l1_opy_ (u"ࠢࠣᏯ"))
                caps = None
                if hasattr(webdriver, bstack11l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᏰ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack11l1_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡨ࡮ࡸࡥࡤࡶ࡯ࡽࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᏱ"))
                    except Exception as e:
                        self.logger.debug(bstack11l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࠣᏲ") + str(e) + bstack11l1_opy_ (u"ࠦࠧᏳ"))
                try:
                    bstack1l11ll1111l_opy_ = json.dumps(caps).encode(bstack11l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᏴ")) if caps else bstack1l11l1ll11l_opy_ (u"ࠨࡻࡾࠤᏵ")
                    req.capabilities = bstack1l11ll1111l_opy_
                except Exception as e:
                    self.logger.debug(bstack11l1_opy_ (u"ࠢࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡶࡩࡷ࡯ࡡ࡭࡫ࡽࡩࠥࡩࡡࡱࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࠥ᏶") + str(e) + bstack11l1_opy_ (u"ࠣࠤ᏷"))
            except Exception as e:
                self.logger.error(bstack11l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯ࡴࡦ࡯࠽ࠤࠧᏸ") + str(str(e)) + bstack11l1_opy_ (u"ࠥࠦᏹ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1ll111l1l_opy_() and len(bstack1l1ll1ll111_opy_) == 0:
            bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l1111l1l_opy_, [])
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏺ") + str(kwargs) + bstack11l1_opy_ (u"ࠧࠨᏻ"))
            return {}
        if len(bstack1l1ll1ll111_opy_) > 1:
            self.logger.debug(bstack11l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᏼ") + str(kwargs) + bstack11l1_opy_ (u"ࠢࠣᏽ"))
            return {}
        bstack1l1l1l11lll_opy_, bstack1l1l1l1l111_opy_ = bstack1l1ll1ll111_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᏾") + str(kwargs) + bstack11l1_opy_ (u"ࠤࠥ᏿"))
            return {}
        capabilities = f.bstack1lllllllll1_opy_(bstack1l1l1l1l111_opy_, bstack1llll1l11l1_opy_.bstack1l1l11l1lll_opy_)
        if not capabilities:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᐀") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧᐁ"))
            return {}
        return capabilities.get(bstack11l1_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᐂ"), {})
    def bstack1ll1l111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1ll111l1l_opy_() and len(bstack1l1ll1ll111_opy_) == 0:
            bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l1111l1l_opy_, [])
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐃ") + str(kwargs) + bstack11l1_opy_ (u"ࠢࠣᐄ"))
            return
        if len(bstack1l1ll1ll111_opy_) > 1:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐅ") + str(kwargs) + bstack11l1_opy_ (u"ࠤࠥᐆ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1l1l111_opy_ = bstack1l1ll1ll111_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack11l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐇ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧᐈ"))
            return
        return driver