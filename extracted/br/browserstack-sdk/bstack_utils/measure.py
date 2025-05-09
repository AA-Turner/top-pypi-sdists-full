# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l11lll1_opy_ import get_logger
from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
bstack1lll1ll1l1_opy_ = bstack1ll1llllll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1111l1ll1_opy_: Optional[str] = None):
    bstack11lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ᰽")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11lll1l1_opy_: str = bstack1lll1ll1l1_opy_.bstack11lllll11ll_opy_(label)
            start_mark: str = label + bstack11lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᰾")
            end_mark: str = label + bstack11lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᰿")
            result = None
            try:
                if stage.value == STAGE.bstack1llll111ll_opy_.value:
                    bstack1lll1ll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll1ll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1111l1ll1_opy_)
                elif stage.value == STAGE.bstack11l111ll_opy_.value:
                    start_mark: str = bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᱀")
                    end_mark: str = bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᱁")
                    bstack1lll1ll1l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll1ll1l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1111l1ll1_opy_)
            except Exception as e:
                bstack1lll1ll1l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1111l1ll1_opy_)
            return result
        return wrapper
    return decorator