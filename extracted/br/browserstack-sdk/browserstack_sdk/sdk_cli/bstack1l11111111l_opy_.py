# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l1ll11l_opy_,
    bstack1l1l111l1l1_opy_,
    bstack1l1lll111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack11ll11lll1l_opy_ import bstack11ll1l11111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1ll111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1111l111l_opy_(bstack11ll1l11111_opy_):
    bstack11l11ll1111_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣᤀ")
    bstack11ll11ll111_opy_ = bstack111l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᤁ")
    bstack11l1lll11l1_opy_ = bstack111l_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᤂ")
    bstack11l11llll11_opy_ = bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᤃ")
    bstack11l1l11111l_opy_ = bstack111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥᤄ")
    bstack11ll11111ll_opy_ = bstack111l_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨᤅ")
    bstack11l11lll1l1_opy_ = bstack111l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᤆ")
    bstack11l11ll1l11_opy_ = bstack111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢᤇ")
    def __init__(self):
        super().__init__(bstack11ll1l11ll1_opy_=self.bstack11l11ll1111_opy_, frameworks=[bstack1l11l11l11l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack111llllllll_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11lll1ll1ll_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack111llllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1ll1ll1l_opy_ = self.bstack11l11111l11_opy_(instance.context)
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᤈ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠦࠧᤉ"))
        f.bstack1l11l1ll11_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, bstack11l1ll1ll1l_opy_)
        bstack11l1111111l_opy_ = self.bstack11l11111l11_opy_(instance.context, bstack11l111111l1_opy_=False)
        f.bstack1l11l1ll11_opy_(instance, bstack1l1111l111l_opy_.bstack11l1lll11l1_opy_, bstack11l1111111l_opy_)
    def bstack11lll1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111llllllll_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if not f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l11lll1l1_opy_, False):
            self.__11l1111l11l_opy_(f,instance,bstack1l1l1lllll1_opy_)
    def bstack11lll1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111llllllll_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        if not f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l11lll1l1_opy_, False):
            self.__11l1111l11l_opy_(f, instance, bstack1l1l1lllll1_opy_)
        if not f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l11ll1l11_opy_, False):
            self.__11l1111l111_opy_(f, instance, bstack1l1l1lllll1_opy_)
    def bstack11l11111111_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11ll1l11l11_opy_(instance):
            return
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l11ll1l11_opy_, False):
            return
        driver.execute_script(
            bstack111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᤊ").format(
                json.dumps(
                    {
                        bstack111l_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᤋ"): bstack111l_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᤌ"),
                        bstack111l_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᤍ"): {bstack111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᤎ"): result},
                    }
                )
            )
        )
        f.bstack1l11l1ll11_opy_(instance, bstack1l1111l111l_opy_.bstack11l11ll1l11_opy_, True)
    def bstack11l11111l11_opy_(self, context: bstack1l1lll111ll_opy_, bstack11l111111l1_opy_= True):
        if bstack11l111111l1_opy_:
            bstack11l1ll1ll1l_opy_ = self.bstack11ll1l11lll_opy_(context, reverse=True)
        else:
            bstack11l1ll1ll1l_opy_ = self.bstack11ll11llll1_opy_(context, reverse=True)
        return [f for f in bstack11l1ll1ll1l_opy_ if f[1].state != bstack11l1ll1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11llllll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __11l1111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᤏ")).get(bstack111l_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᤐ")):
            bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
            if not bstack11l1ll1ll1l_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᤑ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠨࠢᤒ"))
                return
            for bstack11l1l1ll1ll_opy_, _ in bstack11l1ll1ll1l_opy_:
                driver = bstack11l1l1ll1ll_opy_()
                status = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, None)
                if not status:
                    self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᤓ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠣࠤᤔ"))
                    return
                bstack11l11llll1l_opy_ = {bstack111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᤕ"): status.lower()}
                bstack11l11lll111_opy_ = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_, None)
                if status.lower() == bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᤖ") and bstack11l11lll111_opy_ is not None:
                    bstack11l11llll1l_opy_[bstack111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᤗ")] = bstack11l11lll111_opy_[0][bstack111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᤘ")][0] if isinstance(bstack11l11lll111_opy_, list) else str(bstack11l11lll111_opy_)
                driver.execute_script(
                    bstack111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᤙ").format(
                        json.dumps(
                            {
                                bstack111l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᤚ"): bstack111l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᤛ"),
                                bstack111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᤜ"): bstack11l11llll1l_opy_,
                            }
                        )
                    )
                )
            f.bstack1l11l1ll11_opy_(instance, bstack1l1111l111l_opy_.bstack11l11ll1l11_opy_, True)
    @measure(event_name=EVENTS.bstack1l1lllll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __11l1111l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᤝ")).get(bstack111l_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᤞ")):
            test_name = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦ᤟"))
                return
            bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
            if not bstack11l1ll1ll1l_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᤠ") + str(bstack1l1l1lllll1_opy_) + bstack111l_opy_ (u"ࠢࠣᤡ"))
                return
            for bstack11l1l1ll1ll_opy_, bstack11l11111l1l_opy_ in bstack11l1ll1ll1l_opy_:
                if not bstack1l11l11l11l_opy_.bstack11ll1l11l11_opy_(bstack11l11111l1l_opy_):
                    continue
                driver = bstack11l1l1ll1ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᤢ").format(
                        json.dumps(
                            {
                                bstack111l_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᤣ"): bstack111l_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᤤ"),
                                bstack111l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᤥ"): {bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᤦ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1l11l1ll11_opy_(instance, bstack1l1111l111l_opy_.bstack11l11lll1l1_opy_, True)
    def bstack11ll111l1ll_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        f: TestFramework,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111llllllll_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        bstack11l1ll1ll1l_opy_ = [d for d, _ in f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])]
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᤧ"))
            return
        if not bstack1ll1ll111_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᤨ"))
            return
        for bstack11l111111ll_opy_ in bstack11l1ll1ll1l_opy_:
            driver = bstack11l111111ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111l_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨᤩ") + str(timestamp)
            driver.execute_script(
                bstack111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᤪ").format(
                    json.dumps(
                        {
                            bstack111l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᤫ"): bstack111l_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨ᤬"),
                            bstack111l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᤭"): {
                                bstack111l_opy_ (u"ࠨࡴࡺࡲࡨࠦ᤮"): bstack111l_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦ᤯"),
                                bstack111l_opy_ (u"ࠣࡦࡤࡸࡦࠨᤰ"): data,
                                bstack111l_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣᤱ"): bstack111l_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤᤲ")
                            }
                        }
                    )
                )
            )
    def bstack11l1lll11ll_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        f: TestFramework,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111llllllll_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        keys = [
            bstack1l1111l111l_opy_.bstack11ll11ll111_opy_,
            bstack1l1111l111l_opy_.bstack11l1lll11l1_opy_,
        ]
        bstack11l1ll1ll1l_opy_ = []
        for key in keys:
            bstack11l1ll1ll1l_opy_.extend(f.bstack1ll111111ll_opy_(instance, key, []))
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡ࡯ࡻࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᤳ"))
            return
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11111ll_opy_, False):
            self.logger.debug(bstack111l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡃࡃࡖࠣࡥࡱࡸࡥࡢࡦࡼࠤࡨࡸࡥࡢࡶࡨࡨࠧᤴ"))
            return
        self.bstack11lllll1111_opy_()
        bstack1lllllll1ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᤵ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l11_opy_)
        req.test_framework_version = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
        req.test_framework_state = bstack1l1l1lllll1_opy_[0].name
        req.test_hook_state = bstack1l1l1lllll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
        for bstack11l1l1ll1ll_opy_, driver in bstack11l1ll1ll1l_opy_:
            bstack1l11llll111_opy_ = driver.data.get(bstack111l_opy_ (u"ࠢࡳࡣࡱ࡯ࠧᤶ"))
            bstack111lllllll1_opy_ = False
            if bstack1l11llll111_opy_ is None:
                bstack111lllllll1_opy_ = True
            else:
                try:
                    bstack111lllllll1_opy_ = int(bstack1l11llll111_opy_) == 1
                except (TypeError, ValueError):
                    bstack111lllllll1_opy_ = False
            if bstack111lllllll1_opy_:
                try:
                    webdriver = bstack11l1l1ll1ll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack111l_opy_ (u"࡙ࠣࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࠩࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠤࡪࡾࡰࡪࡴࡨࡨ࠮ࠨᤷ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣᤸ")
                        if bstack1l11l11l11l_opy_.bstack1ll111111ll_opy_(driver, bstack1l11l11l11l_opy_.bstack11l11111ll1_opy_, False)
                        else bstack111l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤ᤹")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l11l11l11l_opy_.bstack1ll111111ll_opy_(driver, bstack1l11l11l11l_opy_.bstack11l1ll111l_opy_, bstack111l_opy_ (u"ࠦࠧ᤺"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l11l11l11l_opy_.bstack1ll111111ll_opy_(driver, bstack1l11l11l11l_opy_.bstack1ll11111111_opy_, bstack111l_opy_ (u"ࠧࠨ᤻"))
                    caps = None
                    if hasattr(webdriver, bstack111l_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᤼")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack111l_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡦ࡬ࡶࡪࡩࡴ࡭ࡻࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᤽"))
                        except Exception as e:
                            self.logger.debug(bstack111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨ᤾") + str(e) + bstack111l_opy_ (u"ࠤࠥ᤿"))
                    try:
                        bstack11l11111lll_opy_ = json.dumps(caps).encode(bstack111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᥀")) if caps else bstack1l1l1l111l1_opy_ (u"ࠦࢀࢃࠢ᥁")
                        req.capabilities = bstack11l11111lll_opy_
                    except Exception as e:
                        self.logger.debug(bstack111l_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡧࡵ࡭ࡦࡲࡩࡻࡧࠣࡧࡦࡶࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࠣ᥂") + str(e) + bstack111l_opy_ (u"ࠨࠢ᥃"))
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡹ࡫࡭࠻ࠢࠥ᥄") + str(str(e)) + bstack111l_opy_ (u"ࠣࠤ᥅"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11llll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
        if not bstack1ll1ll111_opy_() and len(bstack11l1ll1ll1l_opy_) == 0:
            bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l1lll11l1_opy_, [])
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᥆") + str(kwargs) + bstack111l_opy_ (u"ࠥࠦ᥇"))
            return {}
        for bstack11l1l1ll1ll_opy_, bstack11l1l1l1lll_opy_ in bstack11l1ll1ll1l_opy_:
            bstack1l11llll111_opy_ = bstack11l1l1l1lll_opy_.data.get(bstack111l_opy_ (u"ࠫࡷࡧ࡮࡬ࠩ᥈"))
            self.logger.info(bstack111l_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭࠽ࠤࠧ᥉") + str(bstack1l11llll111_opy_) + bstack111l_opy_ (u"ࠨࠢ᥊"))
            if bstack1l11llll111_opy_ is None or bstack1l11llll111_opy_ == bstack111l_opy_ (u"ࠧ࠲ࠩ᥋"):
                driver = bstack11l1l1ll1ll_opy_()
                self.logger.debug(bstack111l_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡦࡦࡶࡦ࡬ࡪࡪࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࠤ᥌") + str(bstack11l1l1l1lll_opy_.data[bstack111l_opy_ (u"ࠩࡵࡥࡳࡱࠧ᥍")]) + bstack111l_opy_ (u"ࠥࠦ᥎"))
                if not driver:
                    self.logger.debug(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᥏") + str(kwargs) + bstack111l_opy_ (u"ࠧࠨᥐ"))
                    return {}
                capabilities = f.bstack1ll111111ll_opy_(bstack11l1l1l1lll_opy_, bstack1l11l11l11l_opy_.bstack1111lll1_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧᥑ") + str(capabilities) + bstack111l_opy_ (u"ࠢࠣᥒ"))
                if not capabilities:
                    self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᥓ") + str(kwargs) + bstack111l_opy_ (u"ࠤࠥᥔ"))
                    return {}
                return capabilities.get(bstack111l_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᥕ"), {})
        return None
    def bstack11llll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
        if not bstack1ll1ll111_opy_() and len(bstack11l1ll1ll1l_opy_) == 0:
            bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11l1lll11l1_opy_, [])
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᥖ") + str(kwargs) + bstack111l_opy_ (u"ࠧࠨᥗ"))
            return
        if len(bstack11l1ll1ll1l_opy_) > 1:
            self.logger.debug(bstack111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᥘ") + str(kwargs) + bstack111l_opy_ (u"ࠢࠣᥙ"))
        for bstack11l1l1ll1ll_opy_, bstack11l1l1l1lll_opy_ in bstack11l1ll1ll1l_opy_:
            driver = bstack11l1l1ll1ll_opy_()
            bstack1l11llll111_opy_ = bstack11l1l1l1lll_opy_.data.get(bstack111l_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᥚ"))
            self.logger.info(bstack111l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭࠽ࠤࠧᥛ") + str(bstack1l11llll111_opy_) + bstack111l_opy_ (u"ࠥࠦᥜ"))
            if (bstack1l11llll111_opy_ is None or int(bstack1l11llll111_opy_) == 1) and driver:
                return driver
        return None