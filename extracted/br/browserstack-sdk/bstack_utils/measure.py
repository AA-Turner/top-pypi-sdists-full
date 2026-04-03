# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
bstack1111llll1l_opy_ = bstack11l1111l1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1lll1l1ll1_opy_: Optional[str] = None):
    bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⑸")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l111ll1ll_opy_: str = bstack1111llll1l_opy_.bstack1111llll1ll_opy_(label)
            start_mark: str = label + bstack1ll1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⑹")
            end_mark: str = label + bstack1ll1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⑺")
            result = None
            try:
                if stage.value == STAGE.bstack1l11l11l1_opy_.value:
                    bstack1111llll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1111llll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1lll1l1ll1_opy_)
                elif stage.value == STAGE.bstack1ll11l11_opy_.value:
                    start_mark: str = bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⑻")
                    end_mark: str = bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⑼")
                    bstack1111llll1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1111llll1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1lll1l1ll1_opy_)
            except Exception as e:
                bstack1111llll1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1lll1l1ll1_opy_)
            return result
        return wrapper
    return decorator