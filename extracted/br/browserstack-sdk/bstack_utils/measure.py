# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
bstack1l11ll1lll_opy_ = bstack1l11l1ll11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111l11111_opy_: Optional[str] = None):
    bstack1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⑼")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1lll1lll11_opy_: str = bstack1l11ll1lll_opy_.bstack1111lll111l_opy_(label)
            start_mark: str = label + bstack1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⑽")
            end_mark: str = label + bstack1ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⑾")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1lll1l_opy_.value:
                    bstack1l11ll1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l11ll1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111l11111_opy_)
                elif stage.value == STAGE.bstack11llll111l_opy_.value:
                    start_mark: str = bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⑿")
                    end_mark: str = bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⒀")
                    bstack1l11ll1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l11ll1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111l11111_opy_)
            except Exception as e:
                bstack1l11ll1lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111l11111_opy_)
            return result
        return wrapper
    return decorator