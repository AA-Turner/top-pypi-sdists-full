# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1ll1llll111_opy_,
    bstack1lll11l1l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_, bstack1l1llll111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l11l_opy_ import bstack1l11lllllll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111lll111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll111lll1l_opy_(bstack1l11lllllll_opy_):
    bstack1l1111l1l11_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᖏ")
    bstack1l11lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᖐ")
    bstack1l11111lll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᖑ")
    bstack1l11111llll_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᖒ")
    bstack1l1111l1lll_opy_ = bstack11l1l11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᖓ")
    bstack1l11l1111l1_opy_ = bstack11l1l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᖔ")
    bstack1l11111ll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᖕ")
    bstack1l11111l1ll_opy_ = bstack11l1l11_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᖖ")
    def __init__(self):
        super().__init__(bstack1l1l1111111_opy_=self.bstack1l1111l1l11_opy_, frameworks=[bstack1l1lllll1l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.BEFORE_EACH, bstack1ll11lll1ll_opy_.POST), self.bstack11lll1l1l1l_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE), self.bstack1l1ll11111l_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1l1ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llll111_opy_ = self.bstack11lll1l11ll_opy_(instance.context)
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᖗ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠧࠨᖘ"))
        f.bstack1lll111ll11_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, bstack1l11llll111_opy_)
        bstack11lll1ll1l1_opy_ = self.bstack11lll1l11ll_opy_(instance.context, bstack11lll1lllll_opy_=False)
        f.bstack1lll111ll11_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111lll1_opy_, bstack11lll1ll1l1_opy_)
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1l1l_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if not f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111ll11_opy_, False):
            self.__11lll1lll1l_opy_(f,instance,bstack1lll11ll111_opy_)
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1l1l_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        if not f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111ll11_opy_, False):
            self.__11lll1lll1l_opy_(f, instance, bstack1lll11ll111_opy_)
        if not f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111l1ll_opy_, False):
            self.__11llll11111_opy_(f, instance, bstack1lll11ll111_opy_)
    def bstack11lll1llll1_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1l1111l11_opy_(instance):
            return
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111l1ll_opy_, False):
            return
        driver.execute_script(
            bstack11l1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᖙ").format(
                json.dumps(
                    {
                        bstack11l1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᖚ"): bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᖛ"),
                        bstack11l1l11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᖜ"): {bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᖝ"): result},
                    }
                )
            )
        )
        f.bstack1lll111ll11_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111l1ll_opy_, True)
    def bstack11lll1l11ll_opy_(self, context: bstack1lll11l1l11_opy_, bstack11lll1lllll_opy_= True):
        if bstack11lll1lllll_opy_:
            bstack1l11llll111_opy_ = self.bstack1l1l1111lll_opy_(context, reverse=True)
        else:
            bstack1l11llll111_opy_ = self.bstack1l1l11111l1_opy_(context, reverse=True)
        return [f for f in bstack1l11llll111_opy_ if f[1].state != bstack1ll1lll1lll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1111l1l11_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __11llll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᖞ")).get(bstack11l1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᖟ")):
            bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
            if not bstack1l11llll111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᖠ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠢࠣᖡ"))
                return
            for bstack1l111ll1l1l_opy_, _ in bstack1l11llll111_opy_:
                driver = bstack1l111ll1l1l_opy_()
                status = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1111l11l1_opy_, None)
                if not status:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᖢ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠤࠥᖣ"))
                    return
                bstack1l11111l1l1_opy_ = {bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᖤ"): status.lower()}
                bstack1l11111ll1l_opy_ = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111111lll_opy_, None)
                if status.lower() == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᖥ") and bstack1l11111ll1l_opy_ is not None:
                    bstack1l11111l1l1_opy_[bstack11l1l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᖦ")] = bstack1l11111ll1l_opy_[0][bstack11l1l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᖧ")][0] if isinstance(bstack1l11111ll1l_opy_, list) else str(bstack1l11111ll1l_opy_)
                driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᖨ").format(
                        json.dumps(
                            {
                                bstack11l1l11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᖩ"): bstack11l1l11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᖪ"),
                                bstack11l1l11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᖫ"): bstack1l11111l1l1_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll111ll11_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111l1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1ll11l1lll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __11lll1lll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᖬ")).get(bstack11l1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᖭ")):
            test_name = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11lll1l1lll_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᖮ"))
                return
            bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
            if not bstack1l11llll111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᖯ") + str(bstack1lll11ll111_opy_) + bstack11l1l11_opy_ (u"ࠣࠤᖰ"))
                return
            for bstack1l111ll1l1l_opy_, bstack11lll1l1ll1_opy_ in bstack1l11llll111_opy_:
                if not bstack1l1lllll1l1_opy_.bstack1l1l1111l11_opy_(bstack11lll1l1ll1_opy_):
                    continue
                driver = bstack1l111ll1l1l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᖱ").format(
                        json.dumps(
                            {
                                bstack11l1l11_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᖲ"): bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᖳ"),
                                bstack11l1l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᖴ"): {bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᖵ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll111ll11_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111ll11_opy_, True)
    def bstack1l11l1l11l1_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        f: TestFramework,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1l1l_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        bstack1l11llll111_opy_ = [d for d, _ in f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])]
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᖶ"))
            return
        if not bstack1l111lll111_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᖷ"))
            return
        for bstack11lll1l1l11_opy_ in bstack1l11llll111_opy_:
            driver = bstack11lll1l1l11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1l11_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᖸ") + str(timestamp)
            driver.execute_script(
                bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᖹ").format(
                    json.dumps(
                        {
                            bstack11l1l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᖺ"): bstack11l1l11_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢᖻ"),
                            bstack11l1l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᖼ"): {
                                bstack11l1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧᖽ"): bstack11l1l11_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧᖾ"),
                                bstack11l1l11_opy_ (u"ࠤࡧࡥࡹࡧࠢᖿ"): data,
                                bstack11l1l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᗀ"): bstack11l1l11_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᗁ")
                            }
                        }
                    )
                )
            )
    def bstack1l111llll1l_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        f: TestFramework,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack11lll1l1l1l_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        keys = [
            bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_,
            bstack1ll111lll1l_opy_.bstack1l11111lll1_opy_,
        ]
        bstack1l11llll111_opy_ = []
        for key in keys:
            bstack1l11llll111_opy_.extend(f.bstack1ll1lll111l_opy_(instance, key, []))
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᗂ"))
            return
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11l1111l1_opy_, False):
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨᗃ"))
            return
        self.bstack1l1l1ll1111_opy_()
        bstack111l11l1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᗄ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1ll1l1lll_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_)
        req.test_framework_state = bstack1lll11ll111_opy_[0].name
        req.test_hook_state = bstack1lll11ll111_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
        for bstack1l111ll1l1l_opy_, driver in bstack1l11llll111_opy_:
            bstack1lll1111l11_opy_ = driver.data.get(bstack11l1l11_opy_ (u"ࠣࡴࡤࡲࡰࠨᗅ"))
            bstack11lll1ll111_opy_ = False
            if bstack1lll1111l11_opy_ is None:
                bstack11lll1ll111_opy_ = True
            else:
                try:
                    bstack11lll1ll111_opy_ = int(bstack1lll1111l11_opy_) == 1
                except (TypeError, ValueError):
                    bstack11lll1ll111_opy_ = False
            if bstack11lll1ll111_opy_:
                try:
                    webdriver = bstack1l111ll1l1l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢᗆ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᗇ")
                        if bstack1l1lllll1l1_opy_.bstack1ll1lll111l_opy_(driver, bstack1l1lllll1l1_opy_.bstack11lll1lll11_opy_, False)
                        else bstack11l1l11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᗈ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l1lllll1l1_opy_.bstack1ll1lll111l_opy_(driver, bstack1l1lllll1l1_opy_.bstack1l111l1l11l_opy_, bstack11l1l11_opy_ (u"ࠧࠨᗉ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l1lllll1l1_opy_.bstack1ll1lll111l_opy_(driver, bstack1l1lllll1l1_opy_.bstack1l111l1l111_opy_, bstack11l1l11_opy_ (u"ࠨࠢᗊ"))
                    caps = None
                    if hasattr(webdriver, bstack11l1l11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᗋ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡧ࡭ࡷ࡫ࡣࡵ࡮ࡼࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᗌ"))
                        except Exception as e:
                            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᗍ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦᗎ"))
                    try:
                        bstack11lll1ll11l_opy_ = json.dumps(caps).encode(bstack11l1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᗏ")) if caps else bstack11lll1ll1ll_opy_ (u"ࠧࢁࡽࠣᗐ")
                        req.capabilities = bstack11lll1ll11l_opy_
                    except Exception as e:
                        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡵࡨࡶ࡮ࡧ࡬ࡪࡼࡨࠤࡨࡧࡰࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࠤᗑ") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣᗒ"))
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡺࡥ࡮࠼ࠣࠦᗓ") + str(str(e)) + bstack11l1l11_opy_ (u"ࠤࠥᗔ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1ll1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l111lll111_opy_() and len(bstack1l11llll111_opy_) == 0:
            bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111lll1_opy_, [])
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᗕ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧᗖ"))
            return {}
        for bstack1l111ll1l1l_opy_, bstack1l111l1ll1l_opy_ in bstack1l11llll111_opy_:
            bstack1lll1111l11_opy_ = bstack1l111l1ll1l_opy_.data.get(bstack11l1l11_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᗗ"))
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨᗘ") + str(bstack1lll1111l11_opy_) + bstack11l1l11_opy_ (u"ࠢࠣᗙ"))
            if bstack1lll1111l11_opy_ is None or bstack1lll1111l11_opy_ == bstack11l1l11_opy_ (u"ࠨ࠳ࠪᗚ"):
                driver = bstack1l111ll1l1l_opy_()
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡧࡧࡷࡧ࡭࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࠥᗛ") + str(bstack1l111l1ll1l_opy_.data[bstack11l1l11_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᗜ")]) + bstack11l1l11_opy_ (u"ࠦࠧᗝ"))
                if not driver:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗞ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᗟ"))
                    return {}
                capabilities = f.bstack1ll1lll111l_opy_(bstack1l111l1ll1l_opy_, bstack1l1lllll1l1_opy_.bstack1l1111ll11l_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᗠ") + str(capabilities) + bstack11l1l11_opy_ (u"ࠣࠤᗡ"))
                if not capabilities:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᗢ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦᗣ"))
                    return {}
                return capabilities.get(bstack11l1l11_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᗤ"), {})
        return None
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l111lll111_opy_() and len(bstack1l11llll111_opy_) == 0:
            bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11111lll1_opy_, [])
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᗥ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᗦ"))
            return
        if len(bstack1l11llll111_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗧ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᗨ"))
        for bstack1l111ll1l1l_opy_, bstack1l111l1ll1l_opy_ in bstack1l11llll111_opy_:
            driver = bstack1l111ll1l1l_opy_()
            bstack1lll1111l11_opy_ = bstack1l111l1ll1l_opy_.data.get(bstack11l1l11_opy_ (u"ࠩࡵࡥࡳࡱࠧᗩ"))
            self.logger.info(bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨᗪ") + str(bstack1lll1111l11_opy_) + bstack11l1l11_opy_ (u"ࠦࠧᗫ"))
            if (bstack1lll1111l11_opy_ is None or int(bstack1lll1111l11_opy_) == 1) and driver:
                return driver
        return None