# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll111_opy_,
    bstack1llllll111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_, bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1l1l_opy_ import bstack1l1lllll111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1lll111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1111ll1_opy_(bstack1l1lllll111_opy_):
    bstack1l1l1111111_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣᏀ")
    bstack1l1lll111l1_opy_ = bstack1ll11ll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᏁ")
    bstack1l1l1111lll_opy_ = bstack1ll11ll_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᏂ")
    bstack1l11lllll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᏃ")
    bstack1l1l1111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥᏄ")
    bstack1l1lll1111l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨᏅ")
    bstack1l11llll1ll_opy_ = bstack1ll11ll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᏆ")
    bstack1l1l11111ll_opy_ = bstack1ll11ll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢᏇ")
    def __init__(self):
        super().__init__(bstack1l1llll1l11_opy_=self.bstack1l1l1111111_opy_, frameworks=[bstack1ll1l1ll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.BEFORE_EACH, bstack1ll1lllll11_opy_.POST), self.bstack1l11l1ll11l_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.PRE), self.bstack1ll11ll1l11_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll1l1111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll111ll_opy_ = self.bstack1l11l1l1ll1_opy_(instance.context)
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᏈ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠦࠧᏉ"))
        f.bstack1llll1l1lll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, bstack1l1lll111ll_opy_)
        bstack1l11l1l1l11_opy_ = self.bstack1l11l1l1ll1_opy_(instance.context, bstack1l11l1l11ll_opy_=False)
        f.bstack1llll1l1lll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l1111lll_opy_, bstack1l11l1l1l11_opy_)
    def bstack1ll11ll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll11l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if not f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l11llll1ll_opy_, False):
            self.__1l11l11ll1l_opy_(f,instance,bstack1llll1ll1l1_opy_)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll11l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        if not f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l11llll1ll_opy_, False):
            self.__1l11l11ll1l_opy_(f, instance, bstack1llll1ll1l1_opy_)
        if not f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l11111ll_opy_, False):
            self.__1l11l11llll_opy_(f, instance, bstack1llll1ll1l1_opy_)
    def bstack1l11l1l111l_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1llll11ll_opy_(instance):
            return
        if f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l11111ll_opy_, False):
            return
        driver.execute_script(
            bstack1ll11ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᏊ").format(
                json.dumps(
                    {
                        bstack1ll11ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᏋ"): bstack1ll11ll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᏌ"),
                        bstack1ll11ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᏍ"): {bstack1ll11ll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᏎ"): result},
                    }
                )
            )
        )
        f.bstack1llll1l1lll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l11111ll_opy_, True)
    def bstack1l11l1l1ll1_opy_(self, context: bstack1llllll111l_opy_, bstack1l11l1l11ll_opy_= True):
        if bstack1l11l1l11ll_opy_:
            bstack1l1lll111ll_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        else:
            bstack1l1lll111ll_opy_ = self.bstack1l1llll1lll_opy_(context, reverse=True)
        return [f for f in bstack1l1lll111ll_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1111ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1l11l11llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᏏ")).get(bstack1ll11ll_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᏐ")):
            bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
            if not bstack1l1lll111ll_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᏑ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠨࠢᏒ"))
                return
            driver = bstack1l1lll111ll_opy_[0][0]()
            status = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1l11111l1_opy_, None)
            if not status:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᏓ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤᏔ"))
                return
            bstack1l1l1111l11_opy_ = {bstack1ll11ll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᏕ"): status.lower()}
            bstack1l11llll11l_opy_ = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1l111111l_opy_, None)
            if status.lower() == bstack1ll11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᏖ") and bstack1l11llll11l_opy_ is not None:
                bstack1l1l1111l11_opy_[bstack1ll11ll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᏗ")] = bstack1l11llll11l_opy_[0][bstack1ll11ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᏘ")][0] if isinstance(bstack1l11llll11l_opy_, list) else str(bstack1l11llll11l_opy_)
            driver.execute_script(
                bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᏙ").format(
                    json.dumps(
                        {
                            bstack1ll11ll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᏚ"): bstack1ll11ll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᏛ"),
                            bstack1ll11ll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᏜ"): bstack1l1l1111l11_opy_,
                        }
                    )
                )
            )
            f.bstack1llll1l1lll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l11111ll_opy_, True)
    @measure(event_name=EVENTS.bstack1ll111ll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1l11l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᏝ")).get(bstack1ll11ll_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᏞ")):
            test_name = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᏟ"))
                return
            bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
            if not bstack1l1lll111ll_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᏠ") + str(bstack1llll1ll1l1_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣᏡ"))
                return
            for bstack1l1l11lll11_opy_, bstack1l11l1ll111_opy_ in bstack1l1lll111ll_opy_:
                if not bstack1ll1l1ll111_opy_.bstack1l1llll11ll_opy_(bstack1l11l1ll111_opy_):
                    continue
                driver = bstack1l1l11lll11_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll11ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᏢ").format(
                        json.dumps(
                            {
                                bstack1ll11ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᏣ"): bstack1ll11ll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᏤ"),
                                bstack1ll11ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᏥ"): {bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏦ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llll1l1lll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l11llll1ll_opy_, True)
    def bstack1l1l1llll11_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        f: TestFramework,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll11l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        bstack1l1lll111ll_opy_ = [d for d, _ in f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])]
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᏧ"))
            return
        if not bstack1l1l1lll111_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᏨ"))
            return
        for bstack1l11l11lll1_opy_ in bstack1l1lll111ll_opy_:
            driver = bstack1l11l11lll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll11ll_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨᏩ") + str(timestamp)
            driver.execute_script(
                bstack1ll11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᏪ").format(
                    json.dumps(
                        {
                            bstack1ll11ll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᏫ"): bstack1ll11ll_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨᏬ"),
                            bstack1ll11ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᏭ"): {
                                bstack1ll11ll_opy_ (u"ࠨࡴࡺࡲࡨࠦᏮ"): bstack1ll11ll_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦᏯ"),
                                bstack1ll11ll_opy_ (u"ࠣࡦࡤࡸࡦࠨᏰ"): data,
                                bstack1ll11ll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣᏱ"): bstack1ll11ll_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤᏲ")
                            }
                        }
                    )
                )
            )
    def bstack1l1l1ll111l_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        f: TestFramework,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll11l_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        keys = [
            bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_,
            bstack1lll1111ll1_opy_.bstack1l1l1111lll_opy_,
        ]
        bstack1l1lll111ll_opy_ = []
        for key in keys:
            bstack1l1lll111ll_opy_.extend(f.bstack1llll1lllll_opy_(instance, key, []))
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡ࡯ࡻࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᏳ"))
            return
        if f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll1111l_opy_, False):
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡃࡃࡖࠣࡥࡱࡸࡥࡢࡦࡼࠤࡨࡸࡥࡢࡶࡨࡨࠧᏴ"))
            return
        self.bstack1ll11l11lll_opy_()
        bstack1ll111l11_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll1111lll1_opy_)
        req.test_framework_name = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11ll111l_opy_)
        req.test_framework_version = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1ll1l1111_opy_)
        req.test_framework_state = bstack1llll1ll1l1_opy_[0].name
        req.test_hook_state = bstack1llll1ll1l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
        for bstack1l1l11lll11_opy_, driver in bstack1l1lll111ll_opy_:
            try:
                webdriver = bstack1l1l11lll11_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᏵ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1ll11ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨ᏶")
                    if bstack1ll1l1ll111_opy_.bstack1llll1lllll_opy_(driver, bstack1ll1l1ll111_opy_.bstack1l11l1l1l1l_opy_, False)
                    else bstack1ll11ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢ᏷")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1ll1l1ll111_opy_.bstack1llll1lllll_opy_(driver, bstack1ll1l1ll111_opy_.bstack1l1l11l1ll1_opy_, bstack1ll11ll_opy_ (u"ࠤࠥᏸ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1ll1l1ll111_opy_.bstack1llll1lllll_opy_(driver, bstack1ll1l1ll111_opy_.bstack1l1l111l111_opy_, bstack1ll11ll_opy_ (u"ࠥࠦᏹ"))
                caps = None
                if hasattr(webdriver, bstack1ll11ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᏺ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1ll11ll_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᏻ"))
                    except Exception as e:
                        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᏼ") + str(e) + bstack1ll11ll_opy_ (u"ࠢࠣᏽ"))
                try:
                    bstack1l11l1l1111_opy_ = json.dumps(caps).encode(bstack1ll11ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᏾")) if caps else bstack1l11l1l1lll_opy_ (u"ࠤࡾࢁࠧ᏿")
                    req.capabilities = bstack1l11l1l1111_opy_
                except Exception as e:
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨ᐀") + str(e) + bstack1ll11ll_opy_ (u"ࠦࠧᐁ"))
            except Exception as e:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᐂ") + str(str(e)) + bstack1ll11ll_opy_ (u"ࠨࠢᐃ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l1l1lll111_opy_() and len(bstack1l1lll111ll_opy_) == 0:
            bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l1111lll_opy_, [])
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐄ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠣࠤᐅ"))
            return {}
        if len(bstack1l1lll111ll_opy_) > 1:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐆ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠥࠦᐇ"))
            return {}
        bstack1l1l11lll11_opy_, bstack1l1l11lllll_opy_ = bstack1l1lll111ll_opy_[0]
        driver = bstack1l1l11lll11_opy_()
        if not driver:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐈ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠧࠨᐉ"))
            return {}
        capabilities = f.bstack1llll1lllll_opy_(bstack1l1l11lllll_opy_, bstack1ll1l1ll111_opy_.bstack1l1l11ll111_opy_)
        if not capabilities:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐊ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣᐋ"))
            return {}
        return capabilities.get(bstack1ll11ll_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᐌ"), {})
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l1l1lll111_opy_() and len(bstack1l1lll111ll_opy_) == 0:
            bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1l1111lll_opy_, [])
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐍ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠥࠦᐎ"))
            return
        if len(bstack1l1lll111ll_opy_) > 1:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐏ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠧࠨᐐ"))
        bstack1l1l11lll11_opy_, bstack1l1l11lllll_opy_ = bstack1l1lll111ll_opy_[0]
        driver = bstack1l1l11lll11_opy_()
        if not driver:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐑ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣᐒ"))
            return
        return driver