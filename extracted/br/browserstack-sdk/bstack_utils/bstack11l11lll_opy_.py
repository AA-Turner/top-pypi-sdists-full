# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
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
bstack1ll1l11ll1l1_opy_: Dict[str, float] = {}
bstack1ll1l11llll1_opy_: List = []
bstack11l1ll1ll1_opy_ = os.path.join(os.getcwd(), bstack1l1111l_opy_ (u"࠭࡬ࡰࡩࠪ☤"), bstack1l1111l_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ☥"))
_1ll1l11ll11l_opy_: Dict[str, List] = {}
_1ll1l11l1lll_opy_ = threading.Lock()
_1ll1l11l1ll1_opy_ = False
class bstack1ll1l1l111ll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l1l111l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l1l111l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1111l_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࠤ☦")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack11lll1111_opy_:
    global bstack1ll1l11ll1l1_opy_
    @staticmethod
    def bstack1l11l1ll_opy_(key: str):
        bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1111lll111l_opy_(key)
        bstack11lll1111_opy_.mark(bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ☧"))
        return bstack1l11l1l11_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l11ll1l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ☨").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack11lll1111_opy_.mark(end)
            bstack11lll1111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣ☩").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l11ll1l1_opy_ or end not in bstack1ll1l11ll1l1_opy_:
                logger.debug(bstack1l1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡶࡤࡶࡹࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠣࡳࡷࠦࡥ࡯ࡦࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠢ☪").format(start,end))
                return
            duration: float = bstack1ll1l11ll1l1_opy_[end] - bstack1ll1l11ll1l1_opy_[start]
            bstack1ll1l11lllll_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤ☫"), bstack1l1111l_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ☬")).lower() == bstack1l1111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ☭")
            bstack1ll1l11l1l1l_opy_: bstack1ll1l1l111ll_opy_ = bstack1ll1l1l111ll_opy_(duration, label, bstack1ll1l11ll1l1_opy_[start], bstack1l1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ☮").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack1l1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ☯"), 0), command, test_name, hook_type, bstack1ll1l11lllll_opy_)
            del bstack1ll1l11ll1l1_opy_[start]
            del bstack1ll1l11ll1l1_opy_[end]
            bstack11lll1111_opy_.bstack1ll1l11ll111_opy_(bstack1ll1l11l1l1l_opy_)
            try:
                bstack1ll1l11ll1ll_opy_ = time.time_ns() / 1000000
                bstack1ll1l11lll11_opy_ = bstack1ll1l11ll1ll_opy_ - bstack1ll1l11l1l1l_opy_.startTime
                bstack1ll1l11l1l1l_opy_.duration = bstack1ll1l11lll11_opy_
                bstack11lll1111_opy_.update_last_metric_duration(bstack1ll1l11l1l1l_opy_)
            except Exception as e:
                logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡸࡴࡩࡧࡴࡪࡰࡪࠤࡲ࡫ࡴࡳ࡫ࡦࠤࡩࡻࡲࡢࡶ࡬ࡳࡳࠦࡡࡧࡶࡨࡶࠥࡶࡥࡳࡵ࡬ࡷࡹ࡫࡮ࡤࡧ࠽ࠤࢀࢃࠢ☰").format(e))
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣ☱").format(e))
    @staticmethod
    def bstack1ll1l11ll111_opy_(bstack1ll1l11l1l1l_opy_):
        global _1ll1l11l1ll1_opy_
        os.makedirs(os.path.dirname(bstack11l1ll1ll1_opy_)) if not os.path.exists(os.path.dirname(bstack11l1ll1ll1_opy_)) else None
        bstack1ll1l11lll1l_opy_ = bstack1l1111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ☲").format(threading.get_ident(), os.getpid())
        if not _1ll1l11l1ll1_opy_:
            _1ll1l11l1ll1_opy_ = True
            atexit.register(bstack11lll1111_opy_.bstack1111111lll_opy_)
        with _1ll1l11l1lll_opy_:
            if bstack1ll1l11lll1l_opy_ not in _1ll1l11ll11l_opy_:
                _1ll1l11ll11l_opy_[bstack1ll1l11lll1l_opy_] = []
            _1ll1l11ll11l_opy_[bstack1ll1l11lll1l_opy_].append(bstack1ll1l11l1l1l_opy_.__dict__)
    @staticmethod
    def _1ll1l1l1111l_opy_():
        bstack1l1111l_opy_ (u"ࠢࠣࠤࡉࡰࡺࡹࡨࠡࡣ࡯ࡰࠥࡺࡨࡳࡧࡤࡨࠥࡨࡵࡧࡨࡨࡶࡸࠦࡴࡰࠢࡩ࡭ࡱ࡫ࠢࠣࠤ☳")
        with _1ll1l11l1lll_opy_:
            if not _1ll1l11ll11l_opy_:
                return
            bstack1ll1l1l11111_opy_ = []
            for bstack1ll1l1l111l1_opy_, buffer in _1ll1l11ll11l_opy_.items():
                bstack1ll1l1l11111_opy_.extend(buffer)
            if not bstack1ll1l1l11111_opy_:
                return
        lock = FileLock(bstack11l1ll1ll1_opy_ + bstack1l1111l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ☴"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack11l1ll1ll1_opy_, bstack1l1111l_opy_ (u"ࠤࡵ࠯ࠧ☵"), encoding=bstack1l1111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ☶")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1ll1l1l11111_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack11l1ll1ll1_opy_, bstack1l1111l_opy_ (u"ࠦࡼࠨ☷"), encoding=bstack1l1111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ☸")) as file:
                        json.dump(bstack1ll1l1l11111_opy_, file, indent=4)
            with _1ll1l11l1lll_opy_:
                _1ll1l11ll11l_opy_.clear()
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡨ࡯ࡹࡸ࡮ࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦ☹").format(str(e)))
    @staticmethod
    def bstack1111111lll_opy_():
        bstack1l1111l_opy_ (u"ࠢࠣࠤࡓࡹࡧࡲࡩࡤࠢࡰࡩࡹ࡮࡯ࡥࠢࡷࡳࠥ࡬࡬ࡶࡵ࡫ࠤࡦࡲ࡬ࠡࡤࡸࡪ࡫࡫ࡲࡦࡦࠣࡱࡪࡺࡲࡪࡥࡶࠤ࠭ࡩࡡ࡭࡮ࠣࡦࡪ࡬࡯ࡳࡧࠣࡩࡽ࡯ࡴࠪࠤࠥࠦ☺")
        bstack11lll1111_opy_._1ll1l1l1111l_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1ll1l11l1l1l_opy_):
        bstack1l1111l_opy_ (u"ࠣࠤ࡙ࠥࡵࡪࡡࡵࡧࠣࡨࡺࡸࡡࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡨࡵࡧࡨࡨࡶࠥ࠮࡭ࡶࡥ࡫ࠤ࡫ࡧࡳࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡩ࡭ࡱ࡫ࠠࡊ࠱ࡒ࠭ࠧࠨࠢ☻")
        try:
            bstack1ll1l11lll1l_opy_ = bstack1l1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ☼").format(threading.get_ident(), os.getpid())
            with _1ll1l11l1lll_opy_:
                if bstack1ll1l11lll1l_opy_ in _1ll1l11ll11l_opy_ and _1ll1l11ll11l_opy_[bstack1ll1l11lll1l_opy_]:
                    _1ll1l11ll11l_opy_[bstack1ll1l11lll1l_opy_][-1][bstack1l1111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ☽")] = bstack1ll1l11l1l1l_opy_.duration
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠ࡭ࡣࡶࡸࠥࡳࡥࡵࡴ࡬ࡧࠥࡪࡵࡳࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ☾").format(e))
    @staticmethod
    def bstack1111lll111l_opy_(label: str) -> str:
        try:
            return bstack1l1111l_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦ☿").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ♀").format(e))