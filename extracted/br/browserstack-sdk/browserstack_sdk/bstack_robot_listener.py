# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll1lll111_opy_ import RobotHandler
from bstack_utils.capture import bstack1llll11l11l_opy_
from bstack_utils.bstack1llll1l11ll_opy_ import bstack1lll1llllll_opy_, bstack1llll11l1ll_opy_, bstack1llll1111l1_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll1l1ll_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l111l11l_opy_, bstack111111l1l_opy_, Result, \
    error_handler, bstack1lll11ll11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᄳ"): [],
        bstack1l111l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᄴ"): [],
        bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᄵ"): []
    }
    bstack1lll1ll1l11_opy_ = []
    bstack1lll1lll1l1_opy_ = []
    @staticmethod
    def bstack1llll11ll11_opy_(log):
        if not ((isinstance(log[bstack1l111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᄶ")], list) or (isinstance(log[bstack1l111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄷ")], dict)) and len(log[bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄸ")])>0) or (isinstance(log[bstack1l111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄹ")], str) and log[bstack1l111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᄺ")].strip())):
            return
        active = bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_()
        log = {
            bstack1l111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᄻ"): log[bstack1l111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᄼ")],
            bstack1l111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᄽ"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠫ࡟࠭ᄾ"),
            bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄿ"): log[bstack1l111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅀ")],
        }
        if active:
            if active[bstack1l111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᅁ")] == bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᅂ"):
                log[bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᅃ")] = active[bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᅄ")]
            elif active[bstack1l111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᅅ")] == bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࠪᅆ"):
                log[bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᅇ")] = active[bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᅈ")]
        TestHubHandler.bstack1ll111l11_opy_([log])
    def __init__(self):
        self.messages = bstack1lll11l1lll_opy_()
        self._1lll1l1l1ll_opy_ = None
        self._1lll11lllll_opy_ = None
        self._1lll1ll11l1_opy_ = OrderedDict()
        self.bstack1llll111l1l_opy_ = bstack1llll11l11l_opy_(self.bstack1llll11ll11_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lll11lll11_opy_()
        if not self._1lll1ll11l1_opy_.get(attrs.get(bstack1l111l_opy_ (u"ࠨ࡫ࡧࠫᅉ")), None):
            self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠩ࡬ࡨࠬᅊ"))] = {}
        bstack1lll1l111l1_opy_ = bstack1llll1111l1_opy_(
                bstack1lll1l1111l_opy_=attrs.get(bstack1l111l_opy_ (u"ࠪ࡭ࡩ࠭ᅋ")),
                name=name,
                started_at=bstack111111l1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1l111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᅌ")], start=os.getcwd()) if attrs.get(bstack1l111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᅍ")) != bstack1l111l_opy_ (u"࠭ࠧᅎ") else bstack1l111l_opy_ (u"ࠧࠨᅏ"),
                framework=bstack1l111l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅐ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l111l_opy_ (u"ࠩ࡬ࡨࠬᅑ"), None)
        self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠪ࡭ࡩ࠭ᅒ"))][bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᅓ")] = bstack1lll1l111l1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll1ll11ll_opy_()
        self._1lll1ll111l_opy_(messages)
        with self._lock:
            for bstack1lll1lll11l_opy_ in self.bstack1lll1ll1l11_opy_:
                bstack1lll1lll11l_opy_[bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᅔ")][bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᅕ")].extend(self.store[bstack1l111l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ᅖ")])
                TestHubHandler.bstack1ll1lll11l_opy_(bstack1lll1lll11l_opy_)
            self.bstack1lll1ll1l11_opy_ = []
            self.store[bstack1l111l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᅗ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1llll111l1l_opy_.start()
        if not self._1lll1ll11l1_opy_.get(attrs.get(bstack1l111l_opy_ (u"ࠩ࡬ࡨࠬᅘ")), None):
            self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠪ࡭ࡩ࠭ᅙ"))] = {}
        driver = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᅚ"), None)
        bstack1llll1l11ll_opy_ = bstack1llll1111l1_opy_(
            bstack1lll1l1111l_opy_=attrs.get(bstack1l111l_opy_ (u"ࠬ࡯ࡤࠨᅛ")),
            name=name,
            started_at=bstack111111l1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1l111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᅜ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1l1l1l1_opy_(attrs.get(bstack1l111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᅝ"), None)),
            framework=bstack1l111l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅞ"),
            tags=attrs[bstack1l111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᅟ")],
            hooks=self.store[bstack1l111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩᅠ")],
            integrations=TestHubHandler.bstack1llll11l1l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l111l_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨᅡ").format(bstack1l111l_opy_ (u"ࠧࠦࠢᅢ").join(attrs[bstack1l111l_opy_ (u"࠭ࡴࡢࡩࡶࠫᅣ")]), name) if attrs[bstack1l111l_opy_ (u"ࠧࡵࡣࡪࡷࠬᅤ")] else name
        )
        self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠨ࡫ࡧࠫᅥ"))][bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᅦ")] = bstack1llll1l11ll_opy_
        threading.current_thread().current_test_uuid = bstack1llll1l11ll_opy_.bstack1lll1ll1l1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l111l_opy_ (u"ࠪ࡭ࡩ࠭ᅧ"), None)
        self.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᅨ"), bstack1llll1l11ll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1llll111l1l_opy_.reset()
        bstack1lll1lll1ll_opy_ = bstack1lll11ll1ll_opy_.get(attrs.get(bstack1l111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᅩ")), bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᅪ"))
        self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠧࡪࡦࠪᅫ"))][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅬ")].stop(time=bstack111111l1l_opy_(), duration=int(attrs.get(bstack1l111l_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧᅭ"), bstack1l111l_opy_ (u"ࠪ࠴ࠬᅮ"))), result=Result(result=bstack1lll1lll1ll_opy_, exception=attrs.get(bstack1l111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅯ")), bstack1llll1l111l_opy_=[attrs.get(bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅰ"))]))
        self.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᅱ"), self._1lll1ll11l1_opy_[attrs.get(bstack1l111l_opy_ (u"ࠧࡪࡦࠪᅲ"))][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅳ")], True)
        with self._lock:
            self.store[bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᅴ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lll11lll11_opy_()
        current_test_id = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᅵ"), None)
        bstack1lll1ll1ll1_opy_ = current_test_id if bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᅶ"), None) else bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᅷ"), None)
        if attrs.get(bstack1l111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᅸ"), bstack1l111l_opy_ (u"ࠧࠨᅹ")).lower() in [bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᅺ"), bstack1l111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᅻ")]:
            hook_type = bstack1lll11lll1l_opy_(attrs.get(bstack1l111l_opy_ (u"ࠪࡸࡾࡶࡥࠨᅼ")), bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᅽ"), None))
            hook_name = bstack1l111l_opy_ (u"ࠬࢁࡽࠨᅾ").format(attrs.get(bstack1l111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᅿ"), bstack1l111l_opy_ (u"ࠧࠨᆀ")))
            if hook_type in [bstack1l111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᆁ"), bstack1l111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᆂ")]:
                hook_name = bstack1l111l_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫᆃ").format(bstack1lll1l1ll11_opy_.get(hook_type), attrs.get(bstack1l111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᆄ"), bstack1l111l_opy_ (u"ࠬ࠭ᆅ")))
            bstack1lll1l1ll1l_opy_ = bstack1llll11l1ll_opy_(
                bstack1lll1l1111l_opy_=bstack1lll1ll1ll1_opy_ + bstack1l111l_opy_ (u"࠭࠭ࠨᆆ") + attrs.get(bstack1l111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᆇ"), bstack1l111l_opy_ (u"ࠨࠩᆈ")).lower(),
                name=hook_name,
                started_at=bstack111111l1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᆉ")), start=os.getcwd()),
                framework=bstack1l111l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩᆊ"),
                tags=attrs[bstack1l111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᆋ")],
                scope=RobotHandler.bstack1lll1l1l1l1_opy_(attrs.get(bstack1l111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᆌ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_()
            threading.current_thread().current_hook_id = bstack1lll1ll1ll1_opy_ + bstack1l111l_opy_ (u"࠭࠭ࠨᆍ") + attrs.get(bstack1l111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᆎ"), bstack1l111l_opy_ (u"ࠨࠩᆏ")).lower()
            with self._lock:
                self.store[bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᆐ")] = [bstack1lll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_()]
                if bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᆑ"), None):
                    self.store[bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨᆒ")].append(bstack1lll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_())
                else:
                    self.store[bstack1l111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᆓ")].append(bstack1lll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_())
            if bstack1lll1ll1ll1_opy_:
                self._1lll1ll11l1_opy_[bstack1lll1ll1ll1_opy_ + bstack1l111l_opy_ (u"࠭࠭ࠨᆔ") + attrs.get(bstack1l111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᆕ"), bstack1l111l_opy_ (u"ࠨࠩᆖ")).lower()] = { bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆗ"): bstack1lll1l1ll1l_opy_ }
            TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᆘ"), bstack1lll1l1ll1l_opy_)
        else:
            bstack1llll1111ll_opy_ = {
                bstack1l111l_opy_ (u"ࠫ࡮ࡪࠧᆙ"): uuid4().__str__(),
                bstack1l111l_opy_ (u"ࠬࡺࡥࡹࡶࠪᆚ"): bstack1l111l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬᆛ").format(attrs.get(bstack1l111l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᆜ")), attrs.get(bstack1l111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆝ"), bstack1l111l_opy_ (u"ࠩࠪᆞ"))) if attrs.get(bstack1l111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᆟ"), []) else attrs.get(bstack1l111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᆠ")),
                bstack1l111l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᆡ"): attrs.get(bstack1l111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᆢ"), []),
                bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᆣ"): bstack111111l1l_opy_(),
                bstack1l111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᆤ"): bstack1l111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᆥ"),
                bstack1l111l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᆦ"): attrs.get(bstack1l111l_opy_ (u"ࠫࡩࡵࡣࠨᆧ"), bstack1l111l_opy_ (u"ࠬ࠭ᆨ"))
            }
            if attrs.get(bstack1l111l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧᆩ"), bstack1l111l_opy_ (u"ࠧࠨᆪ")) != bstack1l111l_opy_ (u"ࠨࠩᆫ"):
                bstack1llll1111ll_opy_[bstack1l111l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᆬ")] = attrs.get(bstack1l111l_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫᆭ"))
            if not self.bstack1lll1lll1l1_opy_:
                self._1lll1ll11l1_opy_[self._1lll1l1llll_opy_()][bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆮ")].add_step(bstack1llll1111ll_opy_)
                threading.current_thread().current_step_uuid = bstack1llll1111ll_opy_[bstack1l111l_opy_ (u"ࠬ࡯ࡤࠨᆯ")]
            self.bstack1lll1lll1l1_opy_.append(bstack1llll1111ll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll1ll11ll_opy_()
        self._1lll1ll111l_opy_(messages)
        current_test_id = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᆰ"), None)
        bstack1lll1ll1ll1_opy_ = current_test_id if current_test_id else bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪᆱ"), None)
        bstack1lll11llll1_opy_ = bstack1lll11ll1ll_opy_.get(attrs.get(bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᆲ")), bstack1l111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᆳ"))
        bstack1lll11l1l1l_opy_ = attrs.get(bstack1l111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᆴ"))
        if bstack1lll11llll1_opy_ != bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᆵ") and not attrs.get(bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆶ")) and self._1lll1l1l1ll_opy_:
            bstack1lll11l1l1l_opy_ = self._1lll1l1l1ll_opy_
        bstack1llll11l111_opy_ = Result(result=bstack1lll11llll1_opy_, exception=bstack1lll11l1l1l_opy_, bstack1llll1l111l_opy_=[bstack1lll11l1l1l_opy_])
        if attrs.get(bstack1l111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᆷ"), bstack1l111l_opy_ (u"ࠧࠨᆸ")).lower() in [bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᆹ"), bstack1l111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᆺ")]:
            bstack1lll1ll1ll1_opy_ = current_test_id if current_test_id else bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᆻ"), None)
            if bstack1lll1ll1ll1_opy_:
                bstack1llll11111l_opy_ = bstack1lll1ll1ll1_opy_ + bstack1l111l_opy_ (u"ࠦ࠲ࠨᆼ") + attrs.get(bstack1l111l_opy_ (u"ࠬࡺࡹࡱࡧࠪᆽ"), bstack1l111l_opy_ (u"࠭ࠧᆾ")).lower()
                self._1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᆿ")].stop(time=bstack111111l1l_opy_(), duration=int(attrs.get(bstack1l111l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᇀ"), bstack1l111l_opy_ (u"ࠩ࠳ࠫᇁ"))), result=bstack1llll11l111_opy_)
                TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᇂ"), self._1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᇃ")])
        else:
            bstack1lll1ll1ll1_opy_ = current_test_id if current_test_id else bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧᇄ"), None)
            if bstack1lll1ll1ll1_opy_ and len(self.bstack1lll1lll1l1_opy_) == 1:
                current_step_uuid = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪᇅ"), None)
                self._1lll1ll11l1_opy_[bstack1lll1ll1ll1_opy_][bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᇆ")].bstack1llll1l1l11_opy_(current_step_uuid, duration=int(attrs.get(bstack1l111l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᇇ"), bstack1l111l_opy_ (u"ࠩ࠳ࠫᇈ"))), result=bstack1llll11l111_opy_)
            else:
                self.bstack1lll11l11ll_opy_(attrs)
            self.bstack1lll1lll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l111l_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨᇉ"), bstack1l111l_opy_ (u"ࠫࡳࡵࠧᇊ")) == bstack1l111l_opy_ (u"ࠬࡿࡥࡴࠩᇋ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_():
                logs.append({
                    bstack1l111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᇌ"): bstack111111l1l_opy_(),
                    bstack1l111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᇍ"): message.get(bstack1l111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇎ")),
                    bstack1l111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᇏ"): message.get(bstack1l111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇐ")),
                    **bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1ll111l11_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll1l1lll1_opy_()
    def bstack1lll11l11ll_opy_(self, bstack1lll1l111ll_opy_):
        if not bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_():
            return
        kwname = bstack1l111l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᇑ").format(bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᇒ")), bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᇓ"), bstack1l111l_opy_ (u"ࠧࠨᇔ"))) if bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᇕ"), []) else bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᇖ"))
        error_message = bstack1l111l_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤᇗ").format(kwname, bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᇘ")), str(bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᇙ"))))
        bstack1lll1l1l11l_opy_ = bstack1l111l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧᇚ").format(kwname, bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᇛ")))
        bstack1lll1ll1111_opy_ = error_message if bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇜ")) else bstack1lll1l1l11l_opy_
        bstack1lll1ll1lll_opy_ = {
            bstack1l111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᇝ"): self.bstack1lll1lll1l1_opy_[-1].get(bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᇞ"), bstack111111l1l_opy_()),
            bstack1l111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇟ"): bstack1lll1ll1111_opy_,
            bstack1l111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᇠ"): bstack1l111l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᇡ") if bstack1lll1l111ll_opy_.get(bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᇢ")) == bstack1l111l_opy_ (u"ࠨࡈࡄࡍࡑ࠭ᇣ") else bstack1l111l_opy_ (u"ࠩࡌࡒࡋࡕࠧᇤ"),
            **bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_()
        }
        TestHubHandler.bstack1ll111l11_opy_([bstack1lll1ll1lll_opy_])
    def _1lll1l1llll_opy_(self):
        for bstack1lll1l1111l_opy_ in reversed(self._1lll1ll11l1_opy_):
            bstack1lll1lllll1_opy_ = bstack1lll1l1111l_opy_
            data = self._1lll1ll11l1_opy_[bstack1lll1l1111l_opy_][bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᇥ")]
            if isinstance(data, bstack1llll11l1ll_opy_):
                if not bstack1l111l_opy_ (u"ࠫࡊࡇࡃࡉࠩᇦ") in data.bstack1lll11l1ll1_opy_():
                    return bstack1lll1lllll1_opy_
            else:
                return bstack1lll1lllll1_opy_
    def _1lll1ll111l_opy_(self, messages):
        try:
            bstack1lll1l1l111_opy_ = BuiltIn().get_variable_value(bstack1l111l_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦᇧ")) in (bstack1lll11ll111_opy_.DEBUG, bstack1lll11ll111_opy_.TRACE)
            for message, bstack1lll11ll1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᇨ"))
                level = message.get(bstack1l111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇩ"))
                if level == bstack1lll11ll111_opy_.FAIL:
                    self._1lll1l1l1ll_opy_ = name or self._1lll1l1l1ll_opy_
                    self._1lll11lllll_opy_ = bstack1lll11ll1l1_opy_.get(bstack1l111l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᇪ")) if bstack1lll1l1l111_opy_ and bstack1lll11ll1l1_opy_ else self._1lll11lllll_opy_
        except:
            pass
    @classmethod
    def bstack1llll1l1111_opy_(self, event: str, bstack1lll11l11l1_opy_: bstack1lll1llllll_opy_, bstack1lll1l11l11_opy_=False):
        if event == bstack1l111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᇫ"):
            bstack1lll11l11l1_opy_.set(hooks=self.store[bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧᇬ")])
        if event == bstack1l111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᇭ"):
            event = bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᇮ")
        if bstack1lll1l11l11_opy_:
            bstack1lll1l11lll_opy_ = {
                bstack1l111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᇯ"): event,
                bstack1lll11l11l1_opy_.bstack1lll1llll1l_opy_(): bstack1lll11l11l1_opy_.bstack1lll11l1l11_opy_(event)
            }
            with self._lock:
                self.bstack1lll1ll1l11_opy_.append(bstack1lll1l11lll_opy_)
        else:
            TestHubHandler.bstack1llll1l1111_opy_(event, bstack1lll11l11l1_opy_)
class bstack1lll11l1lll_opy_:
    def __init__(self):
        self._1lll1l11ll1_opy_ = []
    def bstack1lll11lll11_opy_(self):
        self._1lll1l11ll1_opy_.append([])
    def bstack1lll1ll11ll_opy_(self):
        return self._1lll1l11ll1_opy_.pop() if self._1lll1l11ll1_opy_ else list()
    def push(self, message):
        self._1lll1l11ll1_opy_[-1].append(message) if self._1lll1l11ll1_opy_ else self._1lll1l11ll1_opy_.append([message])
class bstack1lll11ll111_opy_:
    FAIL = bstack1l111l_opy_ (u"ࠧࡇࡃࡌࡐࠬᇰ")
    ERROR = bstack1l111l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧᇱ")
    WARNING = bstack1l111l_opy_ (u"࡚ࠩࡅࡗࡔࠧᇲ")
    bstack1lll1l11l1l_opy_ = bstack1l111l_opy_ (u"ࠪࡍࡓࡌࡏࠨᇳ")
    DEBUG = bstack1l111l_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪᇴ")
    TRACE = bstack1l111l_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫᇵ")
    bstack1lll11l111l_opy_ = [FAIL, ERROR]
def bstack1lll1l11111_opy_(bstack1lll1llll11_opy_):
    if not bstack1lll1llll11_opy_:
        return None
    if bstack1lll1llll11_opy_.get(bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᇶ"), None):
        return getattr(bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᇷ")], bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇸ"), None)
    return bstack1lll1llll11_opy_.get(bstack1l111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᇹ"), None)
def bstack1lll11lll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᇺ"), bstack1l111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᇻ")]:
        return
    if hook_type.lower() == bstack1l111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᇼ"):
        if current_test_uuid is None:
            return bstack1l111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᇽ")
        else:
            return bstack1l111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᇾ")
    elif hook_type.lower() == bstack1l111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᇿ"):
        if current_test_uuid is None:
            return bstack1l111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬሀ")
        else:
            return bstack1l111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧሁ")