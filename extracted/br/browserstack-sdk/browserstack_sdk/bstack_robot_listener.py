# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11111llll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1111ll1l11_opy_
from bstack_utils.test_data import bstack1lllllll1ll_opy_, bstack1111ll11l1_opy_, TestData
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11lll1ll1_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll11l111_opy_, current_time, Result, \
    error_handler, bstack1111111l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬဎ"): [],
        bstack11ll111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨဏ"): [],
        bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧတ"): []
    }
    bstack111111111l_opy_ = []
    bstack11111l1111_opy_ = []
    @staticmethod
    def bstack1111ll111l_opy_(log):
        if not ((isinstance(log[bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬထ")], list) or (isinstance(log[bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ဒ")], dict)) and len(log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဓ")])>0) or (isinstance(log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨန")], str) and log[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩပ")].strip())):
            return
        active = bstack11lll1ll1_opy_.bstack1111l1lll1_opy_()
        log = {
            bstack11ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨဖ"): log[bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩဗ")],
            bstack11ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧဘ"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"ࠬࡠࠧမ"),
            bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧယ"): log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨရ")],
        }
        if active:
            if active[bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭လ")] == bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧဝ"):
                log[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪသ")] = active[bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫဟ")]
            elif active[bstack11ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪဠ")] == bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࠫအ"):
                log[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧဢ")] = active[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨဣ")]
        TestHubHandler.bstack1ll11l1ll_opy_([log])
    def __init__(self):
        self.messages = bstack11111lll1l_opy_()
        self._1lllllll111_opy_ = None
        self._111111l1l1_opy_ = None
        self._11111l11ll_opy_ = OrderedDict()
        self.bstack1111l1l11l_opy_ = bstack1111ll1l11_opy_(self.bstack1111ll111l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11111l11l1_opy_()
        if not self._11111l11ll_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬဤ")), None):
            self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ဥ"))] = {}
        bstack1llllll1ll1_opy_ = TestData(
                bstack111111llll_opy_=attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧဦ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack11ll111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬဧ")], start=os.getcwd()) if attrs.get(bstack11ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ဨ")) != bstack11ll111_opy_ (u"ࠧࠨဩ") else bstack11ll111_opy_ (u"ࠨࠩဪ"),
                framework=bstack11ll111_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨါ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ာ"), None)
        self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧိ"))][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨီ")] = bstack1llllll1ll1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llllllll1l_opy_()
        self._1111l11l11_opy_(messages)
        with self._lock:
            for bstack11111l111l_opy_ in self.bstack111111111l_opy_:
                bstack11111l111l_opy_[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨု")][bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ူ")].extend(self.store[bstack11ll111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧေ")])
                TestHubHandler.bstack11ll11111_opy_(bstack11111l111l_opy_)
            self.bstack111111111l_opy_ = []
            self.store[bstack11ll111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨဲ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111l1l11l_opy_.start()
        if not self._11111l11ll_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ဳ")), None):
            self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧဴ"))] = {}
        driver = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫဵ"), None)
        test_data = TestData(
            bstack111111llll_opy_=attrs.get(bstack11ll111_opy_ (u"࠭ࡩࡥࠩံ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack11ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫့ࠧ")], start=os.getcwd()),
            scope=RobotHandler.bstack111111ll1l_opy_(attrs.get(bstack11ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨး"), None)),
            framework=bstack11ll111_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ္"),
            tags=attrs[bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ်")],
            hooks=self.store[bstack11ll111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪျ")],
            integrations=TestHubHandler.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll111_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢြ").format(bstack11ll111_opy_ (u"ࠨࠠࠣွ").join(attrs[bstack11ll111_opy_ (u"ࠧࡵࡣࡪࡷࠬှ")]), name) if attrs[bstack11ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ဿ")] else name
        )
        self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬ၀"))][bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭၁")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llllll1lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧ၂"), None)
        self.send_run_event(bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭၃"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111l1l11l_opy_.reset()
        bstack111111lll1_opy_ = bstack1lllllll1l1_opy_.get(attrs.get(bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭၄")), bstack11ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ၅"))
        self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫ၆"))][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ၇")].stop(time=current_time(), duration=int(attrs.get(bstack11ll111_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ၈"), bstack11ll111_opy_ (u"ࠫ࠵࠭၉"))), result=Result(result=bstack111111lll1_opy_, exception=attrs.get(bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭၊")), bstack1111ll1lll_opy_=[attrs.get(bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ။"))]))
        self.send_run_event(bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ၌"), self._11111l11ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫ၍"))][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ၎")], True)
        with self._lock:
            self.store[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ၏")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11111l11l1_opy_()
        current_test_id = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ၐ"), None)
        bstack11111ll1ll_opy_ = current_test_id if bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧၑ"), None) else bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩၒ"), None)
        if attrs.get(bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬၓ"), bstack11ll111_opy_ (u"ࠨࠩၔ")).lower() in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨၕ"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬၖ")]:
            hook_type = bstack11111l1ll1_opy_(attrs.get(bstack11ll111_opy_ (u"ࠫࡹࡿࡰࡦࠩၗ")), bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩၘ"), None))
            hook_name = bstack11ll111_opy_ (u"࠭ࡻࡾࠩၙ").format(attrs.get(bstack11ll111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧၚ"), bstack11ll111_opy_ (u"ࠨࠩၛ")))
            if hook_type in [bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ၜ"), bstack11ll111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ၝ")]:
                hook_name = bstack11ll111_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬၞ").format(bstack11111ll111_opy_.get(hook_type), attrs.get(bstack11ll111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬၟ"), bstack11ll111_opy_ (u"࠭ࠧၠ")))
            bstack11111ll1l1_opy_ = bstack1111ll11l1_opy_(
                bstack111111llll_opy_=bstack11111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠧ࠮ࠩၡ") + attrs.get(bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၢ"), bstack11ll111_opy_ (u"ࠩࠪၣ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack11ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪၤ")), start=os.getcwd()),
                framework=bstack11ll111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪၥ"),
                tags=attrs[bstack11ll111_opy_ (u"ࠬࡺࡡࡨࡵࠪၦ")],
                scope=RobotHandler.bstack111111ll1l_opy_(attrs.get(bstack11ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ၧ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11111ll1l1_opy_.bstack1llllll1lll_opy_()
            threading.current_thread().current_hook_id = bstack11111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠧ࠮ࠩၨ") + attrs.get(bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၩ"), bstack11ll111_opy_ (u"ࠩࠪၪ")).lower()
            with self._lock:
                self.store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧၫ")] = [bstack11111ll1l1_opy_.bstack1llllll1lll_opy_()]
                if bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨၬ"), None):
                    self.store[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩၭ")].append(bstack11111ll1l1_opy_.bstack1llllll1lll_opy_())
                else:
                    self.store[bstack11ll111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬၮ")].append(bstack11111ll1l1_opy_.bstack1llllll1lll_opy_())
            if bstack11111ll1ll_opy_:
                self._11111l11ll_opy_[bstack11111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠧ࠮ࠩၯ") + attrs.get(bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၰ"), bstack11ll111_opy_ (u"ࠩࠪၱ")).lower()] = { bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ၲ"): bstack11111ll1l1_opy_ }
            TestHubHandler.send_run_event(bstack11ll111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬၳ"), bstack11111ll1l1_opy_)
        else:
            bstack1111l1ll11_opy_ = {
                bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨၴ"): uuid4().__str__(),
                bstack11ll111_opy_ (u"࠭ࡴࡦࡺࡷࠫၵ"): bstack11ll111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ၶ").format(attrs.get(bstack11ll111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨၷ")), attrs.get(bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧၸ"), bstack11ll111_opy_ (u"ࠪࠫၹ"))) if attrs.get(bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩၺ"), []) else attrs.get(bstack11ll111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬၻ")),
                bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ၼ"): attrs.get(bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬၽ"), []),
                bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬၾ"): current_time(),
                bstack11ll111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩၿ"): bstack11ll111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫႀ"),
                bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩႁ"): attrs.get(bstack11ll111_opy_ (u"ࠬࡪ࡯ࡤࠩႂ"), bstack11ll111_opy_ (u"࠭ࠧႃ"))
            }
            if attrs.get(bstack11ll111_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨႄ"), bstack11ll111_opy_ (u"ࠨࠩႅ")) != bstack11ll111_opy_ (u"ࠩࠪႆ"):
                bstack1111l1ll11_opy_[bstack11ll111_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫႇ")] = attrs.get(bstack11ll111_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬႈ"))
            if not self.bstack11111l1111_opy_:
                self._11111l11ll_opy_[self._11111lll11_opy_()][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨႉ")].add_step(bstack1111l1ll11_opy_)
                threading.current_thread().current_step_uuid = bstack1111l1ll11_opy_[bstack11ll111_opy_ (u"࠭ࡩࡥࠩႊ")]
            self.bstack11111l1111_opy_.append(bstack1111l1ll11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llllllll1l_opy_()
        self._1111l11l11_opy_(messages)
        current_test_id = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩႋ"), None)
        bstack11111ll1ll_opy_ = current_test_id if current_test_id else bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫႌ"), None)
        bstack11111lllll_opy_ = bstack1lllllll1l1_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴႍࠩ")), bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫႎ"))
        bstack1111l111l1_opy_ = attrs.get(bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႏ"))
        if bstack11111lllll_opy_ != bstack11ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭႐") and not attrs.get(bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ႑")) and self._1lllllll111_opy_:
            bstack1111l111l1_opy_ = self._1lllllll111_opy_
        bstack1111l1ll1l_opy_ = Result(result=bstack11111lllll_opy_, exception=bstack1111l111l1_opy_, bstack1111ll1lll_opy_=[bstack1111l111l1_opy_])
        if attrs.get(bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬ႒"), bstack11ll111_opy_ (u"ࠨࠩ႓")).lower() in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ႔"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ႕")]:
            bstack11111ll1ll_opy_ = current_test_id if current_test_id else bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ႖"), None)
            if bstack11111ll1ll_opy_:
                bstack1111l1l111_opy_ = bstack11111ll1ll_opy_ + bstack11ll111_opy_ (u"ࠧ࠳ࠢ႗") + attrs.get(bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫ႘"), bstack11ll111_opy_ (u"ࠧࠨ႙")).lower()
                self._11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႚ")].stop(time=current_time(), duration=int(attrs.get(bstack11ll111_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧႛ"), bstack11ll111_opy_ (u"ࠪ࠴ࠬႜ"))), result=bstack1111l1ll1l_opy_)
                TestHubHandler.send_run_event(bstack11ll111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ႝ"), self._11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ႞")])
        else:
            bstack11111ll1ll_opy_ = current_test_id if current_test_id else bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨ႟"), None)
            if bstack11111ll1ll_opy_ and len(self.bstack11111l1111_opy_) == 1:
                current_step_uuid = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫႠ"), None)
                self._11111l11ll_opy_[bstack11111ll1ll_opy_][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႡ")].bstack1111l11lll_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll111_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧႢ"), bstack11ll111_opy_ (u"ࠪ࠴ࠬႣ"))), result=bstack1111l1ll1l_opy_)
            else:
                self.bstack111111l111_opy_(attrs)
            self.bstack11111l1111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll111_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩႤ"), bstack11ll111_opy_ (u"ࠬࡴ࡯ࠨႥ")) == bstack11ll111_opy_ (u"࠭ࡹࡦࡵࠪႦ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11lll1ll1_opy_.bstack1111l1lll1_opy_():
                logs.append({
                    bstack11ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪႧ"): current_time(),
                    bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႨ"): message.get(bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႩ")),
                    bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႪ"): message.get(bstack11ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪႫ")),
                    **bstack11lll1ll1_opy_.bstack1111l1lll1_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1ll11l1ll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1111l111ll_opy_()
    def bstack111111l111_opy_(self, bstack1111111ll1_opy_):
        if not bstack11lll1ll1_opy_.bstack1111l1lll1_opy_():
            return
        kwname = bstack11ll111_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫႬ").format(bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭Ⴍ")), bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬႮ"), bstack11ll111_opy_ (u"ࠨࠩႯ"))) if bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧႰ"), []) else bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪႱ"))
        error_message = bstack11ll111_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥႲ").format(kwname, bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬႳ")), str(bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႴ"))))
        bstack111111l11l_opy_ = bstack11ll111_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨႵ").format(kwname, bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨႶ")))
        bstack1llllllll11_opy_ = error_message if bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႷ")) else bstack111111l11l_opy_
        bstack1lllllllll1_opy_ = {
            bstack11ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ⴘ"): self.bstack11111l1111_opy_[-1].get(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨႹ"), current_time()),
            bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴚ"): bstack1llllllll11_opy_,
            bstack11ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬႻ"): bstack11ll111_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭Ⴜ") if bstack1111111ll1_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨႽ")) == bstack11ll111_opy_ (u"ࠩࡉࡅࡎࡒࠧႾ") else bstack11ll111_opy_ (u"ࠪࡍࡓࡌࡏࠨႿ"),
            **bstack11lll1ll1_opy_.bstack1111l1lll1_opy_()
        }
        TestHubHandler.bstack1ll11l1ll_opy_([bstack1lllllllll1_opy_])
    def _11111lll11_opy_(self):
        for bstack111111llll_opy_ in reversed(self._11111l11ll_opy_):
            bstack11111l1l11_opy_ = bstack111111llll_opy_
            data = self._11111l11ll_opy_[bstack111111llll_opy_][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧჀ")]
            if isinstance(data, bstack1111ll11l1_opy_):
                if not bstack11ll111_opy_ (u"ࠬࡋࡁࡄࡊࠪჁ") in data.bstack1111111lll_opy_():
                    return bstack11111l1l11_opy_
            else:
                return bstack11111l1l11_opy_
    def _1111l11l11_opy_(self, messages):
        try:
            bstack111111ll11_opy_ = BuiltIn().get_variable_value(bstack11ll111_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧჂ")) in (bstack11111l1lll_opy_.DEBUG, bstack11111l1lll_opy_.TRACE)
            for message, bstack1lllllll11l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨჃ"))
                level = message.get(bstack11ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧჄ"))
                if level == bstack11111l1lll_opy_.FAIL:
                    self._1lllllll111_opy_ = name or self._1lllllll111_opy_
                    self._111111l1l1_opy_ = bstack1lllllll11l_opy_.get(bstack11ll111_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥჅ")) if bstack111111ll11_opy_ and bstack1lllllll11l_opy_ else self._111111l1l1_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1111l1111l_opy_: bstack1lllllll1ll_opy_, bstack11111111l1_opy_=False):
        if event == bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ჆"):
            bstack1111l1111l_opy_.set(hooks=self.store[bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨჇ")])
        if event == bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭჈"):
            event = bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ჉")
        if bstack11111111l1_opy_:
            bstack11111111ll_opy_ = {
                bstack11ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ჊"): event,
                bstack1111l1111l_opy_.bstack11111ll11l_opy_(): bstack1111l1111l_opy_.bstack1111111111_opy_(event)
            }
            with self._lock:
                self.bstack111111111l_opy_.append(bstack11111111ll_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1111l1111l_opy_)
class bstack11111lll1l_opy_:
    def __init__(self):
        self._1111111l1l_opy_ = []
    def bstack11111l11l1_opy_(self):
        self._1111111l1l_opy_.append([])
    def bstack1llllllll1l_opy_(self):
        return self._1111111l1l_opy_.pop() if self._1111111l1l_opy_ else list()
    def push(self, message):
        self._1111111l1l_opy_[-1].append(message) if self._1111111l1l_opy_ else self._1111111l1l_opy_.append([message])
class bstack11111l1lll_opy_:
    FAIL = bstack11ll111_opy_ (u"ࠨࡈࡄࡍࡑ࠭჋")
    ERROR = bstack11ll111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ჌")
    WARNING = bstack11ll111_opy_ (u"࡛ࠪࡆࡘࡎࠨჍ")
    bstack1llllllllll_opy_ = bstack11ll111_opy_ (u"ࠫࡎࡔࡆࡐࠩ჎")
    DEBUG = bstack11ll111_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫ჏")
    TRACE = bstack11ll111_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬა")
    bstack11111l1l1l_opy_ = [FAIL, ERROR]
def bstack1111l11111_opy_(bstack111111l1ll_opy_):
    if not bstack111111l1ll_opy_:
        return None
    if bstack111111l1ll_opy_.get(bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪბ"), None):
        return getattr(bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫგ")], bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧდ"), None)
    return bstack111111l1ll_opy_.get(bstack11ll111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨე"), None)
def bstack11111l1ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪვ"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧზ")]:
        return
    if hook_type.lower() == bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬთ"):
        if current_test_uuid is None:
            return bstack11ll111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫი")
        else:
            return bstack11ll111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭კ")
    elif hook_type.lower() == bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫლ"):
        if current_test_uuid is None:
            return bstack11ll111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭მ")
        else:
            return bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨნ")