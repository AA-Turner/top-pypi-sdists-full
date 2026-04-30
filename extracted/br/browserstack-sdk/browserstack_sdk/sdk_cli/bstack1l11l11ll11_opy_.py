# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack11l1l1ll11_opy_,
    bstack1l1ll11l1ll_opy_,
    bstack1l1ll1ll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l11l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lll1l_opy_ import bstack11llll111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1lllllll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l11l11111l_opy_(bstack11llll111ll_opy_):
    bstack11l1l1ll111_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᢊ")
    bstack11ll1lllll1_opy_ = bstack1l1111l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᢋ")
    bstack11ll1lll11l_opy_ = bstack1l1111l_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᢌ")
    bstack11l1l1ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᢍ")
    bstack11l1l1l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᢎ")
    bstack11ll1l1lll1_opy_ = bstack1l1111l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᢏ")
    bstack11l1l1lll1l_opy_ = bstack1l1111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᢐ")
    bstack11l1l1ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᢑ")
    def __init__(self):
        super().__init__(bstack11llll111l1_opy_=self.bstack11l1l1ll111_opy_, frameworks=[bstack1l1l111l111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l11l1ll11_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111111ll_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11l1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1l11111_opy_ = self.bstack11l11l1l1l1_opy_(instance.context)
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᢒ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠧࠨᢓ"))
        f.bstack111l1llll1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, bstack11ll1l11111_opy_)
        bstack11l11l11l11_opy_ = self.bstack11l11l1l1l1_opy_(instance.context, bstack11l11l11ll1_opy_=False)
        f.bstack111l1llll1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lll11l_opy_, bstack11l11l11l11_opy_)
    def bstack1l1111111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll11_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if not f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1lll1l_opy_, False):
            self.__11l11l11lll_opy_(f,instance,bstack1l1ll1ll111_opy_)
    def bstack1l1111ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll11_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        if not f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1lll1l_opy_, False):
            self.__11l11l11lll_opy_(f, instance, bstack1l1ll1ll111_opy_)
        if not f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1ll1l1_opy_, False):
            self.__11l11l111l1_opy_(f, instance, bstack1l1ll1ll111_opy_)
    def bstack11l11l1l1ll_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack11lll1l1ll1_opy_(instance):
            return
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1ll1l1_opy_, False):
            return
        driver.execute_script(
            bstack1l1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᢔ").format(
                json.dumps(
                    {
                        bstack1l1111l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᢕ"): bstack1l1111l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᢖ"),
                        bstack1l1111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᢗ"): {bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᢘ"): result},
                    }
                )
            )
        )
        f.bstack111l1llll1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1ll1l1_opy_, True)
    def bstack11l11l1l1l1_opy_(self, context: bstack1l1ll1ll11l_opy_, bstack11l11l11ll1_opy_= True):
        if bstack11l11l11ll1_opy_:
            bstack11ll1l11111_opy_ = self.bstack11lll1ll111_opy_(context, reverse=True)
        else:
            bstack11ll1l11111_opy_ = self.bstack11llll11111_opy_(context, reverse=True)
        return [f for f in bstack11ll1l11111_opy_ if f[1].state != bstack1lll11l1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack111ll11111_opy_)
    def __11l11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᢙ")).get(bstack1l1111l_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᢚ")):
            bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
            if not bstack11ll1l11111_opy_:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᢛ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠢࠣᢜ"))
                return
            for bstack11ll11111ll_opy_, _ in bstack11ll1l11111_opy_:
                driver = bstack11ll11111ll_opy_()
                status = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l1ll1111l_opy_, None)
                if not status:
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᢝ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠤࠥᢞ"))
                    return
                bstack11l1ll11ll1_opy_ = {bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᢟ"): status.lower()}
                bstack11l1ll111l1_opy_ = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_, None)
                if status.lower() == bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᢠ") and bstack11l1ll111l1_opy_ is not None:
                    bstack11l1ll11ll1_opy_[bstack1l1111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᢡ")] = bstack11l1ll111l1_opy_[0][bstack1l1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᢢ")][0] if isinstance(bstack11l1ll111l1_opy_, list) else str(bstack11l1ll111l1_opy_)
                driver.execute_script(
                    bstack1l1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᢣ").format(
                        json.dumps(
                            {
                                bstack1l1111l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᢤ"): bstack1l1111l_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᢥ"),
                                bstack1l1111l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᢦ"): bstack11l1ll11ll1_opy_,
                            }
                        )
                    )
                )
            f.bstack111l1llll1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1ll1l1_opy_, True)
    @measure(event_name=EVENTS.bstack1l1ll1l11l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def __11l11l11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤᢧ")).get(bstack1l1111l_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᢨ")):
            test_name = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11l11l11l1l_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩᢩࠧ"))
                return
            bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
            if not bstack11ll1l11111_opy_:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᢪ") + str(bstack1l1ll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠣࠤ᢫"))
                return
            for bstack11ll11111ll_opy_, bstack11l11l1ll1l_opy_ in bstack11ll1l11111_opy_:
                if not bstack1l1l111l111_opy_.bstack11lll1l1ll1_opy_(bstack11l11l1ll1l_opy_):
                    continue
                driver = bstack11ll11111ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢ᢬").format(
                        json.dumps(
                            {
                                bstack1l1111l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥ᢭"): bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ᢮"),
                                bstack1l1111l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᢯"): {bstack1l1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᢰ"): test_name},
                            }
                        )
                    )
                )
            f.bstack111l1llll1_opy_(instance, bstack1l11l11111l_opy_.bstack11l1l1lll1l_opy_, True)
    def bstack11ll11l1ll1_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        f: TestFramework,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll11_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        bstack11ll1l11111_opy_ = [d for d, _ in f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])]
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᢱ"))
            return
        if not bstack1lllllll11l_opy_():
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᢲ"))
            return
        for bstack11l11l1l111_opy_ in bstack11ll1l11111_opy_:
            driver = bstack11l11l1l111_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1111l_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢᢳ") + str(timestamp)
            driver.execute_script(
                bstack1l1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᢴ").format(
                    json.dumps(
                        {
                            bstack1l1111l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᢵ"): bstack1l1111l_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢᢶ"),
                            bstack1l1111l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᢷ"): {
                                bstack1l1111l_opy_ (u"ࠢࡵࡻࡳࡩࠧᢸ"): bstack1l1111l_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧᢹ"),
                                bstack1l1111l_opy_ (u"ࠤࡧࡥࡹࡧࠢᢺ"): data,
                                bstack1l1111l_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᢻ"): bstack1l1111l_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥᢼ")
                            }
                        }
                    )
                )
            )
    def bstack11ll1l1l111_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        f: TestFramework,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l11l1ll11_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        keys = [
            bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_,
            bstack1l11l11111l_opy_.bstack11ll1lll11l_opy_,
        ]
        bstack11ll1l11111_opy_ = []
        for key in keys:
            bstack11ll1l11111_opy_.extend(f.bstack1ll1111l1l1_opy_(instance, key, []))
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢᢽ"))
            return
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1l1lll1_opy_, False):
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨᢾ"))
            return
        self.bstack1l1111l1ll1_opy_()
        bstack11l11l1l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᢿ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l11111l11l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11ll11l1lll_opy_)
        req.test_framework_state = bstack1l1ll1ll111_opy_[0].name
        req.test_hook_state = bstack1l1ll1ll111_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_)
        for bstack11ll11111ll_opy_, driver in bstack11ll1l11111_opy_:
            bstack1l1ll11l111_opy_ = driver.data.get(bstack1l1111l_opy_ (u"ࠣࡴࡤࡲࡰࠨᣀ"))
            bstack11l11l1111l_opy_ = False
            if bstack1l1ll11l111_opy_ is None:
                bstack11l11l1111l_opy_ = True
            else:
                try:
                    bstack11l11l1111l_opy_ = int(bstack1l1ll11l111_opy_) == 1
                except (TypeError, ValueError):
                    bstack11l11l1111l_opy_ = False
            if bstack11l11l1111l_opy_:
                try:
                    webdriver = bstack11ll11111ll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1l1111l_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢᣁ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1l1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᣂ")
                        if bstack1l1l111l111_opy_.bstack1ll1111l1l1_opy_(driver, bstack1l1l111l111_opy_.bstack11l11l1l11l_opy_, False)
                        else bstack1l1111l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᣃ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1l1l111l111_opy_.bstack1ll1111l1l1_opy_(driver, bstack1l1l111l111_opy_.bstack11111llll_opy_, bstack1l1111l_opy_ (u"ࠧࠨᣄ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1l1l111l111_opy_.bstack1ll1111l1l1_opy_(driver, bstack1l1l111l111_opy_.bstack1l1lllll1l1_opy_, bstack1l1111l_opy_ (u"ࠨࠢᣅ"))
                    caps = None
                    if hasattr(webdriver, bstack1l1111l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᣆ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡧ࡭ࡷ࡫ࡣࡵ࡮ࡼࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᣇ"))
                        except Exception as e:
                            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᣈ") + str(e) + bstack1l1111l_opy_ (u"ࠥࠦᣉ"))
                    try:
                        bstack11l11l111ll_opy_ = json.dumps(caps).encode(bstack1l1111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᣊ")) if caps else bstack11l11l11111_opy_ (u"ࠧࢁࡽࠣᣋ")
                        req.capabilities = bstack11l11l111ll_opy_
                    except Exception as e:
                        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡵࡨࡶ࡮ࡧ࡬ࡪࡼࡨࠤࡨࡧࡰࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࠤᣌ") + str(e) + bstack1l1111l_opy_ (u"ࠢࠣᣍ"))
                except Exception as e:
                    self.logger.error(bstack1l1111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡺࡥ࡮࠼ࠣࠦᣎ") + str(str(e)) + bstack1l1111l_opy_ (u"ࠤࠥᣏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11lllllllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack1lllllll11l_opy_() and len(bstack11ll1l11111_opy_) == 0:
            bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lll11l_opy_, [])
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᣐ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠦࠧᣑ"))
            return {}
        for bstack11ll11111ll_opy_, bstack11ll1111111_opy_ in bstack11ll1l11111_opy_:
            bstack1l1ll11l111_opy_ = bstack11ll1111111_opy_.data.get(bstack1l1111l_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᣒ"))
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨᣓ") + str(bstack1l1ll11l111_opy_) + bstack1l1111l_opy_ (u"ࠢࠣᣔ"))
            if bstack1l1ll11l111_opy_ is None or bstack1l1ll11l111_opy_ == bstack1l1111l_opy_ (u"ࠨ࠳ࠪᣕ"):
                driver = bstack11ll11111ll_opy_()
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡧࡧࡷࡧ࡭࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࠥᣖ") + str(bstack11ll1111111_opy_.data[bstack1l1111l_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᣗ")]) + bstack1l1111l_opy_ (u"ࠦࠧᣘ"))
                if not driver:
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᣙ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢᣚ"))
                    return {}
                capabilities = f.bstack1ll1111l1l1_opy_(bstack11ll1111111_opy_, bstack1l1l111l111_opy_.bstack1l111111l_opy_)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᣛ") + str(capabilities) + bstack1l1111l_opy_ (u"ࠣࠤᣜ"))
                if not capabilities:
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᣝ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠥࠦᣞ"))
                    return {}
                return capabilities.get(bstack1l1111l_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᣟ"), {})
        return None
    def bstack1l11111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack1lllllll11l_opy_() and len(bstack11ll1l11111_opy_) == 0:
            bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lll11l_opy_, [])
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᣠ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢᣡ"))
            return
        if len(bstack11ll1l11111_opy_) > 1:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᣢ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠣࠤᣣ"))
        for bstack11ll11111ll_opy_, bstack11ll1111111_opy_ in bstack11ll1l11111_opy_:
            driver = bstack11ll11111ll_opy_()
            bstack1l1ll11l111_opy_ = bstack11ll1111111_opy_.data.get(bstack1l1111l_opy_ (u"ࠩࡵࡥࡳࡱࠧᣤ"))
            self.logger.info(bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮࠾ࠥࠨᣥ") + str(bstack1l1ll11l111_opy_) + bstack1l1111l_opy_ (u"ࠦࠧᣦ"))
            if (bstack1l1ll11l111_opy_ is None or int(bstack1l1ll11l111_opy_) == 1) and driver:
                return driver
        return None