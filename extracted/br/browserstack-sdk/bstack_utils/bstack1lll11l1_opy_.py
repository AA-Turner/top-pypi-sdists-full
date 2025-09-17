# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
logger = get_logger(__name__)
bstack1111111l11l_opy_: Dict[str, float] = {}
bstack1111111l1ll_opy_: List = []
bstack1111111ll11_opy_ = 5
bstack1l11l1l11_opy_ = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠪࡰࡴ࡭ࠧἡ"), bstack1l11ll1_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧἢ"))
logging.getLogger(bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠧἣ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l11l1l11_opy_+bstack1l11ll1_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧἤ"))
class bstack1111111llll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1111111l1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1111111l1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l11ll1_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣἥ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11111l1_opy_:
    global bstack1111111l11l_opy_
    @staticmethod
    def bstack1ll111l11ll_opy_(key: str):
        bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack11lll111111_opy_(key)
        bstack1lll11111l1_opy_.mark(bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣἦ"))
        return bstack1ll111l1lll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1111111l11l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧἧ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11111l1_opy_.mark(end)
            bstack1lll11111l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢἨ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1111111l11l_opy_ or end not in bstack1111111l11l_opy_:
                logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨἩ").format(start,end))
                return
            duration: float = bstack1111111l11l_opy_[end] - bstack1111111l11l_opy_[start]
            bstack111111l111l_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣἪ"), bstack1l11ll1_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧἫ")).lower() == bstack1l11ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧἬ")
            bstack1111111ll1l_opy_: bstack1111111llll_opy_ = bstack1111111llll_opy_(duration, label, bstack1111111l11l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l11ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣἭ"), 0), command, test_name, hook_type, bstack111111l111l_opy_)
            del bstack1111111l11l_opy_[start]
            del bstack1111111l11l_opy_[end]
            bstack1lll11111l1_opy_.bstack1111111lll1_opy_(bstack1111111ll1l_opy_)
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧἮ").format(e))
    @staticmethod
    def bstack1111111lll1_opy_(bstack1111111ll1l_opy_):
        os.makedirs(os.path.dirname(bstack1l11l1l11_opy_)) if not os.path.exists(os.path.dirname(bstack1l11l1l11_opy_)) else None
        bstack1lll11111l1_opy_.bstack111111l1111_opy_()
        try:
            with lock:
                with open(bstack1l11l1l11_opy_, bstack1l11ll1_opy_ (u"ࠥࡶ࠰ࠨἯ"), encoding=bstack1l11ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥἰ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1111111ll1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1111111l111_opy_:
            logger.debug(bstack1l11ll1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠦࡻࡾࠤἱ").format(bstack1111111l111_opy_))
            with lock:
                with open(bstack1l11l1l11_opy_, bstack1l11ll1_opy_ (u"ࠨࡷࠣἲ"), encoding=bstack1l11ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨἳ")) as file:
                    data = [bstack1111111ll1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡣࡳࡴࡪࡴࡤࠡࡽࢀࠦἴ").format(str(e)))
        finally:
            if os.path.exists(bstack1l11l1l11_opy_+bstack1l11ll1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣἵ")):
                os.remove(bstack1l11l1l11_opy_+bstack1l11ll1_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤἶ"))
    @staticmethod
    def bstack111111l1111_opy_():
        attempt = 0
        while (attempt < bstack1111111ll11_opy_):
            attempt += 1
            if os.path.exists(bstack1l11l1l11_opy_+bstack1l11ll1_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥἷ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll111111_opy_(label: str) -> str:
        try:
            return bstack1l11ll1_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦἸ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤἹ").format(e))