# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11lll1ll_opy_ import get_logger
logger = get_logger(__name__)
bstack11111llll11_opy_: Dict[str, float] = {}
bstack11111lll111_opy_: List = []
bstack11111llll1l_opy_ = 5
bstack1lll111ll_opy_ = os.path.join(os.getcwd(), bstack1l1ll1_opy_ (u"࠭࡬ࡰࡩࠪṠ"), bstack1l1ll1_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪṡ"))
logging.getLogger(bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠪṢ")).setLevel(logging.WARNING)
lock = FileLock(bstack1lll111ll_opy_+bstack1l1ll1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣṣ"))
class bstack11111lllll1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack11111lll1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11111lll1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1ll1_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࠦṤ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll11l1l11_opy_:
    global bstack11111llll11_opy_
    @staticmethod
    def bstack1ll1l111111_opy_(key: str):
        bstack1ll111l1lll_opy_ = bstack1lll11l1l11_opy_.bstack11lll111ll1_opy_(key)
        bstack1lll11l1l11_opy_.mark(bstack1ll111l1lll_opy_+bstack1l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦṥ"))
        return bstack1ll111l1lll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111llll11_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣṦ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll11l1l11_opy_.mark(end)
            bstack1lll11l1l11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥṧ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111llll11_opy_ or end not in bstack11111llll11_opy_:
                logger.debug(bstack1l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠥࡵࡲࠡࡧࡱࡨࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠤṨ").format(start,end))
                return
            duration: float = bstack11111llll11_opy_[end] - bstack11111llll11_opy_[start]
            bstack1111l11111l_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦṩ"), bstack1l1ll1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣṪ")).lower() == bstack1l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣṫ")
            bstack11111lll1ll_opy_: bstack11111lllll1_opy_ = bstack11111lllll1_opy_(duration, label, bstack11111llll11_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦṬ"), 0), command, test_name, hook_type, bstack1111l11111l_opy_)
            del bstack11111llll11_opy_[start]
            del bstack11111llll11_opy_[end]
            bstack1lll11l1l11_opy_.bstack11111lll11l_opy_(bstack11111lll1ll_opy_)
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣṭ").format(e))
    @staticmethod
    def bstack11111lll11l_opy_(bstack11111lll1ll_opy_):
        os.makedirs(os.path.dirname(bstack1lll111ll_opy_)) if not os.path.exists(os.path.dirname(bstack1lll111ll_opy_)) else None
        bstack1lll11l1l11_opy_.bstack1111l111111_opy_()
        try:
            with lock:
                with open(bstack1lll111ll_opy_, bstack1l1ll1_opy_ (u"ࠨࡲࠬࠤṮ"), encoding=bstack1l1ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨṯ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111lll1ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111llllll_opy_:
            logger.debug(bstack1l1ll1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢࡾࢁࠧṰ").format(bstack11111llllll_opy_))
            with lock:
                with open(bstack1lll111ll_opy_, bstack1l1ll1_opy_ (u"ࠤࡺࠦṱ"), encoding=bstack1l1ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤṲ")) as file:
                    data = [bstack11111lll1ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡦࡶࡰࡦࡰࡧࠤࢀࢃࠢṳ").format(str(e)))
        finally:
            if os.path.exists(bstack1lll111ll_opy_+bstack1l1ll1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦṴ")):
                os.remove(bstack1lll111ll_opy_+bstack1l1ll1_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧṵ"))
    @staticmethod
    def bstack1111l111111_opy_():
        attempt = 0
        while (attempt < bstack11111llll1l_opy_):
            attempt += 1
            if os.path.exists(bstack1lll111ll_opy_+bstack1l1ll1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨṶ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll111ll1_opy_(label: str) -> str:
        try:
            return bstack1l1ll1_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢṷ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧṸ").format(e))