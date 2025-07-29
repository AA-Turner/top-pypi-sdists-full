# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllll11l1l_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l111l11ll_opy_ import bstack1l111l11111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l11l1l_opy_,
    bstack1ll1ll11l1l_opy_,
    bstack1lll111l111_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1l1ll11l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1l1llllll_opy_
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1ll1_opy_ import bstack1ll1lll1111_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1111111lll_opy_
bstack1l1ll1lllll_opy_ = bstack1l1l1llllll_opy_()
bstack1l1llll111l_opy_ = bstackl_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᐢ")
bstack1l1111l1ll1_opy_ = bstackl_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᐣ")
bstack1l111lllll1_opy_ = bstackl_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᐤ")
bstack1l111ll11l1_opy_ = 1.0
_1l1ll1l111l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111111111_opy_ = bstackl_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᐥ")
    bstack1l111l1l1ll_opy_ = bstackl_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᐦ")
    bstack1l11l111l11_opy_ = bstackl_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᐧ")
    bstack11lllll1ll1_opy_ = bstackl_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᐨ")
    bstack1l1111l11ll_opy_ = bstackl_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᐩ")
    bstack1l1111lll1l_opy_: bool
    bstack111111l1l1_opy_: bstack1111111lll_opy_  = None
    bstack1l1111l1111_opy_ = [
        bstack1lll1l11l1l_opy_.BEFORE_ALL,
        bstack1lll1l11l1l_opy_.AFTER_ALL,
        bstack1lll1l11l1l_opy_.BEFORE_EACH,
        bstack1lll1l11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1111lllll_opy_: Dict[str, str],
        bstack1ll1l11111l_opy_: List[str]=[bstackl_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᐪ")],
        bstack111111l1l1_opy_: bstack1111111lll_opy_ = None,
        bstack1lll1l1l1ll_opy_=None
    ):
        super().__init__(bstack1ll1l11111l_opy_, bstack1l1111lllll_opy_, bstack111111l1l1_opy_)
        self.bstack1l1111lll1l_opy_ = any(bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᐫ") in item.lower() for item in bstack1ll1l11111l_opy_)
        self.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l11l1l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l1111l1111_opy_:
            bstack1l111l11111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l11l1l_opy_.NONE:
            self.logger.warning(bstackl_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᐬ") + str(test_hook_state) + bstackl_opy_ (u"ࠨࠢᐭ"))
            return
        if not self.bstack1l1111lll1l_opy_:
            self.logger.warning(bstackl_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᐮ") + str(str(self.bstack1ll1l11111l_opy_)) + bstackl_opy_ (u"ࠣࠤᐯ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstackl_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐰ") + str(kwargs) + bstackl_opy_ (u"ࠥࠦᐱ"))
            return
        instance = self.__1l111l111ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstackl_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᐲ") + str(args) + bstackl_opy_ (u"ࠧࠨᐳ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111l1111_opy_ and test_hook_state == bstack1lll111l111_opy_.PRE:
                bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1ll1l1111l_opy_.value)
                name = str(EVENTS.bstack1ll1l1111l_opy_.name)+bstackl_opy_ (u"ࠨ࠺ࠣᐴ")+str(test_framework_state.name)
                TestFramework.bstack1l1111ll1l1_opy_(instance, name, bstack1ll11lll11l_opy_)
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᐵ").format(e))
        try:
            if test_framework_state == bstack1lll1l11l1l_opy_.TEST:
                if not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l111ll1l11_opy_) and test_hook_state == bstack1lll111l111_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l1111l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstackl_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐶ") + str(test_hook_state) + bstackl_opy_ (u"ࠤࠥᐷ"))
                if test_hook_state == bstack1lll111l111_opy_.PRE and not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1lll111ll_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll111ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11lllll1lll_opy_(instance, args)
                    self.logger.debug(bstackl_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐸ") + str(test_hook_state) + bstackl_opy_ (u"ࠦࠧᐹ"))
                elif test_hook_state == bstack1lll111l111_opy_.POST and not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1lll11111_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstackl_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐺ") + str(test_hook_state) + bstackl_opy_ (u"ࠨࠢᐻ"))
            elif test_framework_state == bstack1lll1l11l1l_opy_.STEP:
                if test_hook_state == bstack1lll111l111_opy_.PRE:
                    PytestBDDFramework.__1l111l11lll_opy_(instance, args)
                elif test_hook_state == bstack1lll111l111_opy_.POST:
                    PytestBDDFramework.__1l111l11ll1_opy_(instance, args)
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG and test_hook_state == bstack1lll111l111_opy_.POST:
                PytestBDDFramework.__1l111llll11_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG_REPORT and test_hook_state == bstack1lll111l111_opy_.POST:
                self.__1l111l11l11_opy_(instance, *args)
                self.__1l11111llll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1111l1111_opy_:
                self.__1l1111l1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstackl_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᐼ") + str(instance.ref()) + bstackl_opy_ (u"ࠣࠤᐽ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1111ll111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111l1111_opy_ and test_hook_state == bstack1lll111l111_opy_.POST:
                name = str(EVENTS.bstack1ll1l1111l_opy_.name)+bstackl_opy_ (u"ࠤ࠽ࠦᐾ")+str(test_framework_state.name)
                bstack1ll11lll11l_opy_ = TestFramework.bstack1l1111ll1ll_opy_(instance, name)
                bstack1lll11lll1l_opy_.end(EVENTS.bstack1ll1l1111l_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᐿ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᑀ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᑁ").format(e))
    def bstack1l1ll11111l_opy_(self):
        return self.bstack1l1111lll1l_opy_
    def __1l11111ll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstackl_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᑂ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1l1ll11_opy_(rep, [bstackl_opy_ (u"ࠢࡸࡪࡨࡲࠧᑃ"), bstackl_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑄ"), bstackl_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᑅ"), bstackl_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᑆ"), bstackl_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᑇ"), bstackl_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᑈ")])
        return None
    def __1l111l11l11_opy_(self, instance: bstack1ll1ll11l1l_opy_, *args):
        result = self.__1l11111ll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111ll11_opy_ = None
        if result.get(bstackl_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑉ"), None) == bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑊ") and len(args) > 1 and getattr(args[1], bstackl_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᑋ"), None) is not None:
            failure = [{bstackl_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᑌ"): [args[1].excinfo.exconly(), result.get(bstackl_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᑍ"), None)]}]
            bstack111111ll11_opy_ = bstackl_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᑎ") if bstackl_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᑏ") in getattr(args[1].excinfo, bstackl_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᑐ"), bstackl_opy_ (u"ࠢࠣᑑ")) else bstackl_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᑒ")
        bstack11llllll1l1_opy_ = result.get(bstackl_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑓ"), TestFramework.bstack1l11111l1ll_opy_)
        if bstack11llllll1l1_opy_ != TestFramework.bstack1l11111l1ll_opy_:
            TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11111l1l1_opy_(instance, {
            TestFramework.bstack1l1l11111ll_opy_: failure,
            TestFramework.bstack1l11111ll11_opy_: bstack111111ll11_opy_,
            TestFramework.bstack1l11lllll1l_opy_: bstack11llllll1l1_opy_,
        })
    def __1l111l111ll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l11l1l_opy_.SETUP_FIXTURE:
            instance = self.__1l1111lll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll1lll_opy_ bstack1l111lll1ll_opy_ this to be bstackl_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑔ")
            if test_framework_state == bstack1lll1l11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111l1l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstackl_opy_ (u"ࠦࡳࡵࡤࡦࠤᑕ"), None), bstackl_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑖ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstackl_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑗ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstackl_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑘ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111111111_opy_(target) if target else None
        return instance
    def __1l1111l1l11_opy_(
        self,
        instance: bstack1ll1ll11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l111l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l111l1l1ll_opy_, {})
        if not key in bstack1l111l111l1_opy_:
            bstack1l111l111l1_opy_[key] = []
        bstack1l111llll1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l11l111l11_opy_, {})
        if not key in bstack1l111llll1l_opy_:
            bstack1l111llll1l_opy_[key] = []
        bstack1l111l1l111_opy_ = {
            PytestBDDFramework.bstack1l111l1l1ll_opy_: bstack1l111l111l1_opy_,
            PytestBDDFramework.bstack1l11l111l11_opy_: bstack1l111llll1l_opy_,
        }
        if test_hook_state == bstack1lll111l111_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstackl_opy_ (u"ࠣ࡭ࡨࡽࠧᑙ"): key,
                TestFramework.bstack1l111llllll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111ll11l_opy_: TestFramework.bstack11llllll111_opy_,
                TestFramework.bstack11lllllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1111ll_opy_: [],
                TestFramework.bstack1l1111l1lll_opy_: hook_name,
                TestFramework.bstack1l111l1llll_opy_: bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()
            }
            bstack1l111l111l1_opy_[key].append(hook)
            bstack1l111l1l111_opy_[PytestBDDFramework.bstack11lllll1ll1_opy_] = key
        elif test_hook_state == bstack1lll111l111_opy_.POST:
            bstack1l111l1ll1l_opy_ = bstack1l111l111l1_opy_.get(key, [])
            hook = bstack1l111l1ll1l_opy_.pop() if bstack1l111l1ll1l_opy_ else None
            if hook:
                result = self.__1l11111ll1l_opy_(*args)
                if result:
                    bstack11llllll1ll_opy_ = result.get(bstackl_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑚ"), TestFramework.bstack11llllll111_opy_)
                    if bstack11llllll1ll_opy_ != TestFramework.bstack11llllll111_opy_:
                        hook[TestFramework.bstack1l1111ll11l_opy_] = bstack11llllll1ll_opy_
                hook[TestFramework.bstack1l11l111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1llll_opy_] = bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()
                self.bstack1l111l1l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111ll1ll1_opy_, [])
                self.bstack1l1ll1l1111_opy_(instance, logs)
                bstack1l111llll1l_opy_[key].append(hook)
                bstack1l111l1l111_opy_[PytestBDDFramework.bstack1l1111l11ll_opy_] = key
        TestFramework.bstack1l11111l1l1_opy_(instance, bstack1l111l1l111_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᑛ") + str(bstack1l111llll1l_opy_) + bstackl_opy_ (u"ࠦࠧᑜ"))
    def __1l1111lll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1l1ll11_opy_(args[0], [bstackl_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑝ"), bstackl_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᑞ"), bstackl_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᑟ"), bstackl_opy_ (u"ࠣ࡫ࡧࡷࠧᑠ"), bstackl_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᑡ"), bstackl_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᑢ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstackl_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑣ")) else fixturedef.get(bstackl_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑤ"), None)
        fixturename = request.fixturename if hasattr(request, bstackl_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᑥ")) else None
        node = request.node if hasattr(request, bstackl_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᑦ")) else None
        target = request.node.nodeid if hasattr(node, bstackl_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑧ")) else None
        baseid = fixturedef.get(bstackl_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᑨ"), None) or bstackl_opy_ (u"ࠥࠦᑩ")
        if (not target or len(baseid) > 0) and hasattr(request, bstackl_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᑪ")):
            target = PytestBDDFramework.__1l11l11111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstackl_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᑫ")) else None
            if target and not TestFramework.bstack1111111111_opy_(target):
                self.__1l111l1l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstackl_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑬ") + str(test_hook_state) + bstackl_opy_ (u"ࠢࠣᑭ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstackl_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᑮ") + str(target) + bstackl_opy_ (u"ࠤࠥᑯ"))
            return None
        instance = TestFramework.bstack1111111111_opy_(target)
        if not instance:
            self.logger.warning(bstackl_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᑰ") + str(target) + bstackl_opy_ (u"ࠦࠧᑱ"))
            return None
        bstack1l111111ll1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l111111111_opy_, {})
        if os.getenv(bstackl_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᑲ"), bstackl_opy_ (u"ࠨ࠱ࠣᑳ")) == bstackl_opy_ (u"ࠢ࠲ࠤᑴ"):
            bstack1l111l1lll1_opy_ = bstackl_opy_ (u"ࠣ࠼ࠥᑵ").join((scope, fixturename))
            bstack1l11111l111_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1111l11l1_opy_ = {
                bstackl_opy_ (u"ࠤ࡮ࡩࡾࠨᑶ"): bstack1l111l1lll1_opy_,
                bstackl_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᑷ"): PytestBDDFramework.__1l111lll1l1_opy_(request.node, scenario),
                bstackl_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᑸ"): fixturedef,
                bstackl_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑹ"): scope,
                bstackl_opy_ (u"ࠨࡴࡺࡲࡨࠦᑺ"): None,
            }
            try:
                if test_hook_state == bstack1lll111l111_opy_.POST and callable(getattr(args[-1], bstackl_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᑻ"), None)):
                    bstack1l1111l11l1_opy_[bstackl_opy_ (u"ࠣࡶࡼࡴࡪࠨᑼ")] = TestFramework.bstack1l1ll1l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111l111_opy_.PRE:
                bstack1l1111l11l1_opy_[bstackl_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᑽ")] = uuid4().__str__()
                bstack1l1111l11l1_opy_[PytestBDDFramework.bstack11lllllll11_opy_] = bstack1l11111l111_opy_
            elif test_hook_state == bstack1lll111l111_opy_.POST:
                bstack1l1111l11l1_opy_[PytestBDDFramework.bstack1l11l111ll1_opy_] = bstack1l11111l111_opy_
            if bstack1l111l1lll1_opy_ in bstack1l111111ll1_opy_:
                bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_].update(bstack1l1111l11l1_opy_)
                self.logger.debug(bstackl_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᑾ") + str(bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_]) + bstackl_opy_ (u"ࠦࠧᑿ"))
            else:
                bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_] = bstack1l1111l11l1_opy_
                self.logger.debug(bstackl_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᒀ") + str(len(bstack1l111111ll1_opy_)) + bstackl_opy_ (u"ࠨࠢᒁ"))
        TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l111111111_opy_, bstack1l111111ll1_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᒂ") + str(instance.ref()) + bstackl_opy_ (u"ࠣࠤᒃ"))
        return instance
    def __1l111l1l11l_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1lllll_opy_.create_context(target)
        ob = bstack1ll1ll11l1l_opy_(ctx, self.bstack1ll1l11111l_opy_, self.bstack1l1111lllll_opy_, test_framework_state)
        TestFramework.bstack1l11111l1l1_opy_(ob, {
            TestFramework.bstack1ll1l1111l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1l1l1_opy_: context.test_framework_version,
            TestFramework.bstack11lllllll1l_opy_: [],
            PytestBDDFramework.bstack1l111111111_opy_: {},
            PytestBDDFramework.bstack1l11l111l11_opy_: {},
            PytestBDDFramework.bstack1l111l1l1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack11llllllll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack1ll111ll1l1_opy_, context.platform_index)
        TestFramework.bstack1lllllll1ll_opy_[ctx.id] = ob
        self.logger.debug(bstackl_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᒄ") + str(TestFramework.bstack1lllllll1ll_opy_.keys()) + bstackl_opy_ (u"ࠥࠦᒅ"))
        return ob
    @staticmethod
    def __11lllll1lll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstackl_opy_ (u"ࠫ࡮ࡪࠧᒆ"): id(step),
                bstackl_opy_ (u"ࠬࡺࡥࡹࡶࠪᒇ"): step.name,
                bstackl_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᒈ"): step.keyword,
            })
        meta = {
            bstackl_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᒉ"): {
                bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᒊ"): feature.name,
                bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᒋ"): feature.filename,
                bstackl_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒌ"): feature.description
            },
            bstackl_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᒍ"): {
                bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒎ"): scenario.name
            },
            bstackl_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒏ"): steps,
            bstackl_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᒐ"): PytestBDDFramework.__1l111ll111l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111ll1111_opy_: meta
            }
        )
    def bstack1l111l1l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstackl_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒑ")
        global _1l1ll1l111l_opy_
        platform_index = os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒒ")]
        bstack1l1lll1ll1l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l1111l1ll1_opy_)
        if not os.path.exists(bstack1l1lll1ll1l_opy_) or not os.path.isdir(bstack1l1lll1ll1l_opy_):
            return
        logs = hook.get(bstackl_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᒓ"), [])
        with os.scandir(bstack1l1lll1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l111l_opy_:
                    self.logger.info(bstackl_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᒔ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstackl_opy_ (u"ࠧࠨᒕ")
                    log_entry = bstack1ll1l1ll11l_opy_(
                        kind=bstackl_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒖ"),
                        message=bstackl_opy_ (u"ࠢࠣᒗ"),
                        level=bstackl_opy_ (u"ࠣࠤᒘ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll11l1_opy_=entry.stat().st_size,
                        bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᒙ"),
                        bstack11llll_opy_=os.path.abspath(entry.path),
                        bstack1l111111l11_opy_=hook.get(TestFramework.bstack1l111llllll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l111l_opy_.add(abs_path)
        platform_index = os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒚ")]
        bstack1l11111111l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l1111l1ll1_opy_, bstack1l111lllll1_opy_)
        if not os.path.exists(bstack1l11111111l_opy_) or not os.path.isdir(bstack1l11111111l_opy_):
            self.logger.info(bstackl_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᒛ").format(bstack1l11111111l_opy_))
        else:
            self.logger.info(bstackl_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᒜ").format(bstack1l11111111l_opy_))
            with os.scandir(bstack1l11111111l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstackl_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᒝ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstackl_opy_ (u"ࠢࠣᒞ")
                        log_entry = bstack1ll1l1ll11l_opy_(
                            kind=bstackl_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒟ"),
                            message=bstackl_opy_ (u"ࠤࠥᒠ"),
                            level=bstackl_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᒡ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll11l1_opy_=entry.stat().st_size,
                            bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᒢ"),
                            bstack11llll_opy_=os.path.abspath(entry.path),
                            bstack1l1l1l1lll1_opy_=hook.get(TestFramework.bstack1l111llllll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l111l_opy_.add(abs_path)
        hook[bstackl_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᒣ")] = logs
    def bstack1l1ll1l1111_opy_(
        self,
        bstack1l1l1l1llll_opy_: bstack1ll1ll11l1l_opy_,
        entries: List[bstack1ll1l1ll11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᒤ"))
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
        req.execution_context.hash = str(bstack1l1l1l1llll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1llll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1llll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1l1lll1l1l1_opy_)
            log_entry.uuid = entry.bstack1l111111l11_opy_ if entry.bstack1l111111l11_opy_ else TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll11l11lll_opy_)
            log_entry.test_framework_state = bstack1l1l1l1llll_opy_.state.name
            log_entry.message = entry.message.encode(bstackl_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒥ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstackl_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒦ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll11l1_opy_
                log_entry.file_path = entry.bstack11llll_opy_
        def bstack1l1ll11l1l1_opy_():
            bstack1l1ll11l1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1l1ll_opy_.LogCreatedEvent(req)
                bstack1l1l1l1llll_opy_.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᒧ"), datetime.now() - bstack1l1ll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstackl_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᒨ").format(str(e)))
                traceback.print_exc()
        self.bstack111111l1l1_opy_.enqueue(bstack1l1ll11l1l1_opy_)
    def __1l11111llll_opy_(self, instance) -> None:
        bstackl_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒩ")
        bstack1l111l1l111_opy_ = {bstackl_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᒪ"): bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()}
        TestFramework.bstack1l11111l1l1_opy_(instance, bstack1l111l1l111_opy_)
    @staticmethod
    def __1l111l11lll_opy_(instance, args):
        request, bstack11llllll11l_opy_ = args
        bstack11lllll1l1l_opy_ = id(bstack11llllll11l_opy_)
        bstack1l111lll11l_opy_ = instance.data[TestFramework.bstack1l111ll1111_opy_]
        step = next(filter(lambda st: st[bstackl_opy_ (u"࠭ࡩࡥࠩᒫ")] == bstack11lllll1l1l_opy_, bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒬ")]), None)
        step.update({
            bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᒭ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒮ")]) if st[bstackl_opy_ (u"ࠪ࡭ࡩ࠭ᒯ")] == step[bstackl_opy_ (u"ࠫ࡮ࡪࠧᒰ")]), None)
        if index is not None:
            bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒱ")][index] = step
        instance.data[TestFramework.bstack1l111ll1111_opy_] = bstack1l111lll11l_opy_
    @staticmethod
    def __1l111l11ll1_opy_(instance, args):
        bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒲ")
        bstack1l1111l111l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11llllll11l_opy_ = args[1]
        bstack11lllll1l1l_opy_ = id(bstack11llllll11l_opy_)
        bstack1l111lll11l_opy_ = instance.data[TestFramework.bstack1l111ll1111_opy_]
        step = None
        if bstack11lllll1l1l_opy_ is not None and bstack1l111lll11l_opy_.get(bstackl_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒳ")):
            step = next(filter(lambda st: st[bstackl_opy_ (u"ࠨ࡫ࡧࠫᒴ")] == bstack11lllll1l1l_opy_, bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒵ")]), None)
            step.update({
                bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᒶ"): bstack1l1111l111l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstackl_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᒷ"): bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒸ"),
                bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᒹ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᒺ"): bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᒻ"),
                })
        index = next((i for i, st in enumerate(bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒼ")]) if st[bstackl_opy_ (u"ࠪ࡭ࡩ࠭ᒽ")] == step[bstackl_opy_ (u"ࠫ࡮ࡪࠧᒾ")]), None)
        if index is not None:
            bstack1l111lll11l_opy_[bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")][index] = step
        instance.data[TestFramework.bstack1l111ll1111_opy_] = bstack1l111lll11l_opy_
    @staticmethod
    def __1l111ll111l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstackl_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᓀ")):
                examples = list(node.callspec.params[bstackl_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᓁ")].values())
            return examples
        except:
            return []
    def bstack1l1l1lll1l1_opy_(self, instance: bstack1ll1ll11l1l_opy_, bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_]):
        bstack1l111lll111_opy_ = (
            PytestBDDFramework.bstack11lllll1ll1_opy_
            if bstack1lllll1l1ll_opy_[1] == bstack1lll111l111_opy_.PRE
            else PytestBDDFramework.bstack1l1111l11ll_opy_
        )
        hook = PytestBDDFramework.bstack11lllllllll_opy_(instance, bstack1l111lll111_opy_)
        entries = hook.get(TestFramework.bstack1l11l1111ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []))
        return entries
    def bstack1l1ll1ll111_opy_(self, instance: bstack1ll1ll11l1l_opy_, bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_]):
        bstack1l111lll111_opy_ = (
            PytestBDDFramework.bstack11lllll1ll1_opy_
            if bstack1lllll1l1ll_opy_[1] == bstack1lll111l111_opy_.PRE
            else PytestBDDFramework.bstack1l1111l11ll_opy_
        )
        PytestBDDFramework.bstack1l11111l11l_opy_(instance, bstack1l111lll111_opy_)
        TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []).clear()
    @staticmethod
    def bstack11lllllllll_opy_(instance: bstack1ll1ll11l1l_opy_, bstack1l111lll111_opy_: str):
        bstack1l111l1111l_opy_ = (
            PytestBDDFramework.bstack1l11l111l11_opy_
            if bstack1l111lll111_opy_ == PytestBDDFramework.bstack1l1111l11ll_opy_
            else PytestBDDFramework.bstack1l111l1l1ll_opy_
        )
        bstack1l111111l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111lll111_opy_, None)
        bstack1l11l111111_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1111l_opy_, None) if bstack1l111111l1l_opy_ else None
        return (
            bstack1l11l111111_opy_[bstack1l111111l1l_opy_][-1]
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l111111l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111l11l_opy_(instance: bstack1ll1ll11l1l_opy_, bstack1l111lll111_opy_: str):
        hook = PytestBDDFramework.bstack11lllllllll_opy_(instance, bstack1l111lll111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1111ll_opy_, []).clear()
    @staticmethod
    def __1l111llll11_opy_(instance: bstack1ll1ll11l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstackl_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᓂ"), None)):
            return
        if os.getenv(bstackl_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᓃ"), bstackl_opy_ (u"ࠥ࠵ࠧᓄ")) != bstackl_opy_ (u"ࠦ࠶ࠨᓅ"):
            PytestBDDFramework.logger.warning(bstackl_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᓆ"))
            return
        bstack1l11111lll1_opy_ = {
            bstackl_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓇ"): (PytestBDDFramework.bstack11lllll1ll1_opy_, PytestBDDFramework.bstack1l111l1l1ll_opy_),
            bstackl_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓈ"): (PytestBDDFramework.bstack1l1111l11ll_opy_, PytestBDDFramework.bstack1l11l111l11_opy_),
        }
        for when in (bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᓉ"), bstackl_opy_ (u"ࠤࡦࡥࡱࡲࠢᓊ"), bstackl_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᓋ")):
            bstack1l1111llll1_opy_ = args[1].get_records(when)
            if not bstack1l1111llll1_opy_:
                continue
            records = [
                bstack1ll1l1ll11l_opy_(
                    kind=TestFramework.bstack1l1lll1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstackl_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᓌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstackl_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᓍ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1111llll1_opy_
                if isinstance(getattr(r, bstackl_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᓎ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111l1ll11_opy_, bstack1l111l1111l_opy_ = bstack1l11111lll1_opy_.get(when, (None, None))
            bstack1l11l111l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1ll11_opy_, None) if bstack1l111l1ll11_opy_ else None
            bstack1l11l111111_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1111l_opy_, None) if bstack1l11l111l1l_opy_ else None
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l11l111l1l_opy_, [])) > 0:
                hook = bstack1l11l111111_opy_[bstack1l11l111l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l1111ll_opy_ in hook:
                    hook[TestFramework.bstack1l11l1111ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1111l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1lll11ll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l111ll1l1l_opy_(request.node, scenario)
        bstack1l1111111ll_opy_ = feature.filename
        if not bstack1lll11ll_opy_ or not test_name or not bstack1l1111111ll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11l11lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111ll1l11_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack1ll1l111l1l_opy_: test_name,
            TestFramework.bstack1l1l1l111ll_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack1l1111l1l1l_opy_: bstack1l1111111ll_opy_,
            TestFramework.bstack1l1111111l1_opy_: PytestBDDFramework.__1l111lll1l1_opy_(feature, scenario),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l11lllll1l_opy_: TestFramework.bstack1l11111l1ll_opy_,
            TestFramework.bstack1l11l1l1l11_opy_: test_name
        }
    @staticmethod
    def __1l111ll1l1l_opy_(node, scenario):
        if hasattr(node, bstackl_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᓏ")):
            parts = node.nodeid.rsplit(bstackl_opy_ (u"ࠣ࡝ࠥᓐ"))
            params = parts[-1]
            return bstackl_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᓑ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111lll1l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstackl_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᓒ")) else []) + (list(scenario.tags) if hasattr(scenario, bstackl_opy_ (u"ࠫࡹࡧࡧࡴࠩᓓ")) else [])
    @staticmethod
    def __1l11l11111l_opy_(location):
        return bstackl_opy_ (u"ࠧࡀ࠺ࠣᓔ").join(filter(lambda x: isinstance(x, str), location))