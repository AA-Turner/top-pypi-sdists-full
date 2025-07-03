# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
from bstack_utils.bstack1lll111l1l_opy_ import bstack1ll1lll1l11_opy_
bstack1lll111l1l_opy_ = bstack1ll1lll1l11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111l111ll_opy_: Optional[str] = None):
    bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᶕ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l111l11_opy_: str = bstack1lll111l1l_opy_.bstack11ll1l1l1ll_opy_(label)
            start_mark: str = label + bstack1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᶖ")
            end_mark: str = label + bstack1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᶗ")
            result = None
            try:
                if stage.value == STAGE.bstack1l111ll111_opy_.value:
                    bstack1lll111l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll111l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111l111ll_opy_)
                elif stage.value == STAGE.bstack11lllll1_opy_.value:
                    start_mark: str = bstack1ll1l111l11_opy_ + bstack1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᶘ")
                    end_mark: str = bstack1ll1l111l11_opy_ + bstack1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᶙ")
                    bstack1lll111l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll111l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111l111ll_opy_)
            except Exception as e:
                bstack1lll111l1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111l111ll_opy_)
            return result
        return wrapper
    return decorator