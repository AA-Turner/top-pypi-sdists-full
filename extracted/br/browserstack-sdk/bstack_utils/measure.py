# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
bstack1llll111_opy_ = bstack111ll11l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1lll1l1l1l_opy_: Optional[str] = None):
    bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⒕")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1l11l11l_opy_: str = bstack1llll111_opy_.bstack1111lll1ll1_opy_(label)
            start_mark: str = label + bstack1l111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⒖")
            end_mark: str = label + bstack1l111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⒗")
            result = None
            try:
                if stage.value == STAGE.bstack11111ll1l1_opy_.value:
                    bstack1llll111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1llll111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1lll1l1l1l_opy_)
                elif stage.value == STAGE.bstack1l11llll1_opy_.value:
                    start_mark: str = bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⒘")
                    end_mark: str = bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⒙")
                    bstack1llll111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1llll111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1lll1l1l1l_opy_)
            except Exception as e:
                bstack1llll111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1lll1l1l1l_opy_)
            return result
        return wrapper
    return decorator