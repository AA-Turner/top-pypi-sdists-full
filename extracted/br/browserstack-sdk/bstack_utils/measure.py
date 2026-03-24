# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
bstack1ll11111_opy_ = bstack1lll1lll11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll1l11l1l_opy_: Optional[str] = None):
    bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣ≳")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack11ll1ll1l_opy_: str = bstack1ll11111_opy_.bstack111lll1111l_opy_(label)
            start_mark: str = label + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ≴")
            end_mark: str = label + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ≵")
            result = None
            try:
                if stage.value == STAGE.bstack11l11l1l1_opy_.value:
                    bstack1ll11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll11111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll1l11l1l_opy_)
                elif stage.value == STAGE.bstack1ll1llll_opy_.value:
                    start_mark: str = bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ≶")
                    end_mark: str = bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ≷")
                    bstack1ll11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll11111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll1l11l1l_opy_)
            except Exception as e:
                bstack1ll11111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll1l11l1l_opy_)
            return result
        return wrapper
    return decorator