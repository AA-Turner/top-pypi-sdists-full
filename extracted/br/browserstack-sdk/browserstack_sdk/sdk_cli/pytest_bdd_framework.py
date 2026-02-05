# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1l1l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1111_opy_ import bstack11ll1ll1111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll11l1l1l1_opy_,
    bstack1ll1ll111l1_opy_,
    bstack1ll1111llll_opy_,
    bstack11lll11llll_opy_,
    bstack1ll1lll11ll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11ll1ll1l_opy_
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1111ll1_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll1llll1l_opy_
bstack1l1l111ll1l_opy_ = bstack1l11ll1ll1l_opy_()
bstack1l11ll1l111_opy_ = bstack11l1ll1_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᔲ")
bstack11lllll11l1_opy_ = bstack11l1ll1_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᔳ")
bstack11lllll1111_opy_ = bstack11l1ll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᔴ")
bstack11lll111l1l_opy_ = 1.0
_1l11llll111_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11llll11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᔵ")
    bstack11ll1ll1ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᔶ")
    bstack11lll1lllll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᔷ")
    bstack11ll1l11l11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᔸ")
    bstack11lll1ll11l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᔹ")
    bstack11lll11l1l1_opy_: bool
    bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_  = None
    bstack11llll1llll_opy_ = [
        bstack1ll11l1l1l1_opy_.BEFORE_ALL,
        bstack1ll11l1l1l1_opy_.AFTER_ALL,
        bstack1ll11l1l1l1_opy_.BEFORE_EACH,
        bstack1ll11l1l1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l11lll_opy_: Dict[str, str],
        bstack1l1lll1l1ll_opy_: List[str]=[bstack11l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᔺ")],
        bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_ = None,
        bstack1ll1llll1ll_opy_=None
    ):
        super().__init__(bstack1l1lll1l1ll_opy_, bstack11ll1l11lll_opy_, bstack1lll1llll11_opy_)
        self.bstack11lll11l1l1_opy_ = any(bstack11l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᔻ") in item.lower() for item in bstack1l1lll1l1ll_opy_)
        self.bstack1ll1llll1ll_opy_ = bstack1ll1llll1ll_opy_
    def track_event(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll11l1l1l1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11llll1llll_opy_:
            bstack11ll1ll1111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll11l1l1l1_opy_.NONE:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᔼ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠧࠨᔽ"))
            return
        if not self.bstack11lll11l1l1_opy_:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᔾ") + str(str(self.bstack1l1lll1l1ll_opy_)) + bstack11l1ll1_opy_ (u"ࠢࠣᔿ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕀ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᕁ"))
            return
        instance = self.__11lll1l11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᕂ") + str(args) + bstack11l1ll1_opy_ (u"ࠦࠧᕃ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11llll1llll_opy_ and test_hook_state == bstack1ll1111llll_opy_.PRE:
                bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11l111ll11_opy_.value)
                name = str(EVENTS.bstack11l111ll11_opy_.name)+bstack11l1ll1_opy_ (u"ࠧࡀࠢᕄ")+str(test_framework_state.name)
                TestFramework.bstack11ll1l1l1l1_opy_(instance, name, bstack1lll1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᕅ").format(e))
        try:
            if test_framework_state == bstack1ll11l1l1l1_opy_.TEST:
                if not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_) and test_hook_state == bstack1ll1111llll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11lll111ll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕆ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠣࠤᕇ"))
                if test_hook_state == bstack1ll1111llll_opy_.PRE and not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll1ll11_opy_):
                    TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l11ll1ll11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11ll1ll1l11_opy_(instance, args)
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕈ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠥࠦᕉ"))
                elif test_hook_state == bstack1ll1111llll_opy_.POST and not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l1l11lll11_opy_):
                    TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕊ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠧࠨᕋ"))
            elif test_framework_state == bstack1ll11l1l1l1_opy_.STEP:
                if test_hook_state == bstack1ll1111llll_opy_.PRE:
                    PytestBDDFramework.__11ll1llll11_opy_(instance, args)
                elif test_hook_state == bstack1ll1111llll_opy_.POST:
                    PytestBDDFramework.__11llll11111_opy_(instance, args)
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG and test_hook_state == bstack1ll1111llll_opy_.POST:
                PytestBDDFramework.__11llll111ll_opy_(instance, *args)
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG_REPORT and test_hook_state == bstack1ll1111llll_opy_.POST:
                self.__11lll1111ll_opy_(instance, *args)
                self.__11ll1l1ll11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11llll1llll_opy_:
                self.__11lll11111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᕌ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠢࠣᕍ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lll1ll111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11llll1llll_opy_ and test_hook_state == bstack1ll1111llll_opy_.POST:
                name = str(EVENTS.bstack11l111ll11_opy_.name)+bstack11l1ll1_opy_ (u"ࠣ࠼ࠥᕎ")+str(test_framework_state.name)
                bstack1lll1llll1_opy_ = TestFramework.bstack11lllll11ll_opy_(instance, name)
                bstack1ll1111ll_opy_.end(EVENTS.bstack11l111ll11_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᕏ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᕐ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᕑ").format(e))
    def bstack1l1l11l11l1_opy_(self):
        return self.bstack11lll11l1l1_opy_
    def __11ll1l1l11l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1ll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᕒ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11l1lll11_opy_(rep, [bstack11l1ll1_opy_ (u"ࠨࡷࡩࡧࡱࠦᕓ"), bstack11l1ll1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᕔ"), bstack11l1ll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᕕ"), bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᕖ"), bstack11l1ll1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᕗ"), bstack11l1ll1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᕘ")])
        return None
    def __11lll1111ll_opy_(self, instance: bstack1ll1ll111l1_opy_, *args):
        result = self.__11ll1l1l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll11111l_opy_ = None
        if result.get(bstack11l1ll1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᕙ"), None) == bstack11l1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕚ") and len(args) > 1 and getattr(args[1], bstack11l1ll1_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᕛ"), None) is not None:
            failure = [{bstack11l1ll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᕜ"): [args[1].excinfo.exconly(), result.get(bstack11l1ll1_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᕝ"), None)]}]
            bstack1llll11111l_opy_ = bstack11l1ll1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᕞ") if bstack11l1ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᕟ") in getattr(args[1].excinfo, bstack11l1ll1_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᕠ"), bstack11l1ll1_opy_ (u"ࠨࠢᕡ")) else bstack11l1ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᕢ")
        bstack11lll1ll1l1_opy_ = result.get(bstack11l1ll1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᕣ"), TestFramework.bstack11ll1l1l111_opy_)
        if bstack11lll1ll1l1_opy_ != TestFramework.bstack11ll1l1l111_opy_:
            TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11lll1111l1_opy_(instance, {
            TestFramework.bstack1l111ll111l_opy_: failure,
            TestFramework.bstack11llll1ll11_opy_: bstack1llll11111l_opy_,
            TestFramework.bstack1l111l1ll11_opy_: bstack11lll1ll1l1_opy_,
        })
    def __11lll1l11l1_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll11l1l1l1_opy_.SETUP_FIXTURE:
            instance = self.__11ll1lll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1l1lll1_opy_ bstack11lll11lll1_opy_ this to be bstack11l1ll1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᕤ")
            if test_framework_state == bstack1ll11l1l1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll1lll1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1ll1_opy_ (u"ࠥࡲࡴࡪࡥࠣᕥ"), None), bstack11l1ll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᕦ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1ll1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᕧ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᕨ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11ll11l_opy_(target) if target else None
        return instance
    def __11lll11111l_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11ll1lllll1_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, PytestBDDFramework.bstack11ll1ll1ll1_opy_, {})
        if not key in bstack11ll1lllll1_opy_:
            bstack11ll1lllll1_opy_[key] = []
        bstack11llll1l11l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, PytestBDDFramework.bstack11lll1lllll_opy_, {})
        if not key in bstack11llll1l11l_opy_:
            bstack11llll1l11l_opy_[key] = []
        bstack11lll1l1ll1_opy_ = {
            PytestBDDFramework.bstack11ll1ll1ll1_opy_: bstack11ll1lllll1_opy_,
            PytestBDDFramework.bstack11lll1lllll_opy_: bstack11llll1l11l_opy_,
        }
        if test_hook_state == bstack1ll1111llll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1ll1_opy_ (u"ࠢ࡬ࡧࡼࠦᕩ"): key,
                TestFramework.bstack11llll1lll1_opy_: uuid4().__str__(),
                TestFramework.bstack11ll1llll1l_opy_: TestFramework.bstack11llll1ll1l_opy_,
                TestFramework.bstack11ll1ll1lll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11lll1l1l1l_opy_: [],
                TestFramework.bstack11lll1llll1_opy_: hook_name,
                TestFramework.bstack11ll1lll111_opy_: bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()
            }
            bstack11ll1lllll1_opy_[key].append(hook)
            bstack11lll1l1ll1_opy_[PytestBDDFramework.bstack11ll1l11l11_opy_] = key
        elif test_hook_state == bstack1ll1111llll_opy_.POST:
            bstack11ll1l11l1l_opy_ = bstack11ll1lllll1_opy_.get(key, [])
            hook = bstack11ll1l11l1l_opy_.pop() if bstack11ll1l11l1l_opy_ else None
            if hook:
                result = self.__11ll1l1l11l_opy_(*args)
                if result:
                    bstack11llll11l11_opy_ = result.get(bstack11l1ll1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᕪ"), TestFramework.bstack11llll1ll1l_opy_)
                    if bstack11llll11l11_opy_ != TestFramework.bstack11llll1ll1l_opy_:
                        hook[TestFramework.bstack11ll1llll1l_opy_] = bstack11llll11l11_opy_
                hook[TestFramework.bstack11llll1l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1lll111_opy_] = bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()
                self.bstack11ll1l1ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11lll11ll1l_opy_, [])
                self.bstack1l11lll1lll_opy_(instance, logs)
                bstack11llll1l11l_opy_[key].append(hook)
                bstack11lll1l1ll1_opy_[PytestBDDFramework.bstack11lll1ll11l_opy_] = key
        TestFramework.bstack11lll1111l1_opy_(instance, bstack11lll1l1ll1_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᕫ") + str(bstack11llll1l11l_opy_) + bstack11l1ll1_opy_ (u"ࠥࠦᕬ"))
    def __11ll1lll1ll_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11l1lll11_opy_(args[0], [bstack11l1ll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᕭ"), bstack11l1ll1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᕮ"), bstack11l1ll1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᕯ"), bstack11l1ll1_opy_ (u"ࠢࡪࡦࡶࠦᕰ"), bstack11l1ll1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᕱ"), bstack11l1ll1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᕲ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1ll1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᕳ")) else fixturedef.get(bstack11l1ll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᕴ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1ll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᕵ")) else None
        node = request.node if hasattr(request, bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᕶ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1ll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᕷ")) else None
        baseid = fixturedef.get(bstack11l1ll1_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᕸ"), None) or bstack11l1ll1_opy_ (u"ࠤࠥᕹ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1ll1_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᕺ")):
            target = PytestBDDFramework.__11lll111l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1ll1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᕻ")) else None
            if target and not TestFramework.bstack1lll11ll11l_opy_(target):
                self.__11ll1lll1l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕼ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠨࠢᕽ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᕾ") + str(target) + bstack11l1ll1_opy_ (u"ࠣࠤᕿ"))
            return None
        instance = TestFramework.bstack1lll11ll11l_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᖀ") + str(target) + bstack11l1ll1_opy_ (u"ࠥࠦᖁ"))
            return None
        bstack11lll1l1l11_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, PytestBDDFramework.bstack11llll11l1l_opy_, {})
        if os.getenv(bstack11l1ll1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᖂ"), bstack11l1ll1_opy_ (u"ࠧ࠷ࠢᖃ")) == bstack11l1ll1_opy_ (u"ࠨ࠱ࠣᖄ"):
            bstack11llll1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠢ࠻ࠤᖅ").join((scope, fixturename))
            bstack11lllll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1lll11l_opy_ = {
                bstack11l1ll1_opy_ (u"ࠣ࡭ࡨࡽࠧᖆ"): bstack11llll1l1ll_opy_,
                bstack11l1ll1_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᖇ"): PytestBDDFramework.__11ll1l111ll_opy_(request.node, scenario),
                bstack11l1ll1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᖈ"): fixturedef,
                bstack11l1ll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᖉ"): scope,
                bstack11l1ll1_opy_ (u"ࠧࡺࡹࡱࡧࠥᖊ"): None,
            }
            try:
                if test_hook_state == bstack1ll1111llll_opy_.POST and callable(getattr(args[-1], bstack11l1ll1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᖋ"), None)):
                    bstack11ll1lll11l_opy_[bstack11l1ll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᖌ")] = TestFramework.bstack1l1l11l1ll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1111llll_opy_.PRE:
                bstack11ll1lll11l_opy_[bstack11l1ll1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᖍ")] = uuid4().__str__()
                bstack11ll1lll11l_opy_[PytestBDDFramework.bstack11ll1ll1lll_opy_] = bstack11lllll111l_opy_
            elif test_hook_state == bstack1ll1111llll_opy_.POST:
                bstack11ll1lll11l_opy_[PytestBDDFramework.bstack11llll1l111_opy_] = bstack11lllll111l_opy_
            if bstack11llll1l1ll_opy_ in bstack11lll1l1l11_opy_:
                bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_].update(bstack11ll1lll11l_opy_)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᖎ") + str(bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_]) + bstack11l1ll1_opy_ (u"ࠥࠦᖏ"))
            else:
                bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_] = bstack11ll1lll11l_opy_
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᖐ") + str(len(bstack11lll1l1l11_opy_)) + bstack11l1ll1_opy_ (u"ࠧࠨᖑ"))
        TestFramework.bstack1lll1l1111l_opy_(instance, PytestBDDFramework.bstack11llll11l1l_opy_, bstack11lll1l1l11_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᖒ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠢࠣᖓ"))
        return instance
    def __11ll1lll1l1_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lll1l1l111_opy_.create_context(target)
        ob = bstack1ll1ll111l1_opy_(ctx, self.bstack1l1lll1l1ll_opy_, self.bstack11ll1l11lll_opy_, test_framework_state)
        TestFramework.bstack11lll1111l1_opy_(ob, {
            TestFramework.bstack1l1llllll11_opy_: context.test_framework_name,
            TestFramework.bstack1l1l111llll_opy_: context.test_framework_version,
            TestFramework.bstack11ll1l1l1ll_opy_: [],
            PytestBDDFramework.bstack11llll11l1l_opy_: {},
            PytestBDDFramework.bstack11lll1lllll_opy_: {},
            PytestBDDFramework.bstack11ll1ll1ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l1111l_opy_(ob, TestFramework.bstack11lll1l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l1111l_opy_(ob, TestFramework.bstack1l1l1lll1l1_opy_, context.platform_index)
        TestFramework.bstack1lll1ll11ll_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᖔ") + str(TestFramework.bstack1lll1ll11ll_opy_.keys()) + bstack11l1ll1_opy_ (u"ࠤࠥᖕ"))
        return ob
    @staticmethod
    def __11ll1ll1l11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭ᖖ"): id(step),
                bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᖗ"): step.name,
                bstack11l1ll1_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ᖘ"): step.keyword,
            })
        meta = {
            bstack11l1ll1_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᖙ"): {
                bstack11l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᖚ"): feature.name,
                bstack11l1ll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭ᖛ"): feature.filename,
                bstack11l1ll1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᖜ"): feature.description
            },
            bstack11l1ll1_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᖝ"): {
                bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᖞ"): scenario.name
            },
            bstack11l1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᖟ"): steps,
            bstack11l1ll1_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᖠ"): PytestBDDFramework.__11lll1lll11_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11lll111lll_opy_: meta
            }
        )
    def bstack11ll1l1ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᖡ")
        global _1l11llll111_opy_
        platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᖢ")]
        bstack1l11llll11l_opy_ = os.path.join(bstack1l1l111ll1l_opy_, (bstack1l11ll1l111_opy_ + str(platform_index)), bstack11lllll11l1_opy_)
        if not os.path.exists(bstack1l11llll11l_opy_) or not os.path.isdir(bstack1l11llll11l_opy_):
            return
        logs = hook.get(bstack11l1ll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᖣ"), [])
        with os.scandir(bstack1l11llll11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11llll111_opy_:
                    self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᖤ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1ll1_opy_ (u"ࠦࠧᖥ")
                    log_entry = bstack1ll1lll11ll_opy_(
                        kind=bstack11l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᖦ"),
                        message=bstack11l1ll1_opy_ (u"ࠨࠢᖧ"),
                        level=bstack11l1ll1_opy_ (u"ࠢࠣᖨ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l1l1_opy_=entry.stat().st_size,
                        bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᖩ"),
                        bstack1ll1lll_opy_=os.path.abspath(entry.path),
                        bstack11ll1llllll_opy_=hook.get(TestFramework.bstack11llll1lll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l11llll111_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᖪ")]
        bstack11llll11ll1_opy_ = os.path.join(bstack1l1l111ll1l_opy_, (bstack1l11ll1l111_opy_ + str(platform_index)), bstack11lllll11l1_opy_, bstack11lllll1111_opy_)
        if not os.path.exists(bstack11llll11ll1_opy_) or not os.path.isdir(bstack11llll11ll1_opy_):
            self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᖫ").format(bstack11llll11ll1_opy_))
        else:
            self.logger.info(bstack11l1ll1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᖬ").format(bstack11llll11ll1_opy_))
            with os.scandir(bstack11llll11ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11llll111_opy_:
                        self.logger.info(bstack11l1ll1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᖭ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1ll1_opy_ (u"ࠨࠢᖮ")
                        log_entry = bstack1ll1lll11ll_opy_(
                            kind=bstack11l1ll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᖯ"),
                            message=bstack11l1ll1_opy_ (u"ࠣࠤᖰ"),
                            level=bstack11l1ll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᖱ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l1l1_opy_=entry.stat().st_size,
                            bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᖲ"),
                            bstack1ll1lll_opy_=os.path.abspath(entry.path),
                            bstack1l1l11l1l11_opy_=hook.get(TestFramework.bstack11llll1lll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l11llll111_opy_.add(abs_path)
        hook[bstack11l1ll1_opy_ (u"ࠦࡱࡵࡧࡴࠤᖳ")] = logs
    def bstack1l11lll1lll_opy_(
        self,
        bstack1l11lll1ll1_opy_: bstack1ll1ll111l1_opy_,
        entries: List[bstack1ll1lll11ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᖴ"))
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᖵ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll1ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll1ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll1ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1llllll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l111llll_opy_)
            log_entry.uuid = entry.bstack11ll1llllll_opy_ if entry.bstack11ll1llllll_opy_ else TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1llll1l11_opy_)
            log_entry.test_framework_state = bstack1l11lll1ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᖶ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᖷ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1l1_opy_
                log_entry.file_path = entry.bstack1ll1lll_opy_
        def bstack1l11ll1llll_opy_():
            bstack111ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1ll1llll1ll_opy_.LogCreatedEvent(req)
                bstack1l11lll1ll1_opy_.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᖸ"), datetime.now() - bstack111ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1ll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᖹ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1llll11_opy_.enqueue(bstack1l11ll1llll_opy_)
    def __11ll1l1ll11_opy_(self, instance) -> None:
        bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᖺ")
        bstack11lll1l1ll1_opy_ = {bstack11l1ll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᖻ"): bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()}
        TestFramework.bstack11lll1111l1_opy_(instance, bstack11lll1l1ll1_opy_)
    @staticmethod
    def __11ll1llll11_opy_(instance, args):
        request, bstack11ll1ll11ll_opy_ = args
        bstack11lll1l1111_opy_ = id(bstack11ll1ll11ll_opy_)
        bstack11lll1l11ll_opy_ = instance.data[TestFramework.bstack11lll111lll_opy_]
        step = next(filter(lambda st: st[bstack11l1ll1_opy_ (u"࠭ࡩࡥࠩᖼ")] == bstack11lll1l1111_opy_, bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᖽ")]), None)
        step.update({
            bstack11l1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖾ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᖿ")]) if st[bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭ᗀ")] == step[bstack11l1ll1_opy_ (u"ࠫ࡮ࡪࠧᗁ")]), None)
        if index is not None:
            bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᗂ")][index] = step
        instance.data[TestFramework.bstack11lll111lll_opy_] = bstack11lll1l11ll_opy_
    @staticmethod
    def __11llll11111_opy_(instance, args):
        bstack11l1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᗃ")
        bstack11lll1lll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1ll11ll_opy_ = args[1]
        bstack11lll1l1111_opy_ = id(bstack11ll1ll11ll_opy_)
        bstack11lll1l11ll_opy_ = instance.data[TestFramework.bstack11lll111lll_opy_]
        step = None
        if bstack11lll1l1111_opy_ is not None and bstack11lll1l11ll_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᗄ")):
            step = next(filter(lambda st: st[bstack11l1ll1_opy_ (u"ࠨ࡫ࡧࠫᗅ")] == bstack11lll1l1111_opy_, bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᗆ")]), None)
            step.update({
                bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗇ"): bstack11lll1lll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᗈ"): bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗉ"),
                bstack11l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᗊ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᗋ"): bstack11l1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗌ"),
                })
        index = next((i for i, st in enumerate(bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᗍ")]) if st[bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭ᗎ")] == step[bstack11l1ll1_opy_ (u"ࠫ࡮ࡪࠧᗏ")]), None)
        if index is not None:
            bstack11lll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᗐ")][index] = step
        instance.data[TestFramework.bstack11lll111lll_opy_] = bstack11lll1l11ll_opy_
    @staticmethod
    def __11lll1lll11_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᗑ")):
                examples = list(node.callspec.params[bstack11l1ll1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᗒ")].values())
            return examples
        except:
            return []
    def bstack1l11llll1ll_opy_(self, instance: bstack1ll1ll111l1_opy_, bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]):
        bstack11lll11l111_opy_ = (
            PytestBDDFramework.bstack11ll1l11l11_opy_
            if bstack1lll1l1ll11_opy_[1] == bstack1ll1111llll_opy_.PRE
            else PytestBDDFramework.bstack11lll1ll11l_opy_
        )
        hook = PytestBDDFramework.bstack11ll1l1llll_opy_(instance, bstack11lll11l111_opy_)
        entries = hook.get(TestFramework.bstack11lll1l1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, []))
        return entries
    def bstack1l11lll11ll_opy_(self, instance: bstack1ll1ll111l1_opy_, bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]):
        bstack11lll11l111_opy_ = (
            PytestBDDFramework.bstack11ll1l11l11_opy_
            if bstack1lll1l1ll11_opy_[1] == bstack1ll1111llll_opy_.PRE
            else PytestBDDFramework.bstack11lll1ll11l_opy_
        )
        PytestBDDFramework.bstack11lll1ll1ll_opy_(instance, bstack11lll11l111_opy_)
        TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, []).clear()
    @staticmethod
    def bstack11ll1l1llll_opy_(instance: bstack1ll1ll111l1_opy_, bstack11lll11l111_opy_: str):
        bstack11llll1l1l1_opy_ = (
            PytestBDDFramework.bstack11lll1lllll_opy_
            if bstack11lll11l111_opy_ == PytestBDDFramework.bstack11lll1ll11l_opy_
            else PytestBDDFramework.bstack11ll1ll1ll1_opy_
        )
        bstack11ll1ll111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11lll11l111_opy_, None)
        bstack11lll1l111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11llll1l1l1_opy_, None) if bstack11ll1ll111l_opy_ else None
        return (
            bstack11lll1l111l_opy_[bstack11ll1ll111l_opy_][-1]
            if isinstance(bstack11lll1l111l_opy_, dict) and len(bstack11lll1l111l_opy_.get(bstack11ll1ll111l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lll1ll1ll_opy_(instance: bstack1ll1ll111l1_opy_, bstack11lll11l111_opy_: str):
        hook = PytestBDDFramework.bstack11ll1l1llll_opy_(instance, bstack11lll11l111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11lll1l1l1l_opy_, []).clear()
    @staticmethod
    def __11llll111ll_opy_(instance: bstack1ll1ll111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1ll1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᗓ"), None)):
            return
        if os.getenv(bstack11l1ll1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᗔ"), bstack11l1ll1_opy_ (u"ࠥ࠵ࠧᗕ")) != bstack11l1ll1_opy_ (u"ࠦ࠶ࠨᗖ"):
            PytestBDDFramework.logger.warning(bstack11l1ll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᗗ"))
            return
        bstack11ll1ll11l1_opy_ = {
            bstack11l1ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᗘ"): (PytestBDDFramework.bstack11ll1l11l11_opy_, PytestBDDFramework.bstack11ll1ll1ll1_opy_),
            bstack11l1ll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᗙ"): (PytestBDDFramework.bstack11lll1ll11l_opy_, PytestBDDFramework.bstack11lll1lllll_opy_),
        }
        for when in (bstack11l1ll1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗚ"), bstack11l1ll1_opy_ (u"ࠤࡦࡥࡱࡲࠢᗛ"), bstack11l1ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᗜ")):
            bstack11llll11lll_opy_ = args[1].get_records(when)
            if not bstack11llll11lll_opy_:
                continue
            records = [
                bstack1ll1lll11ll_opy_(
                    kind=TestFramework.bstack1l1l11l1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1ll1_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᗝ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1ll1_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᗞ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll11lll_opy_
                if isinstance(getattr(r, bstack11l1ll1_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᗟ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11lll11ll11_opy_, bstack11llll1l1l1_opy_ = bstack11ll1ll11l1_opy_.get(when, (None, None))
            bstack11ll1l11ll1_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11lll11ll11_opy_, None) if bstack11lll11ll11_opy_ else None
            bstack11lll1l111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11llll1l1l1_opy_, None) if bstack11ll1l11ll1_opy_ else None
            if isinstance(bstack11lll1l111l_opy_, dict) and len(bstack11lll1l111l_opy_.get(bstack11ll1l11ll1_opy_, [])) > 0:
                hook = bstack11lll1l111l_opy_[bstack11ll1l11ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11lll1l1l1l_opy_ in hook:
                    hook[TestFramework.bstack11lll1l1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11lll111ll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1111ll111_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11lll11l1ll_opy_(request.node, scenario)
        bstack11llll1111l_opy_ = feature.filename
        if not bstack1111ll111_opy_ or not test_name or not bstack11llll1111l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1llll1l11_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1ll1l1l_opy_: bstack1111ll111_opy_,
            TestFramework.bstack1l1l1lll11l_opy_: test_name,
            TestFramework.bstack1l11l1l1l11_opy_: bstack1111ll111_opy_,
            TestFramework.bstack11lll111111_opy_: bstack11llll1111l_opy_,
            TestFramework.bstack11lll11l11l_opy_: PytestBDDFramework.__11ll1l111ll_opy_(feature, scenario),
            TestFramework.bstack11llll111l1_opy_: code,
            TestFramework.bstack1l111l1ll11_opy_: TestFramework.bstack11ll1l1l111_opy_,
            TestFramework.bstack1l111111111_opy_: test_name
        }
    @staticmethod
    def __11lll11l1ll_opy_(node, scenario):
        if hasattr(node, bstack11l1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᗠ")):
            parts = node.nodeid.rsplit(bstack11l1ll1_opy_ (u"ࠣ࡝ࠥᗡ"))
            params = parts[-1]
            return bstack11l1ll1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᗢ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll1l111ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᗣ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1ll1_opy_ (u"ࠫࡹࡧࡧࡴࠩᗤ")) else [])
    @staticmethod
    def __11lll111l11_opy_(location):
        return bstack11l1ll1_opy_ (u"ࠧࡀ࠺ࠣᗥ").join(filter(lambda x: isinstance(x, str), location))