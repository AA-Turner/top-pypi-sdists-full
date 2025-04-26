# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11111llll_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1lll111_opy_: Dict[str, float] = {}
bstack111l1lllll1_opy_: List = []
bstack111l1lll1l1_opy_ = 5
bstack11ll1llll_opy_ = os.path.join(os.getcwd(), bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡪࠫᴃ"), bstack1l11lll_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫᴄ"))
logging.getLogger(bstack1l11lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠫᴅ")).setLevel(logging.WARNING)
lock = FileLock(bstack11ll1llll_opy_+bstack1l11lll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᴆ"))
class bstack111l1ll1lll_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1ll1ll1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1ll1ll1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l11lll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧᴇ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1llll111_opy_:
    global bstack111l1lll111_opy_
    @staticmethod
    def bstack1ll1l1l1111_opy_(key: str):
        bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack11llll111l1_opy_(key)
        bstack1ll1llll111_opy_.mark(bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᴈ"))
        return bstack1ll1ll1l111_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1lll111_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᴉ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1llll111_opy_.mark(end)
            bstack1ll1llll111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᴊ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1lll111_opy_ or end not in bstack111l1lll111_opy_:
                logger.debug(bstack1l11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥᴋ").format(start,end))
                return
            duration: float = bstack111l1lll111_opy_[end] - bstack111l1lll111_opy_[start]
            bstack111l1llll11_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᴌ"), bstack1l11lll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᴍ")).lower() == bstack1l11lll_opy_ (u"ࠦࡹࡸࡵࡦࠤᴎ")
            bstack111l1llll1l_opy_: bstack111l1ll1lll_opy_ = bstack111l1ll1lll_opy_(duration, label, bstack111l1lll111_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᴏ"), 0), command, test_name, hook_type, bstack111l1llll11_opy_)
            del bstack111l1lll111_opy_[start]
            del bstack111l1lll111_opy_[end]
            bstack1ll1llll111_opy_.bstack111l1lll11l_opy_(bstack111l1llll1l_opy_)
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤᴐ").format(e))
    @staticmethod
    def bstack111l1lll11l_opy_(bstack111l1llll1l_opy_):
        os.makedirs(os.path.dirname(bstack11ll1llll_opy_)) if not os.path.exists(os.path.dirname(bstack11ll1llll_opy_)) else None
        bstack1ll1llll111_opy_.bstack111l1lll1ll_opy_()
        try:
            with lock:
                with open(bstack11ll1llll_opy_, bstack1l11lll_opy_ (u"ࠢࡳ࠭ࠥᴑ"), encoding=bstack1l11lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᴒ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1llll1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1ll1l1l_opy_:
            logger.debug(bstack1l11lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠣࡿࢂࠨᴓ").format(bstack111l1ll1l1l_opy_))
            with lock:
                with open(bstack11ll1llll_opy_, bstack1l11lll_opy_ (u"ࠥࡻࠧᴔ"), encoding=bstack1l11lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᴕ")) as file:
                    data = [bstack111l1llll1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡧࡰࡱࡧࡱࡨࠥࢁࡽࠣᴖ").format(str(e)))
        finally:
            if os.path.exists(bstack11ll1llll_opy_+bstack1l11lll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᴗ")):
                os.remove(bstack11ll1llll_opy_+bstack1l11lll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᴘ"))
    @staticmethod
    def bstack111l1lll1ll_opy_():
        attempt = 0
        while (attempt < bstack111l1lll1l1_opy_):
            attempt += 1
            if os.path.exists(bstack11ll1llll_opy_+bstack1l11lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᴙ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11llll111l1_opy_(label: str) -> str:
        try:
            return bstack1l11lll_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣᴚ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᴛ").format(e))