# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack111l1ll111_opy_,
    bstack1ll111lllll_opy_,
    bstack1ll11l11ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l111lll111_opy_ import bstack1l11l11111l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l111l1111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1l1l1l11ll1_opy_(bstack1l11l11111l_opy_):
    bstack11ll1llll11_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣ᜹")
    bstack1l1111ll1l1_opy_ = bstack1ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ᜺")
    bstack1l1111ll111_opy_ = bstack1ll11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨ᜻")
    bstack11lll111lll_opy_ = bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧ᜼")
    bstack11lll11111l_opy_ = bstack1ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥ᜽")
    bstack1l111l11ll1_opy_ = bstack1ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨ᜾")
    bstack11lll1111ll_opy_ = bstack1ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦ᜿")
    bstack11ll1llllll_opy_ = bstack1ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢᝀ")
    def __init__(self):
        super().__init__(bstack1l111lll11l_opy_=self.bstack11ll1llll11_opy_, frameworks=[bstack1ll11111111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11ll11111l1_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11llll1ll_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11lllll11l1_opy_ = self.bstack11ll111ll11_opy_(instance.context)
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨᝁ") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠦࠧᝂ"))
        f.bstack1l11lllll_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, bstack11lllll11l1_opy_)
        bstack11ll111l111_opy_ = self.bstack11ll111ll11_opy_(instance.context, bstack11ll1111lll_opy_=False)
        f.bstack1l11lllll_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll111_opy_, bstack11ll111l111_opy_)
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11111l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if not f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11lll1111ll_opy_, False):
            self.__11ll111l1l1_opy_(f,instance,bstack1ll11l11lll_opy_)
    def bstack1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11111l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        if not f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11lll1111ll_opy_, False):
            self.__11ll111l1l1_opy_(f, instance, bstack1ll11l11lll_opy_)
        if not f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11ll1llllll_opy_, False):
            self.__11ll111111l_opy_(f, instance, bstack1ll11l11lll_opy_)
    def bstack11ll1111l11_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l11l111111_opy_(instance):
            return
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11ll1llllll_opy_, False):
            return
        driver.execute_script(
            bstack1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᝃ").format(
                json.dumps(
                    {
                        bstack1ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᝄ"): bstack1ll11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᝅ"),
                        bstack1ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᝆ"): {bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᝇ"): result},
                    }
                )
            )
        )
        f.bstack1l11lllll_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11ll1llllll_opy_, True)
    def bstack11ll111ll11_opy_(self, context: bstack1ll11l11ll1_opy_, bstack11ll1111lll_opy_= True):
        if bstack11ll1111lll_opy_:
            bstack11lllll11l1_opy_ = self.bstack1l111llllll_opy_(context, reverse=True)
        else:
            bstack11lllll11l1_opy_ = self.bstack1l111llll1l_opy_(context, reverse=True)
        return [f for f in bstack11lllll11l1_opy_ if f[1].state != bstack1ll1l1ll11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack11111llll_opy_)
    def __11ll111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣᝈ")).get(bstack1ll11_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᝉ")):
            bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack11lllll11l1_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᝊ") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠨࠢᝋ"))
                return
            for bstack11llll111l1_opy_, _ in bstack11lllll11l1_opy_:
                driver = bstack11llll111l1_opy_()
                status = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11lll11l111_opy_, None)
                if not status:
                    self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᝌ") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠣࠤᝍ"))
                    return
                bstack11lll111ll1_opy_ = {bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᝎ"): status.lower()}
                bstack11ll1llll1l_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_, None)
                if status.lower() == bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᝏ") and bstack11ll1llll1l_opy_ is not None:
                    bstack11lll111ll1_opy_[bstack1ll11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᝐ")] = bstack11ll1llll1l_opy_[0][bstack1ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᝑ")][0] if isinstance(bstack11ll1llll1l_opy_, list) else str(bstack11ll1llll1l_opy_)
                driver.execute_script(
                    bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᝒ").format(
                        json.dumps(
                            {
                                bstack1ll11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᝓ"): bstack1ll11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ᝔"),
                                bstack1ll11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ᝕"): bstack11lll111ll1_opy_,
                            }
                        )
                    )
                )
            f.bstack1l11lllll_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11ll1llllll_opy_, True)
    @measure(event_name=EVENTS.bstack1111ll1l1l_opy_, stage=STAGE.bstack11111llll_opy_)
    def __11ll111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠣ᝖")).get(bstack1ll11_opy_ (u"ࠦࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨ᝗")):
            test_name = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11ll1111l1l_opy_, None)
            if not test_name:
                self.logger.debug(bstack1ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦ᝘"))
                return
            bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack11lllll11l1_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣ᝙") + str(bstack1ll11l11lll_opy_) + bstack1ll11_opy_ (u"ࠢࠣ᝚"))
                return
            for bstack11llll111l1_opy_, bstack11ll11111ll_opy_ in bstack11lllll11l1_opy_:
                if not bstack1ll11111111_opy_.bstack1l11l111111_opy_(bstack11ll11111ll_opy_):
                    continue
                driver = bstack11llll111l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨ᝛").format(
                        json.dumps(
                            {
                                bstack1ll11_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ᝜"): bstack1ll11_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ᝝"),
                                bstack1ll11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ᝞"): {bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᝟"): test_name},
                            }
                        )
                    )
                )
            f.bstack1l11lllll_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11lll1111ll_opy_, True)
    def bstack1l11111l1ll_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        f: TestFramework,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11111l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        bstack11lllll11l1_opy_ = [d for d, _ in f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])]
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᝠ"))
            return
        if not bstack1l111l1111_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᝡ"))
            return
        for bstack11ll111l1ll_opy_ in bstack11lllll11l1_opy_:
            driver = bstack11ll111l1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1ll11_opy_ (u"ࠣࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡔࡻࡱࡧ࠿ࠨᝢ") + str(timestamp)
            driver.execute_script(
                bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᝣ").format(
                    json.dumps(
                        {
                            bstack1ll11_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᝤ"): bstack1ll11_opy_ (u"ࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨᝥ"),
                            bstack1ll11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᝦ"): {
                                bstack1ll11_opy_ (u"ࠨࡴࡺࡲࡨࠦᝧ"): bstack1ll11_opy_ (u"ࠢࡂࡰࡱࡳࡹࡧࡴࡪࡱࡱࠦᝨ"),
                                bstack1ll11_opy_ (u"ࠣࡦࡤࡸࡦࠨᝩ"): data,
                                bstack1ll11_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣᝪ"): bstack1ll11_opy_ (u"ࠥࡨࡪࡨࡵࡨࠤᝫ")
                            }
                        }
                    )
                )
            )
    def bstack1l111ll11ll_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        f: TestFramework,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11ll11111l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        keys = [
            bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_,
            bstack1l1l1l11ll1_opy_.bstack1l1111ll111_opy_,
        ]
        bstack11lllll11l1_opy_ = []
        for key in keys:
            bstack11lllll11l1_opy_.extend(f.bstack1ll1ll1l1l1_opy_(instance, key, []))
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡ࡯ࡻࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥࡺ࡯ࠡ࡮࡬ࡲࡰࠨᝬ"))
            return
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l111l11ll1_opy_, False):
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡃࡃࡖࠣࡥࡱࡸࡥࡢࡦࡼࠤࡨࡸࡥࡢࡶࡨࡨࠧ᝭"))
            return
        self.bstack1l1l1111l11_opy_()
        bstack11l111ll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᝮ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l11llll_opy_)
        req.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11111lll1_opy_)
        req.test_framework_state = bstack1ll11l11lll_opy_[0].name
        req.test_hook_state = bstack1ll11l11lll_opy_[1].name
        req.test_uuid = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
        for bstack11llll111l1_opy_, driver in bstack11lllll11l1_opy_:
            bstack1ll11ll1l1l_opy_ = driver.data.get(bstack1ll11_opy_ (u"ࠢࡳࡣࡱ࡯ࠧᝯ"))
            bstack11ll111ll1l_opy_ = False
            if bstack1ll11ll1l1l_opy_ is None:
                bstack11ll111ll1l_opy_ = True
            else:
                try:
                    bstack11ll111ll1l_opy_ = int(bstack1ll11ll1l1l_opy_) == 1
                except (TypeError, ValueError):
                    bstack11ll111ll1l_opy_ = False
            if bstack11ll111ll1l_opy_:
                try:
                    webdriver = bstack11llll111l1_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1ll11_opy_ (u"࡙ࠣࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࠩࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠤࡪࡾࡰࡪࡴࡨࡨ࠮ࠨᝰ"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣ᝱")
                        if bstack1ll11111111_opy_.bstack1ll1ll1l1l1_opy_(driver, bstack1ll11111111_opy_.bstack11ll111lll1_opy_, False)
                        else bstack1ll11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤᝲ")
                    )
                    session.ref = driver.ref()
                    session.hub_url = bstack1ll11111111_opy_.bstack1ll1ll1l1l1_opy_(driver, bstack1ll11111111_opy_.bstack1ll11l1lll_opy_, bstack1ll11_opy_ (u"ࠦࠧᝳ"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = bstack1ll11111111_opy_.bstack1ll1ll1l1l1_opy_(driver, bstack1ll11111111_opy_.bstack1ll1l1l1lll_opy_, bstack1ll11_opy_ (u"ࠧࠨ᝴"))
                    caps = None
                    if hasattr(webdriver, bstack1ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᝵")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡦ࡬ࡶࡪࡩࡴ࡭ࡻࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᝶"))
                        except Exception as e:
                            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨ᝷") + str(e) + bstack1ll11_opy_ (u"ࠤࠥ᝸"))
                    try:
                        bstack11ll111l11l_opy_ = json.dumps(caps).encode(bstack1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᝹")) if caps else bstack11ll1111ll1_opy_ (u"ࠦࢀࢃࠢ᝺")
                        req.capabilities = bstack11ll111l11l_opy_
                    except Exception as e:
                        self.logger.debug(bstack1ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡧࡵ࡭ࡦࡲࡩࡻࡧࠣࡧࡦࡶࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࠣ᝻") + str(e) + bstack1ll11_opy_ (u"ࠨࠢ᝼"))
                except Exception as e:
                    self.logger.error(bstack1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡹ࡫࡭࠻ࠢࠥ᝽") + str(str(e)) + bstack1ll11_opy_ (u"ࠣࠤ᝾"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1l11l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack1l111l1111_opy_() and len(bstack11lllll11l1_opy_) == 0:
            bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll111_opy_, [])
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᝿") + str(kwargs) + bstack1ll11_opy_ (u"ࠥࠦក"))
            return {}
        for bstack11llll111l1_opy_, bstack11llll11l11_opy_ in bstack11lllll11l1_opy_:
            bstack1ll11ll1l1l_opy_ = bstack11llll11l11_opy_.data.get(bstack1ll11_opy_ (u"ࠫࡷࡧ࡮࡬ࠩខ"))
            self.logger.info(bstack1ll11_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭࠽ࠤࠧគ") + str(bstack1ll11ll1l1l_opy_) + bstack1ll11_opy_ (u"ࠨࠢឃ"))
            if bstack1ll11ll1l1l_opy_ is None or bstack1ll11ll1l1l_opy_ == bstack1ll11_opy_ (u"ࠧ࠲ࠩង"):
                driver = bstack11llll111l1_opy_()
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡩࡨࡲࡪࡸࡡࡵࡧࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤࡪࡥࡵࡣ࡬ࡰࡸࠦࡦࡦࡶࡦ࡬ࡪࡪࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࠤច") + str(bstack11llll11l11_opy_.data[bstack1ll11_opy_ (u"ࠩࡵࡥࡳࡱࠧឆ")]) + bstack1ll11_opy_ (u"ࠥࠦជ"))
                if not driver:
                    self.logger.debug(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨឈ") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨញ"))
                    return {}
                capabilities = f.bstack1ll1ll1l1l1_opy_(bstack11llll11l11_opy_, bstack1ll11111111_opy_.bstack1lll1l1111_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡧࡦࡰࡨࡶࡦࡺࡥࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡨࡪࡺࡡࡪ࡮ࡶࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧដ") + str(capabilities) + bstack1ll11_opy_ (u"ࠢࠣឋ"))
                if not capabilities:
                    self.logger.debug(bstack1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣឌ") + str(kwargs) + bstack1ll11_opy_ (u"ࠤࠥឍ"))
                    return {}
                return capabilities.get(bstack1ll11_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣណ"), {})
        return None
    def bstack1l11lll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack1l111l1111_opy_() and len(bstack11lllll11l1_opy_) == 0:
            bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll111_opy_, [])
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢត") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨថ"))
            return
        if len(bstack11lllll11l1_opy_) > 1:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤទ") + str(kwargs) + bstack1ll11_opy_ (u"ࠢࠣធ"))
        for bstack11llll111l1_opy_, bstack11llll11l11_opy_ in bstack11lllll11l1_opy_:
            driver = bstack11llll111l1_opy_()
            bstack1ll11ll1l1l_opy_ = bstack11llll11l11_opy_.data.get(bstack1ll11_opy_ (u"ࠨࡴࡤࡲࡰ࠭ន"))
            self.logger.info(bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭࠽ࠤࠧប") + str(bstack1ll11ll1l1l_opy_) + bstack1ll11_opy_ (u"ࠥࠦផ"))
            if (bstack1ll11ll1l1l_opy_ is None or int(bstack1ll11ll1l1l_opy_) == 1) and driver:
                return driver
        return None