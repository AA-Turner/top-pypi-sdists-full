# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import atexit
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
import threading
from filelock import FileLock
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
logger = get_logger(__name__)
bstack1llll11ll111_opy_: Dict[str, float] = {}
bstack1llll11llll1_opy_: List = []
bstack1l1111l1_opy_ = os.path.join(os.getcwd(), bstack11l1ll1_opy_ (u"ࠧ࡭ࡱࡪࠫ₴"), bstack11l1ll1_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ₵"))
_1llll1l11111_opy_: Dict[str, List] = {}
_1llll11lll11_opy_ = threading.Lock()
_1llll1l11l11_opy_ = False
class bstack1llll11l1lll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1llll11lllll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1llll11lllll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1ll1_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥ₶")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1111ll_opy_:
    global bstack1llll11ll111_opy_
    @staticmethod
    def bstack11l11l1l_opy_(key: str):
        bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l1l11ll11_opy_(key)
        bstack1ll1111ll_opy_.mark(bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ₷"))
        return bstack1lll1llll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1llll11ll111_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ₸").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1111ll_opy_.mark(end)
            bstack1ll1111ll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤ₹").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1llll11ll111_opy_ or end not in bstack1llll11ll111_opy_:
                logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣ₺").format(start,end))
                return
            duration: float = bstack1llll11ll111_opy_[end] - bstack1llll11ll111_opy_[start]
            bstack1llll11lll1l_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥ₻"), bstack11l1ll1_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢ₼")).lower() == bstack11l1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ₽")
            bstack1llll11ll1l1_opy_: bstack1llll11l1lll_opy_ = bstack1llll11l1lll_opy_(duration, label, bstack1llll11ll111_opy_[start], bstack11l1ll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ₾").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ₿"), 0), command, test_name, hook_type, bstack1llll11lll1l_opy_)
            del bstack1llll11ll111_opy_[start]
            del bstack1llll11ll111_opy_[end]
            bstack1ll1111ll_opy_.bstack1llll1l11l1l_opy_(bstack1llll11ll1l1_opy_)
            try:
                bstack1llll1l1111l_opy_ = time.time_ns() / 1000000
                bstack1llll1l111ll_opy_ = bstack1llll1l1111l_opy_ - bstack1llll11ll1l1_opy_.startTime
                bstack1llll11ll1l1_opy_.duration = bstack1llll1l111ll_opy_
                bstack1ll1111ll_opy_.update_last_metric_duration(bstack1llll11ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡳࡥࡵࡴ࡬ࡧࠥࡪࡵࡳࡣࡷ࡭ࡴࡴࠠࡢࡨࡷࡩࡷࠦࡰࡦࡴࡶ࡭ࡸࡺࡥ࡯ࡥࡨ࠾ࠥࢁࡽࠣ⃀").format(e))
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤ⃁").format(e))
    @staticmethod
    def bstack1llll1l11l1l_opy_(bstack1llll11ll1l1_opy_):
        global _1llll1l11l11_opy_
        os.makedirs(os.path.dirname(bstack1l1111l1_opy_)) if not os.path.exists(os.path.dirname(bstack1l1111l1_opy_)) else None
        bstack1llll1l111l1_opy_ = bstack11l1ll1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ⃂").format(threading.get_ident(), os.getpid())
        if not _1llll1l11l11_opy_:
            _1llll1l11l11_opy_ = True
            atexit.register(bstack1ll1111ll_opy_.bstack1l111llll_opy_)
        with _1llll11lll11_opy_:
            if bstack1llll1l111l1_opy_ not in _1llll1l11111_opy_:
                _1llll1l11111_opy_[bstack1llll1l111l1_opy_] = []
            _1llll1l11111_opy_[bstack1llll1l111l1_opy_].append(bstack1llll11ll1l1_opy_.__dict__)
    @staticmethod
    def _1llll11ll11l_opy_():
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࡊࡱࡻࡳࡩࠢࡤࡰࡱࠦࡴࡩࡴࡨࡥࡩࠦࡢࡶࡨࡩࡩࡷࡹࠠࡵࡱࠣࡪ࡮ࡲࡥࠣࠤࠥ⃃")
        with _1llll11lll11_opy_:
            if not _1llll1l11111_opy_:
                return
            bstack1llll11ll1ll_opy_ = []
            for bstack1llll11lllll_opy_, buffer in _1llll1l11111_opy_.items():
                bstack1llll11ll1ll_opy_.extend(buffer)
            if not bstack1llll11ll1ll_opy_:
                return
        lock = FileLock(bstack1l1111l1_opy_ + bstack11l1ll1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ⃄"), timeout=0.1)
        try:
            with lock:
                try:
                    with open(bstack1l1111l1_opy_, bstack11l1ll1_opy_ (u"ࠥࡶ࠰ࠨ⃅"), encoding=bstack11l1ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ⃆")) as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = []
                        data.extend(bstack1llll11ll1ll_opy_)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                except FileNotFoundError:
                    with open(bstack1l1111l1_opy_, bstack11l1ll1_opy_ (u"ࠧࡽࠢ⃇"), encoding=bstack11l1ll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ⃈")) as file:
                        json.dump(bstack1llll11ll1ll_opy_, file, indent=4)
            with _1llll11lll11_opy_:
                _1llll1l11111_opy_.clear()
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡩࡰࡺࡹࡨࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧ⃉").format(str(e)))
    @staticmethod
    def bstack1l111llll_opy_():
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࡔࡺࡨ࡬ࡪࡥࠣࡱࡪࡺࡨࡰࡦࠣࡸࡴࠦࡦ࡭ࡷࡶ࡬ࠥࡧ࡬࡭ࠢࡥࡹ࡫࡬ࡥࡳࡧࡧࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥ࠮ࡣࡢ࡮࡯ࠤࡧ࡫ࡦࡰࡴࡨࠤࡪࡾࡩࡵࠫࠥࠦࠧ⃊")
        bstack1ll1111ll_opy_._1llll11ll11l_opy_()
    @staticmethod
    def update_last_metric_duration(bstack1llll11ll1l1_opy_):
        bstack11l1ll1_opy_ (u"ࠤ࡚ࠥࠦࡶࡤࡢࡶࡨࠤࡩࡻࡲࡢࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡢࡶࡨࡩࡩࡷࠦࠨ࡮ࡷࡦ࡬ࠥ࡬ࡡࡴࡶࡨࡶࠥࡺࡨࡢࡰࠣࡪ࡮ࡲࡥࠡࡋ࠲ࡓ࠮ࠨࠢࠣ⃋")
        try:
            bstack1llll1l111l1_opy_ = bstack11l1ll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ⃌").format(threading.get_ident(), os.getpid())
            with _1llll11lll11_opy_:
                if bstack1llll1l111l1_opy_ in _1llll1l11111_opy_ and _1llll1l11111_opy_[bstack1llll1l111l1_opy_]:
                    _1llll1l11111_opy_[bstack1llll1l111l1_opy_][-1][bstack11l1ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⃍")] = bstack1llll11ll1l1_opy_.duration
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡ࡮ࡤࡷࡹࠦ࡭ࡦࡶࡵ࡭ࡨࠦࡤࡶࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ⃎").format(e))
    @staticmethod
    def bstack11l1l11ll11_opy_(label: str) -> str:
        try:
            return bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠼ࡾࢁࠧ⃏").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥ⃐").format(e))