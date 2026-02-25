# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11111ll1ll_opy_ import RobotHandler
from bstack_utils.capture import bstack1111l1lll1_opy_
from bstack_utils.test_data import bstack1lllllll1ll_opy_, bstack1111l11lll_opy_, TestData
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack11llll11l1_opy_, current_time, Result, \
    error_handler, bstack1llllll1lll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩဒ"): [],
        bstack11l1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬဓ"): [],
        bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫန"): []
    }
    bstack1111111l11_opy_ = []
    bstack111111l111_opy_ = []
    @staticmethod
    def bstack1111l1l11l_opy_(log):
        if not ((isinstance(log[bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩပ")], list) or (isinstance(log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဖ")], dict)) and len(log[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဗ")])>0) or (isinstance(log[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬဘ")], str) and log[bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭မ")].strip())):
            return
        active = bstack1l111111_opy_.bstack1111l1l1l1_opy_()
        log = {
            bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬယ"): log[bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ရ")],
            bstack11l1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫလ"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠩ࡝ࠫဝ"),
            bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫသ"): log[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬဟ")],
        }
        if active:
            if active[bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪဠ")] == bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫအ"):
                log[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧဢ")] = active[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨဣ")]
            elif active[bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧဤ")] == bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨဥ"):
                log[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫဦ")] = active[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬဧ")]
        TestHubHandler.bstack1l111ll1_opy_([log])
    def __init__(self):
        self.messages = bstack1llllllllll_opy_()
        self._111111111l_opy_ = None
        self._1lllllll111_opy_ = None
        self._1111l11l11_opy_ = OrderedDict()
        self.bstack1111ll1lll_opy_ = bstack1111l1lll1_opy_(self.bstack1111l1l11l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1111111lll_opy_()
        if not self._1111l11l11_opy_.get(attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩဨ")), None):
            self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠧࡪࡦࠪဩ"))] = {}
        bstack1111l11111_opy_ = TestData(
                bstack11111l111l_opy_=attrs.get(bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫဪ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack11l1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩါ")], start=os.getcwd()) if attrs.get(bstack11l1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪာ")) != bstack11l1l11_opy_ (u"ࠫࠬိ") else bstack11l1l11_opy_ (u"ࠬ࠭ီ"),
                framework=bstack11l1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬု")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1l11_opy_ (u"ࠧࡪࡦࠪူ"), None)
        self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫေ"))][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဲ")] = bstack1111l11111_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11111lll1l_opy_()
        self._1111111ll1_opy_(messages)
        with self._lock:
            for bstack1111l111l1_opy_ in self.bstack1111111l11_opy_:
                bstack1111l111l1_opy_[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬဳ")][bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪဴ")].extend(self.store[bstack11l1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫဵ")])
                TestHubHandler.bstack1l1ll11lll_opy_(bstack1111l111l1_opy_)
            self.bstack1111111l11_opy_ = []
            self.store[bstack11l1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬံ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111ll1lll_opy_.start()
        if not self._1111l11l11_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠧࡪࡦ့ࠪ")), None):
            self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫး"))] = {}
        driver = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ္"), None)
        test_data = TestData(
            bstack11111l111l_opy_=attrs.get(bstack11l1l11_opy_ (u"ࠪ࡭ࡩ်࠭")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack11l1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫျ")], start=os.getcwd()),
            scope=RobotHandler.bstack111111lll1_opy_(attrs.get(bstack11l1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬြ"), None)),
            framework=bstack11l1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬွ"),
            tags=attrs[bstack11l1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬှ")],
            hooks=self.store[bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧဿ")],
            integrations=TestHubHandler.bstack1111ll1ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1l11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦ၀").format(bstack11l1l11_opy_ (u"ࠥࠤࠧ၁").join(attrs[bstack11l1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩ၂")]), name) if attrs[bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪ၃")] else name
        )
        self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ၄"))][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ၅")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack11111ll1l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫ၆"), None)
        self.send_run_event(bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ၇"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111ll1lll_opy_.reset()
        bstack1111111l1l_opy_ = bstack1lllllll11l_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ၈")), bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ၉"))
        self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ၊"))][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ။")].stop(time=current_time(), duration=int(attrs.get(bstack11l1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ၌"), bstack11l1l11_opy_ (u"ࠨ࠲ࠪ၍"))), result=Result(result=bstack1111111l1l_opy_, exception=attrs.get(bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ၎")), bstack1111l11ll1_opy_=[attrs.get(bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ၏"))]))
        self.send_run_event(bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ၐ"), self._1111l11l11_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨၑ"))][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩၒ")], True)
        with self._lock:
            self.store[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫၓ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1111111lll_opy_()
        current_test_id = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪၔ"), None)
        bstack111111llll_opy_ = current_test_id if bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫၕ"), None) else bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ၖ"), None)
        if attrs.get(bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩၗ"), bstack11l1l11_opy_ (u"ࠬ࠭ၘ")).lower() in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬၙ"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩၚ")]:
            hook_type = bstack11111lllll_opy_(attrs.get(bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၛ")), bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ၜ"), None))
            hook_name = bstack11l1l11_opy_ (u"ࠪࡿࢂ࠭ၝ").format(attrs.get(bstack11l1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫၞ"), bstack11l1l11_opy_ (u"ࠬ࠭ၟ")))
            if hook_type in [bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪၠ"), bstack11l1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪၡ")]:
                hook_name = bstack11l1l11_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩၢ").format(bstack11111l1l11_opy_.get(hook_type), attrs.get(bstack11l1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩၣ"), bstack11l1l11_opy_ (u"ࠪࠫၤ")))
            bstack11111l1lll_opy_ = bstack1111l11lll_opy_(
                bstack11111l111l_opy_=bstack111111llll_opy_ + bstack11l1l11_opy_ (u"ࠫ࠲࠭ၥ") + attrs.get(bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪၦ"), bstack11l1l11_opy_ (u"࠭ࠧၧ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack11l1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧၨ")), start=os.getcwd()),
                framework=bstack11l1l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧၩ"),
                tags=attrs[bstack11l1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧၪ")],
                scope=RobotHandler.bstack111111lll1_opy_(attrs.get(bstack11l1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪၫ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11111l1lll_opy_.bstack11111ll1l1_opy_()
            threading.current_thread().current_hook_id = bstack111111llll_opy_ + bstack11l1l11_opy_ (u"ࠫ࠲࠭ၬ") + attrs.get(bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪၭ"), bstack11l1l11_opy_ (u"࠭ࠧၮ")).lower()
            with self._lock:
                self.store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫၯ")] = [bstack11111l1lll_opy_.bstack11111ll1l1_opy_()]
                if bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬၰ"), None):
                    self.store[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ၱ")].append(bstack11111l1lll_opy_.bstack11111ll1l1_opy_())
                else:
                    self.store[bstack11l1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩၲ")].append(bstack11111l1lll_opy_.bstack11111ll1l1_opy_())
            if bstack111111llll_opy_:
                self._1111l11l11_opy_[bstack111111llll_opy_ + bstack11l1l11_opy_ (u"ࠫ࠲࠭ၳ") + attrs.get(bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪၴ"), bstack11l1l11_opy_ (u"࠭ࠧၵ")).lower()] = { bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪၶ"): bstack11111l1lll_opy_ }
            TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩၷ"), bstack11111l1lll_opy_)
        else:
            bstack1111l1l1ll_opy_ = {
                bstack11l1l11_opy_ (u"ࠩ࡬ࡨࠬၸ"): uuid4().__str__(),
                bstack11l1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨၹ"): bstack11l1l11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪၺ").format(attrs.get(bstack11l1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬၻ")), attrs.get(bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫၼ"), bstack11l1l11_opy_ (u"ࠧࠨၽ"))) if attrs.get(bstack11l1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ၾ"), []) else attrs.get(bstack11l1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩၿ")),
                bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪႀ"): attrs.get(bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩႁ"), []),
                bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩႂ"): current_time(),
                bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ႃ"): bstack11l1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨႄ"),
                bstack11l1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ႅ"): attrs.get(bstack11l1l11_opy_ (u"ࠩࡧࡳࡨ࠭ႆ"), bstack11l1l11_opy_ (u"ࠪࠫႇ"))
            }
            if attrs.get(bstack11l1l11_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬႈ"), bstack11l1l11_opy_ (u"ࠬ࠭ႉ")) != bstack11l1l11_opy_ (u"࠭ࠧႊ"):
                bstack1111l1l1ll_opy_[bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨႋ")] = attrs.get(bstack11l1l11_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩႌ"))
            if not self.bstack111111l111_opy_:
                self._1111l11l11_opy_[self._11111l1ll1_opy_()][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥႍࠬ")].add_step(bstack1111l1l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack1111l1l1ll_opy_[bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ႎ")]
            self.bstack111111l111_opy_.append(bstack1111l1l1ll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11111lll1l_opy_()
        self._1111111ll1_opy_(messages)
        current_test_id = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ႏ"), None)
        bstack111111llll_opy_ = current_test_id if current_test_id else bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ႐"), None)
        bstack11111l1l1l_opy_ = bstack1lllllll11l_opy_.get(attrs.get(bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭႑")), bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ႒"))
        bstack1111111111_opy_ = attrs.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ႓"))
        if bstack11111l1l1l_opy_ != bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ႔") and not attrs.get(bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ႕")) and self._111111111l_opy_:
            bstack1111111111_opy_ = self._111111111l_opy_
        bstack1111lll1ll_opy_ = Result(result=bstack11111l1l1l_opy_, exception=bstack1111111111_opy_, bstack1111l11ll1_opy_=[bstack1111111111_opy_])
        if attrs.get(bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ႖"), bstack11l1l11_opy_ (u"ࠬ࠭႗")).lower() in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ႘"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ႙")]:
            bstack111111llll_opy_ = current_test_id if current_test_id else bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫႚ"), None)
            if bstack111111llll_opy_:
                bstack1111l1ll11_opy_ = bstack111111llll_opy_ + bstack11l1l11_opy_ (u"ࠤ࠰ࠦႛ") + attrs.get(bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨႜ"), bstack11l1l11_opy_ (u"ࠫࠬႝ")).lower()
                self._1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ႞")].stop(time=current_time(), duration=int(attrs.get(bstack11l1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ႟"), bstack11l1l11_opy_ (u"ࠧ࠱ࠩႠ"))), result=bstack1111lll1ll_opy_)
                TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪႡ"), self._1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႢ")])
        else:
            bstack111111llll_opy_ = current_test_id if current_test_id else bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬႣ"), None)
            if bstack111111llll_opy_ and len(self.bstack111111l111_opy_) == 1:
                current_step_uuid = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨႤ"), None)
                self._1111l11l11_opy_[bstack111111llll_opy_][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨႥ")].bstack1111l1llll_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫႦ"), bstack11l1l11_opy_ (u"ࠧ࠱ࠩႧ"))), result=bstack1111lll1ll_opy_)
            else:
                self.bstack11111ll11l_opy_(attrs)
            self.bstack111111l111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1l11_opy_ (u"ࠨࡪࡷࡱࡱ࠭Ⴈ"), bstack11l1l11_opy_ (u"ࠩࡱࡳࠬႩ")) == bstack11l1l11_opy_ (u"ࠪࡽࡪࡹࠧႪ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l111111_opy_.bstack1111l1l1l1_opy_():
                logs.append({
                    bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧႫ"): current_time(),
                    bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴌ"): message.get(bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႭ")),
                    bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ⴎ"): message.get(bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧႯ")),
                    **bstack1l111111_opy_.bstack1111l1l1l1_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1l111ll1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1llllllll1l_opy_()
    def bstack11111ll11l_opy_(self, bstack1lllllllll1_opy_):
        if not bstack1l111111_opy_.bstack1111l1l1l1_opy_():
            return
        kwname = bstack11l1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨႰ").format(bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪႱ")), bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩႲ"), bstack11l1l11_opy_ (u"ࠬ࠭Ⴓ"))) if bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫႴ"), []) else bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧႵ"))
        error_message = bstack11l1l11_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢႶ").format(kwname, bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩႷ")), str(bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႸ"))))
        bstack11111llll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥႹ").format(kwname, bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬႺ")))
        bstack1111l111ll_opy_ = error_message if bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႻ")) else bstack11111llll1_opy_
        bstack111111l1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪႼ"): self.bstack111111l111_opy_[-1].get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬႽ"), current_time()),
            bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႾ"): bstack1111l111ll_opy_,
            bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႿ"): bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪჀ") if bstack1lllllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬჁ")) == bstack11l1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫჂ") else bstack11l1l11_opy_ (u"ࠧࡊࡐࡉࡓࠬჃ"),
            **bstack1l111111_opy_.bstack1111l1l1l1_opy_()
        }
        TestHubHandler.bstack1l111ll1_opy_([bstack111111l1ll_opy_])
    def _11111l1ll1_opy_(self):
        for bstack11111l111l_opy_ in reversed(self._1111l11l11_opy_):
            bstack11111111ll_opy_ = bstack11111l111l_opy_
            data = self._1111l11l11_opy_[bstack11111l111l_opy_][bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫჄ")]
            if isinstance(data, bstack1111l11lll_opy_):
                if not bstack11l1l11_opy_ (u"ࠩࡈࡅࡈࡎࠧჅ") in data.bstack11111111l1_opy_():
                    return bstack11111111ll_opy_
            else:
                return bstack11111111ll_opy_
    def _1111111ll1_opy_(self, messages):
        try:
            bstack1111l1111l_opy_ = BuiltIn().get_variable_value(bstack11l1l11_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ჆")) in (bstack11111ll111_opy_.DEBUG, bstack11111ll111_opy_.TRACE)
            for message, bstack111111l11l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჇ"))
                level = message.get(bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ჈"))
                if level == bstack11111ll111_opy_.FAIL:
                    self._111111111l_opy_ = name or self._111111111l_opy_
                    self._1lllllll111_opy_ = bstack111111l11l_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ჉")) if bstack1111l1111l_opy_ and bstack111111l11l_opy_ else self._1lllllll111_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack111111ll11_opy_: bstack1lllllll1ll_opy_, bstack111111ll1l_opy_=False):
        if event == bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ჊"):
            bstack111111ll11_opy_.set(hooks=self.store[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ჋")])
        if event == bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ჌"):
            event = bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬჍ")
        if bstack111111ll1l_opy_:
            bstack111111l1l1_opy_ = {
                bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ჎"): event,
                bstack111111ll11_opy_.bstack1111l11l1l_opy_(): bstack111111ll11_opy_.bstack1llllllll11_opy_(event)
            }
            with self._lock:
                self.bstack1111111l11_opy_.append(bstack111111l1l1_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack111111ll11_opy_)
class bstack1llllllllll_opy_:
    def __init__(self):
        self._11111l1111_opy_ = []
    def bstack1111111lll_opy_(self):
        self._11111l1111_opy_.append([])
    def bstack11111lll1l_opy_(self):
        return self._11111l1111_opy_.pop() if self._11111l1111_opy_ else list()
    def push(self, message):
        self._11111l1111_opy_[-1].append(message) if self._11111l1111_opy_ else self._11111l1111_opy_.append([message])
class bstack11111ll111_opy_:
    FAIL = bstack11l1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪ჏")
    ERROR = bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬა")
    WARNING = bstack11l1l11_opy_ (u"ࠧࡘࡃࡕࡒࠬბ")
    bstack11111l11l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭გ")
    DEBUG = bstack11l1l11_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨდ")
    TRACE = bstack11l1l11_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩე")
    bstack11111l11ll_opy_ = [FAIL, ERROR]
def bstack11111lll11_opy_(bstack1lllllll1l1_opy_):
    if not bstack1lllllll1l1_opy_:
        return None
    if bstack1lllllll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧვ"), None):
        return getattr(bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨზ")], bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫთ"), None)
    return bstack1lllllll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬი"), None)
def bstack11111lllll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧკ"), bstack11l1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫლ")]:
        return
    if hook_type.lower() == bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩმ"):
        if current_test_uuid is None:
            return bstack11l1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨნ")
        else:
            return bstack11l1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪო")
    elif hook_type.lower() == bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨპ"):
        if current_test_uuid is None:
            return bstack11l1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪჟ")
        else:
            return bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬრ")