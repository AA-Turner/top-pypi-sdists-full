# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
bstack111l1l1ll1_opy_ = bstack1l11ll1l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11lll111_opy_: Optional[str] = None):
    bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ∢")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l1llll1_opy_: str = bstack111l1l1ll1_opy_.bstack111lll1l11l_opy_(label)
            start_mark: str = label + bstack1111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ∣")
            end_mark: str = label + bstack1111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ∤")
            result = None
            try:
                if stage.value == STAGE.bstack1lll1l11ll_opy_.value:
                    bstack111l1l1ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack111l1l1ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11lll111_opy_)
                elif stage.value == STAGE.bstack11lll111l_opy_.value:
                    start_mark: str = bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ∥")
                    end_mark: str = bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ∦")
                    bstack111l1l1ll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack111l1l1ll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11lll111_opy_)
            except Exception as e:
                bstack111l1l1ll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11lll111_opy_)
            return result
        return wrapper
    return decorator