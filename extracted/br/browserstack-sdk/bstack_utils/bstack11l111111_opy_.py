# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1ll11l1ll_opy_ import get_logger
logger = get_logger(__name__)
bstack11111ll11ll_opy_: Dict[str, float] = {}
bstack11111lll11l_opy_: List = []
bstack11111lll111_opy_ = 5
bstack1l1lll111_opy_ = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠧ࡭ࡱࡪࠫầ"), bstackl_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫẨ"))
logging.getLogger(bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠫẩ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l1lll111_opy_+bstackl_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤẪ"))
class bstack11111ll1l11_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack11111ll1ll1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11111ll1ll1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstackl_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧẫ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11lll1l_opy_:
    global bstack11111ll11ll_opy_
    @staticmethod
    def bstack1ll11llllll_opy_(key: str):
        bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack11lll11111l_opy_(key)
        bstack1lll11lll1l_opy_.mark(bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧẬ"))
        return bstack1ll11lll11l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111ll11ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤậ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11lll1l_opy_.mark(end)
            bstack1lll11lll1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦẮ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111ll11ll_opy_ or end not in bstack11111ll11ll_opy_:
                logger.debug(bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥắ").format(start,end))
                return
            duration: float = bstack11111ll11ll_opy_[end] - bstack11111ll11ll_opy_[start]
            bstack11111ll11l1_opy_ = os.environ.get(bstackl_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧẰ"), bstackl_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤằ")).lower() == bstackl_opy_ (u"ࠦࡹࡸࡵࡦࠤẲ")
            bstack11111ll111l_opy_: bstack11111ll1l11_opy_ = bstack11111ll1l11_opy_(duration, label, bstack11111ll11ll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstackl_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧẳ"), 0), command, test_name, hook_type, bstack11111ll11l1_opy_)
            del bstack11111ll11ll_opy_[start]
            del bstack11111ll11ll_opy_[end]
            bstack1lll11lll1l_opy_.bstack11111ll1l1l_opy_(bstack11111ll111l_opy_)
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤẴ").format(e))
    @staticmethod
    def bstack11111ll1l1l_opy_(bstack11111ll111l_opy_):
        os.makedirs(os.path.dirname(bstack1l1lll111_opy_)) if not os.path.exists(os.path.dirname(bstack1l1lll111_opy_)) else None
        bstack1lll11lll1l_opy_.bstack11111ll1111_opy_()
        try:
            with lock:
                with open(bstack1l1lll111_opy_, bstackl_opy_ (u"ࠢࡳ࠭ࠥẵ"), encoding=bstackl_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢẶ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111ll111l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111ll1lll_opy_:
            logger.debug(bstackl_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠣࡿࢂࠨặ").format(bstack11111ll1lll_opy_))
            with lock:
                with open(bstack1l1lll111_opy_, bstackl_opy_ (u"ࠥࡻࠧẸ"), encoding=bstackl_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥẹ")) as file:
                    data = [bstack11111ll111l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡧࡰࡱࡧࡱࡨࠥࢁࡽࠣẺ").format(str(e)))
        finally:
            if os.path.exists(bstack1l1lll111_opy_+bstackl_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧẻ")):
                os.remove(bstack1l1lll111_opy_+bstackl_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨẼ"))
    @staticmethod
    def bstack11111ll1111_opy_():
        attempt = 0
        while (attempt < bstack11111lll111_opy_):
            attempt += 1
            if os.path.exists(bstack1l1lll111_opy_+bstackl_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢẽ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll11111l_opy_(label: str) -> str:
        try:
            return bstackl_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣẾ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨế").format(e))