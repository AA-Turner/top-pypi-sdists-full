# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
    bstack11l1111ll_opy_,
    bstack1l1ll11ll11_opy_,
    bstack1l1ll1llll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11ll1llll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11llll11111_opy_ import bstack11llll11lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lll1ll1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1l1llll1l_opy_(bstack11llll11lll_opy_):
    bstack11l1l1llll1_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᡯ")
    bstack11ll11l1111_opy_ = bstack1ll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᡰ")
    bstack11ll111ll1l_opy_ = bstack1ll_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᡱ")
    bstack11l1l1lll11_opy_ = bstack1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᡲ")
    bstack11l1l1lllll_opy_ = bstack1ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᡳ")
    bstack11ll11lll11_opy_ = bstack1ll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᡴ")
    bstack11l1ll1l111_opy_ = bstack1ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᡵ")
    bstack11l1l1ll1ll_opy_ = bstack1ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᡶ")
    def __init__(self):
        super().__init__(bstack11llll11ll1_opy_=self.bstack11l1l1llll1_opy_, frameworks=[bstack1l11ll1llll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11ll1111_opy_)
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111lll11_opy_)
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11ll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lll11l1l1_opy_ = self.bstack11l11l11ll1_opy_(instance.context)
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᡷ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠨࠢᡸ"))
        f.bstack1l1l1l1l_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, bstack11lll11l1l1_opy_)
        bstack11l11l1llll_opy_ = self.bstack11l11l11ll1_opy_(instance.context, bstack11l11l11lll_opy_=False)
        f.bstack1l1l1l1l_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll111ll1l_opy_, bstack11l11l1llll_opy_)
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1111_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if not f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1ll1l111_opy_, False):
            self.__11l11l1ll1l_opy_(f,instance,bstack1l1ll1lll11_opy_)
    def bstack1l1111l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1111_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        if not f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1ll1l111_opy_, False):
            self.__11l11l1ll1l_opy_(f, instance, bstack1l1ll1lll11_opy_)
        if not f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1l1ll1ll_opy_, False):
            self.__11l11l1l111_opy_(f, instance, bstack1l1ll1lll11_opy_)
    def bstack11l11ll111l_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11llll111l1_opy_(instance):
            return
        if f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1l1ll1ll_opy_, False):
            return
        driver.execute_script(
            bstack1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ᡹").format(
                json.dumps(
                    {
                        bstack1ll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ᡺"): bstack1ll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ᡻"),
                        bstack1ll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ᡼"): {bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᡽"): result},
                    }
                )
            )
        )
        f.bstack1l1l1l1l_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1l1ll1ll_opy_, True)
    def bstack11l11l11ll1_opy_(self, context: bstack1l1ll1llll1_opy_, bstack11l11l11lll_opy_= True):
        if bstack11l11l11lll_opy_:
            bstack11lll11l1l1_opy_ = self.bstack11lll1lll11_opy_(context, reverse=True)
        else:
            bstack11lll11l1l1_opy_ = self.bstack11lll1lll1l_opy_(context, reverse=True)
        return [f for f in bstack11lll11l1l1_opy_ if f[1].state != bstack1111ll1l11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l111l1lll_opy_, stage=STAGE.bstack11llll111l_opy_)
    def __11l11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥ᡾")).get(bstack1ll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ᡿")):
            bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
            if not bstack11lll11l1l1_opy_:
                self.logger.debug(bstack1ll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᢀ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠣࠤᢁ"))
                return
            for bstack11ll1111l11_opy_, _ in bstack11lll11l1l1_opy_:
                driver = bstack11ll1111l11_opy_()
                status = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l1ll11lll_opy_, None)
                if not status:
                    self.logger.debug(bstack1ll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᢂ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠥࠦᢃ"))
                    return
                bstack11l1ll1l11l_opy_ = {bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᢄ"): status.lower()}
                bstack11l1l1ll111_opy_ = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l1ll11l11_opy_, None)
                if status.lower() == bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᢅ") and bstack11l1l1ll111_opy_ is not None:
                    bstack11l1ll1l11l_opy_[bstack1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᢆ")] = bstack11l1l1ll111_opy_[0][bstack1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᢇ")][0] if isinstance(bstack11l1l1ll111_opy_, list) else str(bstack11l1l1ll111_opy_)
                driver.execute_script(
                    bstack1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᢈ").format(
                        json.dumps(
                            {
                                bstack1ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᢉ"): bstack1ll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᢊ"),
                                bstack1ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᢋ"): bstack11l1ll1l11l_opy_,
                            }
                        )
                    )
                )
            f.bstack1l1l1l1l_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1l1ll1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack11llll111l_opy_)
    def __11l11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᢌ")).get(bstack1ll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᢍ")):
            test_name = f.bstack1ll11111l11_opy_(instance, TestFramework.bstack11l11l1l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᢎ"))
                return
            bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
            if not bstack11lll11l1l1_opy_:
                self.logger.debug(bstack1ll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᢏ") + str(bstack1l1ll1lll11_opy_) + bstack1ll_opy_ (u"ࠤࠥᢐ"))
                return
            for bstack11ll1111l11_opy_, bstack11l11l1lll1_opy_ in bstack11lll11l1l1_opy_:
                if not bstack1l11ll1llll_opy_.bstack11llll111l1_opy_(bstack11l11l1lll1_opy_):
                    continue
                driver = bstack11ll1111l11_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᢑ").format(
                        json.dumps(
                            {
                                bstack1ll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᢒ"): bstack1ll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᢓ"),
                                bstack1ll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᢔ"): {bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᢕ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1l1l1l1l_opy_(instance, bstack1l1l1llll1l_opy_.bstack11l1ll1l111_opy_, True)
    def bstack11lll1l1l11_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        f: TestFramework,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1111_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        bstack11lll11l1l1_opy_ = [d for d, _ in f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])]
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᢖ"))
            return
        if not bstack1lll1ll1ll_opy_():
            self.logger.debug(bstack1ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᢗ"))
            return
        for bstack11l11l1l11l_opy_ in bstack11lll11l1l1_opy_:
            driver = bstack11l11l1l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣᢘ") + str(timestamp)
            driver.execute_script(
                bstack1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᢙ").format(
                    json.dumps(
                        {
                            bstack1ll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᢚ"): bstack1ll_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᢛ"),
                            bstack1ll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᢜ"): {
                                bstack1ll_opy_ (u"ࠣࡶࡼࡴࡪࠨᢝ"): bstack1ll_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᢞ"),
                                bstack1ll_opy_ (u"ࠥࡨࡦࡺࡡࠣᢟ"): data,
                                bstack1ll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᢠ"): bstack1ll_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᢡ")
                            }
                        }
                    )
                )
            )
    def bstack11ll1l1llll_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        f: TestFramework,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11ll1111_opy_(f, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
        keys = [
            bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_,
            bstack1l1l1llll1l_opy_.bstack11ll111ll1l_opy_,
        ]
        bstack11lll11l1l1_opy_ = []
        for key in keys:
            bstack11lll11l1l1_opy_.extend(f.bstack1ll11111l11_opy_(instance, key, []))
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᢢ"))
            return
        if f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11lll11_opy_, False):
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢᢣ"))
            return
        self.bstack1l111l1ll11_opy_()
        bstack1l1111ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111l11l1_opy_)
        req.client_worker_id = bstack1ll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᢤ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        req.test_framework_version = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack11ll11l11ll_opy_)
        req.test_framework_state = bstack1l1ll1lll11_opy_[0].name
        req.test_hook_state = bstack1l1ll1lll11_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_)
        for bstack11ll1111l11_opy_, driver in bstack11lll11l1l1_opy_:
            bstack1l1ll111lll_opy_ = driver.data.get(bstack1ll_opy_ (u"ࠤࡵࡥࡳࡱࠢᢥ"))
            bstack11l11l1ll11_opy_ = False
            if bstack1l1ll111lll_opy_ is None:
                bstack11l11l1ll11_opy_ = True
            else:
                try:
                    bstack11l11l1ll11_opy_ = int(bstack1l1ll111lll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11l11l1ll11_opy_ = False
            if bstack11l11l1ll11_opy_:
                try:
                    webdriver = bstack11ll1111l11_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1ll_opy_ (u"࡛ࠥࡪࡨࡄࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࠫࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࠦࡥࡹࡲ࡬ࡶࡪࡪࠩࠣᢦ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᢧ")
                        if bstack1l11ll1llll_opy_.bstack1ll11111l11_opy_(driver, bstack1l11ll1llll_opy_.bstack11l11l1l1l1_opy_, False)
                        else bstack1ll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᢨ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l11ll1llll_opy_.bstack1ll11111l11_opy_(driver, bstack1l11ll1llll_opy_.bstack11llll1l11_opy_, bstack1ll_opy_ (u"ࠨᢩࠢ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l11ll1llll_opy_.bstack1ll11111l11_opy_(driver, bstack1l11ll1llll_opy_.bstack1l1lllll11l_opy_, bstack1ll_opy_ (u"ࠢࠣᢪ"))
                    caps = None
                    if hasattr(webdriver, bstack1ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᢫")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1ll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡨ࡮ࡸࡥࡤࡶ࡯ࡽࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᢬"))
                        except Exception as e:
                            self.logger.debug(bstack1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࠣ᢭") + str(e) + bstack1ll_opy_ (u"ࠦࠧ᢮"))
                    try:
                        bstack11l11l11l1l_opy_ = json.dumps(caps).encode(bstack1ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᢯")) if caps else bstack11l11l11l11_opy_ (u"ࠨࡻࡾࠤᢰ")
                        req.capabilities = bstack11l11l11l1l_opy_
                    except Exception as e:
                        self.logger.debug(bstack1ll_opy_ (u"ࠢࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡶࡩࡷ࡯ࡡ࡭࡫ࡽࡩࠥࡩࡡࡱࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࠥᢱ") + str(e) + bstack1ll_opy_ (u"ࠣࠤᢲ"))
                except Exception as e:
                    self.logger.error(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯ࡴࡦ࡯࠽ࠤࠧᢳ") + str(str(e)) + bstack1ll_opy_ (u"ࠥࠦᢴ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11lllll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
        if not bstack1lll1ll1ll_opy_() and len(bstack11lll11l1l1_opy_) == 0:
            bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll111ll1l_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᢵ") + str(kwargs) + bstack1ll_opy_ (u"ࠧࠨᢶ"))
            return {}
        for bstack11ll1111l11_opy_, bstack11ll111l1l1_opy_ in bstack11lll11l1l1_opy_:
            bstack1l1ll111lll_opy_ = bstack11ll111l1l1_opy_.data.get(bstack1ll_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᢷ"))
            self.logger.info(bstack1ll_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢᢸ") + str(bstack1l1ll111lll_opy_) + bstack1ll_opy_ (u"ࠣࠤᢹ"))
            if bstack1l1ll111lll_opy_ is None or bstack1l1ll111lll_opy_ == bstack1ll_opy_ (u"ࠩ࠴ࠫᢺ"):
                driver = bstack11ll1111l11_opy_()
                self.logger.debug(bstack1ll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡨࡨࡸࡨ࡮ࡥࡥࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࠦᢻ") + str(bstack11ll111l1l1_opy_.data[bstack1ll_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᢼ")]) + bstack1ll_opy_ (u"ࠧࠨᢽ"))
                if not driver:
                    self.logger.debug(bstack1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᢾ") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣᢿ"))
                    return {}
                capabilities = f.bstack1ll11111l11_opy_(bstack11ll111l1l1_opy_, bstack1l11ll1llll_opy_.bstack11l1111l1l_opy_)
                self.logger.debug(bstack1ll_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᣀ") + str(capabilities) + bstack1ll_opy_ (u"ࠤࠥᣁ"))
                if not capabilities:
                    self.logger.debug(bstack1ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᣂ") + str(kwargs) + bstack1ll_opy_ (u"ࠦࠧᣃ"))
                    return {}
                return capabilities.get(bstack1ll_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᣄ"), {})
        return None
    def bstack1l111l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
        if not bstack1lll1ll1ll_opy_() and len(bstack11lll11l1l1_opy_) == 0:
            bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll111ll1l_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᣅ") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣᣆ"))
            return
        if len(bstack11lll11l1l1_opy_) > 1:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᣇ") + str(kwargs) + bstack1ll_opy_ (u"ࠤࠥᣈ"))
        for bstack11ll1111l11_opy_, bstack11ll111l1l1_opy_ in bstack11lll11l1l1_opy_:
            driver = bstack11ll1111l11_opy_()
            bstack1l1ll111lll_opy_ = bstack11ll111l1l1_opy_.data.get(bstack1ll_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᣉ"))
            self.logger.info(bstack1ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢᣊ") + str(bstack1l1ll111lll_opy_) + bstack1ll_opy_ (u"ࠧࠨᣋ"))
            if (bstack1l1ll111lll_opy_ is None or int(bstack1l1ll111lll_opy_) == 1) and driver:
                return driver
        return None