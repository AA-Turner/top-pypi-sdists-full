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
bstack1ll1l1l11lll_opy_: Dict[str, float] = {}
bstack1ll1l1l1llll_opy_: List = []
bstack1ll11ll1l_opy_ = os.path.join(os.getcwd(), bstack1ll_opy_ (u"ࠩ࡯ࡳ࡬࠭◯"), bstack1ll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭◰"))
_1ll1l1l1ll11_opy_: Dict[str, List] = {}
_1ll1l1l1l111_opy_ = threading.Lock()
_1ll1l1l11ll1_opy_ = False
class bstack1ll1l1l1ll1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l1ll1111_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l1ll1111_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧ◱")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1l11l1ll11_opy_:
    global bstack1ll1l1l11lll_opy_
    @staticmethod
    def bstack1111ll1111_opy_(key: str):
        bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111lll111l_opy_(key)
        bstack1l11l1ll11_opy_.mark(bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ◲"))
        return bstack1lll1lll11_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l1l11lll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ◳").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1l11l1ll11_opy_.mark(end)
            bstack1l11l1ll11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦ◴").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l1l11lll_opy_ or end not in bstack1ll1l1l11lll_opy_:
                logger.debug(bstack1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥ◵").format(start,end))
                return
            duration: float = bstack1ll1l1l11lll_opy_[end] - bstack1ll1l1l11lll_opy_[start]
            bstack1ll1l1l1l1l1_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧ◶"), bstack1ll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ◷")).lower() == bstack1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ◸")
            bstack1ll1l1ll111l_opy_: bstack1ll1l1l1ll1l_opy_ = bstack1ll1l1l1ll1l_opy_(duration, label, bstack1ll1l1l11lll_opy_[start], bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ◹").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ◺"), 0), command, test_name, hook_type, bstack1ll1l1l1l1l1_opy_)
            del bstack1ll1l1l11lll_opy_[start]
            del bstack1ll1l1l11lll_opy_[end]
            bstack1l11l1ll11_opy_.bstack1ll1l1l11l1l_opy_(bstack1ll1l1ll111l_opy_)
            try:
                bstack1ll1l1l1l11l_opy_ = time.time_ns() / 1000000
                bstack1ll1l1l1l1ll_opy_ = bstack1ll1l1l1l11l_opy_ - bstack1ll1l1ll111l_opy_.startTime
                bstack1ll1l1ll111l_opy_.duration = bstack1ll1l1l1l1ll_opy_
                bstack1l11l1ll11_opy_.update_last_metric_duration(bstack1ll1l1ll111l_opy_)
            except Exception as e:
                logger.debug(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠ࡮ࡧࡷࡶ࡮ࡩࠠࡥࡷࡵࡥࡹ࡯࡯࡯ࠢࡤࡪࡹ࡫ࡲࠡࡲࡨࡶࡸ࡯ࡳࡵࡧࡱࡧࡪࡀࠠࡼࡿࠥ◻").format(e))
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦ◼").format(e))
    @staticmethod
    def bstack1ll1l1l11l1l_opy_(bstack1ll1l1ll111l_opy_):
        global _1ll1l1l11ll1_opy_
        os.makedirs(os.path.dirname(bstack1ll11ll1l_opy_)) if not os.path.exists(os.path.dirname(bstack1ll11ll1l_opy_)) else None
        bstack1ll1l1ll11l1_opy_ = bstack1ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ◽").format(threading.get_ident(), os.getpid())
        if not _1ll1l1l11ll1_opy_:
            _1ll1l1l11ll1_opy_ = True
            atexit.register(bstack1l11l1ll11_opy_.bstack11lllll11_opy_)
        with _1ll1l1l1l111_opy_:
            if bstack1ll1l1ll11l1_opy_ not in _1ll1l1l1ll11_opy_:
                _1ll1l1l1ll11_opy_[bstack1ll1l1ll11l1_opy_] = []
            _1ll1l1l1ll11_opy_[bstack1ll1l1ll11l1_opy_].append(bstack1ll1l1ll111l_opy_.__dict__)
    @staticmethod
    def _1ll1l1l1lll1_opy_():
        bstack1ll_opy_ (u"ࠥࠦࠧࡌ࡬ࡶࡵ࡫ࠤࡦࡲ࡬ࠡࡶ࡫ࡶࡪࡧࡤࠡࡤࡸࡪ࡫࡫ࡲࡴࠢࡷࡳࠥ࡬ࡩ࡭ࡧࠥࠦࠧ◾")
        with _1ll1l1l1l111_opy_:
            if not _1ll1l1l1ll11_opy_:
                return
            bstack1ll1l1l11l11_opy_ = []
            for bstack1ll1l1ll1111_opy_, buffer in _1ll1l1l1ll11_opy_.items():
                bstack1ll1l1l11l11_opy_.extend(buffer)
            if not bstack1ll1l1l11l11_opy_:
                return
        lock = FileLock(bstack1ll11ll1l_opy_ + bstack1ll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ◿"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1ll11ll1l_opy_, bstack1ll_opy_ (u"ࠧࡸࠫࠣ☀"), encoding=bstack1ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ☁")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1ll1l1l11l11_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1ll11ll1l_opy_, bstack1ll_opy_ (u"ࠢࡸࠤ☂"), encoding=bstack1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ☃")) as file:
                        json.dump(bstack1ll1l1l11l11_opy_, file, indent=4)
            with _1ll1l1l1l111_opy_:
                _1ll1l1l1ll11_opy_.clear()
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡫ࡲࡵࡴࡪ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࢀࢃࠢ☄").format(str(e)))
    @staticmethod
    def bstack11lllll11_opy_():
        bstack1ll_opy_ (u"ࠥࠦࠧࡖࡵࡣ࡮࡬ࡧࠥࡳࡥࡵࡪࡲࡨࠥࡺ࡯ࠡࡨ࡯ࡹࡸ࡮ࠠࡢ࡮࡯ࠤࡧࡻࡦࡧࡧࡵࡩࡩࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࠩࡥࡤࡰࡱࠦࡢࡦࡨࡲࡶࡪࠦࡥࡹ࡫ࡷ࠭ࠧࠨࠢ★")
        bstack1l11l1ll11_opy_._1ll1l1l1lll1_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1ll1l1ll111l_opy_):
        bstack1ll_opy_ (u"ࠦࠧࠨࡕࡱࡦࡤࡸࡪࠦࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡤࡸࡪ࡫࡫ࡲࠡࠪࡰࡹࡨ࡮ࠠࡧࡣࡶࡸࡪࡸࠠࡵࡪࡤࡲࠥ࡬ࡩ࡭ࡧࠣࡍ࠴ࡕࠩࠣࠤࠥ☆")
        try:
            bstack1ll1l1ll11l1_opy_ = bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ☇").format(threading.get_ident(), os.getpid())
            with _1ll1l1l1l111_opy_:
                if bstack1ll1l1ll11l1_opy_ in _1ll1l1l1ll11_opy_ and _1ll1l1l1ll11_opy_[bstack1ll1l1ll11l1_opy_]:
                    _1ll1l1l1ll11_opy_[bstack1ll1l1ll11l1_opy_][-1][bstack1ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ☈")] = bstack1ll1l1ll111l_opy_.duration
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡰࡦࡹࡴࠡ࡯ࡨࡸࡷ࡯ࡣࠡࡦࡸࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ☉").format(e))
    @staticmethod
    def bstack1111lll111l_opy_(label: str) -> str:
        try:
            return bstack1ll_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢ☊").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ☋").format(e))