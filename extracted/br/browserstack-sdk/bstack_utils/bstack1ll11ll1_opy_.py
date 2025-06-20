# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
logger = get_logger(__name__)
bstack11111lllll1_opy_: Dict[str, float] = {}
bstack1111l111l1l_opy_: List = []
bstack1111l111111_opy_ = 5
bstack1llll1ll1l_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬḿ"), bstack11ll11_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬṀ"))
logging.getLogger(bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠬṁ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llll1ll1l_opy_+bstack11ll11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥṂ"))
class bstack1111l11111l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1111l1111ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1111l1111ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11ll11_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨṃ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1l1ll1l1_opy_:
    global bstack11111lllll1_opy_
    @staticmethod
    def bstack1ll11ll11l1_opy_(key: str):
        bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack11ll1l1ll11_opy_(key)
        bstack1ll1l1ll1l1_opy_.mark(bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨṄ"))
        return bstack1ll11ll111l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111lllll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥṅ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1l1ll1l1_opy_.mark(end)
            bstack1ll1l1ll1l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧṆ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111lllll1_opy_ or end not in bstack11111lllll1_opy_:
                logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦṇ").format(start,end))
                return
            duration: float = bstack11111lllll1_opy_[end] - bstack11111lllll1_opy_[start]
            bstack1111l1111l1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨṈ"), bstack11ll11_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥṉ")).lower() == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥṊ")
            bstack1111l111ll1_opy_: bstack1111l11111l_opy_ = bstack1111l11111l_opy_(duration, label, bstack11111lllll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨṋ"), 0), command, test_name, hook_type, bstack1111l1111l1_opy_)
            del bstack11111lllll1_opy_[start]
            del bstack11111lllll1_opy_[end]
            bstack1ll1l1ll1l1_opy_.bstack1111l111lll_opy_(bstack1111l111ll1_opy_)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥṌ").format(e))
    @staticmethod
    def bstack1111l111lll_opy_(bstack1111l111ll1_opy_):
        os.makedirs(os.path.dirname(bstack1llll1ll1l_opy_)) if not os.path.exists(os.path.dirname(bstack1llll1ll1l_opy_)) else None
        bstack1ll1l1ll1l1_opy_.bstack1111l111l11_opy_()
        try:
            with lock:
                with open(bstack1llll1ll1l_opy_, bstack11ll11_opy_ (u"ࠣࡴ࠮ࠦṍ"), encoding=bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣṎ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1111l111ll1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111llllll_opy_:
            logger.debug(bstack11ll11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢṏ").format(bstack11111llllll_opy_))
            with lock:
                with open(bstack1llll1ll1l_opy_, bstack11ll11_opy_ (u"ࠦࡼࠨṐ"), encoding=bstack11ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦṑ")) as file:
                    data = [bstack1111l111ll1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤṒ").format(str(e)))
        finally:
            if os.path.exists(bstack1llll1ll1l_opy_+bstack11ll11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨṓ")):
                os.remove(bstack1llll1ll1l_opy_+bstack11ll11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢṔ"))
    @staticmethod
    def bstack1111l111l11_opy_():
        attempt = 0
        while (attempt < bstack1111l111111_opy_):
            attempt += 1
            if os.path.exists(bstack1llll1ll1l_opy_+bstack11ll11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣṕ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1ll11_opy_(label: str) -> str:
        try:
            return bstack11ll11_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤṖ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢṗ").format(e))