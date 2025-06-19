# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1111111l11_opy_,
    bstack1llllll111l_opy_,
    bstack1llllllll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lllll1111l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l1l_opy_ import bstack1ll111l1111_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll11l1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1ll1111_opy_(bstack1ll111l1111_opy_):
    bstack1l1l1l11l1l_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨፇ")
    bstack1ll1111lll1_opy_ = bstack111lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢፈ")
    bstack1l1l11lll11_opy_ = bstack111lll_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦፉ")
    bstack1l1l11lll1l_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥፊ")
    bstack1l1l1l11111_opy_ = bstack111lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣፋ")
    bstack1ll111111ll_opy_ = bstack111lll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦፌ")
    bstack1l1l1l111ll_opy_ = bstack111lll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤፍ")
    bstack1l1l1l111l1_opy_ = bstack111lll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧፎ")
    def __init__(self):
        super().__init__(bstack1ll111l1l11_opy_=self.bstack1l1l1l11l1l_opy_, frameworks=[bstack1llll111lll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.BEFORE_EACH, bstack1lllll1111l_opy_.POST), self.bstack1l11lll1ll1_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE), self.bstack1ll1ll11111_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll1111l11l_opy_ = self.bstack1l11lll1111_opy_(instance.context)
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦፏ") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠤࠥፐ"))
        f.bstack11111ll111_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, bstack1ll1111l11l_opy_)
        bstack1l11lll111l_opy_ = self.bstack1l11lll1111_opy_(instance.context, bstack1l11lll11l1_opy_=False)
        f.bstack11111ll111_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l11lll11_opy_, bstack1l11lll111l_opy_)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if not f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111ll_opy_, False):
            self.__1l11llll11l_opy_(f,instance,bstack11111l1l11_opy_)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        if not f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111ll_opy_, False):
            self.__1l11llll11l_opy_(f, instance, bstack11111l1l11_opy_)
        if not f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111l1_opy_, False):
            self.__1l11lll1lll_opy_(f, instance, bstack11111l1l11_opy_)
    def bstack1l11lll1l1l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll111l111l_opy_(instance):
            return
        if f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111l1_opy_, False):
            return
        driver.execute_script(
            bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣፑ").format(
                json.dumps(
                    {
                        bstack111lll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦፒ"): bstack111lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣፓ"),
                        bstack111lll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤፔ"): {bstack111lll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢፕ"): result},
                    }
                )
            )
        )
        f.bstack11111ll111_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111l1_opy_, True)
    def bstack1l11lll1111_opy_(self, context: bstack1llllllll11_opy_, bstack1l11lll11l1_opy_= True):
        if bstack1l11lll11l1_opy_:
            bstack1ll1111l11l_opy_ = self.bstack1ll111l11l1_opy_(context, reverse=True)
        else:
            bstack1ll1111l11l_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        return [f for f in bstack1ll1111l11l_opy_ if f[1].state != bstack1111111111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1l11lll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨፖ")).get(bstack111lll_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨፗ")):
            bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
            if not bstack1ll1111l11l_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨፘ") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠦࠧፙ"))
                return
            driver = bstack1ll1111l11l_opy_[0][0]()
            status = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l1l1l1l1_opy_, None)
            if not status:
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢፚ") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠨࠢ፛"))
                return
            bstack1l1l1l1111l_opy_ = {bstack111lll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ፜"): status.lower()}
            bstack1l1l11ll11l_opy_ = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_, None)
            if status.lower() == bstack111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ፝") and bstack1l1l11ll11l_opy_ is not None:
                bstack1l1l1l1111l_opy_[bstack111lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ፞")] = bstack1l1l11ll11l_opy_[0][bstack111lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭፟")][0] if isinstance(bstack1l1l11ll11l_opy_, list) else str(bstack1l1l11ll11l_opy_)
            driver.execute_script(
                bstack111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤ፠").format(
                    json.dumps(
                        {
                            bstack111lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ፡"): bstack111lll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ።"),
                            bstack111lll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ፣"): bstack1l1l1l1111l_opy_,
                        }
                    )
                )
            )
            f.bstack11111ll111_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111l1_opy_, True)
    @measure(event_name=EVENTS.bstack1l111l11ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1l11llll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ፤")).get(bstack111lll_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ፥")):
            test_name = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11lllll11_opy_, None)
            if not test_name:
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤ፦"))
                return
            bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
            if not bstack1ll1111l11l_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ፧") + str(bstack11111l1l11_opy_) + bstack111lll_opy_ (u"ࠧࠨ፨"))
                return
            for bstack1l1ll111111_opy_, bstack1l11lll1l11_opy_ in bstack1ll1111l11l_opy_:
                if not bstack1llll111lll_opy_.bstack1ll111l111l_opy_(bstack1l11lll1l11_opy_):
                    continue
                driver = bstack1l1ll111111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦ፩").format(
                        json.dumps(
                            {
                                bstack111lll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢ፪"): bstack111lll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ፫"),
                                bstack111lll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ፬"): {bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ፭"): test_name},
                            }
                        )
                    )
                )
            f.bstack11111ll111_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l1l111ll_opy_, True)
    def bstack1l1lll1lll1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        bstack1ll1111l11l_opy_ = [d for d, _ in f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])]
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦ፮"))
            return
        if not bstack1l1ll11l1ll_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ፯"))
            return
        for bstack1l11llll1l1_opy_ in bstack1ll1111l11l_opy_:
            driver = bstack1l11llll1l1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111lll_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦ፰") + str(timestamp)
            driver.execute_script(
                bstack111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ፱").format(
                    json.dumps(
                        {
                            bstack111lll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ፲"): bstack111lll_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ፳"),
                            bstack111lll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ፴"): {
                                bstack111lll_opy_ (u"ࠦࡹࡿࡰࡦࠤ፵"): bstack111lll_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤ፶"),
                                bstack111lll_opy_ (u"ࠨࡤࡢࡶࡤࠦ፷"): data,
                                bstack111lll_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ፸"): bstack111lll_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢ፹")
                            }
                        }
                    )
                )
            )
    def bstack1l1llll1lll_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        f: TestFramework,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11lll1ll1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        keys = [
            bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_,
            bstack1lll1ll1111_opy_.bstack1l1l11lll11_opy_,
        ]
        bstack1ll1111l11l_opy_ = []
        for key in keys:
            bstack1ll1111l11l_opy_.extend(f.bstack1llllll1l1l_opy_(instance, key, []))
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦ፺"))
            return
        if f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll111111ll_opy_, False):
            self.logger.debug(bstack111lll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥ፻"))
            return
        self.bstack1ll11ll1l11_opy_()
        bstack11ll1ll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l11ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11ll11ll_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_)
        req.test_framework_state = bstack11111l1l11_opy_[0].name
        req.test_hook_state = bstack11111l1l11_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        for bstack1l1ll111111_opy_, driver in bstack1ll1111l11l_opy_:
            try:
                webdriver = bstack1l1ll111111_opy_()
                if webdriver is None:
                    self.logger.debug(bstack111lll_opy_ (u"ࠦ࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࠬࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࠠࡦࡺࡳ࡭ࡷ࡫ࡤࠪࠤ፼"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦ፽")
                    if bstack1llll111lll_opy_.bstack1llllll1l1l_opy_(driver, bstack1llll111lll_opy_.bstack1l11lll11ll_opy_, False)
                    else bstack111lll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧ፾")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1llll111lll_opy_.bstack1llllll1l1l_opy_(driver, bstack1llll111lll_opy_.bstack1l1l1lll1l1_opy_, bstack111lll_opy_ (u"ࠢࠣ፿"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1llll111lll_opy_.bstack1llllll1l1l_opy_(driver, bstack1llll111lll_opy_.bstack1l1l1llll11_opy_, bstack111lll_opy_ (u"ࠣࠤᎀ"))
                caps = None
                if hasattr(webdriver, bstack111lll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎁ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack111lll_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡩ࡯ࡲࡦࡥࡷࡰࡾࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᎂ"))
                    except Exception as e:
                        self.logger.debug(bstack111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࠤᎃ") + str(e) + bstack111lll_opy_ (u"ࠧࠨᎄ"))
                try:
                    bstack1l11llll1ll_opy_ = json.dumps(caps).encode(bstack111lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᎅ")) if caps else bstack1l11llll111_opy_ (u"ࠢࡼࡿࠥᎆ")
                    req.capabilities = bstack1l11llll1ll_opy_
                except Exception as e:
                    self.logger.debug(bstack111lll_opy_ (u"ࠣࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡷࡪࡸࡩࡢ࡮࡬ࡾࡪࠦࡣࡢࡲࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࠦᎇ") + str(e) + bstack111lll_opy_ (u"ࠤࠥᎈ"))
            except Exception as e:
                self.logger.error(bstack111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩࡵࡧࡰ࠾ࠥࠨᎉ") + str(str(e)) + bstack111lll_opy_ (u"ࠦࠧᎊ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1ll11l1ll_opy_() and len(bstack1ll1111l11l_opy_) == 0:
            bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l11lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᎋ") + str(kwargs) + bstack111lll_opy_ (u"ࠨࠢᎌ"))
            return {}
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᎍ") + str(kwargs) + bstack111lll_opy_ (u"ࠣࠤᎎ"))
            return {}
        bstack1l1ll111111_opy_, bstack1l1l1lllll1_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll111111_opy_()
        if not driver:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᎏ") + str(kwargs) + bstack111lll_opy_ (u"ࠥࠦ᎐"))
            return {}
        capabilities = f.bstack1llllll1l1l_opy_(bstack1l1l1lllll1_opy_, bstack1llll111lll_opy_.bstack1l1l1l1l1ll_opy_)
        if not capabilities:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᎑") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨ᎒"))
            return {}
        return capabilities.get(bstack111lll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦ᎓"), {})
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1ll11l1ll_opy_() and len(bstack1ll1111l11l_opy_) == 0:
            bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1l11lll11_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᎔") + str(kwargs) + bstack111lll_opy_ (u"ࠣࠤ᎕"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᎖") + str(kwargs) + bstack111lll_opy_ (u"ࠥࠦ᎗"))
        bstack1l1ll111111_opy_, bstack1l1l1lllll1_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll111111_opy_()
        if not driver:
            self.logger.debug(bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᎘") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨ᎙"))
            return
        return driver