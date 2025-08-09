# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1111111_opy_ import get_logger
from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
bstack1ll111lll1_opy_ = bstack1ll1ll11111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11ll11ll1_opy_: Optional[str] = None):
    bstack11l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᷬ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111llll1_opy_: str = bstack1ll111lll1_opy_.bstack11ll1l1lll1_opy_(label)
            start_mark: str = label + bstack11l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᷭ")
            end_mark: str = label + bstack11l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᷮ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1l111l1_opy_.value:
                    bstack1ll111lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll111lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11ll11ll1_opy_)
                elif stage.value == STAGE.bstack11lll1l1_opy_.value:
                    start_mark: str = bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᷯ")
                    end_mark: str = bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᷰ")
                    bstack1ll111lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll111lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11ll11ll1_opy_)
            except Exception as e:
                bstack1ll111lll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11ll11ll1_opy_)
            return result
        return wrapper
    return decorator