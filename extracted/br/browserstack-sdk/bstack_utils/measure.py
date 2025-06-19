# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1111ll111_opy_ import get_logger
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
bstack1ll1l111ll_opy_ = bstack1llll1l1l11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l11l11l_opy_: Optional[str] = None):
    bstack111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᴥ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11llll11_opy_: str = bstack1ll1l111ll_opy_.bstack11ll1llll11_opy_(label)
            start_mark: str = label + bstack111lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᴦ")
            end_mark: str = label + bstack111lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᴧ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll11l111l_opy_.value:
                    bstack1ll1l111ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll1l111ll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l11l11l_opy_)
                elif stage.value == STAGE.bstack111ll11l1_opy_.value:
                    start_mark: str = bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᴨ")
                    end_mark: str = bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᴩ")
                    bstack1ll1l111ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll1l111ll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l11l11l_opy_)
            except Exception as e:
                bstack1ll1l111ll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l11l11l_opy_)
            return result
        return wrapper
    return decorator