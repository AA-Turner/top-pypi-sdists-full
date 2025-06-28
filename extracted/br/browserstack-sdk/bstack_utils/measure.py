# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11lll1ll_opy_ import get_logger
from bstack_utils.bstack1l11l1llll_opy_ import bstack1lll11l1l11_opy_
bstack1l11l1llll_opy_ = bstack1lll11l1l11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1llll1ll1l_opy_: Optional[str] = None):
    bstack1l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᵕ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111l1lll_opy_: str = bstack1l11l1llll_opy_.bstack11lll111ll1_opy_(label)
            start_mark: str = label + bstack1l1ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᵖ")
            end_mark: str = label + bstack1l1ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᵗ")
            result = None
            try:
                if stage.value == STAGE.bstack111lll111_opy_.value:
                    bstack1l11l1llll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l11l1llll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1llll1ll1l_opy_)
                elif stage.value == STAGE.bstack1l1ll11ll1_opy_.value:
                    start_mark: str = bstack1ll111l1lll_opy_ + bstack1l1ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᵘ")
                    end_mark: str = bstack1ll111l1lll_opy_ + bstack1l1ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᵙ")
                    bstack1l11l1llll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l11l1llll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1llll1ll1l_opy_)
            except Exception as e:
                bstack1l11l1llll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1llll1ll1l_opy_)
            return result
        return wrapper
    return decorator