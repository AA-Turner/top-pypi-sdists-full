# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11111llll_opy_ import get_logger
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
bstack1l111lll_opy_ = bstack1ll1llll111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lll1llll_opy_: Optional[str] = None):
    bstack1l11lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᰲ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll1l111_opy_: str = bstack1l111lll_opy_.bstack11llll111l1_opy_(label)
            start_mark: str = label + bstack1l11lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᰳ")
            end_mark: str = label + bstack1l11lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᰴ")
            result = None
            try:
                if stage.value == STAGE.bstack1l1111l1_opy_.value:
                    bstack1l111lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l111lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lll1llll_opy_)
                elif stage.value == STAGE.bstack1l1ll11ll1_opy_.value:
                    start_mark: str = bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᰵ")
                    end_mark: str = bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᰶ")
                    bstack1l111lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l111lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lll1llll_opy_)
            except Exception as e:
                bstack1l111lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lll1llll_opy_)
            return result
        return wrapper
    return decorator