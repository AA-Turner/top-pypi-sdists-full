# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
bstack11lll11l1l_opy_ = bstack111ll11111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l11l111_opy_: Optional[str] = None):
    bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᲒ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1l1l111_opy_: str = bstack11lll11l1l_opy_.bstack1111l1ll1ll_opy_(label)
            start_mark: str = label + bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᲓ")
            end_mark: str = label + bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᲔ")
            result = None
            try:
                if stage.value == STAGE.bstack11ll11ll1l_opy_.value:
                    bstack11lll11l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11lll11l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l11l111_opy_)
                elif stage.value == STAGE.bstack11ll1111_opy_.value:
                    start_mark: str = bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᲕ")
                    end_mark: str = bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᲖ")
                    bstack11lll11l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11lll11l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l11l111_opy_)
            except Exception as e:
                bstack11lll11l1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l11l111_opy_)
            return result
        return wrapper
    return decorator