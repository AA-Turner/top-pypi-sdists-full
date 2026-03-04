# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
bstack1l1ll1l111_opy_ = bstack1l11l11ll1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l11111ll1_opy_: Optional[str] = None):
    bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣⅢ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll111111l_opy_: str = bstack1l1ll1l111_opy_.bstack11l111llll1_opy_(label)
            start_mark: str = label + bstack1lll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢⅣ")
            end_mark: str = label + bstack1lll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨⅤ")
            result = None
            try:
                if stage.value == STAGE.bstack111l111l1_opy_.value:
                    bstack1l1ll1l111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1ll1l111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l11111ll1_opy_)
                elif stage.value == STAGE.bstack1lllll1ll1_opy_.value:
                    start_mark: str = bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤⅥ")
                    end_mark: str = bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣⅦ")
                    bstack1l1ll1l111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1ll1l111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l11111ll1_opy_)
            except Exception as e:
                bstack1l1ll1l111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l11111ll1_opy_)
            return result
        return wrapper
    return decorator