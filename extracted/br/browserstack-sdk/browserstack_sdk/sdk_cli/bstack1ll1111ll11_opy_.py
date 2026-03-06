# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1lll11l1ll1_opy_,
    bstack1ll1ll1l111_opy_,
    bstack1ll1ll11l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1l1l1_opy_ import bstack1l11ll1llll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111l1ll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1l111l1l_opy_(bstack1l11ll1llll_opy_):
    bstack11lllll1ll1_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢᘧ")
    bstack1l11l1111l1_opy_ = bstack1111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᘨ")
    bstack1l111l1llll_opy_ = bstack1111_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᘩ")
    bstack11llll1lll1_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᘪ")
    bstack11lllll1l11_opy_ = bstack1111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤᘫ")
    bstack1l111lll1ll_opy_ = bstack1111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᘬ")
    bstack11llllll1l1_opy_ = bstack1111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᘭ")
    bstack11llllll1ll_opy_ = bstack1111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨᘮ")
    def __init__(self):
        super().__init__(bstack1l11lll11ll_opy_=self.bstack11lllll1ll1_opy_, frameworks=[bstack1ll11l11111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll1llll1l_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l11ll_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1llll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l111l1l111_opy_ = self.bstack11ll1llll11_opy_(instance.context)
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᘯ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠥࠦᘰ"))
        f.bstack1lll1l11l1l_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, bstack1l111l1l111_opy_)
        bstack11ll1llllll_opy_ = self.bstack11ll1llll11_opy_(instance.context, bstack11ll1lll1ll_opy_=False)
        f.bstack1lll1l11l1l_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111l1llll_opy_, bstack11ll1llllll_opy_)
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1llll1l_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1l1_opy_, False):
            self.__11lll1111l1_opy_(f,instance,bstack1ll1ll1ll1l_opy_)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1llll1l_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1l1_opy_, False):
            self.__11lll1111l1_opy_(f, instance, bstack1ll1ll1ll1l_opy_)
        if not f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_, False):
            self.__11lll1111ll_opy_(f, instance, bstack1ll1ll1ll1l_opy_)
    def bstack11lll111l1l_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11ll1lll1_opy_(instance):
            return
        if f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_, False):
            return
        driver.execute_script(
            bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᘱ").format(
                json.dumps(
                    {
                        bstack1111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᘲ"): bstack1111_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᘳ"),
                        bstack1111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᘴ"): {bstack1111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᘵ"): result},
                    }
                )
            )
        )
        f.bstack1lll1l11l1l_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_, True)
    def bstack11ll1llll11_opy_(self, context: bstack1ll1ll11l11_opy_, bstack11ll1lll1ll_opy_= True):
        if bstack11ll1lll1ll_opy_:
            bstack1l111l1l111_opy_ = self.bstack1l11ll1ll1l_opy_(context, reverse=True)
        else:
            bstack1l111l1l111_opy_ = self.bstack1l11lll11l1_opy_(context, reverse=True)
        return [f for f in bstack1l111l1l111_opy_ if f[1].state != bstack1ll1lll1ll1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __11lll1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᘶ")).get(bstack1111_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᘷ")):
            bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
            if not bstack1l111l1l111_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᘸ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠧࠨᘹ"))
                return
            for bstack1l1111ll11l_opy_, _ in bstack1l111l1l111_opy_:
                driver = bstack1l1111ll11l_opy_()
                status = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll111l_opy_, None)
                if not status:
                    self.logger.debug(bstack1111_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᘺ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠢࠣᘻ"))
                    return
                bstack11lllll1l1l_opy_ = {bstack1111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᘼ"): status.lower()}
                bstack11llll1llll_opy_ = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll11l1_opy_, None)
                if status.lower() == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᘽ") and bstack11llll1llll_opy_ is not None:
                    bstack11lllll1l1l_opy_[bstack1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᘾ")] = bstack11llll1llll_opy_[0][bstack1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᘿ")][0] if isinstance(bstack11llll1llll_opy_, list) else str(bstack11llll1llll_opy_)
                driver.execute_script(
                    bstack1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᙀ").format(
                        json.dumps(
                            {
                                bstack1111_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᙁ"): bstack1111_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᙂ"),
                                bstack1111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᙃ"): bstack11lllll1l1l_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll1l11l1l_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1ll_opy_, True)
    @measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __11lll1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢᙄ")).get(bstack1111_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᙅ")):
            test_name = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1lll1l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack1111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᙆ"))
                return
            bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
            if not bstack1l111l1l111_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᙇ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111_opy_ (u"ࠨࠢᙈ"))
                return
            for bstack1l1111ll11l_opy_, bstack11lll111111_opy_ in bstack1l111l1l111_opy_:
                if not bstack1ll11l11111_opy_.bstack1l11ll1lll1_opy_(bstack11lll111111_opy_):
                    continue
                driver = bstack1l1111ll11l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᙉ").format(
                        json.dumps(
                            {
                                bstack1111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᙊ"): bstack1111_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᙋ"),
                                bstack1111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᙌ"): {bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᙍ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll1l11l1l_opy_(instance, bstack1ll1l111l1l_opy_.bstack11llllll1l1_opy_, True)
    def bstack1l11l1111ll_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1llll1l_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        bstack1l111l1l111_opy_ = [d for d, _ in f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])]
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᙎ"))
            return
        if not bstack1l111l1ll1l_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᙏ"))
            return
        for bstack11lll111ll1_opy_ in bstack1l111l1l111_opy_:
            driver = bstack11lll111ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1111_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧᙐ") + str(timestamp)
            driver.execute_script(
                bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᙑ").format(
                    json.dumps(
                        {
                            bstack1111_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᙒ"): bstack1111_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᙓ"),
                            bstack1111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᙔ"): {
                                bstack1111_opy_ (u"ࠧࡺࡹࡱࡧࠥᙕ"): bstack1111_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᙖ"),
                                bstack1111_opy_ (u"ࠢࡥࡣࡷࡥࠧᙗ"): data,
                                bstack1111_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᙘ"): bstack1111_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᙙ")
                            }
                        }
                    )
                )
            )
    def bstack1l11l111111_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1llll1l_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        keys = [
            bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_,
            bstack1ll1l111l1l_opy_.bstack1l111l1llll_opy_,
        ]
        bstack1l111l1l111_opy_ = []
        for key in keys:
            bstack1l111l1l111_opy_.extend(f.bstack1lll1l11111_opy_(instance, key, []))
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᙚ"))
            return
        if f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111lll1ll_opy_, False):
            self.logger.debug(bstack1111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦᙛ"))
            return
        self.bstack1l1l111ll1l_opy_()
        bstack1l1llll111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᙜ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l111llll11_opy_)
        req.test_framework_state = bstack1ll1ll1ll1l_opy_[0].name
        req.test_hook_state = bstack1ll1ll1ll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
        for bstack1l1111ll11l_opy_, driver in bstack1l111l1l111_opy_:
            bstack1ll1l1l11ll_opy_ = driver.data.get(bstack1111_opy_ (u"ࠨࡲࡢࡰ࡮ࠦᙝ"))
            bstack11lll111l11_opy_ = False
            if bstack1ll1l1l11ll_opy_ is None:
                bstack11lll111l11_opy_ = True
            else:
                try:
                    bstack11lll111l11_opy_ = int(bstack1ll1l1l11ll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11lll111l11_opy_ = False
            if bstack11lll111l11_opy_:
                try:
                    webdriver = bstack1l1111ll11l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1111_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧᙞ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢᙟ")
                        if bstack1ll11l11111_opy_.bstack1lll1l11111_opy_(driver, bstack1ll11l11111_opy_.bstack11lll111lll_opy_, False)
                        else bstack1111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣᙠ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll11l11111_opy_.bstack1lll1l11111_opy_(driver, bstack1ll11l11111_opy_.bstack1lll11lll1l_opy_, bstack1111_opy_ (u"ࠥࠦᙡ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll11l11111_opy_.bstack1lll1l11111_opy_(driver, bstack1ll11l11111_opy_.bstack1lll1l1l1l1_opy_, bstack1111_opy_ (u"ࠦࠧᙢ"))
                    caps = None
                    if hasattr(webdriver, bstack1111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᙣ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1111_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᙤ"))
                        except Exception as e:
                            self.logger.debug(bstack1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧᙥ") + str(e) + bstack1111_opy_ (u"ࠣࠤᙦ"))
                    try:
                        bstack11ll1lllll1_opy_ = json.dumps(caps).encode(bstack1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᙧ")) if caps else bstack11lll11111l_opy_ (u"ࠥࡿࢂࠨᙨ")
                        req.capabilities = bstack11ll1lllll1_opy_
                    except Exception as e:
                        self.logger.debug(bstack1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢᙩ") + str(e) + bstack1111_opy_ (u"ࠧࠨᙪ"))
                except Exception as e:
                    self.logger.error(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤᙫ") + str(str(e)) + bstack1111_opy_ (u"ࠢࠣᙬ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l1l11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack1l111l1ll1l_opy_() and len(bstack1l111l1l111_opy_) == 0:
            bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111l1llll_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᙭") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥ᙮"))
            return {}
        for bstack1l1111ll11l_opy_, bstack1l1111l1lll_opy_ in bstack1l111l1l111_opy_:
            bstack1ll1l1l11ll_opy_ = bstack1l1111l1lll_opy_.data.get(bstack1111_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᙯ"))
            self.logger.info(bstack1111_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᙰ") + str(bstack1ll1l1l11ll_opy_) + bstack1111_opy_ (u"ࠧࠨᙱ"))
            if bstack1ll1l1l11ll_opy_ is None or bstack1ll1l1l11ll_opy_ == bstack1111_opy_ (u"࠭࠱ࠨᙲ"):
                driver = bstack1l1111ll11l_opy_()
                self.logger.debug(bstack1111_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥ࡬ࡥࡵࡥ࡫ࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࠣᙳ") + str(bstack1l1111l1lll_opy_.data[bstack1111_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᙴ")]) + bstack1111_opy_ (u"ࠤࠥᙵ"))
                if not driver:
                    self.logger.debug(bstack1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᙶ") + str(kwargs) + bstack1111_opy_ (u"ࠦࠧᙷ"))
                    return {}
                capabilities = f.bstack1lll1l11111_opy_(bstack1l1111l1lll_opy_, bstack1ll11l11111_opy_.bstack1lll1111l11_opy_)
                self.logger.debug(bstack1111_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᙸ") + str(capabilities) + bstack1111_opy_ (u"ࠨࠢᙹ"))
                if not capabilities:
                    self.logger.debug(bstack1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙺ") + str(kwargs) + bstack1111_opy_ (u"ࠣࠤᙻ"))
                    return {}
                return capabilities.get(bstack1111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᙼ"), {})
        return None
    def bstack1l1l1l1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack1l111l1ll1l_opy_() and len(bstack1l111l1l111_opy_) == 0:
            bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l111l1llll_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙽ") + str(kwargs) + bstack1111_opy_ (u"ࠦࠧᙾ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(bstack1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᙿ") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢ "))
        for bstack1l1111ll11l_opy_, bstack1l1111l1lll_opy_ in bstack1l111l1l111_opy_:
            driver = bstack1l1111ll11l_opy_()
            bstack1ll1l1l11ll_opy_ = bstack1l1111l1lll_opy_.data.get(bstack1111_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᚁ"))
            self.logger.info(bstack1111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬࠼ࠣࠦᚂ") + str(bstack1ll1l1l11ll_opy_) + bstack1111_opy_ (u"ࠤࠥᚃ"))
            if (bstack1ll1l1l11ll_opy_ is None or int(bstack1ll1l1l11ll_opy_) == 1) and driver:
                return driver
        return None