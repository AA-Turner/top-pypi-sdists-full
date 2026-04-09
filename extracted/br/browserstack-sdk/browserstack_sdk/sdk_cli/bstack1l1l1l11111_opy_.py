# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1lll1111ll_opy_,
    bstack1l1lll111ll_opy_,
    bstack1l1ll1l1l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack11lll1ll1l1_opy_ import bstack11lll1lll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1ll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1l111ll11_opy_(bstack11lll1lll1l_opy_):
    bstack11l1ll11lll_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᡬ")
    bstack11ll1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᡭ")
    bstack11lll1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᡮ")
    bstack11l1ll1l1ll_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᡯ")
    bstack11l1ll111ll_opy_ = bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᡰ")
    bstack11lll11l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᡱ")
    bstack11l1ll1ll1l_opy_ = bstack11ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᡲ")
    bstack11l1ll11ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᡳ")
    def __init__(self):
        super().__init__(bstack11llll11ll1_opy_=self.bstack11l1ll11lll_opy_, frameworks=[bstack1l1l1ll11ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11l1l1l1_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111lll11_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lll1l1l11_opy_ = self.bstack11l11ll11l1_opy_(instance.context)
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᡴ") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠥࠦᡵ"))
        f.bstack1l1l1111l1_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, bstack11lll1l1l11_opy_)
        bstack11l11l1lll1_opy_ = self.bstack11l11ll11l1_opy_(instance.context, bstack11l11ll1111_opy_=False)
        f.bstack1l1l1111l1_opy_(instance, bstack1l1l111ll11_opy_.bstack11lll1l1ll1_opy_, bstack11l11l1lll1_opy_)
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l1l1_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if not f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll1ll1l_opy_, False):
            self.__11l11ll1l11_opy_(f,instance,bstack1l1ll1l11l1_opy_)
    def bstack1l1111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l1l1_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        if not f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll1ll1l_opy_, False):
            self.__11l11ll1l11_opy_(f, instance, bstack1l1ll1l11l1_opy_)
        if not f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll11ll1_opy_, False):
            self.__11l11ll11ll_opy_(f, instance, bstack1l1ll1l11l1_opy_)
    def bstack11l11l1l11l_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11lll1llll1_opy_(instance):
            return
        if f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll11ll1_opy_, False):
            return
        driver.execute_script(
            bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᡶ").format(
                json.dumps(
                    {
                        bstack11ll11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᡷ"): bstack11ll11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᡸ"),
                        bstack11ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ᡹"): {bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᡺"): result},
                    }
                )
            )
        )
        f.bstack1l1l1111l1_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll11ll1_opy_, True)
    def bstack11l11ll11l1_opy_(self, context: bstack1l1ll1l1l1l_opy_, bstack11l11ll1111_opy_= True):
        if bstack11l11ll1111_opy_:
            bstack11lll1l1l11_opy_ = self.bstack11llll11l1l_opy_(context, reverse=True)
        else:
            bstack11lll1l1l11_opy_ = self.bstack11lll1lll11_opy_(context, reverse=True)
        return [f for f in bstack11lll1l1l11_opy_ if f[1].state != bstack11111l1ll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11111ll1ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __11l11ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢ᡻")).get(bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ᡼")):
            bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
            if not bstack11lll1l1l11_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ᡽") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠧࠨ᡾"))
                return
            for bstack11ll111l1ll_opy_, _ in bstack11lll1l1l11_opy_:
                driver = bstack11ll111l1ll_opy_()
                status = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1l1lll1l_opy_, None)
                if not status:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣ᡿") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠢࠣᢀ"))
                    return
                bstack11l1ll1l1l1_opy_ = {bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᢁ"): status.lower()}
                bstack11l1ll1ll11_opy_ = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1ll1lll1_opy_, None)
                if status.lower() == bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᢂ") and bstack11l1ll1ll11_opy_ is not None:
                    bstack11l1ll1l1l1_opy_[bstack11ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᢃ")] = bstack11l1ll1ll11_opy_[0][bstack11ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᢄ")][0] if isinstance(bstack11l1ll1ll11_opy_, list) else str(bstack11l1ll1ll11_opy_)
                driver.execute_script(
                    bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᢅ").format(
                        json.dumps(
                            {
                                bstack11ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᢆ"): bstack11ll11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᢇ"),
                                bstack11ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᢈ"): bstack11l1ll1l1l1_opy_,
                            }
                        )
                    )
                )
            f.bstack1l1l1111l1_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll11ll1_opy_, True)
    @measure(event_name=EVENTS.bstack1l11llll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __11l11ll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᢉ")).get(bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᢊ")):
            test_name = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l11ll111l_opy_, None)
            if not test_name:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᢋ"))
                return
            bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
            if not bstack11lll1l1l11_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᢌ") + str(bstack1l1ll1l11l1_opy_) + bstack11ll11_opy_ (u"ࠨࠢᢍ"))
                return
            for bstack11ll111l1ll_opy_, bstack11l11l1ll1l_opy_ in bstack11lll1l1l11_opy_:
                if not bstack1l1l1ll11ll_opy_.bstack11lll1llll1_opy_(bstack11l11l1ll1l_opy_):
                    continue
                driver = bstack11ll111l1ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᢎ").format(
                        json.dumps(
                            {
                                bstack11ll11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᢏ"): bstack11ll11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᢐ"),
                                bstack11ll11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᢑ"): {bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᢒ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1l1l1111l1_opy_(instance, bstack1l1l111ll11_opy_.bstack11l1ll1ll1l_opy_, True)
    def bstack11ll1ll1111_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        f: TestFramework,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l1l1_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        bstack11lll1l1l11_opy_ = [d for d, _ in f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])]
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᢓ"))
            return
        if not bstack1l1ll1ll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᢔ"))
            return
        for bstack11l11ll1ll1_opy_ in bstack11lll1l1l11_opy_:
            driver = bstack11l11ll1ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11ll11_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧᢕ") + str(timestamp)
            driver.execute_script(
                bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᢖ").format(
                    json.dumps(
                        {
                            bstack11ll11_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᢗ"): bstack11ll11_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᢘ"),
                            bstack11ll11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᢙ"): {
                                bstack11ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥᢚ"): bstack11ll11_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᢛ"),
                                bstack11ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧᢜ"): data,
                                bstack11ll11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᢝ"): bstack11ll11_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᢞ")
                            }
                        }
                    )
                )
            )
    def bstack11ll11ll111_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        f: TestFramework,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l1l1_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        keys = [
            bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_,
            bstack1l1l111ll11_opy_.bstack11lll1l1ll1_opy_,
        ]
        bstack11lll1l1l11_opy_ = []
        for key in keys:
            bstack11lll1l1l11_opy_.extend(f.bstack1ll111l1111_opy_(instance, key, []))
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᢟ"))
            return
        if f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11lll11l11l_opy_, False):
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦᢠ"))
            return
        self.bstack1l11111l1l1_opy_()
        bstack1l111ll1ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
        req.client_worker_id = bstack11ll11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᢡ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111ll1111_opy_)
        req.test_framework_version = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11lll1l111l_opy_)
        req.test_framework_state = bstack1l1ll1l11l1_opy_[0].name
        req.test_hook_state = bstack1l1ll1l11l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
        for bstack11ll111l1ll_opy_, driver in bstack11lll1l1l11_opy_:
            bstack1l1ll11llll_opy_ = driver.data.get(bstack11ll11_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᢢ"))
            bstack11l11ll1l1l_opy_ = False
            if bstack1l1ll11llll_opy_ is None:
                bstack11l11ll1l1l_opy_ = True
            else:
                try:
                    bstack11l11ll1l1l_opy_ = int(bstack1l1ll11llll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11l11ll1l1l_opy_ = False
            if bstack11l11ll1l1l_opy_:
                try:
                    webdriver = bstack11ll111l1ll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧᢣ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢᢤ")
                        if bstack1l1l1ll11ll_opy_.bstack1ll111l1111_opy_(driver, bstack1l1l1ll11ll_opy_.bstack11l11l1l1ll_opy_, False)
                        else bstack11ll11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣᢥ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l1l1ll11ll_opy_.bstack1ll111l1111_opy_(driver, bstack1l1l1ll11ll_opy_.bstack1111l1l11_opy_, bstack11ll11_opy_ (u"ࠥࠦᢦ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l1l1ll11ll_opy_.bstack1ll111l1111_opy_(driver, bstack1l1l1ll11ll_opy_.bstack1ll111l11l1_opy_, bstack11ll11_opy_ (u"ࠦࠧᢧ"))
                    caps = None
                    if hasattr(webdriver, bstack11ll11_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᢨ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᢩ"))
                        except Exception as e:
                            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧᢪ") + str(e) + bstack11ll11_opy_ (u"ࠣࠤ᢫"))
                    try:
                        bstack11l11l1ll11_opy_ = json.dumps(caps).encode(bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᢬")) if caps else bstack11l11l1llll_opy_ (u"ࠥࡿࢂࠨ᢭")
                        req.capabilities = bstack11l11l1ll11_opy_
                    except Exception as e:
                        self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢ᢮") + str(e) + bstack11ll11_opy_ (u"ࠧࠨ᢯"))
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤᢰ") + str(str(e)) + bstack11ll11_opy_ (u"ࠢࠣᢱ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack1l1ll1ll1l_opy_() and len(bstack11lll1l1l11_opy_) == 0:
            bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11lll1l1ll1_opy_, [])
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᢲ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥᢳ"))
            return {}
        for bstack11ll111l1ll_opy_, bstack11ll1111ll1_opy_ in bstack11lll1l1l11_opy_:
            bstack1l1ll11llll_opy_ = bstack11ll1111ll1_opy_.data.get(bstack11ll11_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᢴ"))
            self.logger.info(bstack11ll11_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᢵ") + str(bstack1l1ll11llll_opy_) + bstack11ll11_opy_ (u"ࠧࠨᢶ"))
            if bstack1l1ll11llll_opy_ is None or bstack1l1ll11llll_opy_ == bstack11ll11_opy_ (u"࠭࠱ࠨᢷ"):
                driver = bstack11ll111l1ll_opy_()
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥ࡬ࡥࡵࡥ࡫ࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࠣᢸ") + str(bstack11ll1111ll1_opy_.data[bstack11ll11_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᢹ")]) + bstack11ll11_opy_ (u"ࠤࠥᢺ"))
                if not driver:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᢻ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧᢼ"))
                    return {}
                capabilities = f.bstack1ll111l1111_opy_(bstack11ll1111ll1_opy_, bstack1l1l1ll11ll_opy_.bstack11ll1l111l_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᢽ") + str(capabilities) + bstack11ll11_opy_ (u"ࠨࠢᢾ"))
                if not capabilities:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᢿ") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤᣀ"))
                    return {}
                return capabilities.get(bstack11ll11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᣁ"), {})
        return None
    def bstack1l1111ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack1l1ll1ll1l_opy_() and len(bstack11lll1l1l11_opy_) == 0:
            bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11lll1l1ll1_opy_, [])
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᣂ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧᣃ"))
            return
        if len(bstack11lll1l1l11_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᣄ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢᣅ"))
        for bstack11ll111l1ll_opy_, bstack11ll1111ll1_opy_ in bstack11lll1l1l11_opy_:
            driver = bstack11ll111l1ll_opy_()
            bstack1l1ll11llll_opy_ = bstack11ll1111ll1_opy_.data.get(bstack11ll11_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᣆ"))
            self.logger.info(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᣇ") + str(bstack1l1ll11llll_opy_) + bstack11ll11_opy_ (u"ࠤࠥᣈ"))
            if (bstack1l1ll11llll_opy_ is None or int(bstack1l1ll11llll_opy_) == 1) and driver:
                return driver
        return None