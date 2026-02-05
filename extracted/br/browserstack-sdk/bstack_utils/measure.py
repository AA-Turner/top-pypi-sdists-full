# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
bstack11ll1ll111_opy_ = bstack1ll1111ll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll1l111l_opy_: Optional[str] = None):
    bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡉ࡫ࡣࡰࡴࡤࡸࡴࡸࠠࡵࡱࠣࡰࡴ࡭ࠠࡵࡪࡨࠤࡸࡺࡡࡳࡶࠣࡸ࡮ࡳࡥࠡࡱࡩࠤࡦࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠎࠥࠦࠠࠡࡣ࡯ࡳࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨὅ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1lll1llll1_opy_: str = bstack11ll1ll111_opy_.bstack11l1l11ll11_opy_(label)
            start_mark: str = label + bstack11l1ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ὆")
            end_mark: str = label + bstack11l1ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ὇")
            result = None
            try:
                if stage.value == STAGE.bstack11ll1lll1l_opy_.value:
                    bstack11ll1ll111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11ll1ll111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll1l111l_opy_)
                elif stage.value == STAGE.bstack11lll1l1l1_opy_.value:
                    start_mark: str = bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢὈ")
                    end_mark: str = bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨὉ")
                    bstack11ll1ll111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11ll1ll111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll1l111l_opy_)
            except Exception as e:
                bstack11ll1ll111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll1l111l_opy_)
            return result
        return wrapper
    return decorator