# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack11ll11l1l1_opy_,
    bstack1l1ll1ll111_opy_,
    bstack1l1lll11111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l111llll11_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lll11_opy_ import bstack11lll1lll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111llll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l11l1ll111_opy_(bstack11lll1lll1l_opy_):
    bstack11l1ll1l111_opy_ = bstack111ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᢈ")
    bstack11ll1llllll_opy_ = bstack111ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᢉ")
    bstack11ll111ll11_opy_ = bstack111ll11_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᢊ")
    bstack11l1ll111l1_opy_ = bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᢋ")
    bstack11l1l1lll11_opy_ = bstack111ll11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᢌ")
    bstack11ll1ll1lll_opy_ = bstack111ll11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᢍ")
    bstack11l1l1lll1l_opy_ = bstack111ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᢎ")
    bstack11l1ll11l1l_opy_ = bstack111ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᢏ")
    def __init__(self):
        super().__init__(bstack11lll1ll1l1_opy_=self.bstack11l1ll1l111_opy_, frameworks=[bstack1l11l11111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11l1ll1l_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11llllll1l1_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lll11l1l1_opy_ = self.bstack11l11l1l11l_opy_(instance.context)
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᢐ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠥࠦᢑ"))
        f.bstack11l1ll11ll_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, bstack11lll11l1l1_opy_)
        bstack11l11l11l11_opy_ = self.bstack11l11l1l11l_opy_(instance.context, bstack11l11l1l1l1_opy_=False)
        f.bstack11l1ll11ll_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll111ll11_opy_, bstack11l11l11l11_opy_)
    def bstack11llllll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll1l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if not f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1l1lll1l_opy_, False):
            self.__11l11l1l111_opy_(f,instance,bstack1l1ll11l11l_opy_)
    def bstack1l111l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll1l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        if not f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1l1lll1l_opy_, False):
            self.__11l11l1l111_opy_(f, instance, bstack1l1ll11l11l_opy_)
        if not f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1ll11l1l_opy_, False):
            self.__11l11l11ll1_opy_(f, instance, bstack1l1ll11l11l_opy_)
    def bstack11l11l11l1l_opy_(
        self,
        f: bstack1l11l11111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11llll111ll_opy_(instance):
            return
        if f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1ll11l1l_opy_, False):
            return
        driver.execute_script(
            bstack111ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᢒ").format(
                json.dumps(
                    {
                        bstack111ll11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᢓ"): bstack111ll11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᢔ"),
                        bstack111ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᢕ"): {bstack111ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᢖ"): result},
                    }
                )
            )
        )
        f.bstack11l1ll11ll_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1ll11l1l_opy_, True)
    def bstack11l11l1l11l_opy_(self, context: bstack1l1lll11111_opy_, bstack11l11l1l1l1_opy_= True):
        if bstack11l11l1l1l1_opy_:
            bstack11lll11l1l1_opy_ = self.bstack11llll1111l_opy_(context, reverse=True)
        else:
            bstack11lll11l1l1_opy_ = self.bstack11llll11111_opy_(context, reverse=True)
        return [f for f in bstack11lll11l1l1_opy_ if f[1].state != bstack11l111l1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l111l11l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __11l11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᢗ")).get(bstack111ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᢘ")):
            bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
            if not bstack11lll11l1l1_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᢙ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠧࠨᢚ"))
                return
            for bstack11l1lllll1l_opy_, _ in bstack11lll11l1l1_opy_:
                driver = bstack11l1lllll1l_opy_()
                status = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1ll11111_opy_, None)
                if not status:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᢛ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠢࠣᢜ"))
                    return
                bstack11l1l1lllll_opy_ = {bstack111ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᢝ"): status.lower()}
                bstack11l1l1ll111_opy_ = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1ll111ll_opy_, None)
                if status.lower() == bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᢞ") and bstack11l1l1ll111_opy_ is not None:
                    bstack11l1l1lllll_opy_[bstack111ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᢟ")] = bstack11l1l1ll111_opy_[0][bstack111ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᢠ")][0] if isinstance(bstack11l1l1ll111_opy_, list) else str(bstack11l1l1ll111_opy_)
                driver.execute_script(
                    bstack111ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᢡ").format(
                        json.dumps(
                            {
                                bstack111ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᢢ"): bstack111ll11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᢣ"),
                                bstack111ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᢤ"): bstack11l1l1lllll_opy_,
                            }
                        )
                    )
                )
            f.bstack11l1ll11ll_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1ll11l1l_opy_, True)
    @measure(event_name=EVENTS.bstack11ll11111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __11l11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᢥ")).get(bstack111ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᢦ")):
            test_name = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l11l1l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᢧ"))
                return
            bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
            if not bstack11lll11l1l1_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᢨ") + str(bstack1l1ll11l11l_opy_) + bstack111ll11_opy_ (u"ࠨᢩࠢ"))
                return
            for bstack11l1lllll1l_opy_, bstack11l11l11lll_opy_ in bstack11lll11l1l1_opy_:
                if not bstack1l11l11111l_opy_.bstack11llll111ll_opy_(bstack11l11l11lll_opy_):
                    continue
                driver = bstack11l1lllll1l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᢪ").format(
                        json.dumps(
                            {
                                bstack111ll11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ᢫"): bstack111ll11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ᢬"),
                                bstack111ll11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ᢭"): {bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᢮"): test_name},
                            }
                        )
                    )
                )
            f.bstack11l1ll11ll_opy_(instance, bstack1l11l1ll111_opy_.bstack11l1l1lll1l_opy_, True)
    def bstack11ll11l11ll_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        f: TestFramework,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll1l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        bstack11lll11l1l1_opy_ = [d for d, _ in f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])]
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧ᢯"))
            return
        if not bstack1l111llll1_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᢰ"))
            return
        for bstack11l11l1ll11_opy_ in bstack11lll11l1l1_opy_:
            driver = bstack11l11l1ll11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111ll11_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧᢱ") + str(timestamp)
            driver.execute_script(
                bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᢲ").format(
                    json.dumps(
                        {
                            bstack111ll11_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᢳ"): bstack111ll11_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᢴ"),
                            bstack111ll11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᢵ"): {
                                bstack111ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥᢶ"): bstack111ll11_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᢷ"),
                                bstack111ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧᢸ"): data,
                                bstack111ll11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᢹ"): bstack111ll11_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᢺ")
                            }
                        }
                    )
                )
            )
    def bstack11ll111ll1l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        f: TestFramework,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll1l_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        keys = [
            bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_,
            bstack1l11l1ll111_opy_.bstack11ll111ll11_opy_,
        ]
        bstack11lll11l1l1_opy_ = []
        for key in keys:
            bstack11lll11l1l1_opy_.extend(f.bstack1l1lllll1l1_opy_(instance, key, []))
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᢻ"))
            return
        if f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1ll1lll_opy_, False):
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦᢼ"))
            return
        self.bstack1l1111lllll_opy_()
        bstack111l1lllll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11llllll1ll_opy_)
        req.client_worker_id = bstack111ll11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᢽ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111ll11ll_opy_)
        req.test_framework_version = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11111l_opy_)
        req.test_framework_state = bstack1l1ll11l11l_opy_[0].name
        req.test_hook_state = bstack1l1ll11l11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_)
        for bstack11l1lllll1l_opy_, driver in bstack11lll11l1l1_opy_:
            bstack1l1lll1111l_opy_ = driver.data.get(bstack111ll11_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᢾ"))
            bstack11l11l111l1_opy_ = False
            if bstack1l1lll1111l_opy_ is None:
                bstack11l11l111l1_opy_ = True
            else:
                try:
                    bstack11l11l111l1_opy_ = int(bstack1l1lll1111l_opy_) == 1
                except (TypeError, ValueError):
                    bstack11l11l111l1_opy_ = False
            if bstack11l11l111l1_opy_:
                try:
                    webdriver = bstack11l1lllll1l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack111ll11_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧᢿ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢᣀ")
                        if bstack1l11l11111l_opy_.bstack1l1lllll1l1_opy_(driver, bstack1l11l11111l_opy_.bstack11l11l1llll_opy_, False)
                        else bstack111ll11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣᣁ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l11l11111l_opy_.bstack1l1lllll1l1_opy_(driver, bstack1l11l11111l_opy_.bstack111llll1ll_opy_, bstack111ll11_opy_ (u"ࠥࠦᣂ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l11l11111l_opy_.bstack1l1lllll1l1_opy_(driver, bstack1l11l11111l_opy_.bstack1ll11111lll_opy_, bstack111ll11_opy_ (u"ࠦࠧᣃ"))
                    caps = None
                    if hasattr(webdriver, bstack111ll11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᣄ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack111ll11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᣅ"))
                        except Exception as e:
                            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧᣆ") + str(e) + bstack111ll11_opy_ (u"ࠣࠤᣇ"))
                    try:
                        bstack11l11l111ll_opy_ = json.dumps(caps).encode(bstack111ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᣈ")) if caps else bstack11l11l1lll1_opy_ (u"ࠥࡿࢂࠨᣉ")
                        req.capabilities = bstack11l11l111ll_opy_
                    except Exception as e:
                        self.logger.debug(bstack111ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢᣊ") + str(e) + bstack111ll11_opy_ (u"ࠧࠨᣋ"))
                except Exception as e:
                    self.logger.error(bstack111ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤᣌ") + str(str(e)) + bstack111ll11_opy_ (u"ࠢࠣᣍ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
        if not bstack1l111llll1_opy_() and len(bstack11lll11l1l1_opy_) == 0:
            bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll111ll11_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᣎ") + str(kwargs) + bstack111ll11_opy_ (u"ࠤࠥᣏ"))
            return {}
        for bstack11l1lllll1l_opy_, bstack11ll11111ll_opy_ in bstack11lll11l1l1_opy_:
            bstack1l1lll1111l_opy_ = bstack11ll11111ll_opy_.data.get(bstack111ll11_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᣐ"))
            self.logger.info(bstack111ll11_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᣑ") + str(bstack1l1lll1111l_opy_) + bstack111ll11_opy_ (u"ࠧࠨᣒ"))
            if bstack1l1lll1111l_opy_ is None or bstack1l1lll1111l_opy_ == bstack111ll11_opy_ (u"࠭࠱ࠨᣓ"):
                driver = bstack11l1lllll1l_opy_()
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥ࡬ࡥࡵࡥ࡫ࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࠣᣔ") + str(bstack11ll11111ll_opy_.data[bstack111ll11_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᣕ")]) + bstack111ll11_opy_ (u"ࠤࠥᣖ"))
                if not driver:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᣗ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧᣘ"))
                    return {}
                capabilities = f.bstack1l1lllll1l1_opy_(bstack11ll11111ll_opy_, bstack1l11l11111l_opy_.bstack1lllll1l1l_opy_)
                self.logger.debug(bstack111ll11_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᣙ") + str(capabilities) + bstack111ll11_opy_ (u"ࠨࠢᣚ"))
                if not capabilities:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᣛ") + str(kwargs) + bstack111ll11_opy_ (u"ࠣࠤᣜ"))
                    return {}
                return capabilities.get(bstack111ll11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᣝ"), {})
        return None
    def bstack11lllll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
        if not bstack1l111llll1_opy_() and len(bstack11lll11l1l1_opy_) == 0:
            bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll111ll11_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᣞ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧᣟ"))
            return
        if len(bstack11lll11l1l1_opy_) > 1:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᣠ") + str(kwargs) + bstack111ll11_opy_ (u"ࠨࠢᣡ"))
        for bstack11l1lllll1l_opy_, bstack11ll11111ll_opy_ in bstack11lll11l1l1_opy_:
            driver = bstack11l1lllll1l_opy_()
            bstack1l1lll1111l_opy_ = bstack11ll11111ll_opy_.data.get(bstack111ll11_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᣢ"))
            self.logger.info(bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᣣ") + str(bstack1l1lll1111l_opy_) + bstack111ll11_opy_ (u"ࠤࠥᣤ"))
            if (bstack1l1lll1111l_opy_ is None or int(bstack1l1lll1111l_opy_) == 1) and driver:
                return driver
        return None