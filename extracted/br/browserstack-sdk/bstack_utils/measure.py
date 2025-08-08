# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack111111111_opy_ import get_logger
from bstack_utils.bstack11ll11ll1l_opy_ import bstack1lll1l1ll1l_opy_
bstack11ll11ll1l_opy_ = bstack1lll1l1ll1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lll11111_opy_: Optional[str] = None):
    bstack1ll1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᷫ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11l11l1l_opy_: str = bstack11ll11ll1l_opy_.bstack11ll1l1ll1l_opy_(label)
            start_mark: str = label + bstack1ll1ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᷬ")
            end_mark: str = label + bstack1ll1ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᷭ")
            result = None
            try:
                if stage.value == STAGE.bstack1lll1llll_opy_.value:
                    bstack11ll11ll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lll11111_opy_)
                elif stage.value == STAGE.bstack1l1l111lll_opy_.value:
                    start_mark: str = bstack1ll11l11l1l_opy_ + bstack1ll1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᷮ")
                    end_mark: str = bstack1ll11l11l1l_opy_ + bstack1ll1ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᷯ")
                    bstack11ll11ll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lll11111_opy_)
            except Exception as e:
                bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lll11111_opy_)
            return result
        return wrapper
    return decorator