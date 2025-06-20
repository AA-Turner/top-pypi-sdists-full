# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
bstack1ll11ll1_opy_ = bstack1ll1l1ll1l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1111llll_opy_: Optional[str] = None):
    bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡅࡧࡦࡳࡷࡧࡴࡰࡴࠣࡸࡴࠦ࡬ࡰࡩࠣࡸ࡭࡫ࠠࡴࡶࡤࡶࡹࠦࡴࡪ࡯ࡨࠤࡴ࡬ࠠࡢࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࡦࡲ࡯࡯ࡩࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺࠠ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡶࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᴴ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11ll111l_opy_: str = bstack1ll11ll1_opy_.bstack11ll1l1ll11_opy_(label)
            start_mark: str = label + bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᴵ")
            end_mark: str = label + bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᴶ")
            result = None
            try:
                if stage.value == STAGE.bstack11l11l11l1_opy_.value:
                    bstack1ll11ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1111llll_opy_)
                elif stage.value == STAGE.bstack1lll11llll_opy_.value:
                    start_mark: str = bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᴷ")
                    end_mark: str = bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᴸ")
                    bstack1ll11ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1111llll_opy_)
            except Exception as e:
                bstack1ll11ll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1111llll_opy_)
            return result
        return wrapper
    return decorator