# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
import threading
from bstack_utils.bstack111llll1ll_opy_ import get_logger
logger = get_logger(__name__)
bstack1llll11lllll_opy_: Dict[str, float] = {}
bstack1llll1l11l1l_opy_: List = []
bstack1llll1l1111l_opy_ = 2
bstack11ll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1111_opy_ (u"࠭࡬ࡰࡩࠪ€"), bstack1l1111_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ₭"))
logging.getLogger(bstack1l1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠪ₮")).setLevel(logging.WARNING)
lock = FileLock(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ₯"))
class bstack1llll1l11111_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack1llll1l11lll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1llll1l11lll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1111_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࠦ₰")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack11ll111lll_opy_:
    global bstack1llll11lllll_opy_
    @staticmethod
    def bstack111llllll_opy_(key: str):
        bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack11l1ll11111_opy_(key)
        bstack11ll111lll_opy_.mark(bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ₱"))
        return bstack1ll1111lll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1llll11lllll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ₲").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack11ll111lll_opy_.mark(end)
            bstack11ll111lll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥ₳").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1llll11lllll_opy_ or end not in bstack1llll11lllll_opy_:
                logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠥࡵࡲࠡࡧࡱࡨࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠤ₴").format(start,end))
                return
            duration: float = bstack1llll11lllll_opy_[end] - bstack1llll11lllll_opy_[start]
            bstack1llll1l1l111_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦ₵"), bstack1l1111_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ₶")).lower() == bstack1l1111_opy_ (u"ࠥࡸࡷࡻࡥࠣ₷")
            bstack1llll1l11ll1_opy_: bstack1llll1l11111_opy_ = bstack1llll1l11111_opy_(duration, label, bstack1llll11lllll_opy_[start], bstack1l1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ₸").format(threading.get_ident(), os.getpid()), status, failure, details, os.environ.get(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧ₹"), 0), command, test_name, hook_type, bstack1llll1l1l111_opy_)
            del bstack1llll11lllll_opy_[start]
            del bstack1llll11lllll_opy_[end]
            bstack11ll111lll_opy_.bstack1llll1l1l11l_opy_(bstack1llll1l11ll1_opy_)
            try:
                bstack1llll1l11l11_opy_ = time.time_ns() / 1000000
                bstack1llll1l111ll_opy_ = bstack1llll1l11l11_opy_ - bstack1llll1l11ll1_opy_.startTime
                bstack1llll1l11ll1_opy_.duration = bstack1llll1l111ll_opy_
                bstack11ll111lll_opy_.update_last_metric_duration(bstack1llll1l11ll1_opy_)
            except Exception as e:
                logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡺࡶࡤࡢࡶ࡬ࡲ࡬ࠦ࡭ࡦࡶࡵ࡭ࡨࠦࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡣࡩࡸࡪࡸࠠࡱࡧࡵࡷ࡮ࡹࡴࡦࡰࡦࡩ࠿ࠦࡻࡾࠤ₺").format(e))
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥ₻").format(e))
    @staticmethod
    def bstack1llll1l1l11l_opy_(bstack1llll1l11ll1_opy_):
        os.makedirs(os.path.dirname(bstack11ll1ll1l1_opy_)) if not os.path.exists(os.path.dirname(bstack11ll1ll1l1_opy_)) else None
        bstack11ll111lll_opy_.bstack1llll1l111l1_opy_()
        try:
            with lock:
                with open(bstack11ll1ll1l1_opy_, bstack1l1111_opy_ (u"ࠣࡴ࠮ࠦ₼"), encoding=bstack1l1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ₽")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1llll1l11ll1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1llll11llll1_opy_:
            logger.debug(bstack1l1111_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢ₾").format(bstack1llll11llll1_opy_))
            with lock:
                with open(bstack11ll1ll1l1_opy_, bstack1l1111_opy_ (u"ࠦࡼࠨ₿"), encoding=bstack1l1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ⃀")) as file:
                    data = [bstack1llll1l11ll1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤ⃁").format(str(e)))
        finally:
            if os.path.exists(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ⃂")):
                os.remove(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ⃃"))
    @staticmethod
    def update_last_metric_duration(bstack1llll1l11ll1_opy_):
        try:
            bstack11ll111lll_opy_.bstack1llll1l111l1_opy_()
            with lock:
                try:
                    with open(bstack11ll1ll1l1_opy_, bstack1l1111_opy_ (u"ࠤࡵ࠯ࠧ⃄"), encoding=bstack1l1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ⃅")) as file:
                        try:
                            data = json.load(file)
                        except Exception:
                            data = []
                        if isinstance(data, list) and len(data) > 0:
                            data[-1][bstack1l1111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⃆")] = bstack1llll1l11ll1_opy_.duration
                            file.seek(0)
                            file.truncate()
                            json.dump(data, file, indent=4)
                except FileNotFoundError:
                    return
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡ࡮ࡤࡷࡹࠦ࡭ࡦࡶࡵ࡭ࡨࠦࡤࡶࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ⃇").format(e))
        finally:
            if os.path.exists(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ⃈")):
                os.remove(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ⃉"))
    @staticmethod
    def bstack1llll1l111l1_opy_():
        attempt = 0
        while (attempt < bstack1llll1l1111l_opy_):
            attempt += 1
            if os.path.exists(bstack11ll1ll1l1_opy_+bstack1l1111_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ⃊")):
                time.sleep(0.01)
            else:
                break
    @staticmethod
    def bstack11l1ll11111_opy_(label: str) -> str:
        try:
            return bstack1l1111_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣ⃋").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⃌").format(e))