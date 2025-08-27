# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1l11111_opy_ import get_logger
from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
bstack11l11111_opy_ = bstack1ll1llll11l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11llllll1_opy_: Optional[str] = None):
    bstack1111lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᷡ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11l1l11l_opy_: str = bstack11l11111_opy_.bstack11ll1lllll1_opy_(label)
            start_mark: str = label + bstack1111lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᷢ")
            end_mark: str = label + bstack1111lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᷣ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1l1l111l_opy_.value:
                    bstack11l11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11l11111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11llllll1_opy_)
                elif stage.value == STAGE.bstack11111lll_opy_.value:
                    start_mark: str = bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᷤ")
                    end_mark: str = bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᷥ")
                    bstack11l11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11l11111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11llllll1_opy_)
            except Exception as e:
                bstack11l11111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11llllll1_opy_)
            return result
        return wrapper
    return decorator