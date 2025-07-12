# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
logger = get_logger(__name__)
bstack11111ll1lll_opy_: Dict[str, float] = {}
bstack11111lll11l_opy_: List = []
bstack11111ll1ll1_opy_ = 5
bstack1ll1ll1ll1_opy_ = os.path.join(os.getcwd(), bstack11l1111_opy_ (u"ࠩ࡯ࡳ࡬࠭Ả"), bstack11l1111_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ả"))
logging.getLogger(bstack11l1111_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭Ấ")).setLevel(logging.WARNING)
lock = FileLock(bstack1ll1ll1ll1_opy_+bstack11l1111_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦấ"))
class bstack11111ll1l1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack11111lll1ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11111lll1ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1111_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢẦ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1l1l11l_opy_:
    global bstack11111ll1lll_opy_
    @staticmethod
    def bstack1llll1lllll_opy_(key: str):
        bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack11l1l1111ll_opy_(key)
        bstack1lll1l1l11l_opy_.mark(bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢầ"))
        return bstack1lll1lll11l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11111ll1lll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦẨ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1l1l11l_opy_.mark(end)
            bstack1lll1l1l11l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨẩ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11111ll1lll_opy_ or end not in bstack11111ll1lll_opy_:
                logger.debug(bstack11l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧẪ").format(start,end))
                return
            duration: float = bstack11111ll1lll_opy_[end] - bstack11111ll1lll_opy_[start]
            bstack11111llll11_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢẫ"), bstack11l1111_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦẬ")).lower() == bstack11l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦậ")
            bstack11111ll11ll_opy_: bstack11111ll1l1l_opy_ = bstack11111ll1l1l_opy_(duration, label, bstack11111ll1lll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢẮ"), 0), command, test_name, hook_type, bstack11111llll11_opy_)
            del bstack11111ll1lll_opy_[start]
            del bstack11111ll1lll_opy_[end]
            bstack1lll1l1l11l_opy_.bstack11111lll111_opy_(bstack11111ll11ll_opy_)
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦắ").format(e))
    @staticmethod
    def bstack11111lll111_opy_(bstack11111ll11ll_opy_):
        os.makedirs(os.path.dirname(bstack1ll1ll1ll1_opy_)) if not os.path.exists(os.path.dirname(bstack1ll1ll1ll1_opy_)) else None
        bstack1lll1l1l11l_opy_.bstack11111ll1l11_opy_()
        try:
            with lock:
                with open(bstack1ll1ll1ll1_opy_, bstack11l1111_opy_ (u"ࠤࡵ࠯ࠧẰ"), encoding=bstack11l1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤằ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11111ll11ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11111lll1l1_opy_:
            logger.debug(bstack11l1111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣẲ").format(bstack11111lll1l1_opy_))
            with lock:
                with open(bstack1ll1ll1ll1_opy_, bstack11l1111_opy_ (u"ࠧࡽࠢẳ"), encoding=bstack11l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧẴ")) as file:
                    data = [bstack11111ll11ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥẵ").format(str(e)))
        finally:
            if os.path.exists(bstack1ll1ll1ll1_opy_+bstack11l1111_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢẶ")):
                os.remove(bstack1ll1ll1ll1_opy_+bstack11l1111_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣặ"))
    @staticmethod
    def bstack11111ll1l11_opy_():
        attempt = 0
        while (attempt < bstack11111ll1ll1_opy_):
            attempt += 1
            if os.path.exists(bstack1ll1ll1ll1_opy_+bstack11l1111_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤẸ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11l1l1111ll_opy_(label: str) -> str:
        try:
            return bstack11l1111_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥẹ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣẺ").format(e))