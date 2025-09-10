# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1lll1llll_opy_ import get_logger
logger = get_logger(__name__)
bstack11111111l1l_opy_: Dict[str, float] = {}
bstack111111111ll_opy_: List = []
bstack11111111ll1_opy_ = 5
bstack111l1l111_opy_ = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠩ࡯ࡳ࡬࠭ἧ"), bstack1ll11ll_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭Ἠ"))
logging.getLogger(bstack1ll11ll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭Ἡ")).setLevel(logging.WARNING)
lock = FileLock(bstack111l1l111_opy_+bstack1ll11ll_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦἪ"))
class bstack1111111111l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack11111111l11_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11111111l11_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll11ll_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢἫ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1ll11ll1_opy_:
    global bstack11111111l1l_opy_
    @staticmethod
    def bstack1ll111l1111_opy_(key: str):
        bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack11ll1l111ll_opy_(key)
        bstack1ll1ll11ll1_opy_.mark(bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢἬ"))
        return bstack1ll111ll1ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111111l1l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦἭ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1ll11ll1_opy_.mark(end)
            bstack1ll1ll11ll1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨἮ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111111l1l_opy_ or end not in bstack11111111l1l_opy_:
                logger.debug(bstack1ll11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧἯ").format(start,end))
                return
            duration: float = bstack11111111l1l_opy_[end] - bstack11111111l1l_opy_[start]
            bstack1lllllllll1l_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢἰ"), bstack1ll11ll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦἱ")).lower() == bstack1ll11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦἲ")
            bstack11111111111_opy_: bstack1111111111l_opy_ = bstack1111111111l_opy_(duration, label, bstack11111111l1l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢἳ"), 0), command, test_name, hook_type, bstack1lllllllll1l_opy_)
            del bstack11111111l1l_opy_[start]
            del bstack11111111l1l_opy_[end]
            bstack1ll1ll11ll1_opy_.bstack1llllllllll1_opy_(bstack11111111111_opy_)
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦἴ").format(e))
    @staticmethod
    def bstack1llllllllll1_opy_(bstack11111111111_opy_):
        os.makedirs(os.path.dirname(bstack111l1l111_opy_)) if not os.path.exists(os.path.dirname(bstack111l1l111_opy_)) else None
        bstack1ll1ll11ll1_opy_.bstack1lllllllllll_opy_()
        try:
            with lock:
                with open(bstack111l1l111_opy_, bstack1ll11ll_opy_ (u"ࠤࡵ࠯ࠧἵ"), encoding=bstack1ll11ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤἶ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111111111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111111111l1_opy_:
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣἷ").format(bstack111111111l1_opy_))
            with lock:
                with open(bstack111l1l111_opy_, bstack1ll11ll_opy_ (u"ࠧࡽࠢἸ"), encoding=bstack1ll11ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧἹ")) as file:
                    data = [bstack11111111111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥἺ").format(str(e)))
        finally:
            if os.path.exists(bstack111l1l111_opy_+bstack1ll11ll_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢἻ")):
                os.remove(bstack111l1l111_opy_+bstack1ll11ll_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣἼ"))
    @staticmethod
    def bstack1lllllllllll_opy_():
        attempt = 0
        while (attempt < bstack11111111ll1_opy_):
            attempt += 1
            if os.path.exists(bstack111l1l111_opy_+bstack1ll11ll_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤἽ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l111ll_opy_(label: str) -> str:
        try:
            return bstack1ll11ll_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥἾ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣἿ").format(e))