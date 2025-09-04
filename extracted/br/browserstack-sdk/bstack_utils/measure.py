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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l1111l1_opy_ import get_logger
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
bstack1lllll1ll_opy_ = bstack1lll11111ll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll1l1ll_opy_: Optional[str] = None):
    bstack1111l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᷦ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111l1ll1_opy_: str = bstack1lllll1ll_opy_.bstack11ll1l1ll11_opy_(label)
            start_mark: str = label + bstack1111l1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᷧ")
            end_mark: str = label + bstack1111l1l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᷨ")
            result = None
            try:
                if stage.value == STAGE.bstack1111l11ll_opy_.value:
                    bstack1lllll1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lllll1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll1l1ll_opy_)
                elif stage.value == STAGE.bstack1l1111l1ll_opy_.value:
                    start_mark: str = bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᷩ")
                    end_mark: str = bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᷪ")
                    bstack1lllll1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lllll1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll1l1ll_opy_)
            except Exception as e:
                bstack1lllll1ll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll1l1ll_opy_)
            return result
        return wrapper
    return decorator