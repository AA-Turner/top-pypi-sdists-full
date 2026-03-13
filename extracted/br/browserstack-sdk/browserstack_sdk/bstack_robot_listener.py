# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1llllll1l11_opy_ import RobotHandler
from bstack_utils.capture import bstack11111l1l11_opy_
from bstack_utils.test_data import bstack111111111l_opy_, bstack111111llll_opy_, TestData
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l11l11l11_opy_, current_time, Result, \
    error_handler, bstack1lllll1111l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫႵ"): [],
        bstack1111l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧႶ"): [],
        bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭Ⴗ"): []
    }
    bstack1lllll1l111_opy_ = []
    bstack1llllll11ll_opy_ = []
    @staticmethod
    def bstack111111l1l1_opy_(log):
        if not ((isinstance(log[bstack1111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႸ")], list) or (isinstance(log[bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႹ")], dict)) and len(log[bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴚ")])>0) or (isinstance(log[bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႻ")], str) and log[bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႼ")].strip())):
            return
        active = bstack11l11ll1l1_opy_.bstack1111111lll_opy_()
        log = {
            bstack1111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧႽ"): log[bstack1111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨႾ")],
            bstack1111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ⴟ"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠫ࡟࠭Ⴠ"),
            bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴡ"): log[bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧჂ")],
        }
        if active:
            if active[bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬჃ")] == bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭Ⴤ"):
                log[bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩჅ")] = active[bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ჆")]
            elif active[bstack1111l_opy_ (u"ࠫࡹࡿࡰࡦࠩჇ")] == bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࠪ჈"):
                log[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭჉")] = active[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ჊")]
        TestHubHandler.bstack1l1l1111l_opy_([log])
    def __init__(self):
        self.messages = bstack1llll1ll1l1_opy_()
        self._1llllllll11_opy_ = None
        self._1lllllll11l_opy_ = None
        self._1111111111_opy_ = OrderedDict()
        self.bstack11111ll1l1_opy_ = bstack11111l1l11_opy_(self.bstack111111l1l1_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lllll1llll_opy_()
        if not self._1111111111_opy_.get(attrs.get(bstack1111l_opy_ (u"ࠨ࡫ࡧࠫ჋")), None):
            self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠩ࡬ࡨࠬ჌"))] = {}
        bstack1lllll111ll_opy_ = TestData(
                bstack1lllll1ll11_opy_=attrs.get(bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭Ⴭ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ჎")], start=os.getcwd()) if attrs.get(bstack1111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ჏")) != bstack1111l_opy_ (u"࠭ࠧა") else bstack1111l_opy_ (u"ࠧࠨბ"),
                framework=bstack1111l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧგ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1111l_opy_ (u"ࠩ࡬ࡨࠬდ"), None)
        self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭ე"))][bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧვ")] = bstack1lllll111ll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llllllllll_opy_()
        self._1lllll11l11_opy_(messages)
        with self._lock:
            for bstack1lllllllll1_opy_ in self.bstack1lllll1l111_opy_:
                bstack1lllllllll1_opy_[bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧზ")][bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬთ")].extend(self.store[bstack1111l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ი")])
                TestHubHandler.bstack111lllllll_opy_(bstack1lllllllll1_opy_)
            self.bstack1lllll1l111_opy_ = []
            self.store[bstack1111l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧკ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11111ll1l1_opy_.start()
        if not self._1111111111_opy_.get(attrs.get(bstack1111l_opy_ (u"ࠩ࡬ࡨࠬლ")), None):
            self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭მ"))] = {}
        driver = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪნ"), None)
        test_data = TestData(
            bstack1lllll1ll11_opy_=attrs.get(bstack1111l_opy_ (u"ࠬ࡯ࡤࠨო")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭პ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lllll11ll1_opy_(attrs.get(bstack1111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧჟ"), None)),
            framework=bstack1111l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧრ"),
            tags=attrs[bstack1111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧს")],
            hooks=self.store[bstack1111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩტ")],
            integrations=TestHubHandler.bstack11111ll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1111l_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨუ").format(bstack1111l_opy_ (u"ࠧࠦࠢფ").join(attrs[bstack1111l_opy_ (u"࠭ࡴࡢࡩࡶࠫქ")]), name) if attrs[bstack1111l_opy_ (u"ࠧࡵࡣࡪࡷࠬღ")] else name
        )
        self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠨ࡫ࡧࠫყ"))][bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬშ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llll1lll11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭ჩ"), None)
        self.send_run_event(bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬც"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11111ll1l1_opy_.reset()
        bstack1lllllll111_opy_ = bstack1lllll1l1l1_opy_.get(attrs.get(bstack1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬძ")), bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧწ"))
        self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠧࡪࡦࠪჭ"))][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫხ")].stop(time=current_time(), duration=int(attrs.get(bstack1111l_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧჯ"), bstack1111l_opy_ (u"ࠪ࠴ࠬჰ"))), result=Result(result=bstack1lllllll111_opy_, exception=attrs.get(bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჱ")), bstack11111l1111_opy_=[attrs.get(bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ჲ"))]))
        self.send_run_event(bstack1111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨჳ"), self._1111111111_opy_[attrs.get(bstack1111l_opy_ (u"ࠧࡪࡦࠪჴ"))][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫჵ")], True)
        with self._lock:
            self.store[bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ჶ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lllll1llll_opy_()
        current_test_id = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬჷ"), None)
        bstack1lllll11lll_opy_ = current_test_id if bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ჸ"), None) else bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨჹ"), None)
        if attrs.get(bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫჺ"), bstack1111l_opy_ (u"ࠧࠨ჻")).lower() in [bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧჼ"), bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫჽ")]:
            hook_type = bstack1lllll1ll1l_opy_(attrs.get(bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨჾ")), bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨჿ"), None))
            hook_name = bstack1111l_opy_ (u"ࠬࢁࡽࠨᄀ").format(attrs.get(bstack1111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᄁ"), bstack1111l_opy_ (u"ࠧࠨᄂ")))
            if hook_type in [bstack1111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᄃ"), bstack1111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᄄ")]:
                hook_name = bstack1111l_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫᄅ").format(bstack1llll1ll11l_opy_.get(hook_type), attrs.get(bstack1111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᄆ"), bstack1111l_opy_ (u"ࠬ࠭ᄇ")))
            bstack1llll1ll1ll_opy_ = bstack111111llll_opy_(
                bstack1lllll1ll11_opy_=bstack1lllll11lll_opy_ + bstack1111l_opy_ (u"࠭࠭ࠨᄈ") + attrs.get(bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᄉ"), bstack1111l_opy_ (u"ࠨࠩᄊ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᄋ")), start=os.getcwd()),
                framework=bstack1111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩᄌ"),
                tags=attrs[bstack1111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᄍ")],
                scope=RobotHandler.bstack1lllll11ll1_opy_(attrs.get(bstack1111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᄎ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1llll1ll1ll_opy_.bstack1llll1lll11_opy_()
            threading.current_thread().current_hook_id = bstack1lllll11lll_opy_ + bstack1111l_opy_ (u"࠭࠭ࠨᄏ") + attrs.get(bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᄐ"), bstack1111l_opy_ (u"ࠨࠩᄑ")).lower()
            with self._lock:
                self.store[bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᄒ")] = [bstack1llll1ll1ll_opy_.bstack1llll1lll11_opy_()]
                if bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᄓ"), None):
                    self.store[bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨᄔ")].append(bstack1llll1ll1ll_opy_.bstack1llll1lll11_opy_())
                else:
                    self.store[bstack1111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᄕ")].append(bstack1llll1ll1ll_opy_.bstack1llll1lll11_opy_())
            if bstack1lllll11lll_opy_:
                self._1111111111_opy_[bstack1lllll11lll_opy_ + bstack1111l_opy_ (u"࠭࠭ࠨᄖ") + attrs.get(bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᄗ"), bstack1111l_opy_ (u"ࠨࠩᄘ")).lower()] = { bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄙ"): bstack1llll1ll1ll_opy_ }
            TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᄚ"), bstack1llll1ll1ll_opy_)
        else:
            bstack111111l1ll_opy_ = {
                bstack1111l_opy_ (u"ࠫ࡮ࡪࠧᄛ"): uuid4().__str__(),
                bstack1111l_opy_ (u"ࠬࡺࡥࡹࡶࠪᄜ"): bstack1111l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬᄝ").format(attrs.get(bstack1111l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᄞ")), attrs.get(bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᄟ"), bstack1111l_opy_ (u"ࠩࠪᄠ"))) if attrs.get(bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᄡ"), []) else attrs.get(bstack1111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᄢ")),
                bstack1111l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᄣ"): attrs.get(bstack1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᄤ"), []),
                bstack1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᄥ"): current_time(),
                bstack1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᄦ"): bstack1111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᄧ"),
                bstack1111l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᄨ"): attrs.get(bstack1111l_opy_ (u"ࠫࡩࡵࡣࠨᄩ"), bstack1111l_opy_ (u"ࠬ࠭ᄪ"))
            }
            if attrs.get(bstack1111l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧᄫ"), bstack1111l_opy_ (u"ࠧࠨᄬ")) != bstack1111l_opy_ (u"ࠨࠩᄭ"):
                bstack111111l1ll_opy_[bstack1111l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᄮ")] = attrs.get(bstack1111l_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫᄯ"))
            if not self.bstack1llllll11ll_opy_:
                self._1111111111_opy_[self._1llllll1l1l_opy_()][bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᄰ")].add_step(bstack111111l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack111111l1ll_opy_[bstack1111l_opy_ (u"ࠬ࡯ࡤࠨᄱ")]
            self.bstack1llllll11ll_opy_.append(bstack111111l1ll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llllllllll_opy_()
        self._1lllll11l11_opy_(messages)
        current_test_id = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᄲ"), None)
        bstack1lllll11lll_opy_ = current_test_id if current_test_id else bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪᄳ"), None)
        bstack1llll1llll1_opy_ = bstack1lllll1l1l1_opy_.get(attrs.get(bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᄴ")), bstack1111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᄵ"))
        bstack1llllllll1l_opy_ = attrs.get(bstack1111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄶ"))
        if bstack1llll1llll1_opy_ != bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᄷ") and not attrs.get(bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄸ")) and self._1llllllll11_opy_:
            bstack1llllllll1l_opy_ = self._1llllllll11_opy_
        bstack11111l1lll_opy_ = Result(result=bstack1llll1llll1_opy_, exception=bstack1llllllll1l_opy_, bstack11111l1111_opy_=[bstack1llllllll1l_opy_])
        if attrs.get(bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᄹ"), bstack1111l_opy_ (u"ࠧࠨᄺ")).lower() in [bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᄻ"), bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᄼ")]:
            bstack1lllll11lll_opy_ = current_test_id if current_test_id else bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᄽ"), None)
            if bstack1lllll11lll_opy_:
                bstack111111l111_opy_ = bstack1lllll11lll_opy_ + bstack1111l_opy_ (u"ࠦ࠲ࠨᄾ") + attrs.get(bstack1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᄿ"), bstack1111l_opy_ (u"࠭ࠧᅀ")).lower()
                self._1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᅁ")].stop(time=current_time(), duration=int(attrs.get(bstack1111l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᅂ"), bstack1111l_opy_ (u"ࠩ࠳ࠫᅃ"))), result=bstack11111l1lll_opy_)
                TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᅄ"), self._1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᅅ")])
        else:
            bstack1lllll11lll_opy_ = current_test_id if current_test_id else bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧᅆ"), None)
            if bstack1lllll11lll_opy_ and len(self.bstack1llllll11ll_opy_) == 1:
                current_step_uuid = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪᅇ"), None)
                self._1111111111_opy_[bstack1lllll11lll_opy_][bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᅈ")].bstack11111ll11l_opy_(current_step_uuid, duration=int(attrs.get(bstack1111l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᅉ"), bstack1111l_opy_ (u"ࠩ࠳ࠫᅊ"))), result=bstack11111l1lll_opy_)
            else:
                self.bstack1111111l1l_opy_(attrs)
            self.bstack1llllll11ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1111l_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨᅋ"), bstack1111l_opy_ (u"ࠫࡳࡵࠧᅌ")) == bstack1111l_opy_ (u"ࠬࡿࡥࡴࠩᅍ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l11ll1l1_opy_.bstack1111111lll_opy_():
                logs.append({
                    bstack1111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᅎ"): current_time(),
                    bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅏ"): message.get(bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅐ")),
                    bstack1111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᅑ"): message.get(bstack1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᅒ")),
                    **bstack11l11ll1l1_opy_.bstack1111111lll_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1l1l1111l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack11111111ll_opy_()
    def bstack1111111l1l_opy_(self, bstack1llllll1ll1_opy_):
        if not bstack11l11ll1l1_opy_.bstack1111111lll_opy_():
            return
        kwname = bstack1111l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᅓ").format(bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᅔ")), bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᅕ"), bstack1111l_opy_ (u"ࠧࠨᅖ"))) if bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᅗ"), []) else bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᅘ"))
        error_message = bstack1111l_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤᅙ").format(kwname, bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᅚ")), str(bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅛ"))))
        bstack1llllll1lll_opy_ = bstack1111l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧᅜ").format(kwname, bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᅝ")))
        bstack1lllll111l1_opy_ = error_message if bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅞ")) else bstack1llllll1lll_opy_
        bstack1lllll11111_opy_ = {
            bstack1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᅟ"): self.bstack1llllll11ll_opy_[-1].get(bstack1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᅠ"), current_time()),
            bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅡ"): bstack1lllll111l1_opy_,
            bstack1111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᅢ"): bstack1111l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᅣ") if bstack1llllll1ll1_opy_.get(bstack1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᅤ")) == bstack1111l_opy_ (u"ࠨࡈࡄࡍࡑ࠭ᅥ") else bstack1111l_opy_ (u"ࠩࡌࡒࡋࡕࠧᅦ"),
            **bstack11l11ll1l1_opy_.bstack1111111lll_opy_()
        }
        TestHubHandler.bstack1l1l1111l_opy_([bstack1lllll11111_opy_])
    def _1llllll1l1l_opy_(self):
        for bstack1lllll1ll11_opy_ in reversed(self._1111111111_opy_):
            bstack1llll1lllll_opy_ = bstack1lllll1ll11_opy_
            data = self._1111111111_opy_[bstack1lllll1ll11_opy_][bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᅧ")]
            if isinstance(data, bstack111111llll_opy_):
                if not bstack1111l_opy_ (u"ࠫࡊࡇࡃࡉࠩᅨ") in data.bstack1llllll1111_opy_():
                    return bstack1llll1lllll_opy_
            else:
                return bstack1llll1lllll_opy_
    def _1lllll11l11_opy_(self, messages):
        try:
            bstack1lllll1lll1_opy_ = BuiltIn().get_variable_value(bstack1111l_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦᅩ")) in (bstack1llll1ll111_opy_.DEBUG, bstack1llll1ll111_opy_.TRACE)
            for message, bstack1lllllll1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅪ"))
                level = message.get(bstack1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᅫ"))
                if level == bstack1llll1ll111_opy_.FAIL:
                    self._1llllllll11_opy_ = name or self._1llllllll11_opy_
                    self._1lllllll11l_opy_ = bstack1lllllll1l1_opy_.get(bstack1111l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᅬ")) if bstack1lllll1lll1_opy_ and bstack1lllllll1l1_opy_ else self._1lllllll11l_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1lllll1l1ll_opy_: bstack111111111l_opy_, bstack1111111ll1_opy_=False):
        if event == bstack1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᅭ"):
            bstack1lllll1l1ll_opy_.set(hooks=self.store[bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧᅮ")])
        if event == bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᅯ"):
            event = bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᅰ")
        if bstack1111111ll1_opy_:
            bstack1llll1lll1l_opy_ = {
                bstack1111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᅱ"): event,
                bstack1lllll1l1ll_opy_.bstack1lllllll1ll_opy_(): bstack1lllll1l1ll_opy_.bstack11111111l1_opy_(event)
            }
            with self._lock:
                self.bstack1lllll1l111_opy_.append(bstack1llll1lll1l_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1lllll1l1ll_opy_)
class bstack1llll1ll1l1_opy_:
    def __init__(self):
        self._1llllll111l_opy_ = []
    def bstack1lllll1llll_opy_(self):
        self._1llllll111l_opy_.append([])
    def bstack1llllllllll_opy_(self):
        return self._1llllll111l_opy_.pop() if self._1llllll111l_opy_ else list()
    def push(self, message):
        self._1llllll111l_opy_[-1].append(message) if self._1llllll111l_opy_ else self._1llllll111l_opy_.append([message])
class bstack1llll1ll111_opy_:
    FAIL = bstack1111l_opy_ (u"ࠧࡇࡃࡌࡐࠬᅲ")
    ERROR = bstack1111l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧᅳ")
    WARNING = bstack1111l_opy_ (u"࡚ࠩࡅࡗࡔࠧᅴ")
    bstack1llllll11l1_opy_ = bstack1111l_opy_ (u"ࠪࡍࡓࡌࡏࠨᅵ")
    DEBUG = bstack1111l_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪᅶ")
    TRACE = bstack1111l_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫᅷ")
    bstack1111111l11_opy_ = [FAIL, ERROR]
def bstack1lllll11l1l_opy_(bstack1lllll1l11l_opy_):
    if not bstack1lllll1l11l_opy_:
        return None
    if bstack1lllll1l11l_opy_.get(bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅸ"), None):
        return getattr(bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᅹ")], bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᅺ"), None)
    return bstack1lllll1l11l_opy_.get(bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᅻ"), None)
def bstack1lllll1ll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᅼ"), bstack1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᅽ")]:
        return
    if hook_type.lower() == bstack1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᅾ"):
        if current_test_uuid is None:
            return bstack1111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᅿ")
        else:
            return bstack1111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᆀ")
    elif hook_type.lower() == bstack1111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᆁ"):
        if current_test_uuid is None:
            return bstack1111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᆂ")
        else:
            return bstack1111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᆃ")