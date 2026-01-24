# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11111lll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack111l1111ll_opy_
from bstack_utils.bstack1111ll1lll_opy_ import bstack111111111l_opy_, bstack1111ll1l11_opy_, bstack1111llll1l_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.bstack1111ll11l1_opy_ import bstack11l11111l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111111lll_opy_, bstack1111l11l1_opy_, Result, \
    error_handler, bstack11111l1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ࿦"): [],
        bstack1l1111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ࿧"): [],
        bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ࿨"): []
    }
    bstack1111l11ll1_opy_ = []
    bstack1111l11111_opy_ = []
    @staticmethod
    def bstack111l11111l_opy_(log):
        if not ((isinstance(log[bstack1l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿩")], list) or (isinstance(log[bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿪")], dict)) and len(log[bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿫")])>0) or (isinstance(log[bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿬")], str) and log[bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿭")].strip())):
            return
        active = bstack1lll11ll11_opy_.bstack1111lll1l1_opy_()
        log = {
            bstack1l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿮"): log[bstack1l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿯")],
            bstack1l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ࿰"): bstack11111l1l11_opy_().isoformat() + bstack1l1111_opy_ (u"࡛ࠧࠩ࿱"),
            bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿲"): log[bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿳")],
        }
        if active:
            if active[bstack1l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ࿴")] == bstack1l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ࿵"):
                log[bstack1l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ࿶")] = active[bstack1l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭࿷")]
            elif active[bstack1l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ࿸")] == bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭࿹"):
                log[bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ࿺")] = active[bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ࿻")]
        bstack11l11111l_opy_.bstack1l1111ll_opy_([log])
    def __init__(self):
        self.messages = bstack1111l1l11l_opy_()
        self._1lllllll1ll_opy_ = None
        self._11111lll11_opy_ = None
        self._111111ll11_opy_ = OrderedDict()
        self.bstack1111l1lll1_opy_ = bstack111l1111ll_opy_(self.bstack111l11111l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111111l1l1_opy_()
        if not self._111111ll11_opy_.get(attrs.get(bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧ࿼")), None):
            self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨ࿽"))] = {}
        bstack11111lllll_opy_ = bstack1111llll1l_opy_(
                bstack1111l111ll_opy_=attrs.get(bstack1l1111_opy_ (u"࠭ࡩࡥࠩ࿾")),
                name=name,
                started_at=bstack1111l11l1_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿿")], start=os.getcwd()) if attrs.get(bstack1l1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨက")) != bstack1l1111_opy_ (u"ࠩࠪခ") else bstack1l1111_opy_ (u"ࠪࠫဂ"),
                framework=bstack1l1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪဃ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨင"), None)
        self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"࠭ࡩࡥࠩစ"))][bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪဆ")] = bstack11111lllll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111111lll1_opy_()
        self._1111111l1l_opy_(messages)
        with self._lock:
            for bstack11111l1lll_opy_ in self.bstack1111l11ll1_opy_:
                bstack11111l1lll_opy_[bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪဇ")][bstack1l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨဈ")].extend(self.store[bstack1l1111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩဉ")])
                bstack11l11111l_opy_.bstack1l11llll1_opy_(bstack11111l1lll_opy_)
            self.bstack1111l11ll1_opy_ = []
            self.store[bstack1l1111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪည")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1111l1lll1_opy_.start()
        if not self._111111ll11_opy_.get(attrs.get(bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨဋ")), None):
            self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"࠭ࡩࡥࠩဌ"))] = {}
        driver = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ဍ"), None)
        bstack1111ll1lll_opy_ = bstack1111llll1l_opy_(
            bstack1111l111ll_opy_=attrs.get(bstack1l1111_opy_ (u"ࠨ࡫ࡧࠫဎ")),
            name=name,
            started_at=bstack1111l11l1_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩဏ")], start=os.getcwd()),
            scope=RobotHandler.bstack11111l1111_opy_(attrs.get(bstack1l1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪတ"), None)),
            framework=bstack1l1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪထ"),
            tags=attrs[bstack1l1111_opy_ (u"ࠬࡺࡡࡨࡵࠪဒ")],
            hooks=self.store[bstack1l1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬဓ")],
            bstack1111ll11ll_opy_=bstack11l11111l_opy_.bstack1111ll111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1111_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤန").format(bstack1l1111_opy_ (u"ࠣࠢࠥပ").join(attrs[bstack1l1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧဖ")]), name) if attrs[bstack1l1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨဗ")] else name
        )
        self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧဘ"))][bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨမ")] = bstack1111ll1lll_opy_
        threading.current_thread().current_test_uuid = bstack1111ll1lll_opy_.bstack1111l1l111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1111_opy_ (u"࠭ࡩࡥࠩယ"), None)
        self.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨရ"), bstack1111ll1lll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1111l1lll1_opy_.reset()
        bstack111111l11l_opy_ = bstack1llllllll1l_opy_.get(attrs.get(bstack1l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨလ")), bstack1l1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪဝ"))
        self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"ࠪ࡭ࡩ࠭သ"))][bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧဟ")].stop(time=bstack1111l11l1_opy_(), duration=int(attrs.get(bstack1l1111_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪဠ"), bstack1l1111_opy_ (u"࠭࠰ࠨအ"))), result=Result(result=bstack111111l11l_opy_, exception=attrs.get(bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ")), bstack1111lll11l_opy_=[attrs.get(bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဣ"))]))
        self.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫဤ"), self._111111ll11_opy_[attrs.get(bstack1l1111_opy_ (u"ࠪ࡭ࡩ࠭ဥ"))][bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧဦ")], True)
        with self._lock:
            self.store[bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩဧ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111111l1l1_opy_()
        current_test_id = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨဨ"), None)
        bstack1111111lll_opy_ = current_test_id if bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩဩ"), None) else bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫဪ"), None)
        if attrs.get(bstack1l1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧါ"), bstack1l1111_opy_ (u"ࠪࠫာ")).lower() in [bstack1l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪိ"), bstack1l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧီ")]:
            hook_type = bstack1llllllllll_opy_(attrs.get(bstack1l1111_opy_ (u"࠭ࡴࡺࡲࡨࠫု")), bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫူ"), None))
            hook_name = bstack1l1111_opy_ (u"ࠨࡽࢀࠫေ").format(attrs.get(bstack1l1111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩဲ"), bstack1l1111_opy_ (u"ࠪࠫဳ")))
            if hook_type in [bstack1l1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨဴ"), bstack1l1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨဵ")]:
                hook_name = bstack1l1111_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧံ").format(bstack11111l1ll1_opy_.get(hook_type), attrs.get(bstack1l1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫့ࠧ"), bstack1l1111_opy_ (u"ࠨࠩး")))
            bstack11111111ll_opy_ = bstack1111ll1l11_opy_(
                bstack1111l111ll_opy_=bstack1111111lll_opy_ + bstack1l1111_opy_ (u"ࠩ࠰္ࠫ") + attrs.get(bstack1l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ်"), bstack1l1111_opy_ (u"ࠫࠬျ")).lower(),
                name=hook_name,
                started_at=bstack1111l11l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬြ")), start=os.getcwd()),
                framework=bstack1l1111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬွ"),
                tags=attrs[bstack1l1111_opy_ (u"ࠧࡵࡣࡪࡷࠬှ")],
                scope=RobotHandler.bstack11111l1111_opy_(attrs.get(bstack1l1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨဿ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11111111ll_opy_.bstack1111l1l111_opy_()
            threading.current_thread().current_hook_id = bstack1111111lll_opy_ + bstack1l1111_opy_ (u"ࠩ࠰ࠫ၀") + attrs.get(bstack1l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ၁"), bstack1l1111_opy_ (u"ࠫࠬ၂")).lower()
            with self._lock:
                self.store[bstack1l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ၃")] = [bstack11111111ll_opy_.bstack1111l1l111_opy_()]
                if bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ၄"), None):
                    self.store[bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ၅")].append(bstack11111111ll_opy_.bstack1111l1l111_opy_())
                else:
                    self.store[bstack1l1111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ၆")].append(bstack11111111ll_opy_.bstack1111l1l111_opy_())
            if bstack1111111lll_opy_:
                self._111111ll11_opy_[bstack1111111lll_opy_ + bstack1l1111_opy_ (u"ࠩ࠰ࠫ၇") + attrs.get(bstack1l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ၈"), bstack1l1111_opy_ (u"ࠫࠬ၉")).lower()] = { bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ၊"): bstack11111111ll_opy_ }
            bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ။"), bstack11111111ll_opy_)
        else:
            bstack1111lll111_opy_ = {
                bstack1l1111_opy_ (u"ࠧࡪࡦࠪ၌"): uuid4().__str__(),
                bstack1l1111_opy_ (u"ࠨࡶࡨࡼࡹ࠭၍"): bstack1l1111_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ၎").format(attrs.get(bstack1l1111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ၏")), attrs.get(bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩၐ"), bstack1l1111_opy_ (u"ࠬ࠭ၑ"))) if attrs.get(bstack1l1111_opy_ (u"࠭ࡡࡳࡩࡶࠫၒ"), []) else attrs.get(bstack1l1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧၓ")),
                bstack1l1111_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨၔ"): attrs.get(bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧၕ"), []),
                bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧၖ"): bstack1111l11l1_opy_(),
                bstack1l1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫၗ"): bstack1l1111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ၘ"),
                bstack1l1111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫၙ"): attrs.get(bstack1l1111_opy_ (u"ࠧࡥࡱࡦࠫၚ"), bstack1l1111_opy_ (u"ࠨࠩၛ"))
            }
            if attrs.get(bstack1l1111_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪၜ"), bstack1l1111_opy_ (u"ࠪࠫၝ")) != bstack1l1111_opy_ (u"ࠫࠬၞ"):
                bstack1111lll111_opy_[bstack1l1111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ၟ")] = attrs.get(bstack1l1111_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧၠ"))
            if not self.bstack1111l11111_opy_:
                self._111111ll11_opy_[self._1111l11lll_opy_()][bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪၡ")].add_step(bstack1111lll111_opy_)
                threading.current_thread().current_step_uuid = bstack1111lll111_opy_[bstack1l1111_opy_ (u"ࠨ࡫ࡧࠫၢ")]
            self.bstack1111l11111_opy_.append(bstack1111lll111_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111111lll1_opy_()
        self._1111111l1l_opy_(messages)
        current_test_id = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫၣ"), None)
        bstack1111111lll_opy_ = current_test_id if current_test_id else bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ၤ"), None)
        bstack1111l11l1l_opy_ = bstack1llllllll1l_opy_.get(attrs.get(bstack1l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫၥ")), bstack1l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ၦ"))
        bstack111111l1ll_opy_ = attrs.get(bstack1l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧၧ"))
        if bstack1111l11l1l_opy_ != bstack1l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨၨ") and not attrs.get(bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩၩ")) and self._1lllllll1ll_opy_:
            bstack111111l1ll_opy_ = self._1lllllll1ll_opy_
        bstack1111lllll1_opy_ = Result(result=bstack1111l11l1l_opy_, exception=bstack111111l1ll_opy_, bstack1111lll11l_opy_=[bstack111111l1ll_opy_])
        if attrs.get(bstack1l1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧၪ"), bstack1l1111_opy_ (u"ࠪࠫၫ")).lower() in [bstack1l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪၬ"), bstack1l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧၭ")]:
            bstack1111111lll_opy_ = current_test_id if current_test_id else bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩၮ"), None)
            if bstack1111111lll_opy_:
                bstack1111l1l1ll_opy_ = bstack1111111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠮ࠤၯ") + attrs.get(bstack1l1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ၰ"), bstack1l1111_opy_ (u"ࠩࠪၱ")).lower()
                self._111111ll11_opy_[bstack1111l1l1ll_opy_][bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ၲ")].stop(time=bstack1111l11l1_opy_(), duration=int(attrs.get(bstack1l1111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩၳ"), bstack1l1111_opy_ (u"ࠬ࠶ࠧၴ"))), result=bstack1111lllll1_opy_)
                bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨၵ"), self._111111ll11_opy_[bstack1111l1l1ll_opy_][bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪၶ")])
        else:
            bstack1111111lll_opy_ = current_test_id if current_test_id else bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪၷ"), None)
            if bstack1111111lll_opy_ and len(self.bstack1111l11111_opy_) == 1:
                current_step_uuid = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ၸ"), None)
                self._111111ll11_opy_[bstack1111111lll_opy_][bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ၹ")].bstack1111llllll_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩၺ"), bstack1l1111_opy_ (u"ࠬ࠶ࠧၻ"))), result=bstack1111lllll1_opy_)
            else:
                self.bstack11111l1l1l_opy_(attrs)
            self.bstack1111l11111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1111_opy_ (u"࠭ࡨࡵ࡯࡯ࠫၼ"), bstack1l1111_opy_ (u"ࠧ࡯ࡱࠪၽ")) == bstack1l1111_opy_ (u"ࠨࡻࡨࡷࠬၾ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1lll11ll11_opy_.bstack1111lll1l1_opy_():
                logs.append({
                    bstack1l1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬၿ"): bstack1111l11l1_opy_(),
                    bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႀ"): message.get(bstack1l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႁ")),
                    bstack1l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫႂ"): message.get(bstack1l1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬႃ")),
                    **bstack1lll11ll11_opy_.bstack1111lll1l1_opy_()
                })
                if len(logs) > 0:
                    bstack11l11111l_opy_.bstack1l1111ll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11l11111l_opy_.bstack1111l111l1_opy_()
    def bstack11111l1l1l_opy_(self, bstack1lllllllll1_opy_):
        if not bstack1lll11ll11_opy_.bstack1111lll1l1_opy_():
            return
        kwname = bstack1l1111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ႄ").format(bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨႅ")), bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧႆ"), bstack1l1111_opy_ (u"ࠪࠫႇ"))) if bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩႈ"), []) else bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬႉ"))
        error_message = bstack1l1111_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧႊ").format(kwname, bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧႋ")), str(bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႌ"))))
        bstack111111l111_opy_ = bstack1l1111_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢႍࠢࠣ").format(kwname, bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪႎ")))
        bstack11111l11l1_opy_ = error_message if bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႏ")) else bstack111111l111_opy_
        bstack11111111l1_opy_ = {
            bstack1l1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ႐"): self.bstack1111l11111_opy_[-1].get(bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ႑"), bstack1111l11l1_opy_()),
            bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ႒"): bstack11111l11l1_opy_,
            bstack1l1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ႓"): bstack1l1111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ႔") if bstack1lllllllll1_opy_.get(bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ႕")) == bstack1l1111_opy_ (u"ࠫࡋࡇࡉࡍࠩ႖") else bstack1l1111_opy_ (u"ࠬࡏࡎࡇࡑࠪ႗"),
            **bstack1lll11ll11_opy_.bstack1111lll1l1_opy_()
        }
        bstack11l11111l_opy_.bstack1l1111ll_opy_([bstack11111111l1_opy_])
    def _1111l11lll_opy_(self):
        for bstack1111l111ll_opy_ in reversed(self._111111ll11_opy_):
            bstack1111111l11_opy_ = bstack1111l111ll_opy_
            data = self._111111ll11_opy_[bstack1111l111ll_opy_][bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ႘")]
            if isinstance(data, bstack1111ll1l11_opy_):
                if not bstack1l1111_opy_ (u"ࠧࡆࡃࡆࡌࠬ႙") in data.bstack1111111111_opy_():
                    return bstack1111111l11_opy_
            else:
                return bstack1111111l11_opy_
    def _1111111l1l_opy_(self, messages):
        try:
            bstack1llllllll11_opy_ = BuiltIn().get_variable_value(bstack1l1111_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢႚ")) in (bstack11111ll1ll_opy_.DEBUG, bstack11111ll1ll_opy_.TRACE)
            for message, bstack1111l1111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႛ"))
                level = message.get(bstack1l1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႜ"))
                if level == bstack11111ll1ll_opy_.FAIL:
                    self._1lllllll1ll_opy_ = name or self._1lllllll1ll_opy_
                    self._11111lll11_opy_ = bstack1111l1111l_opy_.get(bstack1l1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧႝ")) if bstack1llllllll11_opy_ and bstack1111l1111l_opy_ else self._11111lll11_opy_
        except:
            pass
    @classmethod
    def bstack1111ll1111_opy_(self, event: str, bstack11111l11ll_opy_: bstack111111111l_opy_, bstack11111llll1_opy_=False):
        if event == bstack1l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ႞"):
            bstack11111l11ll_opy_.set(hooks=self.store[bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ႟")])
        if event == bstack1l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨႠ"):
            event = bstack1l1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪႡ")
        if bstack11111llll1_opy_:
            bstack1111111ll1_opy_ = {
                bstack1l1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ⴂ"): event,
                bstack11111l11ll_opy_.bstack11111ll1l1_opy_(): bstack11111l11ll_opy_.bstack111111llll_opy_(event)
            }
            with self._lock:
                self.bstack1111l11ll1_opy_.append(bstack1111111ll1_opy_)
        else:
            bstack11l11111l_opy_.bstack1111ll1111_opy_(event, bstack11111l11ll_opy_)
class bstack1111l1l11l_opy_:
    def __init__(self):
        self._11111ll111_opy_ = []
    def bstack111111l1l1_opy_(self):
        self._11111ll111_opy_.append([])
    def bstack111111lll1_opy_(self):
        return self._11111ll111_opy_.pop() if self._11111ll111_opy_ else list()
    def push(self, message):
        self._11111ll111_opy_[-1].append(message) if self._11111ll111_opy_ else self._11111ll111_opy_.append([message])
class bstack11111ll1ll_opy_:
    FAIL = bstack1l1111_opy_ (u"ࠪࡊࡆࡏࡌࠨႣ")
    ERROR = bstack1l1111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪႤ")
    WARNING = bstack1l1111_opy_ (u"ࠬ࡝ࡁࡓࡐࠪႥ")
    bstack11111ll11l_opy_ = bstack1l1111_opy_ (u"࠭ࡉࡏࡈࡒࠫႦ")
    DEBUG = bstack1l1111_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭Ⴇ")
    TRACE = bstack1l1111_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧႨ")
    bstack1111l11l11_opy_ = [FAIL, ERROR]
def bstack111111ll1l_opy_(bstack11111l111l_opy_):
    if not bstack11111l111l_opy_:
        return None
    if bstack11111l111l_opy_.get(bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႩ"), None):
        return getattr(bstack11111l111l_opy_[bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴊ")], bstack1l1111_opy_ (u"ࠫࡺࡻࡩࡥࠩႫ"), None)
    return bstack11111l111l_opy_.get(bstack1l1111_opy_ (u"ࠬࡻࡵࡪࡦࠪႬ"), None)
def bstack1llllllllll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬႭ"), bstack1l1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩႮ")]:
        return
    if hook_type.lower() == bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧႯ"):
        if current_test_uuid is None:
            return bstack1l1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭Ⴐ")
        else:
            return bstack1l1111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨႱ")
    elif hook_type.lower() == bstack1l1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭Ⴒ"):
        if current_test_uuid is None:
            return bstack1l1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨႳ")
        else:
            return bstack1l1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪႴ")