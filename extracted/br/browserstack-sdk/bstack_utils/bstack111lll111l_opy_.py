# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
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
bstack1lll1llll11l_opy_: Dict[str, float] = {}
bstack1lll1lll11ll_opy_: List = []
bstack11l11l1111_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭↫"), bstack11l1l11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭↬"))
_1lll1ll1lll1_opy_: Dict[str, List] = {}
_1lll1llll111_opy_ = threading.Lock()
_1lll1lll1l1l_opy_ = False
class bstack1lll1lll111l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1lll1llll1ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1lll1llll1ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1l11_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧ↭")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack11ll1l1l1_opy_:
    global bstack1lll1llll11l_opy_
    @staticmethod
    def bstack1l11l111ll_opy_(key: str):
        bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack11l11lll1l1_opy_(key)
        bstack11ll1l1l1_opy_.mark(bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ↮"))
        return bstack1l1l1l1111_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1lll1llll11l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ↯").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack11ll1l1l1_opy_.mark(end)
            bstack11ll1l1l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦ↰").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1lll1llll11l_opy_ or end not in bstack1lll1llll11l_opy_:
                logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥ↱").format(start,end))
                return
            duration: float = bstack1lll1llll11l_opy_[end] - bstack1lll1llll11l_opy_[start]
            bstack1lll1llll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧ↲"), bstack11l1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ↳")).lower() == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ↴")
            bstack1lll1ll1llll_opy_: bstack1lll1lll111l_opy_ = bstack1lll1lll111l_opy_(duration, label, bstack1lll1llll11l_opy_[start], bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ↵").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ↶"), 0), command, test_name, hook_type, bstack1lll1llll1l1_opy_)
            del bstack1lll1llll11l_opy_[start]
            del bstack1lll1llll11l_opy_[end]
            bstack11ll1l1l1_opy_.bstack1lll1lll11l1_opy_(bstack1lll1ll1llll_opy_)
            try:
                bstack1lll1lll1l11_opy_ = time.time_ns() / 1000000
                bstack1lll1lll1ll1_opy_ = bstack1lll1lll1l11_opy_ - bstack1lll1ll1llll_opy_.startTime
                bstack1lll1ll1llll_opy_.duration = bstack1lll1lll1ll1_opy_
                bstack11ll1l1l1_opy_.update_last_metric_duration(bstack1lll1ll1llll_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠ࡮ࡧࡷࡶ࡮ࡩࠠࡥࡷࡵࡥࡹ࡯࡯࡯ࠢࡤࡪࡹ࡫ࡲࠡࡲࡨࡶࡸ࡯ࡳࡵࡧࡱࡧࡪࡀࠠࡼࡿࠥ↷").format(e))
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦ↸").format(e))
    @staticmethod
    def bstack1lll1lll11l1_opy_(bstack1lll1ll1llll_opy_):
        global _1lll1lll1l1l_opy_
        os.makedirs(os.path.dirname(bstack11l11l1111_opy_)) if not os.path.exists(os.path.dirname(bstack11l11l1111_opy_)) else None
        bstack1lll1lllll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ↹").format(threading.get_ident(), os.getpid())
        if not _1lll1lll1l1l_opy_:
            _1lll1lll1l1l_opy_ = True
            atexit.register(bstack11ll1l1l1_opy_.bstack1111l11ll_opy_)
        with _1lll1llll111_opy_:
            if bstack1lll1lllll11_opy_ not in _1lll1ll1lll1_opy_:
                _1lll1ll1lll1_opy_[bstack1lll1lllll11_opy_] = []
            _1lll1ll1lll1_opy_[bstack1lll1lllll11_opy_].append(bstack1lll1ll1llll_opy_.__dict__)
    @staticmethod
    def _1lll1lll1lll_opy_():
        bstack11l1l11_opy_ (u"ࠥࠦࠧࡌ࡬ࡶࡵ࡫ࠤࡦࡲ࡬ࠡࡶ࡫ࡶࡪࡧࡤࠡࡤࡸࡪ࡫࡫ࡲࡴࠢࡷࡳࠥ࡬ࡩ࡭ࡧࠥࠦࠧ↺")
        with _1lll1llll111_opy_:
            if not _1lll1ll1lll1_opy_:
                return
            bstack1lll1lll1111_opy_ = []
            for bstack1lll1llll1ll_opy_, buffer in _1lll1ll1lll1_opy_.items():
                bstack1lll1lll1111_opy_.extend(buffer)
            if not bstack1lll1lll1111_opy_:
                return
        lock = FileLock(bstack11l11l1111_opy_ + bstack11l1l11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ↻"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack11l11l1111_opy_, bstack11l1l11_opy_ (u"ࠧࡸࠫࠣ↼"), encoding=bstack11l1l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ↽")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1lll1lll1111_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack11l11l1111_opy_, bstack11l1l11_opy_ (u"ࠢࡸࠤ↾"), encoding=bstack11l1l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ↿")) as file:
                        json.dump(bstack1lll1lll1111_opy_, file, indent=4)
            with _1lll1llll111_opy_:
                _1lll1ll1lll1_opy_.clear()
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡫ࡲࡵࡴࡪ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࢀࢃࠢ⇀").format(str(e)))
    @staticmethod
    def bstack1111l11ll_opy_():
        bstack11l1l11_opy_ (u"ࠥࠦࠧࡖࡵࡣ࡮࡬ࡧࠥࡳࡥࡵࡪࡲࡨࠥࡺ࡯ࠡࡨ࡯ࡹࡸ࡮ࠠࡢ࡮࡯ࠤࡧࡻࡦࡧࡧࡵࡩࡩࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࠩࡥࡤࡰࡱࠦࡢࡦࡨࡲࡶࡪࠦࡥࡹ࡫ࡷ࠭ࠧࠨࠢ⇁")
        bstack11ll1l1l1_opy_._1lll1lll1lll_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1lll1ll1llll_opy_):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࡕࡱࡦࡤࡸࡪࠦࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡤࡸࡪ࡫࡫ࡲࠡࠪࡰࡹࡨ࡮ࠠࡧࡣࡶࡸࡪࡸࠠࡵࡪࡤࡲࠥ࡬ࡩ࡭ࡧࠣࡍ࠴ࡕࠩࠣࠤࠥ⇂")
        try:
            bstack1lll1lllll11_opy_ = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ⇃").format(threading.get_ident(), os.getpid())
            with _1lll1llll111_opy_:
                if bstack1lll1lllll11_opy_ in _1lll1ll1lll1_opy_ and _1lll1ll1lll1_opy_[bstack1lll1lllll11_opy_]:
                    _1lll1ll1lll1_opy_[bstack1lll1lllll11_opy_][-1][bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⇄")] = bstack1lll1ll1llll_opy_.duration
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡰࡦࡹࡴࠡ࡯ࡨࡸࡷ࡯ࡣࠡࡦࡸࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ⇅").format(e))
    @staticmethod
    def bstack11l11lll1l1_opy_(label: str) -> str:
        try:
            return bstack11l1l11_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢ⇆").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⇇").format(e))