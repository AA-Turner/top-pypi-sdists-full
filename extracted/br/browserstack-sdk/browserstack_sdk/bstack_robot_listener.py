# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111111l1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1111l111ll_opy_
from bstack_utils.test_data import bstack111111l111_opy_, bstack1111l1ll11_opy_, TestData
from bstack_utils.bstack1111l1l1l1_opy_ import bstack11l111ll11_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll11lll1_opy_, current_time, Result, \
    error_handler, bstack11111111l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧဗ"): [],
        bstack1111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪဘ"): [],
        bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩမ"): []
    }
    bstack11111l1ll1_opy_ = []
    bstack1111111ll1_opy_ = []
    @staticmethod
    def bstack1111ll1111_opy_(log):
        if not ((isinstance(log[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧယ")], list) or (isinstance(log[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨရ")], dict)) and len(log[bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩလ")])>0) or (isinstance(log[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဝ")], str) and log[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫသ")].strip())):
            return
        active = bstack11l111ll11_opy_.bstack1111ll1l11_opy_()
        log = {
            bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဟ"): log[bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫဠ")],
            bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩအ"): bstack11111111l1_opy_().isoformat() + bstack1111_opy_ (u"࡛ࠧࠩဢ"),
            bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဣ"): log[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဤ")],
        }
        if active:
            if active[bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨဥ")] == bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩဦ"):
                log[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬဧ")] = active[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ဨ")]
            elif active[bstack1111_opy_ (u"ࠧࡵࡻࡳࡩࠬဩ")] == bstack1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭ဪ"):
                log[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩါ")] = active[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪာ")]
        TestHubHandler.bstack1l1111l11_opy_([log])
    def __init__(self):
        self.messages = bstack111111llll_opy_()
        self._11111l1111_opy_ = None
        self._11111ll11l_opy_ = None
        self._1llllll1111_opy_ = OrderedDict()
        self.bstack1111ll11ll_opy_ = bstack1111l111ll_opy_(self.bstack1111ll1111_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llllllll11_opy_()
        if not self._1llllll1111_opy_.get(attrs.get(bstack1111_opy_ (u"ࠫ࡮ࡪࠧိ")), None):
            self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"ࠬ࡯ࡤࠨီ"))] = {}
        bstack111111111l_opy_ = TestData(
                bstack11111ll111_opy_=attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩု")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧူ")], start=os.getcwd()) if attrs.get(bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨေ")) != bstack1111_opy_ (u"ࠩࠪဲ") else bstack1111_opy_ (u"ࠪࠫဳ"),
                framework=bstack1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪဴ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1111_opy_ (u"ࠬ࡯ࡤࠨဵ"), None)
        self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩံ"))][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣ့ࠪ")] = bstack111111111l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11111llll1_opy_()
        self._11111l1lll_opy_(messages)
        with self._lock:
            for bstack1lllllllll1_opy_ in self.bstack11111l1ll1_opy_:
                bstack1lllllllll1_opy_[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪး")][bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ္")].extend(self.store[bstack1111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴ်ࠩ")])
                TestHubHandler.bstack1111lll11_opy_(bstack1lllllllll1_opy_)
            self.bstack11111l1ll1_opy_ = []
            self.store[bstack1111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪျ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111ll11ll_opy_.start()
        if not self._1llllll1111_opy_.get(attrs.get(bstack1111_opy_ (u"ࠬ࡯ࡤࠨြ")), None):
            self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩွ"))] = {}
        driver = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ှ"), None)
        test_data = TestData(
            bstack11111ll111_opy_=attrs.get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫဿ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ၀")], start=os.getcwd()),
            scope=RobotHandler.bstack11111l1l11_opy_(attrs.get(bstack1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ၁"), None)),
            framework=bstack1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ၂"),
            tags=attrs[bstack1111_opy_ (u"ࠬࡺࡡࡨࡵࠪ၃")],
            hooks=self.store[bstack1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ၄")],
            integrations=TestHubHandler.bstack11111lllll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1111_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤ၅").format(bstack1111_opy_ (u"ࠣࠢࠥ၆").join(attrs[bstack1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ၇")]), name) if attrs[bstack1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ၈")] else name
        )
        self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"ࠫ࡮ࡪࠧ၉"))][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ၊")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1llllll11ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩ။"), None)
        self.send_run_event(bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ၌"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111ll11ll_opy_.reset()
        bstack1lllllll1l1_opy_ = bstack1lllllll1ll_opy_.get(attrs.get(bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ၍")), bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ၎"))
        self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"ࠪ࡭ࡩ࠭၏"))][bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၐ")].stop(time=current_time(), duration=int(attrs.get(bstack1111_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪၑ"), bstack1111_opy_ (u"࠭࠰ࠨၒ"))), result=Result(result=bstack1lllllll1l1_opy_, exception=attrs.get(bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨၓ")), bstack1111l11lll_opy_=[attrs.get(bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩၔ"))]))
        self.send_run_event(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫၕ"), self._1llllll1111_opy_[attrs.get(bstack1111_opy_ (u"ࠪ࡭ࡩ࠭ၖ"))][bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၗ")], True)
        with self._lock:
            self.store[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩၘ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llllllll11_opy_()
        current_test_id = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨၙ"), None)
        bstack1llllll1l1l_opy_ = current_test_id if bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩၚ"), None) else bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫၛ"), None)
        if attrs.get(bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧၜ"), bstack1111_opy_ (u"ࠪࠫၝ")).lower() in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪၞ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧၟ")]:
            hook_type = bstack1llllll1ll1_opy_(attrs.get(bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫၠ")), bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫၡ"), None))
            hook_name = bstack1111_opy_ (u"ࠨࡽࢀࠫၢ").format(attrs.get(bstack1111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩၣ"), bstack1111_opy_ (u"ࠪࠫၤ")))
            if hook_type in [bstack1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨၥ"), bstack1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨၦ")]:
                hook_name = bstack1111_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧၧ").format(bstack1llllll11l1_opy_.get(hook_type), attrs.get(bstack1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧၨ"), bstack1111_opy_ (u"ࠨࠩၩ")))
            bstack11111l11ll_opy_ = bstack1111l1ll11_opy_(
                bstack11111ll111_opy_=bstack1llllll1l1l_opy_ + bstack1111_opy_ (u"ࠩ࠰ࠫၪ") + attrs.get(bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨၫ"), bstack1111_opy_ (u"ࠫࠬၬ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬၭ")), start=os.getcwd()),
                framework=bstack1111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬၮ"),
                tags=attrs[bstack1111_opy_ (u"ࠧࡵࡣࡪࡷࠬၯ")],
                scope=RobotHandler.bstack11111l1l11_opy_(attrs.get(bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨၰ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11111l11ll_opy_.bstack1llllll11ll_opy_()
            threading.current_thread().current_hook_id = bstack1llllll1l1l_opy_ + bstack1111_opy_ (u"ࠩ࠰ࠫၱ") + attrs.get(bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨၲ"), bstack1111_opy_ (u"ࠫࠬၳ")).lower()
            with self._lock:
                self.store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩၴ")] = [bstack11111l11ll_opy_.bstack1llllll11ll_opy_()]
                if bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪၵ"), None):
                    self.store[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫၶ")].append(bstack11111l11ll_opy_.bstack1llllll11ll_opy_())
                else:
                    self.store[bstack1111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧၷ")].append(bstack11111l11ll_opy_.bstack1llllll11ll_opy_())
            if bstack1llllll1l1l_opy_:
                self._1llllll1111_opy_[bstack1llllll1l1l_opy_ + bstack1111_opy_ (u"ࠩ࠰ࠫၸ") + attrs.get(bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨၹ"), bstack1111_opy_ (u"ࠫࠬၺ")).lower()] = { bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၻ"): bstack11111l11ll_opy_ }
            TestHubHandler.send_run_event(bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧၼ"), bstack11111l11ll_opy_)
        else:
            bstack1111l1lll1_opy_ = {
                bstack1111_opy_ (u"ࠧࡪࡦࠪၽ"): uuid4().__str__(),
                bstack1111_opy_ (u"ࠨࡶࡨࡼࡹ࠭ၾ"): bstack1111_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨၿ").format(attrs.get(bstack1111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪႀ")), attrs.get(bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩႁ"), bstack1111_opy_ (u"ࠬ࠭ႂ"))) if attrs.get(bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫႃ"), []) else attrs.get(bstack1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧႄ")),
                bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨႅ"): attrs.get(bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧႆ"), []),
                bstack1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧႇ"): current_time(),
                bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫႈ"): bstack1111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ႉ"),
                bstack1111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫႊ"): attrs.get(bstack1111_opy_ (u"ࠧࡥࡱࡦࠫႋ"), bstack1111_opy_ (u"ࠨࠩႌ"))
            }
            if attrs.get(bstack1111_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧႍࠪ"), bstack1111_opy_ (u"ࠪࠫႎ")) != bstack1111_opy_ (u"ࠫࠬႏ"):
                bstack1111l1lll1_opy_[bstack1111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭႐")] = attrs.get(bstack1111_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ႑"))
            if not self.bstack1111111ll1_opy_:
                self._1llllll1111_opy_[self._1111111lll_opy_()][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ႒")].add_step(bstack1111l1lll1_opy_)
                threading.current_thread().current_step_uuid = bstack1111l1lll1_opy_[bstack1111_opy_ (u"ࠨ࡫ࡧࠫ႓")]
            self.bstack1111111ll1_opy_.append(bstack1111l1lll1_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11111llll1_opy_()
        self._11111l1lll_opy_(messages)
        current_test_id = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ႔"), None)
        bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭႕"), None)
        bstack1llllllllll_opy_ = bstack1lllllll1ll_opy_.get(attrs.get(bstack1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ႖")), bstack1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭႗"))
        bstack111111lll1_opy_ = attrs.get(bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ႘"))
        if bstack1llllllllll_opy_ != bstack1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ႙") and not attrs.get(bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႚ")) and self._11111l1111_opy_:
            bstack111111lll1_opy_ = self._11111l1111_opy_
        bstack1111l11l11_opy_ = Result(result=bstack1llllllllll_opy_, exception=bstack111111lll1_opy_, bstack1111l11lll_opy_=[bstack111111lll1_opy_])
        if attrs.get(bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧႛ"), bstack1111_opy_ (u"ࠪࠫႜ")).lower() in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪႝ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ႞")]:
            bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ႟"), None)
            if bstack1llllll1l1l_opy_:
                bstack1111l1ll1l_opy_ = bstack1llllll1l1l_opy_ + bstack1111_opy_ (u"ࠢ࠮ࠤႠ") + attrs.get(bstack1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ⴁ"), bstack1111_opy_ (u"ࠩࠪႢ")).lower()
                self._1llllll1111_opy_[bstack1111l1ll1l_opy_][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴃ")].stop(time=current_time(), duration=int(attrs.get(bstack1111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩႤ"), bstack1111_opy_ (u"ࠬ࠶ࠧႥ"))), result=bstack1111l11l11_opy_)
                TestHubHandler.send_run_event(bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨႦ"), self._1llllll1111_opy_[bstack1111l1ll1l_opy_][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႧ")])
        else:
            bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪႨ"), None)
            if bstack1llllll1l1l_opy_ and len(self.bstack1111111ll1_opy_) == 1:
                current_step_uuid = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭Ⴉ"), None)
                self._1llllll1111_opy_[bstack1llllll1l1l_opy_][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴊ")].bstack1111l1l11l_opy_(current_step_uuid, duration=int(attrs.get(bstack1111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩႫ"), bstack1111_opy_ (u"ࠬ࠶ࠧႬ"))), result=bstack1111l11l11_opy_)
            else:
                self.bstack1lllllll11l_opy_(attrs)
            self.bstack1111111ll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1111_opy_ (u"࠭ࡨࡵ࡯࡯ࠫႭ"), bstack1111_opy_ (u"ࠧ࡯ࡱࠪႮ")) == bstack1111_opy_ (u"ࠨࡻࡨࡷࠬႯ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l111ll11_opy_.bstack1111ll1l11_opy_():
                logs.append({
                    bstack1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬႰ"): current_time(),
                    bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႱ"): message.get(bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႲ")),
                    bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫႳ"): message.get(bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬႴ")),
                    **bstack11l111ll11_opy_.bstack1111ll1l11_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1l1111l11_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1llllll111l_opy_()
    def bstack1lllllll11l_opy_(self, bstack11111l111l_opy_):
        if not bstack11l111ll11_opy_.bstack1111ll1l11_opy_():
            return
        kwname = bstack1111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭Ⴕ").format(bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨႶ")), bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧႷ"), bstack1111_opy_ (u"ࠪࠫႸ"))) if bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩႹ"), []) else bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬႺ"))
        error_message = bstack1111_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧႻ").format(kwname, bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧႼ")), str(bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႽ"))))
        bstack111111l1ll_opy_ = bstack1111_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣႾ").format(kwname, bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪႿ")))
        bstack11111lll11_opy_ = error_message if bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჀ")) else bstack111111l1ll_opy_
        bstack111111ll11_opy_ = {
            bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨჁ"): self.bstack1111111ll1_opy_[-1].get(bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪჂ"), current_time()),
            bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨჃ"): bstack11111lll11_opy_,
            bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧჄ"): bstack1111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨჅ") if bstack11111l111l_opy_.get(bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ჆")) == bstack1111_opy_ (u"ࠫࡋࡇࡉࡍࠩჇ") else bstack1111_opy_ (u"ࠬࡏࡎࡇࡑࠪ჈"),
            **bstack11l111ll11_opy_.bstack1111ll1l11_opy_()
        }
        TestHubHandler.bstack1l1111l11_opy_([bstack111111ll11_opy_])
    def _1111111lll_opy_(self):
        for bstack11111ll111_opy_ in reversed(self._1llllll1111_opy_):
            bstack11111l1l1l_opy_ = bstack11111ll111_opy_
            data = self._1llllll1111_opy_[bstack11111ll111_opy_][bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ჉")]
            if isinstance(data, bstack1111l1ll11_opy_):
                if not bstack1111_opy_ (u"ࠧࡆࡃࡆࡌࠬ჊") in data.bstack111111l11l_opy_():
                    return bstack11111l1l1l_opy_
            else:
                return bstack11111l1l1l_opy_
    def _11111l1lll_opy_(self, messages):
        try:
            bstack11111111ll_opy_ = BuiltIn().get_variable_value(bstack1111_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ჋")) in (bstack1111111l11_opy_.DEBUG, bstack1111111l11_opy_.TRACE)
            for message, bstack1lllllll111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ჌"))
                level = message.get(bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩჍ"))
                if level == bstack1111111l11_opy_.FAIL:
                    self._11111l1111_opy_ = name or self._11111l1111_opy_
                    self._11111ll11l_opy_ = bstack1lllllll111_opy_.get(bstack1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ჎")) if bstack11111111ll_opy_ and bstack1lllllll111_opy_ else self._11111ll11l_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack11111l11l1_opy_: bstack111111l111_opy_, bstack11111ll1l1_opy_=False):
        if event == bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ჏"):
            bstack11111l11l1_opy_.set(hooks=self.store[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪა")])
        if event == bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨბ"):
            event = bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪგ")
        if bstack11111ll1l1_opy_:
            bstack1llllll1l11_opy_ = {
                bstack1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭დ"): event,
                bstack11111l11l1_opy_.bstack1111111111_opy_(): bstack11111l11l1_opy_.bstack1llllll1lll_opy_(event)
            }
            with self._lock:
                self.bstack11111l1ll1_opy_.append(bstack1llllll1l11_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack11111l11l1_opy_)
class bstack111111llll_opy_:
    def __init__(self):
        self._111111ll1l_opy_ = []
    def bstack1llllllll11_opy_(self):
        self._111111ll1l_opy_.append([])
    def bstack11111llll1_opy_(self):
        return self._111111ll1l_opy_.pop() if self._111111ll1l_opy_ else list()
    def push(self, message):
        self._111111ll1l_opy_[-1].append(message) if self._111111ll1l_opy_ else self._111111ll1l_opy_.append([message])
class bstack1111111l11_opy_:
    FAIL = bstack1111_opy_ (u"ࠪࡊࡆࡏࡌࠨე")
    ERROR = bstack1111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪვ")
    WARNING = bstack1111_opy_ (u"ࠬ࡝ࡁࡓࡐࠪზ")
    bstack111111l1l1_opy_ = bstack1111_opy_ (u"࠭ࡉࡏࡈࡒࠫთ")
    DEBUG = bstack1111_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭ი")
    TRACE = bstack1111_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧკ")
    bstack11111ll1ll_opy_ = [FAIL, ERROR]
def bstack11111lll1l_opy_(bstack1llllllll1l_opy_):
    if not bstack1llllllll1l_opy_:
        return None
    if bstack1llllllll1l_opy_.get(bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬლ"), None):
        return getattr(bstack1llllllll1l_opy_[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭მ")], bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩნ"), None)
    return bstack1llllllll1l_opy_.get(bstack1111_opy_ (u"ࠬࡻࡵࡪࡦࠪო"), None)
def bstack1llllll1ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬპ"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩჟ")]:
        return
    if hook_type.lower() == bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧრ"):
        if current_test_uuid is None:
            return bstack1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ს")
        else:
            return bstack1111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨტ")
    elif hook_type.lower() == bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭უ"):
        if current_test_uuid is None:
            return bstack1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨფ")
        else:
            return bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪქ")