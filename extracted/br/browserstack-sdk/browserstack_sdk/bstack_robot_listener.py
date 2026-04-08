# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll1l1llll_opy_ import RobotHandler
from bstack_utils.capture import bstack1llll111l1l_opy_
from bstack_utils.bstack1llll1ll111_opy_ import bstack1lll11ll1ll_opy_, bstack1llll1l1l1l_opy_, bstack1llll1l1l11_opy_
from bstack_utils.bstack1l1l1111_opy_ import bstack111l1l1l11_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1llll11111_opy_, bstack1lllllllll_opy_, Result, \
    error_handler, bstack1lll11lll11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᄜ"): [],
        bstack111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬᄝ"): [],
        bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᄞ"): []
    }
    bstack1lll1lllll1_opy_ = []
    bstack1lll1lll1l1_opy_ = []
    @staticmethod
    def bstack1llll1111ll_opy_(log):
        if not ((isinstance(log[bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᄟ")], list) or (isinstance(log[bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᄠ")], dict)) and len(log[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄡ")])>0) or (isinstance(log[bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄢ")], str) and log[bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄣ")].strip())):
            return
        active = bstack111l1l1l11_opy_.bstack1llll1l1111_opy_()
        log = {
            bstack111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᄤ"): log[bstack111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᄥ")],
            bstack111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᄦ"): bstack1lll11lll11_opy_().isoformat() + bstack111l_opy_ (u"ࠩ࡝ࠫᄧ"),
            bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄨ"): log[bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄩ")],
        }
        if active:
            if active[bstack111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᄪ")] == bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᄫ"):
                log[bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᄬ")] = active[bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᄭ")]
            elif active[bstack111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᄮ")] == bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࠨᄯ"):
                log[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᄰ")] = active[bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᄱ")]
        TestHubHandler.bstack1llll11ll1_opy_([log])
    def __init__(self):
        self.messages = bstack1lll1l1ll1l_opy_()
        self._1lll1l11ll1_opy_ = None
        self._1lll11ll111_opy_ = None
        self._1llll1111l1_opy_ = OrderedDict()
        self.bstack1llll11l1ll_opy_ = bstack1llll111l1l_opy_(self.bstack1llll1111ll_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lll11l1l1l_opy_()
        if not self._1llll1111l1_opy_.get(attrs.get(bstack111l_opy_ (u"࠭ࡩࡥࠩᄲ")), None):
            self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"ࠧࡪࡦࠪᄳ"))] = {}
        bstack1lll1ll1ll1_opy_ = bstack1llll1l1l11_opy_(
                bstack1lll1l11111_opy_=attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫᄴ")),
                name=name,
                started_at=bstack1lllllllll_opy_(),
                file_path=os.path.relpath(attrs[bstack111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᄵ")], start=os.getcwd()) if attrs.get(bstack111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᄶ")) != bstack111l_opy_ (u"ࠫࠬᄷ") else bstack111l_opy_ (u"ࠬ࠭ᄸ"),
                framework=bstack111l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬᄹ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l_opy_ (u"ࠧࡪࡦࠪᄺ"), None)
        self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫᄻ"))][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄼ")] = bstack1lll1ll1ll1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll1lll111_opy_()
        self._1lll1ll1lll_opy_(messages)
        with self._lock:
            for bstack1lll11ll1l1_opy_ in self.bstack1lll1lllll1_opy_:
                bstack1lll11ll1l1_opy_[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᄽ")][bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᄾ")].extend(self.store[bstack111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᄿ")])
                TestHubHandler.bstack1ll1l11111_opy_(bstack1lll11ll1l1_opy_)
            self.bstack1lll1lllll1_opy_ = []
            self.store[bstack111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬᅀ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1llll11l1ll_opy_.start()
        if not self._1llll1111l1_opy_.get(attrs.get(bstack111l_opy_ (u"ࠧࡪࡦࠪᅁ")), None):
            self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫᅂ"))] = {}
        driver = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᅃ"), None)
        bstack1llll1ll111_opy_ = bstack1llll1l1l11_opy_(
            bstack1lll1l11111_opy_=attrs.get(bstack111l_opy_ (u"ࠪ࡭ࡩ࠭ᅄ")),
            name=name,
            started_at=bstack1lllllllll_opy_(),
            file_path=os.path.relpath(attrs[bstack111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᅅ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1ll1l11_opy_(attrs.get(bstack111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᅆ"), None)),
            framework=bstack111l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬᅇ"),
            tags=attrs[bstack111l_opy_ (u"ࠧࡵࡣࡪࡷࠬᅈ")],
            hooks=self.store[bstack111l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᅉ")],
            integrations=TestHubHandler.bstack1llll1l11l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦᅊ").format(bstack111l_opy_ (u"ࠥࠤࠧᅋ").join(attrs[bstack111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᅌ")]), name) if attrs[bstack111l_opy_ (u"ࠬࡺࡡࡨࡵࠪᅍ")] else name
        )
        self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"࠭ࡩࡥࠩᅎ"))][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᅏ")] = bstack1llll1ll111_opy_
        threading.current_thread().current_test_uuid = bstack1llll1ll111_opy_.bstack1llll111111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫᅐ"), None)
        self.bstack1llll1l1lll_opy_(bstack111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᅑ"), bstack1llll1ll111_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1llll11l1ll_opy_.reset()
        bstack1lll11lllll_opy_ = bstack1lll1llll11_opy_.get(attrs.get(bstack111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᅒ")), bstack111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᅓ"))
        self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"ࠬ࡯ࡤࠨᅔ"))][bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅕ")].stop(time=bstack1lllllllll_opy_(), duration=int(attrs.get(bstack111l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬᅖ"), bstack111l_opy_ (u"ࠨ࠲ࠪᅗ"))), result=Result(result=bstack1lll11lllll_opy_, exception=attrs.get(bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᅘ")), bstack1llll1l111l_opy_=[attrs.get(bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᅙ"))]))
        self.bstack1llll1l1lll_opy_(bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᅚ"), self._1llll1111l1_opy_[attrs.get(bstack111l_opy_ (u"ࠬ࡯ࡤࠨᅛ"))][bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᅜ")], True)
        with self._lock:
            self.store[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᅝ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lll11l1l1l_opy_()
        current_test_id = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪᅞ"), None)
        bstack1lll1lll11l_opy_ = current_test_id if bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫᅟ"), None) else bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᅠ"), None)
        if attrs.get(bstack111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᅡ"), bstack111l_opy_ (u"ࠬ࠭ᅢ")).lower() in [bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᅣ"), bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᅤ")]:
            hook_type = bstack1lll1l1l11l_opy_(attrs.get(bstack111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᅥ")), bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᅦ"), None))
            hook_name = bstack111l_opy_ (u"ࠪࡿࢂ࠭ᅧ").format(attrs.get(bstack111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᅨ"), bstack111l_opy_ (u"ࠬ࠭ᅩ")))
            if hook_type in [bstack111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᅪ"), bstack111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᅫ")]:
                hook_name = bstack111l_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩᅬ").format(bstack1lll1l1111l_opy_.get(hook_type), attrs.get(bstack111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᅭ"), bstack111l_opy_ (u"ࠪࠫᅮ")))
            bstack1lll11ll11l_opy_ = bstack1llll1l1l1l_opy_(
                bstack1lll1l11111_opy_=bstack1lll1lll11l_opy_ + bstack111l_opy_ (u"ࠫ࠲࠭ᅯ") + attrs.get(bstack111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᅰ"), bstack111l_opy_ (u"࠭ࠧᅱ")).lower(),
                name=hook_name,
                started_at=bstack1lllllllll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᅲ")), start=os.getcwd()),
                framework=bstack111l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅳ"),
                tags=attrs[bstack111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᅴ")],
                scope=RobotHandler.bstack1lll1ll1l11_opy_(attrs.get(bstack111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᅵ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lll11ll11l_opy_.bstack1llll111111_opy_()
            threading.current_thread().current_hook_id = bstack1lll1lll11l_opy_ + bstack111l_opy_ (u"ࠫ࠲࠭ᅶ") + attrs.get(bstack111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᅷ"), bstack111l_opy_ (u"࠭ࠧᅸ")).lower()
            with self._lock:
                self.store[bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᅹ")] = [bstack1lll11ll11l_opy_.bstack1llll111111_opy_()]
                if bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᅺ"), None):
                    self.store[bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᅻ")].append(bstack1lll11ll11l_opy_.bstack1llll111111_opy_())
                else:
                    self.store[bstack111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩᅼ")].append(bstack1lll11ll11l_opy_.bstack1llll111111_opy_())
            if bstack1lll1lll11l_opy_:
                self._1llll1111l1_opy_[bstack1lll1lll11l_opy_ + bstack111l_opy_ (u"ࠫ࠲࠭ᅽ") + attrs.get(bstack111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᅾ"), bstack111l_opy_ (u"࠭ࠧᅿ")).lower()] = { bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆀ"): bstack1lll11ll11l_opy_ }
            TestHubHandler.bstack1llll1l1lll_opy_(bstack111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᆁ"), bstack1lll11ll11l_opy_)
        else:
            bstack1llll11l11l_opy_ = {
                bstack111l_opy_ (u"ࠩ࡬ࡨࠬᆂ"): uuid4().__str__(),
                bstack111l_opy_ (u"ࠪࡸࡪࡾࡴࠨᆃ"): bstack111l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᆄ").format(attrs.get(bstack111l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᆅ")), attrs.get(bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᆆ"), bstack111l_opy_ (u"ࠧࠨᆇ"))) if attrs.get(bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆈ"), []) else attrs.get(bstack111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᆉ")),
                bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪᆊ"): attrs.get(bstack111l_opy_ (u"ࠫࡦࡸࡧࡴࠩᆋ"), []),
                bstack111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᆌ"): bstack1lllllllll_opy_(),
                bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᆍ"): bstack111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᆎ"),
                bstack111l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᆏ"): attrs.get(bstack111l_opy_ (u"ࠩࡧࡳࡨ࠭ᆐ"), bstack111l_opy_ (u"ࠪࠫᆑ"))
            }
            if attrs.get(bstack111l_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬᆒ"), bstack111l_opy_ (u"ࠬ࠭ᆓ")) != bstack111l_opy_ (u"࠭ࠧᆔ"):
                bstack1llll11l11l_opy_[bstack111l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᆕ")] = attrs.get(bstack111l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩᆖ"))
            if not self.bstack1lll1lll1l1_opy_:
                self._1llll1111l1_opy_[self._1lll1lll1ll_opy_()][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆗ")].add_step(bstack1llll11l11l_opy_)
                threading.current_thread().current_step_uuid = bstack1llll11l11l_opy_[bstack111l_opy_ (u"ࠪ࡭ࡩ࠭ᆘ")]
            self.bstack1lll1lll1l1_opy_.append(bstack1llll11l11l_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll1lll111_opy_()
        self._1lll1ll1lll_opy_(messages)
        current_test_id = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᆙ"), None)
        bstack1lll1lll11l_opy_ = current_test_id if current_test_id else bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᆚ"), None)
        bstack1lll1l1l111_opy_ = bstack1lll1llll11_opy_.get(attrs.get(bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᆛ")), bstack111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᆜ"))
        bstack1lll1l1lll1_opy_ = attrs.get(bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᆝ"))
        if bstack1lll1l1l111_opy_ != bstack111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᆞ") and not attrs.get(bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᆟ")) and self._1lll1l11ll1_opy_:
            bstack1lll1l1lll1_opy_ = self._1lll1l11ll1_opy_
        bstack1llll1l1ll1_opy_ = Result(result=bstack1lll1l1l111_opy_, exception=bstack1lll1l1lll1_opy_, bstack1llll1l111l_opy_=[bstack1lll1l1lll1_opy_])
        if attrs.get(bstack111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᆠ"), bstack111l_opy_ (u"ࠬ࠭ᆡ")).lower() in [bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᆢ"), bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᆣ")]:
            bstack1lll1lll11l_opy_ = current_test_id if current_test_id else bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫᆤ"), None)
            if bstack1lll1lll11l_opy_:
                bstack1llll11l1l1_opy_ = bstack1lll1lll11l_opy_ + bstack111l_opy_ (u"ࠤ࠰ࠦᆥ") + attrs.get(bstack111l_opy_ (u"ࠪࡸࡾࡶࡥࠨᆦ"), bstack111l_opy_ (u"ࠫࠬᆧ")).lower()
                self._1llll1111l1_opy_[bstack1llll11l1l1_opy_][bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᆨ")].stop(time=bstack1lllllllll_opy_(), duration=int(attrs.get(bstack111l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᆩ"), bstack111l_opy_ (u"ࠧ࠱ࠩᆪ"))), result=bstack1llll1l1ll1_opy_)
                TestHubHandler.bstack1llll1l1lll_opy_(bstack111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᆫ"), self._1llll1111l1_opy_[bstack1llll11l1l1_opy_][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆬ")])
        else:
            bstack1lll1lll11l_opy_ = current_test_id if current_test_id else bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬᆭ"), None)
            if bstack1lll1lll11l_opy_ and len(self.bstack1lll1lll1l1_opy_) == 1:
                current_step_uuid = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨᆮ"), None)
                self._1llll1111l1_opy_[bstack1lll1lll11l_opy_][bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᆯ")].bstack1llll111lll_opy_(current_step_uuid, duration=int(attrs.get(bstack111l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᆰ"), bstack111l_opy_ (u"ࠧ࠱ࠩᆱ"))), result=bstack1llll1l1ll1_opy_)
            else:
                self.bstack1lll1l111l1_opy_(attrs)
            self.bstack1lll1lll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l_opy_ (u"ࠨࡪࡷࡱࡱ࠭ᆲ"), bstack111l_opy_ (u"ࠩࡱࡳࠬᆳ")) == bstack111l_opy_ (u"ࠪࡽࡪࡹࠧᆴ"):
                return
            self.messages.push(message)
            logs = []
            if bstack111l1l1l11_opy_.bstack1llll1l1111_opy_():
                logs.append({
                    bstack111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᆵ"): bstack1lllllllll_opy_(),
                    bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆶ"): message.get(bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆷ")),
                    bstack111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᆸ"): message.get(bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᆹ")),
                    **bstack111l1l1l11_opy_.bstack1llll1l1111_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1llll11ll1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll1ll111l_opy_()
    def bstack1lll1l111l1_opy_(self, bstack1lll11l1l11_opy_):
        if not bstack111l1l1l11_opy_.bstack1llll1l1111_opy_():
            return
        kwname = bstack111l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨᆺ").format(bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᆻ")), bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠫࡦࡸࡧࡴࠩᆼ"), bstack111l_opy_ (u"ࠬ࠭ᆽ"))) if bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᆾ"), []) else bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᆿ"))
        error_message = bstack111l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢᇀ").format(kwname, bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᇁ")), str(bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇂ"))))
        bstack1lll11llll1_opy_ = bstack111l_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥᇃ").format(kwname, bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᇄ")))
        bstack1lll1l111ll_opy_ = error_message if bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᇅ")) else bstack1lll11llll1_opy_
        bstack1lll1ll1l1l_opy_ = {
            bstack111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᇆ"): self.bstack1lll1lll1l1_opy_[-1].get(bstack111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᇇ"), bstack1lllllllll_opy_()),
            bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᇈ"): bstack1lll1l111ll_opy_,
            bstack111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇉ"): bstack111l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪᇊ") if bstack1lll11l1l11_opy_.get(bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᇋ")) == bstack111l_opy_ (u"࠭ࡆࡂࡋࡏࠫᇌ") else bstack111l_opy_ (u"ࠧࡊࡐࡉࡓࠬᇍ"),
            **bstack111l1l1l11_opy_.bstack1llll1l1111_opy_()
        }
        TestHubHandler.bstack1llll11ll1_opy_([bstack1lll1ll1l1l_opy_])
    def _1lll1lll1ll_opy_(self):
        for bstack1lll1l11111_opy_ in reversed(self._1llll1111l1_opy_):
            bstack1lll1ll11ll_opy_ = bstack1lll1l11111_opy_
            data = self._1llll1111l1_opy_[bstack1lll1l11111_opy_][bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᇎ")]
            if isinstance(data, bstack1llll1l1l1l_opy_):
                if not bstack111l_opy_ (u"ࠩࡈࡅࡈࡎࠧᇏ") in data.bstack1lll1l1l1ll_opy_():
                    return bstack1lll1ll11ll_opy_
            else:
                return bstack1lll1ll11ll_opy_
    def _1lll1ll1lll_opy_(self, messages):
        try:
            bstack1lll11lll1l_opy_ = BuiltIn().get_variable_value(bstack111l_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤᇐ")) in (bstack1lll1l11l11_opy_.DEBUG, bstack1lll1l11l11_opy_.TRACE)
            for message, bstack1llll11111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇑ"))
                level = message.get(bstack111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᇒ"))
                if level == bstack1lll1l11l11_opy_.FAIL:
                    self._1lll1l11ll1_opy_ = name or self._1lll1l11ll1_opy_
                    self._1lll11ll111_opy_ = bstack1llll11111l_opy_.get(bstack111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᇓ")) if bstack1lll11lll1l_opy_ and bstack1llll11111l_opy_ else self._1lll11ll111_opy_
        except:
            pass
    @classmethod
    def bstack1llll1l1lll_opy_(self, event: str, bstack1lll1l11l1l_opy_: bstack1lll11ll1ll_opy_, bstack1lll1ll11l1_opy_=False):
        if event == bstack111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᇔ"):
            bstack1lll1l11l1l_opy_.set(hooks=self.store[bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬᇕ")])
        if event == bstack111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᇖ"):
            event = bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᇗ")
        if bstack1lll1ll11l1_opy_:
            bstack1lll1l11lll_opy_ = {
                bstack111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᇘ"): event,
                bstack1lll1l11l1l_opy_.bstack1lll1llllll_opy_(): bstack1lll1l11l1l_opy_.bstack1lll1l1l1l1_opy_(event)
            }
            with self._lock:
                self.bstack1lll1lllll1_opy_.append(bstack1lll1l11lll_opy_)
        else:
            TestHubHandler.bstack1llll1l1lll_opy_(event, bstack1lll1l11l1l_opy_)
class bstack1lll1l1ll1l_opy_:
    def __init__(self):
        self._1lll1llll1l_opy_ = []
    def bstack1lll11l1l1l_opy_(self):
        self._1lll1llll1l_opy_.append([])
    def bstack1lll1lll111_opy_(self):
        return self._1lll1llll1l_opy_.pop() if self._1lll1llll1l_opy_ else list()
    def push(self, message):
        self._1lll1llll1l_opy_[-1].append(message) if self._1lll1llll1l_opy_ else self._1lll1llll1l_opy_.append([message])
class bstack1lll1l11l11_opy_:
    FAIL = bstack111l_opy_ (u"ࠬࡌࡁࡊࡎࠪᇙ")
    ERROR = bstack111l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᇚ")
    WARNING = bstack111l_opy_ (u"ࠧࡘࡃࡕࡒࠬᇛ")
    bstack1lll11l1lll_opy_ = bstack111l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᇜ")
    DEBUG = bstack111l_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨᇝ")
    TRACE = bstack111l_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩᇞ")
    bstack1lll11l1ll1_opy_ = [FAIL, ERROR]
def bstack1lll1ll1111_opy_(bstack1lll1l1ll11_opy_):
    if not bstack1lll1l1ll11_opy_:
        return None
    if bstack1lll1l1ll11_opy_.get(bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᇟ"), None):
        return getattr(bstack1lll1l1ll11_opy_[bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᇠ")], bstack111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᇡ"), None)
    return bstack1lll1l1ll11_opy_.get(bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᇢ"), None)
def bstack1lll1l1l11l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᇣ"), bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᇤ")]:
        return
    if hook_type.lower() == bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᇥ"):
        if current_test_uuid is None:
            return bstack111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᇦ")
        else:
            return bstack111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᇧ")
    elif hook_type.lower() == bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᇨ"):
        if current_test_uuid is None:
            return bstack111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᇩ")
        else:
            return bstack111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᇪ")