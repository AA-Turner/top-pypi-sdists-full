# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1ll1l111l1_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1lllll1_opy_: Dict[str, float] = {}
bstack111l1ll1lll_opy_: List = []
bstack111l1lll11l_opy_ = 5
bstack1llll11l11_opy_ = os.path.join(os.getcwd(), bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡪࠫᴊ"), bstack1l1lll_opy_ (u"ࠨ࡭ࡨࡽ࠲ࡳࡥࡵࡴ࡬ࡧࡸ࠴ࡪࡴࡱࡱࠫᴋ"))
logging.getLogger(bstack1l1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠫᴌ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llll11l11_opy_+bstack1l1lll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᴍ"))
class bstack111l1lll111_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1llll1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1llll1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1lll_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࠧᴎ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1lll111_opy_:
    global bstack111l1lllll1_opy_
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(key: str):
        bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack11lll1ll1ll_opy_(key)
        bstack1lll1lll111_opy_.mark(bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᴏ"))
        return bstack1ll1l11lll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1lllll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᴐ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1lll111_opy_.mark(end)
            bstack1lll1lll111_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᴑ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1lllll1_opy_ or end not in bstack111l1lllll1_opy_:
                logger.debug(bstack1l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠦ࡯ࡳࠢࡨࡲࡩࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠥᴒ").format(start,end))
                return
            duration: float = bstack111l1lllll1_opy_[end] - bstack111l1lllll1_opy_[start]
            bstack111l1lll1l1_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᴓ"), bstack1l1lll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᴔ")).lower() == bstack1l1lll_opy_ (u"ࠦࡹࡸࡵࡦࠤᴕ")
            bstack111l1ll1l1l_opy_: bstack111l1lll111_opy_ = bstack111l1lll111_opy_(duration, label, bstack111l1lllll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᴖ"), 0), command, test_name, hook_type, bstack111l1lll1l1_opy_)
            del bstack111l1lllll1_opy_[start]
            del bstack111l1lllll1_opy_[end]
            bstack1lll1lll111_opy_.bstack111l1llll11_opy_(bstack111l1ll1l1l_opy_)
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲ࡫ࡡࡴࡷࡵ࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤᴗ").format(e))
    @staticmethod
    def bstack111l1llll11_opy_(bstack111l1ll1l1l_opy_):
        os.makedirs(os.path.dirname(bstack1llll11l11_opy_)) if not os.path.exists(os.path.dirname(bstack1llll11l11_opy_)) else None
        bstack1lll1lll111_opy_.bstack111l1ll1ll1_opy_()
        try:
            with lock:
                with open(bstack1llll11l11_opy_, bstack1l1lll_opy_ (u"ࠢࡳ࠭ࠥᴘ"), encoding=bstack1l1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᴙ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1ll1l1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1lll1ll_opy_:
            logger.debug(bstack1l1lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠣࡿࢂࠨᴚ").format(bstack111l1lll1ll_opy_))
            with lock:
                with open(bstack1llll11l11_opy_, bstack1l1lll_opy_ (u"ࠥࡻࠧᴛ"), encoding=bstack1l1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᴜ")) as file:
                    data = [bstack111l1ll1l1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡧࡰࡱࡧࡱࡨࠥࢁࡽࠣᴝ").format(str(e)))
        finally:
            if os.path.exists(bstack1llll11l11_opy_+bstack1l1lll_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᴞ")):
                os.remove(bstack1llll11l11_opy_+bstack1l1lll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᴟ"))
    @staticmethod
    def bstack111l1ll1ll1_opy_():
        attempt = 0
        while (attempt < bstack111l1lll11l_opy_):
            attempt += 1
            if os.path.exists(bstack1llll11l11_opy_+bstack1l1lll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᴠ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll1ll1ll_opy_(label: str) -> str:
        try:
            return bstack1l1lll_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣᴡ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᴢ").format(e))