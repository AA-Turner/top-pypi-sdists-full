# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1lll1llll_opy_ import get_logger
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
bstack1l1ll11l1l_opy_ = bstack1ll1ll11ll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11ll1l1l_opy_: Optional[str] = None):
    bstack1ll11ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡅࡧࡦࡳࡷࡧࡴࡰࡴࠣࡸࡴࠦ࡬ࡰࡩࠣࡸ࡭࡫ࠠࡴࡶࡤࡶࡹࠦࡴࡪ࡯ࡨࠤࡴ࡬ࠠࡢࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࡦࡲ࡯࡯ࡩࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺࠠ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡶࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᷪ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111ll1ll_opy_: str = bstack1l1ll11l1l_opy_.bstack11ll1l111ll_opy_(label)
            start_mark: str = label + bstack1ll11ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᷫ")
            end_mark: str = label + bstack1ll11ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᷬ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1ll1111l_opy_.value:
                    bstack1l1ll11l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1ll11l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11ll1l1l_opy_)
                elif stage.value == STAGE.bstack11lll1ll1l_opy_.value:
                    start_mark: str = bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᷭ")
                    end_mark: str = bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᷮ")
                    bstack1l1ll11l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1ll11l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11ll1l1l_opy_)
            except Exception as e:
                bstack1l1ll11l1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11ll1l1l_opy_)
            return result
        return wrapper
    return decorator