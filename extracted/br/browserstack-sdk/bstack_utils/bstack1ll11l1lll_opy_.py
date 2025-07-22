# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1111ll_opy_ import get_logger
logger = get_logger(__name__)
bstack11111ll1l11_opy_: Dict[str, float] = {}
bstack11111lll1l1_opy_: List = []
bstack11111lll111_opy_ = 5
bstack1llllll1ll_opy_ = os.path.join(os.getcwd(), bstack111l111_opy_ (u"࠭࡬ࡰࡩࠪẦ"), bstack111l111_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪầ"))
logging.getLogger(bstack111l111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠪẨ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llllll1ll_opy_+bstack111l111_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣẩ"))
class bstack11111ll1ll1_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack11111ll1lll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11111ll1lll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack111l111_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࠦẪ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1llll1111l1_opy_:
    global bstack11111ll1l11_opy_
    @staticmethod
    def bstack1ll111llll1_opy_(key: str):
        bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack11ll1l1l11l_opy_(key)
        bstack1llll1111l1_opy_.mark(bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦẫ"))
        return bstack1ll11llll11_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111ll1l11_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣẬ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1llll1111l1_opy_.mark(end)
            bstack1llll1111l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥậ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111ll1l11_opy_ or end not in bstack11111ll1l11_opy_:
                logger.debug(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠥࡵࡲࠡࡧࡱࡨࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠤẮ").format(start,end))
                return
            duration: float = bstack11111ll1l11_opy_[end] - bstack11111ll1l11_opy_[start]
            bstack11111ll111l_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦắ"), bstack111l111_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣẰ")).lower() == bstack111l111_opy_ (u"ࠥࡸࡷࡻࡥࠣằ")
            bstack11111ll11ll_opy_: bstack11111ll1ll1_opy_ = bstack11111ll1ll1_opy_(duration, label, bstack11111ll1l11_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack111l111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦẲ"), 0), command, test_name, hook_type, bstack11111ll111l_opy_)
            del bstack11111ll1l11_opy_[start]
            del bstack11111ll1l11_opy_[end]
            bstack1llll1111l1_opy_.bstack11111lll11l_opy_(bstack11111ll11ll_opy_)
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣẳ").format(e))
    @staticmethod
    def bstack11111lll11l_opy_(bstack11111ll11ll_opy_):
        os.makedirs(os.path.dirname(bstack1llllll1ll_opy_)) if not os.path.exists(os.path.dirname(bstack1llllll1ll_opy_)) else None
        bstack1llll1111l1_opy_.bstack11111ll1l1l_opy_()
        try:
            with lock:
                with open(bstack1llllll1ll_opy_, bstack111l111_opy_ (u"ࠨࡲࠬࠤẴ"), encoding=bstack111l111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨẵ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111ll11ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111ll11l1_opy_:
            logger.debug(bstack111l111_opy_ (u"ࠣࡈ࡬ࡰࡪࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢࡾࢁࠧẶ").format(bstack11111ll11l1_opy_))
            with lock:
                with open(bstack1llllll1ll_opy_, bstack111l111_opy_ (u"ࠤࡺࠦặ"), encoding=bstack111l111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤẸ")) as file:
                    data = [bstack11111ll11ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡦࡶࡰࡦࡰࡧࠤࢀࢃࠢẹ").format(str(e)))
        finally:
            if os.path.exists(bstack1llllll1ll_opy_+bstack111l111_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦẺ")):
                os.remove(bstack1llllll1ll_opy_+bstack111l111_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧẻ"))
    @staticmethod
    def bstack11111ll1l1l_opy_():
        attempt = 0
        while (attempt < bstack11111lll111_opy_):
            attempt += 1
            if os.path.exists(bstack1llllll1ll_opy_+bstack111l111_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨẼ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1l1l11l_opy_(label: str) -> str:
        try:
            return bstack111l111_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢẽ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧẾ").format(e))