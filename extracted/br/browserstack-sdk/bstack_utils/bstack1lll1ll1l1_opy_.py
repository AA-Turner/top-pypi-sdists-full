# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l11lll1_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1ll1ll1_opy_: Dict[str, float] = {}
bstack111l1lll1ll_opy_: List = []
bstack111l1llll11_opy_ = 5
bstack11lllll1l_opy_ = os.path.join(os.getcwd(), bstack11lll_opy_ (u"ࠫࡱࡵࡧࠨᴎ"), bstack11lll_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨᴏ"))
logging.getLogger(bstack11lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠨᴐ")).setLevel(logging.WARNING)
lock = FileLock(bstack11lllll1l_opy_+bstack11lll_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᴑ"))
class bstack111l1lll1l1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1lll111_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1lll111_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11lll_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࠤᴒ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1llllll1_opy_:
    global bstack111l1ll1ll1_opy_
    @staticmethod
    def bstack1ll1ll111ll_opy_(key: str):
        bstack1ll11lll1l1_opy_ = bstack1ll1llllll1_opy_.bstack11lllll11ll_opy_(key)
        bstack1ll1llllll1_opy_.mark(bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᴓ"))
        return bstack1ll11lll1l1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1ll1ll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᴔ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1llllll1_opy_.mark(end)
            bstack1ll1llllll1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣᴕ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1ll1ll1_opy_ or end not in bstack111l1ll1ll1_opy_:
                logger.debug(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡶࡤࡶࡹࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠣࡳࡷࠦࡥ࡯ࡦࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠢᴖ").format(start,end))
                return
            duration: float = bstack111l1ll1ll1_opy_[end] - bstack111l1ll1ll1_opy_[start]
            bstack111l1lll11l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤᴗ"), bstack11lll_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨᴘ")).lower() == bstack11lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᴙ")
            bstack111l1ll11ll_opy_: bstack111l1lll1l1_opy_ = bstack111l1lll1l1_opy_(duration, label, bstack111l1ll1ll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᴚ"), 0), command, test_name, hook_type, bstack111l1lll11l_opy_)
            del bstack111l1ll1ll1_opy_[start]
            del bstack111l1ll1ll1_opy_[end]
            bstack1ll1llllll1_opy_.bstack111l1ll1l11_opy_(bstack111l1ll11ll_opy_)
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡨࡥࡸࡻࡲࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨᴛ").format(e))
    @staticmethod
    def bstack111l1ll1l11_opy_(bstack111l1ll11ll_opy_):
        os.makedirs(os.path.dirname(bstack11lllll1l_opy_)) if not os.path.exists(os.path.dirname(bstack11lllll1l_opy_)) else None
        bstack1ll1llllll1_opy_.bstack111l1ll1lll_opy_()
        try:
            with lock:
                with open(bstack11lllll1l_opy_, bstack11lll_opy_ (u"ࠦࡷ࠱ࠢᴜ"), encoding=bstack11lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᴝ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1ll11ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1ll1l1l_opy_:
            logger.debug(bstack11lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠠࡼࡿࠥᴞ").format(bstack111l1ll1l1l_opy_))
            with lock:
                with open(bstack11lllll1l_opy_, bstack11lll_opy_ (u"ࠢࡸࠤᴟ"), encoding=bstack11lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᴠ")) as file:
                    data = [bstack111l1ll11ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡤࡴࡵ࡫࡮ࡥࠢࡾࢁࠧᴡ").format(str(e)))
        finally:
            if os.path.exists(bstack11lllll1l_opy_+bstack11lll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᴢ")):
                os.remove(bstack11lllll1l_opy_+bstack11lll_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴣ"))
    @staticmethod
    def bstack111l1ll1lll_opy_():
        attempt = 0
        while (attempt < bstack111l1llll11_opy_):
            attempt += 1
            if os.path.exists(bstack11lllll1l_opy_+bstack11lll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᴤ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lllll11ll_opy_(label: str) -> str:
        try:
            return bstack11lll_opy_ (u"ࠨࡻࡾ࠼ࡾࢁࠧᴥ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥᴦ").format(e))