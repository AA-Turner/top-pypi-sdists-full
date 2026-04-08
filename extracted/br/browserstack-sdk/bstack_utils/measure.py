# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
bstack111111lll1_opy_ = bstack11lll11111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111l11l1l1_opy_: Optional[str] = None):
    bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⑸")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1l111lll_opy_: str = bstack111111lll1_opy_.bstack1111lllll1l_opy_(label)
            start_mark: str = label + bstack111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⑹")
            end_mark: str = label + bstack111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⑺")
            result = None
            try:
                if stage.value == STAGE.bstack1lllll1l1_opy_.value:
                    bstack111111lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack111111lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111l11l1l1_opy_)
                elif stage.value == STAGE.bstack1l1l11ll11_opy_.value:
                    start_mark: str = bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⑻")
                    end_mark: str = bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⑼")
                    bstack111111lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack111111lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111l11l1l1_opy_)
            except Exception as e:
                bstack111111lll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111l11l1l1_opy_)
            return result
        return wrapper
    return decorator