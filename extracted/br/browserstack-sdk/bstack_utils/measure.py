# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
bstack11ll11ll1l_opy_ = bstack111l1lllll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l111l11l_opy_: Optional[str] = None):
    bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ‰")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l111l111l_opy_: str = bstack11ll11ll1l_opy_.bstack11l11l111l1_opy_(label)
            start_mark: str = label + bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ‱")
            end_mark: str = label + bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ′")
            result = None
            try:
                if stage.value == STAGE.bstack111l1ll11l_opy_.value:
                    bstack11ll11ll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l111l11l_opy_)
                elif stage.value == STAGE.bstack111ll11l1_opy_.value:
                    start_mark: str = bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ″")
                    end_mark: str = bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ‴")
                    bstack11ll11ll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l111l11l_opy_)
            except Exception as e:
                bstack11ll11ll1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l111l11l_opy_)
            return result
        return wrapper
    return decorator