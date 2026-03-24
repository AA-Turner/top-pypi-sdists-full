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
import atexit
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
import threading
from filelock import FileLock
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
bstack1lll11l11lll_opy_: Dict[str, float] = {}
bstack1lll11l11111_opy_: List = []
bstack1111ll1lll_opy_ = os.path.join(os.getcwd(), bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࠧ⏣"), bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧ⏤"))
_1lll111lll1l_opy_: Dict[str, List] = {}
_1lll11l111l1_opy_ = threading.Lock()
_1lll11l11ll1_opy_ = False
class bstack1lll111llll1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1lll11l1l11l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1lll11l1l11l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll1lll_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨ⏥")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1lll11_opy_:
    global bstack1lll11l11lll_opy_
    @staticmethod
    def bstack11l1llllll_opy_(key: str):
        bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack111lll1111l_opy_(key)
        bstack1lll1lll11_opy_.mark(bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⏦"))
        return bstack11ll1ll1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1lll11l11lll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥ⏧").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1lll11_opy_.mark(end)
            bstack1lll1lll11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧ⏨").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1lll11l11lll_opy_ or end not in bstack1lll11l11lll_opy_:
                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦ⏩").format(start,end))
                return
            duration: float = bstack1lll11l11lll_opy_[end] - bstack1lll11l11lll_opy_[start]
            bstack1lll111lllll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨ⏪"), bstack1ll1lll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ⏫")).lower() == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ⏬")
            bstack1lll111lll11_opy_: bstack1lll111llll1_opy_ = bstack1lll111llll1_opy_(duration, label, bstack1lll11l11lll_opy_[start], bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ⏭").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢ⏮"), 0), command, test_name, hook_type, bstack1lll111lllll_opy_)
            del bstack1lll11l11lll_opy_[start]
            del bstack1lll11l11lll_opy_[end]
            bstack1lll1lll11_opy_.bstack1lll11l11l11_opy_(bstack1lll111lll11_opy_)
            try:
                bstack1lll11l11l1l_opy_ = time.time_ns() / 1000000
                bstack1lll11l1111l_opy_ = bstack1lll11l11l1l_opy_ - bstack1lll111lll11_opy_.startTime
                bstack1lll111lll11_opy_.duration = bstack1lll11l1111l_opy_
                bstack1lll1lll11_opy_.update_last_metric_duration(bstack1lll111lll11_opy_)
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡ࡯ࡨࡸࡷ࡯ࡣࠡࡦࡸࡶࡦࡺࡩࡰࡰࠣࡥ࡫ࡺࡥࡳࠢࡳࡩࡷࡹࡩࡴࡶࡨࡲࡨ࡫࠺ࠡࡽࢀࠦ⏯").format(e))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧ⏰").format(e))
    @staticmethod
    def bstack1lll11l11l11_opy_(bstack1lll111lll11_opy_):
        global _1lll11l11ll1_opy_
        os.makedirs(os.path.dirname(bstack1111ll1lll_opy_)) if not os.path.exists(os.path.dirname(bstack1111ll1lll_opy_)) else None
        bstack1lll11l1l111_opy_ = bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ⏱").format(threading.get_ident(), os.getpid())
        if not _1lll11l11ll1_opy_:
            _1lll11l11ll1_opy_ = True
            atexit.register(bstack1lll1lll11_opy_.bstack1ll11l111_opy_)
        with _1lll11l111l1_opy_:
            if bstack1lll11l1l111_opy_ not in _1lll111lll1l_opy_:
                _1lll111lll1l_opy_[bstack1lll11l1l111_opy_] = []
            _1lll111lll1l_opy_[bstack1lll11l1l111_opy_].append(bstack1lll111lll11_opy_.__dict__)
    @staticmethod
    def _1lll11l111ll_opy_():
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡆ࡭ࡷࡶ࡬ࠥࡧ࡬࡭ࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡥࡹ࡫࡬ࡥࡳࡵࠣࡸࡴࠦࡦࡪ࡮ࡨࠦࠧࠨ⏲")
        with _1lll11l111l1_opy_:
            if not _1lll111lll1l_opy_:
                return
            bstack1lll11l1l1l1_opy_ = []
            for bstack1lll11l1l11l_opy_, buffer in _1lll111lll1l_opy_.items():
                bstack1lll11l1l1l1_opy_.extend(buffer)
            if not bstack1lll11l1l1l1_opy_:
                return
        lock = FileLock(bstack1111ll1lll_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦ⏳"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1111ll1lll_opy_, bstack1ll1lll_opy_ (u"ࠨࡲࠬࠤ⏴"), encoding=bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ⏵")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1lll11l1l1l1_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1111ll1lll_opy_, bstack1ll1lll_opy_ (u"ࠣࡹࠥ⏶"), encoding=bstack1ll1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ⏷")) as file:
                        json.dump(bstack1lll11l1l1l1_opy_, file, indent=4)
            with _1lll11l111l1_opy_:
                _1lll111lll1l_opy_.clear()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡬࡬ࡶࡵ࡫࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࢁࡽࠣ⏸").format(str(e)))
    @staticmethod
    def bstack1ll11l111_opy_():
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡐࡶࡤ࡯࡭ࡨࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡴࡰࠢࡩࡰࡺࡹࡨࠡࡣ࡯ࡰࠥࡨࡵࡧࡨࡨࡶࡪࡪࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࠪࡦࡥࡱࡲࠠࡣࡧࡩࡳࡷ࡫ࠠࡦࡺ࡬ࡸ࠮ࠨࠢࠣ⏹")
        bstack1lll1lll11_opy_._1lll11l111ll_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1lll111lll11_opy_):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡖࡲࡧࡥࡹ࡫ࠠࡥࡷࡵࡥࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡺࡨࡦࠢࡥࡹ࡫࡬ࡥࡳࠢࠫࡱࡺࡩࡨࠡࡨࡤࡷࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡦࡪ࡮ࡨࠤࡎ࠵ࡏࠪࠤࠥࠦ⏺")
        try:
            bstack1lll11l1l111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ⏻").format(threading.get_ident(), os.getpid())
            with _1lll11l111l1_opy_:
                if bstack1lll11l1l111_opy_ in _1lll111lll1l_opy_ and _1lll111lll1l_opy_[bstack1lll11l1l111_opy_]:
                    _1lll111lll1l_opy_[bstack1lll11l1l111_opy_][-1][bstack1ll1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⏼")] = bstack1lll111lll11_opy_.duration
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡱࡧࡳࡵࠢࡰࡩࡹࡸࡩࡤࠢࡧࡹࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ⏽").format(e))
    @staticmethod
    def bstack111lll1111l_opy_(label: str) -> str:
        try:
            return bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣ⏾").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⏿").format(e))