# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1llll1l111_opy_ import get_logger
logger = get_logger(__name__)
bstack1111l111111_opy_: Dict[str, float] = {}
bstack1111l111l11_opy_: List = []
bstack1111l111lll_opy_ = 5
bstack11l1lll11_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳ࡬࠭Ṁ"), bstack1l1l1l1_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ṁ"))
logging.getLogger(bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭Ṃ")).setLevel(logging.WARNING)
lock = FileLock(bstack11l1lll11_opy_+bstack1l1l1l1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦṃ"))
class bstack1111l1111l1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1111l111l1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1111l111l1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1l1l1_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢṄ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1ll11l1_opy_:
    global bstack1111l111111_opy_
    @staticmethod
    def bstack1ll11l1ll1l_opy_(key: str):
        bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack11lll1l11ll_opy_(key)
        bstack1lll1ll11l1_opy_.mark(bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢṅ"))
        return bstack1ll111ll1l1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1111l111111_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦṆ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1ll11l1_opy_.mark(end)
            bstack1lll1ll11l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨṇ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1111l111111_opy_ or end not in bstack1111l111111_opy_:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧṈ").format(start,end))
                return
            duration: float = bstack1111l111111_opy_[end] - bstack1111l111111_opy_[start]
            bstack11111llllll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢṉ"), bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦṊ")).lower() == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦṋ")
            bstack1111l11111l_opy_: bstack1111l1111l1_opy_ = bstack1111l1111l1_opy_(duration, label, bstack1111l111111_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢṌ"), 0), command, test_name, hook_type, bstack11111llllll_opy_)
            del bstack1111l111111_opy_[start]
            del bstack1111l111111_opy_[end]
            bstack1lll1ll11l1_opy_.bstack11111lllll1_opy_(bstack1111l11111l_opy_)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦṍ").format(e))
    @staticmethod
    def bstack11111lllll1_opy_(bstack1111l11111l_opy_):
        os.makedirs(os.path.dirname(bstack11l1lll11_opy_)) if not os.path.exists(os.path.dirname(bstack11l1lll11_opy_)) else None
        bstack1lll1ll11l1_opy_.bstack1111l1111ll_opy_()
        try:
            with lock:
                with open(bstack11l1lll11_opy_, bstack1l1l1l1_opy_ (u"ࠤࡵ࠯ࠧṎ"), encoding=bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤṏ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1111l11111l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1111l111ll1_opy_:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣṐ").format(bstack1111l111ll1_opy_))
            with lock:
                with open(bstack11l1lll11_opy_, bstack1l1l1l1_opy_ (u"ࠧࡽࠢṑ"), encoding=bstack1l1l1l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧṒ")) as file:
                    data = [bstack1111l11111l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥṓ").format(str(e)))
        finally:
            if os.path.exists(bstack11l1lll11_opy_+bstack1l1l1l1_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢṔ")):
                os.remove(bstack11l1lll11_opy_+bstack1l1l1l1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣṕ"))
    @staticmethod
    def bstack1111l1111ll_opy_():
        attempt = 0
        while (attempt < bstack1111l111lll_opy_):
            attempt += 1
            if os.path.exists(bstack11l1lll11_opy_+bstack1l1l1l1_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤṖ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll1l11ll_opy_(label: str) -> str:
        try:
            return bstack1l1l1l1_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥṗ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣṘ").format(e))