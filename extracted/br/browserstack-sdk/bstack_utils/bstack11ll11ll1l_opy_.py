# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
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
bstack1lll1ll1l1l1_opy_: Dict[str, float] = {}
bstack1lll1l1lll1l_opy_: List = []
bstack1lll1l1l_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠬࡲ࡯ࡨࠩ↠"), bstack11l11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ↡"))
_1lll1ll1l111_opy_: Dict[str, List] = {}
_1lll1ll11l11_opy_ = threading.Lock()
_1lll1ll1l1ll_opy_ = False
class bstack1lll1ll1l11l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1lll1ll111ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1lll1ll111ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l11_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣ↢")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack111l1lllll_opy_:
    global bstack1lll1ll1l1l1_opy_
    @staticmethod
    def bstack1l11111111_opy_(key: str):
        bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack11l11l111l1_opy_(key)
        bstack111l1lllll_opy_.mark(bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ↣"))
        return bstack1l111l111l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1lll1ll1l1l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ↤").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack111l1lllll_opy_.mark(end)
            bstack111l1lllll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ↥").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1lll1ll1l1l1_opy_ or end not in bstack1lll1ll1l1l1_opy_:
                logger.debug(bstack11l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨ↦").format(start,end))
                return
            duration: float = bstack1lll1ll1l1l1_opy_[end] - bstack1lll1ll1l1l1_opy_[start]
            bstack1lll1ll11111_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣ↧"), bstack11l11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ↨")).lower() == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ↩")
            bstack1lll1ll11ll1_opy_: bstack1lll1ll1l11l_opy_ = bstack1lll1ll1l11l_opy_(duration, label, bstack1lll1ll1l1l1_opy_[start], bstack11l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ↪").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ↫"), 0), command, test_name, hook_type, bstack1lll1ll11111_opy_)
            del bstack1lll1ll1l1l1_opy_[start]
            del bstack1lll1ll1l1l1_opy_[end]
            bstack111l1lllll_opy_.bstack1lll1ll11lll_opy_(bstack1lll1ll11ll1_opy_)
            try:
                bstack1lll1l1llll1_opy_ = time.time_ns() / 1000000
                bstack1lll1ll1111l_opy_ = bstack1lll1l1llll1_opy_ - bstack1lll1ll11ll1_opy_.startTime
                bstack1lll1ll11ll1_opy_.duration = bstack1lll1ll1111l_opy_
                bstack111l1lllll_opy_.update_last_metric_duration(bstack1lll1ll11ll1_opy_)
            except Exception as e:
                logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡱࡪࡺࡲࡪࡥࠣࡨࡺࡸࡡࡵ࡫ࡲࡲࠥࡧࡦࡵࡧࡵࠤࡵ࡫ࡲࡴ࡫ࡶࡸࡪࡴࡣࡦ࠼ࠣࡿࢂࠨ↬").format(e))
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ↭").format(e))
    @staticmethod
    def bstack1lll1ll11lll_opy_(bstack1lll1ll11ll1_opy_):
        global _1lll1ll1l1ll_opy_
        os.makedirs(os.path.dirname(bstack1lll1l1l_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1l1l_opy_)) else None
        bstack1lll1l1lllll_opy_ = bstack11l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ↮").format(threading.get_ident(), os.getpid())
        if not _1lll1ll1l1ll_opy_:
            _1lll1ll1l1ll_opy_ = True
            atexit.register(bstack111l1lllll_opy_.bstack1ll11ll111_opy_)
        with _1lll1ll11l11_opy_:
            if bstack1lll1l1lllll_opy_ not in _1lll1ll1l111_opy_:
                _1lll1ll1l111_opy_[bstack1lll1l1lllll_opy_] = []
            _1lll1ll1l111_opy_[bstack1lll1l1lllll_opy_].append(bstack1lll1ll11ll1_opy_.__dict__)
    @staticmethod
    def _1lll1ll11l1l_opy_():
        bstack11l11_opy_ (u"ࠨࠢࠣࡈ࡯ࡹࡸ࡮ࠠࡢ࡮࡯ࠤࡹ࡮ࡲࡦࡣࡧࠤࡧࡻࡦࡧࡧࡵࡷࠥࡺ࡯ࠡࡨ࡬ࡰࡪࠨࠢࠣ↯")
        with _1lll1ll11l11_opy_:
            if not _1lll1ll1l111_opy_:
                return
            bstack1lll1ll111l1_opy_ = []
            for bstack1lll1ll111ll_opy_, buffer in _1lll1ll1l111_opy_.items():
                bstack1lll1ll111l1_opy_.extend(buffer)
            if not bstack1lll1ll111l1_opy_:
                return
        lock = FileLock(bstack1lll1l1l_opy_ + bstack11l11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ↰"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1lll1l1l_opy_, bstack11l11_opy_ (u"ࠣࡴ࠮ࠦ↱"), encoding=bstack11l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ↲")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1lll1ll111l1_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1lll1l1l_opy_, bstack11l11_opy_ (u"ࠥࡻࠧ↳"), encoding=bstack11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ↴")) as file:
                        json.dump(bstack1lll1ll111l1_opy_, file, indent=4)
            with _1lll1ll11l11_opy_:
                _1lll1ll1l111_opy_.clear()
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡧ࡮ࡸࡷ࡭࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥ↵").format(str(e)))
    @staticmethod
    def bstack1ll11ll111_opy_():
        bstack11l11_opy_ (u"ࠨࠢࠣࡒࡸࡦࡱ࡯ࡣࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡶࡲࠤ࡫ࡲࡵࡴࡪࠣࡥࡱࡲࠠࡣࡷࡩࡪࡪࡸࡥࡥࠢࡰࡩࡹࡸࡩࡤࡵࠣࠬࡨࡧ࡬࡭ࠢࡥࡩ࡫ࡵࡲࡦࠢࡨࡼ࡮ࡺࠩࠣࠤࠥ↶")
        bstack111l1lllll_opy_._1lll1ll11l1l_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1lll1ll11ll1_opy_):
        bstack11l11_opy_ (u"ࠢࠣࠤࡘࡴࡩࡧࡴࡦࠢࡧࡹࡷࡧࡴࡪࡱࡱࠤ࡮ࡴࠠࡵࡪࡨࠤࡧࡻࡦࡧࡧࡵࠤ࠭ࡳࡵࡤࡪࠣࡪࡦࡹࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡨ࡬ࡰࡪࠦࡉ࠰ࡑࠬࠦࠧࠨ↷")
        try:
            bstack1lll1l1lllll_opy_ = bstack11l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ↸").format(threading.get_ident(), os.getpid())
            with _1lll1ll11l11_opy_:
                if bstack1lll1l1lllll_opy_ in _1lll1ll1l111_opy_ and _1lll1ll1l111_opy_[bstack1lll1l1lllll_opy_]:
                    _1lll1ll1l111_opy_[bstack1lll1l1lllll_opy_][-1][bstack11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ↹")] = bstack1lll1ll11ll1_opy_.duration
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦ࡬ࡢࡵࡷࠤࡲ࡫ࡴࡳ࡫ࡦࠤࡩࡻࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ↺").format(e))
    @staticmethod
    def bstack11l11l111l1_opy_(label: str) -> str:
        try:
            return bstack11l11_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥ↻").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ↼").format(e))