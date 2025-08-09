# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1111111_opy_ import get_logger
logger = get_logger(__name__)
bstack111111lll11_opy_: Dict[str, float] = {}
bstack111111ll11l_opy_: List = []
bstack111111ll1ll_opy_ = 5
bstack11l11lll_opy_ = os.path.join(os.getcwd(), bstack11l1_opy_ (u"࠭࡬ࡰࡩࠪἤ"), bstack11l1_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪἥ"))
logging.getLogger(bstack11l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠪἦ")).setLevel(logging.WARNING)
lock = FileLock(bstack11l11lll_opy_+bstack11l1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣἧ"))
class bstack111111lllll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111111ll1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111111ll1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࠦἨ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1ll11111_opy_:
    global bstack111111lll11_opy_
    @staticmethod
    def bstack1ll11lll11l_opy_(key: str):
        bstack1ll111llll1_opy_ = bstack1ll1ll11111_opy_.bstack11ll1l1lll1_opy_(key)
        bstack1ll1ll11111_opy_.mark(bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦἩ"))
        return bstack1ll111llll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111111lll11_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣἪ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1ll11111_opy_.mark(end)
            bstack1ll1ll11111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥἫ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111111lll11_opy_ or end not in bstack111111lll11_opy_:
                logger.debug(bstack11l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠥࡵࡲࠡࡧࡱࡨࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠤἬ").format(start,end))
                return
            duration: float = bstack111111lll11_opy_[end] - bstack111111lll11_opy_[start]
            bstack11111l1111l_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦἭ"), bstack11l1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣἮ")).lower() == bstack11l1_opy_ (u"ࠥࡸࡷࡻࡥࠣἯ")
            bstack11111l11111_opy_: bstack111111lllll_opy_ = bstack111111lllll_opy_(duration, label, bstack111111lll11_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦἰ"), 0), command, test_name, hook_type, bstack11111l1111l_opy_)
            del bstack111111lll11_opy_[start]
            del bstack111111lll11_opy_[end]
            bstack1ll1ll11111_opy_.bstack111111llll1_opy_(bstack11111l11111_opy_)
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣἱ").format(e))
    @staticmethod
    def bstack111111llll1_opy_(bstack11111l11111_opy_):
        os.makedirs(os.path.dirname(bstack11l11lll_opy_)) if not os.path.exists(os.path.dirname(bstack11l11lll_opy_)) else None
        bstack1ll1ll11111_opy_.bstack111111lll1l_opy_()
        try:
            with lock:
                with open(bstack11l11lll_opy_, bstack11l1_opy_ (u"ࠨࡲࠬࠤἲ"), encoding=bstack11l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨἳ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111l11111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111l111l1_opy_:
            logger.debug(bstack11l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢࡾࢁࠧἴ").format(bstack11111l111l1_opy_))
            with lock:
                with open(bstack11l11lll_opy_, bstack11l1_opy_ (u"ࠤࡺࠦἵ"), encoding=bstack11l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤἶ")) as file:
                    data = [bstack11111l11111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡦࡶࡰࡦࡰࡧࠤࢀࢃࠢἷ").format(str(e)))
        finally:
            if os.path.exists(bstack11l11lll_opy_+bstack11l1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦἸ")):
                os.remove(bstack11l11lll_opy_+bstack11l1_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧἹ"))
    @staticmethod
    def bstack111111lll1l_opy_():
        attempt = 0
        while (attempt < bstack111111ll1ll_opy_):
            attempt += 1
            if os.path.exists(bstack11l11lll_opy_+bstack11l1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨἺ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1lll1_opy_(label: str) -> str:
        try:
            return bstack11l1_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢἻ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧἼ").format(e))