# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack1lllll11lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll11_opy_ import bstack1l111l1l111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1lllll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1ll1llll1ll_opy_,
    bstack1l111ll111l_opy_,
    bstack1lll1l1llll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll1l11l1_opy_
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1l11l_opy_ import bstack1ll1lll11l1_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
bstack1l1ll1l111l_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l111ll1111_opy_ = 1.0
bstack1l1l1lll111_opy_ = bstack1111l1l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᓡ")
bstack11lllll1111_opy_ = bstack1111l1l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᓢ")
bstack11llll1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᓣ")
bstack11llll1lll1_opy_ = bstack1111l1l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᓤ")
bstack11lllll111l_opy_ = bstack1111l1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᓥ")
_1l1l1ll11ll_opy_ = set()
class bstack1lll111llll_opy_(TestFramework):
    bstack1l11l1111l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᓦ")
    bstack1l11111111l_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᓧ")
    bstack1l11111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᓨ")
    bstack1l111l11ll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᓩ")
    bstack1l1111l1111_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᓪ")
    bstack1l11111llll_opy_: bool
    bstack1111111ll1_opy_: bstack1111111lll_opy_  = None
    bstack1ll1ll11l11_opy_ = None
    bstack11llllll111_opy_ = [
        bstack1lll1lllll1_opy_.BEFORE_ALL,
        bstack1lll1lllll1_opy_.AFTER_ALL,
        bstack1lll1lllll1_opy_.BEFORE_EACH,
        bstack1lll1lllll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11111l111_opy_: Dict[str, str],
        bstack1ll11ll1111_opy_: List[str]=[bstack1111l1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᓫ")],
        bstack1111111ll1_opy_: bstack1111111lll_opy_=None,
        bstack1ll1ll11l11_opy_=None
    ):
        super().__init__(bstack1ll11ll1111_opy_, bstack1l11111l111_opy_, bstack1111111ll1_opy_)
        self.bstack1l11111llll_opy_ = any(bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᓬ") in item.lower() for item in bstack1ll11ll1111_opy_)
        self.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_
    def track_event(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1lllll1_opy_.TEST or test_framework_state in bstack1lll111llll_opy_.bstack11llllll111_opy_:
            bstack1l111l1l111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1lllll1_opy_.NONE:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᓭ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠥࠦᓮ"))
            return
        if not self.bstack1l11111llll_opy_:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᓯ") + str(str(self.bstack1ll11ll1111_opy_)) + bstack1111l1l_opy_ (u"ࠧࠨᓰ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᓱ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠢࠣᓲ"))
            return
        instance = self.__1l1111l111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᓳ") + str(args) + bstack1111l1l_opy_ (u"ࠤࠥᓴ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll111llll_opy_.bstack11llllll111_opy_ and test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1l1l1_opy_.value)
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1111l1l_opy_ (u"ࠥ࠾ࠧᓵ")+str(test_framework_state.name)
                TestFramework.bstack1l1111l1ll1_opy_(instance, name, bstack1ll111l1ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᓶ").format(e))
        try:
            if not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l111l111l1_opy_) and test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                test = bstack1lll111llll_opy_.__1l111lll111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᓷ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠨࠢᓸ"))
            if test_framework_state == bstack1lll1lllll1_opy_.TEST:
                if test_hook_state == bstack1ll1llll1ll_opy_.PRE and not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᓹ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠣࠤᓺ"))
                elif test_hook_state == bstack1ll1llll1ll_opy_.POST and not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᓻ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠥࠦᓼ"))
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                bstack1lll111llll_opy_.__1l1111l1l1l_opy_(instance, *args)
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                self.__1l1111111l1_opy_(instance, *args)
                self.__1l111l1l11l_opy_(instance)
            elif test_framework_state in bstack1lll111llll_opy_.bstack11llllll111_opy_:
                self.__1l111l11111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᓽ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠧࠨᓾ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lllll1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll111llll_opy_.bstack11llllll111_opy_ and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1111l1l_opy_ (u"ࠨ࠺ࠣᓿ")+str(test_framework_state.name)
                bstack1ll111l1ll1_opy_ = TestFramework.bstack1l111l1111l_opy_(instance, name)
                bstack1lll11111ll_opy_.end(EVENTS.bstack11l1l1l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᔀ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᔁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᔂ").format(e))
    def bstack1l1l1llll11_opy_(self):
        return self.bstack1l11111llll_opy_
    def __1l11111ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111l1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᔃ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1l1lll1_opy_(rep, [bstack1111l1l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᔄ"), bstack1111l1l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᔅ"), bstack1111l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᔆ"), bstack1111l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᔇ"), bstack1111l1l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᔈ"), bstack1111l1l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᔉ")])
        return None
    def __1l1111111l1_opy_(self, instance: bstack1lll1l1ll1l_opy_, *args):
        result = self.__1l11111ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l1ll_opy_ = None
        if result.get(bstack1111l1l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᔊ"), None) == bstack1111l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᔋ") and len(args) > 1 and getattr(args[1], bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᔌ"), None) is not None:
            failure = [{bstack1111l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᔍ"): [args[1].excinfo.exconly(), result.get(bstack1111l1l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᔎ"), None)]}]
            bstack111111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᔏ") if bstack1111l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔐ") in getattr(args[1].excinfo, bstack1111l1l_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᔑ"), bstack1111l1l_opy_ (u"ࠦࠧᔒ")) else bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᔓ")
        bstack11lllllll1l_opy_ = result.get(bstack1111l1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᔔ"), TestFramework.bstack1l111lllll1_opy_)
        if bstack11lllllll1l_opy_ != TestFramework.bstack1l111lllll1_opy_:
            TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l111111_opy_(instance, {
            TestFramework.bstack1l1l11111l1_opy_: failure,
            TestFramework.bstack1l1111111ll_opy_: bstack111111l1ll_opy_,
            TestFramework.bstack1l1l1111l1l_opy_: bstack11lllllll1l_opy_,
        })
    def __1l1111l111l_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1lllll1_opy_.SETUP_FIXTURE:
            instance = self.__11lllll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11llllll1l1_opy_ bstack1l111ll1lll_opy_ this to be bstack1111l1l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᔕ")
            if test_framework_state == bstack1lll1lllll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111111l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1111l1l_opy_ (u"ࠣࡰࡲࡨࡪࠨᔖ"), None), bstack1111l1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᔗ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111l1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᔘ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll1111l_opy_(target) if target else None
        return instance
    def __1l111l11111_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111l11l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1lll111llll_opy_.bstack1l11111111l_opy_, {})
        if not key in bstack1l1111l11l1_opy_:
            bstack1l1111l11l1_opy_[key] = []
        bstack1l111l111ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1lll111llll_opy_.bstack1l11111l1ll_opy_, {})
        if not key in bstack1l111l111ll_opy_:
            bstack1l111l111ll_opy_[key] = []
        bstack1l111l1lll1_opy_ = {
            bstack1lll111llll_opy_.bstack1l11111111l_opy_: bstack1l1111l11l1_opy_,
            bstack1lll111llll_opy_.bstack1l11111l1ll_opy_: bstack1l111l111ll_opy_,
        }
        if test_hook_state == bstack1ll1llll1ll_opy_.PRE:
            hook = {
                bstack1111l1l_opy_ (u"ࠦࡰ࡫ࡹࠣᔙ"): key,
                TestFramework.bstack1l111111111_opy_: uuid4().__str__(),
                TestFramework.bstack1l111l1l1ll_opy_: TestFramework.bstack1l1111ll111_opy_,
                TestFramework.bstack1l1111lll1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l11111l_opy_: [],
                TestFramework.bstack1l111ll11l1_opy_: args[1] if len(args) > 1 else bstack1111l1l_opy_ (u"ࠬ࠭ᔚ"),
                TestFramework.bstack1l111111l11_opy_: bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()
            }
            bstack1l1111l11l1_opy_[key].append(hook)
            bstack1l111l1lll1_opy_[bstack1lll111llll_opy_.bstack1l111l11ll1_opy_] = key
        elif test_hook_state == bstack1ll1llll1ll_opy_.POST:
            bstack11lllll1ll1_opy_ = bstack1l1111l11l1_opy_.get(key, [])
            hook = bstack11lllll1ll1_opy_.pop() if bstack11lllll1ll1_opy_ else None
            if hook:
                result = self.__1l11111ll11_opy_(*args)
                if result:
                    bstack1l111l1llll_opy_ = result.get(bstack1111l1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᔛ"), TestFramework.bstack1l1111ll111_opy_)
                    if bstack1l111l1llll_opy_ != TestFramework.bstack1l1111ll111_opy_:
                        hook[TestFramework.bstack1l111l1l1ll_opy_] = bstack1l111l1llll_opy_
                hook[TestFramework.bstack11lllll1l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111111l11_opy_]= bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()
                self.bstack1l11111l11l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1111l11ll_opy_, [])
                if logs: self.bstack1l1l1ll1lll_opy_(instance, logs)
                bstack1l111l111ll_opy_[key].append(hook)
                bstack1l111l1lll1_opy_[bstack1lll111llll_opy_.bstack1l1111l1111_opy_] = key
        TestFramework.bstack1l11l111111_opy_(instance, bstack1l111l1lll1_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᔜ") + str(bstack1l111l111ll_opy_) + bstack1111l1l_opy_ (u"ࠣࠤᔝ"))
    def __11lllll1lll_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1l1lll1_opy_(args[0], [bstack1111l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᔞ"), bstack1111l1l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᔟ"), bstack1111l1l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᔠ"), bstack1111l1l_opy_ (u"ࠧ࡯ࡤࡴࠤᔡ"), bstack1111l1l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᔢ"), bstack1111l1l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᔣ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1111l1l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᔤ")) else fixturedef.get(bstack1111l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᔥ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111l1l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᔦ")) else None
        node = request.node if hasattr(request, bstack1111l1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᔧ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111l1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᔨ")) else None
        baseid = fixturedef.get(bstack1111l1l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᔩ"), None) or bstack1111l1l_opy_ (u"ࠢࠣᔪ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111l1l_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᔫ")):
            target = bstack1lll111llll_opy_.__1l111llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111l1l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᔬ")) else None
            if target and not TestFramework.bstack1lllll1111l_opy_(target):
                self.__1l111111l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᔭ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠦࠧᔮ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᔯ") + str(target) + bstack1111l1l_opy_ (u"ࠨࠢᔰ"))
            return None
        instance = TestFramework.bstack1lllll1111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᔱ") + str(target) + bstack1111l1l_opy_ (u"ࠣࠤᔲ"))
            return None
        bstack1l1111ll1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1lll111llll_opy_.bstack1l11l1111l1_opy_, {})
        if os.getenv(bstack1111l1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᔳ"), bstack1111l1l_opy_ (u"ࠥ࠵ࠧᔴ")) == bstack1111l1l_opy_ (u"ࠦ࠶ࠨᔵ"):
            bstack11lllllll11_opy_ = bstack1111l1l_opy_ (u"ࠧࡀࠢᔶ").join((scope, fixturename))
            bstack1l1111ll11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l11l1l_opy_ = {
                bstack1111l1l_opy_ (u"ࠨ࡫ࡦࡻࠥᔷ"): bstack11lllllll11_opy_,
                bstack1111l1l_opy_ (u"ࠢࡵࡣࡪࡷࠧᔸ"): bstack1lll111llll_opy_.__1l11111l1l1_opy_(request.node),
                bstack1111l1l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᔹ"): fixturedef,
                bstack1111l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᔺ"): scope,
                bstack1111l1l_opy_ (u"ࠥࡸࡾࡶࡥࠣᔻ"): None,
            }
            try:
                if test_hook_state == bstack1ll1llll1ll_opy_.POST and callable(getattr(args[-1], bstack1111l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᔼ"), None)):
                    bstack1l111l11l1l_opy_[bstack1111l1l_opy_ (u"ࠧࡺࡹࡱࡧࠥᔽ")] = TestFramework.bstack1l1ll11lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                bstack1l111l11l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᔾ")] = uuid4().__str__()
                bstack1l111l11l1l_opy_[bstack1lll111llll_opy_.bstack1l1111lll1l_opy_] = bstack1l1111ll11l_opy_
            elif test_hook_state == bstack1ll1llll1ll_opy_.POST:
                bstack1l111l11l1l_opy_[bstack1lll111llll_opy_.bstack11lllll1l1l_opy_] = bstack1l1111ll11l_opy_
            if bstack11lllllll11_opy_ in bstack1l1111ll1l1_opy_:
                bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_].update(bstack1l111l11l1l_opy_)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᔿ") + str(bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_]) + bstack1111l1l_opy_ (u"ࠣࠤᕀ"))
            else:
                bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_] = bstack1l111l11l1l_opy_
                self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᕁ") + str(len(bstack1l1111ll1l1_opy_)) + bstack1111l1l_opy_ (u"ࠥࠦᕂ"))
        TestFramework.bstack1lllllllll1_opy_(instance, bstack1lll111llll_opy_.bstack1l11l1111l1_opy_, bstack1l1111ll1l1_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᕃ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠧࠨᕄ"))
        return instance
    def __1l111111l1l_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll11lll_opy_.create_context(target)
        ob = bstack1lll1l1ll1l_opy_(ctx, self.bstack1ll11ll1111_opy_, self.bstack1l11111l111_opy_, test_framework_state)
        TestFramework.bstack1l11l111111_opy_(ob, {
            TestFramework.bstack1ll111lll11_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll11llll_opy_: context.test_framework_version,
            TestFramework.bstack1l111ll1ll1_opy_: [],
            bstack1lll111llll_opy_.bstack1l11l1111l1_opy_: {},
            bstack1lll111llll_opy_.bstack1l11111l1ll_opy_: {},
            bstack1lll111llll_opy_.bstack1l11111111l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack11llllllll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack1ll11l1ll1l_opy_, context.platform_index)
        TestFramework.bstack1111111111_opy_[ctx.id] = ob
        self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᕅ") + str(TestFramework.bstack1111111111_opy_.keys()) + bstack1111l1l_opy_ (u"ࠢࠣᕆ"))
        return ob
    def bstack1l1ll1l11ll_opy_(self, instance: bstack1lll1l1ll1l_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]):
        bstack1l111lll1l1_opy_ = (
            bstack1lll111llll_opy_.bstack1l111l11ll1_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1ll1llll1ll_opy_.PRE
            else bstack1lll111llll_opy_.bstack1l1111l1111_opy_
        )
        hook = bstack1lll111llll_opy_.bstack1l111ll1l11_opy_(instance, bstack1l111lll1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l11111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, []))
        return entries
    def bstack1l1ll1ll1l1_opy_(self, instance: bstack1lll1l1ll1l_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]):
        bstack1l111lll1l1_opy_ = (
            bstack1lll111llll_opy_.bstack1l111l11ll1_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1ll1llll1ll_opy_.PRE
            else bstack1lll111llll_opy_.bstack1l1111l1111_opy_
        )
        bstack1lll111llll_opy_.bstack1l11111lll1_opy_(instance, bstack1l111lll1l1_opy_)
        TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, []).clear()
    def bstack1l11111l11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᕇ")
        global _1l1l1ll11ll_opy_
        platform_index = os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᕈ")]
        bstack1l1lll1l1ll_opy_ = os.path.join(bstack1l1ll1l111l_opy_, (bstack1l1l1lll111_opy_ + str(platform_index)), bstack11llll1lll1_opy_)
        if not os.path.exists(bstack1l1lll1l1ll_opy_) or not os.path.isdir(bstack1l1lll1l1ll_opy_):
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᕉ").format(bstack1l1lll1l1ll_opy_))
            return
        logs = hook.get(bstack1111l1l_opy_ (u"ࠦࡱࡵࡧࡴࠤᕊ"), [])
        with os.scandir(bstack1l1lll1l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1l1ll11ll_opy_:
                    self.logger.info(bstack1111l1l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᕋ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111l1l_opy_ (u"ࠨࠢᕌ")
                    log_entry = bstack1lll1l1llll_opy_(
                        kind=bstack1111l1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᕍ"),
                        message=bstack1111l1l_opy_ (u"ࠣࠤᕎ"),
                        level=bstack1111l1l_opy_ (u"ࠤࠥᕏ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l1ll1111_opy_=entry.stat().st_size,
                        bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᕐ"),
                        bstack1l1llll_opy_=os.path.abspath(entry.path),
                        bstack1l11l1111ll_opy_=hook.get(TestFramework.bstack1l111111111_opy_)
                    )
                    logs.append(log_entry)
                    _1l1l1ll11ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᕑ")]
        bstack1l111l1ll11_opy_ = os.path.join(bstack1l1ll1l111l_opy_, (bstack1l1l1lll111_opy_ + str(platform_index)), bstack11llll1lll1_opy_, bstack11lllll111l_opy_)
        if not os.path.exists(bstack1l111l1ll11_opy_) or not os.path.isdir(bstack1l111l1ll11_opy_):
            self.logger.info(bstack1111l1l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᕒ").format(bstack1l111l1ll11_opy_))
        else:
            self.logger.info(bstack1111l1l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᕓ").format(bstack1l111l1ll11_opy_))
            with os.scandir(bstack1l111l1ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1l1ll11ll_opy_:
                        self.logger.info(bstack1111l1l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᕔ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111l1l_opy_ (u"ࠣࠤᕕ")
                        log_entry = bstack1lll1l1llll_opy_(
                            kind=bstack1111l1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᕖ"),
                            message=bstack1111l1l_opy_ (u"ࠥࠦᕗ"),
                            level=bstack1111l1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᕘ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l1ll1111_opy_=entry.stat().st_size,
                            bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᕙ"),
                            bstack1l1llll_opy_=os.path.abspath(entry.path),
                            bstack1l1lll11ll1_opy_=hook.get(TestFramework.bstack1l111111111_opy_)
                        )
                        logs.append(log_entry)
                        _1l1l1ll11ll_opy_.add(abs_path)
        hook[bstack1111l1l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᕚ")] = logs
    def bstack1l1l1ll1lll_opy_(
        self,
        bstack1l1l1l1ll1l_opy_: bstack1lll1l1ll1l_opy_,
        entries: List[bstack1lll1l1llll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᕛ"))
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll11l1ll1l_opy_)
        req.execution_context.hash = str(bstack1l1l1l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll111lll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1l1ll11llll_opy_)
            log_entry.uuid = entry.bstack1l11l1111ll_opy_
            log_entry.test_framework_state = bstack1l1l1l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᕜ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1111l1l_opy_ (u"ࠤࠥᕝ")
            if entry.kind == bstack1111l1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᕞ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1ll1111_opy_
                log_entry.file_path = entry.bstack1l1llll_opy_
        def bstack1l1ll1lll1l_opy_():
            bstack1ll1l1lll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11l11_opy_.LogCreatedEvent(req)
                bstack1l1l1l1ll1l_opy_.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᕟ"), datetime.now() - bstack1ll1l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l1l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᕠ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1lll1l_opy_)
    def __1l111l1l11l_opy_(self, instance) -> None:
        bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᕡ")
        bstack1l111l1lll1_opy_ = {bstack1111l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᕢ"): bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l111111_opy_(instance, bstack1l111l1lll1_opy_)
    @staticmethod
    def bstack1l111ll1l11_opy_(instance: bstack1lll1l1ll1l_opy_, bstack1l111lll1l1_opy_: str):
        bstack1l111111lll_opy_ = (
            bstack1lll111llll_opy_.bstack1l11111l1ll_opy_
            if bstack1l111lll1l1_opy_ == bstack1lll111llll_opy_.bstack1l1111l1111_opy_
            else bstack1lll111llll_opy_.bstack1l11111111l_opy_
        )
        bstack11lllll11ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111lll1l1_opy_, None)
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111111lll_opy_, None) if bstack11lllll11ll_opy_ else None
        return (
            bstack1l111l1ll1l_opy_[bstack11lllll11ll_opy_][-1]
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack11lllll11ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111lll1_opy_(instance: bstack1lll1l1ll1l_opy_, bstack1l111lll1l1_opy_: str):
        hook = bstack1lll111llll_opy_.bstack1l111ll1l11_opy_(instance, bstack1l111lll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l11111l_opy_, []).clear()
    @staticmethod
    def __1l1111l1l1l_opy_(instance: bstack1lll1l1ll1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111l1l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᕣ"), None)):
            return
        if os.getenv(bstack1111l1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᕤ"), bstack1111l1l_opy_ (u"ࠥ࠵ࠧᕥ")) != bstack1111l1l_opy_ (u"ࠦ࠶ࠨᕦ"):
            bstack1lll111llll_opy_.logger.warning(bstack1111l1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᕧ"))
            return
        bstack1l111l1l1l1_opy_ = {
            bstack1111l1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᕨ"): (bstack1lll111llll_opy_.bstack1l111l11ll1_opy_, bstack1lll111llll_opy_.bstack1l11111111l_opy_),
            bstack1111l1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᕩ"): (bstack1lll111llll_opy_.bstack1l1111l1111_opy_, bstack1lll111llll_opy_.bstack1l11111l1ll_opy_),
        }
        for when in (bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕪ"), bstack1111l1l_opy_ (u"ࠤࡦࡥࡱࡲࠢᕫ"), bstack1111l1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᕬ")):
            bstack1l111lll11l_opy_ = args[1].get_records(when)
            if not bstack1l111lll11l_opy_:
                continue
            records = [
                bstack1lll1l1llll_opy_(
                    kind=TestFramework.bstack1l1lll11l11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111l1l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᕭ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111l1l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᕮ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111lll11l_opy_
                if isinstance(getattr(r, bstack1111l1l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᕯ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111llllll_opy_, bstack1l111111lll_opy_ = bstack1l111l1l1l1_opy_.get(when, (None, None))
            bstack1l111llll11_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111llllll_opy_, None) if bstack1l111llllll_opy_ else None
            bstack1l111l1ll1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111111lll_opy_, None) if bstack1l111llll11_opy_ else None
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack1l111llll11_opy_, [])) > 0:
                hook = bstack1l111l1ll1l_opy_[bstack1l111llll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l11111l_opy_ in hook:
                    hook[TestFramework.bstack1l11l11111l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111lll111_opy_(test) -> Dict[str, Any]:
        bstack1111ll11l_opy_ = bstack1lll111llll_opy_.__1l111llll1l_opy_(test.location) if hasattr(test, bstack1111l1l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᕰ")) else getattr(test, bstack1111l1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᕱ"), None)
        test_name = test.name if hasattr(test, bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᕲ")) else None
        bstack1l1111lllll_opy_ = test.fspath.strpath if hasattr(test, bstack1111l1l_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᕳ")) and test.fspath else None
        if not bstack1111ll11l_opy_ or not test_name or not bstack1l1111lllll_opy_:
            return None
        code = None
        if hasattr(test, bstack1111l1l_opy_ (u"ࠦࡴࡨࡪࠣᕴ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11llll1ll11_opy_ = []
        try:
            bstack11llll1ll11_opy_ = bstack1ll11lll1_opy_.bstack1111lll111_opy_(test)
        except:
            bstack1lll111llll_opy_.logger.warning(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᕵ"))
        return {
            TestFramework.bstack1ll1111ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l111l1_opy_: bstack1111ll11l_opy_,
            TestFramework.bstack1ll111l1l11_opy_: test_name,
            TestFramework.bstack1l1l1l11lll_opy_: getattr(test, bstack1111l1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᕶ"), None),
            TestFramework.bstack1l111l11lll_opy_: bstack1l1111lllll_opy_,
            TestFramework.bstack11lllll11l1_opy_: bstack1lll111llll_opy_.__1l11111l1l1_opy_(test),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l1l1111l1l_opy_: TestFramework.bstack1l111lllll1_opy_,
            TestFramework.bstack1l11l1l111l_opy_: bstack1111ll11l_opy_,
            TestFramework.bstack11llll1llll_opy_: bstack11llll1ll11_opy_
        }
    @staticmethod
    def __1l11111l1l1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1111l1l_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᕷ"), [])
            markers.extend([getattr(m, bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᕸ"), None) for m in own_markers if getattr(m, bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᕹ"), None)])
            current = getattr(current, bstack1111l1l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᕺ"), None)
        return markers
    @staticmethod
    def __1l111llll1l_opy_(location):
        return bstack1111l1l_opy_ (u"ࠦ࠿ࡀࠢᕻ").join(filter(lambda x: isinstance(x, str), location))