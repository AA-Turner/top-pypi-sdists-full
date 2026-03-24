# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack111lll11l_opy_,
    bstack1ll11l1l111_opy_,
    bstack1ll11ll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111l1_opy_ import bstack1l11l111lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l11l1111l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1ll1ll1l1_opy_(bstack1l11l111lll_opy_):
    bstack11lll11111l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᜐ")
    bstack11lllll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᜑ")
    bstack1l111ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᜒ")
    bstack11lll1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᜓ")
    bstack11lll111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶ᜔ࠦ")
    bstack1l1111lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪ᜕ࠢ")
    bstack11lll1l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧ᜖")
    bstack11lll1l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣ᜗")
    def __init__(self):
        super().__init__(bstack1l11l11l1l1_opy_=self.bstack11lll11111l_opy_, frameworks=[bstack1l1llll1111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll11ll111_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11ll1lll1_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l11111ll11_opy_ = self.bstack11ll111ll11_opy_(instance.context)
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ᜘") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠧࠨ᜙"))
        f.bstack1l1l11lll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, bstack1l11111ll11_opy_)
        bstack11ll11l1l11_opy_ = self.bstack11ll111ll11_opy_(instance.context, bstack11ll11l1111_opy_=False)
        f.bstack1l1l11lll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack1l111ll1111_opy_, bstack11ll11l1l11_opy_)
    def bstack1l11ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11ll111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if not f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l11ll_opy_, False):
            self.__11ll11l11ll_opy_(f,instance,bstack1ll11l1ll11_opy_)
    def bstack1l11lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11ll111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        if not f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l11ll_opy_, False):
            self.__11ll11l11ll_opy_(f, instance, bstack1ll11l1ll11_opy_)
        if not f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l1l11_opy_, False):
            self.__11ll11l11l1_opy_(f, instance, bstack1ll11l1ll11_opy_)
    def bstack11ll111l1ll_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l111lllll1_opy_(instance):
            return
        if f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l1l11_opy_, False):
            return
        driver.execute_script(
            bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦ᜚").format(
                json.dumps(
                    {
                        bstack1ll1lll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢ᜛"): bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ᜜"),
                        bstack1ll1lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ᜝"): {bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᜞"): result},
                    }
                )
            )
        )
        f.bstack1l1l11lll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l1l11_opy_, True)
    def bstack11ll111ll11_opy_(self, context: bstack1ll11ll1ll1_opy_, bstack11ll11l1111_opy_= True):
        if bstack11ll11l1111_opy_:
            bstack1l11111ll11_opy_ = self.bstack1l11l111l11_opy_(context, reverse=True)
        else:
            bstack1l11111ll11_opy_ = self.bstack1l11l111l1l_opy_(context, reverse=True)
        return [f for f in bstack1l11111ll11_opy_ if f[1].state != bstack111l11ll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l1ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __11ll11l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᜟ")).get(bstack1ll1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᜠ")):
            bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
            if not bstack1l11111ll11_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᜡ") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣᜢ"))
                return
            for bstack11llll1llll_opy_, _ in bstack1l11111ll11_opy_:
                driver = bstack11llll1llll_opy_()
                status = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11lll11ll11_opy_, None)
                if not status:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᜣ") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᜤ"))
                    return
                bstack11lll1l11l1_opy_ = {bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᜥ"): status.lower()}
                bstack11ll1lllll1_opy_ = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11lll11ll1l_opy_, None)
                if status.lower() == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᜦ") and bstack11ll1lllll1_opy_ is not None:
                    bstack11lll1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᜧ")] = bstack11ll1lllll1_opy_[0][bstack1ll1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᜨ")][0] if isinstance(bstack11ll1lllll1_opy_, list) else str(bstack11ll1lllll1_opy_)
                driver.execute_script(
                    bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᜩ").format(
                        json.dumps(
                            {
                                bstack1ll1lll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᜪ"): bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᜫ"),
                                bstack1ll1lll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᜬ"): bstack11lll1l11l1_opy_,
                            }
                        )
                    )
                )
            f.bstack1l1l11lll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l1l11_opy_, True)
    @measure(event_name=EVENTS.bstack1l1l1l11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __11ll11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᜭ")).get(bstack1ll1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᜮ")):
            test_name = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11ll111llll_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᜯ"))
                return
            bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
            if not bstack1l11111ll11_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᜰ") + str(bstack1ll11l1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᜱ"))
                return
            for bstack11llll1llll_opy_, bstack11ll111lll1_opy_ in bstack1l11111ll11_opy_:
                if not bstack1l1llll1111_opy_.bstack1l111lllll1_opy_(bstack11ll111lll1_opy_):
                    continue
                driver = bstack11llll1llll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᜲ").format(
                        json.dumps(
                            {
                                bstack1ll1lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᜳ"): bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩ᜴ࠧ"),
                                bstack1ll1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᜵"): {bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᜶"): test_name},
                            }
                        )
                    )
                )
            f.bstack1l1l11lll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lll1l11ll_opy_, True)
    def bstack1l11111l1l1_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11ll111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        bstack1l11111ll11_opy_ = [d for d, _ in f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])]
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢ᜷"))
            return
        if not bstack1l11l1111l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᜸"))
            return
        for bstack11ll11l1ll1_opy_ in bstack1l11111ll11_opy_:
            driver = bstack11ll11l1ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll1lll_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢ᜹") + str(timestamp)
            driver.execute_script(
                bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣ᜺").format(
                    json.dumps(
                        {
                            bstack1ll1lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦ᜻"): bstack1ll1lll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ᜼"),
                            bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ᜽"): {
                                bstack1ll1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᜾"): bstack1ll1lll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧ᜿"),
                                bstack1ll1lll_opy_ (u"ࠤࡧࡥࡹࡧࠢᝀ"): data,
                                bstack1ll1lll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᝁ"): bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᝂ")
                            }
                        }
                    )
                )
            )
    def bstack1l1111ll1ll_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11ll111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        keys = [
            bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_,
            bstack1l1ll1ll1l1_opy_.bstack1l111ll1111_opy_,
        ]
        bstack1l11111ll11_opy_ = []
        for key in keys:
            bstack1l11111ll11_opy_.extend(f.bstack1ll1lll11ll_opy_(instance, key, []))
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᝃ"))
            return
        if f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack1l1111lll1l_opy_, False):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨᝄ"))
            return
        self.bstack1l11l1ll111_opy_()
        bstack1ll1l111l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11llll111_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᝅ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11lll111l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1111l1ll1_opy_)
        req.test_framework_state = bstack1ll11l1ll11_opy_[0].name
        req.test_hook_state = bstack1ll11l1ll11_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        for bstack11llll1llll_opy_, driver in bstack1l11111ll11_opy_:
            bstack1ll11l1llll_opy_ = driver.data.get(bstack1ll1lll_opy_ (u"ࠣࡴࡤࡲࡰࠨᝆ"))
            bstack11ll11l1l1l_opy_ = False
            if bstack1ll11l1llll_opy_ is None:
                bstack11ll11l1l1l_opy_ = True
            else:
                try:
                    bstack11ll11l1l1l_opy_ = int(bstack1ll11l1llll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll11l1l1l_opy_ = False
            if bstack11ll11l1l1l_opy_:
                try:
                    webdriver = bstack11llll1llll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢᝇ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᝈ")
                        if bstack1l1llll1111_opy_.bstack1ll1lll11ll_opy_(driver, bstack1l1llll1111_opy_.bstack11ll11l1lll_opy_, False)
                        else bstack1ll1lll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᝉ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l1llll1111_opy_.bstack1ll1lll11ll_opy_(driver, bstack1l1llll1111_opy_.bstack1l111ll111_opy_, bstack1ll1lll_opy_ (u"ࠧࠨᝊ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l1llll1111_opy_.bstack1ll1lll11ll_opy_(driver, bstack1l1llll1111_opy_.bstack1ll1l1l111l_opy_, bstack1ll1lll_opy_ (u"ࠨࠢᝋ"))
                    caps = None
                    if hasattr(webdriver, bstack1ll1lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᝌ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡧ࡭ࡷ࡫ࡣࡵ࡮ࡼࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᝍ"))
                        except Exception as e:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᝎ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᝏ"))
                    try:
                        bstack11ll11l111l_opy_ = json.dumps(caps).encode(bstack1ll1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᝐ")) if caps else bstack11ll111ll1l_opy_ (u"ࠧࢁࡽࠣᝑ")
                        req.capabilities = bstack11ll11l111l_opy_
                    except Exception as e:
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡵࡨࡶ࡮ࡧ࡬ࡪࡼࡨࠤࡨࡧࡰࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࠤᝒ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᝓ"))
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡺࡥ࡮࠼ࠣࠦ᝔") + str(str(e)) + bstack1ll1lll_opy_ (u"ࠤࠥ᝕"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11lll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
        if not bstack1l11l1111l_opy_() and len(bstack1l11111ll11_opy_) == 0:
            bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack1l111ll1111_opy_, [])
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᝖") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧ᝗"))
            return {}
        for bstack11llll1llll_opy_, bstack11llll1ll11_opy_ in bstack1l11111ll11_opy_:
            bstack1ll11l1llll_opy_ = bstack11llll1ll11_opy_.data.get(bstack1ll1lll_opy_ (u"ࠬࡸࡡ࡯࡭ࠪ᝘"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨ᝙") + str(bstack1ll11l1llll_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣ᝚"))
            if bstack1ll11l1llll_opy_ is None or bstack1ll11l1llll_opy_ == bstack1ll1lll_opy_ (u"ࠨ࠳ࠪ᝛"):
                driver = bstack11llll1llll_opy_()
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡧࡧࡷࡧ࡭࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࠥ᝜") + str(bstack11llll1ll11_opy_.data[bstack1ll1lll_opy_ (u"ࠪࡶࡦࡴ࡫ࠨ᝝")]) + bstack1ll1lll_opy_ (u"ࠦࠧ᝞"))
                if not driver:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᝟") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᝠ"))
                    return {}
                capabilities = f.bstack1ll1lll11ll_opy_(bstack11llll1ll11_opy_, bstack1l1llll1111_opy_.bstack11111l11l_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᝡ") + str(capabilities) + bstack1ll1lll_opy_ (u"ࠣࠤᝢ"))
                if not capabilities:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝣ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᝤ"))
                    return {}
                return capabilities.get(bstack1ll1lll_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᝥ"), {})
        return None
    def bstack1l1l11l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
        if not bstack1l11l1111l_opy_() and len(bstack1l11111ll11_opy_) == 0:
            bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack1l111ll1111_opy_, [])
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᝦ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᝧ"))
            return
        if len(bstack1l11111ll11_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝨ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠣࠤᝩ"))
        for bstack11llll1llll_opy_, bstack11llll1ll11_opy_ in bstack1l11111ll11_opy_:
            driver = bstack11llll1llll_opy_()
            bstack1ll11l1llll_opy_ = bstack11llll1ll11_opy_.data.get(bstack1ll1lll_opy_ (u"ࠩࡵࡥࡳࡱࠧᝪ"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨᝫ") + str(bstack1ll11l1llll_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᝬ"))
            if (bstack1ll11l1llll_opy_ is None or int(bstack1ll11l1llll_opy_) == 1) and driver:
                return driver
        return None