# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
bstack1ll1lll11l_opy_ = bstack11ll11l1ll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lll1l111_opy_: Optional[str] = None):
    bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡅࡧࡦࡳࡷࡧࡴࡰࡴࠣࡸࡴࠦ࡬ࡰࡩࠣࡸ࡭࡫ࠠࡴࡶࡤࡶࡹࠦࡴࡪ࡯ࡨࠤࡴ࡬ࠠࡢࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࡦࡲ࡯࡯ࡩࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺࠠ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡶࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⊥")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l11ll1ll1_opy_: str = bstack1ll1lll11l_opy_.bstack111l1llllll_opy_(label)
            start_mark: str = label + bstack1ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⊦")
            end_mark: str = label + bstack1ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⊧")
            result = None
            try:
                if stage.value == STAGE.bstack1l111l1l_opy_.value:
                    bstack1ll1lll11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll1lll11l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lll1l111_opy_)
                elif stage.value == STAGE.bstack11111llll_opy_.value:
                    start_mark: str = bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⊨")
                    end_mark: str = bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⊩")
                    bstack1ll1lll11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll1lll11l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lll1l111_opy_)
            except Exception as e:
                bstack1ll1lll11l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lll1l111_opy_)
            return result
        return wrapper
    return decorator