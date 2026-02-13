# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1ll11l11_opy_,
    bstack1ll1l1ll1ll_opy_,
    bstack1ll1ll1llll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_, bstack1ll11l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11lll11ll_opy_ import bstack1l11lll1l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111lllll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1l111l11_opy_(bstack1l11lll1l1l_opy_):
    bstack1l11111111l_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᖅ")
    bstack1l11l1l11ll_opy_ = bstack11l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᖆ")
    bstack11lllllll11_opy_ = bstack11l11_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᖇ")
    bstack11llllll1l1_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᖈ")
    bstack11llllll1ll_opy_ = bstack11l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᖉ")
    bstack1l11l1lllll_opy_ = bstack11l11_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᖊ")
    bstack1l1111111l1_opy_ = bstack11l11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᖋ")
    bstack11llllll11l_opy_ = bstack11l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᖌ")
    def __init__(self):
        super().__init__(bstack1l11lll11l1_opy_=self.bstack1l11111111l_opy_, frameworks=[bstack1l1llllllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.BEFORE_EACH, bstack1l1lllll1ll_opy_.POST), self.bstack11lll111ll1_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE), self.bstack1l1l11ll111_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l1llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l11l1ll_opy_ = self.bstack11lll11l11l_opy_(instance.context)
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᖍ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠤࠥᖎ"))
        f.bstack1ll1lll111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, bstack1l11l11l1ll_opy_)
        bstack11lll11ll1l_opy_ = self.bstack11lll11l11l_opy_(instance.context, bstack11lll11l1l1_opy_=False)
        f.bstack1ll1lll111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11lllllll11_opy_, bstack11lll11ll1l_opy_)
    def bstack1l1l11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll111ll1_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if not f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l1111111l1_opy_, False):
            self.__11lll111l1l_opy_(f,instance,bstack1ll1l1lll1l_opy_)
    def bstack1l1l1llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll111ll1_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        if not f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l1111111l1_opy_, False):
            self.__11lll111l1l_opy_(f, instance, bstack1ll1l1lll1l_opy_)
        if not f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11llllll11l_opy_, False):
            self.__11lll1l111l_opy_(f, instance, bstack1ll1l1lll1l_opy_)
    def bstack11lll11l111_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11lllll11_opy_(instance):
            return
        if f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11llllll11l_opy_, False):
            return
        driver.execute_script(
            bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᖏ").format(
                json.dumps(
                    {
                        bstack11l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᖐ"): bstack11l11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᖑ"),
                        bstack11l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᖒ"): {bstack11l11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᖓ"): result},
                    }
                )
            )
        )
        f.bstack1ll1lll111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11llllll11l_opy_, True)
    def bstack11lll11l11l_opy_(self, context: bstack1ll1ll1llll_opy_, bstack11lll11l1l1_opy_= True):
        if bstack11lll11l1l1_opy_:
            bstack1l11l11l1ll_opy_ = self.bstack1l11lll1111_opy_(context, reverse=True)
        else:
            bstack1l11l11l1ll_opy_ = self.bstack1l11lll1l11_opy_(context, reverse=True)
        return [f for f in bstack1l11l11l1ll_opy_ if f[1].state != bstack1ll1lllllll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __11lll1l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᖔ")).get(bstack11l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᖕ")):
            bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
            if not bstack1l11l11l1ll_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᖖ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠦࠧᖗ"))
                return
            for bstack1l111l111l1_opy_, _ in bstack1l11l11l1ll_opy_:
                driver = bstack1l111l111l1_opy_()
                status = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l111111l1l_opy_, None)
                if not status:
                    self.logger.debug(bstack11l11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᖘ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠨࠢᖙ"))
                    return
                bstack11lllll1lll_opy_ = {bstack11l11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᖚ"): status.lower()}
                bstack11lllllllll_opy_ = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l111111111_opy_, None)
                if status.lower() == bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᖛ") and bstack11lllllllll_opy_ is not None:
                    bstack11lllll1lll_opy_[bstack11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᖜ")] = bstack11lllllllll_opy_[0][bstack11l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᖝ")][0] if isinstance(bstack11lllllllll_opy_, list) else str(bstack11lllllllll_opy_)
                driver.execute_script(
                    bstack11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᖞ").format(
                        json.dumps(
                            {
                                bstack11l11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᖟ"): bstack11l11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᖠ"),
                                bstack11l11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᖡ"): bstack11lllll1lll_opy_,
                            }
                        )
                    )
                )
            f.bstack1ll1lll111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11llllll11l_opy_, True)
    @measure(event_name=EVENTS.bstack1lllllll11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __11lll111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᖢ")).get(bstack11l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᖣ")):
            test_name = f.bstack1lll111111l_opy_(instance, TestFramework.bstack11lll11ll11_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᖤ"))
                return
            bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
            if not bstack1l11l11l1ll_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᖥ") + str(bstack1ll1l1lll1l_opy_) + bstack11l11_opy_ (u"ࠧࠨᖦ"))
                return
            for bstack1l111l111l1_opy_, bstack11lll1l1111_opy_ in bstack1l11l11l1ll_opy_:
                if not bstack1l1llllllll_opy_.bstack1l11lllll11_opy_(bstack11lll1l1111_opy_):
                    continue
                driver = bstack1l111l111l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᖧ").format(
                        json.dumps(
                            {
                                bstack11l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᖨ"): bstack11l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᖩ"),
                                bstack11l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᖪ"): {bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᖫ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1ll1lll111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l1111111l1_opy_, True)
    def bstack1l11l1ll1l1_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        f: TestFramework,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll111ll1_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        bstack1l11l11l1ll_opy_ = [d for d, _ in f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])]
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᖬ"))
            return
        if not bstack1l111lllll1_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᖭ"))
            return
        for bstack11lll111lll_opy_ in bstack1l11l11l1ll_opy_:
            driver = bstack11lll111lll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l11_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᖮ") + str(timestamp)
            driver.execute_script(
                bstack11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᖯ").format(
                    json.dumps(
                        {
                            bstack11l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᖰ"): bstack11l11_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᖱ"),
                            bstack11l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᖲ"): {
                                bstack11l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᖳ"): bstack11l11_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᖴ"),
                                bstack11l11_opy_ (u"ࠨࡤࡢࡶࡤࠦᖵ"): data,
                                bstack11l11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᖶ"): bstack11l11_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᖷ")
                            }
                        }
                    )
                )
            )
    def bstack1l11l111l1l_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        f: TestFramework,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll111ll1_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        keys = [
            bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_,
            bstack1ll1l111l11_opy_.bstack11lllllll11_opy_,
        ]
        bstack1l11l11l1ll_opy_ = []
        for key in keys:
            bstack1l11l11l1ll_opy_.extend(f.bstack1lll111111l_opy_(instance, key, []))
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᖸ"))
            return
        if f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1lllll_opy_, False):
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᖹ"))
            return
        self.bstack1l1l11l1111_opy_()
        bstack1lllll111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᖺ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l1l11l11_opy_)
        req.test_framework_version = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l11l111l11_opy_)
        req.test_framework_state = bstack1ll1l1lll1l_opy_[0].name
        req.test_hook_state = bstack1ll1l1lll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        for bstack1l111l111l1_opy_, driver in bstack1l11l11l1ll_opy_:
            bstack1ll1llll1l1_opy_ = driver.data.get(bstack11l11_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᖻ"))
            bstack11lll11lll1_opy_ = False
            if bstack1ll1llll1l1_opy_ is None:
                bstack11lll11lll1_opy_ = True
            else:
                try:
                    bstack11lll11lll1_opy_ = int(bstack1ll1llll1l1_opy_) == 1
                except (TypeError, ValueError):
                    bstack11lll11lll1_opy_ = False
            if bstack11lll11lll1_opy_:
                try:
                    webdriver = bstack1l111l111l1_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11l11_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᖼ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᖽ")
                        if bstack1l1llllllll_opy_.bstack1lll111111l_opy_(driver, bstack1l1llllllll_opy_.bstack11lll11l1ll_opy_, False)
                        else bstack11l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᖾ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l1llllllll_opy_.bstack1lll111111l_opy_(driver, bstack1l1llllllll_opy_.bstack1l11111lll1_opy_, bstack11l11_opy_ (u"ࠤࠥᖿ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l1llllllll_opy_.bstack1lll111111l_opy_(driver, bstack1l1llllllll_opy_.bstack1l1111ll1ll_opy_, bstack11l11_opy_ (u"ࠥࠦᗀ"))
                    caps = None
                    if hasattr(webdriver, bstack11l11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᗁ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11l11_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᗂ"))
                        except Exception as e:
                            self.logger.debug(bstack11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᗃ") + str(e) + bstack11l11_opy_ (u"ࠢࠣᗄ"))
                    try:
                        bstack11lll111l11_opy_ = json.dumps(caps).encode(bstack11l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᗅ")) if caps else bstack11lll11llll_opy_ (u"ࠤࡾࢁࠧᗆ")
                        req.capabilities = bstack11lll111l11_opy_
                    except Exception as e:
                        self.logger.debug(bstack11l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨᗇ") + str(e) + bstack11l11_opy_ (u"ࠦࠧᗈ"))
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᗉ") + str(str(e)) + bstack11l11_opy_ (u"ࠨࠢᗊ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111lllll1_opy_() and len(bstack1l11l11l1ll_opy_) == 0:
            bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11lllllll11_opy_, [])
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗋ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤᗌ"))
            return {}
        for bstack1l111l111l1_opy_, bstack1l1111llll1_opy_ in bstack1l11l11l1ll_opy_:
            bstack1ll1llll1l1_opy_ = bstack1l1111llll1_opy_.data.get(bstack11l11_opy_ (u"ࠩࡵࡥࡳࡱࠧᗍ"))
            self.logger.info(bstack11l11_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᗎ") + str(bstack1ll1llll1l1_opy_) + bstack11l11_opy_ (u"ࠦࠧᗏ"))
            if bstack1ll1llll1l1_opy_ is None or bstack1ll1llll1l1_opy_ == bstack11l11_opy_ (u"ࠬ࠷ࠧᗐ"):
                driver = bstack1l111l111l1_opy_()
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤ࡫࡫ࡴࡤࡪࡨࡨࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࠢᗑ") + str(bstack1l1111llll1_opy_.data[bstack11l11_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᗒ")]) + bstack11l11_opy_ (u"ࠣࠤᗓ"))
                if not driver:
                    self.logger.debug(bstack11l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᗔ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᗕ"))
                    return {}
                capabilities = f.bstack1lll111111l_opy_(bstack1l1111llll1_opy_, bstack1l1llllllll_opy_.bstack1l1111l1lll_opy_)
                self.logger.debug(bstack11l11_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᗖ") + str(capabilities) + bstack11l11_opy_ (u"ࠧࠨᗗ"))
                if not capabilities:
                    self.logger.debug(bstack11l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᗘ") + str(kwargs) + bstack11l11_opy_ (u"ࠢࠣᗙ"))
                    return {}
                return capabilities.get(bstack11l11_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᗚ"), {})
        return None
    def bstack1l1l11l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l111lllll1_opy_() and len(bstack1l11l11l1ll_opy_) == 0:
            bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack11lllllll11_opy_, [])
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᗛ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᗜ"))
            return
        if len(bstack1l11l11l1ll_opy_) > 1:
            self.logger.debug(bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗝ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᗞ"))
        for bstack1l111l111l1_opy_, bstack1l1111llll1_opy_ in bstack1l11l11l1ll_opy_:
            driver = bstack1l111l111l1_opy_()
            bstack1ll1llll1l1_opy_ = bstack1l1111llll1_opy_.data.get(bstack11l11_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᗟ"))
            self.logger.info(bstack11l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᗠ") + str(bstack1ll1llll1l1_opy_) + bstack11l11_opy_ (u"ࠣࠤᗡ"))
            if (bstack1ll1llll1l1_opy_ is None or int(bstack1ll1llll1l1_opy_) == 1) and driver:
                return driver
        return None