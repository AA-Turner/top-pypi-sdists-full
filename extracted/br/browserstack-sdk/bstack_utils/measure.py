# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1llllll1ll_opy_ import get_logger
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
bstack1llll1l1_opy_ = bstack1lll1llll1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11llll11l_opy_: Optional[str] = None):
    bstack1llllll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᰴ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll111l1_opy_: str = bstack1llll1l1_opy_.bstack11lllll1lll_opy_(label)
            start_mark: str = label + bstack1llllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᰵ")
            end_mark: str = label + bstack1llllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᰶ")
            result = None
            try:
                if stage.value == STAGE.bstack1lll11l1ll_opy_.value:
                    bstack1llll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1llll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11llll11l_opy_)
                elif stage.value == STAGE.bstack1l1ll11l1_opy_.value:
                    start_mark: str = bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᰷")
                    end_mark: str = bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᰸")
                    bstack1llll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1llll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11llll11l_opy_)
            except Exception as e:
                bstack1llll1l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11llll11l_opy_)
            return result
        return wrapper
    return decorator