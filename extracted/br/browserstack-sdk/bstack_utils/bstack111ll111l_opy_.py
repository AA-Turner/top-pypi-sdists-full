# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1l11lll1_opy_ import get_logger
logger = get_logger(__name__)
bstack111111ll111_opy_: Dict[str, float] = {}
bstack111111ll1l1_opy_: List = []
bstack111111lll11_opy_ = 5
bstack1lll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡨࠩἱ"), bstack1l1l1ll_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩἲ"))
logging.getLogger(bstack1l1l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩἳ")).setLevel(logging.WARNING)
lock = FileLock(bstack1lll1ll1l1_opy_+bstack1l1l1ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢἴ"))
class bstack111111l1lll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111111lllll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111111lllll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1l1ll_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥἵ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11l111l_opy_:
    global bstack111111ll111_opy_
    @staticmethod
    def bstack1ll11ll1l1l_opy_(key: str):
        bstack1ll11lll111_opy_ = bstack1lll11l111l_opy_.bstack11ll1l1l111_opy_(key)
        bstack1lll11l111l_opy_.mark(bstack1ll11lll111_opy_+bstack1l1l1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥἶ"))
        return bstack1ll11lll111_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111111ll111_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢἷ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11l111l_opy_.mark(end)
            bstack1lll11l111l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤἸ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111111ll111_opy_ or end not in bstack111111ll111_opy_:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣἹ").format(start,end))
                return
            duration: float = bstack111111ll111_opy_[end] - bstack111111ll111_opy_[start]
            bstack111111llll1_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥἺ"), bstack1l1l1ll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢἻ")).lower() == bstack1l1l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢἼ")
            bstack11111l11111_opy_: bstack111111l1lll_opy_ = bstack111111l1lll_opy_(duration, label, bstack111111ll111_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1l1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥἽ"), 0), command, test_name, hook_type, bstack111111llll1_opy_)
            del bstack111111ll111_opy_[start]
            del bstack111111ll111_opy_[end]
            bstack1lll11l111l_opy_.bstack111111lll1l_opy_(bstack11111l11111_opy_)
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢἾ").format(e))
    @staticmethod
    def bstack111111lll1l_opy_(bstack11111l11111_opy_):
        os.makedirs(os.path.dirname(bstack1lll1ll1l1_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1ll1l1_opy_)) else None
        bstack1lll11l111l_opy_.bstack111111ll11l_opy_()
        try:
            with lock:
                with open(bstack1lll1ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠧࡸࠫࠣἿ"), encoding=bstack1l1l1ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧὀ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111l11111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111111ll1ll_opy_:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀࠦὁ").format(bstack111111ll1ll_opy_))
            with lock:
                with open(bstack1lll1ll1l1_opy_, bstack1l1l1ll_opy_ (u"ࠣࡹࠥὂ"), encoding=bstack1l1l1ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣὃ")) as file:
                    data = [bstack11111l11111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨὄ").format(str(e)))
        finally:
            if os.path.exists(bstack1lll1ll1l1_opy_+bstack1l1l1ll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥὅ")):
                os.remove(bstack1lll1ll1l1_opy_+bstack1l1l1ll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦ὆"))
    @staticmethod
    def bstack111111ll11l_opy_():
        attempt = 0
        while (attempt < bstack111111lll11_opy_):
            attempt += 1
            if os.path.exists(bstack1lll1ll1l1_opy_+bstack1l1l1ll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ὇")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1l111_opy_(label: str) -> str:
        try:
            return bstack1l1l1ll_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨὈ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦὉ").format(e))