# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1l11111_opy_ import get_logger
logger = get_logger(__name__)
bstack111111l11l1_opy_: Dict[str, float] = {}
bstack111111l1l11_opy_: List = []
bstack111111l111l_opy_ = 5
bstack1111l1ll1_opy_ = os.path.join(os.getcwd(), bstack1111lll_opy_ (u"ࠧ࡭ࡱࡪࠫ἞"), bstack1111lll_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫ἟"))
logging.getLogger(bstack1111lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠫἠ")).setLevel(logging.WARNING)
lock = FileLock(bstack1111l1ll1_opy_+bstack1111lll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤἡ"))
class bstack1111111lll1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111111l1l1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111111l1l1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1111lll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧἢ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1llll11l_opy_:
    global bstack111111l11l1_opy_
    @staticmethod
    def bstack1ll111llll1_opy_(key: str):
        bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack11ll1lllll1_opy_(key)
        bstack1ll1llll11l_opy_.mark(bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧἣ"))
        return bstack1ll11l1l11l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111111l11l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤἤ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1llll11l_opy_.mark(end)
            bstack1ll1llll11l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦἥ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111111l11l1_opy_ or end not in bstack111111l11l1_opy_:
                logger.debug(bstack1111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥἦ").format(start,end))
                return
            duration: float = bstack111111l11l1_opy_[end] - bstack111111l11l1_opy_[start]
            bstack1111111llll_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧἧ"), bstack1111lll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤἨ")).lower() == bstack1111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤἩ")
            bstack111111l1111_opy_: bstack1111111lll1_opy_ = bstack1111111lll1_opy_(duration, label, bstack111111l11l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧἪ"), 0), command, test_name, hook_type, bstack1111111llll_opy_)
            del bstack111111l11l1_opy_[start]
            del bstack111111l11l1_opy_[end]
            bstack1ll1llll11l_opy_.bstack111111l1ll1_opy_(bstack111111l1111_opy_)
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤἫ").format(e))
    @staticmethod
    def bstack111111l1ll1_opy_(bstack111111l1111_opy_):
        os.makedirs(os.path.dirname(bstack1111l1ll1_opy_)) if not os.path.exists(os.path.dirname(bstack1111l1ll1_opy_)) else None
        bstack1ll1llll11l_opy_.bstack111111l11ll_opy_()
        try:
            with lock:
                with open(bstack1111l1ll1_opy_, bstack1111lll_opy_ (u"ࠢࡳ࠭ࠥἬ"), encoding=bstack1111lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢἭ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111111l1111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111111l1lll_opy_:
            logger.debug(bstack1111lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠣࡿࢂࠨἮ").format(bstack111111l1lll_opy_))
            with lock:
                with open(bstack1111l1ll1_opy_, bstack1111lll_opy_ (u"ࠥࡻࠧἯ"), encoding=bstack1111lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥἰ")) as file:
                    data = [bstack111111l1111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡧࡰࡱࡧࡱࡨࠥࢁࡽࠣἱ").format(str(e)))
        finally:
            if os.path.exists(bstack1111l1ll1_opy_+bstack1111lll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧἲ")):
                os.remove(bstack1111l1ll1_opy_+bstack1111lll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨἳ"))
    @staticmethod
    def bstack111111l11ll_opy_():
        attempt = 0
        while (attempt < bstack111111l111l_opy_):
            attempt += 1
            if os.path.exists(bstack1111l1ll1_opy_+bstack1111lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢἴ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1lllll1_opy_(label: str) -> str:
        try:
            return bstack1111lll_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣἵ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨἶ").format(e))