# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
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
bstack1llll1l1ll1l_opy_: Dict[str, float] = {}
bstack1llll1l11l1l_opy_: List = []
bstack1ll1l1ll1_opy_ = os.path.join(os.getcwd(), bstack1ll111_opy_ (u"ࠪࡰࡴ࡭ࠧḂ"), bstack1ll111_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧḃ"))
_1llll1l11ll1_opy_: Dict[str, List] = {}
_1llll1l1ll11_opy_ = threading.Lock()
_1llll1l1l111_opy_ = False
class bstack1llll1l11lll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1llll1l11l11_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1llll1l11l11_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll111_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨḄ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack111ll11111_opy_:
    global bstack1llll1l1ll1l_opy_
    @staticmethod
    def bstack111l11l11_opy_(key: str):
        bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack1111l1ll1ll_opy_(key)
        bstack111ll11111_opy_.mark(bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨḅ"))
        return bstack1l1l1l111_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1llll1l1ll1l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥḆ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack111ll11111_opy_.mark(end)
            bstack111ll11111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧḇ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1llll1l1ll1l_opy_ or end not in bstack1llll1l1ll1l_opy_:
                logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦḈ").format(start,end))
                return
            duration: float = bstack1llll1l1ll1l_opy_[end] - bstack1llll1l1ll1l_opy_[start]
            bstack1llll1l11111_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨḉ"), bstack1ll111_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥḊ")).lower() == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥḋ")
            bstack1llll1l1lll1_opy_: bstack1llll1l11lll_opy_ = bstack1llll1l11lll_opy_(duration, label, bstack1llll1l1ll1l_opy_[start], bstack1ll111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧḌ").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢḍ"), 0), command, test_name, hook_type, bstack1llll1l11111_opy_)
            del bstack1llll1l1ll1l_opy_[start]
            del bstack1llll1l1ll1l_opy_[end]
            bstack111ll11111_opy_.bstack1llll1l1111l_opy_(bstack1llll1l1lll1_opy_)
            try:
                bstack1llll1l111l1_opy_ = time.time_ns() / 1000000
                bstack1llll1l1l1ll_opy_ = bstack1llll1l111l1_opy_ - bstack1llll1l1lll1_opy_.startTime
                bstack1llll1l1lll1_opy_.duration = bstack1llll1l1l1ll_opy_
                bstack111ll11111_opy_.update_last_metric_duration(bstack1llll1l1lll1_opy_)
            except Exception as e:
                logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡ࡯ࡨࡸࡷ࡯ࡣࠡࡦࡸࡶࡦࡺࡩࡰࡰࠣࡥ࡫ࡺࡥࡳࠢࡳࡩࡷࡹࡩࡴࡶࡨࡲࡨ࡫࠺ࠡࡽࢀࠦḎ").format(e))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧḏ").format(e))
    @staticmethod
    def bstack1llll1l1111l_opy_(bstack1llll1l1lll1_opy_):
        global _1llll1l1l111_opy_
        os.makedirs(os.path.dirname(bstack1ll1l1ll1_opy_)) if not os.path.exists(os.path.dirname(bstack1ll1l1ll1_opy_)) else None
        bstack1llll1l111ll_opy_ = bstack1ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤḐ").format(threading.get_ident(), os.getpid())
        if not _1llll1l1l111_opy_:
            _1llll1l1l111_opy_ = True
            atexit.register(bstack111ll11111_opy_.bstack1l1ll1l1ll_opy_)
        with _1llll1l1ll11_opy_:
            if bstack1llll1l111ll_opy_ not in _1llll1l11ll1_opy_:
                _1llll1l11ll1_opy_[bstack1llll1l111ll_opy_] = []
            _1llll1l11ll1_opy_[bstack1llll1l111ll_opy_].append(bstack1llll1l1lll1_opy_.__dict__)
    @staticmethod
    def _1llll1l1l1l1_opy_():
        bstack1ll111_opy_ (u"ࠦࠧࠨࡆ࡭ࡷࡶ࡬ࠥࡧ࡬࡭ࠢࡷ࡬ࡷ࡫ࡡࡥࠢࡥࡹ࡫࡬ࡥࡳࡵࠣࡸࡴࠦࡦࡪ࡮ࡨࠦࠧࠨḑ")
        with _1llll1l1ll11_opy_:
            if not _1llll1l11ll1_opy_:
                return
            bstack1llll1l1l11l_opy_ = []
            for bstack1llll1l11l11_opy_, buffer in _1llll1l11ll1_opy_.items():
                bstack1llll1l1l11l_opy_.extend(buffer)
            if not bstack1llll1l1l11l_opy_:
                return
        lock = FileLock(bstack1ll1l1ll1_opy_ + bstack1ll111_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦḒ"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1ll1l1ll1_opy_, bstack1ll111_opy_ (u"ࠨࡲࠬࠤḓ"), encoding=bstack1ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨḔ")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1llll1l1l11l_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1ll1l1ll1_opy_, bstack1ll111_opy_ (u"ࠣࡹࠥḕ"), encoding=bstack1ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣḖ")) as file:
                        json.dump(bstack1llll1l1l11l_opy_, file, indent=4)
            with _1llll1l1ll11_opy_:
                _1llll1l11ll1_opy_.clear()
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡬࡬ࡶࡵ࡫࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࢁࡽࠣḗ").format(str(e)))
    @staticmethod
    def bstack1l1ll1l1ll_opy_():
        bstack1ll111_opy_ (u"ࠦࠧࠨࡐࡶࡤ࡯࡭ࡨࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡴࡰࠢࡩࡰࡺࡹࡨࠡࡣ࡯ࡰࠥࡨࡵࡧࡨࡨࡶࡪࡪࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࠪࡦࡥࡱࡲࠠࡣࡧࡩࡳࡷ࡫ࠠࡦࡺ࡬ࡸ࠮ࠨࠢࠣḘ")
        bstack111ll11111_opy_._1llll1l1l1l1_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1llll1l1lll1_opy_):
        bstack1ll111_opy_ (u"ࠧࠨࠢࡖࡲࡧࡥࡹ࡫ࠠࡥࡷࡵࡥࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡺࡨࡦࠢࡥࡹ࡫࡬ࡥࡳࠢࠫࡱࡺࡩࡨࠡࡨࡤࡷࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡦࡪ࡮ࡨࠤࡎ࠵ࡏࠪࠤࠥࠦḙ")
        try:
            bstack1llll1l111ll_opy_ = bstack1ll111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧḚ").format(threading.get_ident(), os.getpid())
            with _1llll1l1ll11_opy_:
                if bstack1llll1l111ll_opy_ in _1llll1l11ll1_opy_ and _1llll1l11ll1_opy_[bstack1llll1l111ll_opy_]:
                    _1llll1l11ll1_opy_[bstack1llll1l111ll_opy_][-1][bstack1ll111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩḛ")] = bstack1llll1l1lll1_opy_.duration
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡱࡧࡳࡵࠢࡰࡩࡹࡸࡩࡤࠢࡧࡹࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣḜ").format(e))
    @staticmethod
    def bstack1111l1ll1ll_opy_(label: str) -> str:
        try:
            return bstack1ll111_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣḝ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨḞ").format(e))