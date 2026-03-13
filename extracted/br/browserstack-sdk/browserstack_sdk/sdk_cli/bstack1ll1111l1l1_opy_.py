# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll11lll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1ll111_opy_ import bstack1l11l1l1l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack111l1ll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1ll11l1ll_opy_(bstack1l11l1l1l1l_opy_):
    bstack11llll11111_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᛒ")
    bstack1l111ll1l1l_opy_ = bstack1111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᛓ")
    bstack1l111l11lll_opy_ = bstack1111l_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᛔ")
    bstack11llll1l111_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᛕ")
    bstack11llll11lll_opy_ = bstack1111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᛖ")
    bstack1l1111lll1l_opy_ = bstack1111l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᛗ")
    bstack11llll1l11l_opy_ = bstack1111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᛘ")
    bstack11llll1ll1l_opy_ = bstack1111l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᛙ")
    def __init__(self):
        super().__init__(bstack1l11l1ll1ll_opy_=self.bstack11llll11111_opy_, frameworks=[bstack1ll111ll1ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll1l1l1l1_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l1lll_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l111lll11l_opy_ = self.bstack11ll1ll11l1_opy_(instance.context)
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᛚ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠨࠢᛛ"))
        f.bstack1ll1lllll11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, bstack1l111lll11l_opy_)
        bstack11ll1ll111l_opy_ = self.bstack11ll1ll11l1_opy_(instance.context, bstack11ll1l11lll_opy_=False)
        f.bstack1ll1lllll11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111l11lll_opy_, bstack11ll1ll111l_opy_)
    def bstack1l1l11l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1l1l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if not f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1l11l_opy_, False):
            self.__11ll1l1lll1_opy_(f,instance,bstack1ll1l111l11_opy_)
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1l1l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        if not f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1l11l_opy_, False):
            self.__11ll1l1lll1_opy_(f, instance, bstack1ll1l111l11_opy_)
        if not f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1ll1l_opy_, False):
            self.__11ll1l1ll1l_opy_(f, instance, bstack1ll1l111l11_opy_)
    def bstack11ll1ll11ll_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11l1l1lll_opy_(instance):
            return
        if f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1ll1l_opy_, False):
            return
        driver.execute_script(
            bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᛜ").format(
                json.dumps(
                    {
                        bstack1111l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᛝ"): bstack1111l_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᛞ"),
                        bstack1111l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᛟ"): {bstack1111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᛠ"): result},
                    }
                )
            )
        )
        f.bstack1ll1lllll11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1ll1l_opy_, True)
    def bstack11ll1ll11l1_opy_(self, context: bstack1ll11lll1l1_opy_, bstack11ll1l11lll_opy_= True):
        if bstack11ll1l11lll_opy_:
            bstack1l111lll11l_opy_ = self.bstack1l11ll11111_opy_(context, reverse=True)
        else:
            bstack1l111lll11l_opy_ = self.bstack1l11l1lll11_opy_(context, reverse=True)
        return [f for f in bstack1l111lll11l_opy_ if f[1].state != bstack1ll1l1l1lll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __11ll1l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᛡ")).get(bstack1111l_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᛢ")):
            bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
            if not bstack1l111lll11l_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᛣ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠣࠤᛤ"))
                return
            for bstack1l11111l11l_opy_, _ in bstack1l111lll11l_opy_:
                driver = bstack1l11111l11l_opy_()
                status = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11lll1ll1l1_opy_, None)
                if not status:
                    self.logger.debug(bstack1111l_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᛥ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠥࠦᛦ"))
                    return
                bstack11llll1ll11_opy_ = {bstack1111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᛧ"): status.lower()}
                bstack11llll11l1l_opy_ = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11llll11l11_opy_, None)
                if status.lower() == bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᛨ") and bstack11llll11l1l_opy_ is not None:
                    bstack11llll1ll11_opy_[bstack1111l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᛩ")] = bstack11llll11l1l_opy_[0][bstack1111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᛪ")][0] if isinstance(bstack11llll11l1l_opy_, list) else str(bstack11llll11l1l_opy_)
                driver.execute_script(
                    bstack1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨ᛫").format(
                        json.dumps(
                            {
                                bstack1111l_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ᛬"): bstack1111l_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ᛭"),
                                bstack1111l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᛮ"): bstack11llll1ll11_opy_,
                            }
                        )
                    )
                )
            f.bstack1ll1lllll11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1ll1l_opy_, True)
    @measure(event_name=EVENTS.bstack1lll1l1ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __11ll1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᛯ")).get(bstack1111l_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᛰ")):
            test_name = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_, None)
            if not test_name:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᛱ"))
                return
            bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
            if not bstack1l111lll11l_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᛲ") + str(bstack1ll1l111l11_opy_) + bstack1111l_opy_ (u"ࠤࠥᛳ"))
                return
            for bstack1l11111l11l_opy_, bstack11ll1l11ll1_opy_ in bstack1l111lll11l_opy_:
                if not bstack1ll111ll1ll_opy_.bstack1l11l1l1lll_opy_(bstack11ll1l11ll1_opy_):
                    continue
                driver = bstack1l11111l11l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᛴ").format(
                        json.dumps(
                            {
                                bstack1111l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᛵ"): bstack1111l_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᛶ"),
                                bstack1111l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᛷ"): {bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᛸ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1ll1lllll11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack11llll1l11l_opy_, True)
    def bstack1l111l111l1_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1l1l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        bstack1l111lll11l_opy_ = [d for d, _ in f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])]
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣ᛹"))
            return
        if not bstack111l1ll11l_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢ᛺"))
            return
        for bstack11ll1l1l11l_opy_ in bstack1l111lll11l_opy_:
            driver = bstack11ll1l1l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1111l_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣ᛻") + str(timestamp)
            driver.execute_script(
                bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤ᛼").format(
                    json.dumps(
                        {
                            bstack1111l_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ᛽"): bstack1111l_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ᛾"),
                            bstack1111l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ᛿"): {
                                bstack1111l_opy_ (u"ࠣࡶࡼࡴࡪࠨᜀ"): bstack1111l_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᜁ"),
                                bstack1111l_opy_ (u"ࠥࡨࡦࡺࡡࠣᜂ"): data,
                                bstack1111l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᜃ"): bstack1111l_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᜄ")
                            }
                        }
                    )
                )
            )
    def bstack1l11l1111ll_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        f: TestFramework,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll1l1l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        keys = [
            bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_,
            bstack1l1ll11l1ll_opy_.bstack1l111l11lll_opy_,
        ]
        bstack1l111lll11l_opy_ = []
        for key in keys:
            bstack1l111lll11l_opy_.extend(f.bstack1ll1lll1l11_opy_(instance, key, []))
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᜅ"))
            return
        if f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l1111lll1l_opy_, False):
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢᜆ"))
            return
        self.bstack1l1l111l1ll_opy_()
        bstack1lll1l11l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᜇ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_)
        req.test_framework_state = bstack1ll1l111l11_opy_[0].name
        req.test_hook_state = bstack1ll1l111l11_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        for bstack1l11111l11l_opy_, driver in bstack1l111lll11l_opy_:
            bstack1ll11lll11l_opy_ = driver.data.get(bstack1111l_opy_ (u"ࠤࡵࡥࡳࡱࠢᜈ"))
            bstack11ll1l1l1ll_opy_ = False
            if bstack1ll11lll11l_opy_ is None:
                bstack11ll1l1l1ll_opy_ = True
            else:
                try:
                    bstack11ll1l1l1ll_opy_ = int(bstack1ll11lll11l_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll1l1l1ll_opy_ = False
            if bstack11ll1l1l1ll_opy_:
                try:
                    webdriver = bstack1l11111l11l_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1111l_opy_ (u"࡛ࠥࡪࡨࡄࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࠫࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࠦࡥࡹࡲ࡬ࡶࡪࡪࠩࠣᜉ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥᜊ")
                        if bstack1ll111ll1ll_opy_.bstack1ll1lll1l11_opy_(driver, bstack1ll111ll1ll_opy_.bstack11ll1ll1111_opy_, False)
                        else bstack1111l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦᜋ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll111ll1ll_opy_.bstack1ll1lll1l11_opy_(driver, bstack1ll111ll1ll_opy_.bstack1lll1111ll1_opy_, bstack1111l_opy_ (u"ࠨࠢᜌ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll111ll1ll_opy_.bstack1ll1lll1l11_opy_(driver, bstack1ll111ll1ll_opy_.bstack1ll1llll1l1_opy_, bstack1111l_opy_ (u"ࠢࠣᜍ"))
                    caps = None
                    if hasattr(webdriver, bstack1111l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᜎ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1111l_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡨ࡮ࡸࡥࡤࡶ࡯ࡽࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᜏ"))
                        except Exception as e:
                            self.logger.debug(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࠣᜐ") + str(e) + bstack1111l_opy_ (u"ࠦࠧᜑ"))
                    try:
                        bstack11ll1l1llll_opy_ = json.dumps(caps).encode(bstack1111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᜒ")) if caps else bstack11ll1l1l111_opy_ (u"ࠨࡻࡾࠤᜓ")
                        req.capabilities = bstack11ll1l1llll_opy_
                    except Exception as e:
                        self.logger.debug(bstack1111l_opy_ (u"ࠢࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡶࡩࡷ࡯ࡡ࡭࡫ࡽࡩࠥࡩࡡࡱࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠻᜔ࠢࠥ") + str(e) + bstack1111l_opy_ (u"ࠣࠤ᜕"))
                except Exception as e:
                    self.logger.error(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯ࡴࡦ࡯࠽ࠤࠧ᜖") + str(str(e)) + bstack1111l_opy_ (u"ࠥࠦ᜗"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack111l1ll11l_opy_() and len(bstack1l111lll11l_opy_) == 0:
            bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111l11lll_opy_, [])
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᜘") + str(kwargs) + bstack1111l_opy_ (u"ࠧࠨ᜙"))
            return {}
        for bstack1l11111l11l_opy_, bstack1l111111ll1_opy_ in bstack1l111lll11l_opy_:
            bstack1ll11lll11l_opy_ = bstack1l111111ll1_opy_.data.get(bstack1111l_opy_ (u"࠭ࡲࡢࡰ࡮ࠫ᜚"))
            self.logger.info(bstack1111l_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢ᜛") + str(bstack1ll11lll11l_opy_) + bstack1111l_opy_ (u"ࠣࠤ᜜"))
            if bstack1ll11lll11l_opy_ is None or bstack1ll11lll11l_opy_ == bstack1111l_opy_ (u"ࠩ࠴ࠫ᜝"):
                driver = bstack1l11111l11l_opy_()
                self.logger.debug(bstack1111l_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡨࡨࡸࡨ࡮ࡥࡥࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࠦ᜞") + str(bstack1l111111ll1_opy_.data[bstack1111l_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᜟ")]) + bstack1111l_opy_ (u"ࠧࠨᜠ"))
                if not driver:
                    self.logger.debug(bstack1111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᜡ") + str(kwargs) + bstack1111l_opy_ (u"ࠢࠣᜢ"))
                    return {}
                capabilities = f.bstack1ll1lll1l11_opy_(bstack1l111111ll1_opy_, bstack1ll111ll1ll_opy_.bstack1ll1lll1lll_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᜣ") + str(capabilities) + bstack1111l_opy_ (u"ࠤࠥᜤ"))
                if not capabilities:
                    self.logger.debug(bstack1111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᜥ") + str(kwargs) + bstack1111l_opy_ (u"ࠦࠧᜦ"))
                    return {}
                return capabilities.get(bstack1111l_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᜧ"), {})
        return None
    def bstack1l1l1l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack111l1ll11l_opy_() and len(bstack1l111lll11l_opy_) == 0:
            bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111l11lll_opy_, [])
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᜨ") + str(kwargs) + bstack1111l_opy_ (u"ࠢࠣᜩ"))
            return
        if len(bstack1l111lll11l_opy_) > 1:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᜪ") + str(kwargs) + bstack1111l_opy_ (u"ࠤࠥᜫ"))
        for bstack1l11111l11l_opy_, bstack1l111111ll1_opy_ in bstack1l111lll11l_opy_:
            driver = bstack1l11111l11l_opy_()
            bstack1ll11lll11l_opy_ = bstack1l111111ll1_opy_.data.get(bstack1111l_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᜬ"))
            self.logger.info(bstack1111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡳࡣࡱ࡯࠿ࠦࠢᜭ") + str(bstack1ll11lll11l_opy_) + bstack1111l_opy_ (u"ࠧࠨᜮ"))
            if (bstack1ll11lll11l_opy_ is None or int(bstack1ll11lll11l_opy_) == 1) and driver:
                return driver
        return None