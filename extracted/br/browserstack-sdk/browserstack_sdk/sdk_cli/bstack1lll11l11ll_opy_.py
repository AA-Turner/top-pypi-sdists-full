# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1111111ll1_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1lllllll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_, bstack1llll111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll1l_opy_ import bstack1ll1111ll11_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll111ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1l1l1l1_opy_(bstack1ll1111ll11_opy_):
    bstack1l1l111lll1_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨፕ")
    bstack1l1ll11ll11_opy_ = bstack11ll11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢፖ")
    bstack1l1l11l1l1l_opy_ = bstack11ll11_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦፗ")
    bstack1l1l11ll11l_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥፘ")
    bstack1l1l11l1111_opy_ = bstack11ll11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣፙ")
    bstack1l1llllll11_opy_ = bstack11ll11_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦፚ")
    bstack1l1l11ll1l1_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤ፛")
    bstack1l1l111l1ll_opy_ = bstack11ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧ፜")
    def __init__(self):
        super().__init__(bstack1ll111111ll_opy_=self.bstack1l1l111lll1_opy_, frameworks=[bstack1llll11l111_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.BEFORE_EACH, bstack1ll1l1lll11_opy_.POST), self.bstack1l11ll1ll11_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE), self.bstack1ll11ll1l1l_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll1l111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll11l1l_opy_ = self.bstack1l11ll111l1_opy_(instance.context)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦ፝") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠤࠥ፞"))
        f.bstack1llllllllll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, bstack1l1lll11l1l_opy_)
        bstack1l11ll1l1l1_opy_ = self.bstack1l11ll111l1_opy_(instance.context, bstack1l11ll11l11_opy_=False)
        f.bstack1llllllllll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11l1l1l_opy_, bstack1l11ll1l1l1_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll11_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11ll1l1_opy_, False):
            self.__1l11ll1ll1l_opy_(f,instance,bstack111111111l_opy_)
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll11_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        if not f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11ll1l1_opy_, False):
            self.__1l11ll1ll1l_opy_(f, instance, bstack111111111l_opy_)
        if not f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111l1ll_opy_, False):
            self.__1l11ll1l111_opy_(f, instance, bstack111111111l_opy_)
    def bstack1l11ll1111l_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll11111ll1_opy_(instance):
            return
        if f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111l1ll_opy_, False):
            return
        driver.execute_script(
            bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣ፟").format(
                json.dumps(
                    {
                        bstack11ll11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦ፠"): bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ፡"),
                        bstack11ll11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ።"): {bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ፣"): result},
                    }
                )
            )
        )
        f.bstack1llllllllll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111l1ll_opy_, True)
    def bstack1l11ll111l1_opy_(self, context: bstack1lllllll1l1_opy_, bstack1l11ll11l11_opy_= True):
        if bstack1l11ll11l11_opy_:
            bstack1l1lll11l1l_opy_ = self.bstack1ll11111lll_opy_(context, reverse=True)
        else:
            bstack1l1lll11l1l_opy_ = self.bstack1ll1111111l_opy_(context, reverse=True)
        return [f for f in bstack1l1lll11l1l_opy_ if f[1].state != bstack1111111l11_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1ll1111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ፤")).get(bstack11ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ፥")):
            bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
            if not bstack1l1lll11l1l_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ፦") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠦࠧ፧"))
                return
            driver = bstack1l1lll11l1l_opy_[0][0]()
            status = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_, None)
            if not status:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ፨") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠨࠢ፩"))
                return
            bstack1l1l111llll_opy_ = {bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ፪"): status.lower()}
            bstack1l1l11ll111_opy_ = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1l11l1lll_opy_, None)
            if status.lower() == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ፫") and bstack1l1l11ll111_opy_ is not None:
                bstack1l1l111llll_opy_[bstack11ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ፬")] = bstack1l1l11ll111_opy_[0][bstack11ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭፭")][0] if isinstance(bstack1l1l11ll111_opy_, list) else str(bstack1l1l11ll111_opy_)
            driver.execute_script(
                bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤ፮").format(
                    json.dumps(
                        {
                            bstack11ll11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ፯"): bstack11ll11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ፰"),
                            bstack11ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ፱"): bstack1l1l111llll_opy_,
                        }
                    )
                )
            )
            f.bstack1llllllllll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l111l1ll_opy_, True)
    @measure(event_name=EVENTS.bstack1l11ll11_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1l11ll1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸࠨ፲")).get(bstack11ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ፳")):
            test_name = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l11ll1l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤ፴"))
                return
            bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
            if not bstack1l1lll11l1l_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ፵") + str(bstack111111111l_opy_) + bstack11ll11_opy_ (u"ࠧࠨ፶"))
                return
            for bstack1l1l1ll11l1_opy_, bstack1l11ll111ll_opy_ in bstack1l1lll11l1l_opy_:
                if not bstack1llll11l111_opy_.bstack1ll11111ll1_opy_(bstack1l11ll111ll_opy_):
                    continue
                driver = bstack1l1l1ll11l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦ፷").format(
                        json.dumps(
                            {
                                bstack11ll11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢ፸"): bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ፹"),
                                bstack11ll11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ፺"): {bstack11ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ፻"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llllllllll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11ll1l1_opy_, True)
    def bstack1l1ll11llll_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll11_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        bstack1l1lll11l1l_opy_ = [d for d, _ in f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])]
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦ፼"))
            return
        if not bstack1l1ll111ll1_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ፽"))
            return
        for bstack1l11ll11ll1_opy_ in bstack1l1lll11l1l_opy_:
            driver = bstack1l11ll11ll1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11ll11_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦ፾") + str(timestamp)
            driver.execute_script(
                bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ፿").format(
                    json.dumps(
                        {
                            bstack11ll11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᎀ"): bstack11ll11_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦᎁ"),
                            bstack11ll11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᎂ"): {
                                bstack11ll11_opy_ (u"ࠦࡹࡿࡰࡦࠤᎃ"): bstack11ll11_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤᎄ"),
                                bstack11ll11_opy_ (u"ࠨࡤࡢࡶࡤࠦᎅ"): data,
                                bstack11ll11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨᎆ"): bstack11ll11_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢᎇ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll11l11l_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        f: TestFramework,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11ll1ll11_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        keys = [
            bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_,
            bstack1lll1l1l1l1_opy_.bstack1l1l11l1l1l_opy_,
        ]
        bstack1l1lll11l1l_opy_ = []
        for key in keys:
            bstack1l1lll11l1l_opy_.extend(f.bstack1lllll1l1ll_opy_(instance, key, []))
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦᎈ"))
            return
        if f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1llllll11_opy_, False):
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥᎉ"))
            return
        self.bstack1ll1l1l1111_opy_()
        bstack1ll1lll1ll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11111l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        req.test_uuid = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11ll11_opy_)
        for bstack1l1l1ll11l1_opy_, driver in bstack1l1lll11l1l_opy_:
            try:
                webdriver = bstack1l1l1ll11l1_opy_()
                if webdriver is None:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࠬࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࠠࡦࡺࡳ࡭ࡷ࡫ࡤࠪࠤᎊ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦᎋ")
                    if bstack1llll11l111_opy_.bstack1lllll1l1ll_opy_(driver, bstack1llll11l111_opy_.bstack1l11ll1l11l_opy_, False)
                    else bstack11ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧᎌ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1llll11l111_opy_.bstack1lllll1l1ll_opy_(driver, bstack1llll11l111_opy_.bstack1l1l1l11l1l_opy_, bstack11ll11_opy_ (u"ࠢࠣᎍ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1llll11l111_opy_.bstack1lllll1l1ll_opy_(driver, bstack1llll11l111_opy_.bstack1l1l1l11l11_opy_, bstack11ll11_opy_ (u"ࠣࠤᎎ"))
                caps = None
                if hasattr(webdriver, bstack11ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎏ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack11ll11_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡩ࡯ࡲࡦࡥࡷࡰࡾࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠲ࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᎐"))
                    except Exception as e:
                        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࠤ᎑") + str(e) + bstack11ll11_opy_ (u"ࠧࠨ᎒"))
                try:
                    bstack1l11ll11l1l_opy_ = json.dumps(caps).encode(bstack11ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᎓")) if caps else bstack1l11ll11lll_opy_ (u"ࠢࡼࡿࠥ᎔")
                    req.capabilities = bstack1l11ll11l1l_opy_
                except Exception as e:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡷࡪࡸࡩࡢ࡮࡬ࡾࡪࠦࡣࡢࡲࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࠦ᎕") + str(e) + bstack11ll11_opy_ (u"ࠤࠥ᎖"))
            except Exception as e:
                self.logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡩࡵࡧࡰ࠾ࠥࠨ᎗") + str(str(e)) + bstack11ll11_opy_ (u"ࠦࠧ᎘"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1ll111ll1_opy_() and len(bstack1l1lll11l1l_opy_) == 0:
            bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11l1l1l_opy_, [])
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᎙") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢ᎚"))
            return {}
        if len(bstack1l1lll11l1l_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᎛") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤ᎜"))
            return {}
        bstack1l1l1ll11l1_opy_, bstack1l1l1lll111_opy_ = bstack1l1lll11l1l_opy_[0]
        driver = bstack1l1l1ll11l1_opy_()
        if not driver:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᎝") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦ᎞"))
            return {}
        capabilities = f.bstack1lllll1l1ll_opy_(bstack1l1l1lll111_opy_, bstack1llll11l111_opy_.bstack1l1l1l11111_opy_)
        if not capabilities:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᎟") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨᎠ"))
            return {}
        return capabilities.get(bstack11ll11_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦᎡ"), {})
    def bstack1ll11ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1ll111ll1_opy_() and len(bstack1l1lll11l1l_opy_) == 0:
            bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1l11l1l1l_opy_, [])
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᎢ") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤᎣ"))
            return
        if len(bstack1l1lll11l1l_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᎤ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦᎥ"))
        bstack1l1l1ll11l1_opy_, bstack1l1l1lll111_opy_ = bstack1l1lll11l1l_opy_[0]
        driver = bstack1l1l1ll11l1_opy_()
        if not driver:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᎦ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨᎧ"))
            return
        return driver