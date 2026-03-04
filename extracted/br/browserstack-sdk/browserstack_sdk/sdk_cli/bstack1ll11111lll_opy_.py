# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1lll1111l11_opy_,
    bstack1ll1llll11l_opy_,
    bstack1ll1ll11lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11lll1lll_opy_ import bstack1l11lll1111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11ll1l1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll11ll1lll_opy_(bstack1l11lll1111_opy_):
    bstack11lllll1l11_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᘦ")
    bstack1l111lllll1_opy_ = bstack1lll1l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᘧ")
    bstack1l11ll111ll_opy_ = bstack1lll1l_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᘨ")
    bstack1l111111111_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᘩ")
    bstack11lllll1ll1_opy_ = bstack1lll1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᘪ")
    bstack1l11l11l1l1_opy_ = bstack1lll1l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᘫ")
    bstack11lllllll11_opy_ = bstack1lll1l_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᘬ")
    bstack11llll1llll_opy_ = bstack1lll1l_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧᘭ")
    def __init__(self):
        super().__init__(bstack1l11lll1ll1_opy_=self.bstack11lllll1l11_opy_, frameworks=[bstack1ll11l11l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11lll11l111_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l1l1lll1_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll11l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l111lll111_opy_ = self.bstack11lll11111l_opy_(instance.context)
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᘮ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠤࠥᘯ"))
        f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, bstack1l111lll111_opy_)
        bstack11lll111111_opy_ = self.bstack11lll11111l_opy_(instance.context, bstack11lll111l11_opy_=False)
        f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11ll111ll_opy_, bstack11lll111111_opy_)
    def bstack1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11l111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack11lllllll11_opy_, False):
            self.__11ll1lllll1_opy_(f,instance,bstack1ll1ll1ll1l_opy_)
    def bstack1l1l1l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11l111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        if not f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack11lllllll11_opy_, False):
            self.__11ll1lllll1_opy_(f, instance, bstack1ll1ll1ll1l_opy_)
        if not f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack11llll1llll_opy_, False):
            self.__11lll111l1l_opy_(f, instance, bstack1ll1ll1ll1l_opy_)
    def bstack11lll111lll_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11lll111l_opy_(instance):
            return
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack11llll1llll_opy_, False):
            return
        driver.execute_script(
            bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᘰ").format(
                json.dumps(
                    {
                        bstack1lll1l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᘱ"): bstack1lll1l_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᘲ"),
                        bstack1lll1l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᘳ"): {bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᘴ"): result},
                    }
                )
            )
        )
        f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1lll_opy_.bstack11llll1llll_opy_, True)
    def bstack11lll11111l_opy_(self, context: bstack1ll1ll11lll_opy_, bstack11lll111l11_opy_= True):
        if bstack11lll111l11_opy_:
            bstack1l111lll111_opy_ = self.bstack1l11ll1l1ll_opy_(context, reverse=True)
        else:
            bstack1l111lll111_opy_ = self.bstack1l11lll11ll_opy_(context, reverse=True)
        return [f for f in bstack1l111lll111_opy_ if f[1].state != bstack1ll1l1l11ll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def __11lll111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᘵ")).get(bstack1lll1l_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᘶ")):
            bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
            if not bstack1l111lll111_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᘷ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠦࠧᘸ"))
                return
            for bstack1l1111ll1ll_opy_, _ in bstack1l111lll111_opy_:
                driver = bstack1l1111ll1ll_opy_()
                status = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1111111l1_opy_, None)
                if not status:
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᘹ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠨࠢᘺ"))
                    return
                bstack11llllllll1_opy_ = {bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᘻ"): status.lower()}
                bstack11llllll11l_opy_ = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11llllll1l1_opy_, None)
                if status.lower() == bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᘼ") and bstack11llllll11l_opy_ is not None:
                    bstack11llllllll1_opy_[bstack1lll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᘽ")] = bstack11llllll11l_opy_[0][bstack1lll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᘾ")][0] if isinstance(bstack11llllll11l_opy_, list) else str(bstack11llllll11l_opy_)
                driver.execute_script(
                    bstack1lll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᘿ").format(
                        json.dumps(
                            {
                                bstack1lll1l_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᙀ"): bstack1lll1l_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᙁ"),
                                bstack1lll1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᙂ"): bstack11llllllll1_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1lll_opy_.bstack11llll1llll_opy_, True)
    @measure(event_name=EVENTS.bstack11ll11l1l1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def __11ll1lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᙃ")).get(bstack1lll1l_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᙄ")):
            test_name = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11lll1111l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᙅ"))
                return
            bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
            if not bstack1l111lll111_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᙆ") + str(bstack1ll1ll1ll1l_opy_) + bstack1lll1l_opy_ (u"ࠧࠨᙇ"))
                return
            for bstack1l1111ll1ll_opy_, bstack11ll1llllll_opy_ in bstack1l111lll111_opy_:
                if not bstack1ll11l11l11_opy_.bstack1l11lll111l_opy_(bstack11ll1llllll_opy_):
                    continue
                driver = bstack1l1111ll1ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1lll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᙈ").format(
                        json.dumps(
                            {
                                bstack1lll1l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᙉ"): bstack1lll1l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᙊ"),
                                bstack1lll1l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᙋ"): {bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᙌ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1lll_opy_.bstack11lllllll11_opy_, True)
    def bstack1l11l1l1l11_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11l111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        bstack1l111lll111_opy_ = [d for d, _ in f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])]
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᙍ"))
            return
        if not bstack1l11ll1l1l1_opy_():
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᙎ"))
            return
        for bstack11ll1llll11_opy_ in bstack1l111lll111_opy_:
            driver = bstack11ll1llll11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1lll1l_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦᙏ") + str(timestamp)
            driver.execute_script(
                bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᙐ").format(
                    json.dumps(
                        {
                            bstack1lll1l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᙑ"): bstack1lll1l_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᙒ"),
                            bstack1lll1l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᙓ"): {
                                bstack1lll1l_opy_ (u"ࠦࡹࡿࡰࡦࠤᙔ"): bstack1lll1l_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᙕ"),
                                bstack1lll1l_opy_ (u"ࠨࡤࡢࡶࡤࠦᙖ"): data,
                                bstack1lll1l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᙗ"): bstack1lll1l_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᙘ")
                            }
                        }
                    )
                )
            )
    def bstack1l11l1l111l_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        f: TestFramework,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11lll11l111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        keys = [
            bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_,
            bstack1ll11ll1lll_opy_.bstack1l11ll111ll_opy_,
        ]
        bstack1l111lll111_opy_ = []
        for key in keys:
            bstack1l111lll111_opy_.extend(f.bstack1lll111l1l1_opy_(instance, key, []))
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᙙ"))
            return
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11l11l1l1_opy_, False):
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᙚ"))
            return
        self.bstack1l1l1111ll1_opy_()
        bstack1l1l11ll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᙛ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l11l11l1ll_opy_)
        req.test_framework_state = bstack1ll1ll1ll1l_opy_[0].name
        req.test_hook_state = bstack1ll1ll1ll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        for bstack1l1111ll1ll_opy_, driver in bstack1l111lll111_opy_:
            bstack1ll1l1l1lll_opy_ = driver.data.get(bstack1lll1l_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᙜ"))
            bstack11lll1111ll_opy_ = False
            if bstack1ll1l1l1lll_opy_ is None:
                bstack11lll1111ll_opy_ = True
            else:
                try:
                    bstack11lll1111ll_opy_ = int(bstack1ll1l1l1lll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11lll1111ll_opy_ = False
            if bstack11lll1111ll_opy_:
                try:
                    webdriver = bstack1l1111ll1ll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᙝ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᙞ")
                        if bstack1ll11l11l11_opy_.bstack1lll111l1l1_opy_(driver, bstack1ll11l11l11_opy_.bstack11lll11l11l_opy_, False)
                        else bstack1lll1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᙟ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll11l11l11_opy_.bstack1lll111l1l1_opy_(driver, bstack1ll11l11l11_opy_.bstack1lll1l11ll1_opy_, bstack1lll1l_opy_ (u"ࠤࠥᙠ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll11l11l11_opy_.bstack1lll111l1l1_opy_(driver, bstack1ll11l11l11_opy_.bstack1lll1111ll1_opy_, bstack1lll1l_opy_ (u"ࠥࠦᙡ"))
                    caps = None
                    if hasattr(webdriver, bstack1lll1l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᙢ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1lll1l_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᙣ"))
                        except Exception as e:
                            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᙤ") + str(e) + bstack1lll1l_opy_ (u"ࠢࠣᙥ"))
                    try:
                        bstack11ll1llll1l_opy_ = json.dumps(caps).encode(bstack1lll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᙦ")) if caps else bstack11lll111ll1_opy_ (u"ࠤࡾࢁࠧᙧ")
                        req.capabilities = bstack11ll1llll1l_opy_
                    except Exception as e:
                        self.logger.debug(bstack1lll1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨᙨ") + str(e) + bstack1lll1l_opy_ (u"ࠦࠧᙩ"))
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᙪ") + str(str(e)) + bstack1lll1l_opy_ (u"ࠨࠢᙫ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l11ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
        if not bstack1l11ll1l1l1_opy_() and len(bstack1l111lll111_opy_) == 0:
            bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11ll111ll_opy_, [])
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᙬ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤ᙭"))
            return {}
        for bstack1l1111ll1ll_opy_, bstack1l1111ll111_opy_ in bstack1l111lll111_opy_:
            bstack1ll1l1l1lll_opy_ = bstack1l1111ll111_opy_.data.get(bstack1lll1l_opy_ (u"ࠩࡵࡥࡳࡱࠧ᙮"))
            self.logger.info(bstack1lll1l_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᙯ") + str(bstack1ll1l1l1lll_opy_) + bstack1lll1l_opy_ (u"ࠦࠧᙰ"))
            if bstack1ll1l1l1lll_opy_ is None or bstack1ll1l1l1lll_opy_ == bstack1lll1l_opy_ (u"ࠬ࠷ࠧᙱ"):
                driver = bstack1l1111ll1ll_opy_()
                self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤ࡫࡫ࡴࡤࡪࡨࡨࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࠢᙲ") + str(bstack1l1111ll111_opy_.data[bstack1lll1l_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᙳ")]) + bstack1lll1l_opy_ (u"ࠣࠤᙴ"))
                if not driver:
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙵ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠥࠦᙶ"))
                    return {}
                capabilities = f.bstack1lll111l1l1_opy_(bstack1l1111ll111_opy_, bstack1ll11l11l11_opy_.bstack1lll11ll1l1_opy_)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᙷ") + str(capabilities) + bstack1lll1l_opy_ (u"ࠧࠨᙸ"))
                if not capabilities:
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᙹ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠢࠣᙺ"))
                    return {}
                return capabilities.get(bstack1lll1l_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᙻ"), {})
        return None
    def bstack1l1l1l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
        if not bstack1l11ll1l1l1_opy_() and len(bstack1l111lll111_opy_) == 0:
            bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11ll111ll_opy_, [])
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᙼ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠥࠦᙽ"))
            return
        if len(bstack1l111lll111_opy_) > 1:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᙾ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨᙿ"))
        for bstack1l1111ll1ll_opy_, bstack1l1111ll111_opy_ in bstack1l111lll111_opy_:
            driver = bstack1l1111ll1ll_opy_()
            bstack1ll1l1l1lll_opy_ = bstack1l1111ll111_opy_.data.get(bstack1lll1l_opy_ (u"࠭ࡲࡢࡰ࡮ࠫ "))
            self.logger.info(bstack1lll1l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᚁ") + str(bstack1ll1l1l1lll_opy_) + bstack1lll1l_opy_ (u"ࠣࠤᚂ"))
            if (bstack1ll1l1l1lll_opy_ is None or int(bstack1ll1l1l1lll_opy_) == 1) and driver:
                return driver
        return None