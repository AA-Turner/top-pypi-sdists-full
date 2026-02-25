# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
bstack111lll111l_opy_ = bstack11ll1l1l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l111l11l_opy_: Optional[str] = None):
    bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ※")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1l1l1111_opy_: str = bstack111lll111l_opy_.bstack11l11lll1l1_opy_(label)
            start_mark: str = label + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ‼")
            end_mark: str = label + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ‽")
            result = None
            try:
                if stage.value == STAGE.bstack11111l11l_opy_.value:
                    bstack111lll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack111lll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l111l11l_opy_)
                elif stage.value == STAGE.bstack1l11l1l11l_opy_.value:
                    start_mark: str = bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ‾")
                    end_mark: str = bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ‿")
                    bstack111lll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack111lll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l111l11l_opy_)
            except Exception as e:
                bstack111lll111l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l111l11l_opy_)
            return result
        return wrapper
    return decorator