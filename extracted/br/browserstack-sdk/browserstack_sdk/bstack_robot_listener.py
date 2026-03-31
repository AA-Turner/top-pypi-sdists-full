# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll1ll11l1_opy_ import RobotHandler
from bstack_utils.capture import bstack1llll1llll1_opy_
from bstack_utils.test_data import bstack1lll1llllll_opy_, bstack1lllll111l1_opy_, TestData
from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1111l111_opy_, current_time, Result, \
    error_handler, bstack1lll1ll1ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᄉ"): [],
        bstack1ll11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᄊ"): [],
        bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᄋ"): []
    }
    bstack1llll1ll111_opy_ = []
    bstack1llll11ll11_opy_ = []
    @staticmethod
    def bstack1lllll1ll11_opy_(log):
        if not ((isinstance(log[bstack1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄌ")], list) or (isinstance(log[bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄍ")], dict)) and len(log[bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄎ")])>0) or (isinstance(log[bstack1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄏ")], str) and log[bstack1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᄐ")].strip())):
            return
        active = bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_()
        log = {
            bstack1ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᄑ"): log[bstack1ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᄒ")],
            bstack1ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᄓ"): bstack1lll1ll1ll1_opy_().isoformat() + bstack1ll11_opy_ (u"ࠫ࡟࠭ᄔ"),
            bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄕ"): log[bstack1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄖ")],
        }
        if active:
            if active[bstack1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᄗ")] == bstack1ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᄘ"):
                log[bstack1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᄙ")] = active[bstack1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᄚ")]
            elif active[bstack1ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᄛ")] == bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪᄜ"):
                log[bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᄝ")] = active[bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᄞ")]
        TestHubHandler.bstack11111lll1l_opy_([log])
    def __init__(self):
        self.messages = bstack1lll1l1lll1_opy_()
        self._1lll1ll111l_opy_ = None
        self._1llll1111ll_opy_ = None
        self._1lll1ll1l11_opy_ = OrderedDict()
        self.bstack1lllll1111l_opy_ = bstack1llll1llll1_opy_(self.bstack1lllll1ll11_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llll11llll_opy_()
        if not self._1lll1ll1l11_opy_.get(attrs.get(bstack1ll11_opy_ (u"ࠨ࡫ࡧࠫᄟ")), None):
            self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬᄠ"))] = {}
        bstack1llll111lll_opy_ = TestData(
                bstack1llll1l1111_opy_=attrs.get(bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭ᄡ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᄢ")], start=os.getcwd()) if attrs.get(bstack1ll11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᄣ")) != bstack1ll11_opy_ (u"࠭ࠧᄤ") else bstack1ll11_opy_ (u"ࠧࠨᄥ"),
                framework=bstack1ll11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᄦ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬᄧ"), None)
        self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭ᄨ"))][bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᄩ")] = bstack1llll111lll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llll11l111_opy_()
        self._1lll1lll1ll_opy_(messages)
        with self._lock:
            for bstack1lll1lllll1_opy_ in self.bstack1llll1ll111_opy_:
                bstack1lll1lllll1_opy_[bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᄪ")][bstack1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᄫ")].extend(self.store[bstack1ll11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ᄬ")])
                TestHubHandler.bstack11l1111lll_opy_(bstack1lll1lllll1_opy_)
            self.bstack1llll1ll111_opy_ = []
            self.store[bstack1ll11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᄭ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lllll1111l_opy_.start()
        if not self._1lll1ll1l11_opy_.get(attrs.get(bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬᄮ")), None):
            self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭ᄯ"))] = {}
        driver = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᄰ"), None)
        test_data = TestData(
            bstack1llll1l1111_opy_=attrs.get(bstack1ll11_opy_ (u"ࠬ࡯ࡤࠨᄱ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᄲ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1l1ll11_opy_(attrs.get(bstack1ll11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᄳ"), None)),
            framework=bstack1ll11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᄴ"),
            tags=attrs[bstack1ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᄵ")],
            hooks=self.store[bstack1ll11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩᄶ")],
            integrations=TestHubHandler.bstack1lllll1l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll11_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨᄷ").format(bstack1ll11_opy_ (u"ࠧࠦࠢᄸ").join(attrs[bstack1ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᄹ")]), name) if attrs[bstack1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᄺ")] else name
        )
        self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠨ࡫ࡧࠫᄻ"))][bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄼ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llll1l1l11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭ᄽ"), None)
        self.send_run_event(bstack1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᄾ"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lllll1111l_opy_.reset()
        bstack1llll1l11l1_opy_ = bstack1lll1l1llll_opy_.get(attrs.get(bstack1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᄿ")), bstack1ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᅀ"))
        self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠧࡪࡦࠪᅁ"))][bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅂ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll11_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧᅃ"), bstack1ll11_opy_ (u"ࠪ࠴ࠬᅄ"))), result=Result(result=bstack1llll1l11l1_opy_, exception=attrs.get(bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅅ")), bstack1lllll11l1l_opy_=[attrs.get(bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅆ"))]))
        self.send_run_event(bstack1ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᅇ"), self._1lll1ll1l11_opy_[attrs.get(bstack1ll11_opy_ (u"ࠧࡪࡦࠪᅈ"))][bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅉ")], True)
        with self._lock:
            self.store[bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᅊ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llll11llll_opy_()
        current_test_id = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᅋ"), None)
        bstack1lll1llll11_opy_ = current_test_id if bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᅌ"), None) else bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᅍ"), None)
        if attrs.get(bstack1ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫᅎ"), bstack1ll11_opy_ (u"ࠧࠨᅏ")).lower() in [bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᅐ"), bstack1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᅑ")]:
            hook_type = bstack1llll11111l_opy_(attrs.get(bstack1ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨᅒ")), bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᅓ"), None))
            hook_name = bstack1ll11_opy_ (u"ࠬࢁࡽࠨᅔ").format(attrs.get(bstack1ll11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᅕ"), bstack1ll11_opy_ (u"ࠧࠨᅖ")))
            if hook_type in [bstack1ll11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᅗ"), bstack1ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᅘ")]:
                hook_name = bstack1ll11_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫᅙ").format(bstack1llll1111l1_opy_.get(hook_type), attrs.get(bstack1ll11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᅚ"), bstack1ll11_opy_ (u"ࠬ࠭ᅛ")))
            bstack1llll1l11ll_opy_ = bstack1lllll111l1_opy_(
                bstack1llll1l1111_opy_=bstack1lll1llll11_opy_ + bstack1ll11_opy_ (u"࠭࠭ࠨᅜ") + attrs.get(bstack1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᅝ"), bstack1ll11_opy_ (u"ࠨࠩᅞ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1ll11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᅟ")), start=os.getcwd()),
                framework=bstack1ll11_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩᅠ"),
                tags=attrs[bstack1ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩᅡ")],
                scope=RobotHandler.bstack1lll1l1ll11_opy_(attrs.get(bstack1ll11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᅢ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1llll1l11ll_opy_.bstack1llll1l1l11_opy_()
            threading.current_thread().current_hook_id = bstack1lll1llll11_opy_ + bstack1ll11_opy_ (u"࠭࠭ࠨᅣ") + attrs.get(bstack1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᅤ"), bstack1ll11_opy_ (u"ࠨࠩᅥ")).lower()
            with self._lock:
                self.store[bstack1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᅦ")] = [bstack1llll1l11ll_opy_.bstack1llll1l1l11_opy_()]
                if bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᅧ"), None):
                    self.store[bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨᅨ")].append(bstack1llll1l11ll_opy_.bstack1llll1l1l11_opy_())
                else:
                    self.store[bstack1ll11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᅩ")].append(bstack1llll1l11ll_opy_.bstack1llll1l1l11_opy_())
            if bstack1lll1llll11_opy_:
                self._1lll1ll1l11_opy_[bstack1lll1llll11_opy_ + bstack1ll11_opy_ (u"࠭࠭ࠨᅪ") + attrs.get(bstack1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᅫ"), bstack1ll11_opy_ (u"ࠨࠩᅬ")).lower()] = { bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᅭ"): bstack1llll1l11ll_opy_ }
            TestHubHandler.send_run_event(bstack1ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᅮ"), bstack1llll1l11ll_opy_)
        else:
            bstack1lllll1l11l_opy_ = {
                bstack1ll11_opy_ (u"ࠫ࡮ࡪࠧᅯ"): uuid4().__str__(),
                bstack1ll11_opy_ (u"ࠬࡺࡥࡹࡶࠪᅰ"): bstack1ll11_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬᅱ").format(attrs.get(bstack1ll11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᅲ")), attrs.get(bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᅳ"), bstack1ll11_opy_ (u"ࠩࠪᅴ"))) if attrs.get(bstack1ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᅵ"), []) else attrs.get(bstack1ll11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᅶ")),
                bstack1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᅷ"): attrs.get(bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᅸ"), []),
                bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᅹ"): current_time(),
                bstack1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᅺ"): bstack1ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᅻ"),
                bstack1ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᅼ"): attrs.get(bstack1ll11_opy_ (u"ࠫࡩࡵࡣࠨᅽ"), bstack1ll11_opy_ (u"ࠬ࠭ᅾ"))
            }
            if attrs.get(bstack1ll11_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧᅿ"), bstack1ll11_opy_ (u"ࠧࠨᆀ")) != bstack1ll11_opy_ (u"ࠨࠩᆁ"):
                bstack1lllll1l11l_opy_[bstack1ll11_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᆂ")] = attrs.get(bstack1ll11_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫᆃ"))
            if not self.bstack1llll11ll11_opy_:
                self._1lll1ll1l11_opy_[self._1lll1ll11ll_opy_()][bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆄ")].add_step(bstack1lllll1l11l_opy_)
                threading.current_thread().current_step_uuid = bstack1lllll1l11l_opy_[bstack1ll11_opy_ (u"ࠬ࡯ࡤࠨᆅ")]
            self.bstack1llll11ll11_opy_.append(bstack1lllll1l11l_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llll11l111_opy_()
        self._1lll1lll1ll_opy_(messages)
        current_test_id = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᆆ"), None)
        bstack1lll1llll11_opy_ = current_test_id if current_test_id else bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪᆇ"), None)
        bstack1lll1l1ll1l_opy_ = bstack1lll1l1llll_opy_.get(attrs.get(bstack1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᆈ")), bstack1ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᆉ"))
        bstack1llll111l1l_opy_ = attrs.get(bstack1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᆊ"))
        if bstack1lll1l1ll1l_opy_ != bstack1ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᆋ") and not attrs.get(bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆌ")) and self._1lll1ll111l_opy_:
            bstack1llll111l1l_opy_ = self._1lll1ll111l_opy_
        bstack1llll1lllll_opy_ = Result(result=bstack1lll1l1ll1l_opy_, exception=bstack1llll111l1l_opy_, bstack1lllll11l1l_opy_=[bstack1llll111l1l_opy_])
        if attrs.get(bstack1ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫᆍ"), bstack1ll11_opy_ (u"ࠧࠨᆎ")).lower() in [bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᆏ"), bstack1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᆐ")]:
            bstack1lll1llll11_opy_ = current_test_id if current_test_id else bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᆑ"), None)
            if bstack1lll1llll11_opy_:
                bstack1lllll1l1l1_opy_ = bstack1lll1llll11_opy_ + bstack1ll11_opy_ (u"ࠦ࠲ࠨᆒ") + attrs.get(bstack1ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᆓ"), bstack1ll11_opy_ (u"࠭ࠧᆔ")).lower()
                self._1lll1ll1l11_opy_[bstack1lllll1l1l1_opy_][bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆕ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᆖ"), bstack1ll11_opy_ (u"ࠩ࠳ࠫᆗ"))), result=bstack1llll1lllll_opy_)
                TestHubHandler.send_run_event(bstack1ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᆘ"), self._1lll1ll1l11_opy_[bstack1lllll1l1l1_opy_][bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆙ")])
        else:
            bstack1lll1llll11_opy_ = current_test_id if current_test_id else bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧᆚ"), None)
            if bstack1lll1llll11_opy_ and len(self.bstack1llll11ll11_opy_) == 1:
                current_step_uuid = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪᆛ"), None)
                self._1lll1ll1l11_opy_[bstack1lll1llll11_opy_][bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆜ")].bstack1lllll11lll_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᆝ"), bstack1ll11_opy_ (u"ࠩ࠳ࠫᆞ"))), result=bstack1llll1lllll_opy_)
            else:
                self.bstack1llll111l11_opy_(attrs)
            self.bstack1llll11ll11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll11_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨᆟ"), bstack1ll11_opy_ (u"ࠫࡳࡵࠧᆠ")) == bstack1ll11_opy_ (u"ࠬࡿࡥࡴࠩᆡ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_():
                logs.append({
                    bstack1ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᆢ"): current_time(),
                    bstack1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᆣ"): message.get(bstack1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᆤ")),
                    bstack1ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᆥ"): message.get(bstack1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᆦ")),
                    **bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack11111lll1l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll1l1l1ll_opy_()
    def bstack1llll111l11_opy_(self, bstack1llll111ll1_opy_):
        if not bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_():
            return
        kwname = bstack1ll11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᆧ").format(bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᆨ")), bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᆩ"), bstack1ll11_opy_ (u"ࠧࠨᆪ"))) if bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆫ"), []) else bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᆬ"))
        error_message = bstack1ll11_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤᆭ").format(kwname, bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᆮ")), str(bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆯ"))))
        bstack1llll11l1l1_opy_ = bstack1ll11_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧᆰ").format(kwname, bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᆱ")))
        bstack1llll11lll1_opy_ = error_message if bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᆲ")) else bstack1llll11l1l1_opy_
        bstack1llll1l1ll1_opy_ = {
            bstack1ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᆳ"): self.bstack1llll11ll11_opy_[-1].get(bstack1ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᆴ"), current_time()),
            bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᆵ"): bstack1llll11lll1_opy_,
            bstack1ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᆶ"): bstack1ll11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᆷ") if bstack1llll111ll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᆸ")) == bstack1ll11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ᆹ") else bstack1ll11_opy_ (u"ࠩࡌࡒࡋࡕࠧᆺ"),
            **bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_()
        }
        TestHubHandler.bstack11111lll1l_opy_([bstack1llll1l1ll1_opy_])
    def _1lll1ll11ll_opy_(self):
        for bstack1llll1l1111_opy_ in reversed(self._1lll1ll1l11_opy_):
            bstack1lll1ll1lll_opy_ = bstack1llll1l1111_opy_
            data = self._1lll1ll1l11_opy_[bstack1llll1l1111_opy_][bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᆻ")]
            if isinstance(data, bstack1lllll111l1_opy_):
                if not bstack1ll11_opy_ (u"ࠫࡊࡇࡃࡉࠩᆼ") in data.bstack1llll1ll11l_opy_():
                    return bstack1lll1ll1lll_opy_
            else:
                return bstack1lll1ll1lll_opy_
    def _1lll1lll1ll_opy_(self, messages):
        try:
            bstack1llll11ll1l_opy_ = BuiltIn().get_variable_value(bstack1ll11_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦᆽ")) in (bstack1llll11l11l_opy_.DEBUG, bstack1llll11l11l_opy_.TRACE)
            for message, bstack1llll111111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆾ"))
                level = message.get(bstack1ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᆿ"))
                if level == bstack1llll11l11l_opy_.FAIL:
                    self._1lll1ll111l_opy_ = name or self._1lll1ll111l_opy_
                    self._1llll1111ll_opy_ = bstack1llll111111_opy_.get(bstack1ll11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᇀ")) if bstack1llll11ll1l_opy_ and bstack1llll111111_opy_ else self._1llll1111ll_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1lll1lll11l_opy_: bstack1lll1llllll_opy_, bstack1lll1ll1111_opy_=False):
        if event == bstack1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᇁ"):
            bstack1lll1lll11l_opy_.set(hooks=self.store[bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧᇂ")])
        if event == bstack1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᇃ"):
            event = bstack1ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᇄ")
        if bstack1lll1ll1111_opy_:
            bstack1llll1l111l_opy_ = {
                bstack1ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᇅ"): event,
                bstack1lll1lll11l_opy_.bstack1llll1l1l1l_opy_(): bstack1lll1lll11l_opy_.bstack1llll1l1lll_opy_(event)
            }
            with self._lock:
                self.bstack1llll1ll111_opy_.append(bstack1llll1l111l_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1lll1lll11l_opy_)
class bstack1lll1l1lll1_opy_:
    def __init__(self):
        self._1lll1lll1l1_opy_ = []
    def bstack1llll11llll_opy_(self):
        self._1lll1lll1l1_opy_.append([])
    def bstack1llll11l111_opy_(self):
        return self._1lll1lll1l1_opy_.pop() if self._1lll1lll1l1_opy_ else list()
    def push(self, message):
        self._1lll1lll1l1_opy_[-1].append(message) if self._1lll1lll1l1_opy_ else self._1lll1lll1l1_opy_.append([message])
class bstack1llll11l11l_opy_:
    FAIL = bstack1ll11_opy_ (u"ࠧࡇࡃࡌࡐࠬᇆ")
    ERROR = bstack1ll11_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧᇇ")
    WARNING = bstack1ll11_opy_ (u"࡚ࠩࡅࡗࡔࠧᇈ")
    bstack1llll11l1ll_opy_ = bstack1ll11_opy_ (u"ࠪࡍࡓࡌࡏࠨᇉ")
    DEBUG = bstack1ll11_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪᇊ")
    TRACE = bstack1ll11_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫᇋ")
    bstack1lll1ll1l1l_opy_ = [FAIL, ERROR]
def bstack1lll1llll1l_opy_(bstack1lll1lll111_opy_):
    if not bstack1lll1lll111_opy_:
        return None
    if bstack1lll1lll111_opy_.get(bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᇌ"), None):
        return getattr(bstack1lll1lll111_opy_[bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᇍ")], bstack1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇎ"), None)
    return bstack1lll1lll111_opy_.get(bstack1ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᇏ"), None)
def bstack1llll11111l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᇐ"), bstack1ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᇑ")]:
        return
    if hook_type.lower() == bstack1ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᇒ"):
        if current_test_uuid is None:
            return bstack1ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᇓ")
        else:
            return bstack1ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᇔ")
    elif hook_type.lower() == bstack1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᇕ"):
        if current_test_uuid is None:
            return bstack1ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᇖ")
        else:
            return bstack1ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᇗ")