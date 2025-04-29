# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import (
    bstack11111lll11_opy_,
    bstack1111111l1l_opy_,
    bstack1lllllll11l_opy_,
    bstack111111ll11_opy_,
    bstack1lllllllll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lllll1_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_, bstack1lll1ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll1l_opy_ import bstack1ll11l11l11_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lllll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll1lllll_opy_(bstack1ll11l11l11_opy_):
    bstack1l1l1ll11ll_opy_ = bstack1llllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢጉ")
    bstack1l1lllll11l_opy_ = bstack1llllll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጊ")
    bstack1l1l1lll1l1_opy_ = bstack1llllll_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጋ")
    bstack1l1l1ll11l1_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጌ")
    bstack1l1l1l1ll11_opy_ = bstack1llllll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤግ")
    bstack1l1lll11111_opy_ = bstack1llllll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጎ")
    bstack1l1l1ll111l_opy_ = bstack1llllll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥጏ")
    bstack1l1l1lll1ll_opy_ = bstack1llllll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨጐ")
    def __init__(self):
        super().__init__(bstack1ll11l1111l_opy_=self.bstack1l1l1ll11ll_opy_, frameworks=[bstack1lll11ll1ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l111l1l_opy_((bstack1lllll1lll1_opy_.BEFORE_EACH, bstack1lll1lll1l1_opy_.POST), self.bstack1l1l111ll1l_opy_)
        TestFramework.bstack1ll1l111l1l_opy_((bstack1lllll1lll1_opy_.TEST, bstack1lll1lll1l1_opy_.PRE), self.bstack1ll1l111111_opy_)
        TestFramework.bstack1ll1l111l1l_opy_((bstack1lllll1lll1_opy_.TEST, bstack1lll1lll1l1_opy_.POST), self.bstack1ll11lll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1111l1l1_opy_ = self.bstack1l1l111ll11_opy_(instance.context)
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧ጑") + str(bstack1111111lll_opy_) + bstack1llllll_opy_ (u"ࠥࠦጒ"))
        f.bstack1111l11lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, bstack1ll1111l1l1_opy_)
        bstack1l1l1111l1l_opy_ = self.bstack1l1l111ll11_opy_(instance.context, bstack1l1l111lll1_opy_=False)
        f.bstack1111l11lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1l1_opy_, bstack1l1l1111l1l_opy_)
    def bstack1ll1l111111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111111lll_opy_, *args, **kwargs)
        if not f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1ll111l_opy_, False):
            self.__1l1l111l11l_opy_(f,instance,bstack1111111lll_opy_)
    def bstack1ll11lll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111111lll_opy_, *args, **kwargs)
        if not f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1ll111l_opy_, False):
            self.__1l1l111l11l_opy_(f, instance, bstack1111111lll_opy_)
        if not f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1ll_opy_, False):
            self.__1l1l111l1l1_opy_(f, instance, bstack1111111lll_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1ll1ll1l_opy_(instance):
            return
        if f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1ll_opy_, False):
            return
        driver.execute_script(
            bstack1llllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጓ").format(
                json.dumps(
                    {
                        bstack1llllll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጔ"): bstack1llllll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጕ"),
                        bstack1llllll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ጖"): {bstack1llllll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ጗"): result},
                    }
                )
            )
        )
        f.bstack1111l11lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1ll_opy_, True)
    def bstack1l1l111ll11_opy_(self, context: bstack1lllllllll1_opy_, bstack1l1l111lll1_opy_= True):
        if bstack1l1l111lll1_opy_:
            bstack1ll1111l1l1_opy_ = self.bstack1ll11l1l1l1_opy_(context, reverse=True)
        else:
            bstack1ll1111l1l1_opy_ = self.bstack1ll11l111ll_opy_(context, reverse=True)
        return [f for f in bstack1ll1111l1l1_opy_ if f[1].state != bstack11111lll11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1lll11l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def __1l1l111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack11llll1lll_opy_.get(bstack1llllll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጘ")):
            bstack1ll1111l1l1_opy_ = f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])
            if not bstack1ll1111l1l1_opy_:
                self.logger.debug(bstack1llllll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጙ") + str(bstack1111111lll_opy_) + bstack1llllll_opy_ (u"ࠦࠧጚ"))
                return
            driver = bstack1ll1111l1l1_opy_[0][0]()
            status = f.bstack111111lll1_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, None)
            if not status:
                self.logger.debug(bstack1llllll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጛ") + str(bstack1111111lll_opy_) + bstack1llllll_opy_ (u"ࠨࠢጜ"))
                return
            bstack1l1l1lll111_opy_ = {bstack1llllll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢጝ"): status.lower()}
            bstack1l1l1ll1ll1_opy_ = f.bstack111111lll1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, None)
            if status.lower() == bstack1llllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጞ") and bstack1l1l1ll1ll1_opy_ is not None:
                bstack1l1l1lll111_opy_[bstack1llllll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩጟ")] = bstack1l1l1ll1ll1_opy_[0][bstack1llllll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ጠ")][0] if isinstance(bstack1l1l1ll1ll1_opy_, list) else str(bstack1l1l1ll1ll1_opy_)
            driver.execute_script(
                bstack1llllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጡ").format(
                    json.dumps(
                        {
                            bstack1llllll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጢ"): bstack1llllll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጣ"),
                            bstack1llllll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጤ"): bstack1l1l1lll111_opy_,
                        }
                    )
                )
            )
            f.bstack1111l11lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1ll_opy_, True)
    @measure(event_name=EVENTS.bstack11l1l1l1ll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def __1l1l111l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack11llll1lll_opy_.get(bstack1llllll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨጥ")):
            test_name = f.bstack111111lll1_opy_(instance, TestFramework.bstack1l1l1111l11_opy_, None)
            if not test_name:
                self.logger.debug(bstack1llllll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣጦ"))
                return
            bstack1ll1111l1l1_opy_ = f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])
            if not bstack1ll1111l1l1_opy_:
                self.logger.debug(bstack1llllll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጧ") + str(bstack1111111lll_opy_) + bstack1llllll_opy_ (u"ࠦࠧጨ"))
                return
            for bstack1l1ll1l1l11_opy_, bstack1l1l1111ll1_opy_ in bstack1ll1111l1l1_opy_:
                if not bstack1lll11ll1ll_opy_.bstack1ll1ll1ll1l_opy_(bstack1l1l1111ll1_opy_):
                    continue
                driver = bstack1l1ll1l1l11_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1llllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጩ").format(
                        json.dumps(
                            {
                                bstack1llllll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጪ"): bstack1llllll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣጫ"),
                                bstack1llllll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጬ"): {bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጭ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1111l11lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1ll111l_opy_, True)
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1lll1ll111l_opy_,
        f: TestFramework,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111111lll_opy_, *args, **kwargs)
        bstack1ll1111l1l1_opy_ = [d for d, _ in f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])]
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack1llllll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥጮ"))
            return
        if not bstack1l1lllll1l1_opy_():
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤጯ"))
            return
        for bstack1l1l111l1ll_opy_ in bstack1ll1111l1l1_opy_:
            driver = bstack1l1l111l1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1llllll_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥጰ") + str(timestamp)
            driver.execute_script(
                bstack1llllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጱ").format(
                    json.dumps(
                        {
                            bstack1llllll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጲ"): bstack1llllll_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥጳ"),
                            bstack1llllll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጴ"): {
                                bstack1llllll_opy_ (u"ࠥࡸࡾࡶࡥࠣጵ"): bstack1llllll_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣጶ"),
                                bstack1llllll_opy_ (u"ࠧࡪࡡࡵࡣࠥጷ"): data,
                                bstack1llllll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጸ"): bstack1llllll_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨጹ")
                            }
                        }
                    )
                )
            )
    def bstack1l1llll111l_opy_(
        self,
        instance: bstack1lll1ll111l_opy_,
        f: TestFramework,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111ll1l_opy_(f, instance, bstack1111111lll_opy_, *args, **kwargs)
        bstack1ll1111l1l1_opy_ = [d for _, d in f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])] + [d for _, d in f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1l1lll1l1_opy_, [])]
        keys = [
            bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_,
            bstack1llll1lllll_opy_.bstack1l1l1lll1l1_opy_,
        ]
        bstack1ll1111l1l1_opy_ = [
            d for key in keys for _, d in f.bstack111111lll1_opy_(instance, key, [])
        ]
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack1llllll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡳࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥጺ"))
            return
        if f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lll11111_opy_, False):
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡇࡇ࡚ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡥࡵࡩࡦࡺࡥࡥࠤጻ"))
            return
        self.bstack1ll1ll11lll_opy_()
        bstack11l1ll1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1ll11lll1l1_opy_)
        req.test_framework_name = TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1ll1ll1l1l1_opy_)
        req.test_framework_version = TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l1lll11l11_opy_)
        req.test_framework_state = bstack1111111lll_opy_[0].name
        req.test_hook_state = bstack1111111lll_opy_[1].name
        req.test_uuid = TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1ll1l11l1ll_opy_)
        for driver in bstack1ll1111l1l1_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1llllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤጼ")
                if bstack1lll11ll1ll_opy_.bstack111111lll1_opy_(driver, bstack1lll11ll1ll_opy_.bstack1l1l111l111_opy_, False)
                else bstack1llllll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥጽ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll11ll1ll_opy_.bstack111111lll1_opy_(driver, bstack1lll11ll1ll_opy_.bstack1l1ll111ll1_opy_, bstack1llllll_opy_ (u"ࠧࠨጾ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll11ll1ll_opy_.bstack111111lll1_opy_(driver, bstack1lll11ll1ll_opy_.bstack1l1ll111lll_opy_, bstack1llllll_opy_ (u"ࠨࠢጿ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11llll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l1l1_opy_ = f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack1llllll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፀ") + str(kwargs) + bstack1llllll_opy_ (u"ࠣࠤፁ"))
            return {}
        if len(bstack1ll1111l1l1_opy_) > 1:
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፂ") + str(kwargs) + bstack1llllll_opy_ (u"ࠥࠦፃ"))
            return {}
        bstack1l1ll1l1l11_opy_, bstack1l1ll1ll111_opy_ = bstack1ll1111l1l1_opy_[0]
        driver = bstack1l1ll1l1l11_opy_()
        if not driver:
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፄ") + str(kwargs) + bstack1llllll_opy_ (u"ࠧࠨፅ"))
            return {}
        capabilities = f.bstack111111lll1_opy_(bstack1l1ll1ll111_opy_, bstack1lll11ll1ll_opy_.bstack1l1ll111l1l_opy_)
        if not capabilities:
            self.logger.debug(bstack1llllll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፆ") + str(kwargs) + bstack1llllll_opy_ (u"ࠢࠣፇ"))
            return {}
        return capabilities.get(bstack1llllll_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨፈ"), {})
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l1l1_opy_ = f.bstack111111lll1_opy_(instance, bstack1llll1lllll_opy_.bstack1l1lllll11l_opy_, [])
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፉ") + str(kwargs) + bstack1llllll_opy_ (u"ࠥࠦፊ"))
            return
        if len(bstack1ll1111l1l1_opy_) > 1:
            self.logger.debug(bstack1llllll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፋ") + str(kwargs) + bstack1llllll_opy_ (u"ࠧࠨፌ"))
        bstack1l1ll1l1l11_opy_, bstack1l1ll1ll111_opy_ = bstack1ll1111l1l1_opy_[0]
        driver = bstack1l1ll1l1l11_opy_()
        if not driver:
            self.logger.debug(bstack1llllll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፍ") + str(kwargs) + bstack1llllll_opy_ (u"ࠢࠣፎ"))
            return
        return driver