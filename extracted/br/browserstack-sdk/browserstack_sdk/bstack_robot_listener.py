# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1llllll1lll_opy_ import RobotHandler
from bstack_utils.capture import bstack1111l1l11l_opy_
from bstack_utils.test_data import bstack11111llll1_opy_, bstack1111ll1l11_opy_, TestData
from bstack_utils.bstack1111ll1111_opy_ import bstack111lllll1_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll111ll_opy_, current_time, Result, \
    error_handler, bstack11111l1ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ဖ"): [],
        bstack1lll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩဗ"): [],
        bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨဘ"): []
    }
    bstack1llllll11l1_opy_ = []
    bstack11111lllll_opy_ = []
    @staticmethod
    def bstack1111ll1l1l_opy_(log):
        if not ((isinstance(log[bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭မ")], list) or (isinstance(log[bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧယ")], dict)) and len(log[bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨရ")])>0) or (isinstance(log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩလ")], str) and log[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဝ")].strip())):
            return
        active = bstack111lllll1_opy_.bstack1111l111ll_opy_()
        log = {
            bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩသ"): log[bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဟ")],
            bstack1lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨဠ"): bstack11111l1ll1_opy_().isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨအ"),
            bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ"): log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဣ")],
        }
        if active:
            if active[bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧဤ")] == bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨဥ"):
                log[bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫဦ")] = active[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬဧ")]
            elif active[bstack1lll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫဨ")] == bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬဩ"):
                log[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨဪ")] = active[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩါ")]
        TestHubHandler.bstack11ll1l1l11_opy_([log])
    def __init__(self):
        self.messages = bstack111111l111_opy_()
        self._1lllllll11l_opy_ = None
        self._111111ll11_opy_ = None
        self._111111l11l_opy_ = OrderedDict()
        self.bstack1111ll11l1_opy_ = bstack1111l1l11l_opy_(self.bstack1111ll1l1l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11111l1lll_opy_()
        if not self._111111l11l_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ာ")), None):
            self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧိ"))] = {}
        bstack11111lll1l_opy_ = TestData(
                bstack11111ll11l_opy_=attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨီ")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1lll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ု")], start=os.getcwd()) if attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧူ")) != bstack1lll1l_opy_ (u"ࠨࠩေ") else bstack1lll1l_opy_ (u"ࠩࠪဲ"),
                framework=bstack1lll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩဳ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧဴ"), None)
        self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨဵ"))][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩံ")] = bstack11111lll1l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llllll11ll_opy_()
        self._1llllllllll_opy_(messages)
        with self._lock:
            for bstack111111llll_opy_ in self.bstack1llllll11l1_opy_:
                bstack111111llll_opy_[bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯့ࠩ")][bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧး")].extend(self.store[bstack1lll1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ္")])
                TestHubHandler.bstack11lll111ll_opy_(bstack111111llll_opy_)
            self.bstack1llllll11l1_opy_ = []
            self.store[bstack1lll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴ်ࠩ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111ll11l1_opy_.start()
        if not self._111111l11l_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧျ")), None):
            self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨြ"))] = {}
        driver = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬွ"), None)
        test_data = TestData(
            bstack11111ll11l_opy_=attrs.get(bstack1lll1l_opy_ (u"ࠧࡪࡦࠪှ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1lll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨဿ")], start=os.getcwd()),
            scope=RobotHandler.bstack111111l1ll_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ၀"), None)),
            framework=bstack1lll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ၁"),
            tags=attrs[bstack1lll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩ၂")],
            hooks=self.store[bstack1lll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ၃")],
            integrations=TestHubHandler.bstack1111l11ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1lll1l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣ၄").format(bstack1lll1l_opy_ (u"ࠢࠡࠤ၅").join(attrs[bstack1lll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭၆")]), name) if attrs[bstack1lll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ၇")] else name
        )
        self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭၈"))][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ၉")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack111111lll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨ၊"), None)
        self.send_run_event(bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ။"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111ll11l1_opy_.reset()
        bstack1lllllllll1_opy_ = bstack111111l1l1_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ၌")), bstack1lll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ၍"))
        self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬ၎"))][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭၏")].stop(time=current_time(), duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩၐ"), bstack1lll1l_opy_ (u"ࠬ࠶ࠧၑ"))), result=Result(result=bstack1lllllllll1_opy_, exception=attrs.get(bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧၒ")), bstack1111l1ll1l_opy_=[attrs.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨၓ"))]))
        self.send_run_event(bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪၔ"), self._111111l11l_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬၕ"))][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ၖ")], True)
        with self._lock:
            self.store[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨၗ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11111l1lll_opy_()
        current_test_id = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧၘ"), None)
        bstack1llllll1l1l_opy_ = current_test_id if bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨၙ"), None) else bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪၚ"), None)
        if attrs.get(bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၛ"), bstack1lll1l_opy_ (u"ࠩࠪၜ")).lower() in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩၝ"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ၞ")]:
            hook_type = bstack1llllllll1l_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪၟ")), bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪၠ"), None))
            hook_name = bstack1lll1l_opy_ (u"ࠧࡼࡿࠪၡ").format(attrs.get(bstack1lll1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨၢ"), bstack1lll1l_opy_ (u"ࠩࠪၣ")))
            if hook_type in [bstack1lll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧၤ"), bstack1lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧၥ")]:
                hook_name = bstack1lll1l_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭ၦ").format(bstack11111lll11_opy_.get(hook_type), attrs.get(bstack1lll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ၧ"), bstack1lll1l_opy_ (u"ࠧࠨၨ")))
            bstack1llllll1l11_opy_ = bstack1111ll1l11_opy_(
                bstack11111ll11l_opy_=bstack1llllll1l1l_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪၩ") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧၪ"), bstack1lll1l_opy_ (u"ࠪࠫၫ")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1lll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫၬ")), start=os.getcwd()),
                framework=bstack1lll1l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫၭ"),
                tags=attrs[bstack1lll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫၮ")],
                scope=RobotHandler.bstack111111l1ll_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧၯ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1llllll1l11_opy_.bstack111111lll1_opy_()
            threading.current_thread().current_hook_id = bstack1llllll1l1l_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪၰ") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧၱ"), bstack1lll1l_opy_ (u"ࠪࠫၲ")).lower()
            with self._lock:
                self.store[bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨၳ")] = [bstack1llllll1l11_opy_.bstack111111lll1_opy_()]
                if bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩၴ"), None):
                    self.store[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪၵ")].append(bstack1llllll1l11_opy_.bstack111111lll1_opy_())
                else:
                    self.store[bstack1lll1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ၶ")].append(bstack1llllll1l11_opy_.bstack111111lll1_opy_())
            if bstack1llllll1l1l_opy_:
                self._111111l11l_opy_[bstack1llllll1l1l_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪၷ") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧၸ"), bstack1lll1l_opy_ (u"ࠪࠫၹ")).lower()] = { bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၺ"): bstack1llllll1l11_opy_ }
            TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ၻ"), bstack1llllll1l11_opy_)
        else:
            bstack1111l1l1l1_opy_ = {
                bstack1lll1l_opy_ (u"࠭ࡩࡥࠩၼ"): uuid4().__str__(),
                bstack1lll1l_opy_ (u"ࠧࡵࡧࡻࡸࠬၽ"): bstack1lll1l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧၾ").format(attrs.get(bstack1lll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩၿ")), attrs.get(bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨႀ"), bstack1lll1l_opy_ (u"ࠫࠬႁ"))) if attrs.get(bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪႂ"), []) else attrs.get(bstack1lll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ႃ")),
                bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧႄ"): attrs.get(bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ႅ"), []),
                bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ႆ"): current_time(),
                bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪႇ"): bstack1lll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬႈ"),
                bstack1lll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪႉ"): attrs.get(bstack1lll1l_opy_ (u"࠭ࡤࡰࡥࠪႊ"), bstack1lll1l_opy_ (u"ࠧࠨႋ"))
            }
            if attrs.get(bstack1lll1l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩႌ"), bstack1lll1l_opy_ (u"ႍࠩࠪ")) != bstack1lll1l_opy_ (u"ࠪࠫႎ"):
                bstack1111l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬႏ")] = attrs.get(bstack1lll1l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭႐"))
            if not self.bstack11111lllll_opy_:
                self._111111l11l_opy_[self._11111l111l_opy_()][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ႑")].add_step(bstack1111l1l1l1_opy_)
                threading.current_thread().current_step_uuid = bstack1111l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡪࡦࠪ႒")]
            self.bstack11111lllll_opy_.append(bstack1111l1l1l1_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llllll11ll_opy_()
        self._1llllllllll_opy_(messages)
        current_test_id = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ႓"), None)
        bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ႔"), None)
        bstack11111l11ll_opy_ = bstack111111l1l1_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ႕")), bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ႖"))
        bstack1111111l11_opy_ = attrs.get(bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭႗"))
        if bstack11111l11ll_opy_ != bstack1lll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ႘") and not attrs.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ႙")) and self._1lllllll11l_opy_:
            bstack1111111l11_opy_ = self._1lllllll11l_opy_
        bstack1111l1ll11_opy_ = Result(result=bstack11111l11ll_opy_, exception=bstack1111111l11_opy_, bstack1111l1ll1l_opy_=[bstack1111111l11_opy_])
        if attrs.get(bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ႚ"), bstack1lll1l_opy_ (u"ࠩࠪႛ")).lower() in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩႜ"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ႝ")]:
            bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ႞"), None)
            if bstack1llllll1l1l_opy_:
                bstack1111l1l111_opy_ = bstack1llllll1l1l_opy_ + bstack1lll1l_opy_ (u"ࠨ࠭ࠣ႟") + attrs.get(bstack1lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬႠ"), bstack1lll1l_opy_ (u"ࠨࠩႡ")).lower()
                self._111111l11l_opy_[bstack1111l1l111_opy_][bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႢ")].stop(time=current_time(), duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨႣ"), bstack1lll1l_opy_ (u"ࠫ࠵࠭Ⴄ"))), result=bstack1111l1ll11_opy_)
                TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧႥ"), self._111111l11l_opy_[bstack1111l1l111_opy_][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩႦ")])
        else:
            bstack1llllll1l1l_opy_ = current_test_id if current_test_id else bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩႧ"), None)
            if bstack1llllll1l1l_opy_ and len(self.bstack11111lllll_opy_) == 1:
                current_step_uuid = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬႨ"), None)
                self._111111l11l_opy_[bstack1llllll1l1l_opy_][bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႩ")].bstack1111ll1ll1_opy_(current_step_uuid, duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨႪ"), bstack1lll1l_opy_ (u"ࠫ࠵࠭Ⴋ"))), result=bstack1111l1ll11_opy_)
            else:
                self.bstack11111l1l11_opy_(attrs)
            self.bstack11111lllll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1lll1l_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪႬ"), bstack1lll1l_opy_ (u"࠭࡮ࡰࠩႭ")) == bstack1lll1l_opy_ (u"ࠧࡺࡧࡶࠫႮ"):
                return
            self.messages.push(message)
            logs = []
            if bstack111lllll1_opy_.bstack1111l111ll_opy_():
                logs.append({
                    bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫႯ"): current_time(),
                    bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႰ"): message.get(bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႱ")),
                    bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪႲ"): message.get(bstack1lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫႳ")),
                    **bstack111lllll1_opy_.bstack1111l111ll_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack11ll1l1l11_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack11111ll1ll_opy_()
    def bstack11111l1l11_opy_(self, bstack1111111lll_opy_):
        if not bstack111lllll1_opy_.bstack1111l111ll_opy_():
            return
        kwname = bstack1lll1l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬႴ").format(bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧႵ")), bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭Ⴖ"), bstack1lll1l_opy_ (u"ࠩࠪႷ"))) if bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨႸ"), []) else bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫႹ"))
        error_message = bstack1lll1l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦႺ").format(kwname, bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ⴛ")), str(bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႼ"))))
        bstack11111111ll_opy_ = bstack1lll1l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢႽ").format(kwname, bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩႾ")))
        bstack1llllllll11_opy_ = error_message if bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႿ")) else bstack11111111ll_opy_
        bstack1lllllll1ll_opy_ = {
            bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧჀ"): self.bstack11111lllll_opy_[-1].get(bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩჁ"), current_time()),
            bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧჂ"): bstack1llllllll11_opy_,
            bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ⴣ"): bstack1lll1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧჄ") if bstack1111111lll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩჅ")) == bstack1lll1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ჆") else bstack1lll1l_opy_ (u"ࠫࡎࡔࡆࡐࠩჇ"),
            **bstack111lllll1_opy_.bstack1111l111ll_opy_()
        }
        TestHubHandler.bstack11ll1l1l11_opy_([bstack1lllllll1ll_opy_])
    def _11111l111l_opy_(self):
        for bstack11111ll11l_opy_ in reversed(self._111111l11l_opy_):
            bstack1lllllll111_opy_ = bstack11111ll11l_opy_
            data = self._111111l11l_opy_[bstack11111ll11l_opy_][bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ჈")]
            if isinstance(data, bstack1111ll1l11_opy_):
                if not bstack1lll1l_opy_ (u"࠭ࡅࡂࡅࡋࠫ჉") in data.bstack1111111ll1_opy_():
                    return bstack1lllllll111_opy_
            else:
                return bstack1lllllll111_opy_
    def _1llllllllll_opy_(self, messages):
        try:
            bstack111111111l_opy_ = BuiltIn().get_variable_value(bstack1lll1l_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨ჊")) in (bstack1llllll1ll1_opy_.DEBUG, bstack1llllll1ll1_opy_.TRACE)
            for message, bstack11111ll1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ჋"))
                level = message.get(bstack1lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ჌"))
                if level == bstack1llllll1ll1_opy_.FAIL:
                    self._1lllllll11l_opy_ = name or self._1lllllll11l_opy_
                    self._111111ll11_opy_ = bstack11111ll1l1_opy_.get(bstack1lll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦჍ")) if bstack111111111l_opy_ and bstack11111ll1l1_opy_ else self._111111ll11_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1111l11111_opy_: bstack11111llll1_opy_, bstack11111l1111_opy_=False):
        if event == bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭჎"):
            bstack1111l11111_opy_.set(hooks=self.store[bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ჏")])
        if event == bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧა"):
            event = bstack1lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩბ")
        if bstack11111l1111_opy_:
            bstack1111111l1l_opy_ = {
                bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬგ"): event,
                bstack1111l11111_opy_.bstack11111ll111_opy_(): bstack1111l11111_opy_.bstack1lllllll1l1_opy_(event)
            }
            with self._lock:
                self.bstack1llllll11l1_opy_.append(bstack1111111l1l_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1111l11111_opy_)
class bstack111111l111_opy_:
    def __init__(self):
        self._111111ll1l_opy_ = []
    def bstack11111l1lll_opy_(self):
        self._111111ll1l_opy_.append([])
    def bstack1llllll11ll_opy_(self):
        return self._111111ll1l_opy_.pop() if self._111111ll1l_opy_ else list()
    def push(self, message):
        self._111111ll1l_opy_[-1].append(message) if self._111111ll1l_opy_ else self._111111ll1l_opy_.append([message])
class bstack1llllll1ll1_opy_:
    FAIL = bstack1lll1l_opy_ (u"ࠩࡉࡅࡎࡒࠧდ")
    ERROR = bstack1lll1l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩე")
    WARNING = bstack1lll1l_opy_ (u"ࠫ࡜ࡇࡒࡏࠩვ")
    bstack1111111111_opy_ = bstack1lll1l_opy_ (u"ࠬࡏࡎࡇࡑࠪზ")
    DEBUG = bstack1lll1l_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬთ")
    TRACE = bstack1lll1l_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ი")
    bstack11111l11l1_opy_ = [FAIL, ERROR]
def bstack11111l1l1l_opy_(bstack11111111l1_opy_):
    if not bstack11111111l1_opy_:
        return None
    if bstack11111111l1_opy_.get(bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫკ"), None):
        return getattr(bstack11111111l1_opy_[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬლ")], bstack1lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨმ"), None)
    return bstack11111111l1_opy_.get(bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩნ"), None)
def bstack1llllllll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫო"), bstack1lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨპ")]:
        return
    if hook_type.lower() == bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ჟ"):
        if current_test_uuid is None:
            return bstack1lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬრ")
        else:
            return bstack1lll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧს")
    elif hook_type.lower() == bstack1lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬტ"):
        if current_test_uuid is None:
            return bstack1lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧუ")
        else:
            return bstack1lll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩფ")