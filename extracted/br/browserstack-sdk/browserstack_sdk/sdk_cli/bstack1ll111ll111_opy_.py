# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1lllllll_opy_,
    bstack1ll1l1l111l_opy_,
    bstack1ll11llll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1lll1l_opy_ import bstack1l11l1llll1_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lll111l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll111l1lll_opy_(bstack1l11l1llll1_opy_):
    bstack11llll111ll_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᚏ")
    bstack1l111l1l1l1_opy_ = bstack1ll111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᚐ")
    bstack1l111l1l11l_opy_ = bstack1ll111_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᚑ")
    bstack11lll1lll1l_opy_ = bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᚒ")
    bstack11llll11ll1_opy_ = bstack1ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᚓ")
    bstack1l111l1l111_opy_ = bstack1ll111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᚔ")
    bstack11llll1l111_opy_ = bstack1ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᚕ")
    bstack11llll1l1l1_opy_ = bstack1ll111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᚖ")
    def __init__(self):
        super().__init__(bstack1l11l1l1ll1_opy_=self.bstack11llll111ll_opy_, frameworks=[bstack1ll11lll111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll1ll111l_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11ll1ll_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l11l111lll_opy_ = self.bstack11ll1ll11l1_opy_(instance.context)
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᚗ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠤࠥᚘ"))
        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, bstack1l11l111lll_opy_)
        bstack11ll1l1l11l_opy_ = self.bstack11ll1ll11l1_opy_(instance.context, bstack11ll1ll1111_opy_=False)
        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l11l_opy_, bstack11ll1l1l11l_opy_)
    def bstack1l1l11ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1ll111l_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if not f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l111_opy_, False):
            self.__11ll1l1l1l1_opy_(f,instance,bstack1ll1l1l1l1l_opy_)
    def bstack1l11lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1ll111l_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        if not f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l111_opy_, False):
            self.__11ll1l1l1l1_opy_(f, instance, bstack1ll1l1l1l1l_opy_)
        if not f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l1l1_opy_, False):
            self.__11ll1ll11ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_)
    def bstack11ll1l1llll_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11l1l1lll_opy_(instance):
            return
        if f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l1l1_opy_, False):
            return
        driver.execute_script(
            bstack1ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᚙ").format(
                json.dumps(
                    {
                        bstack1ll111_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᚚ"): bstack1ll111_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ᚛"),
                        bstack1ll111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ᚜"): {bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᚝"): result},
                    }
                )
            )
        )
        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l1l1_opy_, True)
    def bstack11ll1ll11l1_opy_(self, context: bstack1ll11llll1l_opy_, bstack11ll1ll1111_opy_= True):
        if bstack11ll1ll1111_opy_:
            bstack1l11l111lll_opy_ = self.bstack1l11l1ll1ll_opy_(context, reverse=True)
        else:
            bstack1l11l111lll_opy_ = self.bstack1l11l1ll111_opy_(context, reverse=True)
        return [f for f in bstack1l11l111lll_opy_ if f[1].state != bstack1ll1l1l11l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __11ll1ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ᚞")).get(bstack1ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ᚟")):
            bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
            if not bstack1l11l111lll_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᚠ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠦࠧᚡ"))
                return
            for bstack1l111111111_opy_, _ in bstack1l11l111lll_opy_:
                driver = bstack1l111111111_opy_()
                status = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack11lll1llll1_opy_, None)
                if not status:
                    self.logger.debug(bstack1ll111_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᚢ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠨࠢᚣ"))
                    return
                bstack11llll1ll1l_opy_ = {bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᚤ"): status.lower()}
                bstack11llll111l1_opy_ = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack11llll11111_opy_, None)
                if status.lower() == bstack1ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᚥ") and bstack11llll111l1_opy_ is not None:
                    bstack11llll1ll1l_opy_[bstack1ll111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᚦ")] = bstack11llll111l1_opy_[0][bstack1ll111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᚧ")][0] if isinstance(bstack11llll111l1_opy_, list) else str(bstack11llll111l1_opy_)
                driver.execute_script(
                    bstack1ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᚨ").format(
                        json.dumps(
                            {
                                bstack1ll111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᚩ"): bstack1ll111_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᚪ"),
                                bstack1ll111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᚫ"): bstack11llll1ll1l_opy_,
                            }
                        )
                    )
                )
            f.bstack1ll1ll1lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l1l1_opy_, True)
    @measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __11ll1l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᚬ")).get(bstack1ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᚭ")):
            test_name = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᚮ"))
                return
            bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
            if not bstack1l11l111lll_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᚯ") + str(bstack1ll1l1l1l1l_opy_) + bstack1ll111_opy_ (u"ࠧࠨᚰ"))
                return
            for bstack1l111111111_opy_, bstack11ll1l1ll11_opy_ in bstack1l11l111lll_opy_:
                if not bstack1ll11lll111_opy_.bstack1l11l1l1lll_opy_(bstack11ll1l1ll11_opy_):
                    continue
                driver = bstack1l111111111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᚱ").format(
                        json.dumps(
                            {
                                bstack1ll111_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᚲ"): bstack1ll111_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᚳ"),
                                bstack1ll111_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᚴ"): {bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᚵ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1ll1ll1lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack11llll1l111_opy_, True)
    def bstack1l111lll1l1_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        f: TestFramework,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1ll111l_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        bstack1l11l111lll_opy_ = [d for d, _ in f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])]
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᚶ"))
            return
        if not bstack1lll111l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᚷ"))
            return
        for bstack11ll1ll1l11_opy_ in bstack1l11l111lll_opy_:
            driver = bstack11ll1ll1l11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll111_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᚸ") + str(timestamp)
            driver.execute_script(
                bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᚹ").format(
                    json.dumps(
                        {
                            bstack1ll111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᚺ"): bstack1ll111_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᚻ"),
                            bstack1ll111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᚼ"): {
                                bstack1ll111_opy_ (u"ࠦࡹࡿࡰࡦࠤᚽ"): bstack1ll111_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᚾ"),
                                bstack1ll111_opy_ (u"ࠨࡤࡢࡶࡤࠦᚿ"): data,
                                bstack1ll111_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᛀ"): bstack1ll111_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᛁ")
                            }
                        }
                    )
                )
            )
    def bstack1l111llll1l_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        f: TestFramework,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1ll111l_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        keys = [
            bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_,
            bstack1ll111l1lll_opy_.bstack1l111l1l11l_opy_,
        ]
        bstack1l11l111lll_opy_ = []
        for key in keys:
            bstack1l11l111lll_opy_.extend(f.bstack1lll111lll1_opy_(instance, key, []))
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᛂ"))
            return
        if f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l111_opy_, False):
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᛃ"))
            return
        self.bstack1l11ll1llll_opy_()
        bstack1ll1l1l111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᛄ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l11llllll1_opy_)
        req.test_framework_version = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l111l111ll_opy_)
        req.test_framework_state = bstack1ll1l1l1l1l_opy_[0].name
        req.test_hook_state = bstack1ll1l1l1l1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
        for bstack1l111111111_opy_, driver in bstack1l11l111lll_opy_:
            bstack1ll1l11111l_opy_ = driver.data.get(bstack1ll111_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᛅ"))
            bstack11ll1ll1l1l_opy_ = False
            if bstack1ll1l11111l_opy_ is None:
                bstack11ll1ll1l1l_opy_ = True
            else:
                try:
                    bstack11ll1ll1l1l_opy_ = int(bstack1ll1l11111l_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll1ll1l1l_opy_ = False
            if bstack11ll1ll1l1l_opy_:
                try:
                    webdriver = bstack1l111111111_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1ll111_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᛆ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᛇ")
                        if bstack1ll11lll111_opy_.bstack1lll111lll1_opy_(driver, bstack1ll11lll111_opy_.bstack11ll1ll1ll1_opy_, False)
                        else bstack1ll111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᛈ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll11lll111_opy_.bstack1lll111lll1_opy_(driver, bstack1ll11lll111_opy_.bstack1lll111l1ll_opy_, bstack1ll111_opy_ (u"ࠤࠥᛉ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll11lll111_opy_.bstack1lll111lll1_opy_(driver, bstack1ll11lll111_opy_.bstack1ll1lll111l_opy_, bstack1ll111_opy_ (u"ࠥࠦᛊ"))
                    caps = None
                    if hasattr(webdriver, bstack1ll111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᛋ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1ll111_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᛌ"))
                        except Exception as e:
                            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᛍ") + str(e) + bstack1ll111_opy_ (u"ࠢࠣᛎ"))
                    try:
                        bstack11ll1l1ll1l_opy_ = json.dumps(caps).encode(bstack1ll111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᛏ")) if caps else bstack11ll1l1lll1_opy_ (u"ࠤࡾࢁࠧᛐ")
                        req.capabilities = bstack11ll1l1ll1l_opy_
                    except Exception as e:
                        self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨᛑ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧᛒ"))
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᛓ") + str(str(e)) + bstack1ll111_opy_ (u"ࠨࠢᛔ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack1lll111l1_opy_() and len(bstack1l11l111lll_opy_) == 0:
            bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l11l_opy_, [])
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᛕ") + str(kwargs) + bstack1ll111_opy_ (u"ࠣࠤᛖ"))
            return {}
        for bstack1l111111111_opy_, bstack11lllllllll_opy_ in bstack1l11l111lll_opy_:
            bstack1ll1l11111l_opy_ = bstack11lllllllll_opy_.data.get(bstack1ll111_opy_ (u"ࠩࡵࡥࡳࡱࠧᛗ"))
            self.logger.info(bstack1ll111_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᛘ") + str(bstack1ll1l11111l_opy_) + bstack1ll111_opy_ (u"ࠦࠧᛙ"))
            if bstack1ll1l11111l_opy_ is None or bstack1ll1l11111l_opy_ == bstack1ll111_opy_ (u"ࠬ࠷ࠧᛚ"):
                driver = bstack1l111111111_opy_()
                self.logger.debug(bstack1ll111_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤ࡫࡫ࡴࡤࡪࡨࡨࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࠢᛛ") + str(bstack11lllllllll_opy_.data[bstack1ll111_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᛜ")]) + bstack1ll111_opy_ (u"ࠣࠤᛝ"))
                if not driver:
                    self.logger.debug(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᛞ") + str(kwargs) + bstack1ll111_opy_ (u"ࠥࠦᛟ"))
                    return {}
                capabilities = f.bstack1lll111lll1_opy_(bstack11lllllllll_opy_, bstack1ll11lll111_opy_.bstack1ll1lll1l1l_opy_)
                self.logger.debug(bstack1ll111_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᛠ") + str(capabilities) + bstack1ll111_opy_ (u"ࠧࠨᛡ"))
                if not capabilities:
                    self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᛢ") + str(kwargs) + bstack1ll111_opy_ (u"ࠢࠣᛣ"))
                    return {}
                return capabilities.get(bstack1ll111_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᛤ"), {})
        return None
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack1lll111l1_opy_() and len(bstack1l11l111lll_opy_) == 0:
            bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l11l_opy_, [])
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᛥ") + str(kwargs) + bstack1ll111_opy_ (u"ࠥࠦᛦ"))
            return
        if len(bstack1l11l111lll_opy_) > 1:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᛧ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᛨ"))
        for bstack1l111111111_opy_, bstack11lllllllll_opy_ in bstack1l11l111lll_opy_:
            driver = bstack1l111111111_opy_()
            bstack1ll1l11111l_opy_ = bstack11lllllllll_opy_.data.get(bstack1ll111_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᛩ"))
            self.logger.info(bstack1ll111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᛪ") + str(bstack1ll1l11111l_opy_) + bstack1ll111_opy_ (u"ࠣࠤ᛫"))
            if (bstack1ll1l11111l_opy_ is None or int(bstack1ll1l11111l_opy_) == 1) and driver:
                return driver
        return None