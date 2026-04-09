# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
bstack1l11l1l11_opy_ = bstack1ll111lll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l111l1111_opy_: Optional[str] = None):
    bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⑹")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1111l1ll1l_opy_: str = bstack1l11l1l11_opy_.bstack1111ll11l1l_opy_(label)
            start_mark: str = label + bstack11ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⑺")
            end_mark: str = label + bstack11ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⑻")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1ll1ll1_opy_.value:
                    bstack1l11l1l11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l11l1l11_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l111l1111_opy_)
                elif stage.value == STAGE.bstack1111l1111l_opy_.value:
                    start_mark: str = bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⑼")
                    end_mark: str = bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⑽")
                    bstack1l11l1l11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l11l1l11_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l111l1111_opy_)
            except Exception as e:
                bstack1l11l1l11_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l111l1111_opy_)
            return result
        return wrapper
    return decorator