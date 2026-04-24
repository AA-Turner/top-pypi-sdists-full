# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
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
bstack1ll1l1l111ll_opy_: Dict[str, float] = {}
bstack1ll1l1l11l11_opy_: List = []
bstack111ll1l11_opy_ = os.path.join(os.getcwd(), bstack111ll11_opy_ (u"ࠫࡱࡵࡧࠨ☢"), bstack111ll11_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨ☣"))
_1ll1l1l111l1_opy_: Dict[str, List] = {}
_1ll1l11ll111_opy_ = threading.Lock()
_1ll1l11lll1l_opy_ = False
class bstack1ll1l11ll1l1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l11l1lll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l11l1lll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack111ll11_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢ☤")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1l11l1_opy_:
    global bstack1ll1l1l111ll_opy_
    @staticmethod
    def bstack11lllll1_opy_(key: str):
        bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack1111lll11l1_opy_(key)
        bstack1ll1l11l1_opy_.mark(bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ☥"))
        return bstack11111l11ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l1l111ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ☦").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1l11l1_opy_.mark(end)
            bstack1ll1l11l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨ☧").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l1l111ll_opy_ or end not in bstack1ll1l1l111ll_opy_:
                logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧ☨").format(start,end))
                return
            duration: float = bstack1ll1l1l111ll_opy_[end] - bstack1ll1l1l111ll_opy_[start]
            bstack1ll1l11ll11l_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢ☩"), bstack111ll11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ☪")).lower() == bstack111ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ☫")
            bstack1ll1l1l11111_opy_: bstack1ll1l11ll1l1_opy_ = bstack1ll1l11ll1l1_opy_(duration, label, bstack1ll1l1l111ll_opy_[start], bstack111ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ☬").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack111ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ☭"), 0), command, test_name, hook_type, bstack1ll1l11ll11l_opy_)
            del bstack1ll1l1l111ll_opy_[start]
            del bstack1ll1l1l111ll_opy_[end]
            bstack1ll1l11l1_opy_.bstack1ll1l11lll11_opy_(bstack1ll1l1l11111_opy_)
            try:
                bstack1ll1l1l11l1l_opy_ = time.time_ns() / 1000000
                bstack1ll1l11lllll_opy_ = bstack1ll1l1l11l1l_opy_ - bstack1ll1l1l11111_opy_.startTime
                bstack1ll1l1l11111_opy_.duration = bstack1ll1l11lllll_opy_
                bstack1ll1l11l1_opy_.update_last_metric_duration(bstack1ll1l1l11111_opy_)
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡰࡩࡹࡸࡩࡤࠢࡧࡹࡷࡧࡴࡪࡱࡱࠤࡦ࡬ࡴࡦࡴࠣࡴࡪࡸࡳࡪࡵࡷࡩࡳࡩࡥ࠻ࠢࡾࢁࠧ☮").format(e))
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡨࡥࡸࡻࡲࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨ☯").format(e))
    @staticmethod
    def bstack1ll1l11lll11_opy_(bstack1ll1l1l11111_opy_):
        global _1ll1l11lll1l_opy_
        os.makedirs(os.path.dirname(bstack111ll1l11_opy_)) if not os.path.exists(os.path.dirname(bstack111ll1l11_opy_)) else None
        bstack1ll1l1l1111l_opy_ = bstack111ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ☰").format(threading.get_ident(), os.getpid())
        if not _1ll1l11lll1l_opy_:
            _1ll1l11lll1l_opy_ = True
            atexit.register(bstack1ll1l11l1_opy_.bstack1111lll111_opy_)
        with _1ll1l11ll111_opy_:
            if bstack1ll1l1l1111l_opy_ not in _1ll1l1l111l1_opy_:
                _1ll1l1l111l1_opy_[bstack1ll1l1l1111l_opy_] = []
            _1ll1l1l111l1_opy_[bstack1ll1l1l1111l_opy_].append(bstack1ll1l1l11111_opy_.__dict__)
    @staticmethod
    def _1ll1l11llll1_opy_():
        bstack111ll11_opy_ (u"ࠧࠨࠢࡇ࡮ࡸࡷ࡭ࠦࡡ࡭࡮ࠣࡸ࡭ࡸࡥࡢࡦࠣࡦࡺ࡬ࡦࡦࡴࡶࠤࡹࡵࠠࡧ࡫࡯ࡩࠧࠨࠢ☱")
        with _1ll1l11ll111_opy_:
            if not _1ll1l1l111l1_opy_:
                return
            bstack1ll1l11ll1ll_opy_ = []
            for bstack1ll1l11l1lll_opy_, buffer in _1ll1l1l111l1_opy_.items():
                bstack1ll1l11ll1ll_opy_.extend(buffer)
            if not bstack1ll1l11ll1ll_opy_:
                return
        lock = FileLock(bstack111ll1l11_opy_ + bstack111ll11_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ☲"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack111ll1l11_opy_, bstack111ll11_opy_ (u"ࠢࡳ࠭ࠥ☳"), encoding=bstack111ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ☴")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1ll1l11ll1ll_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack111ll1l11_opy_, bstack111ll11_opy_ (u"ࠤࡺࠦ☵"), encoding=bstack111ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ☶")) as file:
                        json.dump(bstack1ll1l11ll1ll_opy_, file, indent=4)
            with _1ll1l11ll111_opy_:
                _1ll1l1l111l1_opy_.clear()
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡦ࡭ࡷࡶ࡬࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤ☷").format(str(e)))
    @staticmethod
    def bstack1111lll111_opy_():
        bstack111ll11_opy_ (u"ࠧࠨࠢࡑࡷࡥࡰ࡮ࡩࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡵࡱࠣࡪࡱࡻࡳࡩࠢࡤࡰࡱࠦࡢࡶࡨࡩࡩࡷ࡫ࡤࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࠫࡧࡦࡲ࡬ࠡࡤࡨࡪࡴࡸࡥࠡࡧࡻ࡭ࡹ࠯ࠢࠣࠤ☸")
        bstack1ll1l11l1_opy_._1ll1l11llll1_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1ll1l1l11111_opy_):
        bstack111ll11_opy_ (u"ࠨࠢࠣࡗࡳࡨࡦࡺࡥࠡࡦࡸࡶࡦࡺࡩࡰࡰࠣ࡭ࡳࠦࡴࡩࡧࠣࡦࡺ࡬ࡦࡦࡴࠣࠬࡲࡻࡣࡩࠢࡩࡥࡸࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡧ࡫࡯ࡩࠥࡏ࠯ࡐࠫࠥࠦࠧ☹")
        try:
            bstack1ll1l1l1111l_opy_ = bstack111ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ☺").format(threading.get_ident(), os.getpid())
            with _1ll1l11ll111_opy_:
                if bstack1ll1l1l1111l_opy_ in _1ll1l1l111l1_opy_ and _1ll1l1l111l1_opy_[bstack1ll1l1l1111l_opy_]:
                    _1ll1l1l111l1_opy_[bstack1ll1l1l1111l_opy_][-1][bstack111ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ☻")] = bstack1ll1l1l11111_opy_.duration
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡲࡡࡴࡶࠣࡱࡪࡺࡲࡪࡥࠣࡨࡺࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ☼").format(e))
    @staticmethod
    def bstack1111lll11l1_opy_(label: str) -> str:
        try:
            return bstack111ll11_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤ☽").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ☾").format(e))