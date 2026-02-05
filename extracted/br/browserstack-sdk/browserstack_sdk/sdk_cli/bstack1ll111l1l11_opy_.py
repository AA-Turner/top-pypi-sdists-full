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
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll111llll_opy_,
    bstack1lll11lll1l_opy_,
    bstack1lll1lll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_, bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l1l1l1111l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1111ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1l11l11l_opy_(bstack1l1l1l1111l_opy_):
    bstack1l111l11lll_opy_ = bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᓄ")
    bstack1l1l11l111l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᓅ")
    bstack1l111ll11l1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᓆ")
    bstack1l111ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᓇ")
    bstack1l111lll111_opy_ = bstack11l1ll1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᓈ")
    bstack1l1l1111l11_opy_ = bstack11l1ll1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᓉ")
    bstack1l111l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᓊ")
    bstack1l111ll11ll_opy_ = bstack11l1ll1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᓋ")
    def __init__(self):
        super().__init__(bstack1l1l1l11l11_opy_=self.bstack1l111l11lll_opy_, frameworks=[bstack1ll1ll1lll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.BEFORE_EACH, bstack1ll1111llll_opy_.POST), self.bstack1l11111111l_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1llll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l111111l_opy_ = self.bstack1l11111l1l1_opy_(instance.context)
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᓌ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠧࠨᓍ"))
        f.bstack1lll1l1111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, bstack1l1l111111l_opy_)
        bstack1l111111lll_opy_ = self.bstack1l11111l1l1_opy_(instance.context, bstack1l1111111ll_opy_=False)
        f.bstack1lll1l1111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11l1_opy_, bstack1l111111lll_opy_)
    def bstack1l1ll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11111111l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if not f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111l1l1ll_opy_, False):
            self.__1l111111l1l_opy_(f,instance,bstack1lll1l1ll11_opy_)
    def bstack1l1llll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11111111l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        if not f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111l1l1ll_opy_, False):
            self.__1l111111l1l_opy_(f, instance, bstack1lll1l1ll11_opy_)
        if not f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11ll_opy_, False):
            self.__1l11111l11l_opy_(f, instance, bstack1lll1l1ll11_opy_)
    def bstack1l11111l111_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1l1l11ll1_opy_(instance):
            return
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11ll_opy_, False):
            return
        driver.execute_script(
            bstack11l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᓎ").format(
                json.dumps(
                    {
                        bstack11l1ll1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᓏ"): bstack11l1ll1_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᓐ"),
                        bstack11l1ll1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᓑ"): {bstack11l1ll1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᓒ"): result},
                    }
                )
            )
        )
        f.bstack1lll1l1111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11ll_opy_, True)
    def bstack1l11111l1l1_opy_(self, context: bstack1lll1lll11l_opy_, bstack1l1111111ll_opy_= True):
        if bstack1l1111111ll_opy_:
            bstack1l1l111111l_opy_ = self.bstack1l1l1l1l111_opy_(context, reverse=True)
        else:
            bstack1l1l111111l_opy_ = self.bstack1l1l1l1l1ll_opy_(context, reverse=True)
        return [f for f in bstack1l1l111111l_opy_ if f[1].state != bstack1lll111lll1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1l11111l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᓓ")).get(bstack11l1ll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᓔ")):
            bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
            if not bstack1l1l111111l_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᓕ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠢࠣᓖ"))
                return
            driver = bstack1l1l111111l_opy_[0][0]()
            status = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, None)
            if not status:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᓗ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠤࠥᓘ"))
                return
            bstack1l111ll1lll_opy_ = {bstack11l1ll1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᓙ"): status.lower()}
            bstack1l111ll1l1l_opy_ = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l111ll111l_opy_, None)
            if status.lower() == bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᓚ") and bstack1l111ll1l1l_opy_ is not None:
                bstack1l111ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᓛ")] = bstack1l111ll1l1l_opy_[0][bstack11l1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᓜ")][0] if isinstance(bstack1l111ll1l1l_opy_, list) else str(bstack1l111ll1l1l_opy_)
            driver.execute_script(
                bstack11l1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᓝ").format(
                    json.dumps(
                        {
                            bstack11l1ll1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᓞ"): bstack11l1ll1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᓟ"),
                            bstack11l1ll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᓠ"): bstack1l111ll1lll_opy_,
                        }
                    )
                )
            )
            f.bstack1lll1l1111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11ll_opy_, True)
    @measure(event_name=EVENTS.bstack1l11l11l1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1l111111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᓡ")).get(bstack11l1ll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᓢ")):
            test_name = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l111111111_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᓣ"))
                return
            bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
            if not bstack1l1l111111l_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᓤ") + str(bstack1lll1l1ll11_opy_) + bstack11l1ll1_opy_ (u"ࠣࠤᓥ"))
                return
            for bstack1l11l1l1ll1_opy_, bstack1l1111111l1_opy_ in bstack1l1l111111l_opy_:
                if not bstack1ll1ll1lll1_opy_.bstack1l1l1l11ll1_opy_(bstack1l1111111l1_opy_):
                    continue
                driver = bstack1l11l1l1ll1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᓦ").format(
                        json.dumps(
                            {
                                bstack11l1ll1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᓧ"): bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᓨ"),
                                bstack11l1ll1_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᓩ"): {bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓪ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll1l1111l_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111l1l1ll_opy_, True)
    def bstack1l1l1111l1l_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        f: TestFramework,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11111111l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        bstack1l1l111111l_opy_ = [d for d, _ in f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])]
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᓫ"))
            return
        if not bstack1l1l1111ll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᓬ"))
            return
        for bstack1l111111ll1_opy_ in bstack1l1l111111l_opy_:
            driver = bstack1l111111ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1ll1_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᓭ") + str(timestamp)
            driver.execute_script(
                bstack11l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᓮ").format(
                    json.dumps(
                        {
                            bstack11l1ll1_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᓯ"): bstack11l1ll1_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢᓰ"),
                            bstack11l1ll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᓱ"): {
                                bstack11l1ll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᓲ"): bstack11l1ll1_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧᓳ"),
                                bstack11l1ll1_opy_ (u"ࠤࡧࡥࡹࡧࠢᓴ"): data,
                                bstack11l1ll1_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᓵ"): bstack11l1ll1_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᓶ")
                            }
                        }
                    )
                )
            )
    def bstack1l11ll111l1_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        f: TestFramework,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11111111l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        keys = [
            bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_,
            bstack1ll1l11l11l_opy_.bstack1l111ll11l1_opy_,
        ]
        bstack1l1l111111l_opy_ = []
        for key in keys:
            bstack1l1l111111l_opy_.extend(f.bstack1lll1ll11l1_opy_(instance, key, []))
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᓷ"))
            return
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l1111l11_opy_, False):
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨᓸ"))
            return
        self.bstack1l1lll1ll1l_opy_()
        bstack111ll1ll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᓹ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llllll11_opy_)
        req.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l111llll_opy_)
        req.test_framework_state = bstack1lll1l1ll11_opy_[0].name
        req.test_hook_state = bstack1lll1l1ll11_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
        for bstack1l11l1l1ll1_opy_, driver in bstack1l1l111111l_opy_:
            try:
                webdriver = bstack1l11l1l1ll1_opy_()
                if webdriver is None:
                    self.logger.debug(bstack11l1ll1_opy_ (u"࡙ࠣࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࠩࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠤࡪࡾࡰࡪࡴࡨࡨ࠮ࠨᓺ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣᓻ")
                    if bstack1ll1ll1lll1_opy_.bstack1lll1ll11l1_opy_(driver, bstack1ll1ll1lll1_opy_.bstack1l111111l11_opy_, False)
                    else bstack11l1ll1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤᓼ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1ll1ll1lll1_opy_.bstack1lll1ll11l1_opy_(driver, bstack1ll1ll1lll1_opy_.bstack1l111llll11_opy_, bstack11l1ll1_opy_ (u"ࠦࠧᓽ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1ll1ll1lll1_opy_.bstack1lll1ll11l1_opy_(driver, bstack1ll1ll1lll1_opy_.bstack1l111lll1ll_opy_, bstack11l1ll1_opy_ (u"ࠧࠨᓾ"))
                caps = None
                if hasattr(webdriver, bstack11l1ll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᓿ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡦ࡬ࡶࡪࡩࡴ࡭ࡻࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᔀ"))
                    except Exception as e:
                        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᔁ") + str(e) + bstack11l1ll1_opy_ (u"ࠤࠥᔂ"))
                try:
                    bstack11llllllll1_opy_ = json.dumps(caps).encode(bstack11l1ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᔃ")) if caps else bstack11lllllllll_opy_ (u"ࠦࢀࢃࠢᔄ")
                    req.capabilities = bstack11llllllll1_opy_
                except Exception as e:
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡧࡵ࡭ࡦࡲࡩࡻࡧࠣࡧࡦࡶࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࠣᔅ") + str(e) + bstack11l1ll1_opy_ (u"ࠨࠢᔆ"))
            except Exception as e:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡹ࡫࡭࠻ࠢࠥᔇ") + str(str(e)) + bstack11l1ll1_opy_ (u"ࠣࠤᔈ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1l1111ll1_opy_() and len(bstack1l1l111111l_opy_) == 0:
            bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11l1_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᔉ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠥࠦᔊ"))
            return {}
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔋ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠧࠨᔌ"))
            return {}
        bstack1l11l1l1ll1_opy_, bstack1l11l1l111l_opy_ = bstack1l1l111111l_opy_[0]
        driver = bstack1l11l1l1ll1_opy_()
        if not driver:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔍ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠢࠣᔎ"))
            return {}
        capabilities = f.bstack1lll1ll11l1_opy_(bstack1l11l1l111l_opy_, bstack1ll1ll1lll1_opy_.bstack1l11l111lll_opy_)
        if not capabilities:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔏ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᔐ"))
            return {}
        return capabilities.get(bstack11l1ll1_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᔑ"), {})
    def bstack1l1ll11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1l1111ll1_opy_() and len(bstack1l1l111111l_opy_) == 0:
            bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l111ll11l1_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔒ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠧࠨᔓ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔔ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠢࠣᔕ"))
        bstack1l11l1l1ll1_opy_, bstack1l11l1l111l_opy_ = bstack1l1l111111l_opy_[0]
        driver = bstack1l11l1l1ll1_opy_()
        if not driver:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔖ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᔗ"))
            return
        return driver