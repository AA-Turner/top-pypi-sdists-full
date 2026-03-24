# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1llll1l1ll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1lllll1ll1l_opy_
from bstack_utils.test_data import bstack1llll1l11l1_opy_, bstack1llllll11l1_opy_, TestData
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack111l1lll11_opy_, current_time, Result, \
    error_handler, bstack1llll1ll111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬრ"): [],
        bstack1ll1lll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨს"): [],
        bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧტ"): []
    }
    bstack1llll1111ll_opy_ = []
    bstack1lll1llllll_opy_ = []
    @staticmethod
    def bstack1lllllllll1_opy_(log):
        if not ((isinstance(log[bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬუ")], list) or (isinstance(log[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ფ")], dict)) and len(log[bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧქ")])>0) or (isinstance(log[bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨღ")], str) and log[bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩყ")].strip())):
            return
        active = bstack11lll1l11_opy_.bstack1llllll1l1l_opy_()
        log = {
            bstack1ll1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨშ"): log[bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩჩ")],
            bstack1ll1lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧც"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠬࡠࠧძ"),
            bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧწ"): log[bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨჭ")],
        }
        if active:
            if active[bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ხ")] == bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧჯ"):
                log[bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪჰ")] = active[bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫჱ")]
            elif active[bstack1ll1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪჲ")] == bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࠫჳ"):
                log[bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧჴ")] = active[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨჵ")]
        TestHubHandler.bstack11lllll111_opy_([log])
    def __init__(self):
        self.messages = bstack1llll1l1lll_opy_()
        self._1llll1ll1ll_opy_ = None
        self._1llll1llll1_opy_ = None
        self._1llll111lll_opy_ = OrderedDict()
        self.bstack1lllll1llll_opy_ = bstack1lllll1ll1l_opy_(self.bstack1lllllllll1_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llll1ll1l1_opy_()
        if not self._1llll111lll_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬჶ")), None):
            self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ჷ"))] = {}
        bstack1lll1llll1l_opy_ = TestData(
                bstack1llll11l111_opy_=attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧჸ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1ll1lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬჹ")], start=os.getcwd()) if attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ჺ")) != bstack1ll1lll_opy_ (u"ࠧࠨ჻") else bstack1ll1lll_opy_ (u"ࠨࠩჼ"),
                framework=bstack1ll1lll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨჽ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ჾ"), None)
        self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧჿ"))][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄀ")] = bstack1lll1llll1l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lllll1111l_opy_()
        self._1lllll11111_opy_(messages)
        with self._lock:
            for bstack1llll1l111l_opy_ in self.bstack1llll1111ll_opy_:
                bstack1llll1l111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᄁ")][bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᄂ")].extend(self.store[bstack1ll1lll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᄃ")])
                TestHubHandler.bstack11l1ll111l_opy_(bstack1llll1l111l_opy_)
            self.bstack1llll1111ll_opy_ = []
            self.store[bstack1ll1lll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨᄄ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lllll1llll_opy_.start()
        if not self._1llll111lll_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ᄅ")), None):
            self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᄆ"))] = {}
        driver = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᄇ"), None)
        test_data = TestData(
            bstack1llll11l111_opy_=attrs.get(bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᄈ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1ll1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᄉ")], start=os.getcwd()),
            scope=RobotHandler.bstack1llll1l1111_opy_(attrs.get(bstack1ll1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᄊ"), None)),
            framework=bstack1ll1lll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨᄋ"),
            tags=attrs[bstack1ll1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᄌ")],
            hooks=self.store[bstack1ll1lll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪᄍ")],
            integrations=TestHubHandler.bstack1llllllll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1lll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢᄎ").format(bstack1ll1lll_opy_ (u"ࠨࠠࠣᄏ").join(attrs[bstack1ll1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬᄐ")]), name) if attrs[bstack1ll1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᄑ")] else name
        )
        self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬᄒ"))][bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᄓ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llll11ll11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᄔ"), None)
        self.send_run_event(bstack1ll1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᄕ"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lllll1llll_opy_.reset()
        bstack1llll11l11l_opy_ = bstack1lllll1l11l_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᄖ")), bstack1ll1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᄗ"))
        self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫᄘ"))][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄙ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll1lll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨᄚ"), bstack1ll1lll_opy_ (u"ࠫ࠵࠭ᄛ"))), result=Result(result=bstack1llll11l11l_opy_, exception=attrs.get(bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄜ")), bstack1llllllll1l_opy_=[attrs.get(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄝ"))]))
        self.send_run_event(bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᄞ"), self._1llll111lll_opy_[attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫᄟ"))][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄠ")], True)
        with self._lock:
            self.store[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧᄡ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llll1ll1l1_opy_()
        current_test_id = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᄢ"), None)
        bstack1llll111l11_opy_ = current_test_id if bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧᄣ"), None) else bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩᄤ"), None)
        if attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬᄥ"), bstack1ll1lll_opy_ (u"ࠨࠩᄦ")).lower() in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᄧ"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᄨ")]:
            hook_type = bstack1llll111l1l_opy_(attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩᄩ")), bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᄪ"), None))
            hook_name = bstack1ll1lll_opy_ (u"࠭ࡻࡾࠩᄫ").format(attrs.get(bstack1ll1lll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᄬ"), bstack1ll1lll_opy_ (u"ࠨࠩᄭ")))
            if hook_type in [bstack1ll1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᄮ"), bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᄯ")]:
                hook_name = bstack1ll1lll_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬᄰ").format(bstack1llll1ll11l_opy_.get(hook_type), attrs.get(bstack1ll1lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᄱ"), bstack1ll1lll_opy_ (u"࠭ࠧᄲ")))
            bstack1lllll11l1l_opy_ = bstack1llllll11l1_opy_(
                bstack1llll11l111_opy_=bstack1llll111l11_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠮ࠩᄳ") + attrs.get(bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᄴ"), bstack1ll1lll_opy_ (u"ࠩࠪᄵ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᄶ")), start=os.getcwd()),
                framework=bstack1ll1lll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪᄷ"),
                tags=attrs[bstack1ll1lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᄸ")],
                scope=RobotHandler.bstack1llll1l1111_opy_(attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᄹ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lllll11l1l_opy_.bstack1llll11ll11_opy_()
            threading.current_thread().current_hook_id = bstack1llll111l11_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠮ࠩᄺ") + attrs.get(bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᄻ"), bstack1ll1lll_opy_ (u"ࠩࠪᄼ")).lower()
            with self._lock:
                self.store[bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᄽ")] = [bstack1lllll11l1l_opy_.bstack1llll11ll11_opy_()]
                if bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᄾ"), None):
                    self.store[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩᄿ")].append(bstack1lllll11l1l_opy_.bstack1llll11ll11_opy_())
                else:
                    self.store[bstack1ll1lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬᅀ")].append(bstack1lllll11l1l_opy_.bstack1llll11ll11_opy_())
            if bstack1llll111l11_opy_:
                self._1llll111lll_opy_[bstack1llll111l11_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠮ࠩᅁ") + attrs.get(bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᅂ"), bstack1ll1lll_opy_ (u"ࠩࠪᅃ")).lower()] = { bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᅄ"): bstack1lllll11l1l_opy_ }
            TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᅅ"), bstack1lllll11l1l_opy_)
        else:
            bstack1llllll1l11_opy_ = {
                bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨᅆ"): uuid4().__str__(),
                bstack1ll1lll_opy_ (u"࠭ࡴࡦࡺࡷࠫᅇ"): bstack1ll1lll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ᅈ").format(attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨᅉ")), attrs.get(bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᅊ"), bstack1ll1lll_opy_ (u"ࠪࠫᅋ"))) if attrs.get(bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᅌ"), []) else attrs.get(bstack1ll1lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᅍ")),
                bstack1ll1lll_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ᅎ"): attrs.get(bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᅏ"), []),
                bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᅐ"): current_time(),
                bstack1ll1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᅑ"): bstack1ll1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᅒ"),
                bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᅓ"): attrs.get(bstack1ll1lll_opy_ (u"ࠬࡪ࡯ࡤࠩᅔ"), bstack1ll1lll_opy_ (u"࠭ࠧᅕ"))
            }
            if attrs.get(bstack1ll1lll_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨᅖ"), bstack1ll1lll_opy_ (u"ࠨࠩᅗ")) != bstack1ll1lll_opy_ (u"ࠩࠪᅘ"):
                bstack1llllll1l11_opy_[bstack1ll1lll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᅙ")] = attrs.get(bstack1ll1lll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬᅚ"))
            if not self.bstack1lll1llllll_opy_:
                self._1llll111lll_opy_[self._1llll11lll1_opy_()][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᅛ")].add_step(bstack1llllll1l11_opy_)
                threading.current_thread().current_step_uuid = bstack1llllll1l11_opy_[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᅜ")]
            self.bstack1lll1llllll_opy_.append(bstack1llllll1l11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lllll1111l_opy_()
        self._1lllll11111_opy_(messages)
        current_test_id = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩᅝ"), None)
        bstack1llll111l11_opy_ = current_test_id if current_test_id else bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫᅞ"), None)
        bstack1llll1lllll_opy_ = bstack1lllll1l11l_opy_.get(attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᅟ")), bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᅠ"))
        bstack1lllll1l1l1_opy_ = attrs.get(bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅡ"))
        if bstack1llll1lllll_opy_ != bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᅢ") and not attrs.get(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅣ")) and self._1llll1ll1ll_opy_:
            bstack1lllll1l1l1_opy_ = self._1llll1ll1ll_opy_
        bstack1llllll11ll_opy_ = Result(result=bstack1llll1lllll_opy_, exception=bstack1lllll1l1l1_opy_, bstack1llllllll1l_opy_=[bstack1lllll1l1l1_opy_])
        if attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬᅤ"), bstack1ll1lll_opy_ (u"ࠨࠩᅥ")).lower() in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᅦ"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᅧ")]:
            bstack1llll111l11_opy_ = current_test_id if current_test_id else bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧᅨ"), None)
            if bstack1llll111l11_opy_:
                bstack1llllll111l_opy_ = bstack1llll111l11_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠳ࠢᅩ") + attrs.get(bstack1ll1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫᅪ"), bstack1ll1lll_opy_ (u"ࠧࠨᅫ")).lower()
                self._1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅬ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll1lll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧᅭ"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬᅮ"))), result=bstack1llllll11ll_opy_)
                TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᅯ"), self._1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᅰ")])
        else:
            bstack1llll111l11_opy_ = current_test_id if current_test_id else bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨᅱ"), None)
            if bstack1llll111l11_opy_ and len(self.bstack1lll1llllll_opy_) == 1:
                current_step_uuid = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫᅲ"), None)
                self._1llll111lll_opy_[bstack1llll111l11_opy_][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅳ")].bstack1lllll1ll11_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1lll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧᅴ"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬᅵ"))), result=bstack1llllll11ll_opy_)
            else:
                self.bstack1llll111ll1_opy_(attrs)
            self.bstack1lll1llllll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩᅶ"), bstack1ll1lll_opy_ (u"ࠬࡴ࡯ࠨᅷ")) == bstack1ll1lll_opy_ (u"࠭ࡹࡦࡵࠪᅸ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11lll1l11_opy_.bstack1llllll1l1l_opy_():
                logs.append({
                    bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᅹ"): current_time(),
                    bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅺ"): message.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᅻ")),
                    bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᅼ"): message.get(bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᅽ")),
                    **bstack11lll1l11_opy_.bstack1llllll1l1l_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack11lllll111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1llll1l1l11_opy_()
    def bstack1llll111ll1_opy_(self, bstack1llll1l1l1l_opy_):
        if not bstack11lll1l11_opy_.bstack1llllll1l1l_opy_():
            return
        kwname = bstack1ll1lll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫᅾ").format(bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᅿ")), bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᆀ"), bstack1ll1lll_opy_ (u"ࠨࠩᆁ"))) if bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᆂ"), []) else bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᆃ"))
        error_message = bstack1ll1lll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥᆄ").format(kwname, bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᆅ")), str(bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆆ"))))
        bstack1llll111111_opy_ = bstack1ll1lll_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨᆇ").format(kwname, bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᆈ")))
        bstack1lllll111l1_opy_ = error_message if bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᆉ")) else bstack1llll111111_opy_
        bstack1llll11l1l1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᆊ"): self.bstack1lll1llllll_opy_[-1].get(bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᆋ"), current_time()),
            bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆌ"): bstack1lllll111l1_opy_,
            bstack1ll1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᆍ"): bstack1ll1lll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ᆎ") if bstack1llll1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᆏ")) == bstack1ll1lll_opy_ (u"ࠩࡉࡅࡎࡒࠧᆐ") else bstack1ll1lll_opy_ (u"ࠪࡍࡓࡌࡏࠨᆑ"),
            **bstack11lll1l11_opy_.bstack1llllll1l1l_opy_()
        }
        TestHubHandler.bstack11lllll111_opy_([bstack1llll11l1l1_opy_])
    def _1llll11lll1_opy_(self):
        for bstack1llll11l111_opy_ in reversed(self._1llll111lll_opy_):
            bstack1lll1lllll1_opy_ = bstack1llll11l111_opy_
            data = self._1llll111lll_opy_[bstack1llll11l111_opy_][bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆒ")]
            if isinstance(data, bstack1llllll11l1_opy_):
                if not bstack1ll1lll_opy_ (u"ࠬࡋࡁࡄࡊࠪᆓ") in data.bstack1lllll11l11_opy_():
                    return bstack1lll1lllll1_opy_
            else:
                return bstack1lll1lllll1_opy_
    def _1lllll11111_opy_(self, messages):
        try:
            bstack1llll11llll_opy_ = BuiltIn().get_variable_value(bstack1ll1lll_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧᆔ")) in (bstack1llll1lll1l_opy_.DEBUG, bstack1llll1lll1l_opy_.TRACE)
            for message, bstack1llll11l1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᆕ"))
                level = message.get(bstack1ll1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᆖ"))
                if level == bstack1llll1lll1l_opy_.FAIL:
                    self._1llll1ll1ll_opy_ = name or self._1llll1ll1ll_opy_
                    self._1llll1llll1_opy_ = bstack1llll11l1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᆗ")) if bstack1llll11llll_opy_ and bstack1llll11l1ll_opy_ else self._1llll1llll1_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1llll1lll11_opy_: bstack1llll1l11l1_opy_, bstack1llll11ll1l_opy_=False):
        if event == bstack1ll1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᆘ"):
            bstack1llll1lll11_opy_.set(hooks=self.store[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨᆙ")])
        if event == bstack1ll1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᆚ"):
            event = bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᆛ")
        if bstack1llll11ll1l_opy_:
            bstack1lllll11ll1_opy_ = {
                bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᆜ"): event,
                bstack1llll1lll11_opy_.bstack1lllll1l111_opy_(): bstack1llll1lll11_opy_.bstack1lll1llll11_opy_(event)
            }
            with self._lock:
                self.bstack1llll1111ll_opy_.append(bstack1lllll11ll1_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1llll1lll11_opy_)
class bstack1llll1l1lll_opy_:
    def __init__(self):
        self._1llll1111l1_opy_ = []
    def bstack1llll1ll1l1_opy_(self):
        self._1llll1111l1_opy_.append([])
    def bstack1lllll1111l_opy_(self):
        return self._1llll1111l1_opy_.pop() if self._1llll1111l1_opy_ else list()
    def push(self, message):
        self._1llll1111l1_opy_[-1].append(message) if self._1llll1111l1_opy_ else self._1llll1111l1_opy_.append([message])
class bstack1llll1lll1l_opy_:
    FAIL = bstack1ll1lll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ᆝ")
    ERROR = bstack1ll1lll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨᆞ")
    WARNING = bstack1ll1lll_opy_ (u"࡛ࠪࡆࡘࡎࠨᆟ")
    bstack1llll1l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠫࡎࡔࡆࡐࠩᆠ")
    DEBUG = bstack1ll1lll_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫᆡ")
    TRACE = bstack1ll1lll_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬᆢ")
    bstack1lllll11lll_opy_ = [FAIL, ERROR]
def bstack1lllll111ll_opy_(bstack1llll11111l_opy_):
    if not bstack1llll11111l_opy_:
        return None
    if bstack1llll11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆣ"), None):
        return getattr(bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᆤ")], bstack1ll1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᆥ"), None)
    return bstack1llll11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᆦ"), None)
def bstack1llll111l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᆧ"), bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᆨ")]:
        return
    if hook_type.lower() == bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᆩ"):
        if current_test_uuid is None:
            return bstack1ll1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᆪ")
        else:
            return bstack1ll1lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᆫ")
    elif hook_type.lower() == bstack1ll1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᆬ"):
        if current_test_uuid is None:
            return bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᆭ")
        else:
            return bstack1ll1lll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᆮ")