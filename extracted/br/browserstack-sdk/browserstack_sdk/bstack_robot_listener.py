# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111l11ll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1111ll1l1l_opy_
from bstack_utils.bstack1111llllll_opy_ import bstack111111llll_opy_, bstack1111ll1lll_opy_, bstack1111ll11ll_opy_
from bstack_utils.bstack1111l1lll1_opy_ import bstack1l1l11llll_opy_
from bstack_utils.bstack1111lll1l1_opy_ import bstack11lll1111l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1ll1ll1_opy_, bstack1lll11lll1_opy_, Result, \
    error_handler, bstack11111ll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ࿫"): [],
        bstack11lllll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ࿬"): [],
        bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿭"): []
    }
    bstack1llllllll1l_opy_ = []
    bstack11111ll1l1_opy_ = []
    @staticmethod
    def bstack1111ll1l11_opy_(log):
        if not ((isinstance(log[bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿮")], list) or (isinstance(log[bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿯")], dict)) and len(log[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿰")])>0) or (isinstance(log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿱")], str) and log[bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿲")].strip())):
            return
        active = bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_()
        log = {
            bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿳"): log[bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿴")],
            bstack11lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ࿵"): bstack11111ll1ll_opy_().isoformat() + bstack11lllll_opy_ (u"ࠬࡠࠧ࿶"),
            bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿷"): log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿸")],
        }
        if active:
            if active[bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿹")] == bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ࿺"):
                log[bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ࿻")] = active[bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ࿼")]
            elif active[bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿽")] == bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࠫ࿾"):
                log[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ࿿")] = active[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨက")]
        bstack11lll1111l_opy_.bstack1ll111l1ll_opy_([log])
    def __init__(self):
        self.messages = bstack111111l111_opy_()
        self._1lllllllll1_opy_ = None
        self._1111l111l1_opy_ = None
        self._111111l1l1_opy_ = OrderedDict()
        self.bstack1111llll1l_opy_ = bstack1111ll1l1l_opy_(self.bstack1111ll1l11_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1llllllll11_opy_()
        if not self._111111l1l1_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬခ")), None):
            self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭ဂ"))] = {}
        bstack1111l11l11_opy_ = bstack1111ll11ll_opy_(
                bstack11111lll11_opy_=attrs.get(bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧဃ")),
                name=name,
                started_at=bstack1lll11lll1_opy_(),
                file_path=os.path.relpath(attrs[bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬင")], start=os.getcwd()) if attrs.get(bstack11lllll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭စ")) != bstack11lllll_opy_ (u"ࠧࠨဆ") else bstack11lllll_opy_ (u"ࠨࠩဇ"),
                framework=bstack11lllll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨဈ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭ဉ"), None)
        self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧည"))][bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဋ")] = bstack1111l11l11_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11111111ll_opy_()
        self._1111111111_opy_(messages)
        with self._lock:
            for bstack11111lll1l_opy_ in self.bstack1llllllll1l_opy_:
                bstack11111lll1l_opy_[bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨဌ")][bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ဍ")].extend(self.store[bstack11lllll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧဎ")])
                bstack11lll1111l_opy_.bstack11ll1llll1_opy_(bstack11111lll1l_opy_)
            self.bstack1llllllll1l_opy_ = []
            self.store[bstack11lllll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨဏ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111llll1l_opy_.start()
        if not self._111111l1l1_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭တ")), None):
            self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧထ"))] = {}
        driver = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫဒ"), None)
        bstack1111llllll_opy_ = bstack1111ll11ll_opy_(
            bstack11111lll11_opy_=attrs.get(bstack11lllll_opy_ (u"࠭ࡩࡥࠩဓ")),
            name=name,
            started_at=bstack1lll11lll1_opy_(),
            file_path=os.path.relpath(attrs[bstack11lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧန")], start=os.getcwd()),
            scope=RobotHandler.bstack1111111lll_opy_(attrs.get(bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨပ"), None)),
            framework=bstack11lllll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨဖ"),
            tags=attrs[bstack11lllll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨဗ")],
            hooks=self.store[bstack11lllll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪဘ")],
            bstack1111lllll1_opy_=bstack11lll1111l_opy_.bstack1111lll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11lllll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢမ").format(bstack11lllll_opy_ (u"ࠨࠠࠣယ").join(attrs[bstack11lllll_opy_ (u"ࠧࡵࡣࡪࡷࠬရ")]), name) if attrs[bstack11lllll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭လ")] else name
        )
        self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬဝ"))][bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭သ")] = bstack1111llllll_opy_
        threading.current_thread().current_test_uuid = bstack1111llllll_opy_.bstack1111111ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧဟ"), None)
        self.bstack111l111111_opy_(bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ဠ"), bstack1111llllll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111llll1l_opy_.reset()
        bstack1111l1l111_opy_ = bstack11111l1l1l_opy_.get(attrs.get(bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭အ")), bstack11lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨဢ"))
        self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫဣ"))][bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဤ")].stop(time=bstack1lll11lll1_opy_(), duration=int(attrs.get(bstack11lllll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨဥ"), bstack11lllll_opy_ (u"ࠫ࠵࠭ဦ"))), result=Result(result=bstack1111l1l111_opy_, exception=attrs.get(bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ဧ")), bstack1111ll11l1_opy_=[attrs.get(bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဨ"))]))
        self.bstack111l111111_opy_(bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩဩ"), self._111111l1l1_opy_[attrs.get(bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫဪ"))][bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬါ")], True)
        with self._lock:
            self.store[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧာ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1llllllll11_opy_()
        current_test_id = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ိ"), None)
        bstack11111llll1_opy_ = current_test_id if bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧီ"), None) else bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩု"), None)
        if attrs.get(bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬူ"), bstack11lllll_opy_ (u"ࠨࠩေ")).lower() in [bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨဲ"), bstack11lllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬဳ")]:
            hook_type = bstack11111l1l11_opy_(attrs.get(bstack11lllll_opy_ (u"ࠫࡹࡿࡰࡦࠩဴ")), bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩဵ"), None))
            hook_name = bstack11lllll_opy_ (u"࠭ࡻࡾࠩံ").format(attrs.get(bstack11lllll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫့ࠧ"), bstack11lllll_opy_ (u"ࠨࠩး")))
            if hook_type in [bstack11lllll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ္࠭"), bstack11lllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ်࠭")]:
                hook_name = bstack11lllll_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬျ").format(bstack111111l11l_opy_.get(hook_type), attrs.get(bstack11lllll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬြ"), bstack11lllll_opy_ (u"࠭ࠧွ")))
            bstack1111l11lll_opy_ = bstack1111ll1lll_opy_(
                bstack11111lll11_opy_=bstack11111llll1_opy_ + bstack11lllll_opy_ (u"ࠧ࠮ࠩှ") + attrs.get(bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ဿ"), bstack11lllll_opy_ (u"ࠩࠪ၀")).lower(),
                name=hook_name,
                started_at=bstack1lll11lll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11lllll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ၁")), start=os.getcwd()),
                framework=bstack11lllll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ၂"),
                tags=attrs[bstack11lllll_opy_ (u"ࠬࡺࡡࡨࡵࠪ၃")],
                scope=RobotHandler.bstack1111111lll_opy_(attrs.get(bstack11lllll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭၄"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1111l11lll_opy_.bstack1111111ll1_opy_()
            threading.current_thread().current_hook_id = bstack11111llll1_opy_ + bstack11lllll_opy_ (u"ࠧ࠮ࠩ၅") + attrs.get(bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭၆"), bstack11lllll_opy_ (u"ࠩࠪ၇")).lower()
            with self._lock:
                self.store[bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ၈")] = [bstack1111l11lll_opy_.bstack1111111ll1_opy_()]
                if bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ၉"), None):
                    self.store[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ၊")].append(bstack1111l11lll_opy_.bstack1111111ll1_opy_())
                else:
                    self.store[bstack11lllll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ။")].append(bstack1111l11lll_opy_.bstack1111111ll1_opy_())
            if bstack11111llll1_opy_:
                self._111111l1l1_opy_[bstack11111llll1_opy_ + bstack11lllll_opy_ (u"ࠧ࠮ࠩ၌") + attrs.get(bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭၍"), bstack11lllll_opy_ (u"ࠩࠪ၎")).lower()] = { bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭၏"): bstack1111l11lll_opy_ }
            bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬၐ"), bstack1111l11lll_opy_)
        else:
            bstack111l111l11_opy_ = {
                bstack11lllll_opy_ (u"ࠬ࡯ࡤࠨၑ"): uuid4().__str__(),
                bstack11lllll_opy_ (u"࠭ࡴࡦࡺࡷࠫၒ"): bstack11lllll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ၓ").format(attrs.get(bstack11lllll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨၔ")), attrs.get(bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧၕ"), bstack11lllll_opy_ (u"ࠪࠫၖ"))) if attrs.get(bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩၗ"), []) else attrs.get(bstack11lllll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬၘ")),
                bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ၙ"): attrs.get(bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬၚ"), []),
                bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬၛ"): bstack1lll11lll1_opy_(),
                bstack11lllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩၜ"): bstack11lllll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫၝ"),
                bstack11lllll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩၞ"): attrs.get(bstack11lllll_opy_ (u"ࠬࡪ࡯ࡤࠩၟ"), bstack11lllll_opy_ (u"࠭ࠧၠ"))
            }
            if attrs.get(bstack11lllll_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨၡ"), bstack11lllll_opy_ (u"ࠨࠩၢ")) != bstack11lllll_opy_ (u"ࠩࠪၣ"):
                bstack111l111l11_opy_[bstack11lllll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫၤ")] = attrs.get(bstack11lllll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬၥ"))
            if not self.bstack11111ll1l1_opy_:
                self._111111l1l1_opy_[self._1lllllll1ll_opy_()][bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၦ")].add_step(bstack111l111l11_opy_)
                threading.current_thread().current_step_uuid = bstack111l111l11_opy_[bstack11lllll_opy_ (u"࠭ࡩࡥࠩၧ")]
            self.bstack11111ll1l1_opy_.append(bstack111l111l11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11111111ll_opy_()
        self._1111111111_opy_(messages)
        current_test_id = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩၨ"), None)
        bstack11111llll1_opy_ = current_test_id if current_test_id else bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫၩ"), None)
        bstack11111ll11l_opy_ = bstack11111l1l1l_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩၪ")), bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫၫ"))
        bstack11111l1ll1_opy_ = attrs.get(bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬၬ"))
        if bstack11111ll11l_opy_ != bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ၭ") and not attrs.get(bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧၮ")) and self._1lllllllll1_opy_:
            bstack11111l1ll1_opy_ = self._1lllllllll1_opy_
        bstack1111l1ll11_opy_ = Result(result=bstack11111ll11l_opy_, exception=bstack11111l1ll1_opy_, bstack1111ll11l1_opy_=[bstack11111l1ll1_opy_])
        if attrs.get(bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬၯ"), bstack11lllll_opy_ (u"ࠨࠩၰ")).lower() in [bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨၱ"), bstack11lllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬၲ")]:
            bstack11111llll1_opy_ = current_test_id if current_test_id else bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧၳ"), None)
            if bstack11111llll1_opy_:
                bstack1111lll11l_opy_ = bstack11111llll1_opy_ + bstack11lllll_opy_ (u"ࠧ࠳ࠢၴ") + attrs.get(bstack11lllll_opy_ (u"࠭ࡴࡺࡲࡨࠫၵ"), bstack11lllll_opy_ (u"ࠧࠨၶ")).lower()
                self._111111l1l1_opy_[bstack1111lll11l_opy_][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫၷ")].stop(time=bstack1lll11lll1_opy_(), duration=int(attrs.get(bstack11lllll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧၸ"), bstack11lllll_opy_ (u"ࠪ࠴ࠬၹ"))), result=bstack1111l1ll11_opy_)
                bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ၺ"), self._111111l1l1_opy_[bstack1111lll11l_opy_][bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၻ")])
        else:
            bstack11111llll1_opy_ = current_test_id if current_test_id else bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨၼ"), None)
            if bstack11111llll1_opy_ and len(self.bstack11111ll1l1_opy_) == 1:
                current_step_uuid = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫၽ"), None)
                self._111111l1l1_opy_[bstack11111llll1_opy_][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫၾ")].bstack1111l1llll_opy_(current_step_uuid, duration=int(attrs.get(bstack11lllll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧၿ"), bstack11lllll_opy_ (u"ࠪ࠴ࠬႀ"))), result=bstack1111l1ll11_opy_)
            else:
                self.bstack1111111l11_opy_(attrs)
            self.bstack11111ll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11lllll_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩႁ"), bstack11lllll_opy_ (u"ࠬࡴ࡯ࠨႂ")) == bstack11lllll_opy_ (u"࠭ࡹࡦࡵࠪႃ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_():
                logs.append({
                    bstack11lllll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪႄ"): bstack1lll11lll1_opy_(),
                    bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႅ"): message.get(bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႆ")),
                    bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႇ"): message.get(bstack11lllll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪႈ")),
                    **bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_()
                })
                if len(logs) > 0:
                    bstack11lll1111l_opy_.bstack1ll111l1ll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11lll1111l_opy_.bstack1111l1l11l_opy_()
    def bstack1111111l11_opy_(self, bstack1llllllllll_opy_):
        if not bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_():
            return
        kwname = bstack11lllll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫႉ").format(bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ႊ")), bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬႋ"), bstack11lllll_opy_ (u"ࠨࠩႌ"))) if bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡹႍࠧ"), []) else bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪႎ"))
        error_message = bstack11lllll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥႏ").format(kwname, bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ႐")), str(bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ႑"))))
        bstack111111111l_opy_ = bstack11lllll_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨ႒").format(kwname, bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ႓")))
        bstack1111l1111l_opy_ = error_message if bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ႔")) else bstack111111111l_opy_
        bstack11111lllll_opy_ = {
            bstack11lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭႕"): self.bstack11111ll1l1_opy_[-1].get(bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ႖"), bstack1lll11lll1_opy_()),
            bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭႗"): bstack1111l1111l_opy_,
            bstack11lllll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ႘"): bstack11lllll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭႙") if bstack1llllllllll_opy_.get(bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨႚ")) == bstack11lllll_opy_ (u"ࠩࡉࡅࡎࡒࠧႛ") else bstack11lllll_opy_ (u"ࠪࡍࡓࡌࡏࠨႜ"),
            **bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_()
        }
        bstack11lll1111l_opy_.bstack1ll111l1ll_opy_([bstack11111lllll_opy_])
    def _1lllllll1ll_opy_(self):
        for bstack11111lll11_opy_ in reversed(self._111111l1l1_opy_):
            bstack1111l11111_opy_ = bstack11111lll11_opy_
            data = self._111111l1l1_opy_[bstack11111lll11_opy_][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧႝ")]
            if isinstance(data, bstack1111ll1lll_opy_):
                if not bstack11lllll_opy_ (u"ࠬࡋࡁࡄࡊࠪ႞") in data.bstack111111l1ll_opy_():
                    return bstack1111l11111_opy_
            else:
                return bstack1111l11111_opy_
    def _1111111111_opy_(self, messages):
        try:
            bstack111111ll1l_opy_ = BuiltIn().get_variable_value(bstack11lllll_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧ႟")) in (bstack111111ll11_opy_.DEBUG, bstack111111ll11_opy_.TRACE)
            for message, bstack11111l1111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႠ"))
                level = message.get(bstack11lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧႡ"))
                if level == bstack111111ll11_opy_.FAIL:
                    self._1lllllllll1_opy_ = name or self._1lllllllll1_opy_
                    self._1111l111l1_opy_ = bstack11111l1111_opy_.get(bstack11lllll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥႢ")) if bstack111111ll1l_opy_ and bstack11111l1111_opy_ else self._1111l111l1_opy_
        except:
            pass
    @classmethod
    def bstack111l111111_opy_(self, event: str, bstack1111111l1l_opy_: bstack111111llll_opy_, bstack11111ll111_opy_=False):
        if event == bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬႣ"):
            bstack1111111l1l_opy_.set(hooks=self.store[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨႤ")])
        if event == bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭Ⴅ"):
            event = bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨႦ")
        if bstack11111ll111_opy_:
            bstack1111l11l1l_opy_ = {
                bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫႧ"): event,
                bstack1111111l1l_opy_.bstack11111111l1_opy_(): bstack1111111l1l_opy_.bstack11111l11ll_opy_(event)
            }
            with self._lock:
                self.bstack1llllllll1l_opy_.append(bstack1111l11l1l_opy_)
        else:
            bstack11lll1111l_opy_.bstack111l111111_opy_(event, bstack1111111l1l_opy_)
class bstack111111l111_opy_:
    def __init__(self):
        self._11111l111l_opy_ = []
    def bstack1llllllll11_opy_(self):
        self._11111l111l_opy_.append([])
    def bstack11111111ll_opy_(self):
        return self._11111l111l_opy_.pop() if self._11111l111l_opy_ else list()
    def push(self, message):
        self._11111l111l_opy_[-1].append(message) if self._11111l111l_opy_ else self._11111l111l_opy_.append([message])
class bstack111111ll11_opy_:
    FAIL = bstack11lllll_opy_ (u"ࠨࡈࡄࡍࡑ࠭Ⴈ")
    ERROR = bstack11lllll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨႩ")
    WARNING = bstack11lllll_opy_ (u"࡛ࠪࡆࡘࡎࠨႪ")
    bstack11111l11l1_opy_ = bstack11lllll_opy_ (u"ࠫࡎࡔࡆࡐࠩႫ")
    DEBUG = bstack11lllll_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫႬ")
    TRACE = bstack11lllll_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬႭ")
    bstack11111l1lll_opy_ = [FAIL, ERROR]
def bstack111111lll1_opy_(bstack1111l111ll_opy_):
    if not bstack1111l111ll_opy_:
        return None
    if bstack1111l111ll_opy_.get(bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႮ"), None):
        return getattr(bstack1111l111ll_opy_[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႯ")], bstack11lllll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧႰ"), None)
    return bstack1111l111ll_opy_.get(bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨႱ"), None)
def bstack11111l1l11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪႲ"), bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧႳ")]:
        return
    if hook_type.lower() == bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬႴ"):
        if current_test_uuid is None:
            return bstack11lllll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫႵ")
        else:
            return bstack11lllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ⴖ")
    elif hook_type.lower() == bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫႷ"):
        if current_test_uuid is None:
            return bstack11lllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭Ⴘ")
        else:
            return bstack11lllll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨႹ")