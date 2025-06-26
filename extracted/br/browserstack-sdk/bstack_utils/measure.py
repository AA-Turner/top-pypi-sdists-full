# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l1l1l111_opy_ import get_logger
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
bstack1l1ll1111_opy_ = bstack1llll11lll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11llll111l_opy_: Optional[str] = None):
    bstack11ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᵕ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11l111ll_opy_: str = bstack1l1ll1111_opy_.bstack11ll1l1llll_opy_(label)
            start_mark: str = label + bstack11ll1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᵖ")
            end_mark: str = label + bstack11ll1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᵗ")
            result = None
            try:
                if stage.value == STAGE.bstack111l1l1l1_opy_.value:
                    bstack1l1ll1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11llll111l_opy_)
                elif stage.value == STAGE.bstack11l1lll1l1_opy_.value:
                    start_mark: str = bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᵘ")
                    end_mark: str = bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᵙ")
                    bstack1l1ll1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11llll111l_opy_)
            except Exception as e:
                bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11llll111l_opy_)
            return result
        return wrapper
    return decorator