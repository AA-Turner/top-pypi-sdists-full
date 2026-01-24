# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1ll11_opy_ import bstack11llll11lll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll111ll_opy_,
    bstack1ll111l1lll_opy_,
    bstack1ll1l111111_opy_,
    bstack11lllll1l11_opy_,
    bstack1ll11l1l11l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1l1111l11_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1lllll11_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1lll1lllll1_opy_
bstack1l11ll111ll_opy_ = bstack1l1l1111l11_opy_()
bstack1l1l11l11l1_opy_ = bstack1l1111_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᔬ")
bstack11lll1l11l1_opy_ = bstack1l1111_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᔭ")
bstack11lll1111l1_opy_ = bstack1l1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᔮ")
bstack11llll1ll1l_opy_ = 1.0
_1l11lll1ll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11llll11l1l_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᔯ")
    bstack11ll1ll1111_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᔰ")
    bstack11ll1ll1lll_opy_ = bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᔱ")
    bstack11ll1l11l1l_opy_ = bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᔲ")
    bstack11ll1ll111l_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᔳ")
    bstack11ll1l11ll1_opy_: bool
    bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_  = None
    bstack11lll1ll1ll_opy_ = [
        bstack1ll1ll111ll_opy_.BEFORE_ALL,
        bstack1ll1ll111ll_opy_.AFTER_ALL,
        bstack1ll1ll111ll_opy_.BEFORE_EACH,
        bstack1ll1ll111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l1l11l_opy_: Dict[str, str],
        bstack1l1ll1l1l1l_opy_: List[str]=[bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᔴ")],
        bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_ = None,
        bstack1ll1111l1ll_opy_=None
    ):
        super().__init__(bstack1l1ll1l1l1l_opy_, bstack11ll1l1l11l_opy_, bstack1lll1llll1l_opy_)
        self.bstack11ll1l11ll1_opy_ = any(bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᔵ") in item.lower() for item in bstack1l1ll1l1l1l_opy_)
        self.bstack1ll1111l1ll_opy_ = bstack1ll1111l1ll_opy_
    def track_event(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll111ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11lll1ll1ll_opy_:
            bstack11llll11lll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll111ll_opy_.NONE:
            self.logger.warning(bstack1l1111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᔶ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠨࠢᔷ"))
            return
        if not self.bstack11ll1l11ll1_opy_:
            self.logger.warning(bstack1l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᔸ") + str(str(self.bstack1l1ll1l1l1l_opy_)) + bstack1l1111_opy_ (u"ࠣࠤᔹ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᔺ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᔻ"))
            return
        instance = self.__11ll1l1lll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᔼ") + str(args) + bstack1l1111_opy_ (u"ࠧࠨᔽ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lll1ll1ll_opy_ and test_hook_state == bstack1ll1l111111_opy_.PRE:
                bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll11l111_opy_.value)
                name = str(EVENTS.bstack11ll11l111_opy_.name)+bstack1l1111_opy_ (u"ࠨ࠺ࠣᔾ")+str(test_framework_state.name)
                TestFramework.bstack11lll1ll111_opy_(instance, name, bstack1ll1111lll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᔿ").format(e))
        try:
            if test_framework_state == bstack1ll1ll111ll_opy_.TEST:
                if not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll111l_opy_) and test_hook_state == bstack1ll1l111111_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll1lll1l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1111_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᕀ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠤࠥᕁ"))
                if test_hook_state == bstack1ll1l111111_opy_.PRE and not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l11lll1l11_opy_):
                    TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l11lll1l11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11lllll1111_opy_(instance, args)
                    self.logger.debug(bstack1l1111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᕂ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠦࠧᕃ"))
                elif test_hook_state == bstack1ll1l111111_opy_.POST and not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l11_opy_):
                    TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l1l11l1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᕄ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠨࠢᕅ"))
            elif test_framework_state == bstack1ll1ll111ll_opy_.STEP:
                if test_hook_state == bstack1ll1l111111_opy_.PRE:
                    PytestBDDFramework.__11lll111lll_opy_(instance, args)
                elif test_hook_state == bstack1ll1l111111_opy_.POST:
                    PytestBDDFramework.__11lll1l11ll_opy_(instance, args)
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG and test_hook_state == bstack1ll1l111111_opy_.POST:
                PytestBDDFramework.__11llll1ll11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG_REPORT and test_hook_state == bstack1ll1l111111_opy_.POST:
                self.__11llll1l111_opy_(instance, *args)
                self.__11ll1lll1ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11lll1ll1ll_opy_:
                self.__11lll111l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᕆ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠣࠤᕇ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lllll11ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lll1ll1ll_opy_ and test_hook_state == bstack1ll1l111111_opy_.POST:
                name = str(EVENTS.bstack11ll11l111_opy_.name)+bstack1l1111_opy_ (u"ࠤ࠽ࠦᕈ")+str(test_framework_state.name)
                bstack1ll1111lll_opy_ = TestFramework.bstack11ll1llllll_opy_(instance, name)
                bstack11ll111lll_opy_.end(EVENTS.bstack11ll11l111_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᕉ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᕊ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᕋ").format(e))
    def bstack1l11lll11ll_opy_(self):
        return self.bstack11ll1l11ll1_opy_
    def __11lll11llll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᕌ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1111111_opy_(rep, [bstack1l1111_opy_ (u"ࠢࡸࡪࡨࡲࠧᕍ"), bstack1l1111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᕎ"), bstack1l1111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᕏ"), bstack1l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᕐ"), bstack1l1111_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᕑ"), bstack1l1111_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᕒ")])
        return None
    def __11llll1l111_opy_(self, instance: bstack1ll111l1lll_opy_, *args):
        result = self.__11lll11llll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll1111l1_opy_ = None
        if result.get(bstack1l1111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᕓ"), None) == bstack1l1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᕔ") and len(args) > 1 and getattr(args[1], bstack1l1111_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᕕ"), None) is not None:
            failure = [{bstack1l1111_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᕖ"): [args[1].excinfo.exconly(), result.get(bstack1l1111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᕗ"), None)]}]
            bstack1llll1111l1_opy_ = bstack1l1111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᕘ") if bstack1l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᕙ") in getattr(args[1].excinfo, bstack1l1111_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᕚ"), bstack1l1111_opy_ (u"ࠢࠣᕛ")) else bstack1l1111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᕜ")
        bstack11lll11l11l_opy_ = result.get(bstack1l1111_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᕝ"), TestFramework.bstack11lll1l111l_opy_)
        if bstack11lll11l11l_opy_ != TestFramework.bstack11lll1l111l_opy_:
            TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l1l1111lll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11llll1llll_opy_(instance, {
            TestFramework.bstack1l111l1ll11_opy_: failure,
            TestFramework.bstack11lll11lll1_opy_: bstack1llll1111l1_opy_,
            TestFramework.bstack1l111l1l1l1_opy_: bstack11lll11l11l_opy_,
        })
    def __11ll1l1lll1_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll111ll_opy_.SETUP_FIXTURE:
            instance = self.__11llll11l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lll1l1111_opy_ bstack11ll1l1l1ll_opy_ this to be bstack1l1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᕞ")
            if test_framework_state == bstack1ll1ll111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lll1l1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1111_opy_ (u"ࠦࡳࡵࡤࡦࠤᕟ"), None), bstack1l1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᕠ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᕡ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᕢ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11l1lll_opy_(target) if target else None
        return instance
    def __11lll111l11_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11llll1lll1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, PytestBDDFramework.bstack11ll1ll1111_opy_, {})
        if not key in bstack11llll1lll1_opy_:
            bstack11llll1lll1_opy_[key] = []
        bstack11lll11l1ll_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, PytestBDDFramework.bstack11ll1ll1lll_opy_, {})
        if not key in bstack11lll11l1ll_opy_:
            bstack11lll11l1ll_opy_[key] = []
        bstack11ll1l1llll_opy_ = {
            PytestBDDFramework.bstack11ll1ll1111_opy_: bstack11llll1lll1_opy_,
            PytestBDDFramework.bstack11ll1ll1lll_opy_: bstack11lll11l1ll_opy_,
        }
        if test_hook_state == bstack1ll1l111111_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1111_opy_ (u"ࠣ࡭ࡨࡽࠧᕣ"): key,
                TestFramework.bstack11lll1l1lll_opy_: uuid4().__str__(),
                TestFramework.bstack11llll11111_opy_: TestFramework.bstack11lll11l111_opy_,
                TestFramework.bstack11lllll1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11lll1ll11l_opy_: [],
                TestFramework.bstack11lll111l1l_opy_: hook_name,
                TestFramework.bstack11llll111l1_opy_: bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()
            }
            bstack11llll1lll1_opy_[key].append(hook)
            bstack11ll1l1llll_opy_[PytestBDDFramework.bstack11ll1l11l1l_opy_] = key
        elif test_hook_state == bstack1ll1l111111_opy_.POST:
            bstack11ll1ll11l1_opy_ = bstack11llll1lll1_opy_.get(key, [])
            hook = bstack11ll1ll11l1_opy_.pop() if bstack11ll1ll11l1_opy_ else None
            if hook:
                result = self.__11lll11llll_opy_(*args)
                if result:
                    bstack11lll11ll1l_opy_ = result.get(bstack1l1111_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᕤ"), TestFramework.bstack11lll11l111_opy_)
                    if bstack11lll11ll1l_opy_ != TestFramework.bstack11lll11l111_opy_:
                        hook[TestFramework.bstack11llll11111_opy_] = bstack11lll11ll1l_opy_
                hook[TestFramework.bstack11ll1ll1ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11llll111l1_opy_] = bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()
                self.bstack11ll1l1l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack11lll11ll11_opy_, [])
                self.bstack1l1l111l1ll_opy_(instance, logs)
                bstack11lll11l1ll_opy_[key].append(hook)
                bstack11ll1l1llll_opy_[PytestBDDFramework.bstack11ll1ll111l_opy_] = key
        TestFramework.bstack11llll1llll_opy_(instance, bstack11ll1l1llll_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᕥ") + str(bstack11lll11l1ll_opy_) + bstack1l1111_opy_ (u"ࠦࠧᕦ"))
    def __11llll11l11_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1111111_opy_(args[0], [bstack1l1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᕧ"), bstack1l1111_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᕨ"), bstack1l1111_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᕩ"), bstack1l1111_opy_ (u"ࠣ࡫ࡧࡷࠧᕪ"), bstack1l1111_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᕫ"), bstack1l1111_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᕬ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᕭ")) else fixturedef.get(bstack1l1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᕮ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1111_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᕯ")) else None
        node = request.node if hasattr(request, bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᕰ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᕱ")) else None
        baseid = fixturedef.get(bstack1l1111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᕲ"), None) or bstack1l1111_opy_ (u"ࠥࠦᕳ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1111_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᕴ")):
            target = PytestBDDFramework.__11lll1ll1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1111_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᕵ")) else None
            if target and not TestFramework.bstack1lll11l1lll_opy_(target):
                self.__11lll1l1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᕶ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠢࠣᕷ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᕸ") + str(target) + bstack1l1111_opy_ (u"ࠤࠥᕹ"))
            return None
        instance = TestFramework.bstack1lll11l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᕺ") + str(target) + bstack1l1111_opy_ (u"ࠦࠧᕻ"))
            return None
        bstack11ll1ll1l1l_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, PytestBDDFramework.bstack11llll11l1l_opy_, {})
        if os.getenv(bstack1l1111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᕼ"), bstack1l1111_opy_ (u"ࠨ࠱ࠣᕽ")) == bstack1l1111_opy_ (u"ࠢ࠲ࠤᕾ"):
            bstack11lll1lll11_opy_ = bstack1l1111_opy_ (u"ࠣ࠼ࠥᕿ").join((scope, fixturename))
            bstack11ll1lll111_opy_ = datetime.now(tz=timezone.utc)
            bstack11lllll11l1_opy_ = {
                bstack1l1111_opy_ (u"ࠤ࡮ࡩࡾࠨᖀ"): bstack11lll1lll11_opy_,
                bstack1l1111_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᖁ"): PytestBDDFramework.__11lll1llll1_opy_(request.node, scenario),
                bstack1l1111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᖂ"): fixturedef,
                bstack1l1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᖃ"): scope,
                bstack1l1111_opy_ (u"ࠨࡴࡺࡲࡨࠦᖄ"): None,
            }
            try:
                if test_hook_state == bstack1ll1l111111_opy_.POST and callable(getattr(args[-1], bstack1l1111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᖅ"), None)):
                    bstack11lllll11l1_opy_[bstack1l1111_opy_ (u"ࠣࡶࡼࡴࡪࠨᖆ")] = TestFramework.bstack1l1l11l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1l111111_opy_.PRE:
                bstack11lllll11l1_opy_[bstack1l1111_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᖇ")] = uuid4().__str__()
                bstack11lllll11l1_opy_[PytestBDDFramework.bstack11lllll1l1l_opy_] = bstack11ll1lll111_opy_
            elif test_hook_state == bstack1ll1l111111_opy_.POST:
                bstack11lllll11l1_opy_[PytestBDDFramework.bstack11ll1ll1ll1_opy_] = bstack11ll1lll111_opy_
            if bstack11lll1lll11_opy_ in bstack11ll1ll1l1l_opy_:
                bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_].update(bstack11lllll11l1_opy_)
                self.logger.debug(bstack1l1111_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᖈ") + str(bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_]) + bstack1l1111_opy_ (u"ࠦࠧᖉ"))
            else:
                bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_] = bstack11lllll11l1_opy_
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᖊ") + str(len(bstack11ll1ll1l1l_opy_)) + bstack1l1111_opy_ (u"ࠨࠢᖋ"))
        TestFramework.bstack1lll11l1ll1_opy_(instance, PytestBDDFramework.bstack11llll11l1l_opy_, bstack11ll1ll1l1l_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᖌ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠣࠤᖍ"))
        return instance
    def __11lll1l1l1l_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lll1l1llll_opy_.create_context(target)
        ob = bstack1ll111l1lll_opy_(ctx, self.bstack1l1ll1l1l1l_opy_, self.bstack11ll1l1l11l_opy_, test_framework_state)
        TestFramework.bstack11llll1llll_opy_(ob, {
            TestFramework.bstack1l1lll1ll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1l1111l_opy_: context.test_framework_version,
            TestFramework.bstack11lll111ll1_opy_: [],
            PytestBDDFramework.bstack11llll11l1l_opy_: {},
            PytestBDDFramework.bstack11ll1ll1lll_opy_: {},
            PytestBDDFramework.bstack11ll1ll1111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll11l1ll1_opy_(ob, TestFramework.bstack11lll1l1l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll11l1ll1_opy_(ob, TestFramework.bstack1l1ll1l11ll_opy_, context.platform_index)
        TestFramework.bstack1lll11ll1ll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1111_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᖎ") + str(TestFramework.bstack1lll11ll1ll_opy_.keys()) + bstack1l1111_opy_ (u"ࠥࠦᖏ"))
        return ob
    @staticmethod
    def __11lllll1111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧᖐ"): id(step),
                bstack1l1111_opy_ (u"ࠬࡺࡥࡹࡶࠪᖑ"): step.name,
                bstack1l1111_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᖒ"): step.keyword,
            })
        meta = {
            bstack1l1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᖓ"): {
                bstack1l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᖔ"): feature.name,
                bstack1l1111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᖕ"): feature.filename,
                bstack1l1111_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᖖ"): feature.description
            },
            bstack1l1111_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᖗ"): {
                bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᖘ"): scenario.name
            },
            bstack1l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᖙ"): steps,
            bstack1l1111_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᖚ"): PytestBDDFramework.__11ll1ll11ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11llll1111l_opy_: meta
            }
        )
    def bstack11ll1l1l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᖛ")
        global _1l11lll1ll1_opy_
        platform_index = os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᖜ")]
        bstack1l11ll1ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l1l11l11l1_opy_ + str(platform_index)), bstack11lll1l11l1_opy_)
        if not os.path.exists(bstack1l11ll1ll1l_opy_) or not os.path.isdir(bstack1l11ll1ll1l_opy_):
            return
        logs = hook.get(bstack1l1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᖝ"), [])
        with os.scandir(bstack1l11ll1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11lll1ll1_opy_:
                    self.logger.info(bstack1l1111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᖞ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1111_opy_ (u"ࠧࠨᖟ")
                    log_entry = bstack1ll11l1l11l_opy_(
                        kind=bstack1l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᖠ"),
                        message=bstack1l1111_opy_ (u"ࠢࠣᖡ"),
                        level=bstack1l1111_opy_ (u"ࠣࠤᖢ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l11l_opy_=entry.stat().st_size,
                        bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᖣ"),
                        bstack1llllll1_opy_=os.path.abspath(entry.path),
                        bstack11lll111111_opy_=hook.get(TestFramework.bstack11lll1l1lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11lll1ll1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᖤ")]
        bstack11llll11ll1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l1l11l11l1_opy_ + str(platform_index)), bstack11lll1l11l1_opy_, bstack11lll1111l1_opy_)
        if not os.path.exists(bstack11llll11ll1_opy_) or not os.path.isdir(bstack11llll11ll1_opy_):
            self.logger.info(bstack1l1111_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᖥ").format(bstack11llll11ll1_opy_))
        else:
            self.logger.info(bstack1l1111_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᖦ").format(bstack11llll11ll1_opy_))
            with os.scandir(bstack11llll11ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11lll1ll1_opy_:
                        self.logger.info(bstack1l1111_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᖧ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1111_opy_ (u"ࠢࠣᖨ")
                        log_entry = bstack1ll11l1l11l_opy_(
                            kind=bstack1l1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᖩ"),
                            message=bstack1l1111_opy_ (u"ࠤࠥᖪ"),
                            level=bstack1l1111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᖫ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l11l_opy_=entry.stat().st_size,
                            bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᖬ"),
                            bstack1llllll1_opy_=os.path.abspath(entry.path),
                            bstack1l1l11lllll_opy_=hook.get(TestFramework.bstack11lll1l1lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11lll1ll1_opy_.add(abs_path)
        hook[bstack1l1111_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᖭ")] = logs
    def bstack1l1l111l1ll_opy_(
        self,
        bstack1l11l1lll11_opy_: bstack1ll111l1lll_opy_,
        entries: List[bstack1ll11l1l11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᖮ"))
        req.platform_index = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
        req.client_worker_id = bstack1l1111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᖯ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11l1lll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11l1lll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11l1lll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1lll1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1l1l1111l_opy_)
            log_entry.uuid = entry.bstack11lll111111_opy_ if entry.bstack11lll111111_opy_ else TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1lll111ll_opy_)
            log_entry.test_framework_state = bstack1l11l1lll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᖰ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᖱ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l11l_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l11ll1111l_opy_():
            bstack1ll1lll11l_opy_ = datetime.now()
            try:
                self.bstack1ll1111l1ll_opy_.LogCreatedEvent(req)
                bstack1l11l1lll11_opy_.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᖲ"), datetime.now() - bstack1ll1lll11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᖳ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1llll1l_opy_.enqueue(bstack1l11ll1111l_opy_)
    def __11ll1lll1ll_opy_(self, instance) -> None:
        bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᖴ")
        bstack11ll1l1llll_opy_ = {bstack1l1111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᖵ"): bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()}
        TestFramework.bstack11llll1llll_opy_(instance, bstack11ll1l1llll_opy_)
    @staticmethod
    def __11lll111lll_opy_(instance, args):
        request, bstack11ll1llll1l_opy_ = args
        bstack11ll1l1ll1l_opy_ = id(bstack11ll1llll1l_opy_)
        bstack11ll1ll1l11_opy_ = instance.data[TestFramework.bstack11llll1111l_opy_]
        step = next(filter(lambda st: st[bstack1l1111_opy_ (u"ࠧࡪࡦࠪᖶ")] == bstack11ll1l1ll1l_opy_, bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᖷ")]), None)
        step.update({
            bstack1l1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖸ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᖹ")]) if st[bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧᖺ")] == step[bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨᖻ")]), None)
        if index is not None:
            bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᖼ")][index] = step
        instance.data[TestFramework.bstack11llll1111l_opy_] = bstack11ll1ll1l11_opy_
    @staticmethod
    def __11lll1l11ll_opy_(instance, args):
        bstack1l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᖽ")
        bstack11lll1111ll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1llll1l_opy_ = args[1]
        bstack11ll1l1ll1l_opy_ = id(bstack11ll1llll1l_opy_)
        bstack11ll1ll1l11_opy_ = instance.data[TestFramework.bstack11llll1111l_opy_]
        step = None
        if bstack11ll1l1ll1l_opy_ is not None and bstack11ll1ll1l11_opy_.get(bstack1l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᖾ")):
            step = next(filter(lambda st: st[bstack1l1111_opy_ (u"ࠩ࡬ࡨࠬᖿ")] == bstack11ll1l1ll1l_opy_, bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᗀ")]), None)
            step.update({
                bstack1l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗁ"): bstack11lll1111ll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᗂ"): bstack1l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗃ"),
                bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᗄ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᗅ"): bstack1l1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᗆ"),
                })
        index = next((i for i, st in enumerate(bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᗇ")]) if st[bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧᗈ")] == step[bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨᗉ")]), None)
        if index is not None:
            bstack11ll1ll1l11_opy_[bstack1l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᗊ")][index] = step
        instance.data[TestFramework.bstack11llll1111l_opy_] = bstack11ll1ll1l11_opy_
    @staticmethod
    def __11ll1ll11ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᗋ")):
                examples = list(node.callspec.params[bstack1l1111_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᗌ")].values())
            return examples
        except:
            return []
    def bstack1l11ll11lll_opy_(self, instance: bstack1ll111l1lll_opy_, bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_]):
        bstack11lll1lllll_opy_ = (
            PytestBDDFramework.bstack11ll1l11l1l_opy_
            if bstack1lll111llll_opy_[1] == bstack1ll1l111111_opy_.PRE
            else PytestBDDFramework.bstack11ll1ll111l_opy_
        )
        hook = PytestBDDFramework.bstack11lll11111l_opy_(instance, bstack11lll1lllll_opy_)
        entries = hook.get(TestFramework.bstack11lll1ll11l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, []))
        return entries
    def bstack1l11lllll11_opy_(self, instance: bstack1ll111l1lll_opy_, bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_]):
        bstack11lll1lllll_opy_ = (
            PytestBDDFramework.bstack11ll1l11l1l_opy_
            if bstack1lll111llll_opy_[1] == bstack1ll1l111111_opy_.PRE
            else PytestBDDFramework.bstack11ll1ll111l_opy_
        )
        PytestBDDFramework.bstack11lllll1ll1_opy_(instance, bstack11lll1lllll_opy_)
        TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, []).clear()
    @staticmethod
    def bstack11lll11111l_opy_(instance: bstack1ll111l1lll_opy_, bstack11lll1lllll_opy_: str):
        bstack11ll1l11lll_opy_ = (
            PytestBDDFramework.bstack11ll1ll1lll_opy_
            if bstack11lll1lllll_opy_ == PytestBDDFramework.bstack11ll1ll111l_opy_
            else PytestBDDFramework.bstack11ll1ll1111_opy_
        )
        bstack11llll111ll_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11lll1lllll_opy_, None)
        bstack11llll1l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l11lll_opy_, None) if bstack11llll111ll_opy_ else None
        return (
            bstack11llll1l1l1_opy_[bstack11llll111ll_opy_][-1]
            if isinstance(bstack11llll1l1l1_opy_, dict) and len(bstack11llll1l1l1_opy_.get(bstack11llll111ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lllll1ll1_opy_(instance: bstack1ll111l1lll_opy_, bstack11lll1lllll_opy_: str):
        hook = PytestBDDFramework.bstack11lll11111l_opy_(instance, bstack11lll1lllll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11lll1ll11l_opy_, []).clear()
    @staticmethod
    def __11llll1ll11_opy_(instance: bstack1ll111l1lll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1111_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᗍ"), None)):
            return
        if os.getenv(bstack1l1111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᗎ"), bstack1l1111_opy_ (u"ࠦ࠶ࠨᗏ")) != bstack1l1111_opy_ (u"ࠧ࠷ࠢᗐ"):
            PytestBDDFramework.logger.warning(bstack1l1111_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᗑ"))
            return
        bstack11ll1lll11l_opy_ = {
            bstack1l1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᗒ"): (PytestBDDFramework.bstack11ll1l11l1l_opy_, PytestBDDFramework.bstack11ll1ll1111_opy_),
            bstack1l1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᗓ"): (PytestBDDFramework.bstack11ll1ll111l_opy_, PytestBDDFramework.bstack11ll1ll1lll_opy_),
        }
        for when in (bstack1l1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᗔ"), bstack1l1111_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᗕ"), bstack1l1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᗖ")):
            bstack11llll1l1ll_opy_ = args[1].get_records(when)
            if not bstack11llll1l1ll_opy_:
                continue
            records = [
                bstack1ll11l1l11l_opy_(
                    kind=TestFramework.bstack1l1l11ll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᗗ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1111_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᗘ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll1l1ll_opy_
                if isinstance(getattr(r, bstack1l1111_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᗙ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1l1l111_opy_, bstack11ll1l11lll_opy_ = bstack11ll1lll11l_opy_.get(when, (None, None))
            bstack11lll1lll1l_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l1l111_opy_, None) if bstack11ll1l1l111_opy_ else None
            bstack11llll1l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l11lll_opy_, None) if bstack11lll1lll1l_opy_ else None
            if isinstance(bstack11llll1l1l1_opy_, dict) and len(bstack11llll1l1l1_opy_.get(bstack11lll1lll1l_opy_, [])) > 0:
                hook = bstack11llll1l1l1_opy_[bstack11lll1lll1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11lll1ll11l_opy_ in hook:
                    hook[TestFramework.bstack11lll1ll11l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1lll1l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l1llll1ll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11lll1l1ll1_opy_(request.node, scenario)
        bstack11ll1lllll1_opy_ = feature.filename
        if not bstack1l1llll1ll_opy_ or not test_name or not bstack11ll1lllll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1lll111ll_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll111l_opy_: bstack1l1llll1ll_opy_,
            TestFramework.bstack1l1ll11111l_opy_: test_name,
            TestFramework.bstack1l11l1l1111_opy_: bstack1l1llll1ll_opy_,
            TestFramework.bstack11llll1l11l_opy_: bstack11ll1lllll1_opy_,
            TestFramework.bstack11lll11l1l1_opy_: PytestBDDFramework.__11lll1llll1_opy_(feature, scenario),
            TestFramework.bstack11ll1l1ll11_opy_: code,
            TestFramework.bstack1l111l1l1l1_opy_: TestFramework.bstack11lll1l111l_opy_,
            TestFramework.bstack1l111111lll_opy_: test_name
        }
    @staticmethod
    def __11lll1l1ll1_opy_(node, scenario):
        if hasattr(node, bstack1l1111_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᗚ")):
            parts = node.nodeid.rsplit(bstack1l1111_opy_ (u"ࠤ࡞ࠦᗛ"))
            params = parts[-1]
            return bstack1l1111_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᗜ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11lll1llll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1111_opy_ (u"ࠫࡹࡧࡧࡴࠩᗝ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1111_opy_ (u"ࠬࡺࡡࡨࡵࠪᗞ")) else [])
    @staticmethod
    def __11lll1ll1l1_opy_(location):
        return bstack1l1111_opy_ (u"ࠨ࠺࠻ࠤᗟ").join(filter(lambda x: isinstance(x, str), location))