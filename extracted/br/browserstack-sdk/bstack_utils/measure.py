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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
bstack1lll11l1_opy_ = bstack1lll11111l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l11111l1_opy_: Optional[str] = None):
    bstack1l11ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᷤ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111l1lll_opy_: str = bstack1lll11l1_opy_.bstack11lll111111_opy_(label)
            start_mark: str = label + bstack1l11ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᷥ")
            end_mark: str = label + bstack1l11ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᷦ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1lll11ll_opy_.value:
                    bstack1lll11l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll11l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l11111l1_opy_)
                elif stage.value == STAGE.bstack11lllll111_opy_.value:
                    start_mark: str = bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᷧ")
                    end_mark: str = bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᷨ")
                    bstack1lll11l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll11l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l11111l1_opy_)
            except Exception as e:
                bstack1lll11l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l11111l1_opy_)
            return result
        return wrapper
    return decorator