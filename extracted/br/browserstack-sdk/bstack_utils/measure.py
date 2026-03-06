# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
bstack1ll1l11ll1_opy_ = bstack1l11l1ll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11ll1l11l1_opy_: Optional[str] = None):
    bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡅࡧࡦࡳࡷࡧࡴࡰࡴࠣࡸࡴࠦ࡬ࡰࡩࠣࡸ࡭࡫ࠠࡴࡶࡤࡶࡹࠦࡴࡪ࡯ࡨࠤࡴ࡬ࠠࡢࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࡦࡲ࡯࡯ࡩࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺࠠ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡶࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤⅣ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1l1llll1_opy_: str = bstack1ll1l11ll1_opy_.bstack11l111111ll_opy_(label)
            start_mark: str = label + bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣⅤ")
            end_mark: str = label + bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢⅥ")
            result = None
            try:
                if stage.value == STAGE.bstack1llllll11l_opy_.value:
                    bstack1ll1l11ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll1l11ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11ll1l11l1_opy_)
                elif stage.value == STAGE.bstack111l1lllll_opy_.value:
                    start_mark: str = bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥⅦ")
                    end_mark: str = bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤⅧ")
                    bstack1ll1l11ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll1l11ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11ll1l11l1_opy_)
            except Exception as e:
                bstack1ll1l11ll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11ll1l11l1_opy_)
            return result
        return wrapper
    return decorator