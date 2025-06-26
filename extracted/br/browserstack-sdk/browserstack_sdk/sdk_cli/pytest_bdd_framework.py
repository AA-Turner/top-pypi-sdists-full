# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1lllll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1l11_opy_ import bstack1l111l1l111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1ll111l_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1lll1111l1l_opy_,
    bstack1l111l11l11_opy_,
    bstack1lll111ll1l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll1l11l1_opy_
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1lll_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111ll11_opy_
bstack1l1l1llll11_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l1l1ll1ll1_opy_ = bstack11ll1l1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᏣ")
bstack1l11l111ll1_opy_ = bstack11ll1l1_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᏤ")
bstack1l1111l1l11_opy_ = bstack11ll1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᏥ")
bstack1l11111l1l1_opy_ = 1.0
_1l1ll11l1l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111lllll1_opy_ = bstack11ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᏦ")
    bstack1l111111111_opy_ = bstack11ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᏧ")
    bstack11lllllll11_opy_ = bstack11ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᏨ")
    bstack1l1111111ll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᏩ")
    bstack1l11111ll11_opy_ = bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᏪ")
    bstack1l111l111l1_opy_: bool
    bstack111111lll1_opy_: bstack111111ll11_opy_  = None
    bstack1l111l1lll1_opy_ = [
        bstack1lll1ll111l_opy_.BEFORE_ALL,
        bstack1lll1ll111l_opy_.AFTER_ALL,
        bstack1lll1ll111l_opy_.BEFORE_EACH,
        bstack1lll1ll111l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1111l11l1_opy_: Dict[str, str],
        bstack1ll11l1l1ll_opy_: List[str]=[bstack11ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᏫ")],
        bstack111111lll1_opy_: bstack111111ll11_opy_ = None,
        bstack1lll1l1ll1l_opy_=None
    ):
        super().__init__(bstack1ll11l1l1ll_opy_, bstack1l1111l11l1_opy_, bstack111111lll1_opy_)
        self.bstack1l111l111l1_opy_ = any(bstack11ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᏬ") in item.lower() for item in bstack1ll11l1l1ll_opy_)
        self.bstack1lll1l1ll1l_opy_ = bstack1lll1l1ll1l_opy_
    def track_event(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1ll111l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l1lll1_opy_:
            bstack1l111l1l111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1ll111l_opy_.NONE:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᏭ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠨࠢᏮ"))
            return
        if not self.bstack1l111l111l1_opy_:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᏯ") + str(str(self.bstack1ll11l1l1ll_opy_)) + bstack11ll1l1_opy_ (u"ࠣࠤᏰ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᏱ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦᏲ"))
            return
        instance = self.__1l1111ll111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᏳ") + str(args) + bstack11ll1l1_opy_ (u"ࠧࠨᏴ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1lll1_opy_ and test_hook_state == bstack1lll1111l1l_opy_.PRE:
                bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack11l1111ll1_opy_.value)
                name = str(EVENTS.bstack11l1111ll1_opy_.name)+bstack11ll1l1_opy_ (u"ࠨ࠺ࠣᏵ")+str(test_framework_state.name)
                TestFramework.bstack1l1111lll1l_opy_(instance, name, bstack1ll11l111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦ᏶").format(e))
        try:
            if test_framework_state == bstack1lll1ll111l_opy_.TEST:
                if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l111l11lll_opy_) and test_hook_state == bstack1lll1111l1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111111ll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11ll1l1_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣ᏷") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠤࠥᏸ"))
                if test_hook_state == bstack1lll1111l1l_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11ll1_opy_):
                    TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1lll11ll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l111lll1l1_opy_(instance, args)
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᏹ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠦࠧᏺ"))
                elif test_hook_state == bstack1lll1111l1l_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1l1lll111_opy_):
                    TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᏻ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠨࠢᏼ"))
            elif test_framework_state == bstack1lll1ll111l_opy_.STEP:
                if test_hook_state == bstack1lll1111l1l_opy_.PRE:
                    PytestBDDFramework.__1l11111l1ll_opy_(instance, args)
                elif test_hook_state == bstack1lll1111l1l_opy_.POST:
                    PytestBDDFramework.__1l1111l1ll1_opy_(instance, args)
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG and test_hook_state == bstack1lll1111l1l_opy_.POST:
                PytestBDDFramework.__1l111111lll_opy_(instance, *args)
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG_REPORT and test_hook_state == bstack1lll1111l1l_opy_.POST:
                self.__1l111l11l1l_opy_(instance, *args)
                self.__1l11l1111ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l1lll1_opy_:
                self.__1l11111111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᏽ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠣࠤ᏾"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111111l1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1lll1_opy_ and test_hook_state == bstack1lll1111l1l_opy_.POST:
                name = str(EVENTS.bstack11l1111ll1_opy_.name)+bstack11ll1l1_opy_ (u"ࠤ࠽ࠦ᏿")+str(test_framework_state.name)
                bstack1ll11l111ll_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1llll11lll1_opy_.end(EVENTS.bstack11l1111ll1_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᐀"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᐁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᐂ").format(e))
    def bstack1l1l1lll1l1_opy_(self):
        return self.bstack1l111l111l1_opy_
    def __1l1111l111l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᐃ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1l1l1l_opy_(rep, [bstack11ll1l1_opy_ (u"ࠢࡸࡪࡨࡲࠧᐄ"), bstack11ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᐅ"), bstack11ll1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᐆ"), bstack11ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᐇ"), bstack11ll1l1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᐈ"), bstack11ll1l1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᐉ")])
        return None
    def __1l111l11l1l_opy_(self, instance: bstack1ll1l1lll1l_opy_, *args):
        result = self.__1l1111l111l_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l1111_opy_ = None
        if result.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᐊ"), None) == bstack11ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᐋ") and len(args) > 1 and getattr(args[1], bstack11ll1l1_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᐌ"), None) is not None:
            failure = [{bstack11ll1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᐍ"): [args[1].excinfo.exconly(), result.get(bstack11ll1l1_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᐎ"), None)]}]
            bstack11111l1111_opy_ = bstack11ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᐏ") if bstack11ll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᐐ") in getattr(args[1].excinfo, bstack11ll1l1_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᐑ"), bstack11ll1l1_opy_ (u"ࠢࠣᐒ")) else bstack11ll1l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᐓ")
        bstack1l111ll1lll_opy_ = result.get(bstack11ll1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᐔ"), TestFramework.bstack1l111l1l11l_opy_)
        if bstack1l111ll1lll_opy_ != TestFramework.bstack1l111l1l11l_opy_:
            TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111l1l1l_opy_(instance, {
            TestFramework.bstack1l1l111l1ll_opy_: failure,
            TestFramework.bstack1l11111l11l_opy_: bstack11111l1111_opy_,
            TestFramework.bstack1l1l111ll1l_opy_: bstack1l111ll1lll_opy_,
        })
    def __1l1111ll111_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1ll111l_opy_.SETUP_FIXTURE:
            instance = self.__11llllllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll11ll_opy_ bstack1l1111lllll_opy_ this to be bstack11ll1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᐕ")
            if test_framework_state == bstack1lll1ll111l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111ll11l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll1l1_opy_ (u"ࠦࡳࡵࡤࡦࠤᐖ"), None), bstack11ll1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᐗ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll1l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᐘ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᐙ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11111_opy_(target) if target else None
        return instance
    def __1l11111111l_opy_(
        self,
        instance: bstack1ll1l1lll1l_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111lll1ll_opy_ = TestFramework.bstack11111111ll_opy_(instance, PytestBDDFramework.bstack1l111111111_opy_, {})
        if not key in bstack1l111lll1ll_opy_:
            bstack1l111lll1ll_opy_[key] = []
        bstack1l11l111l1l_opy_ = TestFramework.bstack11111111ll_opy_(instance, PytestBDDFramework.bstack11lllllll11_opy_, {})
        if not key in bstack1l11l111l1l_opy_:
            bstack1l11l111l1l_opy_[key] = []
        bstack1l111ll1l1l_opy_ = {
            PytestBDDFramework.bstack1l111111111_opy_: bstack1l111lll1ll_opy_,
            PytestBDDFramework.bstack11lllllll11_opy_: bstack1l11l111l1l_opy_,
        }
        if test_hook_state == bstack1lll1111l1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11ll1l1_opy_ (u"ࠣ࡭ࡨࡽࠧᐚ"): key,
                TestFramework.bstack1l111ll111l_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111llll1_opy_: TestFramework.bstack1l111l11111_opy_,
                TestFramework.bstack1l111l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l111lll_opy_: [],
                TestFramework.bstack1l111ll1111_opy_: hook_name,
                TestFramework.bstack1l11111llll_opy_: bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()
            }
            bstack1l111lll1ll_opy_[key].append(hook)
            bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l1111111ll_opy_] = key
        elif test_hook_state == bstack1lll1111l1l_opy_.POST:
            bstack1l11l11ll11_opy_ = bstack1l111lll1ll_opy_.get(key, [])
            hook = bstack1l11l11ll11_opy_.pop() if bstack1l11l11ll11_opy_ else None
            if hook:
                result = self.__1l1111l111l_opy_(*args)
                if result:
                    bstack1l111111l11_opy_ = result.get(bstack11ll1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᐛ"), TestFramework.bstack1l111l11111_opy_)
                    if bstack1l111111l11_opy_ != TestFramework.bstack1l111l11111_opy_:
                        hook[TestFramework.bstack1l1111llll1_opy_] = bstack1l111111l11_opy_
                hook[TestFramework.bstack1l1111lll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11111llll_opy_] = bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()
                self.bstack1l11l11l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111lll11l_opy_, [])
                self.bstack1l1ll11l11l_opy_(instance, logs)
                bstack1l11l111l1l_opy_[key].append(hook)
                bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l11111ll11_opy_] = key
        TestFramework.bstack1l1111l1l1l_opy_(instance, bstack1l111ll1l1l_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᐜ") + str(bstack1l11l111l1l_opy_) + bstack11ll1l1_opy_ (u"ࠦࠧᐝ"))
    def __11llllllll1_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1l1l1l_opy_(args[0], [bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᐞ"), bstack11ll1l1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᐟ"), bstack11ll1l1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᐠ"), bstack11ll1l1_opy_ (u"ࠣ࡫ࡧࡷࠧᐡ"), bstack11ll1l1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᐢ"), bstack11ll1l1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᐣ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᐤ")) else fixturedef.get(bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᐥ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll1l1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᐦ")) else None
        node = request.node if hasattr(request, bstack11ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᐧ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᐨ")) else None
        baseid = fixturedef.get(bstack11ll1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᐩ"), None) or bstack11ll1l1_opy_ (u"ࠥࠦᐪ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll1l1_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᐫ")):
            target = PytestBDDFramework.__1l11111l111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll1l1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᐬ")) else None
            if target and not TestFramework.bstack1lllll11111_opy_(target):
                self.__1l111ll11l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐭ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠢࠣᐮ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᐯ") + str(target) + bstack11ll1l1_opy_ (u"ࠤࠥᐰ"))
            return None
        instance = TestFramework.bstack1lllll11111_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᐱ") + str(target) + bstack11ll1l1_opy_ (u"ࠦࠧᐲ"))
            return None
        bstack1l111ll1ll1_opy_ = TestFramework.bstack11111111ll_opy_(instance, PytestBDDFramework.bstack1l111lllll1_opy_, {})
        if os.getenv(bstack11ll1l1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᐳ"), bstack11ll1l1_opy_ (u"ࠨ࠱ࠣᐴ")) == bstack11ll1l1_opy_ (u"ࠢ࠲ࠤᐵ"):
            bstack1l1111ll1l1_opy_ = bstack11ll1l1_opy_ (u"ࠣ࠼ࠥᐶ").join((scope, fixturename))
            bstack1l11l11111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l111ll_opy_ = {
                bstack11ll1l1_opy_ (u"ࠤ࡮ࡩࡾࠨᐷ"): bstack1l1111ll1l1_opy_,
                bstack11ll1l1_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᐸ"): PytestBDDFramework.__1l111l1l1ll_opy_(request.node, scenario),
                bstack11ll1l1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᐹ"): fixturedef,
                bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᐺ"): scope,
                bstack11ll1l1_opy_ (u"ࠨࡴࡺࡲࡨࠦᐻ"): None,
            }
            try:
                if test_hook_state == bstack1lll1111l1l_opy_.POST and callable(getattr(args[-1], bstack11ll1l1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᐼ"), None)):
                    bstack1l111l111ll_opy_[bstack11ll1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨᐽ")] = TestFramework.bstack1l1ll1ll1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1111l1l_opy_.PRE:
                bstack1l111l111ll_opy_[bstack11ll1l1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᐾ")] = uuid4().__str__()
                bstack1l111l111ll_opy_[PytestBDDFramework.bstack1l111l1ll11_opy_] = bstack1l11l11111l_opy_
            elif test_hook_state == bstack1lll1111l1l_opy_.POST:
                bstack1l111l111ll_opy_[PytestBDDFramework.bstack1l1111lll11_opy_] = bstack1l11l11111l_opy_
            if bstack1l1111ll1l1_opy_ in bstack1l111ll1ll1_opy_:
                bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_].update(bstack1l111l111ll_opy_)
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᐿ") + str(bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_]) + bstack11ll1l1_opy_ (u"ࠦࠧᑀ"))
            else:
                bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_] = bstack1l111l111ll_opy_
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᑁ") + str(len(bstack1l111ll1ll1_opy_)) + bstack11ll1l1_opy_ (u"ࠨࠢᑂ"))
        TestFramework.bstack1lllll1ll1l_opy_(instance, PytestBDDFramework.bstack1l111lllll1_opy_, bstack1l111ll1ll1_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᑃ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠣࠤᑄ"))
        return instance
    def __1l111ll11l1_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll11l11_opy_.create_context(target)
        ob = bstack1ll1l1lll1l_opy_(ctx, self.bstack1ll11l1l1ll_opy_, self.bstack1l1111l11l1_opy_, test_framework_state)
        TestFramework.bstack1l1111l1l1l_opy_(ob, {
            TestFramework.bstack1ll11lll111_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1111l1_opy_: context.test_framework_version,
            TestFramework.bstack11lllllll1l_opy_: [],
            PytestBDDFramework.bstack1l111lllll1_opy_: {},
            PytestBDDFramework.bstack11lllllll11_opy_: {},
            PytestBDDFramework.bstack1l111111111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllll1ll1l_opy_(ob, TestFramework.bstack11lllllllll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllll1ll1l_opy_(ob, TestFramework.bstack1ll111ll11l_opy_, context.platform_index)
        TestFramework.bstack1llllll11l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᑅ") + str(TestFramework.bstack1llllll11l1_opy_.keys()) + bstack11ll1l1_opy_ (u"ࠥࠦᑆ"))
        return ob
    @staticmethod
    def __1l111lll1l1_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll1l1_opy_ (u"ࠫ࡮ࡪࠧᑇ"): id(step),
                bstack11ll1l1_opy_ (u"ࠬࡺࡥࡹࡶࠪᑈ"): step.name,
                bstack11ll1l1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᑉ"): step.keyword,
            })
        meta = {
            bstack11ll1l1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᑊ"): {
                bstack11ll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑋ"): feature.name,
                bstack11ll1l1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᑌ"): feature.filename,
                bstack11ll1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᑍ"): feature.description
            },
            bstack11ll1l1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᑎ"): {
                bstack11ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑏ"): scenario.name
            },
            bstack11ll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑐ"): steps,
            bstack11ll1l1_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᑑ"): PytestBDDFramework.__1l11l11l11l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l1111l_opy_: meta
            }
        )
    def bstack1l11l11l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᑒ")
        global _1l1ll11l1l1_opy_
        platform_index = os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᑓ")]
        bstack1l1lll1l11l_opy_ = os.path.join(bstack1l1l1llll11_opy_, (bstack1l1l1ll1ll1_opy_ + str(platform_index)), bstack1l11l111ll1_opy_)
        if not os.path.exists(bstack1l1lll1l11l_opy_) or not os.path.isdir(bstack1l1lll1l11l_opy_):
            return
        logs = hook.get(bstack11ll1l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᑔ"), [])
        with os.scandir(bstack1l1lll1l11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll11l1l1_opy_:
                    self.logger.info(bstack11ll1l1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᑕ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll1l1_opy_ (u"ࠧࠨᑖ")
                    log_entry = bstack1lll111ll1l_opy_(
                        kind=bstack11ll1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᑗ"),
                        message=bstack11ll1l1_opy_ (u"ࠢࠣᑘ"),
                        level=bstack11ll1l1_opy_ (u"ࠣࠤᑙ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll1llll_opy_=entry.stat().st_size,
                        bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᑚ"),
                        bstack11111ll_opy_=os.path.abspath(entry.path),
                        bstack1l111l1llll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll11l1l1_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᑛ")]
        bstack1l11l11l1ll_opy_ = os.path.join(bstack1l1l1llll11_opy_, (bstack1l1l1ll1ll1_opy_ + str(platform_index)), bstack1l11l111ll1_opy_, bstack1l1111l1l11_opy_)
        if not os.path.exists(bstack1l11l11l1ll_opy_) or not os.path.isdir(bstack1l11l11l1ll_opy_):
            self.logger.info(bstack11ll1l1_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᑜ").format(bstack1l11l11l1ll_opy_))
        else:
            self.logger.info(bstack11ll1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᑝ").format(bstack1l11l11l1ll_opy_))
            with os.scandir(bstack1l11l11l1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll11l1l1_opy_:
                        self.logger.info(bstack11ll1l1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᑞ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll1l1_opy_ (u"ࠢࠣᑟ")
                        log_entry = bstack1lll111ll1l_opy_(
                            kind=bstack11ll1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᑠ"),
                            message=bstack11ll1l1_opy_ (u"ࠤࠥᑡ"),
                            level=bstack11ll1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᑢ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll1llll_opy_=entry.stat().st_size,
                            bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᑣ"),
                            bstack11111ll_opy_=os.path.abspath(entry.path),
                            bstack1l1llll111l_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll11l1l1_opy_.add(abs_path)
        hook[bstack11ll1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᑤ")] = logs
    def bstack1l1ll11l11l_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1ll1l1lll1l_opy_,
        entries: List[bstack1lll111ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᑥ"))
        req.platform_index = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll111ll11l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11lll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = entry.bstack1l111l1llll_opy_
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᑦ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll1l1_opy_ (u"ࠣࠤᑧ")
            if entry.kind == bstack11ll1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᑨ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1llll_opy_
                log_entry.file_path = entry.bstack11111ll_opy_
        def bstack1l1ll1l1l11_opy_():
            bstack11ll11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1ll1l_opy_.LogCreatedEvent(req)
                bstack1l1lll1l1l1_opy_.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᑩ"), datetime.now() - bstack11ll11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᑪ").format(str(e)))
                traceback.print_exc()
        self.bstack111111lll1_opy_.enqueue(bstack1l1ll1l1l11_opy_)
    def __1l11l1111ll_opy_(self, instance) -> None:
        bstack11ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᑫ")
        bstack1l111ll1l1l_opy_ = {bstack11ll1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᑬ"): bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()}
        TestFramework.bstack1l1111l1l1l_opy_(instance, bstack1l111ll1l1l_opy_)
    @staticmethod
    def __1l11111l1ll_opy_(instance, args):
        request, bstack1l11l11ll1l_opy_ = args
        bstack1l11111ll1l_opy_ = id(bstack1l11l11ll1l_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack1l111l1111l_opy_]
        step = next(filter(lambda st: st[bstack11ll1l1_opy_ (u"ࠧࡪࡦࠪᑭ")] == bstack1l11111ll1l_opy_, bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑮ")]), None)
        step.update({
            bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᑯ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑰ")]) if st[bstack11ll1l1_opy_ (u"ࠫ࡮ࡪࠧᑱ")] == step[bstack11ll1l1_opy_ (u"ࠬ࡯ࡤࠨᑲ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑳ")][index] = step
        instance.data[TestFramework.bstack1l111l1111l_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l1111l1ll1_opy_(instance, args):
        bstack11ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᑴ")
        bstack1l111llll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l11ll1l_opy_ = args[1]
        bstack1l11111ll1l_opy_ = id(bstack1l11l11ll1l_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack1l111l1111l_opy_]
        step = None
        if bstack1l11111ll1l_opy_ is not None and bstack1l1111l1lll_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑵ")):
            step = next(filter(lambda st: st[bstack11ll1l1_opy_ (u"ࠩ࡬ࡨࠬᑶ")] == bstack1l11111ll1l_opy_, bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑷ")]), None)
            step.update({
                bstack11ll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᑸ"): bstack1l111llll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᑹ"): bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑺ"),
                bstack11ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᑻ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᑼ"): bstack11ll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᑽ"),
                })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑾ")]) if st[bstack11ll1l1_opy_ (u"ࠫ࡮ࡪࠧᑿ")] == step[bstack11ll1l1_opy_ (u"ࠬ࡯ࡤࠨᒀ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack11ll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒁ")][index] = step
        instance.data[TestFramework.bstack1l111l1111l_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l11l11l11l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11ll1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᒂ")):
                examples = list(node.callspec.params[bstack11ll1l1_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᒃ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1l111l_opy_(self, instance: bstack1ll1l1lll1l_opy_, bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_]):
        bstack1l111l1l1l1_opy_ = (
            PytestBDDFramework.bstack1l1111111ll_opy_
            if bstack1llllllllll_opy_[1] == bstack1lll1111l1l_opy_.PRE
            else PytestBDDFramework.bstack1l11111ll11_opy_
        )
        hook = PytestBDDFramework.bstack1l11l1111l1_opy_(instance, bstack1l111l1l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []))
        return entries
    def bstack1l1ll11l111_opy_(self, instance: bstack1ll1l1lll1l_opy_, bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_]):
        bstack1l111l1l1l1_opy_ = (
            PytestBDDFramework.bstack1l1111111ll_opy_
            if bstack1llllllllll_opy_[1] == bstack1lll1111l1l_opy_.PRE
            else PytestBDDFramework.bstack1l11111ll11_opy_
        )
        PytestBDDFramework.bstack1l111llllll_opy_(instance, bstack1l111l1l1l1_opy_)
        TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []).clear()
    @staticmethod
    def bstack1l11l1111l1_opy_(instance: bstack1ll1l1lll1l_opy_, bstack1l111l1l1l1_opy_: str):
        bstack1l111l1ll1l_opy_ = (
            PytestBDDFramework.bstack11lllllll11_opy_
            if bstack1l111l1l1l1_opy_ == PytestBDDFramework.bstack1l11111ll11_opy_
            else PytestBDDFramework.bstack1l111111111_opy_
        )
        bstack1l1111ll1ll_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1l1l1_opy_, None)
        bstack1l111llll11_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1ll1l_opy_, None) if bstack1l1111ll1ll_opy_ else None
        return (
            bstack1l111llll11_opy_[bstack1l1111ll1ll_opy_][-1]
            if isinstance(bstack1l111llll11_opy_, dict) and len(bstack1l111llll11_opy_.get(bstack1l1111ll1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111llllll_opy_(instance: bstack1ll1l1lll1l_opy_, bstack1l111l1l1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l11l1111l1_opy_(instance, bstack1l111l1l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l111lll_opy_, []).clear()
    @staticmethod
    def __1l111111lll_opy_(instance: bstack1ll1l1lll1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᒄ"), None)):
            return
        if os.getenv(bstack11ll1l1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᒅ"), bstack11ll1l1_opy_ (u"ࠦ࠶ࠨᒆ")) != bstack11ll1l1_opy_ (u"ࠧ࠷ࠢᒇ"):
            PytestBDDFramework.logger.warning(bstack11ll1l1_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᒈ"))
            return
        bstack1l1111l1111_opy_ = {
            bstack11ll1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᒉ"): (PytestBDDFramework.bstack1l1111111ll_opy_, PytestBDDFramework.bstack1l111111111_opy_),
            bstack11ll1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᒊ"): (PytestBDDFramework.bstack1l11111ll11_opy_, PytestBDDFramework.bstack11lllllll11_opy_),
        }
        for when in (bstack11ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᒋ"), bstack11ll1l1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᒌ"), bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᒍ")):
            bstack1l111ll1l11_opy_ = args[1].get_records(when)
            if not bstack1l111ll1l11_opy_:
                continue
            records = [
                bstack1lll111ll1l_opy_(
                    kind=TestFramework.bstack1l1ll11ll1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll1l1_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᒎ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll1l1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᒏ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1l11_opy_
                if isinstance(getattr(r, bstack11ll1l1_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᒐ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l111111_opy_, bstack1l111l1ll1l_opy_ = bstack1l1111l1111_opy_.get(when, (None, None))
            bstack1l111l11ll1_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l11l111111_opy_, None) if bstack1l11l111111_opy_ else None
            bstack1l111llll11_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1ll1l_opy_, None) if bstack1l111l11ll1_opy_ else None
            if isinstance(bstack1l111llll11_opy_, dict) and len(bstack1l111llll11_opy_.get(bstack1l111l11ll1_opy_, [])) > 0:
                hook = bstack1l111llll11_opy_[bstack1l111l11ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l111lll_opy_ in hook:
                    hook[TestFramework.bstack1l11l111lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111111ll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1111ll1ll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11111lll1_opy_(request.node, scenario)
        bstack1l11l11l111_opy_ = feature.filename
        if not bstack1111ll1ll_opy_ or not test_name or not bstack1l11l11l111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11l11l11_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l11lll_opy_: bstack1111ll1ll_opy_,
            TestFramework.bstack1ll11ll11l1_opy_: test_name,
            TestFramework.bstack1l1l1l1l111_opy_: bstack1111ll1ll_opy_,
            TestFramework.bstack1l1111ll11l_opy_: bstack1l11l11l111_opy_,
            TestFramework.bstack1l1111l11ll_opy_: PytestBDDFramework.__1l111l1l1ll_opy_(feature, scenario),
            TestFramework.bstack1l1111111l1_opy_: code,
            TestFramework.bstack1l1l111ll1l_opy_: TestFramework.bstack1l111l1l11l_opy_,
            TestFramework.bstack1l11l1ll1l1_opy_: test_name
        }
    @staticmethod
    def __1l11111lll1_opy_(node, scenario):
        if hasattr(node, bstack11ll1l1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᒑ")):
            parts = node.nodeid.rsplit(bstack11ll1l1_opy_ (u"ࠤ࡞ࠦᒒ"))
            params = parts[-1]
            return bstack11ll1l1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᒓ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111l1l1ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᒔ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11ll1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪᒕ")) else [])
    @staticmethod
    def __1l11111l111_opy_(location):
        return bstack11ll1l1_opy_ (u"ࠨ࠺࠻ࠤᒖ").join(filter(lambda x: isinstance(x, str), location))