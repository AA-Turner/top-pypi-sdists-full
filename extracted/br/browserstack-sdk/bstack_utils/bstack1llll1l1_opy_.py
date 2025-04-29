# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1llllll1ll_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1lll1ll_opy_: Dict[str, float] = {}
bstack111l1lll111_opy_: List = []
bstack111l1llll11_opy_ = 5
bstack1l1ll11ll_opy_ = os.path.join(os.getcwd(), bstack1llllll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᴅ"), bstack1llllll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ᴆ"))
logging.getLogger(bstack1llllll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭ᴇ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l1ll11ll_opy_+bstack1llllll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᴈ"))
class bstack111l1lllll1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1ll1lll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1ll1lll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1llllll_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢᴉ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1llll1l_opy_:
    global bstack111l1lll1ll_opy_
    @staticmethod
    def bstack1ll1ll1l11l_opy_(key: str):
        bstack1ll1ll111l1_opy_ = bstack1lll1llll1l_opy_.bstack11lllll1lll_opy_(key)
        bstack1lll1llll1l_opy_.mark(bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᴊ"))
        return bstack1ll1ll111l1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1lll1ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᴋ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1llll1l_opy_.mark(end)
            bstack1lll1llll1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨᴌ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1lll1ll_opy_ or end not in bstack111l1lll1ll_opy_:
                logger.debug(bstack1llllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧᴍ").format(start,end))
                return
            duration: float = bstack111l1lll1ll_opy_[end] - bstack111l1lll1ll_opy_[start]
            bstack111l1lll1l1_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᴎ"), bstack1llllll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᴏ")).lower() == bstack1llllll_opy_ (u"ࠨࡴࡳࡷࡨࠦᴐ")
            bstack111l1llll1l_opy_: bstack111l1lllll1_opy_ = bstack111l1lllll1_opy_(duration, label, bstack111l1lll1ll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1llllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᴑ"), 0), command, test_name, hook_type, bstack111l1lll1l1_opy_)
            del bstack111l1lll1ll_opy_[start]
            del bstack111l1lll1ll_opy_[end]
            bstack1lll1llll1l_opy_.bstack111l1ll1ll1_opy_(bstack111l1llll1l_opy_)
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᴒ").format(e))
    @staticmethod
    def bstack111l1ll1ll1_opy_(bstack111l1llll1l_opy_):
        os.makedirs(os.path.dirname(bstack1l1ll11ll_opy_)) if not os.path.exists(os.path.dirname(bstack1l1ll11ll_opy_)) else None
        bstack1lll1llll1l_opy_.bstack111l1ll1l1l_opy_()
        try:
            with lock:
                with open(bstack1l1ll11ll_opy_, bstack1llllll_opy_ (u"ࠤࡵ࠯ࠧᴓ"), encoding=bstack1llllll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᴔ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1llll1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1lll11l_opy_:
            logger.debug(bstack1llllll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣᴕ").format(bstack111l1lll11l_opy_))
            with lock:
                with open(bstack1l1ll11ll_opy_, bstack1llllll_opy_ (u"ࠧࡽࠢᴖ"), encoding=bstack1llllll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᴗ")) as file:
                    data = [bstack111l1llll1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥᴘ").format(str(e)))
        finally:
            if os.path.exists(bstack1l1ll11ll_opy_+bstack1llllll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᴙ")):
                os.remove(bstack1l1ll11ll_opy_+bstack1llllll_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣᴚ"))
    @staticmethod
    def bstack111l1ll1l1l_opy_():
        attempt = 0
        while (attempt < bstack111l1llll11_opy_):
            attempt += 1
            if os.path.exists(bstack1l1ll11ll_opy_+bstack1llllll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᴛ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lllll1lll_opy_(label: str) -> str:
        try:
            return bstack1llllll_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥᴜ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᴝ").format(e))