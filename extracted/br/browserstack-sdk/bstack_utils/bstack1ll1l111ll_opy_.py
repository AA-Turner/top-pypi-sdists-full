# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1111ll111_opy_ import get_logger
logger = get_logger(__name__)
bstack1111ll1llll_opy_: Dict[str, float] = {}
bstack1111lll1ll1_opy_: List = []
bstack1111ll1lll1_opy_ = 5
bstack11lll111l1_opy_ = os.path.join(os.getcwd(), bstack111lll_opy_ (u"ࠧ࡭ࡱࡪࠫḔ"), bstack111lll_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫḕ"))
logging.getLogger(bstack111lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠫḖ")).setLevel(logging.WARNING)
lock = FileLock(bstack11lll111l1_opy_+bstack111lll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤḗ"))
class bstack1111lll1lll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1111lll1l1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1111lll1l1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack111lll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧḘ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1llll1l1l11_opy_:
    global bstack1111ll1llll_opy_
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(key: str):
        bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack11ll1llll11_opy_(key)
        bstack1llll1l1l11_opy_.mark(bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧḙ"))
        return bstack1ll11llll11_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1111ll1llll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤḚ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1llll1l1l11_opy_.mark(end)
            bstack1llll1l1l11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦḛ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1111ll1llll_opy_ or end not in bstack1111ll1llll_opy_:
                logger.debug(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥḜ").format(start,end))
                return
            duration: float = bstack1111ll1llll_opy_[end] - bstack1111ll1llll_opy_[start]
            bstack1111lll111l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧḝ"), bstack111lll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤḞ")).lower() == bstack111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤḟ")
            bstack1111lll11ll_opy_: bstack1111lll1lll_opy_ = bstack1111lll1lll_opy_(duration, label, bstack1111ll1llll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧḠ"), 0), command, test_name, hook_type, bstack1111lll111l_opy_)
            del bstack1111ll1llll_opy_[start]
            del bstack1111ll1llll_opy_[end]
            bstack1llll1l1l11_opy_.bstack1111lll11l1_opy_(bstack1111lll11ll_opy_)
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤḡ").format(e))
    @staticmethod
    def bstack1111lll11l1_opy_(bstack1111lll11ll_opy_):
        os.makedirs(os.path.dirname(bstack11lll111l1_opy_)) if not os.path.exists(os.path.dirname(bstack11lll111l1_opy_)) else None
        bstack1llll1l1l11_opy_.bstack1111lll1111_opy_()
        try:
            with lock:
                with open(bstack11lll111l1_opy_, bstack111lll_opy_ (u"ࠢࡳ࠭ࠥḢ"), encoding=bstack111lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢḣ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1111lll11ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1111lll1l11_opy_:
            logger.debug(bstack111lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠣࡿࢂࠨḤ").format(bstack1111lll1l11_opy_))
            with lock:
                with open(bstack11lll111l1_opy_, bstack111lll_opy_ (u"ࠥࡻࠧḥ"), encoding=bstack111lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥḦ")) as file:
                    data = [bstack1111lll11ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡧࡰࡱࡧࡱࡨࠥࢁࡽࠣḧ").format(str(e)))
        finally:
            if os.path.exists(bstack11lll111l1_opy_+bstack111lll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧḨ")):
                os.remove(bstack11lll111l1_opy_+bstack111lll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨḩ"))
    @staticmethod
    def bstack1111lll1111_opy_():
        attempt = 0
        while (attempt < bstack1111ll1lll1_opy_):
            attempt += 1
            if os.path.exists(bstack11lll111l1_opy_+bstack111lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢḪ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1llll11_opy_(label: str) -> str:
        try:
            return bstack111lll_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣḫ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨḬ").format(e))