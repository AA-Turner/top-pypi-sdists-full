# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
bstack11lllll1l1_opy_ = bstack1lll1l1l11l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll1ll11ll_opy_: Optional[str] = None):
    bstack11l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥṔ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1lll1lll11l_opy_: str = bstack11lllll1l1_opy_.bstack11l1l1111ll_opy_(label)
            start_mark: str = label + bstack11l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤṕ")
            end_mark: str = label + bstack11l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣṖ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1l1ll1ll_opy_.value:
                    bstack11lllll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11lllll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll1ll11ll_opy_)
                elif stage.value == STAGE.bstack1111llll1_opy_.value:
                    start_mark: str = bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦṗ")
                    end_mark: str = bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥṘ")
                    bstack11lllll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11lllll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll1ll11ll_opy_)
            except Exception as e:
                bstack11lllll1l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll1ll11ll_opy_)
            return result
        return wrapper
    return decorator