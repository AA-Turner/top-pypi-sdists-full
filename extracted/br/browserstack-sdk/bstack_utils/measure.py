# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
bstack11ll1l1l_opy_ = bstack111l1l1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1111l11lll_opy_: Optional[str] = None):
    bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡉ࡫ࡣࡰࡴࡤࡸࡴࡸࠠࡵࡱࠣࡰࡴ࡭ࠠࡵࡪࡨࠤࡸࡺࡡࡳࡶࠣࡸ࡮ࡳࡥࠡࡱࡩࠤࡦࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠎࠥࠦࠠࠡࡣ࡯ࡳࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⓮")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack11111l11l_opy_: str = bstack11ll1l1l_opy_.bstack1111ll1ll11_opy_(label)
            start_mark: str = label + bstack111ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⓯")
            end_mark: str = label + bstack111ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⓰")
            result = None
            try:
                if stage.value == STAGE.bstack11llll1l1_opy_.value:
                    bstack11ll1l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11ll1l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1111l11lll_opy_)
                elif stage.value == STAGE.bstack1l1l11l1l_opy_.value:
                    start_mark: str = bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⓱")
                    end_mark: str = bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⓲")
                    bstack11ll1l1l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11ll1l1l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1111l11lll_opy_)
            except Exception as e:
                bstack11ll1l1l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1111l11lll_opy_)
            return result
        return wrapper
    return decorator