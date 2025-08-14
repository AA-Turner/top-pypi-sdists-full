# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1l11lll1_opy_ import get_logger
from bstack_utils.bstack111ll111l_opy_ import bstack1lll11l111l_opy_
bstack111ll111l_opy_ = bstack1lll11l111l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111l1llll_opy_: Optional[str] = None):
    bstack1l1l1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡆࡨࡧࡴࡸࡡࡵࡱࡵࠤࡹࡵࠠ࡭ࡱࡪࠤࡹ࡮ࡥࠡࡵࡷࡥࡷࡺࠠࡵ࡫ࡰࡩࠥࡵࡦࠡࡣࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡧ࡬ࡰࡰࡪࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠣࠤ᷹ࠥ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11lll111_opy_: str = bstack111ll111l_opy_.bstack11ll1l1l111_opy_(label)
            start_mark: str = label + bstack1l1l1ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᷺")
            end_mark: str = label + bstack1l1l1ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᷻")
            result = None
            try:
                if stage.value == STAGE.bstack11llll11l1_opy_.value:
                    bstack111ll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack111ll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111l1llll_opy_)
                elif stage.value == STAGE.bstack1l1ll11l1_opy_.value:
                    start_mark: str = bstack1ll11lll111_opy_ + bstack1l1l1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᷼")
                    end_mark: str = bstack1ll11lll111_opy_ + bstack1l1l1ll_opy_ (u"ࠧࡀࡥ࡯ࡦ᷽ࠥ")
                    bstack111ll111l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack111ll111l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111l1llll_opy_)
            except Exception as e:
                bstack111ll111l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111l1llll_opy_)
            return result
        return wrapper
    return decorator