# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll111l_opy_ import bstack1llll1lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1l1111lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l1l_opy_,
    bstack1lll11l1111_opy_,
    bstack1lll111l1l1_opy_,
    bstack1l111l1l11l_opy_,
    bstack1ll1lll1l11_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll11ll1l_opy_
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1l1ll1_opy_ import bstack1lll1l111ll_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack11llllllll_opy_
bstack1l1lll1lll1_opy_ = bstack1l1ll11ll1l_opy_()
bstack1l111ll1l1l_opy_ = 1.0
bstack1l1ll1l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᓟ")
bstack11lllll1111_opy_ = bstack1l11ll1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᓠ")
bstack11llll1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᓡ")
bstack11llll1lll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᓢ")
bstack11llll1ll11_opy_ = bstack1l11ll1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᓣ")
_1l1ll1111ll_opy_ = set()
class bstack1llll111l1l_opy_(TestFramework):
    bstack1l1111ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᓤ")
    bstack1l111lll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᓥ")
    bstack1l1111l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᓦ")
    bstack1l1111l111l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᓧ")
    bstack1l1111l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᓨ")
    bstack1l11l1111l1_opy_: bool
    bstack1111111ll1_opy_: bstack11111111ll_opy_  = None
    bstack1lll111111l_opy_ = None
    bstack1l111l1llll_opy_ = [
        bstack1ll1ll11l1l_opy_.BEFORE_ALL,
        bstack1ll1ll11l1l_opy_.AFTER_ALL,
        bstack1ll1ll11l1l_opy_.BEFORE_EACH,
        bstack1ll1ll11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11lllll111l_opy_: Dict[str, str],
        bstack1ll111ll1l1_opy_: List[str]=[bstack1l11ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᓩ")],
        bstack1111111ll1_opy_: bstack11111111ll_opy_=None,
        bstack1lll111111l_opy_=None
    ):
        super().__init__(bstack1ll111ll1l1_opy_, bstack11lllll111l_opy_, bstack1111111ll1_opy_)
        self.bstack1l11l1111l1_opy_ = any(bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᓪ") in item.lower() for item in bstack1ll111ll1l1_opy_)
        self.bstack1lll111111l_opy_ = bstack1lll111111l_opy_
    def track_event(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l1l_opy_.TEST or test_framework_state in bstack1llll111l1l_opy_.bstack1l111l1llll_opy_:
            bstack1l1111lllll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l1l_opy_.NONE:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᓫ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠣࠤᓬ"))
            return
        if not self.bstack1l11l1111l1_opy_:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᓭ") + str(str(self.bstack1ll111ll1l1_opy_)) + bstack1l11ll1_opy_ (u"ࠥࠦᓮ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᓯ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠧࠨᓰ"))
            return
        instance = self.__1l111l1l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᓱ") + str(args) + bstack1l11ll1_opy_ (u"ࠢࠣᓲ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll111l1l_opy_.bstack1l111l1llll_opy_ and test_hook_state == bstack1lll111l1l1_opy_.PRE:
                bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1l111ll1_opy_.value)
                name = str(EVENTS.bstack1l111ll1_opy_.name)+bstack1l11ll1_opy_ (u"ࠣ࠼ࠥᓳ")+str(test_framework_state.name)
                TestFramework.bstack1l111lllll1_opy_(instance, name, bstack1ll111l1lll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᓴ").format(e))
        try:
            if not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l11l11111l_opy_) and test_hook_state == bstack1lll111l1l1_opy_.PRE:
                test = bstack1llll111l1l_opy_.__1l11111lll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᓵ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠦࠧᓶ"))
            if test_framework_state == bstack1ll1ll11l1l_opy_.TEST:
                if test_hook_state == bstack1lll111l1l1_opy_.PRE and not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_):
                    TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᓷ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠨࠢᓸ"))
                elif test_hook_state == bstack1lll111l1l1_opy_.POST and not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_):
                    TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᓹ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠣࠤᓺ"))
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG and test_hook_state == bstack1lll111l1l1_opy_.POST:
                bstack1llll111l1l_opy_.__11llllll111_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT and test_hook_state == bstack1lll111l1l1_opy_.POST:
                self.__11lllllllll_opy_(instance, *args)
                self.__1l1111l1111_opy_(instance)
            elif test_framework_state in bstack1llll111l1l_opy_.bstack1l111l1llll_opy_:
                self.__1l111l1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᓻ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠥࠦᓼ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111ll1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll111l1l_opy_.bstack1l111l1llll_opy_ and test_hook_state == bstack1lll111l1l1_opy_.POST:
                name = str(EVENTS.bstack1l111ll1_opy_.name)+bstack1l11ll1_opy_ (u"ࠦ࠿ࠨᓽ")+str(test_framework_state.name)
                bstack1ll111l1lll_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1lll11111l1_opy_.end(EVENTS.bstack1l111ll1_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᓾ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᓿ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᔀ").format(e))
    def bstack1l1lll11111_opy_(self):
        return self.bstack1l11l1111l1_opy_
    def __1l111ll1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11ll1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᔁ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll111111_opy_(rep, [bstack1l11ll1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᔂ"), bstack1l11ll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᔃ"), bstack1l11ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᔄ"), bstack1l11ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᔅ"), bstack1l11ll1_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᔆ"), bstack1l11ll1_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᔇ")])
        return None
    def __11lllllllll_opy_(self, instance: bstack1lll11l1111_opy_, *args):
        result = self.__1l111ll1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l1l1_opy_ = None
        if result.get(bstack1l11ll1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᔈ"), None) == bstack1l11ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᔉ") and len(args) > 1 and getattr(args[1], bstack1l11ll1_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᔊ"), None) is not None:
            failure = [{bstack1l11ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᔋ"): [args[1].excinfo.exconly(), result.get(bstack1l11ll1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᔌ"), None)]}]
            bstack111111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᔍ") if bstack1l11ll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᔎ") in getattr(args[1].excinfo, bstack1l11ll1_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᔏ"), bstack1l11ll1_opy_ (u"ࠤࠥᔐ")) else bstack1l11ll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᔑ")
        bstack1l11111l111_opy_ = result.get(bstack1l11ll1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᔒ"), TestFramework.bstack1l111111lll_opy_)
        if bstack1l11111l111_opy_ != TestFramework.bstack1l111111lll_opy_:
            TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111l111l1_opy_(instance, {
            TestFramework.bstack1l1l1111l11_opy_: failure,
            TestFramework.bstack1l11111l1ll_opy_: bstack111111l1l1_opy_,
            TestFramework.bstack1l1l1111ll1_opy_: bstack1l11111l111_opy_,
        })
    def __1l111l1l1l1_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
            instance = self.__11llllllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1111lll11_opy_ bstack1l1111llll1_opy_ this to be bstack1l11ll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᔓ")
            if test_framework_state == bstack1ll1ll11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11llllll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᔔ"), None), bstack1l11ll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᔕ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11ll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᔖ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11l1l_opy_(target) if target else None
        return instance
    def __1l111l1l1ll_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l11lll_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1llll111l1l_opy_.bstack1l111lll1ll_opy_, {})
        if not key in bstack1l111l11lll_opy_:
            bstack1l111l11lll_opy_[key] = []
        bstack1l1111ll11l_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1llll111l1l_opy_.bstack1l1111l11l1_opy_, {})
        if not key in bstack1l1111ll11l_opy_:
            bstack1l1111ll11l_opy_[key] = []
        bstack11lllllll1l_opy_ = {
            bstack1llll111l1l_opy_.bstack1l111lll1ll_opy_: bstack1l111l11lll_opy_,
            bstack1llll111l1l_opy_.bstack1l1111l11l1_opy_: bstack1l1111ll11l_opy_,
        }
        if test_hook_state == bstack1lll111l1l1_opy_.PRE:
            hook = {
                bstack1l11ll1_opy_ (u"ࠤ࡮ࡩࡾࠨᔗ"): key,
                TestFramework.bstack1l11111ll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l111ll1111_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l111l111ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111ll1ll_opy_: [],
                TestFramework.bstack1l11111l1l1_opy_: args[1] if len(args) > 1 else bstack1l11ll1_opy_ (u"ࠪࠫᔘ"),
                TestFramework.bstack11lllll11ll_opy_: bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()
            }
            bstack1l111l11lll_opy_[key].append(hook)
            bstack11lllllll1l_opy_[bstack1llll111l1l_opy_.bstack1l1111l111l_opy_] = key
        elif test_hook_state == bstack1lll111l1l1_opy_.POST:
            bstack1l111111111_opy_ = bstack1l111l11lll_opy_.get(key, [])
            hook = bstack1l111111111_opy_.pop() if bstack1l111111111_opy_ else None
            if hook:
                result = self.__1l111ll1ll1_opy_(*args)
                if result:
                    bstack1l111ll11l1_opy_ = result.get(bstack1l11ll1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᔙ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l111ll11l1_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l111ll1111_opy_] = bstack1l111ll11l1_opy_
                hook[TestFramework.bstack11lllllll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lllll11ll_opy_]= bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()
                self.bstack1l111ll1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111111l1l_opy_, [])
                if logs: self.bstack1l1l1ll1ll1_opy_(instance, logs)
                bstack1l1111ll11l_opy_[key].append(hook)
                bstack11lllllll1l_opy_[bstack1llll111l1l_opy_.bstack1l1111l11ll_opy_] = key
        TestFramework.bstack1l111l111l1_opy_(instance, bstack11lllllll1l_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᔚ") + str(bstack1l1111ll11l_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢᔛ"))
    def __11llllllll1_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll111111_opy_(args[0], [bstack1l11ll1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᔜ"), bstack1l11ll1_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᔝ"), bstack1l11ll1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᔞ"), bstack1l11ll1_opy_ (u"ࠥ࡭ࡩࡹࠢᔟ"), bstack1l11ll1_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᔠ"), bstack1l11ll1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᔡ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l11ll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᔢ")) else fixturedef.get(bstack1l11ll1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᔣ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11ll1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᔤ")) else None
        node = request.node if hasattr(request, bstack1l11ll1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᔥ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11ll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᔦ")) else None
        baseid = fixturedef.get(bstack1l11ll1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᔧ"), None) or bstack1l11ll1_opy_ (u"ࠧࠨᔨ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11ll1_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᔩ")):
            target = bstack1llll111l1l_opy_.__1l111l1111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11ll1_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᔪ")) else None
            if target and not TestFramework.bstack1lllll11l1l_opy_(target):
                self.__11llllll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᔫ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠤࠥᔬ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᔭ") + str(target) + bstack1l11ll1_opy_ (u"ࠦࠧᔮ"))
            return None
        instance = TestFramework.bstack1lllll11l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᔯ") + str(target) + bstack1l11ll1_opy_ (u"ࠨࠢᔰ"))
            return None
        bstack1l111l11ll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1llll111l1l_opy_.bstack1l1111ll1l1_opy_, {})
        if os.getenv(bstack1l11ll1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᔱ"), bstack1l11ll1_opy_ (u"ࠣ࠳ࠥᔲ")) == bstack1l11ll1_opy_ (u"ࠤ࠴ࠦᔳ"):
            bstack1l11111l11l_opy_ = bstack1l11ll1_opy_ (u"ࠥ࠾ࠧᔴ").join((scope, fixturename))
            bstack1l1111l1l11_opy_ = datetime.now(tz=timezone.utc)
            bstack11llllll1l1_opy_ = {
                bstack1l11ll1_opy_ (u"ࠦࡰ࡫ࡹࠣᔵ"): bstack1l11111l11l_opy_,
                bstack1l11ll1_opy_ (u"ࠧࡺࡡࡨࡵࠥᔶ"): bstack1llll111l1l_opy_.__1l11111llll_opy_(request.node),
                bstack1l11ll1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᔷ"): fixturedef,
                bstack1l11ll1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᔸ"): scope,
                bstack1l11ll1_opy_ (u"ࠣࡶࡼࡴࡪࠨᔹ"): None,
            }
            try:
                if test_hook_state == bstack1lll111l1l1_opy_.POST and callable(getattr(args[-1], bstack1l11ll1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᔺ"), None)):
                    bstack11llllll1l1_opy_[bstack1l11ll1_opy_ (u"ࠥࡸࡾࡶࡥࠣᔻ")] = TestFramework.bstack1l1ll111ll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111l1l1_opy_.PRE:
                bstack11llllll1l1_opy_[bstack1l11ll1_opy_ (u"ࠦࡺࡻࡩࡥࠤᔼ")] = uuid4().__str__()
                bstack11llllll1l1_opy_[bstack1llll111l1l_opy_.bstack1l111l111ll_opy_] = bstack1l1111l1l11_opy_
            elif test_hook_state == bstack1lll111l1l1_opy_.POST:
                bstack11llllll1l1_opy_[bstack1llll111l1l_opy_.bstack11lllllll11_opy_] = bstack1l1111l1l11_opy_
            if bstack1l11111l11l_opy_ in bstack1l111l11ll1_opy_:
                bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_].update(bstack11llllll1l1_opy_)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᔽ") + str(bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_]) + bstack1l11ll1_opy_ (u"ࠨࠢᔾ"))
            else:
                bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_] = bstack11llllll1l1_opy_
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᔿ") + str(len(bstack1l111l11ll1_opy_)) + bstack1l11ll1_opy_ (u"ࠣࠤᕀ"))
        TestFramework.bstack1llllll1ll1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1111ll1l1_opy_, bstack1l111l11ll1_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᕁ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠥࠦᕂ"))
        return instance
    def __11llllll1ll_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1lll11_opy_.create_context(target)
        ob = bstack1lll11l1111_opy_(ctx, self.bstack1ll111ll1l1_opy_, self.bstack11lllll111l_opy_, test_framework_state)
        TestFramework.bstack1l111l111l1_opy_(ob, {
            TestFramework.bstack1ll1l111l1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1l1l1ll_opy_: context.test_framework_version,
            TestFramework.bstack1l111llll1l_opy_: [],
            bstack1llll111l1l_opy_.bstack1l1111ll1l1_opy_: {},
            bstack1llll111l1l_opy_.bstack1l1111l11l1_opy_: {},
            bstack1llll111l1l_opy_.bstack1l111lll1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllll1ll1_opy_(ob, TestFramework.bstack11lllll11l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllll1ll1_opy_(ob, TestFramework.bstack1ll1111l1l1_opy_, context.platform_index)
        TestFramework.bstack1llllll1lll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᕃ") + str(TestFramework.bstack1llllll1lll_opy_.keys()) + bstack1l11ll1_opy_ (u"ࠧࠨᕄ"))
        return ob
    def bstack1l1l1ll11ll_opy_(self, instance: bstack1lll11l1111_opy_, bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]):
        bstack1l11111ll1l_opy_ = (
            bstack1llll111l1l_opy_.bstack1l1111l111l_opy_
            if bstack1lllll1llll_opy_[1] == bstack1lll111l1l1_opy_.PRE
            else bstack1llll111l1l_opy_.bstack1l1111l11ll_opy_
        )
        hook = bstack1llll111l1l_opy_.bstack1l111111ll1_opy_(instance, bstack1l11111ll1l_opy_)
        entries = hook.get(TestFramework.bstack1l1111ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, []))
        return entries
    def bstack1l1l1ll111l_opy_(self, instance: bstack1lll11l1111_opy_, bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]):
        bstack1l11111ll1l_opy_ = (
            bstack1llll111l1l_opy_.bstack1l1111l111l_opy_
            if bstack1lllll1llll_opy_[1] == bstack1lll111l1l1_opy_.PRE
            else bstack1llll111l1l_opy_.bstack1l1111l11ll_opy_
        )
        bstack1llll111l1l_opy_.bstack1l111llll11_opy_(instance, bstack1l11111ll1l_opy_)
        TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, []).clear()
    def bstack1l111ll1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᕅ")
        global _1l1ll1111ll_opy_
        platform_index = os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕆ")]
        bstack1l1ll11ll11_opy_ = os.path.join(bstack1l1lll1lll1_opy_, (bstack1l1ll1l11ll_opy_ + str(platform_index)), bstack11llll1lll1_opy_)
        if not os.path.exists(bstack1l1ll11ll11_opy_) or not os.path.isdir(bstack1l1ll11ll11_opy_):
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᕇ").format(bstack1l1ll11ll11_opy_))
            return
        logs = hook.get(bstack1l11ll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᕈ"), [])
        with os.scandir(bstack1l1ll11ll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1111ll_opy_:
                    self.logger.info(bstack1l11ll1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᕉ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l11ll1_opy_ (u"ࠦࠧᕊ")
                    log_entry = bstack1ll1lll1l11_opy_(
                        kind=bstack1l11ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᕋ"),
                        message=bstack1l11ll1_opy_ (u"ࠨࠢᕌ"),
                        level=bstack1l11ll1_opy_ (u"ࠢࠣᕍ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1l111l_opy_=entry.stat().st_size,
                        bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᕎ"),
                        bstack111l111_opy_=os.path.abspath(entry.path),
                        bstack1l1111111ll_opy_=hook.get(TestFramework.bstack1l11111ll11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1111ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᕏ")]
        bstack11lllll1l1l_opy_ = os.path.join(bstack1l1lll1lll1_opy_, (bstack1l1ll1l11ll_opy_ + str(platform_index)), bstack11llll1lll1_opy_, bstack11llll1ll11_opy_)
        if not os.path.exists(bstack11lllll1l1l_opy_) or not os.path.isdir(bstack11lllll1l1l_opy_):
            self.logger.info(bstack1l11ll1_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᕐ").format(bstack11lllll1l1l_opy_))
        else:
            self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᕑ").format(bstack11lllll1l1l_opy_))
            with os.scandir(bstack11lllll1l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1111ll_opy_:
                        self.logger.info(bstack1l11ll1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᕒ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l11ll1_opy_ (u"ࠨࠢᕓ")
                        log_entry = bstack1ll1lll1l11_opy_(
                            kind=bstack1l11ll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᕔ"),
                            message=bstack1l11ll1_opy_ (u"ࠣࠤᕕ"),
                            level=bstack1l11ll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᕖ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1l111l_opy_=entry.stat().st_size,
                            bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᕗ"),
                            bstack111l111_opy_=os.path.abspath(entry.path),
                            bstack1l1l1ll1l1l_opy_=hook.get(TestFramework.bstack1l11111ll11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1111ll_opy_.add(abs_path)
        hook[bstack1l11ll1_opy_ (u"ࠦࡱࡵࡧࡴࠤᕘ")] = logs
    def bstack1l1l1ll1ll1_opy_(
        self,
        bstack1l1lll11lll_opy_: bstack1lll11l1111_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᕙ"))
        req.platform_index = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1111l1l1_opy_)
        req.execution_context.hash = str(bstack1l1lll11lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll11lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll11lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1l111l1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1l1l1l1l1ll_opy_)
            log_entry.uuid = entry.bstack1l1111111ll_opy_
            log_entry.test_framework_state = bstack1l1lll11lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11ll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᕚ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l11ll1_opy_ (u"ࠢࠣᕛ")
            if entry.kind == bstack1l11ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᕜ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1l111l_opy_
                log_entry.file_path = entry.bstack111l111_opy_
        def bstack1l1l1ll1lll_opy_():
            bstack1l11ll1ll_opy_ = datetime.now()
            try:
                self.bstack1lll111111l_opy_.LogCreatedEvent(req)
                bstack1l1lll11lll_opy_.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᕝ"), datetime.now() - bstack1l11ll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11ll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᕞ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    def __1l1111l1111_opy_(self, instance) -> None:
        bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᕟ")
        bstack11lllllll1l_opy_ = {bstack1l11ll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᕠ"): bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l111l111l1_opy_(instance, bstack11lllllll1l_opy_)
    @staticmethod
    def bstack1l111111ll1_opy_(instance: bstack1lll11l1111_opy_, bstack1l11111ll1l_opy_: str):
        bstack1l1111ll111_opy_ = (
            bstack1llll111l1l_opy_.bstack1l1111l11l1_opy_
            if bstack1l11111ll1l_opy_ == bstack1llll111l1l_opy_.bstack1l1111l11ll_opy_
            else bstack1llll111l1l_opy_.bstack1l111lll1ll_opy_
        )
        bstack1l1111lll1l_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l11111ll1l_opy_, None)
        bstack1l111l1lll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l1111ll111_opy_, None) if bstack1l1111lll1l_opy_ else None
        return (
            bstack1l111l1lll1_opy_[bstack1l1111lll1l_opy_][-1]
            if isinstance(bstack1l111l1lll1_opy_, dict) and len(bstack1l111l1lll1_opy_.get(bstack1l1111lll1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111llll11_opy_(instance: bstack1lll11l1111_opy_, bstack1l11111ll1l_opy_: str):
        hook = bstack1llll111l1l_opy_.bstack1l111111ll1_opy_(instance, bstack1l11111ll1l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111ll1ll_opy_, []).clear()
    @staticmethod
    def __11llllll111_opy_(instance: bstack1lll11l1111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11ll1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᕡ"), None)):
            return
        if os.getenv(bstack1l11ll1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᕢ"), bstack1l11ll1_opy_ (u"ࠣ࠳ࠥᕣ")) != bstack1l11ll1_opy_ (u"ࠤ࠴ࠦᕤ"):
            bstack1llll111l1l_opy_.logger.warning(bstack1l11ll1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᕥ"))
            return
        bstack1l111lll11l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᕦ"): (bstack1llll111l1l_opy_.bstack1l1111l111l_opy_, bstack1llll111l1l_opy_.bstack1l111lll1ll_opy_),
            bstack1l11ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᕧ"): (bstack1llll111l1l_opy_.bstack1l1111l11ll_opy_, bstack1llll111l1l_opy_.bstack1l1111l11l1_opy_),
        }
        for when in (bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᕨ"), bstack1l11ll1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᕩ"), bstack1l11ll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᕪ")):
            bstack11lllll1lll_opy_ = args[1].get_records(when)
            if not bstack11lllll1lll_opy_:
                continue
            records = [
                bstack1ll1lll1l11_opy_(
                    kind=TestFramework.bstack1l1ll1l1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11ll1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᕫ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11ll1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᕬ")) and r.created
                        else None
                    ),
                )
                for r in bstack11lllll1lll_opy_
                if isinstance(getattr(r, bstack1l11ll1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᕭ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111l11l1l_opy_, bstack1l1111ll111_opy_ = bstack1l111lll11l_opy_.get(when, (None, None))
            bstack1l1111l1ll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l111l11l1l_opy_, None) if bstack1l111l11l1l_opy_ else None
            bstack1l111l1lll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l1111ll111_opy_, None) if bstack1l1111l1ll1_opy_ else None
            if isinstance(bstack1l111l1lll1_opy_, dict) and len(bstack1l111l1lll1_opy_.get(bstack1l1111l1ll1_opy_, [])) > 0:
                hook = bstack1l111l1lll1_opy_[bstack1l1111l1ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111ll1ll_opy_ in hook:
                    hook[TestFramework.bstack1l1111ll1ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11111lll1_opy_(test) -> Dict[str, Any]:
        bstack111lllll1_opy_ = bstack1llll111l1l_opy_.__1l111l1111l_opy_(test.location) if hasattr(test, bstack1l11ll1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᕮ")) else getattr(test, bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᕯ"), None)
        test_name = test.name if hasattr(test, bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᕰ")) else None
        bstack1l111l1l111_opy_ = test.fspath.strpath if hasattr(test, bstack1l11ll1_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᕱ")) and test.fspath else None
        if not bstack111lllll1_opy_ or not test_name or not bstack1l111l1l111_opy_:
            return None
        code = None
        if hasattr(test, bstack1l11ll1_opy_ (u"ࠤࡲࡦ࡯ࠨᕲ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11llll1llll_opy_ = []
        try:
            bstack11llll1llll_opy_ = bstack11llllllll_opy_.bstack1111llllll_opy_(test)
        except:
            bstack1llll111l1l_opy_.logger.warning(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᕳ"))
        return {
            TestFramework.bstack1ll111ll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l11111l_opy_: bstack111lllll1_opy_,
            TestFramework.bstack1ll11llll1l_opy_: test_name,
            TestFramework.bstack1l1l1l111l1_opy_: getattr(test, bstack1l11ll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᕴ"), None),
            TestFramework.bstack1l111111l11_opy_: bstack1l111l1l111_opy_,
            TestFramework.bstack1l111ll111l_opy_: bstack1llll111l1l_opy_.__1l11111llll_opy_(test),
            TestFramework.bstack11lllll1ll1_opy_: code,
            TestFramework.bstack1l1l1111ll1_opy_: TestFramework.bstack1l111111lll_opy_,
            TestFramework.bstack1l11l1l11l1_opy_: bstack111lllll1_opy_,
            TestFramework.bstack11llll1l1ll_opy_: bstack11llll1llll_opy_
        }
    @staticmethod
    def __1l11111llll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l11ll1_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᕵ"), [])
            markers.extend([getattr(m, bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᕶ"), None) for m in own_markers if getattr(m, bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᕷ"), None)])
            current = getattr(current, bstack1l11ll1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᕸ"), None)
        return markers
    @staticmethod
    def __1l111l1111l_opy_(location):
        return bstack1l11ll1_opy_ (u"ࠤ࠽࠾ࠧᕹ").join(filter(lambda x: isinstance(x, str), location))