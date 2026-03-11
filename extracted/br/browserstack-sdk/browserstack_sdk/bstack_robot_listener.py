# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1llllllll11_opy_ import RobotHandler
from bstack_utils.capture import bstack111111ll1l_opy_
from bstack_utils.test_data import bstack1lllll1ll11_opy_, bstack11111l11ll_opy_, TestData
from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack11llll11l_opy_, current_time, Result, \
    error_handler, bstack1lllllll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ၿ"): [],
        bstack1ll111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩႀ"): [],
        bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨႁ"): []
    }
    bstack1lllll11lll_opy_ = []
    bstack1111111lll_opy_ = []
    @staticmethod
    def bstack111111ll11_opy_(log):
        if not ((isinstance(log[bstack1ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ႂ")], list) or (isinstance(log[bstack1ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႃ")], dict)) and len(log[bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႄ")])>0) or (isinstance(log[bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႅ")], str) and log[bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႆ")].strip())):
            return
        active = bstack11l1ll1111_opy_.bstack11111l1111_opy_()
        log = {
            bstack1ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႇ"): log[bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪႈ")],
            bstack1ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨႉ"): bstack1lllllll1ll_opy_().isoformat() + bstack1ll111_opy_ (u"࡚࠭ࠨႊ"),
            bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႋ"): log[bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႌ")],
        }
        if active:
            if active[bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ႍࠧ")] == bstack1ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨႎ"):
                log[bstack1ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫႏ")] = active[bstack1ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ႐")]
            elif active[bstack1ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫ႑")] == bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࠬ႒"):
                log[bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ႓")] = active[bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ႔")]
        TestHubHandler.bstack11lll1l1_opy_([log])
    def __init__(self):
        self.messages = bstack1llll1llll1_opy_()
        self._1llll1lll11_opy_ = None
        self._1lllll1ll1l_opy_ = None
        self._111111l111_opy_ = OrderedDict()
        self.bstack11111ll1l1_opy_ = bstack111111ll1l_opy_(self.bstack111111ll11_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llllll1l11_opy_()
        if not self._111111l111_opy_.get(attrs.get(bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭႕")), None):
            self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠫ࡮ࡪࠧ႖"))] = {}
        bstack1llllllll1l_opy_ = TestData(
                bstack1lllllll11l_opy_=attrs.get(bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨ႗")),
                name=name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs[bstack1ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭႘")], start=os.getcwd()) if attrs.get(bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ႙")) != bstack1ll111_opy_ (u"ࠨࠩႚ") else bstack1ll111_opy_ (u"ࠩࠪႛ"),
                framework=bstack1ll111_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩႜ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll111_opy_ (u"ࠫ࡮ࡪࠧႝ"), None)
        self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨ႞"))][bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ႟")] = bstack1llllllll1l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llllllllll_opy_()
        self._1lllll1l111_opy_(messages)
        with self._lock:
            for bstack1lllll1111l_opy_ in self.bstack1lllll11lll_opy_:
                bstack1lllll1111l_opy_[bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩႠ")][bstack1ll111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧႡ")].extend(self.store[bstack1ll111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨႢ")])
                TestHubHandler.bstack111l1lll11_opy_(bstack1lllll1111l_opy_)
            self.bstack1lllll11lll_opy_ = []
            self.store[bstack1ll111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩႣ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11111ll1l1_opy_.start()
        if not self._111111l111_opy_.get(attrs.get(bstack1ll111_opy_ (u"ࠫ࡮ࡪࠧႤ")), None):
            self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨႥ"))] = {}
        driver = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬႦ"), None)
        test_data = TestData(
            bstack1lllllll11l_opy_=attrs.get(bstack1ll111_opy_ (u"ࠧࡪࡦࠪႧ")),
            name=name,
            started_at=current_time(),
            file_path=os.path.relpath(attrs[bstack1ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨႨ")], start=os.getcwd()),
            scope=RobotHandler.bstack111111l1l1_opy_(attrs.get(bstack1ll111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩႩ"), None)),
            framework=bstack1ll111_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩႪ"),
            tags=attrs[bstack1ll111_opy_ (u"ࠫࡹࡧࡧࡴࠩႫ")],
            hooks=self.store[bstack1ll111_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫႬ")],
            integrations=TestHubHandler.bstack11111l111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll111_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣႭ").format(bstack1ll111_opy_ (u"ࠢࠡࠤႮ").join(attrs[bstack1ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ⴏ")]), name) if attrs[bstack1ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧႰ")] else name
        )
        self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭Ⴑ"))][bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧႲ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1lllll1l1l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨႳ"), None)
        self.send_run_event(bstack1ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧႴ"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11111ll1l1_opy_.reset()
        bstack1111111111_opy_ = bstack1lllll11111_opy_.get(attrs.get(bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧႵ")), bstack1ll111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩႶ"))
        self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬႷ"))][bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴘ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩႹ"), bstack1ll111_opy_ (u"ࠬ࠶ࠧႺ"))), result=Result(result=bstack1111111111_opy_, exception=attrs.get(bstack1ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႻ")), bstack11111ll1ll_opy_=[attrs.get(bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႼ"))]))
        self.send_run_event(bstack1ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪႽ"), self._111111l111_opy_[attrs.get(bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬႾ"))][bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴟ")], True)
        with self._lock:
            self.store[bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨჀ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llllll1l11_opy_()
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧჁ"), None)
        bstack1111111l11_opy_ = current_test_id if bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨჂ"), None) else bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪჃ"), None)
        if attrs.get(bstack1ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ⴤ"), bstack1ll111_opy_ (u"ࠩࠪჅ")).lower() in [bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ჆"), bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭Ⴧ")]:
            hook_type = bstack1lllll1l11l_opy_(attrs.get(bstack1ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪ჈")), bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ჉"), None))
            hook_name = bstack1ll111_opy_ (u"ࠧࡼࡿࠪ჊").format(attrs.get(bstack1ll111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ჋"), bstack1ll111_opy_ (u"ࠩࠪ჌")))
            if hook_type in [bstack1ll111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧჍ"), bstack1ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ჎")]:
                hook_name = bstack1ll111_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭჏").format(bstack1lllll11ll1_opy_.get(hook_type), attrs.get(bstack1ll111_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ა"), bstack1ll111_opy_ (u"ࠧࠨბ")))
            bstack1lllll1lll1_opy_ = bstack11111l11ll_opy_(
                bstack1lllllll11l_opy_=bstack1111111l11_opy_ + bstack1ll111_opy_ (u"ࠨ࠯ࠪგ") + attrs.get(bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧდ"), bstack1ll111_opy_ (u"ࠪࠫე")).lower(),
                name=hook_name,
                started_at=current_time(),
                file_path=os.path.relpath(attrs.get(bstack1ll111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫვ")), start=os.getcwd()),
                framework=bstack1ll111_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫზ"),
                tags=attrs[bstack1ll111_opy_ (u"࠭ࡴࡢࡩࡶࠫთ")],
                scope=RobotHandler.bstack111111l1l1_opy_(attrs.get(bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧი"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lllll1lll1_opy_.bstack1lllll1l1l1_opy_()
            threading.current_thread().current_hook_id = bstack1111111l11_opy_ + bstack1ll111_opy_ (u"ࠨ࠯ࠪკ") + attrs.get(bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧლ"), bstack1ll111_opy_ (u"ࠪࠫმ")).lower()
            with self._lock:
                self.store[bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨნ")] = [bstack1lllll1lll1_opy_.bstack1lllll1l1l1_opy_()]
                if bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩო"), None):
                    self.store[bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪპ")].append(bstack1lllll1lll1_opy_.bstack1lllll1l1l1_opy_())
                else:
                    self.store[bstack1ll111_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ჟ")].append(bstack1lllll1lll1_opy_.bstack1lllll1l1l1_opy_())
            if bstack1111111l11_opy_:
                self._111111l111_opy_[bstack1111111l11_opy_ + bstack1ll111_opy_ (u"ࠨ࠯ࠪრ") + attrs.get(bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧს"), bstack1ll111_opy_ (u"ࠪࠫტ")).lower()] = { bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧუ"): bstack1lllll1lll1_opy_ }
            TestHubHandler.send_run_event(bstack1ll111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ფ"), bstack1lllll1lll1_opy_)
        else:
            bstack11111l1lll_opy_ = {
                bstack1ll111_opy_ (u"࠭ࡩࡥࠩქ"): uuid4().__str__(),
                bstack1ll111_opy_ (u"ࠧࡵࡧࡻࡸࠬღ"): bstack1ll111_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧყ").format(attrs.get(bstack1ll111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩშ")), attrs.get(bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨჩ"), bstack1ll111_opy_ (u"ࠫࠬც"))) if attrs.get(bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪძ"), []) else attrs.get(bstack1ll111_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭წ")),
                bstack1ll111_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧჭ"): attrs.get(bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ხ"), []),
                bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ჯ"): current_time(),
                bstack1ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪჰ"): bstack1ll111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬჱ"),
                bstack1ll111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪჲ"): attrs.get(bstack1ll111_opy_ (u"࠭ࡤࡰࡥࠪჳ"), bstack1ll111_opy_ (u"ࠧࠨჴ"))
            }
            if attrs.get(bstack1ll111_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩჵ"), bstack1ll111_opy_ (u"ࠩࠪჶ")) != bstack1ll111_opy_ (u"ࠪࠫჷ"):
                bstack11111l1lll_opy_[bstack1ll111_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬჸ")] = attrs.get(bstack1ll111_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ჹ"))
            if not self.bstack1111111lll_opy_:
                self._111111l111_opy_[self._1llllll1ll1_opy_()][bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩჺ")].add_step(bstack11111l1lll_opy_)
                threading.current_thread().current_step_uuid = bstack11111l1lll_opy_[bstack1ll111_opy_ (u"ࠧࡪࡦࠪ჻")]
            self.bstack1111111lll_opy_.append(bstack11111l1lll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llllllllll_opy_()
        self._1lllll1l111_opy_(messages)
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪჼ"), None)
        bstack1111111l11_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬჽ"), None)
        bstack1llllll111l_opy_ = bstack1lllll11111_opy_.get(attrs.get(bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪჾ")), bstack1ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬჿ"))
        bstack1llllll11ll_opy_ = attrs.get(bstack1ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄀ"))
        if bstack1llllll111l_opy_ != bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᄁ") and not attrs.get(bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᄂ")) and self._1llll1lll11_opy_:
            bstack1llllll11ll_opy_ = self._1llll1lll11_opy_
        bstack111111llll_opy_ = Result(result=bstack1llllll111l_opy_, exception=bstack1llllll11ll_opy_, bstack11111ll1ll_opy_=[bstack1llllll11ll_opy_])
        if attrs.get(bstack1ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᄃ"), bstack1ll111_opy_ (u"ࠩࠪᄄ")).lower() in [bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᄅ"), bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᄆ")]:
            bstack1111111l11_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᄇ"), None)
            if bstack1111111l11_opy_:
                bstack11111l11l1_opy_ = bstack1111111l11_opy_ + bstack1ll111_opy_ (u"ࠨ࠭ࠣᄈ") + attrs.get(bstack1ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬᄉ"), bstack1ll111_opy_ (u"ࠨࠩᄊ")).lower()
                self._111111l111_opy_[bstack11111l11l1_opy_][bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄋ")].stop(time=current_time(), duration=int(attrs.get(bstack1ll111_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨᄌ"), bstack1ll111_opy_ (u"ࠫ࠵࠭ᄍ"))), result=bstack111111llll_opy_)
                TestHubHandler.send_run_event(bstack1ll111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᄎ"), self._111111l111_opy_[bstack11111l11l1_opy_][bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᄏ")])
        else:
            bstack1111111l11_opy_ = current_test_id if current_test_id else bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩᄐ"), None)
            if bstack1111111l11_opy_ and len(self.bstack1111111lll_opy_) == 1:
                current_step_uuid = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬᄑ"), None)
                self._111111l111_opy_[bstack1111111l11_opy_][bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄒ")].bstack11111lllll_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll111_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨᄓ"), bstack1ll111_opy_ (u"ࠫ࠵࠭ᄔ"))), result=bstack111111llll_opy_)
            else:
                self.bstack1llllll1lll_opy_(attrs)
            self.bstack1111111lll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll111_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪᄕ"), bstack1ll111_opy_ (u"࠭࡮ࡰࠩᄖ")) == bstack1ll111_opy_ (u"ࠧࡺࡧࡶࠫᄗ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1ll1111_opy_.bstack11111l1111_opy_():
                logs.append({
                    bstack1ll111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᄘ"): current_time(),
                    bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᄙ"): message.get(bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄚ")),
                    bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᄛ"): message.get(bstack1ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᄜ")),
                    **bstack11l1ll1111_opy_.bstack11111l1111_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack11lll1l1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lllll111ll_opy_()
    def bstack1llllll1lll_opy_(self, bstack1llllll11l1_opy_):
        if not bstack11l1ll1111_opy_.bstack11111l1111_opy_():
            return
        kwname = bstack1ll111_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬᄝ").format(bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᄞ")), bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᄟ"), bstack1ll111_opy_ (u"ࠩࠪᄠ"))) if bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᄡ"), []) else bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᄢ"))
        error_message = bstack1ll111_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦᄣ").format(kwname, bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᄤ")), str(bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᄥ"))))
        bstack1111111l1l_opy_ = bstack1ll111_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢᄦ").format(kwname, bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᄧ")))
        bstack111111111l_opy_ = error_message if bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄨ")) else bstack1111111l1l_opy_
        bstack1lllllll1l1_opy_ = {
            bstack1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᄩ"): self.bstack1111111lll_opy_[-1].get(bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᄪ"), current_time()),
            bstack1ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄫ"): bstack111111111l_opy_,
            bstack1ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᄬ"): bstack1ll111_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧᄭ") if bstack1llllll11l1_opy_.get(bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᄮ")) == bstack1ll111_opy_ (u"ࠪࡊࡆࡏࡌࠨᄯ") else bstack1ll111_opy_ (u"ࠫࡎࡔࡆࡐࠩᄰ"),
            **bstack11l1ll1111_opy_.bstack11111l1111_opy_()
        }
        TestHubHandler.bstack11lll1l1_opy_([bstack1lllllll1l1_opy_])
    def _1llllll1ll1_opy_(self):
        for bstack1lllllll11l_opy_ in reversed(self._111111l111_opy_):
            bstack1llll1lllll_opy_ = bstack1lllllll11l_opy_
            data = self._111111l111_opy_[bstack1lllllll11l_opy_][bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄱ")]
            if isinstance(data, bstack11111l11ll_opy_):
                if not bstack1ll111_opy_ (u"࠭ࡅࡂࡅࡋࠫᄲ") in data.bstack1lllll1l1ll_opy_():
                    return bstack1llll1lllll_opy_
            else:
                return bstack1llll1lllll_opy_
    def _1lllll1l111_opy_(self, messages):
        try:
            bstack1lllllll111_opy_ = BuiltIn().get_variable_value(bstack1ll111_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨᄳ")) in (bstack1llllll1111_opy_.DEBUG, bstack1llllll1111_opy_.TRACE)
            for message, bstack11111111l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᄴ"))
                level = message.get(bstack1ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᄵ"))
                if level == bstack1llllll1111_opy_.FAIL:
                    self._1llll1lll11_opy_ = name or self._1llll1lll11_opy_
                    self._1lllll1ll1l_opy_ = bstack11111111l1_opy_.get(bstack1ll111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᄶ")) if bstack1lllllll111_opy_ and bstack11111111l1_opy_ else self._1lllll1ll1l_opy_
        except:
            pass
    @classmethod
    def send_run_event(self, event: str, bstack1lllll111l1_opy_: bstack1lllll1ll11_opy_, bstack11111111ll_opy_=False):
        if event == bstack1ll111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᄷ"):
            bstack1lllll111l1_opy_.set(hooks=self.store[bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩᄸ")])
        if event == bstack1ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᄹ"):
            event = bstack1ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᄺ")
        if bstack11111111ll_opy_:
            bstack1lllll1llll_opy_ = {
                bstack1ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᄻ"): event,
                bstack1lllll111l1_opy_.bstack1111111ll1_opy_(): bstack1lllll111l1_opy_.bstack111111l11l_opy_(event)
            }
            with self._lock:
                self.bstack1lllll11lll_opy_.append(bstack1lllll1llll_opy_)
        else:
            TestHubHandler.send_run_event(event, bstack1lllll111l1_opy_)
class bstack1llll1llll1_opy_:
    def __init__(self):
        self._1lllll11l11_opy_ = []
    def bstack1llllll1l11_opy_(self):
        self._1lllll11l11_opy_.append([])
    def bstack1llllllllll_opy_(self):
        return self._1lllll11l11_opy_.pop() if self._1lllll11l11_opy_ else list()
    def push(self, message):
        self._1lllll11l11_opy_[-1].append(message) if self._1lllll11l11_opy_ else self._1lllll11l11_opy_.append([message])
class bstack1llllll1111_opy_:
    FAIL = bstack1ll111_opy_ (u"ࠩࡉࡅࡎࡒࠧᄼ")
    ERROR = bstack1ll111_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩᄽ")
    WARNING = bstack1ll111_opy_ (u"ࠫ࡜ࡇࡒࡏࠩᄾ")
    bstack1llll1lll1l_opy_ = bstack1ll111_opy_ (u"ࠬࡏࡎࡇࡑࠪᄿ")
    DEBUG = bstack1ll111_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬᅀ")
    TRACE = bstack1ll111_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ᅁ")
    bstack1llllll1l1l_opy_ = [FAIL, ERROR]
def bstack1lllllllll1_opy_(bstack1lllll11l1l_opy_):
    if not bstack1lllll11l1l_opy_:
        return None
    if bstack1lllll11l1l_opy_.get(bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅂ"), None):
        return getattr(bstack1lllll11l1l_opy_[bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᅃ")], bstack1ll111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᅄ"), None)
    return bstack1lllll11l1l_opy_.get(bstack1ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩᅅ"), None)
def bstack1lllll1l11l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᅆ"), bstack1ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᅇ")]:
        return
    if hook_type.lower() == bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᅈ"):
        if current_test_uuid is None:
            return bstack1ll111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᅉ")
        else:
            return bstack1ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᅊ")
    elif hook_type.lower() == bstack1ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᅋ"):
        if current_test_uuid is None:
            return bstack1ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᅌ")
        else:
            return bstack1ll111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᅍ")