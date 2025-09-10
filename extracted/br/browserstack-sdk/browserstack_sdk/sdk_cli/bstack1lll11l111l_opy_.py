# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1111111111_opy_
from browserstack_sdk.sdk_cli.utils.bstack11ll1lll11_opy_ import bstack1l1111lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l1ll11_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1ll1lllll11_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1l1l1ll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1lll1l1_opy_
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.bstack111ll11111_opy_ import bstack11lllllll1_opy_
bstack1l1ll1llll1_opy_ = bstack1l1l1lll1l1_opy_()
bstack11lllll1ll1_opy_ = 1.0
bstack1l1ll11111l_opy_ = bstack1ll11ll_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᓠ")
bstack11llll1llll_opy_ = bstack1ll11ll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᓡ")
bstack11llll1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᓢ")
bstack11llll1lll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᓣ")
bstack11llll1ll1l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᓤ")
_1l1ll1l111l_opy_ = set()
class bstack1ll1llll111_opy_(TestFramework):
    bstack1l1111l1111_opy_ = bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᓥ")
    bstack1l1111ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᓦ")
    bstack1l111l1l111_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᓧ")
    bstack1l111l11l11_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᓨ")
    bstack1l1111l1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᓩ")
    bstack1l111lll1ll_opy_: bool
    bstack1111111ll1_opy_: bstack11111111ll_opy_  = None
    bstack1ll1llllll1_opy_ = None
    bstack11lllll11ll_opy_ = [
        bstack1lll1l1ll11_opy_.BEFORE_ALL,
        bstack1lll1l1ll11_opy_.AFTER_ALL,
        bstack1lll1l1ll11_opy_.BEFORE_EACH,
        bstack1lll1l1ll11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111ll1lll_opy_: Dict[str, str],
        bstack1ll1l111l11_opy_: List[str]=[bstack1ll11ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᓪ")],
        bstack1111111ll1_opy_: bstack11111111ll_opy_=None,
        bstack1ll1llllll1_opy_=None
    ):
        super().__init__(bstack1ll1l111l11_opy_, bstack1l111ll1lll_opy_, bstack1111111ll1_opy_)
        self.bstack1l111lll1ll_opy_ = any(bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᓫ") in item.lower() for item in bstack1ll1l111l11_opy_)
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l1ll11_opy_.TEST or test_framework_state in bstack1ll1llll111_opy_.bstack11lllll11ll_opy_:
            bstack1l1111lll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l1ll11_opy_.NONE:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᓬ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠤࠥᓭ"))
            return
        if not self.bstack1l111lll1ll_opy_:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᓮ") + str(str(self.bstack1ll1l111l11_opy_)) + bstack1ll11ll_opy_ (u"ࠦࠧᓯ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᓰ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠨࠢᓱ"))
            return
        instance = self.__1l111l11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᓲ") + str(args) + bstack1ll11ll_opy_ (u"ࠣࠤᓳ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1llll111_opy_.bstack11lllll11ll_opy_ and test_hook_state == bstack1ll1lllll11_opy_.PRE:
                bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1ll11l111l_opy_.value)
                name = str(EVENTS.bstack1ll11l111l_opy_.name)+bstack1ll11ll_opy_ (u"ࠤ࠽ࠦᓴ")+str(test_framework_state.name)
                TestFramework.bstack1l1111ll11l_opy_(instance, name, bstack1ll111ll1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᓵ").format(e))
        try:
            if not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1111l1l11_opy_) and test_hook_state == bstack1ll1lllll11_opy_.PRE:
                test = bstack1ll1llll111_opy_.__11lllllll1l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᓶ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠧࠨᓷ"))
            if test_framework_state == bstack1lll1l1ll11_opy_.TEST:
                if test_hook_state == bstack1ll1lllll11_opy_.PRE and not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1lll11111_opy_):
                    TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᓸ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠢࠣᓹ"))
                elif test_hook_state == bstack1ll1lllll11_opy_.POST and not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll111lll_opy_):
                    TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1ll111lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᓺ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠤࠥᓻ"))
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG and test_hook_state == bstack1ll1lllll11_opy_.POST:
                bstack1ll1llll111_opy_.__1l1111ll1ll_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG_REPORT and test_hook_state == bstack1ll1lllll11_opy_.POST:
                self.__1l111l1llll_opy_(instance, *args)
                self.__1l11111lll1_opy_(instance)
            elif test_framework_state in bstack1ll1llll111_opy_.bstack11lllll11ll_opy_:
                self.__1l111l1111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᓼ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠦࠧᓽ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11llllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1llll111_opy_.bstack11lllll11ll_opy_ and test_hook_state == bstack1ll1lllll11_opy_.POST:
                name = str(EVENTS.bstack1ll11l111l_opy_.name)+bstack1ll11ll_opy_ (u"ࠧࡀࠢᓾ")+str(test_framework_state.name)
                bstack1ll111ll1ll_opy_ = TestFramework.bstack11lllllll11_opy_(instance, name)
                bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1ll11l111l_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᓿ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᔀ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᔁ").format(e))
    def bstack1l1ll1l11l1_opy_(self):
        return self.bstack1l111lll1ll_opy_
    def __1l1111l1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll11ll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᔂ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1ll1111_opy_(rep, [bstack1ll11ll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᔃ"), bstack1ll11ll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᔄ"), bstack1ll11ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᔅ"), bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᔆ"), bstack1ll11ll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᔇ"), bstack1ll11ll_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᔈ")])
        return None
    def __1l111l1llll_opy_(self, instance: bstack1lll11ll1l1_opy_, *args):
        result = self.__1l1111l1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l11l_opy_ = None
        if result.get(bstack1ll11ll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᔉ"), None) == bstack1ll11ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᔊ") and len(args) > 1 and getattr(args[1], bstack1ll11ll_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᔋ"), None) is not None:
            failure = [{bstack1ll11ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᔌ"): [args[1].excinfo.exconly(), result.get(bstack1ll11ll_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᔍ"), None)]}]
            bstack111111l11l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᔎ") if bstack1ll11ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᔏ") in getattr(args[1].excinfo, bstack1ll11ll_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᔐ"), bstack1ll11ll_opy_ (u"ࠥࠦᔑ")) else bstack1ll11ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔒ")
        bstack1l1111111ll_opy_ = result.get(bstack1ll11ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᔓ"), TestFramework.bstack1l1111llll1_opy_)
        if bstack1l1111111ll_opy_ != TestFramework.bstack1l1111llll1_opy_:
            TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111l1lll_opy_(instance, {
            TestFramework.bstack1l1l111111l_opy_: failure,
            TestFramework.bstack1l111llll1l_opy_: bstack111111l11l_opy_,
            TestFramework.bstack1l1l11111l1_opy_: bstack1l1111111ll_opy_,
        })
    def __1l111l11lll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l1ll11_opy_.SETUP_FIXTURE:
            instance = self.__11lllll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11111l1l1_opy_ bstack1l111ll11ll_opy_ this to be bstack1ll11ll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᔔ")
            if test_framework_state == bstack1lll1l1ll11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111llll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᔕ"), None), bstack1ll11ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᔖ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll11ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᔗ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llllllll11_opy_(target) if target else None
        return instance
    def __1l111l1111l_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11111l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1ll1llll111_opy_.bstack1l1111ll1l1_opy_, {})
        if not key in bstack1l11l11111l_opy_:
            bstack1l11l11111l_opy_[key] = []
        bstack1l11111111l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1ll1llll111_opy_.bstack1l111l1l111_opy_, {})
        if not key in bstack1l11111111l_opy_:
            bstack1l11111111l_opy_[key] = []
        bstack1l1111l11l1_opy_ = {
            bstack1ll1llll111_opy_.bstack1l1111ll1l1_opy_: bstack1l11l11111l_opy_,
            bstack1ll1llll111_opy_.bstack1l111l1l111_opy_: bstack1l11111111l_opy_,
        }
        if test_hook_state == bstack1ll1lllll11_opy_.PRE:
            hook = {
                bstack1ll11ll_opy_ (u"ࠥ࡯ࡪࡿࠢᔘ"): key,
                TestFramework.bstack1l111ll11l1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l111111_opy_: TestFramework.bstack1l111lll1l1_opy_,
                TestFramework.bstack1l111ll1111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11llllll111_opy_: [],
                TestFramework.bstack1l111111l1l_opy_: args[1] if len(args) > 1 else bstack1ll11ll_opy_ (u"ࠫࠬᔙ"),
                TestFramework.bstack1l111l1l11l_opy_: bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()
            }
            bstack1l11l11111l_opy_[key].append(hook)
            bstack1l1111l11l1_opy_[bstack1ll1llll111_opy_.bstack1l111l11l11_opy_] = key
        elif test_hook_state == bstack1ll1lllll11_opy_.POST:
            bstack1l111l111ll_opy_ = bstack1l11l11111l_opy_.get(key, [])
            hook = bstack1l111l111ll_opy_.pop() if bstack1l111l111ll_opy_ else None
            if hook:
                result = self.__1l1111l1ll1_opy_(*args)
                if result:
                    bstack1l111l1ll1l_opy_ = result.get(bstack1ll11ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᔚ"), TestFramework.bstack1l111lll1l1_opy_)
                    if bstack1l111l1ll1l_opy_ != TestFramework.bstack1l111lll1l1_opy_:
                        hook[TestFramework.bstack1l11l111111_opy_] = bstack1l111l1ll1l_opy_
                hook[TestFramework.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1l11l_opy_]= bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()
                self.bstack1l11111llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111111111_opy_, [])
                if logs: self.bstack1l1ll11l111_opy_(instance, logs)
                bstack1l11111111l_opy_[key].append(hook)
                bstack1l1111l11l1_opy_[bstack1ll1llll111_opy_.bstack1l1111l1l1l_opy_] = key
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l1111l11l1_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᔛ") + str(bstack1l11111111l_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣᔜ"))
    def __11lllll1lll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1ll1111_opy_(args[0], [bstack1ll11ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᔝ"), bstack1ll11ll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᔞ"), bstack1ll11ll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᔟ"), bstack1ll11ll_opy_ (u"ࠦ࡮ࡪࡳࠣᔠ"), bstack1ll11ll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᔡ"), bstack1ll11ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᔢ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll11ll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᔣ")) else fixturedef.get(bstack1ll11ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᔤ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll11ll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᔥ")) else None
        node = request.node if hasattr(request, bstack1ll11ll_opy_ (u"ࠥࡲࡴࡪࡥࠣᔦ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll11ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔧ")) else None
        baseid = fixturedef.get(bstack1ll11ll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᔨ"), None) or bstack1ll11ll_opy_ (u"ࠨࠢᔩ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll11ll_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᔪ")):
            target = bstack1ll1llll111_opy_.__1l1111lllll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll11ll_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᔫ")) else None
            if target and not TestFramework.bstack1llllllll11_opy_(target):
                self.__1l111llll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᔬ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠥࠦᔭ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᔮ") + str(target) + bstack1ll11ll_opy_ (u"ࠧࠨᔯ"))
            return None
        instance = TestFramework.bstack1llllllll11_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᔰ") + str(target) + bstack1ll11ll_opy_ (u"ࠢࠣᔱ"))
            return None
        bstack11lllll1l1l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1ll1llll111_opy_.bstack1l1111l1111_opy_, {})
        if os.getenv(bstack1ll11ll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᔲ"), bstack1ll11ll_opy_ (u"ࠤ࠴ࠦᔳ")) == bstack1ll11ll_opy_ (u"ࠥ࠵ࠧᔴ"):
            bstack1l111lll11l_opy_ = bstack1ll11ll_opy_ (u"ࠦ࠿ࠨᔵ").join((scope, fixturename))
            bstack1l111l1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l111l1_opy_ = {
                bstack1ll11ll_opy_ (u"ࠧࡱࡥࡺࠤᔶ"): bstack1l111lll11l_opy_,
                bstack1ll11ll_opy_ (u"ࠨࡴࡢࡩࡶࠦᔷ"): bstack1ll1llll111_opy_.__1l111ll1l11_opy_(request.node),
                bstack1ll11ll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᔸ"): fixturedef,
                bstack1ll11ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᔹ"): scope,
                bstack1ll11ll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᔺ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lllll11_opy_.POST and callable(getattr(args[-1], bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᔻ"), None)):
                    bstack1l111l111l1_opy_[bstack1ll11ll_opy_ (u"ࠦࡹࡿࡰࡦࠤᔼ")] = TestFramework.bstack1l1ll1lllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lllll11_opy_.PRE:
                bstack1l111l111l1_opy_[bstack1ll11ll_opy_ (u"ࠧࡻࡵࡪࡦࠥᔽ")] = uuid4().__str__()
                bstack1l111l111l1_opy_[bstack1ll1llll111_opy_.bstack1l111ll1111_opy_] = bstack1l111l1lll1_opy_
            elif test_hook_state == bstack1ll1lllll11_opy_.POST:
                bstack1l111l111l1_opy_[bstack1ll1llll111_opy_.bstack1l111l11111_opy_] = bstack1l111l1lll1_opy_
            if bstack1l111lll11l_opy_ in bstack11lllll1l1l_opy_:
                bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_].update(bstack1l111l111l1_opy_)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᔾ") + str(bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_]) + bstack1ll11ll_opy_ (u"ࠢࠣᔿ"))
            else:
                bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_] = bstack1l111l111l1_opy_
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᕀ") + str(len(bstack11lllll1l1l_opy_)) + bstack1ll11ll_opy_ (u"ࠤࠥᕁ"))
        TestFramework.bstack1llll1l1lll_opy_(instance, bstack1ll1llll111_opy_.bstack1l1111l1111_opy_, bstack11lllll1l1l_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᕂ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠦࠧᕃ"))
        return instance
    def __1l111llll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111111111_opy_.create_context(target)
        ob = bstack1lll11ll1l1_opy_(ctx, self.bstack1ll1l111l11_opy_, self.bstack1l111ll1lll_opy_, test_framework_state)
        TestFramework.bstack1l1111l1lll_opy_(ob, {
            TestFramework.bstack1ll11ll111l_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1l1111_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1l1ll_opy_: [],
            bstack1ll1llll111_opy_.bstack1l1111l1111_opy_: {},
            bstack1ll1llll111_opy_.bstack1l111l1l111_opy_: {},
            bstack1ll1llll111_opy_.bstack1l1111ll1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll1l1lll_opy_(ob, TestFramework.bstack1l1111lll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll1l1lll_opy_(ob, TestFramework.bstack1ll1111lll1_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᕄ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack1ll11ll_opy_ (u"ࠨࠢᕅ"))
        return ob
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1lll11ll1l1_opy_, bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]):
        bstack1l111l1ll11_opy_ = (
            bstack1ll1llll111_opy_.bstack1l111l11l11_opy_
            if bstack1llll1ll1l1_opy_[1] == bstack1ll1lllll11_opy_.PRE
            else bstack1ll1llll111_opy_.bstack1l1111l1l1l_opy_
        )
        hook = bstack1ll1llll111_opy_.bstack1l111l11ll1_opy_(instance, bstack1l111l1ll11_opy_)
        entries = hook.get(TestFramework.bstack11llllll111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []))
        return entries
    def bstack1l1l1ll11l1_opy_(self, instance: bstack1lll11ll1l1_opy_, bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]):
        bstack1l111l1ll11_opy_ = (
            bstack1ll1llll111_opy_.bstack1l111l11l11_opy_
            if bstack1llll1ll1l1_opy_[1] == bstack1ll1lllll11_opy_.PRE
            else bstack1ll1llll111_opy_.bstack1l1111l1l1l_opy_
        )
        bstack1ll1llll111_opy_.bstack11lllll111l_opy_(instance, bstack1l111l1ll11_opy_)
        TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []).clear()
    def bstack1l11111llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll11ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᕆ")
        global _1l1ll1l111l_opy_
        platform_index = os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᕇ")]
        bstack1l1ll1l1l11_opy_ = os.path.join(bstack1l1ll1llll1_opy_, (bstack1l1ll11111l_opy_ + str(platform_index)), bstack11llll1lll1_opy_)
        if not os.path.exists(bstack1l1ll1l1l11_opy_) or not os.path.isdir(bstack1l1ll1l1l11_opy_):
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢᕈ").format(bstack1l1ll1l1l11_opy_))
            return
        logs = hook.get(bstack1ll11ll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᕉ"), [])
        with os.scandir(bstack1l1ll1l1l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l111l_opy_:
                    self.logger.info(bstack1ll11ll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᕊ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll11ll_opy_ (u"ࠧࠨᕋ")
                    log_entry = bstack1ll1l1l1ll1_opy_(
                        kind=bstack1ll11ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᕌ"),
                        message=bstack1ll11ll_opy_ (u"ࠢࠣᕍ"),
                        level=bstack1ll11ll_opy_ (u"ࠣࠤᕎ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l1lll11l_opy_=entry.stat().st_size,
                        bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᕏ"),
                        bstack11l111l_opy_=os.path.abspath(entry.path),
                        bstack11lllll1l11_opy_=hook.get(TestFramework.bstack1l111ll11l1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l111l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᕐ")]
        bstack11llllll1ll_opy_ = os.path.join(bstack1l1ll1llll1_opy_, (bstack1l1ll11111l_opy_ + str(platform_index)), bstack11llll1lll1_opy_, bstack11llll1ll1l_opy_)
        if not os.path.exists(bstack11llllll1ll_opy_) or not os.path.isdir(bstack11llllll1ll_opy_):
            self.logger.info(bstack1ll11ll_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᕑ").format(bstack11llllll1ll_opy_))
        else:
            self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᕒ").format(bstack11llllll1ll_opy_))
            with os.scandir(bstack11llllll1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstack1ll11ll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᕓ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll11ll_opy_ (u"ࠢࠣᕔ")
                        log_entry = bstack1ll1l1l1ll1_opy_(
                            kind=bstack1ll11ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᕕ"),
                            message=bstack1ll11ll_opy_ (u"ࠤࠥᕖ"),
                            level=bstack1ll11ll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᕗ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l1lll11l_opy_=entry.stat().st_size,
                            bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᕘ"),
                            bstack11l111l_opy_=os.path.abspath(entry.path),
                            bstack1l1ll11l1ll_opy_=hook.get(TestFramework.bstack1l111ll11l1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l111l_opy_.add(abs_path)
        hook[bstack1ll11ll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᕙ")] = logs
    def bstack1l1ll11l111_opy_(
        self,
        bstack1l1ll1ll1l1_opy_: bstack1lll11ll1l1_opy_,
        entries: List[bstack1ll1l1l1ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᕚ"))
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll1111lll1_opy_)
        req.execution_context.hash = str(bstack1l1ll1ll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll1ll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll1ll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll11ll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1l1ll1l1111_opy_)
            log_entry.uuid = entry.bstack11lllll1l11_opy_
            log_entry.test_framework_state = bstack1l1ll1ll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᕛ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll11ll_opy_ (u"ࠣࠤᕜ")
            if entry.kind == bstack1ll11ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᕝ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1lll11l_opy_
                log_entry.file_path = entry.bstack11l111l_opy_
        def bstack1l1ll1l11ll_opy_():
            bstack1ll111l11_opy_ = datetime.now()
            try:
                self.bstack1ll1llllll1_opy_.LogCreatedEvent(req)
                bstack1l1ll1ll1l1_opy_.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᕞ"), datetime.now() - bstack1ll111l11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᕟ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1l11ll_opy_)
    def __1l11111lll1_opy_(self, instance) -> None:
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᕠ")
        bstack1l1111l11l1_opy_ = {bstack1ll11ll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᕡ"): bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l1111l11l1_opy_)
    @staticmethod
    def bstack1l111l11ll1_opy_(instance: bstack1lll11ll1l1_opy_, bstack1l111l1ll11_opy_: str):
        bstack1l11111l11l_opy_ = (
            bstack1ll1llll111_opy_.bstack1l111l1l111_opy_
            if bstack1l111l1ll11_opy_ == bstack1ll1llll111_opy_.bstack1l1111l1l1l_opy_
            else bstack1ll1llll111_opy_.bstack1l1111ll1l1_opy_
        )
        bstack1l111111lll_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l111l1ll11_opy_, None)
        bstack1l111ll1ll1_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l11111l11l_opy_, None) if bstack1l111111lll_opy_ else None
        return (
            bstack1l111ll1ll1_opy_[bstack1l111111lll_opy_][-1]
            if isinstance(bstack1l111ll1ll1_opy_, dict) and len(bstack1l111ll1ll1_opy_.get(bstack1l111111lll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lllll111l_opy_(instance: bstack1lll11ll1l1_opy_, bstack1l111l1ll11_opy_: str):
        hook = bstack1ll1llll111_opy_.bstack1l111l11ll1_opy_(instance, bstack1l111l1ll11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11llllll111_opy_, []).clear()
    @staticmethod
    def __1l1111ll1ll_opy_(instance: bstack1lll11ll1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll11ll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᕢ"), None)):
            return
        if os.getenv(bstack1ll11ll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᕣ"), bstack1ll11ll_opy_ (u"ࠤ࠴ࠦᕤ")) != bstack1ll11ll_opy_ (u"ࠥ࠵ࠧᕥ"):
            bstack1ll1llll111_opy_.logger.warning(bstack1ll11ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᕦ"))
            return
        bstack1l1111l111l_opy_ = {
            bstack1ll11ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᕧ"): (bstack1ll1llll111_opy_.bstack1l111l11l11_opy_, bstack1ll1llll111_opy_.bstack1l1111ll1l1_opy_),
            bstack1ll11ll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᕨ"): (bstack1ll1llll111_opy_.bstack1l1111l1l1l_opy_, bstack1ll1llll111_opy_.bstack1l111l1l111_opy_),
        }
        for when in (bstack1ll11ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᕩ"), bstack1ll11ll_opy_ (u"ࠣࡥࡤࡰࡱࠨᕪ"), bstack1ll11ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕫ")):
            bstack1l11111l111_opy_ = args[1].get_records(when)
            if not bstack1l11111l111_opy_:
                continue
            records = [
                bstack1ll1l1l1ll1_opy_(
                    kind=TestFramework.bstack1l1ll1l1lll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll11ll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᕬ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll11ll_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᕭ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11111l111_opy_
                if isinstance(getattr(r, bstack1ll11ll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᕮ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll111l_opy_, bstack1l11111l11l_opy_ = bstack1l1111l111l_opy_.get(when, (None, None))
            bstack1l111ll1l1l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l111ll111l_opy_ else None
            bstack1l111ll1ll1_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l11111l11l_opy_, None) if bstack1l111ll1l1l_opy_ else None
            if isinstance(bstack1l111ll1ll1_opy_, dict) and len(bstack1l111ll1ll1_opy_.get(bstack1l111ll1l1l_opy_, [])) > 0:
                hook = bstack1l111ll1ll1_opy_[bstack1l111ll1l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11llllll111_opy_ in hook:
                    hook[TestFramework.bstack11llllll111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11lllllll1l_opy_(test) -> Dict[str, Any]:
        bstack1l1l1ll1l1_opy_ = bstack1ll1llll111_opy_.__1l1111lllll_opy_(test.location) if hasattr(test, bstack1ll11ll_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᕯ")) else getattr(test, bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᕰ"), None)
        test_name = test.name if hasattr(test, bstack1ll11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᕱ")) else None
        bstack1l111l1l1l1_opy_ = test.fspath.strpath if hasattr(test, bstack1ll11ll_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤᕲ")) and test.fspath else None
        if not bstack1l1l1ll1l1_opy_ or not test_name or not bstack1l111l1l1l1_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll11ll_opy_ (u"ࠥࡳࡧࡰࠢᕳ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lllll1111_opy_ = []
        try:
            bstack11lllll1111_opy_ = bstack11lllllll1_opy_.bstack111l11111l_opy_(test)
        except:
            bstack1ll1llll111_opy_.logger.warning(bstack1ll11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧᕴ"))
        return {
            TestFramework.bstack1ll11l1111l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111l1l11_opy_: bstack1l1l1ll1l1_opy_,
            TestFramework.bstack1ll11l111l1_opy_: test_name,
            TestFramework.bstack1l1l1l11ll1_opy_: getattr(test, bstack1ll11ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᕵ"), None),
            TestFramework.bstack11lllllllll_opy_: bstack1l111l1l1l1_opy_,
            TestFramework.bstack1l111llllll_opy_: bstack1ll1llll111_opy_.__1l111ll1l11_opy_(test),
            TestFramework.bstack1l1111111l1_opy_: code,
            TestFramework.bstack1l1l11111l1_opy_: TestFramework.bstack1l1111llll1_opy_,
            TestFramework.bstack1l11l1l11l1_opy_: bstack1l1l1ll1l1_opy_,
            TestFramework.bstack11llll1l1ll_opy_: bstack11lllll1111_opy_
        }
    @staticmethod
    def __1l111ll1l11_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll11ll_opy_ (u"ࠨ࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠦᕶ"), [])
            markers.extend([getattr(m, bstack1ll11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᕷ"), None) for m in own_markers if getattr(m, bstack1ll11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᕸ"), None)])
            current = getattr(current, bstack1ll11ll_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᕹ"), None)
        return markers
    @staticmethod
    def __1l1111lllll_opy_(location):
        return bstack1ll11ll_opy_ (u"ࠥ࠾࠿ࠨᕺ").join(filter(lambda x: isinstance(x, str), location))