# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11l1111l1_opy_ import get_logger
logger = get_logger(__name__)
bstack1111111lll1_opy_: Dict[str, float] = {}
bstack1111111l1l1_opy_: List = []
bstack1111111ll11_opy_ = 5
bstack1llll11l_opy_ = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡨࠩἣ"), bstack1111l1l_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩἤ"))
logging.getLogger(bstack1111l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩἥ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llll11l_opy_+bstack1111l1l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢἦ"))
class bstack1111111ll1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111111l1111_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111111l1111_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1111l1l_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧࠥἧ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11111ll_opy_:
    global bstack1111111lll1_opy_
    @staticmethod
    def bstack1ll1l111111_opy_(key: str):
        bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack11ll1l1ll11_opy_(key)
        bstack1lll11111ll_opy_.mark(bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥἨ"))
        return bstack1ll111l1ll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1111111lll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢἩ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11111ll_opy_.mark(end)
            bstack1lll11111ll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤἪ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1111111lll1_opy_ or end not in bstack1111111lll1_opy_:
                logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣἫ").format(start,end))
                return
            duration: float = bstack1111111lll1_opy_[end] - bstack1111111lll1_opy_[start]
            bstack1111111l11l_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥἬ"), bstack1111l1l_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢἭ")).lower() == bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢἮ")
            bstack111111l11l1_opy_: bstack1111111ll1l_opy_ = bstack1111111ll1l_opy_(duration, label, bstack1111111lll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1111l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥἯ"), 0), command, test_name, hook_type, bstack1111111l11l_opy_)
            del bstack1111111lll1_opy_[start]
            del bstack1111111lll1_opy_[end]
            bstack1lll11111ll_opy_.bstack111111l111l_opy_(bstack111111l11l1_opy_)
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢἰ").format(e))
    @staticmethod
    def bstack111111l111l_opy_(bstack111111l11l1_opy_):
        os.makedirs(os.path.dirname(bstack1llll11l_opy_)) if not os.path.exists(os.path.dirname(bstack1llll11l_opy_)) else None
        bstack1lll11111ll_opy_.bstack1111111llll_opy_()
        try:
            with lock:
                with open(bstack1llll11l_opy_, bstack1111l1l_opy_ (u"ࠧࡸࠫࠣἱ"), encoding=bstack1111l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧἲ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111111l11l1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1111111l1ll_opy_:
            logger.debug(bstack1111l1l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀࠦἳ").format(bstack1111111l1ll_opy_))
            with lock:
                with open(bstack1llll11l_opy_, bstack1111l1l_opy_ (u"ࠣࡹࠥἴ"), encoding=bstack1111l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣἵ")) as file:
                    data = [bstack111111l11l1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨἶ").format(str(e)))
        finally:
            if os.path.exists(bstack1llll11l_opy_+bstack1111l1l_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥἷ")):
                os.remove(bstack1llll11l_opy_+bstack1111l1l_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦἸ"))
    @staticmethod
    def bstack1111111llll_opy_():
        attempt = 0
        while (attempt < bstack1111111ll11_opy_):
            attempt += 1
            if os.path.exists(bstack1llll11l_opy_+bstack1111l1l_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧἹ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1ll11_opy_(label: str) -> str:
        try:
            return bstack1111l1l_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨἺ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦἻ").format(e))