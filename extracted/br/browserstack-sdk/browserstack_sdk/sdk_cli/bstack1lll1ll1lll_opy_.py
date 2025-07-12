# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1ll1lllll11_opy_,
    bstack1lll1llll11_opy_,
    bstack1ll1ll1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_, bstack1lllll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1llll1ll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack111111l1ll_opy_(bstack1ll1ll1l1ll_opy_):
    bstack1ll1l11l1ll_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤም")
    bstack1lll1l1ll11_opy_ = bstack11l1111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥሞ")
    bstack1ll1l111ll1_opy_ = bstack11l1111_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢሟ")
    bstack1ll1l11ll1l_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨሠ")
    bstack1ll1l11lll1_opy_ = bstack11l1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦሡ")
    bstack1111111ll1_opy_ = bstack11l1111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢሢ")
    bstack1ll11lll1l1_opy_ = bstack11l1111_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧሣ")
    bstack1ll1l11llll_opy_ = bstack11l1111_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣሤ")
    def __init__(self):
        super().__init__(bstack1ll1ll1l1l1_opy_=self.bstack1ll1l11l1ll_opy_, frameworks=[bstack1lll1ll1l1l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.BEFORE_EACH, bstack1lll1lll1ll_opy_.POST), self.bstack1ll1111llll_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE), self.bstack1lllll1lll1_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1llll11l1l1_opy_ = self.bstack1ll111l11ll_opy_(instance.context)
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢሥ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠧࠨሦ"))
        f.bstack1llll111l11_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, bstack1llll11l1l1_opy_)
        bstack1ll111l1l1l_opy_ = self.bstack1ll111l11ll_opy_(instance.context, bstack1ll1111ll1l_opy_=False)
        f.bstack1llll111l11_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l111ll1_opy_, bstack1ll111l1l1l_opy_)
    def bstack1lllll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1111llll_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll11lll1l1_opy_, False):
            self.__1ll111l1ll1_opy_(f,instance,bstack1llll11l111_opy_)
    def bstack1lllll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1111llll_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        if not f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll11lll1l1_opy_, False):
            self.__1ll111l1ll1_opy_(f, instance, bstack1llll11l111_opy_)
        if not f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l11llll_opy_, False):
            self.__1ll111l11l1_opy_(f, instance, bstack1llll11l111_opy_)
    def bstack1ll111l111l_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1lllll1l_opy_(instance):
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l11llll_opy_, False):
            return
        driver.execute_script(
            bstack11l1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦሧ").format(
                json.dumps(
                    {
                        bstack11l1111_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢረ"): bstack11l1111_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦሩ"),
                        bstack11l1111_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧሪ"): {bstack11l1111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥራ"): result},
                    }
                )
            )
        )
        f.bstack1llll111l11_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l11llll_opy_, True)
    def bstack1ll111l11ll_opy_(self, context: bstack1ll1ll1l11l_opy_, bstack1ll1111ll1l_opy_= True):
        if bstack1ll1111ll1l_opy_:
            bstack1llll11l1l1_opy_ = self.bstack1ll1llll1l1_opy_(context, reverse=True)
        else:
            bstack1llll11l1l1_opy_ = self.bstack1ll1lll1ll1_opy_(context, reverse=True)
        return [f for f in bstack1llll11l1l1_opy_ if f[1].state != bstack1lll1llllll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1ll111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤሬ")).get(bstack11l1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤር")):
            bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
            if not bstack1llll11l1l1_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤሮ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠢࠣሯ"))
                return
            driver = bstack1llll11l1l1_opy_[0][0]()
            status = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1l11l111_opy_, None)
            if not status:
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥሰ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠤࠥሱ"))
                return
            bstack1ll1l111lll_opy_ = {bstack11l1111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥሲ"): status.lower()}
            bstack1ll11llll1l_opy_ = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1l111l11_opy_, None)
            if status.lower() == bstack11l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫሳ") and bstack1ll11llll1l_opy_ is not None:
                bstack1ll1l111lll_opy_[bstack11l1111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬሴ")] = bstack1ll11llll1l_opy_[0][bstack11l1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩስ")][0] if isinstance(bstack1ll11llll1l_opy_, list) else str(bstack1ll11llll1l_opy_)
            driver.execute_script(
                bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧሶ").format(
                    json.dumps(
                        {
                            bstack11l1111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣሷ"): bstack11l1111_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧሸ"),
                            bstack11l1111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨሹ"): bstack1ll1l111lll_opy_,
                        }
                    )
                )
            )
            f.bstack1llll111l11_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l11llll_opy_, True)
    @measure(event_name=EVENTS.bstack1l11111l1l_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1ll111l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤሺ")).get(bstack11l1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢሻ")):
            test_name = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111lll1_opy_, None)
            if not test_name:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧሼ"))
                return
            bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
            if not bstack1llll11l1l1_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤሽ") + str(bstack1llll11l111_opy_) + bstack11l1111_opy_ (u"ࠣࠤሾ"))
                return
            for bstack1lll11l111l_opy_, bstack1ll1111ll11_opy_ in bstack1llll11l1l1_opy_:
                if not bstack1lll1ll1l1l_opy_.bstack1ll1lllll1l_opy_(bstack1ll1111ll11_opy_):
                    continue
                driver = bstack1lll11l111l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢሿ").format(
                        json.dumps(
                            {
                                bstack11l1111_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥቀ"): bstack11l1111_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧቁ"),
                                bstack11l1111_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣቂ"): {bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቃ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llll111l11_opy_(instance, bstack111111l1ll_opy_.bstack1ll11lll1l1_opy_, True)
    def bstack1llllllll11_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        f: TestFramework,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1111llll_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        bstack1llll11l1l1_opy_ = [d for d, _ in f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])]
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢቄ"))
            return
        if not bstack1llll1ll1l1_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨቅ"))
            return
        for bstack1ll111l1l11_opy_ in bstack1llll11l1l1_opy_:
            driver = bstack1ll111l1l11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11l1111_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢቆ") + str(timestamp)
            driver.execute_script(
                bstack11l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣቇ").format(
                    json.dumps(
                        {
                            bstack11l1111_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦቈ"): bstack11l1111_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ቉"),
                            bstack11l1111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤቊ"): {
                                bstack11l1111_opy_ (u"ࠢࡵࡻࡳࡩࠧቋ"): bstack11l1111_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧቌ"),
                                bstack11l1111_opy_ (u"ࠤࡧࡥࡹࡧࠢቍ"): data,
                                bstack11l1111_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤ቎"): bstack11l1111_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥ቏")
                            }
                        }
                    )
                )
            )
    def bstack1llllll1111_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        f: TestFramework,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1ll1111llll_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        keys = [
            bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_,
            bstack111111l1ll_opy_.bstack1ll1l111ll1_opy_,
        ]
        bstack1llll11l1l1_opy_ = []
        for key in keys:
            bstack1llll11l1l1_opy_.extend(f.bstack1lllll1l11l_opy_(instance, key, []))
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢቐ"))
            return
        if f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1111111ll1_opy_, False):
            self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨቑ"))
            return
        self.bstack1lll1lll1l1_opy_()
        bstack1ll1l1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1llllll1lll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1ll1l11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l11ll1_opy_)
        req.test_framework_state = bstack1llll11l111_opy_[0].name
        req.test_hook_state = bstack1llll11l111_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
        for bstack1lll11l111l_opy_, driver in bstack1llll11l1l1_opy_:
            try:
                webdriver = bstack1lll11l111l_opy_()
                if webdriver is None:
                    self.logger.debug(bstack11l1111_opy_ (u"ࠢࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠦࠨࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࠣࡩࡽࡶࡩࡳࡧࡧ࠭ࠧቒ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack11l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢቓ")
                    if bstack1lll1ll1l1l_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1ll1l1l_opy_.bstack1ll1111l1ll_opy_, False)
                    else bstack11l1111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣቔ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1lll1ll1l1l_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1ll1l1l_opy_.bstack1ll1ll1l111_opy_, bstack11l1111_opy_ (u"ࠥࠦቕ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1lll1ll1l1l_opy_.bstack1lllll1l11l_opy_(driver, bstack1lll1ll1l1l_opy_.bstack1ll1l1l1ll1_opy_, bstack11l1111_opy_ (u"ࠦࠧቖ"))
                caps = None
                if hasattr(webdriver, bstack11l1111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ቗")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack11l1111_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡥ࡫ࡵࡩࡨࡺ࡬ࡺࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨቘ"))
                    except Exception as e:
                        self.logger.debug(bstack11l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠤࠧ቙") + str(e) + bstack11l1111_opy_ (u"ࠣࠤቚ"))
                try:
                    bstack1ll111l1111_opy_ = json.dumps(caps).encode(bstack11l1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቛ")) if caps else bstack1ll111l1lll_opy_ (u"ࠥࡿࢂࠨቜ")
                    req.capabilities = bstack1ll111l1111_opy_
                except Exception as e:
                    self.logger.debug(bstack11l1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡳࡦࡴ࡬ࡥࡱ࡯ࡺࡦࠢࡦࡥࡵࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࠢቝ") + str(e) + bstack11l1111_opy_ (u"ࠧࠨ቞"))
            except Exception as e:
                self.logger.error(bstack11l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡸࡪࡳ࠺ࠡࠤ቟") + str(str(e)) + bstack11l1111_opy_ (u"ࠢࠣበ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1llll1ll1l1_opy_() and len(bstack1llll11l1l1_opy_) == 0:
            bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l111ll1_opy_, [])
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቡ") + str(kwargs) + bstack11l1111_opy_ (u"ࠤࠥቢ"))
            return {}
        if len(bstack1llll11l1l1_opy_) > 1:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨባ") + str(kwargs) + bstack11l1111_opy_ (u"ࠦࠧቤ"))
            return {}
        bstack1lll11l111l_opy_, bstack1lll11ll11l_opy_ = bstack1llll11l1l1_opy_[0]
        driver = bstack1lll11l111l_opy_()
        if not driver:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢብ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢቦ"))
            return {}
        capabilities = f.bstack1lllll1l11l_opy_(bstack1lll11ll11l_opy_, bstack1lll1ll1l1l_opy_.bstack1ll1ll11l11_opy_)
        if not capabilities:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢቧ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤቨ"))
            return {}
        return capabilities.get(bstack11l1111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢቩ"), {})
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1llll1ll1l1_opy_() and len(bstack1llll11l1l1_opy_) == 0:
            bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1ll1l111ll1_opy_, [])
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቪ") + str(kwargs) + bstack11l1111_opy_ (u"ࠦࠧቫ"))
            return
        if len(bstack1llll11l1l1_opy_) > 1:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቬ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢቭ"))
        bstack1lll11l111l_opy_, bstack1lll11ll11l_opy_ = bstack1llll11l1l1_opy_[0]
        driver = bstack1lll11l111l_opy_()
        if not driver:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤቮ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤቯ"))
            return
        return driver