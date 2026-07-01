# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.performance_tester import PerformanceTester
performance_tester = PerformanceTester()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lllll111_opy_: Optional[str] = None, bstack1ll1111ll1_opy_: bool = False):
    bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏ࡚ࠦࠠࠡࠢ࡬ࡪࡴࠠࡳࡧࡢࡶࡦ࡯ࡳࡦ࠿ࡗࡶࡺ࡫ࠬࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡸࡴࡤࡴࡵ࡫ࡤࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡥࡷ࡫ࠠࡳࡧࡦࡳࡷࡪࡥࡥࠢࡤࡲࡩࠐࠠࠡࠢࠣࡸ࡭࡫࡮ࠡࡴࡨ࠱ࡷࡧࡩࡴࡧࡧࠤࡸࡵࠠࡤࡣ࡯ࡰࡪࡸࡳࠡࠪࡤࡲࡩࠦࡡ࡯ࡻࠣࡳࡺࡺࡥࡳࠢࡺࡶࡦࡶࡰࡦࡴࡶ࠭ࠥࡵࡢࡴࡧࡵࡺࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨ࠲ࠏࠦࠠࠡࠢࡇࡩ࡫ࡧࡵ࡭ࡶࠣࡊࡦࡲࡳࡦࠢࡳࡶࡪࡹࡥࡳࡸࡨࡷࠥࡲࡥࡨࡣࡦࡽࠥࡹࡷࡢ࡮࡯ࡳࡼ࠳ࡡ࡯ࡦ࠰ࡶࡪࡺࡵࡳࡰ࠰ࡒࡴࡴࡥࠡࡤࡨ࡬ࡦࡼࡩࡰࡷࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⡭")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            random_label: str = performance_tester.bstack11111ll1111_opy_(label)
            start_mark: str = label + bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⡮")
            end_mark: str = label + bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⡯")
            result = None
            try:
                if stage.value == STAGE.bstack1l11ll1l1l_opy_.value:
                    performance_tester.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    performance_tester.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lllll111_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = random_label + bstack1l1llll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⡰")
                    end_mark: str = random_label + bstack1l1llll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⡱")
                    performance_tester.mark(start_mark)
                    result = func(*args, **kwargs)
                    performance_tester.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lllll111_opy_)
            except Exception as e:
                performance_tester.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lllll111_opy_)
                if bstack1ll1111ll1_opy_:
                    raise
            return result
        return wrapper
    return decorator