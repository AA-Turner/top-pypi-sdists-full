# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll1lll1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack1llll11l1l1_opy_
from bstack_utils.bstack1llll11llll_opy_ import bstack1lll1llll11_opy_, bstack1llll111l11_opy_, bstack1llll1l111l_opy_
from bstack_utils.bstack111ll111ll_opy_ import bstack11l1l1l1_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l11l1ll_opy_, bstack111ll1ll1l_opy_, Result, \
    error_handler, bstack1lll1l11ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᄜ"): [],
        bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬᄝ"): [],
        bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᄞ"): []
    }
    bstack1lll11ll1l1_opy_ = []
    bstack1lll1lllll1_opy_ = []
    @staticmethod
    def bstack1llll1l1l1l_opy_(log):
        if not ((isinstance(log[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᄟ")], list) or (isinstance(log[bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᄠ")], dict)) and len(log[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄡ")])>0) or (isinstance(log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄢ")], str) and log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄣ")].strip())):
            return
        active = bstack11l1l1l1_opy_.bstack1llll1111ll_opy_()
        log = {
            bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᄤ"): log[bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᄥ")],
            bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᄦ"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫᄧ"),
            bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄨ"): log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄩ")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᄪ")] == bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᄫ"):
                log[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᄬ")] = active[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᄭ")]
            elif active[bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᄮ")] == bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨᄯ"):
                log[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᄰ")] = active[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᄱ")]
        TestHubHandler.bstack1l11ll11l_opy_([log])
    def __init__(self):
        self.messages = bstack1lll11l1l1l_opy_()
        self._1lll11lll1l_opy_ = None
        self._1lll11lll11_opy_ = None
        self._1lll1l11l11_opy_ = OrderedDict()
        self.bstack1llll1l1111_opy_ = bstack1llll11l1l1_opy_(self.bstack1llll1l1l1l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lll1l111l1_opy_()
        if not self._1lll1l11l11_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᄲ")), None):
            self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᄳ"))] = {}
        bstack1lll1ll111l_opy_ = bstack1llll1l111l_opy_(
                bstack1lll11ll1ll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᄴ")),
                name=name,
                started_at=bstack111ll1ll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᄵ")], start=os.getcwd()) if attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᄶ")) != bstack1ll1l11_opy_ (u"ࠫࠬᄷ") else bstack1ll1l11_opy_ (u"ࠬ࠭ᄸ"),
                framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬᄹ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᄺ"), None)
        self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᄻ"))][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄼ")] = bstack1lll1ll111l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll1l1l1ll_opy_()
        self._1lll1l111ll_opy_(messages)
        with self._lock:
            for bstack1lll1lll1ll_opy_ in self.bstack1lll11ll1l1_opy_:
                bstack1lll1lll1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᄽ")][bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᄾ")].extend(self.store[bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᄿ")])
                TestHubHandler.bstack1ll11ll11_opy_(bstack1lll1lll1ll_opy_)
            self.bstack1lll11ll1l1_opy_ = []
            self.store[bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬᅀ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1llll1l1111_opy_.start()
        if not self._1lll1l11l11_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᅁ")), None):
            self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᅂ"))] = {}
        driver = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᅃ"), None)
        bstack1llll11llll_opy_ = bstack1llll1l111l_opy_(
            bstack1lll11ll1ll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ᅄ")),
            name=name,
            started_at=bstack111ll1ll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᅅ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1ll11l1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᅆ"), None)),
            framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬᅇ"),
            tags=attrs[bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᅈ")],
            hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᅉ")],
            integrations=TestHubHandler.bstack1llll11lll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1l11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦᅊ").format(bstack1ll1l11_opy_ (u"ࠥࠤࠧᅋ").join(attrs[bstack1ll1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᅌ")]), name) if attrs[bstack1ll1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᅍ")] else name
        )
        self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᅎ"))][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᅏ")] = bstack1llll11llll_opy_
        threading.current_thread().current_test_uuid = bstack1llll11llll_opy_.bstack1lll1ll1111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᅐ"), None)
        self.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᅑ"), bstack1llll11llll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1llll1l1111_opy_.reset()
        bstack1lll1l1llll_opy_ = bstack1lll11l1ll1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᅒ")), bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᅓ"))
        self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨᅔ"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅕ")].stop(time=bstack111ll1ll1l_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬᅖ"), bstack1ll1l11_opy_ (u"ࠨ࠲ࠪᅗ"))), result=Result(result=bstack1lll1l1llll_opy_, exception=attrs.get(bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᅘ")), bstack1llll1l11l1_opy_=[attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᅙ"))]))
        self.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᅚ"), self._1lll1l11l11_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨᅛ"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅜ")], True)
        with self._lock:
            self.store[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᅝ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lll1l111l1_opy_()
        current_test_id = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪᅞ"), None)
        bstack1lll1ll1l1l_opy_ = current_test_id if bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫᅟ"), None) else bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᅠ"), None)
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᅡ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᅢ")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᅣ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᅤ")]:
            hook_type = bstack1lll1l1lll1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᅥ")), bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᅦ"), None))
            hook_name = bstack1ll1l11_opy_ (u"ࠪࡿࢂ࠭ᅧ").format(attrs.get(bstack1ll1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᅨ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᅩ")))
            if hook_type in [bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᅪ"), bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᅫ")]:
                hook_name = bstack1ll1l11_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩᅬ").format(bstack1lll1l1l1l1_opy_.get(hook_type), attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᅭ"), bstack1ll1l11_opy_ (u"ࠪࠫᅮ")))
            bstack1lll1ll1ll1_opy_ = bstack1llll111l11_opy_(
                bstack1lll11ll1ll_opy_=bstack1lll1ll1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭ᅯ") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᅰ"), bstack1ll1l11_opy_ (u"࠭ࠧᅱ")).lower(),
                name=hook_name,
                started_at=bstack111ll1ll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᅲ")), start=os.getcwd()),
                framework=bstack1ll1l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅳ"),
                tags=attrs[bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᅴ")],
                scope=RobotHandler.bstack1lll1ll11l1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᅵ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lll1ll1ll1_opy_.bstack1lll1ll1111_opy_()
            threading.current_thread().current_hook_id = bstack1lll1ll1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭ᅶ") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᅷ"), bstack1ll1l11_opy_ (u"࠭ࠧᅸ")).lower()
            with self._lock:
                self.store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᅹ")] = [bstack1lll1ll1ll1_opy_.bstack1lll1ll1111_opy_()]
                if bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᅺ"), None):
                    self.store[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᅻ")].append(bstack1lll1ll1ll1_opy_.bstack1lll1ll1111_opy_())
                else:
                    self.store[bstack1ll1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩᅼ")].append(bstack1lll1ll1ll1_opy_.bstack1lll1ll1111_opy_())
            if bstack1lll1ll1l1l_opy_:
                self._1lll1l11l11_opy_[bstack1lll1ll1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭ᅽ") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᅾ"), bstack1ll1l11_opy_ (u"࠭ࠧᅿ")).lower()] = { bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆀ"): bstack1lll1ll1ll1_opy_ }
            TestHubHandler.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᆁ"), bstack1lll1ll1ll1_opy_)
        else:
            bstack1llll11ll11_opy_ = {
                bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬᆂ"): uuid4().__str__(),
                bstack1ll1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨᆃ"): bstack1ll1l11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᆄ").format(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᆅ")), attrs.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᆆ"), bstack1ll1l11_opy_ (u"ࠧࠨᆇ"))) if attrs.get(bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆈ"), []) else attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᆉ")),
                bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪᆊ"): attrs.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩᆋ"), []),
                bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᆌ"): bstack111ll1ll1l_opy_(),
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᆍ"): bstack1ll1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᆎ"),
                bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᆏ"): attrs.get(bstack1ll1l11_opy_ (u"ࠩࡧࡳࡨ࠭ᆐ"), bstack1ll1l11_opy_ (u"ࠪࠫᆑ"))
            }
            if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬᆒ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᆓ")) != bstack1ll1l11_opy_ (u"࠭ࠧᆔ"):
                bstack1llll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᆕ")] = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩᆖ"))
            if not self.bstack1lll1lllll1_opy_:
                self._1lll1l11l11_opy_[self._1lll1l11lll_opy_()][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆗ")].add_step(bstack1llll11ll11_opy_)
                threading.current_thread().current_step_uuid = bstack1llll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ᆘ")]
            self.bstack1lll1lllll1_opy_.append(bstack1llll11ll11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll1l1l1ll_opy_()
        self._1lll1l111ll_opy_(messages)
        current_test_id = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᆙ"), None)
        bstack1lll1ll1l1l_opy_ = current_test_id if current_test_id else bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᆚ"), None)
        bstack1lll1lll111_opy_ = bstack1lll11l1ll1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᆛ")), bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᆜ"))
        bstack1lll1l11111_opy_ = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᆝ"))
        if bstack1lll1lll111_opy_ != bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᆞ") and not attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᆟ")) and self._1lll11lll1l_opy_:
            bstack1lll1l11111_opy_ = self._1lll11lll1l_opy_
        bstack1llll1l1lll_opy_ = Result(result=bstack1lll1lll111_opy_, exception=bstack1lll1l11111_opy_, bstack1llll1l11l1_opy_=[bstack1lll1l11111_opy_])
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᆠ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᆡ")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᆢ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᆣ")]:
            bstack1lll1ll1l1l_opy_ = current_test_id if current_test_id else bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫᆤ"), None)
            if bstack1lll1ll1l1l_opy_:
                bstack1llll1ll11l_opy_ = bstack1lll1ll1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠰ࠦᆥ") + attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᆦ"), bstack1ll1l11_opy_ (u"ࠫࠬᆧ")).lower()
                self._1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᆨ")].stop(time=bstack111ll1ll1l_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᆩ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩᆪ"))), result=bstack1llll1l1lll_opy_)
                TestHubHandler.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᆫ"), self._1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆬ")])
        else:
            bstack1lll1ll1l1l_opy_ = current_test_id if current_test_id else bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬᆭ"), None)
            if bstack1lll1ll1l1l_opy_ and len(self.bstack1lll1lllll1_opy_) == 1:
                current_step_uuid = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨᆮ"), None)
                self._1lll1l11l11_opy_[bstack1lll1ll1l1l_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᆯ")].bstack1llll1ll111_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᆰ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩᆱ"))), result=bstack1llll1l1lll_opy_)
            else:
                self.bstack1lll11llll1_opy_(attrs)
            self.bstack1lll1lllll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡱࡱ࠭ᆲ"), bstack1ll1l11_opy_ (u"ࠩࡱࡳࠬᆳ")) == bstack1ll1l11_opy_ (u"ࠪࡽࡪࡹࠧᆴ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1l1l1_opy_.bstack1llll1111ll_opy_():
                logs.append({
                    bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᆵ"): bstack111ll1ll1l_opy_(),
                    bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆶ"): message.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆷ")),
                    bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᆸ"): message.get(bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᆹ")),
                    **bstack11l1l1l1_opy_.bstack1llll1111ll_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1l11ll11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll1ll11ll_opy_()
    def bstack1lll11llll1_opy_(self, bstack1llll1111l1_opy_):
        if not bstack11l1l1l1_opy_.bstack1llll1111ll_opy_():
            return
        kwname = bstack1ll1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨᆺ").format(bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᆻ")), bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩᆼ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᆽ"))) if bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᆾ"), []) else bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᆿ"))
        error_message = bstack1ll1l11_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢᇀ").format(kwname, bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᇁ")), str(bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇂ"))))
        bstack1lll11lllll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥᇃ").format(kwname, bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᇄ")))
        bstack1lll1l1111l_opy_ = error_message if bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᇅ")) else bstack1lll11lllll_opy_
        bstack1llll11111l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᇆ"): self.bstack1lll1lllll1_opy_[-1].get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᇇ"), bstack111ll1ll1l_opy_()),
            bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᇈ"): bstack1lll1l1111l_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇉ"): bstack1ll1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪᇊ") if bstack1llll1111l1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᇋ")) == bstack1ll1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫᇌ") else bstack1ll1l11_opy_ (u"ࠧࡊࡐࡉࡓࠬᇍ"),
            **bstack11l1l1l1_opy_.bstack1llll1111ll_opy_()
        }
        TestHubHandler.bstack1l11ll11l_opy_([bstack1llll11111l_opy_])
    def _1lll1l11lll_opy_(self):
        for bstack1lll11ll1ll_opy_ in reversed(self._1lll1l11l11_opy_):
            bstack1lll1l1ll11_opy_ = bstack1lll11ll1ll_opy_
            data = self._1lll1l11l11_opy_[bstack1lll11ll1ll_opy_][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᇎ")]
            if isinstance(data, bstack1llll111l11_opy_):
                if not bstack1ll1l11_opy_ (u"ࠩࡈࡅࡈࡎࠧᇏ") in data.bstack1lll1l1ll1l_opy_():
                    return bstack1lll1l1ll11_opy_
            else:
                return bstack1lll1l1ll11_opy_
    def _1lll1l111ll_opy_(self, messages):
        try:
            bstack1lll1llllll_opy_ = BuiltIn().get_variable_value(bstack1ll1l11_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤᇐ")) in (bstack1lll1l11l1l_opy_.DEBUG, bstack1lll1l11l1l_opy_.TRACE)
            for message, bstack1lll1ll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇑ"))
                level = message.get(bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᇒ"))
                if level == bstack1lll1l11l1l_opy_.FAIL:
                    self._1lll11lll1l_opy_ = name or self._1lll11lll1l_opy_
                    self._1lll11lll11_opy_ = bstack1lll1ll1l11_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᇓ")) if bstack1lll1llllll_opy_ and bstack1lll1ll1l11_opy_ else self._1lll11lll11_opy_
        except:
            pass
    @classmethod
    def bstack1llll11l111_opy_(self, event: str, bstack1lll11l1lll_opy_: bstack1lll1llll11_opy_, bstack1lll1l1l11l_opy_=False):
        if event == bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᇔ"):
            bstack1lll11l1lll_opy_.set(hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬᇕ")])
        if event == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᇖ"):
            event = bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᇗ")
        if bstack1lll1l1l11l_opy_:
            bstack1lll1llll1l_opy_ = {
                bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᇘ"): event,
                bstack1lll11l1lll_opy_.bstack1lll11l1l11_opy_(): bstack1lll11l1lll_opy_.bstack1lll11ll11l_opy_(event)
            }
            with self._lock:
                self.bstack1lll11ll1l1_opy_.append(bstack1lll1llll1l_opy_)
        else:
            TestHubHandler.bstack1llll11l111_opy_(event, bstack1lll11l1lll_opy_)
class bstack1lll11l1l1l_opy_:
    def __init__(self):
        self._1lll1lll11l_opy_ = []
    def bstack1lll1l111l1_opy_(self):
        self._1lll1lll11l_opy_.append([])
    def bstack1lll1l1l1ll_opy_(self):
        return self._1lll1lll11l_opy_.pop() if self._1lll1lll11l_opy_ else list()
    def push(self, message):
        self._1lll1lll11l_opy_[-1].append(message) if self._1lll1lll11l_opy_ else self._1lll1lll11l_opy_.append([message])
class bstack1lll1l11l1l_opy_:
    FAIL = bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪᇙ")
    ERROR = bstack1ll1l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᇚ")
    WARNING = bstack1ll1l11_opy_ (u"ࠧࡘࡃࡕࡒࠬᇛ")
    bstack1lll1ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᇜ")
    DEBUG = bstack1ll1l11_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨᇝ")
    TRACE = bstack1ll1l11_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩᇞ")
    bstack1llll111111_opy_ = [FAIL, ERROR]
def bstack1lll11ll111_opy_(bstack1lll1l1l111_opy_):
    if not bstack1lll1l1l111_opy_:
        return None
    if bstack1lll1l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᇟ"), None):
        return getattr(bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᇠ")], bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᇡ"), None)
    return bstack1lll1l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᇢ"), None)
def bstack1lll1l1lll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᇣ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᇤ")]:
        return
    if hook_type.lower() == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᇥ"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᇦ")
        else:
            return bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᇧ")
    elif hook_type.lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᇨ"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᇩ")
        else:
            return bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᇪ")