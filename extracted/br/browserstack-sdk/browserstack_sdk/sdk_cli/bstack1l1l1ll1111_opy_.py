# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack11ll11l1_opy_,
    bstack1ll11ll1l11_opy_,
    bstack1ll11l1l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l111ll1ll1_opy_ import bstack1l11l1111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack11lll11l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1llll11ll_opy_(bstack1l11l1111ll_opy_):
    bstack11lll111l11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᜨ")
    bstack1l1111ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᜩ")
    bstack11lllllll1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᜪ")
    bstack11ll1ll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᜫ")
    bstack11lll11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᜬ")
    bstack11lllll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᜭ")
    bstack11lll11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᜮ")
    bstack11lll11l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᜯ")
    def __init__(self):
        super().__init__(bstack1l111lll11l_opy_=self.bstack11lll111l11_opy_, frameworks=[bstack1ll111l1111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll111ll11_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11lllll11_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lllll1lll_opy_ = self.bstack11ll1111ll1_opy_(instance.context)
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᜰ") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᜱ"))
        f.bstack1lll1111ll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, bstack11lllll1lll_opy_)
        bstack11ll111llll_opy_ = self.bstack11ll1111ll1_opy_(instance.context, bstack11ll111l1l1_opy_=False)
        f.bstack1lll1111ll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lllllll1l_opy_, bstack11ll111llll_opy_)
    def bstack1l11lllll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll111ll11_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if not f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1l1_opy_, False):
            self.__11ll11111ll_opy_(f,instance,bstack1ll11l1l111_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll111ll11_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        if not f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1l1_opy_, False):
            self.__11ll11111ll_opy_(f, instance, bstack1ll11l1l111_opy_)
        if not f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1ll_opy_, False):
            self.__11ll111l111_opy_(f, instance, bstack1ll11l1l111_opy_)
    def bstack11ll111ll1l_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l111lll1l1_opy_(instance):
            return
        if f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1ll_opy_, False):
            return
        driver.execute_script(
            bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᜲ").format(
                json.dumps(
                    {
                        bstack1ll1lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᜳ"): bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹ᜴ࠢ"),
                        bstack1ll1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᜵"): {bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᜶"): result},
                    }
                )
            )
        )
        f.bstack1lll1111ll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1ll_opy_, True)
    def bstack11ll1111ll1_opy_(self, context: bstack1ll11l1l1l1_opy_, bstack11ll111l1l1_opy_= True):
        if bstack11ll111l1l1_opy_:
            bstack11lllll1lll_opy_ = self.bstack1l11l1111l1_opy_(context, reverse=True)
        else:
            bstack11lllll1lll_opy_ = self.bstack1l111llll11_opy_(context, reverse=True)
        return [f for f in bstack11lllll1lll_opy_ if f[1].state != bstack11lll111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l111l111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __11ll111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧ᜷")).get(bstack1ll1lll_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ᜸")):
            bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack11lllll1lll_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧ᜹") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦ᜺"))
                return
            for bstack11llll111ll_opy_, _ in bstack11lllll1lll_opy_:
                driver = bstack11llll111ll_opy_()
                status = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11lll1111ll_opy_, None)
                if not status:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ᜻") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠧࠨ᜼"))
                    return
                bstack11lll1111l1_opy_ = {bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᜽"): status.lower()}
                bstack11lll111ll1_opy_ = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11ll1llll11_opy_, None)
                if status.lower() == bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᜾") and bstack11lll111ll1_opy_ is not None:
                    bstack11lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ᜿")] = bstack11lll111ll1_opy_[0][bstack1ll1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᝀ")][0] if isinstance(bstack11lll111ll1_opy_, list) else str(bstack11lll111ll1_opy_)
                driver.execute_script(
                    bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᝁ").format(
                        json.dumps(
                            {
                                bstack1ll1lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᝂ"): bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᝃ"),
                                bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᝄ"): bstack11lll1111l1_opy_,
                            }
                        )
                    )
                )
            f.bstack1lll1111ll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1l11l1l1ll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __11ll11111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᝅ")).get(bstack1ll1lll_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᝆ")):
            test_name = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11ll11l1111_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᝇ"))
                return
            bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack11lllll1lll_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᝈ") + str(bstack1ll11l1l111_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᝉ"))
                return
            for bstack11llll111ll_opy_, bstack11ll1111l11_opy_ in bstack11lllll1lll_opy_:
                if not bstack1ll111l1111_opy_.bstack1l111lll1l1_opy_(bstack11ll1111l11_opy_):
                    continue
                driver = bstack11llll111ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᝊ").format(
                        json.dumps(
                            {
                                bstack1ll1lll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᝋ"): bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᝌ"),
                                bstack1ll1lll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᝍ"): {bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᝎ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lll1111ll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lll11l1l1_opy_, True)
    def bstack1l1111l11ll_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        f: TestFramework,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll111ll11_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        bstack11lllll1lll_opy_ = [d for d, _ in f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])]
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥᝏ"))
            return
        if not bstack11lll11l1_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᝐ"))
            return
        for bstack11ll111l11l_opy_ in bstack11lllll1lll_opy_:
            driver = bstack11ll111l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll1lll_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥᝑ") + str(timestamp)
            driver.execute_script(
                bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᝒ").format(
                    json.dumps(
                        {
                            bstack1ll1lll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᝓ"): bstack1ll1lll_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ᝔"),
                            bstack1ll1lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ᝕"): {
                                bstack1ll1lll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᝖"): bstack1ll1lll_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣ᝗"),
                                bstack1ll1lll_opy_ (u"ࠧࡪࡡࡵࡣࠥ᝘"): data,
                                bstack1ll1lll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧ᝙"): bstack1ll1lll_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨ᝚")
                            }
                        }
                    )
                )
            )
    def bstack1l1111l1l11_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        f: TestFramework,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll111ll11_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        keys = [
            bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_,
            bstack1l1llll11ll_opy_.bstack11lllllll1l_opy_,
        ]
        bstack11lllll1lll_opy_ = []
        for key in keys:
            bstack11lllll1lll_opy_.extend(f.bstack1ll1l11llll_opy_(instance, key, []))
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡳࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥ᝛"))
            return
        if f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lllll1ll1_opy_, False):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡇࡇ࡚ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡥࡵࡩࡦࡺࡥࡥࠤ᝜"))
            return
        self.bstack1l11l1l111l_opy_()
        bstack11lllll111_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᝝").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll1l111_opy_)
        req.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        req.test_framework_state = bstack1ll11l1l111_opy_[0].name
        req.test_hook_state = bstack1ll11l1l111_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
        for bstack11llll111ll_opy_, driver in bstack11lllll1lll_opy_:
            bstack1ll11ll11ll_opy_ = driver.data.get(bstack1ll1lll_opy_ (u"ࠦࡷࡧ࡮࡬ࠤ᝞"))
            bstack11ll1111l1l_opy_ = False
            if bstack1ll11ll11ll_opy_ is None:
                bstack11ll1111l1l_opy_ = True
            else:
                try:
                    bstack11ll1111l1l_opy_ = int(bstack1ll11ll11ll_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll1111l1l_opy_ = False
            if bstack11ll1111l1l_opy_:
                try:
                    webdriver = bstack11llll111ll_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠤ࠭ࡸࡥࡧࡧࡵࡩࡳࡩࡥࠡࡧࡻࡴ࡮ࡸࡥࡥࠫࠥ᝟"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᝠ")
                        if bstack1ll111l1111_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll111l1111_opy_.bstack11ll111l1ll_opy_, False)
                        else bstack1ll1lll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨᝡ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll111l1111_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll111l1111_opy_.bstack1lll111l_opy_, bstack1ll1lll_opy_ (u"ࠣࠤᝢ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll111l1111_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll111l1111_opy_.bstack1ll1ll111ll_opy_, bstack1ll1lll_opy_ (u"ࠤࠥᝣ"))
                    caps = None
                    if hasattr(webdriver, bstack1ll1lll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᝤ")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡪࡩࡳࡧࡦࡸࡱࡿࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᝥ"))
                        except Exception as e:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᝦ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᝧ"))
                    try:
                        bstack11ll1111lll_opy_ = json.dumps(caps).encode(bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᝨ")) if caps else bstack11ll111lll1_opy_ (u"ࠣࡽࢀࠦᝩ")
                        req.capabilities = bstack11ll1111lll_opy_
                    except Exception as e:
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸ࡫ࡲࡪࡣ࡯࡭ࡿ࡫ࠠࡤࡣࡳࡷࠥ࡬࡯ࡳࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࠧᝪ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᝫ"))
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡶࡨࡱ࠿ࠦࠢᝬ") + str(str(e)) + bstack1ll1lll_opy_ (u"ࠧࠨ᝭"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11ll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll11l1_opy_() and len(bstack11lllll1lll_opy_) == 0:
            bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lllllll1l_opy_, [])
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝮ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᝯ"))
            return {}
        for bstack11llll111ll_opy_, bstack11llll11l1l_opy_ in bstack11lllll1lll_opy_:
            bstack1ll11ll11ll_opy_ = bstack11llll11l1l_opy_.data.get(bstack1ll1lll_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᝰ"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱ࠺ࠡࠤ᝱") + str(bstack1ll11ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦᝲ"))
            if bstack1ll11ll11ll_opy_ is None or bstack1ll11ll11ll_opy_ == bstack1ll1lll_opy_ (u"ࠫ࠶࠭ᝳ"):
                driver = bstack11llll111ll_opy_()
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡪࡪࡺࡣࡩࡧࡧࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࠨ᝴") + str(bstack11llll11l1l_opy_.data[bstack1ll1lll_opy_ (u"࠭ࡲࡢࡰ࡮ࠫ᝵")]) + bstack1ll1lll_opy_ (u"ࠢࠣ᝶"))
                if not driver:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᝷") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥ᝸"))
                    return {}
                capabilities = f.bstack1ll1l11llll_opy_(bstack11llll11l1l_opy_, bstack1ll111l1111_opy_.bstack11l11l11_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࠤ᝹") + str(capabilities) + bstack1ll1lll_opy_ (u"ࠦࠧ᝺"))
                if not capabilities:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᝻") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢ᝼"))
                    return {}
                return capabilities.get(bstack1ll1lll_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧ᝽"), {})
        return None
    def bstack1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lll11l1_opy_() and len(bstack11lllll1lll_opy_) == 0:
            bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack11lllllll1l_opy_, [])
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᝾") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥ᝿"))
            return
        if len(bstack11lllll1lll_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨក") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧខ"))
        for bstack11llll111ll_opy_, bstack11llll11l1l_opy_ in bstack11lllll1lll_opy_:
            driver = bstack11llll111ll_opy_()
            bstack1ll11ll11ll_opy_ = bstack11llll11l1l_opy_.data.get(bstack1ll1lll_opy_ (u"ࠬࡸࡡ࡯࡭ࠪគ"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱ࠺ࠡࠤឃ") + str(bstack1ll11ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣង"))
            if (bstack1ll11ll11ll_opy_ is None or int(bstack1ll11ll11ll_opy_) == 1) and driver:
                return driver
        return None