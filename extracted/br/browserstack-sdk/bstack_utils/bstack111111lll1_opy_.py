# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
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
bstack1ll1l1l1llll_opy_: Dict[str, float] = {}
bstack1ll1l1ll1l11_opy_: List = []
bstack1llll11l_opy_ = os.path.join(os.getcwd(), bstack111l_opy_ (u"ࠬࡲ࡯ࡨࠩ◫"), bstack111l_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ◬"))
_1ll1l1ll11ll_opy_: Dict[str, List] = {}
_1ll1l1l1lll1_opy_ = threading.Lock()
_1ll1l1l1ll11_opy_ = False
class bstack1ll1l1ll111l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l1ll1ll1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l1ll1ll1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack111l_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣ◭")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack11lll11111_opy_:
    global bstack1ll1l1l1llll_opy_
    @staticmethod
    def bstack111111l11l_opy_(key: str):
        bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack1111lllll1l_opy_(key)
        bstack11lll11111_opy_.mark(bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ◮"))
        return bstack1l1l111lll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l1l1llll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ◯").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack11lll11111_opy_.mark(end)
            bstack11lll11111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ◰").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l1l1llll_opy_ or end not in bstack1ll1l1l1llll_opy_:
                logger.debug(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨ◱").format(start,end))
                return
            duration: float = bstack1ll1l1l1llll_opy_[end] - bstack1ll1l1l1llll_opy_[start]
            bstack1ll1l1lll111_opy_ = os.environ.get(bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣ◲"), bstack111l_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ◳")).lower() == bstack111l_opy_ (u"ࠢࡵࡴࡸࡩࠧ◴")
            bstack1ll1l1l1l1l1_opy_: bstack1ll1l1ll111l_opy_ = bstack1ll1l1ll111l_opy_(duration, label, bstack1ll1l1l1llll_opy_[start], bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ◵").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ◶"), 0), command, test_name, hook_type, bstack1ll1l1lll111_opy_)
            del bstack1ll1l1l1llll_opy_[start]
            del bstack1ll1l1l1llll_opy_[end]
            bstack11lll11111_opy_.bstack1ll1l1ll1l1l_opy_(bstack1ll1l1l1l1l1_opy_)
            try:
                bstack1ll1l1l1l1ll_opy_ = time.time_ns() / 1000000
                bstack1ll1l1l1ll1l_opy_ = bstack1ll1l1l1l1ll_opy_ - bstack1ll1l1l1l1l1_opy_.startTime
                bstack1ll1l1l1l1l1_opy_.duration = bstack1ll1l1l1ll1l_opy_
                bstack11lll11111_opy_.update_last_metric_duration(bstack1ll1l1l1l1l1_opy_)
            except Exception as e:
                logger.debug(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡱࡪࡺࡲࡪࡥࠣࡨࡺࡸࡡࡵ࡫ࡲࡲࠥࡧࡦࡵࡧࡵࠤࡵ࡫ࡲࡴ࡫ࡶࡸࡪࡴࡣࡦ࠼ࠣࡿࢂࠨ◷").format(e))
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢ◸").format(e))
    @staticmethod
    def bstack1ll1l1ll1l1l_opy_(bstack1ll1l1l1l1l1_opy_):
        global _1ll1l1l1ll11_opy_
        os.makedirs(os.path.dirname(bstack1llll11l_opy_)) if not os.path.exists(os.path.dirname(bstack1llll11l_opy_)) else None
        bstack1ll1l1ll11l1_opy_ = bstack111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ◹").format(threading.get_ident(), os.getpid())
        if not _1ll1l1l1ll11_opy_:
            _1ll1l1l1ll11_opy_ = True
            atexit.register(bstack11lll11111_opy_.bstack1l1ll1111l_opy_)
        with _1ll1l1l1lll1_opy_:
            if bstack1ll1l1ll11l1_opy_ not in _1ll1l1ll11ll_opy_:
                _1ll1l1ll11ll_opy_[bstack1ll1l1ll11l1_opy_] = []
            _1ll1l1ll11ll_opy_[bstack1ll1l1ll11l1_opy_].append(bstack1ll1l1l1l1l1_opy_.__dict__)
    @staticmethod
    def _1ll1l1ll1lll_opy_():
        bstack111l_opy_ (u"ࠨࠢࠣࡈ࡯ࡹࡸ࡮ࠠࡢ࡮࡯ࠤࡹ࡮ࡲࡦࡣࡧࠤࡧࡻࡦࡧࡧࡵࡷࠥࡺ࡯ࠡࡨ࡬ࡰࡪࠨࠢࠣ◺")
        with _1ll1l1l1lll1_opy_:
            if not _1ll1l1ll11ll_opy_:
                return
            bstack1ll1l1ll1111_opy_ = []
            for bstack1ll1l1ll1ll1_opy_, buffer in _1ll1l1ll11ll_opy_.items():
                bstack1ll1l1ll1111_opy_.extend(buffer)
            if not bstack1ll1l1ll1111_opy_:
                return
        lock = FileLock(bstack1llll11l_opy_ + bstack111l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ◻"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1llll11l_opy_, bstack111l_opy_ (u"ࠣࡴ࠮ࠦ◼"), encoding=bstack111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ◽")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1ll1l1ll1111_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1llll11l_opy_, bstack111l_opy_ (u"ࠥࡻࠧ◾"), encoding=bstack111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ◿")) as file:
                        json.dump(bstack1ll1l1ll1111_opy_, file, indent=4)
            with _1ll1l1l1lll1_opy_:
                _1ll1l1ll11ll_opy_.clear()
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡧ࡮ࡸࡷ࡭࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥ☀").format(str(e)))
    @staticmethod
    def bstack1l1ll1111l_opy_():
        bstack111l_opy_ (u"ࠨࠢࠣࡒࡸࡦࡱ࡯ࡣࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡶࡲࠤ࡫ࡲࡵࡴࡪࠣࡥࡱࡲࠠࡣࡷࡩࡪࡪࡸࡥࡥࠢࡰࡩࡹࡸࡩࡤࡵࠣࠬࡨࡧ࡬࡭ࠢࡥࡩ࡫ࡵࡲࡦࠢࡨࡼ࡮ࡺࠩࠣࠤࠥ☁")
        bstack11lll11111_opy_._1ll1l1ll1lll_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1ll1l1l1l1l1_opy_):
        bstack111l_opy_ (u"ࠢࠣࠤࡘࡴࡩࡧࡴࡦࠢࡧࡹࡷࡧࡴࡪࡱࡱࠤ࡮ࡴࠠࡵࡪࡨࠤࡧࡻࡦࡧࡧࡵࠤ࠭ࡳࡵࡤࡪࠣࡪࡦࡹࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡨ࡬ࡰࡪࠦࡉ࠰ࡑࠬࠦࠧࠨ☂")
        try:
            bstack1ll1l1ll11l1_opy_ = bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ☃").format(threading.get_ident(), os.getpid())
            with _1ll1l1l1lll1_opy_:
                if bstack1ll1l1ll11l1_opy_ in _1ll1l1ll11ll_opy_ and _1ll1l1ll11ll_opy_[bstack1ll1l1ll11l1_opy_]:
                    _1ll1l1ll11ll_opy_[bstack1ll1l1ll11l1_opy_][-1][bstack111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ☄")] = bstack1ll1l1l1l1l1_opy_.duration
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦ࡬ࡢࡵࡷࠤࡲ࡫ࡴࡳ࡫ࡦࠤࡩࡻࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ★").format(e))
    @staticmethod
    def bstack1111lllll1l_opy_(label: str) -> str:
        try:
            return bstack111l_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥ☆").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ☇").format(e))