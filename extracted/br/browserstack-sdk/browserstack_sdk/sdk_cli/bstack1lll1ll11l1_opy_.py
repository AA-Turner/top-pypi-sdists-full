# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
    bstack111111l11l_opy_,
    bstack11111111ll_opy_,
    bstack1111l11lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_, bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll11_opy_ import bstack1ll11l11l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1lllll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1l111ll_opy_(bstack1ll11l11l1l_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢጉ")
    bstack1l1llllll1l_opy_ = bstack1l11lll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጊ")
    bstack1l1l1ll1lll_opy_ = bstack1l11lll_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጋ")
    bstack1l1l1l1l1ll_opy_ = bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጌ")
    bstack1l1l1llll11_opy_ = bstack1l11lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤግ")
    bstack1l1llll11ll_opy_ = bstack1l11lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጎ")
    bstack1l1l1lll1l1_opy_ = bstack1l11lll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥጏ")
    bstack1l1l1ll1l11_opy_ = bstack1l11lll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨጐ")
    def __init__(self):
        super().__init__(bstack1ll11l1ll1l_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1lll1l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.BEFORE_EACH, bstack1lll1l1l11l_opy_.POST), self.bstack1l1l111l1ll_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.PRE), self.bstack1ll1ll1ll11_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll11ll1_opy_ = self.bstack1l1l111lll1_opy_(instance.context)
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧ጑") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠥࠦጒ"))
        f.bstack1111l111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, bstack1l1lll11ll1_opy_)
        bstack1l1l111ll11_opy_ = self.bstack1l1l111lll1_opy_(instance.context, bstack1l1l1111l11_opy_=False)
        f.bstack1111l111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, bstack1l1l111ll11_opy_)
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1lll1l1_opy_, False):
            self.__1l1l1111l1l_opy_(f,instance,bstack11111l11ll_opy_)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1lll1l1_opy_, False):
            self.__1l1l1111l1l_opy_(f, instance, bstack11111l11ll_opy_)
        if not f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1l11_opy_, False):
            self.__1l1l111ll1l_opy_(f, instance, bstack11111l11ll_opy_)
    def bstack1l1l111l11l_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1ll1l1l1_opy_(instance):
            return
        if f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1l11_opy_, False):
            return
        driver.execute_script(
            bstack1l11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጓ").format(
                json.dumps(
                    {
                        bstack1l11lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጔ"): bstack1l11lll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጕ"),
                        bstack1l11lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ጖"): {bstack1l11lll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ጗"): result},
                    }
                )
            )
        )
        f.bstack1111l111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1l11_opy_, True)
    def bstack1l1l111lll1_opy_(self, context: bstack1111l11lll_opy_, bstack1l1l1111l11_opy_= True):
        if bstack1l1l1111l11_opy_:
            bstack1l1lll11ll1_opy_ = self.bstack1ll11l1l11l_opy_(context, reverse=True)
        else:
            bstack1l1lll11ll1_opy_ = self.bstack1ll11l111l1_opy_(context, reverse=True)
        return [f for f in bstack1l1lll11ll1_opy_ if f[1].state != bstack111111lll1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l1lll11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def __1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
    ):
        bstack1l1lll11ll1_opy_ = f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጘ") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠥࠦጙ"))
            return
        driver = bstack1l1lll11ll1_opy_[0][0]()
        status = f.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, None)
        if not status:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጚ") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠧࠨጛ"))
            return
        bstack1l1l1l1ll1l_opy_ = {bstack1l11lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጜ"): status.lower()}
        bstack1l1l1ll1111_opy_ = f.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1lll1ll_opy_, None)
        if status.lower() == bstack1l11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧጝ") and bstack1l1l1ll1111_opy_ is not None:
            bstack1l1l1l1ll1l_opy_[bstack1l11lll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨጞ")] = bstack1l1l1ll1111_opy_[0][bstack1l11lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬጟ")][0] if isinstance(bstack1l1l1ll1111_opy_, list) else str(bstack1l1l1ll1111_opy_)
        driver.execute_script(
            bstack1l11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጠ").format(
                json.dumps(
                    {
                        bstack1l11lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጡ"): bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣጢ"),
                        bstack1l11lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጣ"): bstack1l1l1l1ll1l_opy_,
                    }
                )
            )
        )
        f.bstack1111l111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1l11_opy_, True)
    @measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def __1l1l1111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]
    ):
        test_name = f.bstack1111111111_opy_(instance, TestFramework.bstack1l1l111l1l1_opy_, None)
        if not test_name:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨጤ"))
            return
        bstack1l1lll11ll1_opy_ = f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጥ") + str(bstack11111l11ll_opy_) + bstack1l11lll_opy_ (u"ࠤࠥጦ"))
            return
        for bstack1l1ll1l11ll_opy_, bstack1l1l1111ll1_opy_ in bstack1l1lll11ll1_opy_:
            if not bstack1lll1lll1l1_opy_.bstack1ll1ll1l1l1_opy_(bstack1l1l1111ll1_opy_):
                continue
            driver = bstack1l1ll1l11ll_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1l11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጧ").format(
                    json.dumps(
                        {
                            bstack1l11lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጨ"): bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨጩ"),
                            bstack1l11lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጪ"): {bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጫ"): test_name},
                        }
                    )
                )
            )
        f.bstack1111l111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1lll1l1_opy_, True)
    def bstack1l1lll1l11l_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        bstack1l1lll11ll1_opy_ = [d for d, _ in f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])]
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጬ"))
            return
        if not bstack1l1ll1lllll_opy_():
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጭ"))
            return
        for bstack1l1l1111lll_opy_ in bstack1l1lll11ll1_opy_:
            driver = bstack1l1l1111lll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l11lll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣጮ") + str(timestamp)
            driver.execute_script(
                bstack1l11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጯ").format(
                    json.dumps(
                        {
                            bstack1l11lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጰ"): bstack1l11lll_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣጱ"),
                            bstack1l11lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጲ"): {
                                bstack1l11lll_opy_ (u"ࠣࡶࡼࡴࡪࠨጳ"): bstack1l11lll_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨጴ"),
                                bstack1l11lll_opy_ (u"ࠥࡨࡦࡺࡡࠣጵ"): data,
                                bstack1l11lll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥጶ"): bstack1l11lll_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦጷ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        bstack1l1lll11ll1_opy_ = [d for _, d in f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])] + [d for _, d in f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_, [])]
        keys = [
            bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_,
            bstack1lll1l111ll_opy_.bstack1l1l1ll1lll_opy_,
        ]
        bstack1l1lll11ll1_opy_ = [
            d for key in keys for _, d in f.bstack1111111111_opy_(instance, key, [])
        ]
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጸ"))
            return
        if f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llll11ll_opy_, False):
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢጹ"))
            return
        self.bstack1ll1ll1l11l_opy_()
        bstack1ll1ll11ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        req.test_framework_name = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l1ll111_opy_)
        req.test_framework_version = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_)
        req.test_framework_state = bstack11111l11ll_opy_[0].name
        req.test_hook_state = bstack11111l11ll_opy_[1].name
        req.test_uuid = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1ll1ll11lll_opy_)
        for driver in bstack1l1lll11ll1_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢጺ")
                if bstack1lll1lll1l1_opy_.bstack1111111111_opy_(driver, bstack1lll1lll1l1_opy_.bstack1l1l111l111_opy_, False)
                else bstack1l11lll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣጻ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll1lll1l1_opy_.bstack1111111111_opy_(driver, bstack1lll1lll1l1_opy_.bstack1l1ll11l1ll_opy_, bstack1l11lll_opy_ (u"ࠥࠦጼ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll1lll1l1_opy_.bstack1111111111_opy_(driver, bstack1lll1lll1l1_opy_.bstack1l1ll111l1l_opy_, bstack1l11lll_opy_ (u"ࠦࠧጽ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11ll1_opy_ = f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣጾ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠨࠢጿ"))
            return {}
        if len(bstack1l1lll11ll1_opy_) > 1:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፀ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠣࠤፁ"))
            return {}
        bstack1l1ll1l11ll_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1lll11ll1_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፂ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠥࠦፃ"))
            return {}
        capabilities = f.bstack1111111111_opy_(bstack1l1ll1l1l1l_opy_, bstack1lll1lll1l1_opy_.bstack1l1ll11llll_opy_)
        if not capabilities:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፄ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨፅ"))
            return {}
        return capabilities.get(bstack1l11lll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦፆ"), {})
    def bstack1ll1ll1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11ll1_opy_ = f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፇ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠣࠤፈ"))
            return
        if len(bstack1l1lll11ll1_opy_) > 1:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፉ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠥࠦፊ"))
        bstack1l1ll1l11ll_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1lll11ll1_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፋ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨፌ"))
            return
        return driver