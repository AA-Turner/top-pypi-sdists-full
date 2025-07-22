# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack11111111ll_opy_,
    bstack1lllll1ll1l_opy_,
    bstack1llll1ll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_, bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1l1llll1lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll11llll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1ll1ll1l_opy_(bstack1l1llll1lll_opy_):
    bstack1l1l111ll11_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥᎴ")
    bstack1l1llll111l_opy_ = bstack111l111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦᎵ")
    bstack1l1l111l1ll_opy_ = bstack111l111_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᎶ")
    bstack1l1l1111l1l_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᎷ")
    bstack1l11lllllll_opy_ = bstack111l111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧᎸ")
    bstack1l1l1llll11_opy_ = bstack111l111_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᎹ")
    bstack1l11lllll1l_opy_ = bstack111l111_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᎺ")
    bstack1l1l1111lll_opy_ = bstack111l111_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤᎻ")
    def __init__(self):
        super().__init__(bstack1ll1111111l_opy_=self.bstack1l1l111ll11_opy_, frameworks=[bstack1lll1l11l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.BEFORE_EACH, bstack1lll111llll_opy_.POST), self.bstack1l11l1ll1ll_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll111lll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1lll11_opy_ = self.bstack1l11l1llll1_opy_(instance.context)
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣᎼ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠨࠢᎽ"))
        f.bstack1111111111_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, bstack1l1ll1lll11_opy_)
        bstack1l11l1lll1l_opy_ = self.bstack1l11l1llll1_opy_(instance.context, bstack1l11l1lll11_opy_=False)
        f.bstack1111111111_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l111l1ll_opy_, bstack1l11l1lll1l_opy_)
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll1ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if not f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l11lllll1l_opy_, False):
            self.__1l11l1ll11l_opy_(f,instance,bstack1llllll111l_opy_)
    def bstack1ll111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll1ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        if not f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l11lllll1l_opy_, False):
            self.__1l11l1ll11l_opy_(f, instance, bstack1llllll111l_opy_)
        if not f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l1111lll_opy_, False):
            self.__1l11l1ll1l1_opy_(f, instance, bstack1llllll111l_opy_)
    def bstack1l11l1l11l1_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1l1llllll1l_opy_(instance):
            return
        if f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l1111lll_opy_, False):
            return
        driver.execute_script(
            bstack111l111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧᎾ").format(
                json.dumps(
                    {
                        bstack111l111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣᎿ"): bstack111l111_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᏀ"),
                        bstack111l111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨᏁ"): {bstack111l111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᏂ"): result},
                    }
                )
            )
        )
        f.bstack1111111111_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l1111lll_opy_, True)
    def bstack1l11l1llll1_opy_(self, context: bstack1llll1ll11l_opy_, bstack1l11l1lll11_opy_= True):
        if bstack1l11l1lll11_opy_:
            bstack1l1ll1lll11_opy_ = self.bstack1l1lllllll1_opy_(context, reverse=True)
        else:
            bstack1l1ll1lll11_opy_ = self.bstack1l1llll1ll1_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1lll11_opy_ if f[1].state != bstack1lllllll11l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1l11l1ll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᏃ")).get(bstack111l111_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᏄ")):
            bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
            if not bstack1l1ll1lll11_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᏅ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠣࠤᏆ"))
                return
            driver = bstack1l1ll1lll11_opy_[0][0]()
            status = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1111111_opy_, None)
            if not status:
                self.logger.debug(bstack111l111_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᏇ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠥࠦᏈ"))
                return
            bstack1l11llll1ll_opy_ = {bstack111l111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᏉ"): status.lower()}
            bstack1l1l111l1l1_opy_ = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1l11lllll11_opy_, None)
            if status.lower() == bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏊ") and bstack1l1l111l1l1_opy_ is not None:
                bstack1l11llll1ll_opy_[bstack111l111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭Ꮛ")] = bstack1l1l111l1l1_opy_[0][bstack111l111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᏌ")][0] if isinstance(bstack1l1l111l1l1_opy_, list) else str(bstack1l1l111l1l1_opy_)
            driver.execute_script(
                bstack111l111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᏍ").format(
                    json.dumps(
                        {
                            bstack111l111_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᏎ"): bstack111l111_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᏏ"),
                            bstack111l111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᏐ"): bstack1l11llll1ll_opy_,
                        }
                    )
                )
            )
            f.bstack1111111111_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l1111lll_opy_, True)
    @measure(event_name=EVENTS.bstack11llllll11_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1l11l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᏑ")).get(bstack111l111_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᏒ")):
            test_name = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1l11l1l1l11_opy_, None)
            if not test_name:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᏓ"))
                return
            bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
            if not bstack1l1ll1lll11_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥᏔ") + str(bstack1llllll111l_opy_) + bstack111l111_opy_ (u"ࠤࠥᏕ"))
                return
            for bstack1l1l1l11lll_opy_, bstack1l11l1l11ll_opy_ in bstack1l1ll1lll11_opy_:
                if not bstack1lll1l11l11_opy_.bstack1l1llllll1l_opy_(bstack1l11l1l11ll_opy_):
                    continue
                driver = bstack1l1l1l11lll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack111l111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣᏖ").format(
                        json.dumps(
                            {
                                bstack111l111_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦᏗ"): bstack111l111_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᏘ"),
                                bstack111l111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤᏙ"): {bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏚ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1111111111_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l11lllll1l_opy_, True)
    def bstack1l1lll1l1ll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll1ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        bstack1l1ll1lll11_opy_ = [d for d, _ in f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])]
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᏛ"))
            return
        if not bstack1l1ll11llll_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏜ"))
            return
        for bstack1l11l1l1l1l_opy_ in bstack1l1ll1lll11_opy_:
            driver = bstack1l11l1l1l1l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack111l111_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣᏝ") + str(timestamp)
            driver.execute_script(
                bstack111l111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᏞ").format(
                    json.dumps(
                        {
                            bstack111l111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᏟ"): bstack111l111_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣᏠ"),
                            bstack111l111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᏡ"): {
                                bstack111l111_opy_ (u"ࠣࡶࡼࡴࡪࠨᏢ"): bstack111l111_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨᏣ"),
                                bstack111l111_opy_ (u"ࠥࡨࡦࡺࡡࠣᏤ"): data,
                                bstack111l111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᏥ"): bstack111l111_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦᏦ")
                            }
                        }
                    )
                )
            )
    def bstack1l1ll111111_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        f: TestFramework,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l11l1ll1ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        keys = [
            bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_,
            bstack1ll1ll1ll1l_opy_.bstack1l1l111l1ll_opy_,
        ]
        bstack1l1ll1lll11_opy_ = []
        for key in keys:
            bstack1l1ll1lll11_opy_.extend(f.bstack1111111l1l_opy_(instance, key, []))
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡱࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡵࡱࠣࡰ࡮ࡴ࡫ࠣᏧ"))
            return
        if f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l1llll11_opy_, False):
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡅࡅࡘࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡣࡳࡧࡤࡸࡪࡪࠢᏨ"))
            return
        self.bstack1ll111l1l11_opy_()
        bstack1l1111lll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
        req.test_framework_name = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_)
        req.test_framework_state = bstack1llllll111l_opy_[0].name
        req.test_hook_state = bstack1llllll111l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
        for bstack1l1l1l11lll_opy_, driver in bstack1l1ll1lll11_opy_:
            try:
                webdriver = bstack1l1l1l11lll_opy_()
                if webdriver is None:
                    self.logger.debug(bstack111l111_opy_ (u"࡙ࠣࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࠩࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠤࡪࡾࡰࡪࡴࡨࡨ࠮ࠨᏩ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack111l111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣᏪ")
                    if bstack1lll1l11l11_opy_.bstack1111111l1l_opy_(driver, bstack1lll1l11l11_opy_.bstack1l11l1ll111_opy_, False)
                    else bstack111l111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤᏫ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1lll1l11l11_opy_.bstack1111111l1l_opy_(driver, bstack1lll1l11l11_opy_.bstack1l1l11l11l1_opy_, bstack111l111_opy_ (u"ࠦࠧᏬ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1lll1l11l11_opy_.bstack1111111l1l_opy_(driver, bstack1lll1l11l11_opy_.bstack1l1l111lll1_opy_, bstack111l111_opy_ (u"ࠧࠨᏭ"))
                caps = None
                if hasattr(webdriver, bstack111l111_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᏮ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack111l111_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡦ࡬ࡶࡪࡩࡴ࡭ࡻࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᏯ"))
                    except Exception as e:
                        self.logger.debug(bstack111l111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࠨᏰ") + str(e) + bstack111l111_opy_ (u"ࠤࠥᏱ"))
                try:
                    bstack1l11l1l1ll1_opy_ = json.dumps(caps).encode(bstack111l111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᏲ")) if caps else bstack1l11l1l1lll_opy_ (u"ࠦࢀࢃࠢᏳ")
                    req.capabilities = bstack1l11l1l1ll1_opy_
                except Exception as e:
                    self.logger.debug(bstack111l111_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡴࡧࡵ࡭ࡦࡲࡩࡻࡧࠣࡧࡦࡶࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࠣᏴ") + str(e) + bstack111l111_opy_ (u"ࠨࠢᏵ"))
            except Exception as e:
                self.logger.error(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡹ࡫࡭࠻ࠢࠥ᏶") + str(str(e)) + bstack111l111_opy_ (u"ࠣࠤ᏷"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1ll11llll_opy_() and len(bstack1l1ll1lll11_opy_) == 0:
            bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l111l1ll_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏸ") + str(kwargs) + bstack111l111_opy_ (u"ࠥࠦᏹ"))
            return {}
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏺ") + str(kwargs) + bstack111l111_opy_ (u"ࠧࠨᏻ"))
            return {}
        bstack1l1l1l11lll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏼ") + str(kwargs) + bstack111l111_opy_ (u"ࠢࠣᏽ"))
            return {}
        capabilities = f.bstack1111111l1l_opy_(bstack1l1l1l1ll11_opy_, bstack1lll1l11l11_opy_.bstack1l1l111ll1l_opy_)
        if not capabilities:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᏾") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥ᏿"))
            return {}
        return capabilities.get(bstack111l111_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣ᐀"), {})
    def bstack1ll11lll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1ll11llll_opy_() and len(bstack1l1ll1lll11_opy_) == 0:
            bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1l111l1ll_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐁ") + str(kwargs) + bstack111l111_opy_ (u"ࠧࠨᐂ"))
            return
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack111l111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐃ") + str(kwargs) + bstack111l111_opy_ (u"ࠢࠣᐄ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐅ") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥᐆ"))
            return
        return driver