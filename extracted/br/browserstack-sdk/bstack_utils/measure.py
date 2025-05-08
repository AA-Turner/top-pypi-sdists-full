# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1ll1l111l1_opy_ import get_logger
from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
bstack1ll11111l1_opy_ = bstack1lll1lll111_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111lll1ll_opy_: Optional[str] = None):
    bstack1l1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᰹")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l11lll1_opy_: str = bstack1ll11111l1_opy_.bstack11lll1ll1ll_opy_(label)
            start_mark: str = label + bstack1l1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᰺")
            end_mark: str = label + bstack1l1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᰻")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1l1l1_opy_.value:
                    bstack1ll11111l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11111l1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111lll1ll_opy_)
                elif stage.value == STAGE.bstack1111lll1_opy_.value:
                    start_mark: str = bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᰼")
                    end_mark: str = bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᰽")
                    bstack1ll11111l1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11111l1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111lll1ll_opy_)
            except Exception as e:
                bstack1ll11111l1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111lll1ll_opy_)
            return result
        return wrapper
    return decorator