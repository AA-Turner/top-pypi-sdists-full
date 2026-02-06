# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
bstack1llll11ll1ll_opy_: Dict[str, float] = {}
bstack1llll11llll1_opy_: List = []
bstack1l1111lll_opy_ = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"ࠫࡱࡵࡧࠨ⃔"), bstack11lllll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨ⃕"))
_1llll11l1l1l_opy_: Dict[str, List] = {}
_1llll11l1ll1_opy_ = threading.Lock()
_1llll11lll1l_opy_ = False
class bstack1llll11ll111_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1llll11ll1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1llll11ll1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11lllll_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢ⃖")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11l1ll_opy_:
    global bstack1llll11ll1ll_opy_
    @staticmethod
    def bstack1llll1l1ll_opy_(key: str):
        bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack11l1l111l1l_opy_(key)
        bstack1lll11l1ll_opy_.mark(bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⃗"))
        return bstack1ll11111l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1llll11ll1ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀ⃘ࠦ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11l1ll_opy_.mark(end)
            bstack1lll11l1ll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨ⃙").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1llll11ll1ll_opy_ or end not in bstack1llll11ll1ll_opy_:
                logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁ⃚ࠧ").format(start,end))
                return
            duration: float = bstack1llll11ll1ll_opy_[end] - bstack1llll11ll1ll_opy_[start]
            bstack1llll11lll11_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢ⃛"), bstack11lllll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ⃜")).lower() == bstack11lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦ⃝")
            bstack1llll11l111l_opy_: bstack1llll11ll111_opy_ = bstack1llll11ll111_opy_(duration, label, bstack1llll11ll1ll_opy_[start], bstack11lllll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ⃞").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ⃟"), 0), command, test_name, hook_type, bstack1llll11lll11_opy_)
            del bstack1llll11ll1ll_opy_[start]
            del bstack1llll11ll1ll_opy_[end]
            bstack1lll11l1ll_opy_.bstack1llll11l11ll_opy_(bstack1llll11l111l_opy_)
            try:
                bstack1llll11l1lll_opy_ = time.time_ns() / 1000000
                bstack1llll11lllll_opy_ = bstack1llll11l1lll_opy_ - bstack1llll11l111l_opy_.startTime
                bstack1llll11l111l_opy_.duration = bstack1llll11lllll_opy_
                bstack1lll11l1ll_opy_.update_last_metric_duration(bstack1llll11l111l_opy_)
            except Exception as e:
                logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡰࡩࡹࡸࡩࡤࠢࡧࡹࡷࡧࡴࡪࡱࡱࠤࡦ࡬ࡴࡦࡴࠣࡴࡪࡸࡳࡪࡵࡷࡩࡳࡩࡥ࠻ࠢࡾࢁࠧ⃠").format(e))
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡨࡥࡸࡻࡲࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨ⃡").format(e))
    @staticmethod
    def bstack1llll11l11ll_opy_(bstack1llll11l111l_opy_):
        global _1llll11lll1l_opy_
        os.makedirs(os.path.dirname(bstack1l1111lll_opy_)) if not os.path.exists(os.path.dirname(bstack1l1111lll_opy_)) else None
        bstack1llll11l1l11_opy_ = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ⃢").format(threading.get_ident(), os.getpid())
        if not _1llll11lll1l_opy_:
            _1llll11lll1l_opy_ = True
            atexit.register(bstack1lll11l1ll_opy_.bstack11llllllll_opy_)
        with _1llll11l1ll1_opy_:
            if bstack1llll11l1l11_opy_ not in _1llll11l1l1l_opy_:
                _1llll11l1l1l_opy_[bstack1llll11l1l11_opy_] = []
            _1llll11l1l1l_opy_[bstack1llll11l1l11_opy_].append(bstack1llll11l111l_opy_.__dict__)
    @staticmethod
    def _1llll11ll11l_opy_():
        bstack11lllll_opy_ (u"ࠧࠨࠢࡇ࡮ࡸࡷ࡭ࠦࡡ࡭࡮ࠣࡸ࡭ࡸࡥࡢࡦࠣࡦࡺ࡬ࡦࡦࡴࡶࠤࡹࡵࠠࡧ࡫࡯ࡩࠧࠨࠢ⃣")
        with _1llll11l1ll1_opy_:
            if not _1llll11l1l1l_opy_:
                return
            bstack1llll11l11l1_opy_ = []
            for bstack1llll11ll1l1_opy_, buffer in _1llll11l1l1l_opy_.items():
                bstack1llll11l11l1_opy_.extend(buffer)
            if not bstack1llll11l11l1_opy_:
                return
        lock = FileLock(bstack1l1111lll_opy_ + bstack11lllll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ⃤"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1l1111lll_opy_, bstack11lllll_opy_ (u"ࠢࡳ⃥࠭ࠥ"), encoding=bstack11lllll_opy_ (u"ࠣࡷࡷࡪ࠲࠾⃦ࠢ")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1llll11l11l1_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1l1111lll_opy_, bstack11lllll_opy_ (u"ࠤࡺࠦ⃧"), encoding=bstack11lllll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ⃨")) as file:
                        json.dump(bstack1llll11l11l1_opy_, file, indent=4)
            with _1llll11l1ll1_opy_:
                _1llll11l1l1l_opy_.clear()
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡦ࡭ࡷࡶ࡬࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤ⃩").format(str(e)))
    @staticmethod
    def bstack11llllllll_opy_():
        bstack11lllll_opy_ (u"ࠧࠨࠢࡑࡷࡥࡰ࡮ࡩࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡵࡱࠣࡪࡱࡻࡳࡩࠢࡤࡰࡱࠦࡢࡶࡨࡩࡩࡷ࡫ࡤࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࠫࡧࡦࡲ࡬ࠡࡤࡨࡪࡴࡸࡥࠡࡧࡻ࡭ࡹ࠯ࠢࠣࠤ⃪")
        bstack1lll11l1ll_opy_._1llll11ll11l_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1llll11l111l_opy_):
        bstack11lllll_opy_ (u"ࠨࠢࠣࡗࡳࡨࡦࡺࡥࠡࡦࡸࡶࡦࡺࡩࡰࡰࠣ࡭ࡳࠦࡴࡩࡧࠣࡦࡺ࡬ࡦࡦࡴࠣࠬࡲࡻࡣࡩࠢࡩࡥࡸࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡧ࡫࡯ࡩࠥࡏ࠯ࡐ⃫ࠫࠥࠦࠧ")
        try:
            bstack1llll11l1l11_opy_ = bstack11lllll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ⃬").format(threading.get_ident(), os.getpid())
            with _1llll11l1ll1_opy_:
                if bstack1llll11l1l11_opy_ in _1llll11l1l1l_opy_ and _1llll11l1l1l_opy_[bstack1llll11l1l11_opy_]:
                    _1llll11l1l1l_opy_[bstack1llll11l1l11_opy_][-1][bstack11lllll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰ⃭ࠪ")] = bstack1llll11l111l_opy_.duration
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡲࡡࡴࡶࠣࡱࡪࡺࡲࡪࡥࠣࡨࡺࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ⃮").format(e))
    @staticmethod
    def bstack11l1l111l1l_opy_(label: str) -> str:
        try:
            return bstack11lllll_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤ⃯").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ⃰").format(e))