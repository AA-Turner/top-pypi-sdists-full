# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll1llllll_opy_ import RobotHandler
from bstack_utils.capture import bstack1lllll11l1l_opy_
from bstack_utils.test_data import bstack1llll11l111_opy_, bstack1lllll1l111_opy_, TestData
from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l11lll1_opy_, current_time, Result, \
    error_handler, bstack1llll1l1111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨჸ"): [],
        bstack1ll1lll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫჹ"): [],
        bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪჺ"): []
    }
    bstack1lll1llll1l_opy_ = []
    bstack1lll1ll11ll_opy_ = []
    @staticmethod
    def bstack1lllll11l11_opy_(log):
        if not ((isinstance(log[bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ჻")], list) or (isinstance(log[bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩჼ")], dict)) and len(log[bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪჽ")])>0) or (isinstance(log[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫჾ")], str) and log[bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჿ")].strip())):
            return
        active = bstack11llll1l_opy_.bstack1llll1lll11_opy_()
        log = {
            bstack1ll1lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᄀ"): log[bstack1ll1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᄁ")],
            bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᄂ"): bstack1llll1l1111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠨ࡜ࠪᄃ"),
            bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᄄ"): log[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄅ")],
        }
        if active:
            if active[bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᄆ")] == bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᄇ"):
                log[bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᄈ")] = active[bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᄉ")]
            elif active[bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᄊ")] == bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧᄋ"):
                log[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᄌ")] = active[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᄍ")]
        TestHubHandler.bstack11111l1l1l_opy_([log])
    def __init__(self):
        self.messages = bstack1lll1lll11l_opy_()
        self._1llll1111l1_opy_ = None
        self._1llll11ll11_opy_ = None
        self._1llll1l11ll_opy_ = OrderedDict()
        self.bstack1lllll1ll11_opy_ = bstack1lllll11l1l_opy_(self.bstack1lllll11l11_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llll1ll1l1_opy_()
        if not self._1llll1l11ll_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨᄎ")), None):
            self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᄏ"))] = {}
        bstack1llll111111_opy_ = TestData(
                bstack1llll11lll1_opy_=attrs.get(bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪᄐ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1ll1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᄑ")], start=os.getcwd()) if attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᄒ")) != bstack1ll1lll_opy_ (u"ࠪࠫᄓ") else bstack1ll1lll_opy_ (u"ࠫࠬᄔ"),
                framework=bstack1ll1lll_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫᄕ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᄖ"), None)
        self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪᄗ"))][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᄘ")] = bstack1llll111111_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll1ll1l11_opy_()
        self._1llll1l11l1_opy_(messages)
        with self._lock:
            for bstack1llll111l1l_opy_ in self.bstack1lll1llll1l_opy_:
                bstack1llll111l1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᄙ")][bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᄚ")].extend(self.store[bstack1ll1lll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪᄛ")])
                TestHubHandler.bstack1lll11l111_opy_(bstack1llll111l1l_opy_)
            self.bstack1lll1llll1l_opy_ = []
            self.store[bstack1ll1lll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᄜ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lllll1ll11_opy_.start()
        if not self._1llll1l11ll_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᄝ")), None):
            self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪᄞ"))] = {}
        driver = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᄟ"), None)
        test_data = TestData(
            bstack1llll11lll1_opy_=attrs.get(bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬᄠ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᄡ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1ll11l1_opy_(attrs.get(bstack1ll1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᄢ"), None)),
            framework=bstack1ll1lll_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫᄣ"),
            tags=attrs[bstack1ll1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᄤ")],
            hooks=self.store[bstack1ll1lll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ᄥ")],
            integrations=TestHubHandler.bstack1lllll1l11l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1lll_opy_ (u"ࠣࡽࢀࠤࡡࡴࠠࡼࡿࠥᄦ").format(bstack1ll1lll_opy_ (u"ࠤࠣࠦᄧ").join(attrs[bstack1ll1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᄨ")]), name) if attrs[bstack1ll1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩᄩ")] else name
        )
        self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨᄪ"))][bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᄫ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llll11111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪᄬ"), None)
        self.send_run_event(bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᄭ"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lllll1ll11_opy_.reset()
        bstack1llll111l11_opy_ = bstack1llll1ll11l_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᄮ")), bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᄯ"))
        self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᄰ"))][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄱ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll1lll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᄲ"), bstack1ll1lll_opy_ (u"ࠧ࠱ࠩᄳ"))), result=Result(result=bstack1llll111l11_opy_, exception=attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᄴ")), bstack1llll1llll1_opy_=[attrs.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᄵ"))]))
        self.send_run_event(bstack1ll1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᄶ"), self._1llll1l11ll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᄷ"))][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄸ")], True)
        with self._lock:
            self.store[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪᄹ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llll1ll1l1_opy_()
        current_test_id = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩᄺ"), None)
        bstack1lll1l1lll1_opy_ = current_test_id if bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪᄻ"), None) else bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬᄼ"), None)
        if attrs.get(bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨᄽ"), bstack1ll1lll_opy_ (u"ࠫࠬᄾ")).lower() in [bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᄿ"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᅀ")]:
            hook_type = bstack1llll1ll1ll_opy_(attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬᅁ")), bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᅂ"), None))
            hook_name = bstack1ll1lll_opy_ (u"ࠩࡾࢁࠬᅃ").format(attrs.get(bstack1ll1lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᅄ"), bstack1ll1lll_opy_ (u"ࠫࠬᅅ")))
            if hook_type in [bstack1ll1lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᅆ"), bstack1ll1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᅇ")]:
                hook_name = bstack1ll1lll_opy_ (u"ࠧ࡜ࡽࢀࡡࠥࢁࡽࠨᅈ").format(bstack1llll11l1ll_opy_.get(hook_type), attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨᅉ"), bstack1ll1lll_opy_ (u"ࠩࠪᅊ")))
            bstack1llll11l11l_opy_ = bstack1lllll1l111_opy_(
                bstack1llll11lll1_opy_=bstack1lll1l1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠪ࠱ࠬᅋ") + attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᅌ"), bstack1ll1lll_opy_ (u"ࠬ࠭ᅍ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᅎ")), start=os.getcwd()),
                framework=bstack1ll1lll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ᅏ"),
                tags=attrs[bstack1ll1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᅐ")],
                scope=RobotHandler.bstack1lll1ll11l1_opy_(attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᅑ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1llll11l11l_opy_.bstack1llll11111l_opy_()
            threading.current_thread().current_hook_id = bstack1lll1l1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠪ࠱ࠬᅒ") + attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᅓ"), bstack1ll1lll_opy_ (u"ࠬ࠭ᅔ")).lower()
            with self._lock:
                self.store[bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᅕ")] = [bstack1llll11l11l_opy_.bstack1llll11111l_opy_()]
                if bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᅖ"), None):
                    self.store[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬᅗ")].append(bstack1llll11l11l_opy_.bstack1llll11111l_opy_())
                else:
                    self.store[bstack1ll1lll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨᅘ")].append(bstack1llll11l11l_opy_.bstack1llll11111l_opy_())
            if bstack1lll1l1lll1_opy_:
                self._1llll1l11ll_opy_[bstack1lll1l1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠪ࠱ࠬᅙ") + attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᅚ"), bstack1ll1lll_opy_ (u"ࠬ࠭ᅛ")).lower()] = { bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅜ"): bstack1llll11l11l_opy_ }
            TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᅝ"), bstack1llll11l11l_opy_)
        else:
            bstack1llll1lll1l_opy_ = {
                bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫᅞ"): uuid4().__str__(),
                bstack1ll1lll_opy_ (u"ࠩࡷࡩࡽࡺࠧᅟ"): bstack1ll1lll_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩᅠ").format(attrs.get(bstack1ll1lll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᅡ")), attrs.get(bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪᅢ"), bstack1ll1lll_opy_ (u"࠭ࠧᅣ"))) if attrs.get(bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᅤ"), []) else attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨᅥ")),
                bstack1ll1lll_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩᅦ"): attrs.get(bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᅧ"), []),
                bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᅨ"): current_time(),
                bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᅩ"): bstack1ll1lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᅪ"),
                bstack1ll1lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᅫ"): attrs.get(bstack1ll1lll_opy_ (u"ࠨࡦࡲࡧࠬᅬ"), bstack1ll1lll_opy_ (u"ࠩࠪᅭ"))
            }
            if attrs.get(bstack1ll1lll_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫᅮ"), bstack1ll1lll_opy_ (u"ࠫࠬᅯ")) != bstack1ll1lll_opy_ (u"ࠬ࠭ᅰ"):
                bstack1llll1lll1l_opy_[bstack1ll1lll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᅱ")] = attrs.get(bstack1ll1lll_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨᅲ"))
            if not self.bstack1lll1ll11ll_opy_:
                self._1llll1l11ll_opy_[self._1llll1l1lll_opy_()][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅳ")].add_step(bstack1llll1lll1l_opy_)
                threading.current_thread().current_step_uuid = bstack1llll1lll1l_opy_[bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬᅴ")]
            self.bstack1lll1ll11ll_opy_.append(bstack1llll1lll1l_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll1ll1l11_opy_()
        self._1llll1l11l1_opy_(messages)
        current_test_id = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᅵ"), None)
        bstack1lll1l1lll1_opy_ = current_test_id if current_test_id else bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧᅶ"), None)
        bstack1lll1ll111l_opy_ = bstack1llll1ll11l_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᅷ")), bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᅸ"))
        bstack1lll1ll1l1l_opy_ = attrs.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅹ"))
        if bstack1lll1ll111l_opy_ != bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᅺ") and not attrs.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᅻ")) and self._1llll1111l1_opy_:
            bstack1lll1ll1l1l_opy_ = self._1llll1111l1_opy_
        bstack1lllll11111_opy_ = Result(result=bstack1lll1ll111l_opy_, exception=bstack1lll1ll1l1l_opy_, bstack1llll1llll1_opy_=[bstack1lll1ll1l1l_opy_])
        if attrs.get(bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨᅼ"), bstack1ll1lll_opy_ (u"ࠫࠬᅽ")).lower() in [bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᅾ"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᅿ")]:
            bstack1lll1l1lll1_opy_ = current_test_id if current_test_id else bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪᆀ"), None)
            if bstack1lll1l1lll1_opy_:
                bstack1lllll1l1l1_opy_ = bstack1lll1l1lll1_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠯ࠥᆁ") + attrs.get(bstack1ll1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᆂ"), bstack1ll1lll_opy_ (u"ࠪࠫᆃ")).lower()
                self._1llll1l11ll_opy_[bstack1lllll1l1l1_opy_][bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆄ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪᆅ"), bstack1ll1lll_opy_ (u"࠭࠰ࠨᆆ"))), result=bstack1lllll11111_opy_)
                TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᆇ"), self._1llll1l11ll_opy_[bstack1lllll1l1l1_opy_][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᆈ")])
        else:
            bstack1lll1l1lll1_opy_ = current_test_id if current_test_id else bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠ࡫ࡧࠫᆉ"), None)
            if bstack1lll1l1lll1_opy_ and len(self.bstack1lll1ll11ll_opy_) == 1:
                current_step_uuid = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧᆊ"), None)
                self._1llll1l11ll_opy_[bstack1lll1l1lll1_opy_][bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆋ")].bstack1lllll11ll1_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪᆌ"), bstack1ll1lll_opy_ (u"࠭࠰ࠨᆍ"))), result=bstack1lllll11111_opy_)
            else:
                self.bstack1llll111ll1_opy_(attrs)
            self.bstack1lll1ll11ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1lll_opy_ (u"ࠧࡩࡶࡰࡰࠬᆎ"), bstack1ll1lll_opy_ (u"ࠨࡰࡲࠫᆏ")) == bstack1ll1lll_opy_ (u"ࠩࡼࡩࡸ࠭ᆐ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11llll1l_opy_.bstack1llll1lll11_opy_():
                logs.append({
                    bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᆑ"): current_time(),
                    bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᆒ"): message.get(bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆓ")),
                    bstack1ll1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᆔ"): message.get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᆕ")),
                    **bstack11llll1l_opy_.bstack1llll1lll11_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack11111l1l1l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll1lllll1_opy_()
    def bstack1llll111ll1_opy_(self, bstack1llll111lll_opy_):
        if not bstack11llll1l_opy_.bstack1llll1lll11_opy_():
            return
        kwname = bstack1ll1lll_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧᆖ").format(bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᆗ")), bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᆘ"), bstack1ll1lll_opy_ (u"ࠫࠬᆙ"))) if bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪᆚ"), []) else bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᆛ"))
        error_message = bstack1ll1lll_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠦࡼࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࡢࠢࡼ࠴ࢀࡠࠧࠨᆜ").format(kwname, bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᆝ")), str(bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᆞ"))))
        bstack1lll1ll1lll_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠤᆟ").format(kwname, bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᆠ")))
        bstack1llll11llll_opy_ = error_message if bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆡ")) else bstack1lll1ll1lll_opy_
        bstack1llll1l111l_opy_ = {
            bstack1ll1lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᆢ"): self.bstack1lll1ll11ll_opy_[-1].get(bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᆣ"), current_time()),
            bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᆤ"): bstack1llll11llll_opy_,
            bstack1ll1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᆥ"): bstack1ll1lll_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩᆦ") if bstack1llll111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᆧ")) == bstack1ll1lll_opy_ (u"ࠬࡌࡁࡊࡎࠪᆨ") else bstack1ll1lll_opy_ (u"࠭ࡉࡏࡈࡒࠫᆩ"),
            **bstack11llll1l_opy_.bstack1llll1lll11_opy_()
        }
        TestHubHandler.bstack11111l1l1l_opy_([bstack1llll1l111l_opy_])
    def _1llll1l1lll_opy_(self):
        for bstack1llll11lll1_opy_ in reversed(self._1llll1l11ll_opy_):
            bstack1lll1lll111_opy_ = bstack1llll11lll1_opy_
            data = self._1llll1l11ll_opy_[bstack1llll11lll1_opy_][bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆪ")]
            if isinstance(data, bstack1lllll1l111_opy_):
                if not bstack1ll1lll_opy_ (u"ࠨࡇࡄࡇࡍ࠭ᆫ") in data.bstack1llll1ll111_opy_():
                    return bstack1lll1lll111_opy_
            else:
                return bstack1lll1lll111_opy_
    def _1llll1l11l1_opy_(self, messages):
        try:
            bstack1llll1l1l1l_opy_ = BuiltIn().get_variable_value(bstack1ll1lll_opy_ (u"ࠤࠧࡿࡑࡕࡇࠡࡎࡈ࡚ࡊࡒࡽࠣᆬ")) in (bstack1lll1ll1ll1_opy_.DEBUG, bstack1lll1ll1ll1_opy_.TRACE)
            for message, bstack1lll1lll1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᆭ"))
                level = message.get(bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᆮ"))
                if level == bstack1lll1ll1ll1_opy_.FAIL:
                    self._1llll1111l1_opy_ = name or self._1llll1111l1_opy_
                    self._1llll11ll11_opy_ = bstack1lll1lll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᆯ")) if bstack1llll1l1l1l_opy_ and bstack1lll1lll1ll_opy_ else self._1llll11ll11_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1lll1l1ll1l_opy_: bstack1llll11l111_opy_, bstack1llll1111ll_opy_=False):
        if event == bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᆰ"):
            bstack1lll1l1ll1l_opy_.set(hooks=self.store[bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᆱ")])
        if event == bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᆲ"):
            event = bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᆳ")
        if bstack1llll1111ll_opy_:
            bstack1llll1l1l11_opy_ = {
                bstack1ll1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᆴ"): event,
                bstack1lll1l1ll1l_opy_.bstack1lll1l1llll_opy_(): bstack1lll1l1ll1l_opy_.bstack1llll11l1l1_opy_(event)
            }
            with self._lock:
                self.bstack1lll1llll1l_opy_.append(bstack1llll1l1l11_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1lll1l1ll1l_opy_)
class bstack1lll1lll11l_opy_:
    def __init__(self):
        self._1llll11ll1l_opy_ = []
    def bstack1llll1ll1l1_opy_(self):
        self._1llll11ll1l_opy_.append([])
    def bstack1lll1ll1l11_opy_(self):
        return self._1llll11ll1l_opy_.pop() if self._1llll11ll1l_opy_ else list()
    def push(self, message):
        self._1llll11ll1l_opy_[-1].append(message) if self._1llll11ll1l_opy_ else self._1llll11ll1l_opy_.append([message])
class bstack1lll1ll1ll1_opy_:
    FAIL = bstack1ll1lll_opy_ (u"ࠫࡋࡇࡉࡍࠩᆵ")
    ERROR = bstack1ll1lll_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫᆶ")
    WARNING = bstack1ll1lll_opy_ (u"࠭ࡗࡂࡔࡑࠫᆷ")
    bstack1llll1l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡊࡐࡉࡓࠬᆸ")
    DEBUG = bstack1ll1lll_opy_ (u"ࠨࡆࡈࡆ࡚ࡍࠧᆹ")
    TRACE = bstack1ll1lll_opy_ (u"ࠩࡗࡖࡆࡉࡅࠨᆺ")
    bstack1lll1ll1111_opy_ = [FAIL, ERROR]
def bstack1lll1llll11_opy_(bstack1lll1lll1l1_opy_):
    if not bstack1lll1lll1l1_opy_:
        return None
    if bstack1lll1lll1l1_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᆻ"), None):
        return getattr(bstack1lll1lll1l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆼ")], bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᆽ"), None)
    return bstack1lll1lll1l1_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᆾ"), None)
def bstack1llll1ll1ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᆿ"), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᇀ")]:
        return
    if hook_type.lower() == bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᇁ"):
        if current_test_uuid is None:
            return bstack1ll1lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᇂ")
        else:
            return bstack1ll1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᇃ")
    elif hook_type.lower() == bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᇄ"):
        if current_test_uuid is None:
            return bstack1ll1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᇅ")
        else:
            return bstack1ll1lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᇆ")