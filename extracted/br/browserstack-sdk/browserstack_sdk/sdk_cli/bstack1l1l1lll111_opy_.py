# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1l1lll1111_opy_,
    bstack1ll11llllll_opy_,
    bstack1ll11lll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.bstack1l111lllll1_opy_ import bstack1l11l111111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack11l1111l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1ll111111_opy_(bstack1l11l111111_opy_):
    bstack11lll1l1l1l_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨᜍ")
    bstack11llllll11l_opy_ = bstack11lll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᜎ")
    bstack1l1111ll11l_opy_ = bstack11lll1_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᜏ")
    bstack11lll11l111_opy_ = bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᜐ")
    bstack11lll111l11_opy_ = bstack11lll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣᜑ")
    bstack1l1111111ll_opy_ = bstack11lll1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᜒ")
    bstack11lll111l1l_opy_ = bstack11lll1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᜓ")
    bstack11lll1111ll_opy_ = bstack11lll1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷ᜔ࠧ")
    def __init__(self):
        super().__init__(bstack1l11l1111ll_opy_=self.bstack11lll1l1l1l_opy_, frameworks=[bstack1ll111l11ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll11l1ll1_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l111111l_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack1l111llll1l_opy_ = self.bstack11ll11ll1ll_opy_(instance.context)
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀ᜕ࠦ") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠤࠥ᜖"))
        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, bstack1l111llll1l_opy_)
        bstack11ll11l1l11_opy_ = self.bstack11ll11ll1ll_opy_(instance.context, bstack11ll11l11ll_opy_=False)
        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll111111_opy_.bstack1l1111ll11l_opy_, bstack11ll11l1l11_opy_)
    def bstack1l1l111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11l1ll1_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if not f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11lll111l1l_opy_, False):
            self.__11ll11l111l_opy_(f,instance,bstack1ll1l111111_opy_)
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11l1ll1_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        if not f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11lll111l1l_opy_, False):
            self.__11ll11l111l_opy_(f, instance, bstack1ll1l111111_opy_)
        if not f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11lll1111ll_opy_, False):
            self.__11ll11ll111_opy_(f, instance, bstack1ll1l111111_opy_)
    def bstack11ll11l1111_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11l111l1l_opy_(instance):
            return
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11lll1111ll_opy_, False):
            return
        driver.execute_script(
            bstack11lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣ᜗").format(
                json.dumps(
                    {
                        bstack11lll1_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦ᜘"): bstack11lll1_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ᜙"),
                        bstack11lll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ᜚"): {bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᜛"): result},
                    }
                )
            )
        )
        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll111111_opy_.bstack11lll1111ll_opy_, True)
    def bstack11ll11ll1ll_opy_(self, context: bstack1ll11lll1ll_opy_, bstack11ll11l11ll_opy_= True):
        if bstack11ll11l11ll_opy_:
            bstack1l111llll1l_opy_ = self.bstack1l11l111l11_opy_(context, reverse=True)
        else:
            bstack1l111llll1l_opy_ = self.bstack1l11l11l1ll_opy_(context, reverse=True)
        return [f for f in bstack1l111llll1l_opy_ if f[1].state != bstack111ll1lll1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l1llll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def __11ll11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ᜜")).get(bstack11lll1_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ᜝")):
            bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
            if not bstack1l111llll1l_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ᜞") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠦࠧᜟ"))
                return
            for bstack11llll1llll_opy_, _ in bstack1l111llll1l_opy_:
                driver = bstack11llll1llll_opy_()
                status = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11lll11111l_opy_, None)
                if not status:
                    self.logger.debug(bstack11lll1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᜠ") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠨࠢᜡ"))
                    return
                bstack11lll1l1ll1_opy_ = {bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᜢ"): status.lower()}
                bstack11lll1l1lll_opy_ = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11lll1l1111_opy_, None)
                if status.lower() == bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜣ") and bstack11lll1l1lll_opy_ is not None:
                    bstack11lll1l1ll1_opy_[bstack11lll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᜤ")] = bstack11lll1l1lll_opy_[0][bstack11lll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᜥ")][0] if isinstance(bstack11lll1l1lll_opy_, list) else str(bstack11lll1l1lll_opy_)
                driver.execute_script(
                    bstack11lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᜦ").format(
                        json.dumps(
                            {
                                bstack11lll1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᜧ"): bstack11lll1_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᜨ"),
                                bstack11lll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᜩ"): bstack11lll1l1ll1_opy_,
                            }
                        )
                    )
                )
            f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll111111_opy_.bstack11lll1111ll_opy_, True)
    @measure(event_name=EVENTS.bstack1111l1llll_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def __11ll11l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨᜪ")).get(bstack11lll1_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᜫ")):
            test_name = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, None)
            if not test_name:
                self.logger.debug(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᜬ"))
                return
            bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
            if not bstack1l111llll1l_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᜭ") + str(bstack1ll1l111111_opy_) + bstack11lll1_opy_ (u"ࠧࠨᜮ"))
                return
            for bstack11llll1llll_opy_, bstack11ll11l1lll_opy_ in bstack1l111llll1l_opy_:
                if not bstack1ll111l11ll_opy_.bstack1l11l111l1l_opy_(bstack11ll11l1lll_opy_):
                    continue
                driver = bstack11llll1llll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11lll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᜯ").format(
                        json.dumps(
                            {
                                bstack11lll1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᜰ"): bstack11lll1_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᜱ"),
                                bstack11lll1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᜲ"): {bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᜳ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll111111_opy_.bstack11lll111l1l_opy_, True)
    def bstack1l111lll11l_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        f: TestFramework,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11l1ll1_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        bstack1l111llll1l_opy_ = [d for d, _ in f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])]
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮᜴ࠦ"))
            return
        if not bstack11l1111l1l_opy_():
            self.logger.debug(bstack11lll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ᜵"))
            return
        for bstack11ll11l1l1l_opy_ in bstack1l111llll1l_opy_:
            driver = bstack11ll11l1l1l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11lll1_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦ᜶") + str(timestamp)
            driver.execute_script(
                bstack11lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ᜷").format(
                    json.dumps(
                        {
                            bstack11lll1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ᜸"): bstack11lll1_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ᜹"),
                            bstack11lll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ᜺"): {
                                bstack11lll1_opy_ (u"ࠦࡹࡿࡰࡦࠤ᜻"): bstack11lll1_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤ᜼"),
                                bstack11lll1_opy_ (u"ࠨࡤࡢࡶࡤࠦ᜽"): data,
                                bstack11lll1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ᜾"): bstack11lll1_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢ᜿")
                            }
                        }
                    )
                )
            )
    def bstack1l111lll1ll_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        f: TestFramework,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11l1ll1_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        keys = [
            bstack1l1ll111111_opy_.bstack11llllll11l_opy_,
            bstack1l1ll111111_opy_.bstack1l1111ll11l_opy_,
        ]
        bstack1l111llll1l_opy_ = []
        for key in keys:
            bstack1l111llll1l_opy_.extend(f.bstack1ll1l1l1111_opy_(instance, key, []))
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᝀ"))
            return
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack1l1111111ll_opy_, False):
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᝁ"))
            return
        self.bstack1l1l1111l1l_opy_()
        bstack111ll1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᝂ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll111l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l111l11lll_opy_)
        req.test_framework_state = bstack1ll1l111111_opy_[0].name
        req.test_hook_state = bstack1ll1l111111_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
        for bstack11llll1llll_opy_, driver in bstack1l111llll1l_opy_:
            bstack1ll11l11ll1_opy_ = driver.data.get(bstack11lll1_opy_ (u"ࠧࡸࡡ࡯࡭ࠥᝃ"))
            bstack11ll11ll1l1_opy_ = False
            if bstack1ll11l11ll1_opy_ is None:
                bstack11ll11ll1l1_opy_ = True
            else:
                try:
                    bstack11ll11ll1l1_opy_ = int(bstack1ll11l11ll1_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll11ll1l1_opy_ = False
            if bstack11ll11ll1l1_opy_:
                try:
                    webdriver = bstack11llll1llll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack11lll1_opy_ (u"ࠨࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥ࠮ࡲࡦࡨࡨࡶࡪࡴࡣࡦࠢࡨࡼࡵ࡯ࡲࡦࡦࠬࠦᝄ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack11lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᝅ")
                        if bstack1ll111l11ll_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll111l11ll_opy_.bstack11ll111lll1_opy_, False)
                        else bstack11lll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᝆ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll111l11ll_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll111l11ll_opy_.bstack11l1111lll_opy_, bstack11lll1_opy_ (u"ࠤࠥᝇ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll111l11ll_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll111l11ll_opy_.bstack1ll1ll1ll1l_opy_, bstack11lll1_opy_ (u"ࠥࠦᝈ"))
                    caps = None
                    if hasattr(webdriver, bstack11lll1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᝉ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack11lll1_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᝊ"))
                        except Exception as e:
                            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠼ࠣࠦᝋ") + str(e) + bstack11lll1_opy_ (u"ࠢࠣᝌ"))
                    try:
                        bstack11ll111llll_opy_ = json.dumps(caps).encode(bstack11lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᝍ")) if caps else bstack11ll11l11l1_opy_ (u"ࠤࡾࢁࠧᝎ")
                        req.capabilities = bstack11ll111llll_opy_
                    except Exception as e:
                        self.logger.debug(bstack11lll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥࡹࡥࡳ࡫ࡤࡰ࡮ࢀࡥࠡࡥࡤࡴࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࠨᝏ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᝐ"))
                except Exception as e:
                    self.logger.error(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡷࡩࡲࡀࠠࠣᝑ") + str(str(e)) + bstack11lll1_opy_ (u"ࠨࠢᝒ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
        if not bstack11l1111l1l_opy_() and len(bstack1l111llll1l_opy_) == 0:
            bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack1l1111ll11l_opy_, [])
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝓ") + str(kwargs) + bstack11lll1_opy_ (u"ࠣࠤ᝔"))
            return {}
        for bstack11llll1llll_opy_, bstack11lllll111l_opy_ in bstack1l111llll1l_opy_:
            bstack1ll11l11ll1_opy_ = bstack11lllll111l_opy_.data.get(bstack11lll1_opy_ (u"ࠩࡵࡥࡳࡱࠧ᝕"))
            self.logger.info(bstack11lll1_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥ᝖") + str(bstack1ll11l11ll1_opy_) + bstack11lll1_opy_ (u"ࠦࠧ᝗"))
            if bstack1ll11l11ll1_opy_ is None or bstack1ll11l11ll1_opy_ == bstack11lll1_opy_ (u"ࠬ࠷ࠧ᝘"):
                driver = bstack11llll1llll_opy_()
                self.logger.debug(bstack11lll1_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤ࡫࡫ࡴࡤࡪࡨࡨࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࠢ᝙") + str(bstack11lllll111l_opy_.data[bstack11lll1_opy_ (u"ࠧࡳࡣࡱ࡯ࠬ᝚")]) + bstack11lll1_opy_ (u"ࠣࠤ᝛"))
                if not driver:
                    self.logger.debug(bstack11lll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᝜") + str(kwargs) + bstack11lll1_opy_ (u"ࠥࠦ᝝"))
                    return {}
                capabilities = f.bstack1ll1l1l1111_opy_(bstack11lllll111l_opy_, bstack1ll111l11ll_opy_.bstack1l1l111l11_opy_)
                self.logger.debug(bstack11lll1_opy_ (u"ࠦ࡬࡫࡮ࡦࡴࡤࡸࡪࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡦࡨࡸࡦ࡯࡬ࡴࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥ᝞") + str(capabilities) + bstack11lll1_opy_ (u"ࠧࠨ᝟"))
                if not capabilities:
                    self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᝠ") + str(kwargs) + bstack11lll1_opy_ (u"ࠢࠣᝡ"))
                    return {}
                return capabilities.get(bstack11lll1_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᝢ"), {})
        return None
    def bstack1l1l11l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
        if not bstack11l1111l1l_opy_() and len(bstack1l111llll1l_opy_) == 0:
            bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack1l1111ll11l_opy_, [])
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᝣ") + str(kwargs) + bstack11lll1_opy_ (u"ࠥࠦᝤ"))
            return
        if len(bstack1l111llll1l_opy_) > 1:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᝥ") + str(kwargs) + bstack11lll1_opy_ (u"ࠧࠨᝦ"))
        for bstack11llll1llll_opy_, bstack11lllll111l_opy_ in bstack1l111llll1l_opy_:
            driver = bstack11llll1llll_opy_()
            bstack1ll11l11ll1_opy_ = bstack11lllll111l_opy_.data.get(bstack11lll1_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᝧ"))
            self.logger.info(bstack11lll1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫࠻ࠢࠥᝨ") + str(bstack1ll11l11ll1_opy_) + bstack11lll1_opy_ (u"ࠣࠤᝩ"))
            if (bstack1ll11l11ll1_opy_ is None or int(bstack1ll11l11ll1_opy_) == 1) and driver:
                return driver
        return None