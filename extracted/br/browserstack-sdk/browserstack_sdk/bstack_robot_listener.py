# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1lll11lll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1llll11111l_opy_
from bstack_utils.bstack1lll1lllll1_opy_ import bstack1lll1ll11l1_opy_, bstack1llll111111_opy_, bstack1llll11l1ll_opy_
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11l1ll1_opy_, bstack1111l1l1l_opy_, Result, \
    error_handler, bstack1lll11ll11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᅁ"): [],
        bstack111ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᅂ"): [],
        bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᅃ"): []
    }
    bstack1lll111lll1_opy_ = []
    bstack1lll11ll111_opy_ = []
    @staticmethod
    def bstack1llll11l111_opy_(log):
        if not ((isinstance(log[bstack111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᅄ")], list) or (isinstance(log[bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅅ")], dict)) and len(log[bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅆ")])>0) or (isinstance(log[bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅇ")], str) and log[bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅈ")].strip())):
            return
        active = bstack111ll111_opy_.bstack1llll111l1l_opy_()
        log = {
            bstack111ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᅉ"): log[bstack111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᅊ")],
            bstack111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᅋ"): bstack1lll11ll11l_opy_().isoformat() + bstack111ll_opy_ (u"ࠫ࡟࠭ᅌ"),
            bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅍ"): log[bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅎ")],
        }
        if active:
            if active[bstack111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᅏ")] == bstack111ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᅐ"):
                log[bstack111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᅑ")] = active[bstack111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᅒ")]
            elif active[bstack111ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᅓ")] == bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࠪᅔ"):
                log[bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᅕ")] = active[bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᅖ")]
        TestHubHandler.bstack1lllll1l1_opy_([log])
    def __init__(self):
        self.messages = bstack1lll1ll1111_opy_()
        self._1lll11l1l11_opy_ = None
        self._1lll11l1lll_opy_ = None
        self._1lll1l1111l_opy_ = OrderedDict()
        self.bstack1lll1llll1l_opy_ = bstack1llll11111l_opy_(self.bstack1llll11l111_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lll1l1lll1_opy_()
        if not self._1lll1l1111l_opy_.get(attrs.get(bstack111ll_opy_ (u"ࠨ࡫ࡧࠫᅗ")), None):
            self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠩ࡬ࡨࠬᅘ"))] = {}
        bstack1lll11ll1l1_opy_ = bstack1llll11l1ll_opy_(
                bstack1lll1l111l1_opy_=attrs.get(bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭ᅙ")),
                name=name,
                started_at=bstack1111l1l1l_opy_(),
                file_path=os.path.relpath(attrs[bstack111ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᅚ")], start=os.getcwd()) if attrs.get(bstack111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᅛ")) != bstack111ll_opy_ (u"࠭ࠧᅜ") else bstack111ll_opy_ (u"ࠧࠨᅝ"),
                framework=bstack111ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅞ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111ll_opy_ (u"ࠩ࡬ࡨࠬᅟ"), None)
        self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭ᅠ"))][bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᅡ")] = bstack1lll11ll1l1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll1l1l11l_opy_()
        self._1lll111llll_opy_(messages)
        with self._lock:
            for bstack1lll1ll11ll_opy_ in self.bstack1lll111lll1_opy_:
                bstack1lll1ll11ll_opy_[bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᅢ")][bstack111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᅣ")].extend(self.store[bstack111ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ᅤ")])
                TestHubHandler.bstack11lll1l11l_opy_(bstack1lll1ll11ll_opy_)
            self.bstack1lll111lll1_opy_ = []
            self.store[bstack111ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧᅥ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lll1llll1l_opy_.start()
        if not self._1lll1l1111l_opy_.get(attrs.get(bstack111ll_opy_ (u"ࠩ࡬ࡨࠬᅦ")), None):
            self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭ᅧ"))] = {}
        driver = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᅨ"), None)
        bstack1lll1lllll1_opy_ = bstack1llll11l1ll_opy_(
            bstack1lll1l111l1_opy_=attrs.get(bstack111ll_opy_ (u"ࠬ࡯ࡤࠨᅩ")),
            name=name,
            started_at=bstack1111l1l1l_opy_(),
            file_path=os.path.relpath(attrs[bstack111ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᅪ")], start=os.getcwd()),
            scope=RobotHandler.bstack1lll1l1l1l1_opy_(attrs.get(bstack111ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᅫ"), None)),
            framework=bstack111ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧᅬ"),
            tags=attrs[bstack111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᅭ")],
            hooks=self.store[bstack111ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩᅮ")],
            integrations=TestHubHandler.bstack1llll11lll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111ll_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨᅯ").format(bstack111ll_opy_ (u"ࠧࠦࠢᅰ").join(attrs[bstack111ll_opy_ (u"࠭ࡴࡢࡩࡶࠫᅱ")]), name) if attrs[bstack111ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᅲ")] else name
        )
        self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠨ࡫ࡧࠫᅳ"))][bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᅴ")] = bstack1lll1lllll1_opy_
        threading.current_thread().current_test_uuid = bstack1lll1lllll1_opy_.bstack1lll11l1111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭ᅵ"), None)
        self.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᅶ"), bstack1lll1lllll1_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lll1llll1l_opy_.reset()
        bstack1lll1l1l111_opy_ = bstack1lll11l11l1_opy_.get(attrs.get(bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᅷ")), bstack111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᅸ"))
        self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠧࡪࡦࠪᅹ"))][bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᅺ")].stop(time=bstack1111l1l1l_opy_(), duration=int(attrs.get(bstack111ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧᅻ"), bstack111ll_opy_ (u"ࠪ࠴ࠬᅼ"))), result=Result(result=bstack1lll1l1l111_opy_, exception=attrs.get(bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅽ")), bstack1llll1l111l_opy_=[attrs.get(bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅾ"))]))
        self.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᅿ"), self._1lll1l1111l_opy_[attrs.get(bstack111ll_opy_ (u"ࠧࡪࡦࠪᆀ"))][bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᆁ")], True)
        with self._lock:
            self.store[bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ᆂ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lll1l1lll1_opy_()
        current_test_id = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᆃ"), None)
        bstack1lll1l11111_opy_ = current_test_id if bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᆄ"), None) else bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨᆅ"), None)
        if attrs.get(bstack111ll_opy_ (u"࠭ࡴࡺࡲࡨࠫᆆ"), bstack111ll_opy_ (u"ࠧࠨᆇ")).lower() in [bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᆈ"), bstack111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᆉ")]:
            hook_type = bstack1lll11l1l1l_opy_(attrs.get(bstack111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᆊ")), bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᆋ"), None))
            hook_name = bstack111ll_opy_ (u"ࠬࢁࡽࠨᆌ").format(attrs.get(bstack111ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᆍ"), bstack111ll_opy_ (u"ࠧࠨᆎ")))
            if hook_type in [bstack111ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᆏ"), bstack111ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᆐ")]:
                hook_name = bstack111ll_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫᆑ").format(bstack1lll1l1l1ll_opy_.get(hook_type), attrs.get(bstack111ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᆒ"), bstack111ll_opy_ (u"ࠬ࠭ᆓ")))
            bstack1lll11llll1_opy_ = bstack1llll111111_opy_(
                bstack1lll1l111l1_opy_=bstack1lll1l11111_opy_ + bstack111ll_opy_ (u"࠭࠭ࠨᆔ") + attrs.get(bstack111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᆕ"), bstack111ll_opy_ (u"ࠨࠩᆖ")).lower(),
                name=hook_name,
                started_at=bstack1111l1l1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᆗ")), start=os.getcwd()),
                framework=bstack111ll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩᆘ"),
                tags=attrs[bstack111ll_opy_ (u"ࠫࡹࡧࡧࡴࠩᆙ")],
                scope=RobotHandler.bstack1lll1l1l1l1_opy_(attrs.get(bstack111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᆚ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lll11llll1_opy_.bstack1lll11l1111_opy_()
            threading.current_thread().current_hook_id = bstack1lll1l11111_opy_ + bstack111ll_opy_ (u"࠭࠭ࠨᆛ") + attrs.get(bstack111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᆜ"), bstack111ll_opy_ (u"ࠨࠩᆝ")).lower()
            with self._lock:
                self.store[bstack111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᆞ")] = [bstack1lll11llll1_opy_.bstack1lll11l1111_opy_()]
                if bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᆟ"), None):
                    self.store[bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨᆠ")].append(bstack1lll11llll1_opy_.bstack1lll11l1111_opy_())
                else:
                    self.store[bstack111ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫᆡ")].append(bstack1lll11llll1_opy_.bstack1lll11l1111_opy_())
            if bstack1lll1l11111_opy_:
                self._1lll1l1111l_opy_[bstack1lll1l11111_opy_ + bstack111ll_opy_ (u"࠭࠭ࠨᆢ") + attrs.get(bstack111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᆣ"), bstack111ll_opy_ (u"ࠨࠩᆤ")).lower()] = { bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᆥ"): bstack1lll11llll1_opy_ }
            TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᆦ"), bstack1lll11llll1_opy_)
        else:
            bstack1lll1llll11_opy_ = {
                bstack111ll_opy_ (u"ࠫ࡮ࡪࠧᆧ"): uuid4().__str__(),
                bstack111ll_opy_ (u"ࠬࡺࡥࡹࡶࠪᆨ"): bstack111ll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬᆩ").format(attrs.get(bstack111ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧᆪ")), attrs.get(bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆫ"), bstack111ll_opy_ (u"ࠩࠪᆬ"))) if attrs.get(bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᆭ"), []) else attrs.get(bstack111ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᆮ")),
                bstack111ll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᆯ"): attrs.get(bstack111ll_opy_ (u"࠭ࡡࡳࡩࡶࠫᆰ"), []),
                bstack111ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᆱ"): bstack1111l1l1l_opy_(),
                bstack111ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᆲ"): bstack111ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᆳ"),
                bstack111ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᆴ"): attrs.get(bstack111ll_opy_ (u"ࠫࡩࡵࡣࠨᆵ"), bstack111ll_opy_ (u"ࠬ࠭ᆶ"))
            }
            if attrs.get(bstack111ll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧᆷ"), bstack111ll_opy_ (u"ࠧࠨᆸ")) != bstack111ll_opy_ (u"ࠨࠩᆹ"):
                bstack1lll1llll11_opy_[bstack111ll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᆺ")] = attrs.get(bstack111ll_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫᆻ"))
            if not self.bstack1lll11ll111_opy_:
                self._1lll1l1111l_opy_[self._1lll111ll1l_opy_()][bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᆼ")].add_step(bstack1lll1llll11_opy_)
                threading.current_thread().current_step_uuid = bstack1lll1llll11_opy_[bstack111ll_opy_ (u"ࠬ࡯ࡤࠨᆽ")]
            self.bstack1lll11ll111_opy_.append(bstack1lll1llll11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll1l1l11l_opy_()
        self._1lll111llll_opy_(messages)
        current_test_id = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᆾ"), None)
        bstack1lll1l11111_opy_ = current_test_id if current_test_id else bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪᆿ"), None)
        bstack1lll1lll1l1_opy_ = bstack1lll11l11l1_opy_.get(attrs.get(bstack111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᇀ")), bstack111ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᇁ"))
        bstack1lll1ll111l_opy_ = attrs.get(bstack111ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇂ"))
        if bstack1lll1lll1l1_opy_ != bstack111ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᇃ") and not attrs.get(bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᇄ")) and self._1lll11l1l11_opy_:
            bstack1lll1ll111l_opy_ = self._1lll11l1l11_opy_
        bstack1llll1l11ll_opy_ = Result(result=bstack1lll1lll1l1_opy_, exception=bstack1lll1ll111l_opy_, bstack1llll1l111l_opy_=[bstack1lll1ll111l_opy_])
        if attrs.get(bstack111ll_opy_ (u"࠭ࡴࡺࡲࡨࠫᇅ"), bstack111ll_opy_ (u"ࠧࠨᇆ")).lower() in [bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᇇ"), bstack111ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᇈ")]:
            bstack1lll1l11111_opy_ = current_test_id if current_test_id else bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ᇉ"), None)
            if bstack1lll1l11111_opy_:
                bstack1llll11l1l1_opy_ = bstack1lll1l11111_opy_ + bstack111ll_opy_ (u"ࠦ࠲ࠨᇊ") + attrs.get(bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᇋ"), bstack111ll_opy_ (u"࠭ࠧᇌ")).lower()
                self._1lll1l1111l_opy_[bstack1llll11l1l1_opy_][bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᇍ")].stop(time=bstack1111l1l1l_opy_(), duration=int(attrs.get(bstack111ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᇎ"), bstack111ll_opy_ (u"ࠩ࠳ࠫᇏ"))), result=bstack1llll1l11ll_opy_)
                TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᇐ"), self._1lll1l1111l_opy_[bstack1llll11l1l1_opy_][bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᇑ")])
        else:
            bstack1lll1l11111_opy_ = current_test_id if current_test_id else bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧᇒ"), None)
            if bstack1lll1l11111_opy_ and len(self.bstack1lll11ll111_opy_) == 1:
                current_step_uuid = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪᇓ"), None)
                self._1lll1l1111l_opy_[bstack1lll1l11111_opy_][bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᇔ")].bstack1llll111lll_opy_(current_step_uuid, duration=int(attrs.get(bstack111ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᇕ"), bstack111ll_opy_ (u"ࠩ࠳ࠫᇖ"))), result=bstack1llll1l11ll_opy_)
            else:
                self.bstack1lll1ll1ll1_opy_(attrs)
            self.bstack1lll11ll111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111ll_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨᇗ"), bstack111ll_opy_ (u"ࠫࡳࡵࠧᇘ")) == bstack111ll_opy_ (u"ࠬࡿࡥࡴࠩᇙ"):
                return
            self.messages.push(message)
            logs = []
            if bstack111ll111_opy_.bstack1llll111l1l_opy_():
                logs.append({
                    bstack111ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᇚ"): bstack1111l1l1l_opy_(),
                    bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᇛ"): message.get(bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇜ")),
                    bstack111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᇝ"): message.get(bstack111ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇞ")),
                    **bstack111ll111_opy_.bstack1llll111l1l_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1lllll1l1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1lll11ll1ll_opy_()
    def bstack1lll1ll1ll1_opy_(self, bstack1lll1ll1l1l_opy_):
        if not bstack111ll111_opy_.bstack1llll111l1l_opy_():
            return
        kwname = bstack111ll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪᇟ").format(bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬᇠ")), bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"࠭ࡡࡳࡩࡶࠫᇡ"), bstack111ll_opy_ (u"ࠧࠨᇢ"))) if bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᇣ"), []) else bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᇤ"))
        error_message = bstack111ll_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤᇥ").format(kwname, bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᇦ")), str(bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᇧ"))))
        bstack1lll1ll1l11_opy_ = bstack111ll_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧᇨ").format(kwname, bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᇩ")))
        bstack1lll1l11l11_opy_ = error_message if bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇪ")) else bstack1lll1ll1l11_opy_
        bstack1lll11lllll_opy_ = {
            bstack111ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᇫ"): self.bstack1lll11ll111_opy_[-1].get(bstack111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᇬ"), bstack1111l1l1l_opy_()),
            bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇭ"): bstack1lll1l11l11_opy_,
            bstack111ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᇮ"): bstack111ll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬᇯ") if bstack1lll1ll1l1l_opy_.get(bstack111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᇰ")) == bstack111ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ᇱ") else bstack111ll_opy_ (u"ࠩࡌࡒࡋࡕࠧᇲ"),
            **bstack111ll111_opy_.bstack1llll111l1l_opy_()
        }
        TestHubHandler.bstack1lllll1l1_opy_([bstack1lll11lllll_opy_])
    def _1lll111ll1l_opy_(self):
        for bstack1lll1l111l1_opy_ in reversed(self._1lll1l1111l_opy_):
            bstack1lll1l1llll_opy_ = bstack1lll1l111l1_opy_
            data = self._1lll1l1111l_opy_[bstack1lll1l111l1_opy_][bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᇳ")]
            if isinstance(data, bstack1llll111111_opy_):
                if not bstack111ll_opy_ (u"ࠫࡊࡇࡃࡉࠩᇴ") in data.bstack1lll1l1ll1l_opy_():
                    return bstack1lll1l1llll_opy_
            else:
                return bstack1lll1l1llll_opy_
    def _1lll111llll_opy_(self, messages):
        try:
            bstack1lll1lll1ll_opy_ = BuiltIn().get_variable_value(bstack111ll_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦᇵ")) in (bstack1lll1lll11l_opy_.DEBUG, bstack1lll1lll11l_opy_.TRACE)
            for message, bstack1lll11l1ll1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᇶ"))
                level = message.get(bstack111ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇷ"))
                if level == bstack1lll1lll11l_opy_.FAIL:
                    self._1lll11l1l11_opy_ = name or self._1lll11l1l11_opy_
                    self._1lll11l1lll_opy_ = bstack1lll11l1ll1_opy_.get(bstack111ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᇸ")) if bstack1lll1lll1ll_opy_ and bstack1lll11l1ll1_opy_ else self._1lll11l1lll_opy_
        except:
            pass
    @classmethod
    def bstack1llll11ll11_opy_(self, event: str, bstack1lll11l111l_opy_: bstack1lll1ll11l1_opy_, bstack1lll11l11ll_opy_=False):
        if event == bstack111ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᇹ"):
            bstack1lll11l111l_opy_.set(hooks=self.store[bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧᇺ")])
        if event == bstack111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᇻ"):
            event = bstack111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᇼ")
        if bstack1lll11l11ll_opy_:
            bstack1lll1lll111_opy_ = {
                bstack111ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᇽ"): event,
                bstack1lll11l111l_opy_.bstack1lll11lll11_opy_(): bstack1lll11l111l_opy_.bstack1lll1l111ll_opy_(event)
            }
            with self._lock:
                self.bstack1lll111lll1_opy_.append(bstack1lll1lll111_opy_)
        else:
            TestHubHandler.bstack1llll11ll11_opy_(event, bstack1lll11l111l_opy_)
class bstack1lll1ll1111_opy_:
    def __init__(self):
        self._1lll1l11l1l_opy_ = []
    def bstack1lll1l1lll1_opy_(self):
        self._1lll1l11l1l_opy_.append([])
    def bstack1lll1l1l11l_opy_(self):
        return self._1lll1l11l1l_opy_.pop() if self._1lll1l11l1l_opy_ else list()
    def push(self, message):
        self._1lll1l11l1l_opy_[-1].append(message) if self._1lll1l11l1l_opy_ else self._1lll1l11l1l_opy_.append([message])
class bstack1lll1lll11l_opy_:
    FAIL = bstack111ll_opy_ (u"ࠧࡇࡃࡌࡐࠬᇾ")
    ERROR = bstack111ll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧᇿ")
    WARNING = bstack111ll_opy_ (u"࡚ࠩࡅࡗࡔࠧሀ")
    bstack1lll1l1ll11_opy_ = bstack111ll_opy_ (u"ࠪࡍࡓࡌࡏࠨሁ")
    DEBUG = bstack111ll_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪሂ")
    TRACE = bstack111ll_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫሃ")
    bstack1lll1l11ll1_opy_ = [FAIL, ERROR]
def bstack1lll1ll1lll_opy_(bstack1lll1l11lll_opy_):
    if not bstack1lll1l11lll_opy_:
        return None
    if bstack1lll1l11lll_opy_.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩሄ"), None):
        return getattr(bstack1lll1l11lll_opy_[bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪህ")], bstack111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ሆ"), None)
    return bstack1lll1l11lll_opy_.get(bstack111ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧሇ"), None)
def bstack1lll11l1l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩለ"), bstack111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ሉ")]:
        return
    if hook_type.lower() == bstack111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫሊ"):
        if current_test_uuid is None:
            return bstack111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪላ")
        else:
            return bstack111ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬሌ")
    elif hook_type.lower() == bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪል"):
        if current_test_uuid is None:
            return bstack111ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬሎ")
        else:
            return bstack111ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧሏ")