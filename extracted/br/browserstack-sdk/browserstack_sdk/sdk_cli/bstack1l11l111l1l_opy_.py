# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack11l1l1l1_opy_,
    bstack1l1ll111lll_opy_,
    bstack1l1ll1111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lllll_opy_ import bstack11lll1ll111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l1l11_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1l1111ll1_opy_(bstack11lll1ll111_opy_):
    bstack11l1l1l1l1l_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᢙ")
    bstack11ll1lll1ll_opy_ = bstack111ll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᢚ")
    bstack11ll1l1ll11_opy_ = bstack111ll_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᢛ")
    bstack11l1ll11l1l_opy_ = bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᢜ")
    bstack11l1l1l111l_opy_ = bstack111ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᢝ")
    bstack11ll11l11ll_opy_ = bstack111ll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᢞ")
    bstack11l1ll11111_opy_ = bstack111ll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᢟ")
    bstack11l1l1l11ll_opy_ = bstack111ll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᢠ")
    def __init__(self):
        super().__init__(bstack11lll1llll1_opy_=self.bstack11l1l1l1l1l_opy_, frameworks=[bstack1l11lll111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11l1l11l_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111l11ll_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11l1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1111ll1_opy_ = self.bstack11l11l11lll_opy_(instance.context)
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᢡ") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠨࠢᢢ"))
        f.bstack11ll11l1_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, bstack11ll1111ll1_opy_)
        bstack11l111llll1_opy_ = self.bstack11l11l11lll_opy_(instance.context, bstack11l11l111ll_opy_=False)
        f.bstack11ll11l1_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1l1ll11_opy_, bstack11l111llll1_opy_)
    def bstack1l1111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l11l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if not f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1ll11111_opy_, False):
            self.__11l11l11l11_opy_(f,instance,bstack1l1l1lll11l_opy_)
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l11l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        if not f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1ll11111_opy_, False):
            self.__11l11l11l11_opy_(f, instance, bstack1l1l1lll11l_opy_)
        if not f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1l1l11ll_opy_, False):
            self.__11l11l11ll1_opy_(f, instance, bstack1l1l1lll11l_opy_)
    def bstack11l111lll1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11lll1ll11l_opy_(instance):
            return
        if f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1l1l11ll_opy_, False):
            return
        driver.execute_script(
            bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᢣ").format(
                json.dumps(
                    {
                        bstack111ll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᢤ"): bstack111ll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᢥ"),
                        bstack111ll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᢦ"): {bstack111ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᢧ"): result},
                    }
                )
            )
        )
        f.bstack11ll11l1_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1l1l11ll_opy_, True)
    def bstack11l11l11lll_opy_(self, context: bstack1l1ll1111l1_opy_, bstack11l11l111ll_opy_= True):
        if bstack11l11l111ll_opy_:
            bstack11ll1111ll1_opy_ = self.bstack11lll1ll1ll_opy_(context, reverse=True)
        else:
            bstack11ll1111ll1_opy_ = self.bstack11lll1ll1l1_opy_(context, reverse=True)
        return [f for f in bstack11ll1111ll1_opy_ if f[1].state != bstack1ll1l1111l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1lll1lll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def __11l11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᢨ")).get(bstack111ll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵᢩࠥ")):
            bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
            if not bstack11ll1111ll1_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᢪ") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠣࠤ᢫"))
                return
            for bstack11ll111111l_opy_, _ in bstack11ll1111ll1_opy_:
                driver = bstack11ll111111l_opy_()
                status = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1ll11l11_opy_, None)
                if not status:
                    self.logger.debug(bstack111ll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦ᢬") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠥࠦ᢭"))
                    return
                bstack11l1l1l1111_opy_ = {bstack111ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᢮"): status.lower()}
                bstack11l1l1lll11_opy_ = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1l1ll1ll_opy_, None)
                if status.lower() == bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᢯") and bstack11l1l1lll11_opy_ is not None:
                    bstack11l1l1l1111_opy_[bstack111ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᢰ")] = bstack11l1l1lll11_opy_[0][bstack111ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᢱ")][0] if isinstance(bstack11l1l1lll11_opy_, list) else str(bstack11l1l1lll11_opy_)
                driver.execute_script(
                    bstack111ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᢲ").format(
                        json.dumps(
                            {
                                bstack111ll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᢳ"): bstack111ll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᢴ"),
                                bstack111ll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᢵ"): bstack11l1l1l1111_opy_,
                            }
                        )
                    )
                )
            f.bstack11ll11l1_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1l1l11ll_opy_, True)
    @measure(event_name=EVENTS.bstack1llllll11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def __11l11l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᢶ")).get(bstack111ll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᢷ")):
            test_name = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l11l1111l_opy_, None)
            if not test_name:
                self.logger.debug(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᢸ"))
                return
            bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
            if not bstack11ll1111ll1_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᢹ") + str(bstack1l1l1lll11l_opy_) + bstack111ll_opy_ (u"ࠤࠥᢺ"))
                return
            for bstack11ll111111l_opy_, bstack11l11l11l1l_opy_ in bstack11ll1111ll1_opy_:
                if not bstack1l11lll111l_opy_.bstack11lll1ll11l_opy_(bstack11l11l11l1l_opy_):
                    continue
                driver = bstack11ll111111l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᢻ").format(
                        json.dumps(
                            {
                                bstack111ll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᢼ"): bstack111ll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᢽ"),
                                bstack111ll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᢾ"): {bstack111ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᢿ"): test_name},
                            }
                        )
                    )
                )
            f.bstack11ll11l1_opy_(instance, bstack1l1l1111ll1_opy_.bstack11l1ll11111_opy_, True)
    def bstack11ll11lll1l_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        f: TestFramework,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l11l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        bstack11ll1111ll1_opy_ = [d for d, _ in f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])]
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᣀ"))
            return
        if not bstack1l1l1l11_opy_():
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᣁ"))
            return
        for bstack11l11l111l1_opy_ in bstack11ll1111ll1_opy_:
            driver = bstack11l11l111l1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111ll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣᣂ") + str(timestamp)
            driver.execute_script(
                bstack111ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᣃ").format(
                    json.dumps(
                        {
                            bstack111ll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᣄ"): bstack111ll_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᣅ"),
                            bstack111ll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᣆ"): {
                                bstack111ll_opy_ (u"ࠣࡶࡼࡴࡪࠨᣇ"): bstack111ll_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᣈ"),
                                bstack111ll_opy_ (u"ࠥࡨࡦࡺࡡࠣᣉ"): data,
                                bstack111ll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᣊ"): bstack111ll_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᣋ")
                            }
                        }
                    )
                )
            )
    def bstack11ll111llll_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        f: TestFramework,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1l11l_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        keys = [
            bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_,
            bstack1l1l1111ll1_opy_.bstack11ll1l1ll11_opy_,
        ]
        bstack11ll1111ll1_opy_ = []
        for key in keys:
            bstack11ll1111ll1_opy_.extend(f.bstack1l1llll1111_opy_(instance, key, []))
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᣌ"))
            return
        if f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll11l11ll_opy_, False):
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢᣍ"))
            return
        self.bstack11llllll111_opy_()
        bstack1l11111lll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᣎ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111l111l_opy_)
        req.test_framework_version = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l11l1l_opy_)
        req.test_framework_state = bstack1l1l1lll11l_opy_[0].name
        req.test_hook_state = bstack1l1l1lll11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        for bstack11ll111111l_opy_, driver in bstack11ll1111ll1_opy_:
            bstack1l1ll1l11l1_opy_ = driver.data.get(bstack111ll_opy_ (u"ࠤࡵࡥࡳࡱࠢᣏ"))
            bstack11l11l11111_opy_ = False
            if bstack1l1ll1l11l1_opy_ is None:
                bstack11l11l11111_opy_ = True
            else:
                try:
                    bstack11l11l11111_opy_ = int(bstack1l1ll1l11l1_opy_) == 1
                except (TypeError, ValueError):
                    bstack11l11l11111_opy_ = False
            if bstack11l11l11111_opy_:
                try:
                    webdriver = bstack11ll111111l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack111ll_opy_ (u"࡛ࠥࡪࡨࡄࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࠫࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࠦࡥࡹࡲ࡬ࡶࡪࡪࠩࠣᣐ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack111ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᣑ")
                        if bstack1l11lll111l_opy_.bstack1l1llll1111_opy_(driver, bstack1l11lll111l_opy_.bstack11l111lllll_opy_, False)
                        else bstack111ll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᣒ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l11lll111l_opy_.bstack1l1llll1111_opy_(driver, bstack1l11lll111l_opy_.bstack1ll1llll1_opy_, bstack111ll_opy_ (u"ࠨࠢᣓ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l11lll111l_opy_.bstack1l1llll1111_opy_(driver, bstack1l11lll111l_opy_.bstack1ll1111ll11_opy_, bstack111ll_opy_ (u"ࠢࠣᣔ"))
                    caps = None
                    if hasattr(webdriver, bstack111ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᣕ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack111ll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡨ࡮ࡸࡥࡤࡶ࡯ࡽࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᣖ"))
                        except Exception as e:
                            self.logger.debug(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࠣᣗ") + str(e) + bstack111ll_opy_ (u"ࠦࠧᣘ"))
                    try:
                        bstack11l11l1l1l1_opy_ = json.dumps(caps).encode(bstack111ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᣙ")) if caps else bstack11l11l1l111_opy_ (u"ࠨࡻࡾࠤᣚ")
                        req.capabilities = bstack11l11l1l1l1_opy_
                    except Exception as e:
                        self.logger.debug(bstack111ll_opy_ (u"ࠢࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡶࡩࡷ࡯ࡡ࡭࡫ࡽࡩࠥࡩࡡࡱࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࠥᣛ") + str(e) + bstack111ll_opy_ (u"ࠣࠤᣜ"))
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯ࡴࡦ࡯࠽ࠤࠧᣝ") + str(str(e)) + bstack111ll_opy_ (u"ࠥࠦᣞ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11llllllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack1l1l1l11_opy_() and len(bstack11ll1111ll1_opy_) == 0:
            bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1l1ll11_opy_, [])
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᣟ") + str(kwargs) + bstack111ll_opy_ (u"ࠧࠨᣠ"))
            return {}
        for bstack11ll111111l_opy_, bstack11l1llll11l_opy_ in bstack11ll1111ll1_opy_:
            bstack1l1ll1l11l1_opy_ = bstack11l1llll11l_opy_.data.get(bstack111ll_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᣡ"))
            self.logger.info(bstack111ll_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢᣢ") + str(bstack1l1ll1l11l1_opy_) + bstack111ll_opy_ (u"ࠣࠤᣣ"))
            if bstack1l1ll1l11l1_opy_ is None or bstack1l1ll1l11l1_opy_ == bstack111ll_opy_ (u"ࠩ࠴ࠫᣤ"):
                driver = bstack11ll111111l_opy_()
                self.logger.debug(bstack111ll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡨࡨࡸࡨ࡮ࡥࡥࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࠦᣥ") + str(bstack11l1llll11l_opy_.data[bstack111ll_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᣦ")]) + bstack111ll_opy_ (u"ࠧࠨᣧ"))
                if not driver:
                    self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᣨ") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣᣩ"))
                    return {}
                capabilities = f.bstack1l1llll1111_opy_(bstack11l1llll11l_opy_, bstack1l11lll111l_opy_.bstack1ll111ll_opy_)
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᣪ") + str(capabilities) + bstack111ll_opy_ (u"ࠤࠥᣫ"))
                if not capabilities:
                    self.logger.debug(bstack111ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᣬ") + str(kwargs) + bstack111ll_opy_ (u"ࠦࠧᣭ"))
                    return {}
                return capabilities.get(bstack111ll_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᣮ"), {})
        return None
    def bstack1l111l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack1l1l1l11_opy_() and len(bstack11ll1111ll1_opy_) == 0:
            bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1l1ll11_opy_, [])
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᣯ") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣᣰ"))
            return
        if len(bstack11ll1111ll1_opy_) > 1:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᣱ") + str(kwargs) + bstack111ll_opy_ (u"ࠤࠥᣲ"))
        for bstack11ll111111l_opy_, bstack11l1llll11l_opy_ in bstack11ll1111ll1_opy_:
            driver = bstack11ll111111l_opy_()
            bstack1l1ll1l11l1_opy_ = bstack11l1llll11l_opy_.data.get(bstack111ll_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᣳ"))
            self.logger.info(bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢᣴ") + str(bstack1l1ll1l11l1_opy_) + bstack111ll_opy_ (u"ࠧࠨᣵ"))
            if (bstack1l1ll1l11l1_opy_ is None or int(bstack1l1ll1l11l1_opy_) == 1) and driver:
                return driver
        return None