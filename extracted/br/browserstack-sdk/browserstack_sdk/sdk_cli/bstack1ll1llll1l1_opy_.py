# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import (
    bstack1llllllllll_opy_,
    bstack11111lll1l_opy_,
    bstack111111ll11_opy_,
    bstack11111ll111_opy_,
    bstack11111l1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll11111_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_, bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1ll11l11l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111lll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1lllll11_opy_(bstack1ll11l11l1l_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧጎ")
    bstack1ll111lllll_opy_ = bstack1l1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጏ")
    bstack1l1l1lll11l_opy_ = bstack1l1lll_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጐ")
    bstack1l1l1ll11l1_opy_ = bstack1l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ጑")
    bstack1l1l1ll1111_opy_ = bstack1l1lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢጒ")
    bstack1ll11l11111_opy_ = bstack1l1lll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥጓ")
    bstack1l1l1l1ll11_opy_ = bstack1l1lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣጔ")
    bstack1l1l1l1l1ll_opy_ = bstack1l1lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦጕ")
    def __init__(self):
        super().__init__(bstack1ll11l11l11_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll11lllll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.POST), self.bstack1l1l111l111_opy_)
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.PRE), self.bstack1ll1l11ll1l_opy_)
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll11lll_opy_ = self.bstack1l1l111l11l_opy_(instance.context)
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ጖") + str(bstack1lllllll1l1_opy_) + bstack1l1lll_opy_ (u"ࠣࠤ጗"))
        f.bstack1111l11l1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, bstack1l1lll11lll_opy_)
        bstack1l1l1111lll_opy_ = self.bstack1l1l111l11l_opy_(instance.context, bstack1l1l111ll11_opy_=False)
        f.bstack1111l11l1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1lll11l_opy_, bstack1l1l1111lll_opy_)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l111_opy_(f, instance, bstack1lllllll1l1_opy_, *args, **kwargs)
        if not f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1ll11_opy_, False):
            self.__1l1l1111l11_opy_(f,instance,bstack1lllllll1l1_opy_)
    def bstack1ll1l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l111_opy_(f, instance, bstack1lllllll1l1_opy_, *args, **kwargs)
        if not f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1ll11_opy_, False):
            self.__1l1l1111l11_opy_(f, instance, bstack1lllllll1l1_opy_)
        if not f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1l1ll_opy_, False):
            self.__1l1l111ll1l_opy_(f, instance, bstack1lllllll1l1_opy_)
    def bstack1l1l1111l1l_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll11llllll_opy_(instance):
            return
        if f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1l1ll_opy_, False):
            return
        driver.execute_script(
            bstack1l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢጘ").format(
                json.dumps(
                    {
                        bstack1l1lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥጙ"): bstack1l1lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጚ"),
                        bstack1l1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጛ"): {bstack1l1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጜ"): result},
                    }
                )
            )
        )
        f.bstack1111l11l1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1l1ll_opy_, True)
    def bstack1l1l111l11l_opy_(self, context: bstack11111l1ll1_opy_, bstack1l1l111ll11_opy_= True):
        if bstack1l1l111ll11_opy_:
            bstack1l1lll11lll_opy_ = self.bstack1ll11l1l11l_opy_(context, reverse=True)
        else:
            bstack1l1lll11lll_opy_ = self.bstack1ll11l11ll1_opy_(context, reverse=True)
        return [f for f in bstack1l1lll11lll_opy_ if f[1].state != bstack1llllllllll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l1l1lll_opy_, stage=STAGE.bstack1111lll1_opy_)
    def __1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack111l1111_opy_.get(bstack1l1lll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጝ")):
            bstack1l1lll11lll_opy_ = f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
            if not bstack1l1lll11lll_opy_:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጞ") + str(bstack1lllllll1l1_opy_) + bstack1l1lll_opy_ (u"ࠤࠥጟ"))
                return
            driver = bstack1l1lll11lll_opy_[0][0]()
            status = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, None)
            if not status:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጠ") + str(bstack1lllllll1l1_opy_) + bstack1l1lll_opy_ (u"ࠦࠧጡ"))
                return
            bstack1l1l1l1ll1l_opy_ = {bstack1l1lll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧጢ"): status.lower()}
            bstack1l1l1lll1ll_opy_ = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1l1l1llll_opy_, None)
            if status.lower() == bstack1l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጣ") and bstack1l1l1lll1ll_opy_ is not None:
                bstack1l1l1l1ll1l_opy_[bstack1l1lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧጤ")] = bstack1l1l1lll1ll_opy_[0][bstack1l1lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫጥ")][0] if isinstance(bstack1l1l1lll1ll_opy_, list) else str(bstack1l1l1lll1ll_opy_)
            driver.execute_script(
                bstack1l1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢጦ").format(
                    json.dumps(
                        {
                            bstack1l1lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥጧ"): bstack1l1lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጨ"),
                            bstack1l1lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጩ"): bstack1l1l1l1ll1l_opy_,
                        }
                    )
                )
            )
            f.bstack1111l11l1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1l1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1l1ll1l11_opy_, stage=STAGE.bstack1111lll1_opy_)
    def __1l1l1111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack111l1111_opy_.get(bstack1l1lll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦጪ")):
            test_name = f.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1l111l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨጫ"))
                return
            bstack1l1lll11lll_opy_ = f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
            if not bstack1l1lll11lll_opy_:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጬ") + str(bstack1lllllll1l1_opy_) + bstack1l1lll_opy_ (u"ࠤࠥጭ"))
                return
            for bstack1l1ll1ll111_opy_, bstack1l1l111lll1_opy_ in bstack1l1lll11lll_opy_:
                if not bstack1lll11lllll_opy_.bstack1ll11llllll_opy_(bstack1l1l111lll1_opy_):
                    continue
                driver = bstack1l1ll1ll111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጮ").format(
                        json.dumps(
                            {
                                bstack1l1lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጯ"): bstack1l1lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨጰ"),
                                bstack1l1lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጱ"): {bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጲ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1111l11l1l_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1l1ll11_opy_, True)
    def bstack1ll11111lll_opy_(
        self,
        instance: bstack1llllll11ll_opy_,
        f: TestFramework,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l111_opy_(f, instance, bstack1lllllll1l1_opy_, *args, **kwargs)
        bstack1l1lll11lll_opy_ = [d for d, _ in f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])]
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጳ"))
            return
        if not bstack1ll1111lll1_opy_():
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጴ"))
            return
        for bstack1l1l1111ll1_opy_ in bstack1l1lll11lll_opy_:
            driver = bstack1l1l1111ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1lll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣጵ") + str(timestamp)
            driver.execute_script(
                bstack1l1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጶ").format(
                    json.dumps(
                        {
                            bstack1l1lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጷ"): bstack1l1lll_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣጸ"),
                            bstack1l1lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጹ"): {
                                bstack1l1lll_opy_ (u"ࠣࡶࡼࡴࡪࠨጺ"): bstack1l1lll_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨጻ"),
                                bstack1l1lll_opy_ (u"ࠥࡨࡦࡺࡡࠣጼ"): data,
                                bstack1l1lll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥጽ"): bstack1l1lll_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦጾ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1ll11_opy_(
        self,
        instance: bstack1llllll11ll_opy_,
        f: TestFramework,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l111_opy_(f, instance, bstack1lllllll1l1_opy_, *args, **kwargs)
        bstack1l1lll11lll_opy_ = [d for _, d in f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])] + [d for _, d in f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1l1l1lll11l_opy_, [])]
        keys = [
            bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_,
            bstack1ll1lllll11_opy_.bstack1l1l1lll11l_opy_,
        ]
        bstack1l1lll11lll_opy_ = [
            d for key in keys for _, d in f.bstack11111l11l1_opy_(instance, key, [])
        ]
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጿ"))
            return
        if f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll11l11111_opy_, False):
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢፀ"))
            return
        self.bstack1ll1ll1l1l1_opy_()
        bstack1ll1l11l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1lllll_opy_)
        req.test_framework_name = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1ll11l_opy_)
        req.test_framework_version = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll111ll111_opy_)
        req.test_framework_state = bstack1lllllll1l1_opy_[0].name
        req.test_hook_state = bstack1lllllll1l1_opy_[1].name
        req.test_uuid = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1l11l1_opy_)
        for driver in bstack1l1lll11lll_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢፁ")
                if bstack1lll11lllll_opy_.bstack11111l11l1_opy_(driver, bstack1lll11lllll_opy_.bstack1l1l111l1l1_opy_, False)
                else bstack1l1lll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣፂ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll11lllll_opy_.bstack11111l11l1_opy_(driver, bstack1lll11lllll_opy_.bstack1l1ll11l111_opy_, bstack1l1lll_opy_ (u"ࠥࠦፃ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll11lllll_opy_.bstack11111l11l1_opy_(driver, bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_, bstack1l1lll_opy_ (u"ࠦࠧፄ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11lll_opy_ = f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፅ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠨࠢፆ"))
            return {}
        if len(bstack1l1lll11lll_opy_) > 1:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፇ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠣࠤፈ"))
            return {}
        bstack1l1ll1ll111_opy_, bstack1l1ll1lll11_opy_ = bstack1l1lll11lll_opy_[0]
        driver = bstack1l1ll1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፉ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠥࠦፊ"))
            return {}
        capabilities = f.bstack11111l11l1_opy_(bstack1l1ll1lll11_opy_, bstack1lll11lllll_opy_.bstack1l1ll11ll11_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፋ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠧࠨፌ"))
            return {}
        return capabilities.get(bstack1l1lll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦፍ"), {})
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11lll_opy_ = f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፎ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠣࠤፏ"))
            return
        if len(bstack1l1lll11lll_opy_) > 1:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፐ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠥࠦፑ"))
        bstack1l1ll1ll111_opy_, bstack1l1ll1lll11_opy_ = bstack1l1lll11lll_opy_[0]
        driver = bstack1l1ll1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፒ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠧࠨፓ"))
            return
        return driver