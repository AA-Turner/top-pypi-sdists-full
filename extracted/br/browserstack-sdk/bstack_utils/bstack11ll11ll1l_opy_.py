# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack111111111_opy_ import get_logger
logger = get_logger(__name__)
bstack111111llll1_opy_: Dict[str, float] = {}
bstack111111ll11l_opy_: List = []
bstack11111l1111l_opy_ = 5
bstack1ll1ll11_opy_ = os.path.join(os.getcwd(), bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡨࠩἣ"), bstack1ll1ll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩἤ"))
logging.getLogger(bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩἥ")).setLevel(logging.WARNING)
lock = FileLock(bstack1ll1ll11_opy_+bstack1ll1ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢἦ"))
class bstack111111lll11_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111111ll1ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111111ll1ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll1ll_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥἧ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1l1ll1l_opy_:
    global bstack111111llll1_opy_
    @staticmethod
    def bstack1ll11ll11ll_opy_(key: str):
        bstack1ll11l11l1l_opy_ = bstack1lll1l1ll1l_opy_.bstack11ll1l1ll1l_opy_(key)
        bstack1lll1l1ll1l_opy_.mark(bstack1ll11l11l1l_opy_+bstack1ll1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥἨ"))
        return bstack1ll11l11l1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111111llll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢἩ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1l1ll1l_opy_.mark(end)
            bstack1lll1l1ll1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤἪ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111111llll1_opy_ or end not in bstack111111llll1_opy_:
                logger.debug(bstack1ll1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣἫ").format(start,end))
                return
            duration: float = bstack111111llll1_opy_[end] - bstack111111llll1_opy_[start]
            bstack111111lll1l_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥἬ"), bstack1ll1ll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢἭ")).lower() == bstack1ll1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢἮ")
            bstack11111l111l1_opy_: bstack111111lll11_opy_ = bstack111111lll11_opy_(duration, label, bstack111111llll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1ll1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥἯ"), 0), command, test_name, hook_type, bstack111111lll1l_opy_)
            del bstack111111llll1_opy_[start]
            del bstack111111llll1_opy_[end]
            bstack1lll1l1ll1l_opy_.bstack111111ll1l1_opy_(bstack11111l111l1_opy_)
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢἰ").format(e))
    @staticmethod
    def bstack111111ll1l1_opy_(bstack11111l111l1_opy_):
        os.makedirs(os.path.dirname(bstack1ll1ll11_opy_)) if not os.path.exists(os.path.dirname(bstack1ll1ll11_opy_)) else None
        bstack1lll1l1ll1l_opy_.bstack111111lllll_opy_()
        try:
            with lock:
                with open(bstack1ll1ll11_opy_, bstack1ll1ll_opy_ (u"ࠧࡸࠫࠣἱ"), encoding=bstack1ll1ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧἲ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111l111l1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111l11111_opy_:
            logger.debug(bstack1ll1ll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀࠦἳ").format(bstack11111l11111_opy_))
            with lock:
                with open(bstack1ll1ll11_opy_, bstack1ll1ll_opy_ (u"ࠣࡹࠥἴ"), encoding=bstack1ll1ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣἵ")) as file:
                    data = [bstack11111l111l1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨἶ").format(str(e)))
        finally:
            if os.path.exists(bstack1ll1ll11_opy_+bstack1ll1ll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥἷ")):
                os.remove(bstack1ll1ll11_opy_+bstack1ll1ll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦἸ"))
    @staticmethod
    def bstack111111lllll_opy_():
        attempt = 0
        while (attempt < bstack11111l1111l_opy_):
            attempt += 1
            if os.path.exists(bstack1ll1ll11_opy_+bstack1ll1ll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧἹ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1ll1l_opy_(label: str) -> str:
        try:
            return bstack1ll1ll_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨἺ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦἻ").format(e))