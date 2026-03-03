# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1ll1lll1_opy_,
    bstack1ll1lll1111_opy_,
    bstack1ll1lll11l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l111111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l1ll_opy_ import bstack1l1l1111111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11l1111ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll11l1ll1l_opy_(bstack1l1l1111111_opy_):
    bstack1l111111ll1_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᖌ")
    bstack1l11l11l111_opy_ = bstack11ll111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᖍ")
    bstack1l11l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᖎ")
    bstack1l11111ll11_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᖏ")
    bstack1l1111l1l11_opy_ = bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᖐ")
    bstack1l11l1ll11l_opy_ = bstack11ll111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᖑ")
    bstack1l11111llll_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᖒ")
    bstack1l1111l11l1_opy_ = bstack11ll111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᖓ")
    def __init__(self):
        super().__init__(bstack1l1l11111l1_opy_=self.bstack1l111111ll1_opy_, frameworks=[bstack1ll1111ll11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1l1llll1l1l_opy_.POST), self.bstack11lll1l1ll1_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE), self.bstack1l1ll1111ll_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lll111l_opy_ = self.bstack11lll1ll111_opy_(instance.context)
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᖔ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᖕ"))
        f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, bstack1l11lll111l_opy_)
        bstack11lll1l1l11_opy_ = self.bstack11lll1ll111_opy_(instance.context, bstack11lll1ll11l_opy_=False)
        f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l1l1l1l_opy_, bstack11lll1l1l11_opy_)
    def bstack1l1ll1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1ll1_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if not f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11111llll_opy_, False):
            self.__11lll1l11ll_opy_(f,instance,bstack1ll1ll1llll_opy_)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1ll1_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        if not f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11111llll_opy_, False):
            self.__11lll1l11ll_opy_(f, instance, bstack1ll1ll1llll_opy_)
        if not f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l1111l11l1_opy_, False):
            self.__11lll1lll11_opy_(f, instance, bstack1ll1ll1llll_opy_)
    def bstack11lll1lll1l_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1l1111l1l_opy_(instance):
            return
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l1111l11l1_opy_, False):
            return
        driver.execute_script(
            bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᖖ").format(
                json.dumps(
                    {
                        bstack11ll111_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᖗ"): bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᖘ"),
                        bstack11ll111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᖙ"): {bstack11ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᖚ"): result},
                    }
                )
            )
        )
        f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l1111l11l1_opy_, True)
    def bstack11lll1ll111_opy_(self, context: bstack1ll1lll11l1_opy_, bstack11lll1ll11l_opy_= True):
        if bstack11lll1ll11l_opy_:
            bstack1l11lll111l_opy_ = self.bstack1l1l111l11l_opy_(context, reverse=True)
        else:
            bstack1l11lll111l_opy_ = self.bstack1l1l111l111_opy_(context, reverse=True)
        return [f for f in bstack1l11lll111l_opy_ if f[1].state != bstack1ll1ll1l1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __11lll1lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᖛ")).get(bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᖜ")):
            bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
            if not bstack1l11lll111l_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᖝ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠦࠧᖞ"))
                return
            for bstack1l111l1ll1l_opy_, _ in bstack1l11lll111l_opy_:
                driver = bstack1l111l1ll1l_opy_()
                status = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11111l1l1_opy_, None)
                if not status:
                    self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᖟ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠨࠢᖠ"))
                    return
                bstack1l1111l111l_opy_ = {bstack11ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᖡ"): status.lower()}
                bstack1l111111lll_opy_ = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1111l1l1l_opy_, None)
                if status.lower() == bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᖢ") and bstack1l111111lll_opy_ is not None:
                    bstack1l1111l111l_opy_[bstack11ll111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᖣ")] = bstack1l111111lll_opy_[0][bstack11ll111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᖤ")][0] if isinstance(bstack1l111111lll_opy_, list) else str(bstack1l111111lll_opy_)
                driver.execute_script(
                    bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᖥ").format(
                        json.dumps(
                            {
                                bstack11ll111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᖦ"): bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᖧ"),
                                bstack11ll111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᖨ"): bstack1l1111l111l_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l1111l11l1_opy_, True)
    @measure(event_name=EVENTS.bstack1l1l11l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __11lll1l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᖩ")).get(bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᖪ")):
            test_name = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11lll1lllll_opy_, None)
            if not test_name:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᖫ"))
                return
            bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
            if not bstack1l11lll111l_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᖬ") + str(bstack1ll1ll1llll_opy_) + bstack11ll111_opy_ (u"ࠧࠨᖭ"))
                return
            for bstack1l111l1ll1l_opy_, bstack11lll1ll1l1_opy_ in bstack1l11lll111l_opy_:
                if not bstack1ll1111ll11_opy_.bstack1l1l1111l1l_opy_(bstack11lll1ll1l1_opy_):
                    continue
                driver = bstack1l111l1ll1l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᖮ").format(
                        json.dumps(
                            {
                                bstack11ll111_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᖯ"): bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᖰ"),
                                bstack11ll111_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᖱ"): {bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᖲ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11111llll_opy_, True)
    def bstack1l11l1111l1_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        f: TestFramework,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1ll1_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        bstack1l11lll111l_opy_ = [d for d, _ in f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])]
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᖳ"))
            return
        if not bstack1l11l1111ll_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᖴ"))
            return
        for bstack11lll1ll1ll_opy_ in bstack1l11lll111l_opy_:
            driver = bstack11lll1ll1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11ll111_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᖵ") + str(timestamp)
            driver.execute_script(
                bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᖶ").format(
                    json.dumps(
                        {
                            bstack11ll111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᖷ"): bstack11ll111_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᖸ"),
                            bstack11ll111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᖹ"): {
                                bstack11ll111_opy_ (u"ࠦࡹࡿࡰࡦࠤᖺ"): bstack11ll111_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᖻ"),
                                bstack11ll111_opy_ (u"ࠨࡤࡢࡶࡤࠦᖼ"): data,
                                bstack11ll111_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᖽ"): bstack11ll111_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᖾ")
                            }
                        }
                    )
                )
            )
    def bstack1l11l11l1ll_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        f: TestFramework,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1ll1_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        keys = [
            bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_,
            bstack1ll11l1ll1l_opy_.bstack1l11l1l1l1l_opy_,
        ]
        bstack1l11lll111l_opy_ = []
        for key in keys:
            bstack1l11lll111l_opy_.extend(f.bstack1ll1lllll11_opy_(instance, key, []))
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᖿ"))
            return
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l1ll11l_opy_, False):
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᗀ"))
            return
        self.bstack1l1l11llll1_opy_()
        bstack11lll11111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᗁ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_)
        req.test_framework_state = bstack1ll1ll1llll_opy_[0].name
        req.test_hook_state = bstack1ll1ll1llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
        for bstack1l111l1ll1l_opy_, driver in bstack1l11lll111l_opy_:
            bstack1ll1llll111_opy_ = driver.data.get(bstack11ll111_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᗂ"))
            bstack11lll1l1lll_opy_ = False
            if bstack1ll1llll111_opy_ is None:
                bstack11lll1l1lll_opy_ = True
            else:
                try:
                    bstack11lll1l1lll_opy_ = int(bstack1ll1llll111_opy_) == 1
                except (TypeError, ValueError):
                    bstack11lll1l1lll_opy_ = False
            if bstack11lll1l1lll_opy_:
                try:
                    webdriver = bstack1l111l1ll1l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᗃ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᗄ")
                        if bstack1ll1111ll11_opy_.bstack1ll1lllll11_opy_(driver, bstack1ll1111ll11_opy_.bstack11lll1l1l1l_opy_, False)
                        else bstack11ll111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᗅ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll1111ll11_opy_.bstack1ll1lllll11_opy_(driver, bstack1ll1111ll11_opy_.bstack1l111l11ll1_opy_, bstack11ll111_opy_ (u"ࠤࠥᗆ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll1111ll11_opy_.bstack1ll1lllll11_opy_(driver, bstack1ll1111ll11_opy_.bstack1l111l111l1_opy_, bstack11ll111_opy_ (u"ࠥࠦᗇ"))
                    caps = None
                    if hasattr(webdriver, bstack11ll111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᗈ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11ll111_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᗉ"))
                        except Exception as e:
                            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᗊ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣᗋ"))
                    try:
                        bstack11lll1l11l1_opy_ = json.dumps(caps).encode(bstack11ll111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᗌ")) if caps else bstack11lll1llll1_opy_ (u"ࠤࡾࢁࠧᗍ")
                        req.capabilities = bstack11lll1l11l1_opy_
                    except Exception as e:
                        self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨᗎ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧᗏ"))
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᗐ") + str(str(e)) + bstack11ll111_opy_ (u"ࠨࠢᗑ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l11l1111ll_opy_() and len(bstack1l11lll111l_opy_) == 0:
            bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l1l1l1l_opy_, [])
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗒ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤᗓ"))
            return {}
        for bstack1l111l1ll1l_opy_, bstack1l111ll1l1l_opy_ in bstack1l11lll111l_opy_:
            bstack1ll1llll111_opy_ = bstack1l111ll1l1l_opy_.data.get(bstack11ll111_opy_ (u"ࠩࡵࡥࡳࡱࠧᗔ"))
            self.logger.info(bstack11ll111_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᗕ") + str(bstack1ll1llll111_opy_) + bstack11ll111_opy_ (u"ࠦࠧᗖ"))
            if bstack1ll1llll111_opy_ is None or bstack1ll1llll111_opy_ == bstack11ll111_opy_ (u"ࠬ࠷ࠧᗗ"):
                driver = bstack1l111l1ll1l_opy_()
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤ࡫࡫ࡴࡤࡪࡨࡨࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࠢᗘ") + str(bstack1l111ll1l1l_opy_.data[bstack11ll111_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᗙ")]) + bstack11ll111_opy_ (u"ࠣࠤᗚ"))
                if not driver:
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᗛ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᗜ"))
                    return {}
                capabilities = f.bstack1ll1lllll11_opy_(bstack1l111ll1l1l_opy_, bstack1ll1111ll11_opy_.bstack1l111l11111_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᗝ") + str(capabilities) + bstack11ll111_opy_ (u"ࠧࠨᗞ"))
                if not capabilities:
                    self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᗟ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣᗠ"))
                    return {}
                return capabilities.get(bstack11ll111_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᗡ"), {})
        return None
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l11l1111ll_opy_() and len(bstack1l11lll111l_opy_) == 0:
            bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l1l1l1l_opy_, [])
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᗢ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᗣ"))
            return
        if len(bstack1l11lll111l_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗤ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᗥ"))
        for bstack1l111l1ll1l_opy_, bstack1l111ll1l1l_opy_ in bstack1l11lll111l_opy_:
            driver = bstack1l111l1ll1l_opy_()
            bstack1ll1llll111_opy_ = bstack1l111ll1l1l_opy_.data.get(bstack11ll111_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᗦ"))
            self.logger.info(bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᗧ") + str(bstack1ll1llll111_opy_) + bstack11ll111_opy_ (u"ࠣࠤᗨ"))
            if (bstack1ll1llll111_opy_ is None or int(bstack1ll1llll111_opy_) == 1) and driver:
                return driver
        return None