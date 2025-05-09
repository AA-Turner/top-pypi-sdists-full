# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack1llllllll1l_opy_,
    bstack11111l1ll1_opy_,
    bstack111111l1ll_opy_,
    bstack1111l111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_, bstack1lll1ll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1ll_opy_ import bstack1ll11l111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lllll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll111l1l_opy_(bstack1ll11l111ll_opy_):
    bstack1l1l1l1ll11_opy_ = bstack11lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧጎ")
    bstack1l1lll111l1_opy_ = bstack11lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጏ")
    bstack1l1l1ll1l1l_opy_ = bstack11lll_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጐ")
    bstack1l1l1ll111l_opy_ = bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ጑")
    bstack1l1l1ll1ll1_opy_ = bstack11lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢጒ")
    bstack1l1lllll111_opy_ = bstack11lll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥጓ")
    bstack1l1l1ll11l1_opy_ = bstack11lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣጔ")
    bstack1l1l1l1ll1l_opy_ = bstack11lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦጕ")
    def __init__(self):
        super().__init__(bstack1ll11l11l11_opy_=self.bstack1l1l1l1ll11_opy_, frameworks=[bstack1lll1ll1lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll1ll1l_opy_((bstack1lll111ll11_opy_.BEFORE_EACH, bstack1lll1l111l1_opy_.POST), self.bstack1l1l11111l1_opy_)
        TestFramework.bstack1ll1ll1ll1l_opy_((bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.PRE), self.bstack1ll11llll1l_opy_)
        TestFramework.bstack1ll1ll1ll1l_opy_((bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.POST), self.bstack1ll1l11l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1111ll1l_opy_ = self.bstack1l1l1111ll1_opy_(instance.context)
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ጖") + str(bstack1111111ll1_opy_) + bstack11lll_opy_ (u"ࠣࠤ጗"))
        f.bstack11111llll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, bstack1ll1111ll1l_opy_)
        bstack1l1l1111l1l_opy_ = self.bstack1l1l1111ll1_opy_(instance.context, bstack1l1l111l1ll_opy_=False)
        f.bstack11111llll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1ll1l1l_opy_, bstack1l1l1111l1l_opy_)
    def bstack1ll11llll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11111l1_opy_(f, instance, bstack1111111ll1_opy_, *args, **kwargs)
        if not f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1ll11l1_opy_, False):
            self.__1l1l1111l11_opy_(f,instance,bstack1111111ll1_opy_)
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11111l1_opy_(f, instance, bstack1111111ll1_opy_, *args, **kwargs)
        if not f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1ll11l1_opy_, False):
            self.__1l1l1111l11_opy_(f, instance, bstack1111111ll1_opy_)
        if not f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1l1ll1l_opy_, False):
            self.__1l1l11111ll_opy_(f, instance, bstack1111111ll1_opy_)
    def bstack1l1l111ll11_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1llll1_opy_(instance):
            return
        if f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1l1ll1l_opy_, False):
            return
        driver.execute_script(
            bstack11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢጘ").format(
                json.dumps(
                    {
                        bstack11lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥጙ"): bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጚ"),
                        bstack11lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጛ"): {bstack11lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጜ"): result},
                    }
                )
            )
        )
        f.bstack11111llll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1l1ll1l_opy_, True)
    def bstack1l1l1111ll1_opy_(self, context: bstack1111l111ll_opy_, bstack1l1l111l1ll_opy_= True):
        if bstack1l1l111l1ll_opy_:
            bstack1ll1111ll1l_opy_ = self.bstack1ll11l11111_opy_(context, reverse=True)
        else:
            bstack1ll1111ll1l_opy_ = self.bstack1ll11l11ll1_opy_(context, reverse=True)
        return [f for f in bstack1ll1111ll1l_opy_ if f[1].state != bstack1lllllll1l1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l11l1ll11_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1l1l11111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack1lll111lll_opy_.get(bstack11lll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጝ")):
            bstack1ll1111ll1l_opy_ = f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
            if not bstack1ll1111ll1l_opy_:
                self.logger.debug(bstack11lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጞ") + str(bstack1111111ll1_opy_) + bstack11lll_opy_ (u"ࠤࠥጟ"))
                return
            driver = bstack1ll1111ll1l_opy_[0][0]()
            status = f.bstack111111l1l1_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, None)
            if not status:
                self.logger.debug(bstack11lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጠ") + str(bstack1111111ll1_opy_) + bstack11lll_opy_ (u"ࠦࠧጡ"))
                return
            bstack1l1l1l1lll1_opy_ = {bstack11lll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧጢ"): status.lower()}
            bstack1l1l1lll1l1_opy_ = f.bstack111111l1l1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, None)
            if status.lower() == bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጣ") and bstack1l1l1lll1l1_opy_ is not None:
                bstack1l1l1l1lll1_opy_[bstack11lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧጤ")] = bstack1l1l1lll1l1_opy_[0][bstack11lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫጥ")][0] if isinstance(bstack1l1l1lll1l1_opy_, list) else str(bstack1l1l1lll1l1_opy_)
            driver.execute_script(
                bstack11lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢጦ").format(
                    json.dumps(
                        {
                            bstack11lll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥጧ"): bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጨ"),
                            bstack11lll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጩ"): bstack1l1l1l1lll1_opy_,
                        }
                    )
                )
            )
            f.bstack11111llll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1l1ll1l_opy_, True)
    @measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1l1l1111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.bstack1lll111lll_opy_.get(bstack11lll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦጪ")):
            test_name = f.bstack111111l1l1_opy_(instance, TestFramework.bstack1l1l111l111_opy_, None)
            if not test_name:
                self.logger.debug(bstack11lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨጫ"))
                return
            bstack1ll1111ll1l_opy_ = f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
            if not bstack1ll1111ll1l_opy_:
                self.logger.debug(bstack11lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥጬ") + str(bstack1111111ll1_opy_) + bstack11lll_opy_ (u"ࠤࠥጭ"))
                return
            for bstack1l1ll1ll1l1_opy_, bstack1l1l111l1l1_opy_ in bstack1ll1111ll1l_opy_:
                if not bstack1lll1ll1lll_opy_.bstack1ll1l1llll1_opy_(bstack1l1l111l1l1_opy_):
                    continue
                driver = bstack1l1ll1ll1l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጮ").format(
                        json.dumps(
                            {
                                bstack11lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጯ"): bstack11lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨጰ"),
                                bstack11lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጱ"): {bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጲ"): test_name},
                            }
                        )
                    )
                )
            f.bstack11111llll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1ll11l1_opy_, True)
    def bstack1l1lll11111_opy_(
        self,
        instance: bstack1lll1ll1ll1_opy_,
        f: TestFramework,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11111l1_opy_(f, instance, bstack1111111ll1_opy_, *args, **kwargs)
        bstack1ll1111ll1l_opy_ = [d for d, _ in f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])]
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጳ"))
            return
        if not bstack1l1lllll1l1_opy_():
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢጴ"))
            return
        for bstack1l1l111l11l_opy_ in bstack1ll1111ll1l_opy_:
            driver = bstack1l1l111l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11lll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣጵ") + str(timestamp)
            driver.execute_script(
                bstack11lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጶ").format(
                    json.dumps(
                        {
                            bstack11lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጷ"): bstack11lll_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣጸ"),
                            bstack11lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጹ"): {
                                bstack11lll_opy_ (u"ࠣࡶࡼࡴࡪࠨጺ"): bstack11lll_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨጻ"),
                                bstack11lll_opy_ (u"ࠥࡨࡦࡺࡡࠣጼ"): data,
                                bstack11lll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥጽ"): bstack11lll_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦጾ")
                            }
                        }
                    )
                )
            )
    def bstack1ll111ll1ll_opy_(
        self,
        instance: bstack1lll1ll1ll1_opy_,
        f: TestFramework,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11111l1_opy_(f, instance, bstack1111111ll1_opy_, *args, **kwargs)
        bstack1ll1111ll1l_opy_ = [d for _, d in f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])] + [d for _, d in f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1l1ll1l1l_opy_, [])]
        keys = [
            bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_,
            bstack1llll111l1l_opy_.bstack1l1l1ll1l1l_opy_,
        ]
        bstack1ll1111ll1l_opy_ = [
            d for key in keys for _, d in f.bstack111111l1l1_opy_(instance, key, [])
        ]
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣጿ"))
            return
        if f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lllll111_opy_, False):
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢፀ"))
            return
        self.bstack1ll11llll11_opy_()
        bstack111ll1lll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1ll1l1l111l_opy_)
        req.test_framework_name = TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
        req.test_framework_version = TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1ll111l1111_opy_)
        req.test_framework_state = bstack1111111ll1_opy_[0].name
        req.test_hook_state = bstack1111111ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1ll1l1ll1ll_opy_)
        for driver in bstack1ll1111ll1l_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢፁ")
                if bstack1lll1ll1lll_opy_.bstack111111l1l1_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1l1111lll_opy_, False)
                else bstack11lll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣፂ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll1ll1lll_opy_.bstack111111l1l1_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1ll11l1l1_opy_, bstack11lll_opy_ (u"ࠥࠦፃ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll1ll1lll_opy_.bstack111111l1l1_opy_(driver, bstack1lll1ll1lll_opy_.bstack1l1l1llll11_opy_, bstack11lll_opy_ (u"ࠦࠧፄ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11lll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111ll1l_opy_ = f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፅ") + str(kwargs) + bstack11lll_opy_ (u"ࠨࠢፆ"))
            return {}
        if len(bstack1ll1111ll1l_opy_) > 1:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፇ") + str(kwargs) + bstack11lll_opy_ (u"ࠣࠤፈ"))
            return {}
        bstack1l1ll1ll1l1_opy_, bstack1l1ll1l1l11_opy_ = bstack1ll1111ll1l_opy_[0]
        driver = bstack1l1ll1ll1l1_opy_()
        if not driver:
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፉ") + str(kwargs) + bstack11lll_opy_ (u"ࠥࠦፊ"))
            return {}
        capabilities = f.bstack111111l1l1_opy_(bstack1l1ll1l1l11_opy_, bstack1lll1ll1lll_opy_.bstack1l1l1llllll_opy_)
        if not capabilities:
            self.logger.debug(bstack11lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፋ") + str(kwargs) + bstack11lll_opy_ (u"ࠧࠨፌ"))
            return {}
        return capabilities.get(bstack11lll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦፍ"), {})
    def bstack1ll11ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111ll1l_opy_ = f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፎ") + str(kwargs) + bstack11lll_opy_ (u"ࠣࠤፏ"))
            return
        if len(bstack1ll1111ll1l_opy_) > 1:
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፐ") + str(kwargs) + bstack11lll_opy_ (u"ࠥࠦፑ"))
        bstack1l1ll1ll1l1_opy_, bstack1l1ll1l1l11_opy_ = bstack1ll1111ll1l_opy_[0]
        driver = bstack1l1ll1ll1l1_opy_()
        if not driver:
            self.logger.debug(bstack11lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፒ") + str(kwargs) + bstack11lll_opy_ (u"ࠧࠨፓ"))
            return
        return driver