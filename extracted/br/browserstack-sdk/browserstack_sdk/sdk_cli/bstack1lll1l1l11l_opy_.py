# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll111l_opy_,
    bstack1lllllll111_opy_,
    bstack1lllll1l1l1_opy_,
    bstack1111111111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_, bstack1ll1lll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1ll_opy_ import bstack1l1lllll111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1lllll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1ll1lll_opy_(bstack1l1lllll111_opy_):
    bstack1l1l1111ll1_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᎭ")
    bstack1l1ll1l1l1l_opy_ = bstack1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᎮ")
    bstack1l11lllll1l_opy_ = bstack1l1_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᎯ")
    bstack1l1l111ll1l_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᎰ")
    bstack1l1l111ll11_opy_ = bstack1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᎱ")
    bstack1l1ll1l1ll1_opy_ = bstack1l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᎲ")
    bstack1l1l1111l1l_opy_ = bstack1l1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᎳ")
    bstack1l1l1111111_opy_ = bstack1l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᎴ")
    def __init__(self):
        super().__init__(bstack1l1llllll11_opy_=self.bstack1l1l1111ll1_opy_, frameworks=[bstack1ll1ll111l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111lllll_opy_((bstack1lll11ll1l1_opy_.BEFORE_EACH, bstack1ll1lll1111_opy_.POST), self.bstack1l11l1l1ll1_opy_)
        TestFramework.bstack1ll111lllll_opy_((bstack1lll11ll1l1_opy_.TEST, bstack1ll1lll1111_opy_.PRE), self.bstack1ll11l11l1l_opy_)
        TestFramework.bstack1ll111lllll_opy_((bstack1lll11ll1l1_opy_.TEST, bstack1ll1lll1111_opy_.POST), self.bstack1ll1l11l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1ll111_opy_ = self.bstack1l11ll11111_opy_(instance.context)
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᎵ") + str(bstack1111111l1l_opy_) + bstack1l1_opy_ (u"ࠨࠢᎶ"))
        f.bstack1llll1ll1ll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, bstack1l1ll1ll111_opy_)
        bstack1l11l1ll1ll_opy_ = self.bstack1l11ll11111_opy_(instance.context, bstack1l11l1ll111_opy_=False)
        f.bstack1llll1ll1ll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l11lllll1l_opy_, bstack1l11l1ll1ll_opy_)
    def bstack1ll11l11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1111111l1l_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111l1l_opy_, False):
            self.__1l11l1l1l11_opy_(f,instance,bstack1111111l1l_opy_)
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1111111l1l_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111l1l_opy_, False):
            self.__1l11l1l1l11_opy_(f, instance, bstack1111111l1l_opy_)
        if not f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111111_opy_, False):
            self.__1l11l1lllll_opy_(f, instance, bstack1111111l1l_opy_)
    def bstack1l11l1llll1_opy_(
        self,
        f: bstack1ll1ll111l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1l1l1_opy_, str],
        bstack1111111l1l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1llll1ll1_opy_(instance):
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111111_opy_, False):
            return
        driver.execute_script(
            bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᎷ").format(
                json.dumps(
                    {
                        bstack1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᎸ"): bstack1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᎹ"),
                        bstack1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᎺ"): {bstack1l1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᎻ"): result},
                    }
                )
            )
        )
        f.bstack1llll1ll1ll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111111_opy_, True)
    def bstack1l11ll11111_opy_(self, context: bstack1111111111_opy_, bstack1l11l1ll111_opy_= True):
        if bstack1l11l1ll111_opy_:
            bstack1l1ll1ll111_opy_ = self.bstack1l1llll11ll_opy_(context, reverse=True)
        else:
            bstack1l1ll1ll111_opy_ = self.bstack1l1llllll1l_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1ll111_opy_ if f[1].state != bstack1lllll1ll11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l1l1l1_opy_, stage=STAGE.bstack11lllll1_opy_)
    def __1l11l1lllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᎼ")).get(bstack1l1_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᎽ")):
            bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, [])
            if not bstack1l1ll1ll111_opy_:
                self.logger.debug(bstack1l1_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᎾ") + str(bstack1111111l1l_opy_) + bstack1l1_opy_ (u"ࠣࠤᎿ"))
                return
            driver = bstack1l1ll1ll111_opy_[0][0]()
            status = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l11llllll1_opy_, None)
            if not status:
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᏀ") + str(bstack1111111l1l_opy_) + bstack1l1_opy_ (u"ࠥࠦᏁ"))
                return
            bstack1l1l11111l1_opy_ = {bstack1l1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᏂ"): status.lower()}
            bstack1l1l11111ll_opy_ = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l111l1l1_opy_, None)
            if status.lower() == bstack1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏃ") and bstack1l1l11111ll_opy_ is not None:
                bstack1l1l11111l1_opy_[bstack1l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭Ꮔ")] = bstack1l1l11111ll_opy_[0][bstack1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᏅ")][0] if isinstance(bstack1l1l11111ll_opy_, list) else str(bstack1l1l11111ll_opy_)
            driver.execute_script(
                bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᏆ").format(
                    json.dumps(
                        {
                            bstack1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᏇ"): bstack1l1_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᏈ"),
                            bstack1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᏉ"): bstack1l1l11111l1_opy_,
                        }
                    )
                )
            )
            f.bstack1llll1ll1ll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111111_opy_, True)
    @measure(event_name=EVENTS.bstack1lllll1l1_opy_, stage=STAGE.bstack11lllll1_opy_)
    def __1l11l1l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᏊ")).get(bstack1l1_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᏋ")):
            test_name = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᏌ"))
                return
            bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, [])
            if not bstack1l1ll1ll111_opy_:
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᏍ") + str(bstack1111111l1l_opy_) + bstack1l1_opy_ (u"ࠤࠥᏎ"))
                return
            for bstack1l1l1l1ll1l_opy_, bstack1l11l1l1l1l_opy_ in bstack1l1ll1ll111_opy_:
                if not bstack1ll1ll111l1_opy_.bstack1l1llll1ll1_opy_(bstack1l11l1l1l1l_opy_):
                    continue
                driver = bstack1l1l1l1ll1l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᏏ").format(
                        json.dumps(
                            {
                                bstack1l1_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᏐ"): bstack1l1_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᏑ"),
                                bstack1l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᏒ"): {bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏓ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llll1ll1ll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1l1111l1l_opy_, True)
    def bstack1l1l1lll111_opy_(
        self,
        instance: bstack1ll1lll11ll_opy_,
        f: TestFramework,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1111111l1l_opy_, *args, **kwargs)
        bstack1l1ll1ll111_opy_ = [d for d, _ in f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, [])]
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᏔ"))
            return
        if not bstack1l1ll1lllll_opy_():
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏕ"))
            return
        for bstack1l11l1lll11_opy_ in bstack1l1ll1ll111_opy_:
            driver = bstack1l11l1lll11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣᏖ") + str(timestamp)
            driver.execute_script(
                bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᏗ").format(
                    json.dumps(
                        {
                            bstack1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᏘ"): bstack1l1_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᏙ"),
                            bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᏚ"): {
                                bstack1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨᏛ"): bstack1l1_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᏜ"),
                                bstack1l1_opy_ (u"ࠥࡨࡦࡺࡡࠣᏝ"): data,
                                bstack1l1_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᏞ"): bstack1l1_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᏟ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll11l1l_opy_(
        self,
        instance: bstack1ll1lll11ll_opy_,
        f: TestFramework,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1l1ll1_opy_(f, instance, bstack1111111l1l_opy_, *args, **kwargs)
        keys = [
            bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_,
            bstack1lll1ll1lll_opy_.bstack1l11lllll1l_opy_,
        ]
        bstack1l1ll1ll111_opy_ = []
        for key in keys:
            bstack1l1ll1ll111_opy_.extend(f.bstack1lllll1l11l_opy_(instance, key, []))
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᏠ"))
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1ll1_opy_, False):
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢᏡ"))
            return
        self.bstack1ll1l111ll1_opy_()
        bstack111l1lll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll11l111ll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111l11l1_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_)
        req.test_framework_state = bstack1111111l1l_opy_[0].name
        req.test_hook_state = bstack1111111l1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_)
        for bstack1l1l1l1ll1l_opy_, driver in bstack1l1ll1ll111_opy_:
            try:
                webdriver = bstack1l1l1l1ll1l_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1l1_opy_ (u"࡙ࠣࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࠩࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠤࡪࡾࡰࡪࡴࡨࡨ࠮ࠨᏢ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣᏣ")
                    if bstack1ll1ll111l1_opy_.bstack1lllll1l11l_opy_(driver, bstack1ll1ll111l1_opy_.bstack1l11l1ll1l1_opy_, False)
                    else bstack1l1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤᏤ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1ll1ll111l1_opy_.bstack1lllll1l11l_opy_(driver, bstack1ll1ll111l1_opy_.bstack1l1l11l1ll1_opy_, bstack1l1_opy_ (u"ࠦࠧᏥ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1ll1ll111l1_opy_.bstack1lllll1l11l_opy_(driver, bstack1ll1ll111l1_opy_.bstack1l1l11l11ll_opy_, bstack1l1_opy_ (u"ࠧࠨᏦ"))
                caps = None
                if hasattr(webdriver, bstack1l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᏧ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1l1_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡦ࡬ࡶࡪࡩࡴ࡭ࡻࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᏨ"))
                    except Exception as e:
                        self.logger.debug(bstack1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᏩ") + str(e) + bstack1l1_opy_ (u"ࠤࠥᏪ"))
                try:
                    bstack1l11l1ll11l_opy_ = json.dumps(caps).encode(bstack1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᏫ")) if caps else bstack1l11l1l1lll_opy_ (u"ࠦࢀࢃࠢᏬ")
                    req.capabilities = bstack1l11l1ll11l_opy_
                except Exception as e:
                    self.logger.debug(bstack1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡧࡵ࡭ࡦࡲࡩࡻࡧࠣࡧࡦࡶࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࠣᏭ") + str(e) + bstack1l1_opy_ (u"ࠨࠢᏮ"))
            except Exception as e:
                self.logger.error(bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡹ࡫࡭࠻ࠢࠥᏯ") + str(str(e)) + bstack1l1_opy_ (u"ࠣࠤᏰ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, [])
        if not bstack1l1ll1lllll_opy_() and len(bstack1l1ll1ll111_opy_) == 0:
            bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l11lllll1l_opy_, [])
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏱ") + str(kwargs) + bstack1l1_opy_ (u"ࠥࠦᏲ"))
            return {}
        if len(bstack1l1ll1ll111_opy_) > 1:
            self.logger.debug(bstack1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏳ") + str(kwargs) + bstack1l1_opy_ (u"ࠧࠨᏴ"))
            return {}
        bstack1l1l1l1ll1l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1ll1ll111_opy_[0]
        driver = bstack1l1l1l1ll1l_opy_()
        if not driver:
            self.logger.debug(bstack1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏵ") + str(kwargs) + bstack1l1_opy_ (u"ࠢࠣ᏶"))
            return {}
        capabilities = f.bstack1lllll1l11l_opy_(bstack1l1l1l1l111_opy_, bstack1ll1ll111l1_opy_.bstack1l1l11l1l1l_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᏷") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥᏸ"))
            return {}
        return capabilities.get(bstack1l1_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᏹ"), {})
    def bstack1ll1111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll11ll_opy_,
        bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1ll1l1l1l_opy_, [])
        if not bstack1l1ll1lllll_opy_() and len(bstack1l1ll1ll111_opy_) == 0:
            bstack1l1ll1ll111_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l11lllll1l_opy_, [])
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏺ") + str(kwargs) + bstack1l1_opy_ (u"ࠧࠨᏻ"))
            return
        if len(bstack1l1ll1ll111_opy_) > 1:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᏼ") + str(kwargs) + bstack1l1_opy_ (u"ࠢࠣᏽ"))
        bstack1l1l1l1ll1l_opy_, bstack1l1l1l1l111_opy_ = bstack1l1ll1ll111_opy_[0]
        driver = bstack1l1l1l1ll1l_opy_()
        if not driver:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᏾") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥ᏿"))
            return
        return driver