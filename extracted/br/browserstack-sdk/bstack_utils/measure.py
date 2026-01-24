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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack111llll1ll_opy_ import get_logger
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
bstack11l111111l_opy_ = bstack11ll111lll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1l111l_opy_: Optional[str] = None):
    bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧἽ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1111lll_opy_: str = bstack11l111111l_opy_.bstack11l1ll11111_opy_(label)
            start_mark: str = label + bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦἾ")
            end_mark: str = label + bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥἿ")
            result = None
            try:
                if stage.value == STAGE.bstack1l111ll1_opy_.value:
                    bstack11l111111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11l111111l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1l111l_opy_)
                elif stage.value == STAGE.bstack1111lll11_opy_.value:
                    start_mark: str = bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨὀ")
                    end_mark: str = bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧὁ")
                    bstack11l111111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11l111111l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1l111l_opy_)
            except Exception as e:
                bstack11l111111l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1l111l_opy_)
            return result
        return wrapper
    return decorator