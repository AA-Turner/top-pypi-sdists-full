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
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1lll1llll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_, bstack1ll11111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll1l1111l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11llll111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll11l1llll_opy_(bstack1lll1l1111l_opy_):
    bstack1l111ll1l1l_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦᓛ")
    bstack1l1l11l1111_opy_ = bstack11lllll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᓜ")
    bstack1l111l1l111_opy_ = bstack11lllll_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᓝ")
    bstack1l111ll11ll_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᓞ")
    bstack1l111ll1ll1_opy_ = bstack11lllll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨᓟ")
    bstack1l11l1ll111_opy_ = bstack11lllll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᓠ")
    bstack1l111l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᓡ")
    bstack1l111l1llll_opy_ = bstack11lllll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥᓢ")
    def __init__(self):
        super().__init__(bstack1llll111111_opy_=self.bstack1l111ll1l1l_opy_, frameworks=[bstack1lll11lllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.BEFORE_EACH, bstack1ll11l1l11l_opy_.POST), self.bstack11lllll1lll_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.PRE), self.bstack1l1lll1111l_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1l1l1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lllll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l11ll111_opy_ = self.bstack11llllll1l1_opy_(instance.context)
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᓣ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠢࠣᓤ"))
        f.bstack1lll1ll1lll_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, bstack1l1l11ll111_opy_)
        bstack11llllll11l_opy_ = self.bstack11llllll1l1_opy_(instance.context, bstack1l1111111ll_opy_=False)
        f.bstack1lll1ll1lll_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l111_opy_, bstack11llllll11l_opy_)
    def bstack1l1lll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if not f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l1l1_opy_, False):
            self.__11lllllllll_opy_(f,instance,bstack1lll1l11lll_opy_)
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        if not f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l1l1_opy_, False):
            self.__11lllllllll_opy_(f, instance, bstack1lll1l11lll_opy_)
        if not f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1llll_opy_, False):
            self.__1l1111111l1_opy_(f, instance, bstack1lll1l11lll_opy_)
    def bstack1l11111111l_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1lll1l1llll_opy_(instance):
            return
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1llll_opy_, False):
            return
        driver.execute_script(
            bstack11lllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᓥ").format(
                json.dumps(
                    {
                        bstack11lllll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᓦ"): bstack11lllll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᓧ"),
                        bstack11lllll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᓨ"): {bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᓩ"): result},
                    }
                )
            )
        )
        f.bstack1lll1ll1lll_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1llll_opy_, True)
    def bstack11llllll1l1_opy_(self, context: bstack1lll1llll1l_opy_, bstack1l1111111ll_opy_= True):
        if bstack1l1111111ll_opy_:
            bstack1l1l11ll111_opy_ = self.bstack1lll1llll11_opy_(context, reverse=True)
        else:
            bstack1l1l11ll111_opy_ = self.bstack1lll1ll1l11_opy_(context, reverse=True)
        return [f for f in bstack1l1l11ll111_opy_ if f[1].state != bstack1lll1l1ll1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1l1111111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᓪ")).get(bstack11lllll_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᓫ")):
            bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
            if not bstack1l1l11ll111_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᓬ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠤࠥᓭ"))
                return
            for bstack1l11l1l1lll_opy_, _ in bstack1l1l11ll111_opy_:
                driver = bstack1l11l1l1lll_opy_()
                status = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, None)
                if not status:
                    self.logger.debug(bstack11lllll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᓮ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠦࠧᓯ"))
                    return
                bstack1l111ll1l11_opy_ = {bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᓰ"): status.lower()}
                bstack1l111ll111l_opy_ = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l111ll1111_opy_, None)
                if status.lower() == bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᓱ") and bstack1l111ll111l_opy_ is not None:
                    bstack1l111ll1l11_opy_[bstack11lllll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᓲ")] = bstack1l111ll111l_opy_[0][bstack11lllll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᓳ")][0] if isinstance(bstack1l111ll111l_opy_, list) else str(bstack1l111ll111l_opy_)
                driver.execute_script(
                    bstack11lllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᓴ").format(
                        json.dumps(
                            {
                                bstack11lllll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᓵ"): bstack11lllll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᓶ"),
                                bstack11lllll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᓷ"): bstack1l111ll1l11_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll1ll1lll_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1llll_opy_, True)
    @measure(event_name=EVENTS.bstack11ll11l11_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __11lllllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᓸ")).get(bstack11lllll_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᓹ")):
            test_name = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11lllllll11_opy_, None)
            if not test_name:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᓺ"))
                return
            bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
            if not bstack1l1l11ll111_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᓻ") + str(bstack1lll1l11lll_opy_) + bstack11lllll_opy_ (u"ࠥࠦᓼ"))
                return
            for bstack1l11l1l1lll_opy_, bstack11lllllll1l_opy_ in bstack1l1l11ll111_opy_:
                if not bstack1lll11lllll_opy_.bstack1lll1l1llll_opy_(bstack11lllllll1l_opy_):
                    continue
                driver = bstack1l11l1l1lll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᓽ").format(
                        json.dumps(
                            {
                                bstack11lllll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᓾ"): bstack11lllll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᓿ"),
                                bstack11lllll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᔀ"): {bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᔁ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll1ll1lll_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l1l1_opy_, True)
    def bstack1l11ll11111_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        f: TestFramework,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        bstack1l1l11ll111_opy_ = [d for d, _ in f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])]
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᔂ"))
            return
        if not bstack1l11llll111_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᔃ"))
            return
        for bstack1l111111l11_opy_ in bstack1l1l11ll111_opy_:
            driver = bstack1l111111l11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11lllll_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤᔄ") + str(timestamp)
            driver.execute_script(
                bstack11lllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᔅ").format(
                    json.dumps(
                        {
                            bstack11lllll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᔆ"): bstack11lllll_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤᔇ"),
                            bstack11lllll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᔈ"): {
                                bstack11lllll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᔉ"): bstack11lllll_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢᔊ"),
                                bstack11lllll_opy_ (u"ࠦࡩࡧࡴࡢࠤᔋ"): data,
                                bstack11lllll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦᔌ"): bstack11lllll_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧᔍ")
                            }
                        }
                    )
                )
            )
    def bstack1l11ll111ll_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        f: TestFramework,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lllll1lll_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        keys = [
            bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_,
            bstack1ll11l1llll_opy_.bstack1l111l1l111_opy_,
        ]
        bstack1l1l11ll111_opy_ = []
        for key in keys:
            bstack1l1l11ll111_opy_.extend(f.bstack1lll1l1l111_opy_(instance, key, []))
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡲࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᔎ"))
            return
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l11l1ll111_opy_, False):
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡆࡆ࡙ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡤࡴࡨࡥࡹ࡫ࡤࠣᔏ"))
            return
        self.bstack1l1ll1l11ll_opy_()
        bstack1l1111l111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᔐ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1ll111ll1_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        req.test_framework_state = bstack1lll1l11lll_opy_[0].name
        req.test_hook_state = bstack1lll1l11lll_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        for bstack1l11l1l1lll_opy_, driver in bstack1l1l11ll111_opy_:
            bstack1lll1l111ll_opy_ = driver.data.get(bstack11lllll_opy_ (u"ࠥࡶࡦࡴ࡫ࠣᔑ"))
            bstack11llllllll1_opy_ = False
            if bstack1lll1l111ll_opy_ is None:
                bstack11llllllll1_opy_ = True
            else:
                try:
                    bstack11llllllll1_opy_ = int(bstack1lll1l111ll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11llllllll1_opy_ = False
            if bstack11llllllll1_opy_:
                try:
                    webdriver = bstack1l11l1l1lll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11lllll_opy_ (u"ࠦ࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࠬࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࠠࡦࡺࡳ࡭ࡷ࡫ࡤࠪࠤᔒ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11lllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᔓ")
                        if bstack1lll11lllll_opy_.bstack1lll1l1l111_opy_(driver, bstack1lll11lllll_opy_.bstack1l111111111_opy_, False)
                        else bstack11lllll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᔔ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1lll11lllll_opy_.bstack1lll1l1l111_opy_(driver, bstack1lll11lllll_opy_.bstack1l111lll111_opy_, bstack11lllll_opy_ (u"ࠢࠣᔕ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1lll11lllll_opy_.bstack1lll1l1l111_opy_(driver, bstack1lll11lllll_opy_.bstack1l111llll11_opy_, bstack11lllll_opy_ (u"ࠣࠤᔖ"))
                    caps = None
                    if hasattr(webdriver, bstack11lllll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᔗ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡩ࡯ࡲࡦࡥࡷࡰࡾࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᔘ"))
                        except Exception as e:
                            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࠤᔙ") + str(e) + bstack11lllll_opy_ (u"ࠧࠨᔚ"))
                    try:
                        bstack11llllll111_opy_ = json.dumps(caps).encode(bstack11lllll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᔛ")) if caps else bstack11llllll1ll_opy_ (u"ࠢࡼࡿࠥᔜ")
                        req.capabilities = bstack11llllll111_opy_
                    except Exception as e:
                        self.logger.debug(bstack11lllll_opy_ (u"ࠣࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡷࡪࡸࡩࡢ࡮࡬ࡾࡪࠦࡣࡢࡲࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࠦᔝ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥᔞ"))
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩࡵࡧࡰ࠾ࠥࠨᔟ") + str(str(e)) + bstack11lllll_opy_ (u"ࠦࠧᔠ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l11llll111_opy_() and len(bstack1l1l11ll111_opy_) == 0:
            bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l111_opy_, [])
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔡ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᔢ"))
            return {}
        for bstack1l11l1l1lll_opy_, bstack1l11l11l1ll_opy_ in bstack1l1l11ll111_opy_:
            bstack1lll1l111ll_opy_ = bstack1l11l11l1ll_opy_.data.get(bstack11lllll_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᔣ"))
            self.logger.info(bstack11lllll_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡴࡤࡲࡰࡀࠠࠣᔤ") + str(bstack1lll1l111ll_opy_) + bstack11lllll_opy_ (u"ࠤࠥᔥ"))
            if bstack1lll1l111ll_opy_ is None or bstack1lll1l111ll_opy_ == bstack11lllll_opy_ (u"ࠪ࠵ࠬᔦ"):
                driver = bstack1l11l1l1lll_opy_()
                self.logger.debug(bstack11lllll_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡩࡩࡹࡩࡨࡦࡦࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࠧᔧ") + str(bstack1l11l11l1ll_opy_.data[bstack11lllll_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᔨ")]) + bstack11lllll_opy_ (u"ࠨࠢᔩ"))
                if not driver:
                    self.logger.debug(bstack11lllll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔪ") + str(kwargs) + bstack11lllll_opy_ (u"ࠣࠤᔫ"))
                    return {}
                capabilities = f.bstack1lll1l1l111_opy_(bstack1l11l11l1ll_opy_, bstack1lll11lllll_opy_.bstack1l11l1111ll_opy_)
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࠣᔬ") + str(capabilities) + bstack11lllll_opy_ (u"ࠥࠦᔭ"))
                if not capabilities:
                    self.logger.debug(bstack11lllll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᔮ") + str(kwargs) + bstack11lllll_opy_ (u"ࠧࠨᔯ"))
                    return {}
                return capabilities.get(bstack11lllll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦᔰ"), {})
        return None
    def bstack1l1ll11l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l11llll111_opy_() and len(bstack1l1l11ll111_opy_) == 0:
            bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l111l1l111_opy_, [])
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔱ") + str(kwargs) + bstack11lllll_opy_ (u"ࠣࠤᔲ"))
            return
        if len(bstack1l1l11ll111_opy_) > 1:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᔳ") + str(kwargs) + bstack11lllll_opy_ (u"ࠥࠦᔴ"))
        for bstack1l11l1l1lll_opy_, bstack1l11l11l1ll_opy_ in bstack1l1l11ll111_opy_:
            driver = bstack1l11l1l1lll_opy_()
            bstack1lll1l111ll_opy_ = bstack1l11l11l1ll_opy_.data.get(bstack11lllll_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᔵ"))
            self.logger.info(bstack11lllll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡴࡤࡲࡰࡀࠠࠣᔶ") + str(bstack1lll1l111ll_opy_) + bstack11lllll_opy_ (u"ࠨࠢᔷ"))
            if (bstack1lll1l111ll_opy_ is None or int(bstack1lll1l111ll_opy_) == 1) and driver:
                return driver
        return None