# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
bstack1lll1l1ll1_opy_ = bstack1ll1l11l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll11l1l1_opy_: Optional[str] = None):
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⒢")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack11111l11ll_opy_: str = bstack1lll1l1ll1_opy_.bstack1111lll11l1_opy_(label)
            start_mark: str = label + bstack111ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⒣")
            end_mark: str = label + bstack111ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⒤")
            result = None
            try:
                if stage.value == STAGE.bstack1l1111l1l_opy_.value:
                    bstack1lll1l1ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll1l1ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll11l1l1_opy_)
                elif stage.value == STAGE.bstack1l1l1ll111_opy_.value:
                    start_mark: str = bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⒥")
                    end_mark: str = bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⒦")
                    bstack1lll1l1ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll1l1ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll11l1l1_opy_)
            except Exception as e:
                bstack1lll1l1ll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll11l1l1_opy_)
            return result
        return wrapper
    return decorator