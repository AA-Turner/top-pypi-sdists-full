# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1111ll_opy_ import get_logger
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
bstack1ll11l1lll_opy_ = bstack1llll1111l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11llll1lll_opy_: Optional[str] = None):
    bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᶛ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11llll11_opy_: str = bstack1ll11l1lll_opy_.bstack11ll1l1l11l_opy_(label)
            start_mark: str = label + bstack111l111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᶜ")
            end_mark: str = label + bstack111l111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᶝ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll11111l_opy_.value:
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11llll1lll_opy_)
                elif stage.value == STAGE.bstack11l1llll1_opy_.value:
                    start_mark: str = bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᶞ")
                    end_mark: str = bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᶟ")
                    bstack1ll11l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11llll1lll_opy_)
            except Exception as e:
                bstack1ll11l1lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11llll1lll_opy_)
            return result
        return wrapper
    return decorator