# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1llllll11ll_opy_ import RobotHandler
from bstack_utils.capture import bstack11111llll1_opy_
from bstack_utils.bstack11111lll1l_opy_ import bstack11111111l1_opy_, bstack1111l1lll1_opy_, bstack1111ll1111_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
from bstack_utils.bstack1111l11lll_opy_ import bstack1ll111l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll11l11_opy_, bstack11l1lll11_opy_, Result, \
    error_handler, bstack111111l11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧဉ"): [],
        bstack11l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪည"): [],
        bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩဋ"): []
    }
    bstack1llllllll1l_opy_ = []
    bstack1111111l1l_opy_ = []
    @staticmethod
    def bstack1111ll111l_opy_(log):
        if not ((isinstance(log[bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဌ")], list) or (isinstance(log[bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဍ")], dict)) and len(log[bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဎ")])>0) or (isinstance(log[bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဏ")], str) and log[bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫတ")].strip())):
            return
        active = bstack11l1ll111l_opy_.bstack11111ll1ll_opy_()
        log = {
            bstack11l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪထ"): log[bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫဒ")],
            bstack11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩဓ"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"࡛ࠧࠩန"),
            bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩပ"): log[bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဖ")],
        }
        if active:
            if active[bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨဗ")] == bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩဘ"):
                log[bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬမ")] = active[bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ယ")]
            elif active[bstack11l11_opy_ (u"ࠧࡵࡻࡳࡩࠬရ")] == bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭လ"):
                log[bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩဝ")] = active[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪသ")]
        bstack1ll111l1_opy_.bstack1l1l1l11l_opy_([log])
    def __init__(self):
        self.messages = bstack1llllll11l1_opy_()
        self._1lllllllll1_opy_ = None
        self._111111l111_opy_ = None
        self._1lllllll11l_opy_ = OrderedDict()
        self.bstack1111l1l1l1_opy_ = bstack11111llll1_opy_(self.bstack1111ll111l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1111111111_opy_()
        if not self._1lllllll11l_opy_.get(attrs.get(bstack11l11_opy_ (u"ࠫ࡮ࡪࠧဟ")), None):
            self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"ࠬ࡯ࡤࠨဠ"))] = {}
        bstack11111l111l_opy_ = bstack1111ll1111_opy_(
                bstack111111llll_opy_=attrs.get(bstack11l11_opy_ (u"࠭ࡩࡥࠩအ")),
                name=name,
                started_at=bstack11l1lll11_opy_(),
                file_path=os.path.relpath(attrs[bstack11l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧဢ")], start=os.getcwd()) if attrs.get(bstack11l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨဣ")) != bstack11l11_opy_ (u"ࠩࠪဤ") else bstack11l11_opy_ (u"ࠪࠫဥ"),
                framework=bstack11l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪဦ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l11_opy_ (u"ࠬ࡯ࡤࠨဧ"), None)
        self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"࠭ࡩࡥࠩဨ"))][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪဩ")] = bstack11111l111l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1llllll1111_opy_()
        self._11111111ll_opy_(messages)
        with self._lock:
            for bstack1llllllll11_opy_ in self.bstack1llllllll1l_opy_:
                bstack1llllllll11_opy_[bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪဪ")][bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨါ")].extend(self.store[bstack11l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩာ")])
                bstack1ll111l1_opy_.bstack11l11lll_opy_(bstack1llllllll11_opy_)
            self.bstack1llllllll1l_opy_ = []
            self.store[bstack11l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪိ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111l1l1l1_opy_.start()
        if not self._1lllllll11l_opy_.get(attrs.get(bstack11l11_opy_ (u"ࠬ࡯ࡤࠨီ")), None):
            self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"࠭ࡩࡥࠩု"))] = {}
        driver = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ူ"), None)
        bstack11111lll1l_opy_ = bstack1111ll1111_opy_(
            bstack111111llll_opy_=attrs.get(bstack11l11_opy_ (u"ࠨ࡫ࡧࠫေ")),
            name=name,
            started_at=bstack11l1lll11_opy_(),
            file_path=os.path.relpath(attrs[bstack11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩဲ")], start=os.getcwd()),
            scope=RobotHandler.bstack11111l11ll_opy_(attrs.get(bstack11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪဳ"), None)),
            framework=bstack11l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪဴ"),
            tags=attrs[bstack11l11_opy_ (u"ࠬࡺࡡࡨࡵࠪဵ")],
            hooks=self.store[bstack11l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬံ")],
            bstack1111l111l1_opy_=bstack1ll111l1_opy_.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l11_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤ့").format(bstack11l11_opy_ (u"ࠣࠢࠥး").join(attrs[bstack11l11_opy_ (u"ࠩࡷࡥ࡬ࡹ္ࠧ")]), name) if attrs[bstack11l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ်")] else name
        )
        self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"ࠫ࡮ࡪࠧျ"))][bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨြ")] = bstack11111lll1l_opy_
        threading.current_thread().current_test_uuid = bstack11111lll1l_opy_.bstack111111ll1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l11_opy_ (u"࠭ࡩࡥࠩွ"), None)
        self.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨှ"), bstack11111lll1l_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111l1l1l1_opy_.reset()
        bstack11111l1l11_opy_ = bstack1111111ll1_opy_.get(attrs.get(bstack11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨဿ")), bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ၀"))
        self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭၁"))][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ၂")].stop(time=bstack11l1lll11_opy_(), duration=int(attrs.get(bstack11l11_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ၃"), bstack11l11_opy_ (u"࠭࠰ࠨ၄"))), result=Result(result=bstack11111l1l11_opy_, exception=attrs.get(bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ၅")), bstack1111ll11l1_opy_=[attrs.get(bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ၆"))]))
        self.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ၇"), self._1lllllll11l_opy_[attrs.get(bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭၈"))][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ၉")], True)
        with self._lock:
            self.store[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ၊")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1111111111_opy_()
        current_test_id = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ။"), None)
        bstack111111111l_opy_ = current_test_id if bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩ၌"), None) else bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ၍"), None)
        if attrs.get(bstack11l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ၎"), bstack11l11_opy_ (u"ࠪࠫ၏")).lower() in [bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪၐ"), bstack11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧၑ")]:
            hook_type = bstack11111l11l1_opy_(attrs.get(bstack11l11_opy_ (u"࠭ࡴࡺࡲࡨࠫၒ")), bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫၓ"), None))
            hook_name = bstack11l11_opy_ (u"ࠨࡽࢀࠫၔ").format(attrs.get(bstack11l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩၕ"), bstack11l11_opy_ (u"ࠪࠫၖ")))
            if hook_type in [bstack11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨၗ"), bstack11l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨၘ")]:
                hook_name = bstack11l11_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧၙ").format(bstack1lllll1llll_opy_.get(hook_type), attrs.get(bstack11l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧၚ"), bstack11l11_opy_ (u"ࠨࠩၛ")))
            bstack11111l1ll1_opy_ = bstack1111l1lll1_opy_(
                bstack111111llll_opy_=bstack111111111l_opy_ + bstack11l11_opy_ (u"ࠩ࠰ࠫၜ") + attrs.get(bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨၝ"), bstack11l11_opy_ (u"ࠫࠬၞ")).lower(),
                name=hook_name,
                started_at=bstack11l1lll11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬၟ")), start=os.getcwd()),
                framework=bstack11l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬၠ"),
                tags=attrs[bstack11l11_opy_ (u"ࠧࡵࡣࡪࡷࠬၡ")],
                scope=RobotHandler.bstack11111l11ll_opy_(attrs.get(bstack11l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨၢ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11111l1ll1_opy_.bstack111111ll1l_opy_()
            threading.current_thread().current_hook_id = bstack111111111l_opy_ + bstack11l11_opy_ (u"ࠩ࠰ࠫၣ") + attrs.get(bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨၤ"), bstack11l11_opy_ (u"ࠫࠬၥ")).lower()
            with self._lock:
                self.store[bstack11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩၦ")] = [bstack11111l1ll1_opy_.bstack111111ll1l_opy_()]
                if bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪၧ"), None):
                    self.store[bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫၨ")].append(bstack11111l1ll1_opy_.bstack111111ll1l_opy_())
                else:
                    self.store[bstack11l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧၩ")].append(bstack11111l1ll1_opy_.bstack111111ll1l_opy_())
            if bstack111111111l_opy_:
                self._1lllllll11l_opy_[bstack111111111l_opy_ + bstack11l11_opy_ (u"ࠩ࠰ࠫၪ") + attrs.get(bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨၫ"), bstack11l11_opy_ (u"ࠫࠬၬ")).lower()] = { bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၭ"): bstack11111l1ll1_opy_ }
            bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧၮ"), bstack11111l1ll1_opy_)
        else:
            bstack1111l1llll_opy_ = {
                bstack11l11_opy_ (u"ࠧࡪࡦࠪၯ"): uuid4().__str__(),
                bstack11l11_opy_ (u"ࠨࡶࡨࡼࡹ࠭ၰ"): bstack11l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨၱ").format(attrs.get(bstack11l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪၲ")), attrs.get(bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩၳ"), bstack11l11_opy_ (u"ࠬ࠭ၴ"))) if attrs.get(bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫၵ"), []) else attrs.get(bstack11l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧၶ")),
                bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨၷ"): attrs.get(bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧၸ"), []),
                bstack11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧၹ"): bstack11l1lll11_opy_(),
                bstack11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫၺ"): bstack11l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ၻ"),
                bstack11l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫၼ"): attrs.get(bstack11l11_opy_ (u"ࠧࡥࡱࡦࠫၽ"), bstack11l11_opy_ (u"ࠨࠩၾ"))
            }
            if attrs.get(bstack11l11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪၿ"), bstack11l11_opy_ (u"ࠪࠫႀ")) != bstack11l11_opy_ (u"ࠫࠬႁ"):
                bstack1111l1llll_opy_[bstack11l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ႂ")] = attrs.get(bstack11l11_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧႃ"))
            if not self.bstack1111111l1l_opy_:
                self._1lllllll11l_opy_[self._1lllllll111_opy_()][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႄ")].add_step(bstack1111l1llll_opy_)
                threading.current_thread().current_step_uuid = bstack1111l1llll_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡧࠫႅ")]
            self.bstack1111111l1l_opy_.append(bstack1111l1llll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1llllll1111_opy_()
        self._11111111ll_opy_(messages)
        current_test_id = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫႆ"), None)
        bstack111111111l_opy_ = current_test_id if current_test_id else bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ႇ"), None)
        bstack1lllll1ll1l_opy_ = bstack1111111ll1_opy_.get(attrs.get(bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫႈ")), bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ႉ"))
        bstack1lllll1l1ll_opy_ = attrs.get(bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႊ"))
        if bstack1lllll1ll1l_opy_ != bstack11l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨႋ") and not attrs.get(bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႌ")) and self._1lllllllll1_opy_:
            bstack1lllll1l1ll_opy_ = self._1lllllllll1_opy_
        bstack11111lll11_opy_ = Result(result=bstack1lllll1ll1l_opy_, exception=bstack1lllll1l1ll_opy_, bstack1111ll11l1_opy_=[bstack1lllll1l1ll_opy_])
        if attrs.get(bstack11l11_opy_ (u"ࠩࡷࡽࡵ࡫ႍࠧ"), bstack11l11_opy_ (u"ࠪࠫႎ")).lower() in [bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪႏ"), bstack11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ႐")]:
            bstack111111111l_opy_ = current_test_id if current_test_id else bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ႑"), None)
            if bstack111111111l_opy_:
                bstack1111ll11ll_opy_ = bstack111111111l_opy_ + bstack11l11_opy_ (u"ࠢ࠮ࠤ႒") + attrs.get(bstack11l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭႓"), bstack11l11_opy_ (u"ࠩࠪ႔")).lower()
                self._1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭႕")].stop(time=bstack11l1lll11_opy_(), duration=int(attrs.get(bstack11l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ႖"), bstack11l11_opy_ (u"ࠬ࠶ࠧ႗"))), result=bstack11111lll11_opy_)
                bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ႘"), self._1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ႙")])
        else:
            bstack111111111l_opy_ = current_test_id if current_test_id else bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪႚ"), None)
            if bstack111111111l_opy_ and len(self.bstack1111111l1l_opy_) == 1:
                current_step_uuid = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ႛ"), None)
                self._1lllllll11l_opy_[bstack111111111l_opy_][bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ႜ")].bstack11111ll11l_opy_(current_step_uuid, duration=int(attrs.get(bstack11l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩႝ"), bstack11l11_opy_ (u"ࠬ࠶ࠧ႞"))), result=bstack11111lll11_opy_)
            else:
                self.bstack1llllll1l11_opy_(attrs)
            self.bstack1111111l1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l11_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ႟"), bstack11l11_opy_ (u"ࠧ࡯ࡱࠪႠ")) == bstack11l11_opy_ (u"ࠨࡻࡨࡷࠬႡ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1ll111l_opy_.bstack11111ll1ll_opy_():
                logs.append({
                    bstack11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬႢ"): bstack11l1lll11_opy_(),
                    bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႣ"): message.get(bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႤ")),
                    bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫႥ"): message.get(bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬႦ")),
                    **bstack11l1ll111l_opy_.bstack11111ll1ll_opy_()
                })
                if len(logs) > 0:
                    bstack1ll111l1_opy_.bstack1l1l1l11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1ll111l1_opy_.bstack11111l1l1l_opy_()
    def bstack1llllll1l11_opy_(self, bstack1llllll1ll1_opy_):
        if not bstack11l1ll111l_opy_.bstack11111ll1ll_opy_():
            return
        kwname = bstack11l11_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭Ⴇ").format(bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨႨ")), bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧႩ"), bstack11l11_opy_ (u"ࠪࠫႪ"))) if bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩႫ"), []) else bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬႬ"))
        error_message = bstack11l11_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧႭ").format(kwname, bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧႮ")), str(bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႯ"))))
        bstack111111lll1_opy_ = bstack11l11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣႰ").format(kwname, bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪႱ")))
        bstack1lllllll1ll_opy_ = error_message if bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႲ")) else bstack111111lll1_opy_
        bstack1llllll1l1l_opy_ = {
            bstack11l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨႳ"): self.bstack1111111l1l_opy_[-1].get(bstack11l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪႴ"), bstack11l1lll11_opy_()),
            bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႵ"): bstack1lllllll1ll_opy_,
            bstack11l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧႶ"): bstack11l11_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨႷ") if bstack1llllll1ll1_opy_.get(bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪႸ")) == bstack11l11_opy_ (u"ࠫࡋࡇࡉࡍࠩႹ") else bstack11l11_opy_ (u"ࠬࡏࡎࡇࡑࠪႺ"),
            **bstack11l1ll111l_opy_.bstack11111ll1ll_opy_()
        }
        bstack1ll111l1_opy_.bstack1l1l1l11l_opy_([bstack1llllll1l1l_opy_])
    def _1lllllll111_opy_(self):
        for bstack111111llll_opy_ in reversed(self._1lllllll11l_opy_):
            bstack1lllll1lll1_opy_ = bstack111111llll_opy_
            data = self._1lllllll11l_opy_[bstack111111llll_opy_][bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩႻ")]
            if isinstance(data, bstack1111l1lll1_opy_):
                if not bstack11l11_opy_ (u"ࠧࡆࡃࡆࡌࠬႼ") in data.bstack111111l1l1_opy_():
                    return bstack1lllll1lll1_opy_
            else:
                return bstack1lllll1lll1_opy_
    def _11111111ll_opy_(self, messages):
        try:
            bstack111111l1ll_opy_ = BuiltIn().get_variable_value(bstack11l11_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢႽ")) in (bstack1llllllllll_opy_.DEBUG, bstack1llllllllll_opy_.TRACE)
            for message, bstack1lllll1l1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႾ"))
                level = message.get(bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႿ"))
                if level == bstack1llllllllll_opy_.FAIL:
                    self._1lllllllll1_opy_ = name or self._1lllllllll1_opy_
                    self._111111l111_opy_ = bstack1lllll1l1l1_opy_.get(bstack11l11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧჀ")) if bstack111111l1ll_opy_ and bstack1lllll1l1l1_opy_ else self._111111l111_opy_
        except:
            pass
    @classmethod
    def bstack1111l11111_opy_(self, event: str, bstack111111ll11_opy_: bstack11111111l1_opy_, bstack1llllll111l_opy_=False):
        if event == bstack11l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧჁ"):
            bstack111111ll11_opy_.set(hooks=self.store[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪჂ")])
        if event == bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨჃ"):
            event = bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪჄ")
        if bstack1llllll111l_opy_:
            bstack11111l1lll_opy_ = {
                bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ⴥ"): event,
                bstack111111ll11_opy_.bstack1111111lll_opy_(): bstack111111ll11_opy_.bstack1lllllll1l1_opy_(event)
            }
            with self._lock:
                self.bstack1llllllll1l_opy_.append(bstack11111l1lll_opy_)
        else:
            bstack1ll111l1_opy_.bstack1111l11111_opy_(event, bstack111111ll11_opy_)
class bstack1llllll11l1_opy_:
    def __init__(self):
        self._1llllll1lll_opy_ = []
    def bstack1111111111_opy_(self):
        self._1llllll1lll_opy_.append([])
    def bstack1llllll1111_opy_(self):
        return self._1llllll1lll_opy_.pop() if self._1llllll1lll_opy_ else list()
    def push(self, message):
        self._1llllll1lll_opy_[-1].append(message) if self._1llllll1lll_opy_ else self._1llllll1lll_opy_.append([message])
class bstack1llllllllll_opy_:
    FAIL = bstack11l11_opy_ (u"ࠪࡊࡆࡏࡌࠨ჆")
    ERROR = bstack11l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪჇ")
    WARNING = bstack11l11_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ჈")
    bstack1lllll1ll11_opy_ = bstack11l11_opy_ (u"࠭ࡉࡏࡈࡒࠫ჉")
    DEBUG = bstack11l11_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭჊")
    TRACE = bstack11l11_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ჋")
    bstack11111ll111_opy_ = [FAIL, ERROR]
def bstack1111111l11_opy_(bstack11111l1111_opy_):
    if not bstack11111l1111_opy_:
        return None
    if bstack11111l1111_opy_.get(bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ჌"), None):
        return getattr(bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴭ")], bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ჎"), None)
    return bstack11111l1111_opy_.get(bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ჏"), None)
def bstack11111l11l1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬა"), bstack11l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩბ")]:
        return
    if hook_type.lower() == bstack11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧგ"):
        if current_test_uuid is None:
            return bstack11l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭დ")
        else:
            return bstack11l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨე")
    elif hook_type.lower() == bstack11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ვ"):
        if current_test_uuid is None:
            return bstack11l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨზ")
        else:
            return bstack11l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪთ")