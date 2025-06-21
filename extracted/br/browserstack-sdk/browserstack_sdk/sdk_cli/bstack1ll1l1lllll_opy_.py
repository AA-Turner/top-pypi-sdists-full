# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1llllll1lll_opy_,
    bstack1111111111_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_, bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1ll11111lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1lll11ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1llll1l_opy_(bstack1ll11111lll_opy_):
    bstack1l1l11l1111_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢፖ")
    bstack1l1ll1l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣፗ")
    bstack1l1l11l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧፘ")
    bstack1l1l11l1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦፙ")
    bstack1l1l111lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤፚ")
    bstack1l1ll1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧ፛")
    bstack1l1l11l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥ፜")
    bstack1l1l11ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨ፝")
    def __init__(self):
        super().__init__(bstack1ll1111l111_opy_=self.bstack1l1l11l1111_opy_, frameworks=[bstack1llll111lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.BEFORE_EACH, bstack1lll1lll111_opy_.POST), self.bstack1l11ll1ll1l_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE), self.bstack1ll11l1l111_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll1l11ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lllll1ll_opy_ = self.bstack1l11ll111ll_opy_(instance.context)
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧ፞") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠦ፟"))
        f.bstack1lllll1111l_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, bstack1l1lllll1ll_opy_)
        bstack1l11ll1l111_opy_ = self.bstack1l11ll111ll_opy_(instance.context, bstack1l11ll11l1l_opy_=False)
        f.bstack1lllll1111l_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l111l_opy_, bstack1l11ll1l111_opy_)
    def bstack1ll11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll1l_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l11ll_opy_, False):
            self.__1l11ll1ll11_opy_(f,instance,bstack1lllll11ll1_opy_)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll1l_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        if not f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l11ll_opy_, False):
            self.__1l11ll1ll11_opy_(f, instance, bstack1lllll11ll1_opy_)
        if not f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11ll111_opy_, False):
            self.__1l11ll1l1ll_opy_(f, instance, bstack1lllll11ll1_opy_)
    def bstack1l11ll1l11l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll11111l11_opy_(instance):
            return
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11ll111_opy_, False):
            return
        driver.execute_script(
            bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤ፠").format(
                json.dumps(
                    {
                        bstack1l1l1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ፡"): bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ።"),
                        bstack1l1l1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ፣"): {bstack1l1l1l1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ፤"): result},
                    }
                )
            )
        )
        f.bstack1lllll1111l_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11ll111_opy_, True)
    def bstack1l11ll111ll_opy_(self, context: bstack1lllll1ll1l_opy_, bstack1l11ll11l1l_opy_= True):
        if bstack1l11ll11l1l_opy_:
            bstack1l1lllll1ll_opy_ = self.bstack1ll1111l1l1_opy_(context, reverse=True)
        else:
            bstack1l1lllll1ll_opy_ = self.bstack1ll11111l1l_opy_(context, reverse=True)
        return [f for f in bstack1l1lllll1ll_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1111ll11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def __1l11ll1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢ፥")).get(bstack1l1l1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ፦")):
            bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
            if not bstack1l1lllll1ll_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ፧") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠧࠨ፨"))
                return
            driver = bstack1l1lllll1ll_opy_[0][0]()
            status = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_, None)
            if not status:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣ፩") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣ፪"))
                return
            bstack1l1l111llll_opy_ = {bstack1l1l1l1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ፫"): status.lower()}
            bstack1l1l11l11l1_opy_ = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1l111l1l1_opy_, None)
            if status.lower() == bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ፬") and bstack1l1l11l11l1_opy_ is not None:
                bstack1l1l111llll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ፭")] = bstack1l1l11l11l1_opy_[0][bstack1l1l1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ፮")][0] if isinstance(bstack1l1l11l11l1_opy_, list) else str(bstack1l1l11l11l1_opy_)
            driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥ፯").format(
                    json.dumps(
                        {
                            bstack1l1l1l1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨ፰"): bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ፱"),
                            bstack1l1l1l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ፲"): bstack1l1l111llll_opy_,
                        }
                    )
                )
            )
            f.bstack1lllll1111l_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11ll111_opy_, True)
    @measure(event_name=EVENTS.bstack1ll11111l1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def __1l11ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢ፳")).get(bstack1l1l1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ፴")):
            test_name = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l11ll1l1l1_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥ፵"))
                return
            bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
            if not bstack1l1lllll1ll_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ፶") + str(bstack1lllll11ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢ፷"))
                return
            for bstack1l1l1ll111l_opy_, bstack1l11ll11ll1_opy_ in bstack1l1lllll1ll_opy_:
                if not bstack1llll111lll_opy_.bstack1ll11111l11_opy_(bstack1l11ll11ll1_opy_):
                    continue
                driver = bstack1l1l1ll111l_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ፸").format(
                        json.dumps(
                            {
                                bstack1l1l1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ፹"): bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ፺"),
                                bstack1l1l1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ፻"): {bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፼"): test_name},
                            }
                        )
                    )
                )
            f.bstack1lllll1111l_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l11ll_opy_, True)
    def bstack1l1ll1l11l1_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll1l_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        bstack1l1lllll1ll_opy_ = [d for d, _ in f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])]
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧ፽"))
            return
        if not bstack1l1lll11ll1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ፾"))
            return
        for bstack1l11ll11l11_opy_ in bstack1l1lllll1ll_opy_:
            driver = bstack1l11ll11l11_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1l1l1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧ፿") + str(timestamp)
            driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᎀ").format(
                    json.dumps(
                        {
                            bstack1l1l1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᎁ"): bstack1l1l1l1_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧᎂ"),
                            bstack1l1l1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᎃ"): {
                                bstack1l1l1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᎄ"): bstack1l1l1l1_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥᎅ"),
                                bstack1l1l1l1_opy_ (u"ࠢࡥࡣࡷࡥࠧᎆ"): data,
                                bstack1l1l1l1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᎇ"): bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣᎈ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1llll_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        f: TestFramework,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll1l_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        keys = [
            bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_,
            bstack1lll1llll1l_opy_.bstack1l1l11l111l_opy_,
        ]
        bstack1l1lllll1ll_opy_ = []
        for key in keys:
            bstack1l1lllll1ll_opy_.extend(f.bstack1lllll1ll11_opy_(instance, key, []))
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧᎉ"))
            return
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1ll111_opy_, False):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦᎊ"))
            return
        self.bstack1ll11l1l1ll_opy_()
        bstack1l1ll1l1ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
        for bstack1l1l1ll111l_opy_, driver in bstack1l1lllll1ll_opy_:
            try:
                webdriver = bstack1l1l1ll111l_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠤ࠭ࡸࡥࡧࡧࡵࡩࡳࡩࡥࠡࡧࡻࡴ࡮ࡸࡥࡥࠫࠥᎋ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧᎌ")
                    if bstack1llll111lll_opy_.bstack1lllll1ll11_opy_(driver, bstack1llll111lll_opy_.bstack1l11ll11lll_opy_, False)
                    else bstack1l1l1l1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩࠨᎍ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1llll111lll_opy_.bstack1lllll1ll11_opy_(driver, bstack1llll111lll_opy_.bstack1l1l11lllll_opy_, bstack1l1l1l1_opy_ (u"ࠣࠤᎎ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1llll111lll_opy_.bstack1lllll1ll11_opy_(driver, bstack1llll111lll_opy_.bstack1l1l11lll1l_opy_, bstack1l1l1l1_opy_ (u"ࠤࠥᎏ"))
                caps = None
                if hasattr(webdriver, bstack1l1l1l1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᎐")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡪࡩࡳࡧࡦࡸࡱࡿࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᎑"))
                    except Exception as e:
                        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥ᎒") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢ᎓"))
                try:
                    bstack1l11ll1111l_opy_ = json.dumps(caps).encode(bstack1l1l1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᎔")) if caps else bstack1l11ll111l1_opy_ (u"ࠣࡽࢀࠦ᎕")
                    req.capabilities = bstack1l11ll1111l_opy_
                except Exception as e:
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸ࡫ࡲࡪࡣ࡯࡭ࡿ࡫ࠠࡤࡣࡳࡷࠥ࡬࡯ࡳࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࠧ᎖") + str(e) + bstack1l1l1l1_opy_ (u"ࠥࠦ᎗"))
            except Exception as e:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡶࡨࡱ࠿ࠦࠢ᎘") + str(str(e)) + bstack1l1l1l1_opy_ (u"ࠧࠨ᎙"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1lll11ll1_opy_() and len(bstack1l1lllll1ll_opy_) == 0:
            bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ᎚") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠢࠣ᎛"))
            return {}
        if len(bstack1l1lllll1ll_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᎜") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥ᎝"))
            return {}
        bstack1l1l1ll111l_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1lllll1ll_opy_[0]
        driver = bstack1l1l1ll111l_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᎞") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧ᎟"))
            return {}
        capabilities = f.bstack1lllll1ll11_opy_(bstack1l1l1ll1l11_opy_, bstack1llll111lll_opy_.bstack1l1l1l1lll1_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᎠ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢᎡ"))
            return {}
        return capabilities.get(bstack1l1l1l1_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧᎢ"), {})
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1lll11ll1_opy_() and len(bstack1l1lllll1ll_opy_) == 0:
            bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᎣ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥᎤ"))
            return
        if len(bstack1l1lllll1ll_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᎥ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧᎦ"))
        bstack1l1l1ll111l_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1lllll1ll_opy_[0]
        driver = bstack1l1l1ll111l_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᎧ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢᎨ"))
            return
        return driver