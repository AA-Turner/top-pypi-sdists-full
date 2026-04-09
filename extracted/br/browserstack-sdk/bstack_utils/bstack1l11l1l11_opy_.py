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
bstack1ll1l1l1l1ll_opy_: Dict[str, float] = {}
bstack1ll1l1l1ll11_opy_: List = []
bstack1l111llll_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"࠭࡬ࡰࡩࠪ◬"), bstack11ll11_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ◭"))
_1ll1l1ll1111_opy_: Dict[str, List] = {}
_1ll1l1ll1l11_opy_ = threading.Lock()
_1ll1l1l1ll1l_opy_ = False
class bstack1ll1l1ll1l1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l1l1l1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l1l1l1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11ll11_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࠤ◮")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll111lll_opy_:
    global bstack1ll1l1l1l1ll_opy_
    @staticmethod
    def bstack1ll11l11_opy_(key: str):
        bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1111ll11l1l_opy_(key)
        bstack1ll111lll_opy_.mark(bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ◯"))
        return bstack1111l1ll1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l1l1l1ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ◰").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll111lll_opy_.mark(end)
            bstack1ll111lll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣ◱").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l1l1l1ll_opy_ or end not in bstack1ll1l1l1l1ll_opy_:
                logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡶࡤࡶࡹࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠣࡳࡷࠦࡥ࡯ࡦࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠢ◲").format(start,end))
                return
            duration: float = bstack1ll1l1l1l1ll_opy_[end] - bstack1ll1l1l1l1ll_opy_[start]
            bstack1ll1l1ll1ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤ◳"), bstack11ll11_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ◴")).lower() == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ◵")
            bstack1ll1l1ll11ll_opy_: bstack1ll1l1ll1l1l_opy_ = bstack1ll1l1ll1l1l_opy_(duration, label, bstack1ll1l1l1l1ll_opy_[start], bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ◶").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ◷"), 0), command, test_name, hook_type, bstack1ll1l1ll1ll1_opy_)
            del bstack1ll1l1l1l1ll_opy_[start]
            del bstack1ll1l1l1l1ll_opy_[end]
            bstack1ll111lll_opy_.bstack1ll1l1l1lll1_opy_(bstack1ll1l1ll11ll_opy_)
            try:
                bstack1ll1l1ll11l1_opy_ = time.time_ns() / 1000000
                bstack1ll1l1l1l11l_opy_ = bstack1ll1l1ll11l1_opy_ - bstack1ll1l1ll11ll_opy_.startTime
                bstack1ll1l1ll11ll_opy_.duration = bstack1ll1l1l1l11l_opy_
                bstack1ll111lll_opy_.update_last_metric_duration(bstack1ll1l1ll11ll_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡸࡴࡩࡧࡴࡪࡰࡪࠤࡲ࡫ࡴࡳ࡫ࡦࠤࡩࡻࡲࡢࡶ࡬ࡳࡳࠦࡡࡧࡶࡨࡶࠥࡶࡥࡳࡵ࡬ࡷࡹ࡫࡮ࡤࡧ࠽ࠤࢀࢃࠢ◸").format(e))
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣ◹").format(e))
    @staticmethod
    def bstack1ll1l1l1lll1_opy_(bstack1ll1l1ll11ll_opy_):
        global _1ll1l1l1ll1l_opy_
        os.makedirs(os.path.dirname(bstack1l111llll_opy_)) if not os.path.exists(os.path.dirname(bstack1l111llll_opy_)) else None
        bstack1ll1l1ll1lll_opy_ = bstack11ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ◺").format(threading.get_ident(), os.getpid())
        if not _1ll1l1l1ll1l_opy_:
            _1ll1l1l1ll1l_opy_ = True
            atexit.register(bstack1ll111lll_opy_.bstack11l1l1l1ll_opy_)
        with _1ll1l1ll1l11_opy_:
            if bstack1ll1l1ll1lll_opy_ not in _1ll1l1ll1111_opy_:
                _1ll1l1ll1111_opy_[bstack1ll1l1ll1lll_opy_] = []
            _1ll1l1ll1111_opy_[bstack1ll1l1ll1lll_opy_].append(bstack1ll1l1ll11ll_opy_.__dict__)
    @staticmethod
    def _1ll1l1ll111l_opy_():
        bstack11ll11_opy_ (u"ࠢࠣࠤࡉࡰࡺࡹࡨࠡࡣ࡯ࡰࠥࡺࡨࡳࡧࡤࡨࠥࡨࡵࡧࡨࡨࡶࡸࠦࡴࡰࠢࡩ࡭ࡱ࡫ࠢࠣࠤ◻")
        with _1ll1l1ll1l11_opy_:
            if not _1ll1l1ll1111_opy_:
                return
            bstack1ll1l1l1llll_opy_ = []
            for bstack1ll1l1l1l1l1_opy_, buffer in _1ll1l1ll1111_opy_.items():
                bstack1ll1l1l1llll_opy_.extend(buffer)
            if not bstack1ll1l1l1llll_opy_:
                return
        lock = FileLock(bstack1l111llll_opy_ + bstack11ll11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ◼"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1l111llll_opy_, bstack11ll11_opy_ (u"ࠤࡵ࠯ࠧ◽"), encoding=bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ◾")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1ll1l1l1llll_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1l111llll_opy_, bstack11ll11_opy_ (u"ࠦࡼࠨ◿"), encoding=bstack11ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ☀")) as file:
                        json.dump(bstack1ll1l1l1llll_opy_, file, indent=4)
            with _1ll1l1ll1l11_opy_:
                _1ll1l1ll1111_opy_.clear()
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡨ࡯ࡹࡸ࡮ࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦ☁").format(str(e)))
    @staticmethod
    def bstack11l1l1l1ll_opy_():
        bstack11ll11_opy_ (u"ࠢࠣࠤࡓࡹࡧࡲࡩࡤࠢࡰࡩࡹ࡮࡯ࡥࠢࡷࡳࠥ࡬࡬ࡶࡵ࡫ࠤࡦࡲ࡬ࠡࡤࡸࡪ࡫࡫ࡲࡦࡦࠣࡱࡪࡺࡲࡪࡥࡶࠤ࠭ࡩࡡ࡭࡮ࠣࡦࡪ࡬࡯ࡳࡧࠣࡩࡽ࡯ࡴࠪࠤࠥࠦ☂")
        bstack1ll111lll_opy_._1ll1l1ll111l_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1ll1l1ll11ll_opy_):
        bstack11ll11_opy_ (u"ࠣࠤ࡙ࠥࡵࡪࡡࡵࡧࠣࡨࡺࡸࡡࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡨࡵࡧࡨࡨࡶࠥ࠮࡭ࡶࡥ࡫ࠤ࡫ࡧࡳࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡩ࡭ࡱ࡫ࠠࡊ࠱ࡒ࠭ࠧࠨࠢ☃")
        try:
            bstack1ll1l1ll1lll_opy_ = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ☄").format(threading.get_ident(), os.getpid())
            with _1ll1l1ll1l11_opy_:
                if bstack1ll1l1ll1lll_opy_ in _1ll1l1ll1111_opy_ and _1ll1l1ll1111_opy_[bstack1ll1l1ll1lll_opy_]:
                    _1ll1l1ll1111_opy_[bstack1ll1l1ll1lll_opy_][-1][bstack11ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ★")] = bstack1ll1l1ll11ll_opy_.duration
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠ࡭ࡣࡶࡸࠥࡳࡥࡵࡴ࡬ࡧࠥࡪࡵࡳࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ☆").format(e))
    @staticmethod
    def bstack1111ll11l1l_opy_(label: str) -> str:
        try:
            return bstack11ll11_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦ☇").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ☈").format(e))