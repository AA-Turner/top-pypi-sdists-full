# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111llllll_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll111l1_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1111l1lll1_opy_, bstack111l1lll1l_opy_, bstack111l1ll1ll_opy_
from bstack_utils.bstack111ll11111_opy_ import bstack11lllllll1_opy_
from bstack_utils.bstack111ll11l1l_opy_ import bstack1l11ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1111l1l11_opy_, bstack11l1l1l1l1_opy_, Result, \
    error_handler, bstack111l1l11ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ྆"): [],
        bstack1ll11ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ྇"): [],
        bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫྈ"): []
    }
    bstack1111llll1l_opy_ = []
    bstack1111ll1l1l_opy_ = []
    @staticmethod
    def bstack111l1llll1_opy_(log):
        if not ((isinstance(log[bstack1ll11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྉ")], list) or (isinstance(log[bstack1ll11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྊ")], dict)) and len(log[bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྋ")])>0) or (isinstance(log[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྌ")], str) and log[bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྍ")].strip())):
            return
        active = bstack11lllllll1_opy_.bstack111ll1l11l_opy_()
        log = {
            bstack1ll11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྎ"): log[bstack1ll11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྏ")],
            bstack1ll11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫྐ"): bstack111l1l11ll_opy_().isoformat() + bstack1ll11ll_opy_ (u"ࠩ࡝ࠫྑ"),
            bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྒ"): log[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྒྷ")],
        }
        if active:
            if active[bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪྔ")] == bstack1ll11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫྕ"):
                log[bstack1ll11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧྖ")] = active[bstack1ll11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྗ")]
            elif active[bstack1ll11ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ྘")] == bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࠨྙ"):
                log[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྚ")] = active[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྛ")]
        bstack1l11ll1l_opy_.bstack11lllll11l_opy_([log])
    def __init__(self):
        self.messages = bstack1111l1llll_opy_()
        self._111l11l1l1_opy_ = None
        self._111l11l1ll_opy_ = None
        self._111l111lll_opy_ = OrderedDict()
        self.bstack111ll1l111_opy_ = bstack111ll111l1_opy_(self.bstack111l1llll1_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1l1l_opy_()
        if not self._111l111lll_opy_.get(attrs.get(bstack1ll11ll_opy_ (u"࠭ࡩࡥࠩྜ")), None):
            self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪྜྷ"))] = {}
        bstack1111lllll1_opy_ = bstack111l1ll1ll_opy_(
                bstack111l1111l1_opy_=attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫྞ")),
                name=name,
                started_at=bstack11l1l1l1l1_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll11ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩྟ")], start=os.getcwd()) if attrs.get(bstack1ll11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྠ")) != bstack1ll11ll_opy_ (u"ࠫࠬྡ") else bstack1ll11ll_opy_ (u"ࠬ࠭ྡྷ"),
                framework=bstack1ll11ll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬྣ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪྤ"), None)
        self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫྥ"))][bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྦ")] = bstack1111lllll1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111l1ll1l_opy_()
        self._111l1ll1l1_opy_(messages)
        with self._lock:
            for bstack111l1l1111_opy_ in self.bstack1111llll1l_opy_:
                bstack111l1l1111_opy_[bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬྦྷ")][bstack1ll11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪྨ")].extend(self.store[bstack1ll11ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫྩ")])
                bstack1l11ll1l_opy_.bstack11l11l1l11_opy_(bstack111l1l1111_opy_)
            self.bstack1111llll1l_opy_ = []
            self.store[bstack1ll11ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬྪ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111ll1l111_opy_.start()
        if not self._111l111lll_opy_.get(attrs.get(bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪྫ")), None):
            self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫྫྷ"))] = {}
        driver = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨྭ"), None)
        bstack111lll1111_opy_ = bstack111l1ll1ll_opy_(
            bstack111l1111l1_opy_=attrs.get(bstack1ll11ll_opy_ (u"ࠪ࡭ࡩ࠭ྮ")),
            name=name,
            started_at=bstack11l1l1l1l1_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll11ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫྯ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l11111l_opy_(attrs.get(bstack1ll11ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྰ"), None)),
            framework=bstack1ll11ll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬྱ"),
            tags=attrs[bstack1ll11ll_opy_ (u"ࠧࡵࡣࡪࡷࠬྲ")],
            hooks=self.store[bstack1ll11ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧླ")],
            bstack111l1lllll_opy_=bstack1l11ll1l_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll11ll_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦྴ").format(bstack1ll11ll_opy_ (u"ࠥࠤࠧྵ").join(attrs[bstack1ll11ll_opy_ (u"ࠫࡹࡧࡧࡴࠩྶ")]), name) if attrs[bstack1ll11ll_opy_ (u"ࠬࡺࡡࡨࡵࠪྷ")] else name
        )
        self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"࠭ࡩࡥࠩྸ"))][bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྐྵ")] = bstack111lll1111_opy_
        threading.current_thread().current_test_uuid = bstack111lll1111_opy_.bstack111l11lll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫྺ"), None)
        self.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪྻ"), bstack111lll1111_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111ll1l111_opy_.reset()
        bstack1111ll1lll_opy_ = bstack1111lll1l1_opy_.get(attrs.get(bstack1ll11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪྼ")), bstack1ll11ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ྽"))
        self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࠨ྾"))][bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ྿")].stop(time=bstack11l1l1l1l1_opy_(), duration=int(attrs.get(bstack1ll11ll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿀"), bstack1ll11ll_opy_ (u"ࠨ࠲ࠪ࿁"))), result=Result(result=bstack1111ll1lll_opy_, exception=attrs.get(bstack1ll11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂")), bstack111ll1l1l1_opy_=[attrs.get(bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃"))]))
        self.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿄"), self._111l111lll_opy_[attrs.get(bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࠨ࿅"))][bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ࿆ࠩ")], True)
        with self._lock:
            self.store[bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ࿇")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1l1l_opy_()
        current_test_id = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ࿈"), None)
        bstack1111l1ll11_opy_ = current_test_id if bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ࿉"), None) else bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭࿊"), None)
        if attrs.get(bstack1ll11ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿋"), bstack1ll11ll_opy_ (u"ࠬ࠭࿌")).lower() in [bstack1ll11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ࿍"), bstack1ll11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿎")]:
            hook_type = bstack111l11l111_opy_(attrs.get(bstack1ll11ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿏")), bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭࿐"), None))
            hook_name = bstack1ll11ll_opy_ (u"ࠪࡿࢂ࠭࿑").format(attrs.get(bstack1ll11ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࿒"), bstack1ll11ll_opy_ (u"ࠬ࠭࿓")))
            if hook_type in [bstack1ll11ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ࿔"), bstack1ll11ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ࿕")]:
                hook_name = bstack1ll11ll_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩ࿖").format(bstack111l1l11l1_opy_.get(hook_type), attrs.get(bstack1ll11ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿗"), bstack1ll11ll_opy_ (u"ࠪࠫ࿘")))
            bstack111l1l1lll_opy_ = bstack111l1lll1l_opy_(
                bstack111l1111l1_opy_=bstack1111l1ll11_opy_ + bstack1ll11ll_opy_ (u"ࠫ࠲࠭࿙") + attrs.get(bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿚"), bstack1ll11ll_opy_ (u"࠭ࠧ࿛")).lower(),
                name=hook_name,
                started_at=bstack11l1l1l1l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll11ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿜")), start=os.getcwd()),
                framework=bstack1ll11ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ࿝"),
                tags=attrs[bstack1ll11ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ࿞")],
                scope=RobotHandler.bstack111l11111l_opy_(attrs.get(bstack1ll11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ࿟"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l1lll_opy_.bstack111l11lll1_opy_()
            threading.current_thread().current_hook_id = bstack1111l1ll11_opy_ + bstack1ll11ll_opy_ (u"ࠫ࠲࠭࿠") + attrs.get(bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿡"), bstack1ll11ll_opy_ (u"࠭ࠧ࿢")).lower()
            with self._lock:
                self.store[bstack1ll11ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿣")] = [bstack111l1l1lll_opy_.bstack111l11lll1_opy_()]
                if bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ࿤"), None):
                    self.store[bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿥")].append(bstack111l1l1lll_opy_.bstack111l11lll1_opy_())
                else:
                    self.store[bstack1ll11ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ࿦")].append(bstack111l1l1lll_opy_.bstack111l11lll1_opy_())
            if bstack1111l1ll11_opy_:
                self._111l111lll_opy_[bstack1111l1ll11_opy_ + bstack1ll11ll_opy_ (u"ࠫ࠲࠭࿧") + attrs.get(bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿨"), bstack1ll11ll_opy_ (u"࠭ࠧ࿩")).lower()] = { bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿪"): bstack111l1l1lll_opy_ }
            bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ࿫"), bstack111l1l1lll_opy_)
        else:
            bstack111ll1l1ll_opy_ = {
                bstack1ll11ll_opy_ (u"ࠩ࡬ࡨࠬ࿬"): uuid4().__str__(),
                bstack1ll11ll_opy_ (u"ࠪࡸࡪࡾࡴࠨ࿭"): bstack1ll11ll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ࿮").format(attrs.get(bstack1ll11ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿯")), attrs.get(bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ࿰"), bstack1ll11ll_opy_ (u"ࠧࠨ࿱"))) if attrs.get(bstack1ll11ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭࿲"), []) else attrs.get(bstack1ll11ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿳")),
                bstack1ll11ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ࿴"): attrs.get(bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿵"), []),
                bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ࿶"): bstack11l1l1l1l1_opy_(),
                bstack1ll11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭࿷"): bstack1ll11ll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ࿸"),
                bstack1ll11ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭࿹"): attrs.get(bstack1ll11ll_opy_ (u"ࠩࡧࡳࡨ࠭࿺"), bstack1ll11ll_opy_ (u"ࠪࠫ࿻"))
            }
            if attrs.get(bstack1ll11ll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ࿼"), bstack1ll11ll_opy_ (u"ࠬ࠭࿽")) != bstack1ll11ll_opy_ (u"࠭ࠧ࿾"):
                bstack111ll1l1ll_opy_[bstack1ll11ll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ࿿")] = attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩက"))
            if not self.bstack1111ll1l1l_opy_:
                self._111l111lll_opy_[self._111l11l11l_opy_()][bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬခ")].add_step(bstack111ll1l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack111ll1l1ll_opy_[bstack1ll11ll_opy_ (u"ࠪ࡭ࡩ࠭ဂ")]
            self.bstack1111ll1l1l_opy_.append(bstack111ll1l1ll_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111l1ll1l_opy_()
        self._111l1ll1l1_opy_(messages)
        current_test_id = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ဃ"), None)
        bstack1111l1ll11_opy_ = current_test_id if current_test_id else bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨင"), None)
        bstack1111ll111l_opy_ = bstack1111lll1l1_opy_.get(attrs.get(bstack1ll11ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭စ")), bstack1ll11ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨဆ"))
        bstack111l111ll1_opy_ = attrs.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဇ"))
        if bstack1111ll111l_opy_ != bstack1ll11ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪဈ") and not attrs.get(bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဉ")) and self._111l11l1l1_opy_:
            bstack111l111ll1_opy_ = self._111l11l1l1_opy_
        bstack111ll11l11_opy_ = Result(result=bstack1111ll111l_opy_, exception=bstack111l111ll1_opy_, bstack111ll1l1l1_opy_=[bstack111l111ll1_opy_])
        if attrs.get(bstack1ll11ll_opy_ (u"ࠫࡹࡿࡰࡦࠩည"), bstack1ll11ll_opy_ (u"ࠬ࠭ဋ")).lower() in [bstack1ll11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬဌ"), bstack1ll11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩဍ")]:
            bstack1111l1ll11_opy_ = current_test_id if current_test_id else bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫဎ"), None)
            if bstack1111l1ll11_opy_:
                bstack111ll1llll_opy_ = bstack1111l1ll11_opy_ + bstack1ll11ll_opy_ (u"ࠤ࠰ࠦဏ") + attrs.get(bstack1ll11ll_opy_ (u"ࠪࡸࡾࡶࡥࠨတ"), bstack1ll11ll_opy_ (u"ࠫࠬထ")).lower()
                self._111l111lll_opy_[bstack111ll1llll_opy_][bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဒ")].stop(time=bstack11l1l1l1l1_opy_(), duration=int(attrs.get(bstack1ll11ll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫဓ"), bstack1ll11ll_opy_ (u"ࠧ࠱ࠩန"))), result=bstack111ll11l11_opy_)
                bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪပ"), self._111l111lll_opy_[bstack111ll1llll_opy_][bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဖ")])
        else:
            bstack1111l1ll11_opy_ = current_test_id if current_test_id else bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬဗ"), None)
            if bstack1111l1ll11_opy_ and len(self.bstack1111ll1l1l_opy_) == 1:
                current_step_uuid = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨဘ"), None)
                self._111l111lll_opy_[bstack1111l1ll11_opy_][bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨမ")].bstack111ll1lll1_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll11ll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫယ"), bstack1ll11ll_opy_ (u"ࠧ࠱ࠩရ"))), result=bstack111ll11l11_opy_)
            else:
                self.bstack1111lll1ll_opy_(attrs)
            self.bstack1111ll1l1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll11ll_opy_ (u"ࠨࡪࡷࡱࡱ࠭လ"), bstack1ll11ll_opy_ (u"ࠩࡱࡳࠬဝ")) == bstack1ll11ll_opy_ (u"ࠪࡽࡪࡹࠧသ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11lllllll1_opy_.bstack111ll1l11l_opy_():
                logs.append({
                    bstack1ll11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧဟ"): bstack11l1l1l1l1_opy_(),
                    bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ဠ"): message.get(bstack1ll11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧအ")),
                    bstack1ll11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ဢ"): message.get(bstack1ll11ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧဣ")),
                    **bstack11lllllll1_opy_.bstack111ll1l11l_opy_()
                })
                if len(logs) > 0:
                    bstack1l11ll1l_opy_.bstack11lllll11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l11ll1l_opy_.bstack1111lll111_opy_()
    def bstack1111lll1ll_opy_(self, bstack111l11ll1l_opy_):
        if not bstack11lllllll1_opy_.bstack111ll1l11l_opy_():
            return
        kwname = bstack1ll11ll_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨဤ").format(bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪဥ")), bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡦࡸࡧࡴࠩဦ"), bstack1ll11ll_opy_ (u"ࠬ࠭ဧ"))) if bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫဨ"), []) else bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧဩ"))
        error_message = bstack1ll11ll_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢဪ").format(kwname, bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩါ")), str(bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫာ"))))
        bstack1111ll11l1_opy_ = bstack1ll11ll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥိ").format(kwname, bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬီ")))
        bstack111l1ll111_opy_ = error_message if bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧု")) else bstack1111ll11l1_opy_
        bstack1111lll11l_opy_ = {
            bstack1ll11ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪူ"): self.bstack1111ll1l1l_opy_[-1].get(bstack1ll11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬေ"), bstack11l1l1l1l1_opy_()),
            bstack1ll11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဲ"): bstack111l1ll111_opy_,
            bstack1ll11ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩဳ"): bstack1ll11ll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪဴ") if bstack111l11ll1l_opy_.get(bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬဵ")) == bstack1ll11ll_opy_ (u"࠭ࡆࡂࡋࡏࠫံ") else bstack1ll11ll_opy_ (u"ࠧࡊࡐࡉࡓ့ࠬ"),
            **bstack11lllllll1_opy_.bstack111ll1l11l_opy_()
        }
        bstack1l11ll1l_opy_.bstack11lllll11l_opy_([bstack1111lll11l_opy_])
    def _111l11l11l_opy_(self):
        for bstack111l1111l1_opy_ in reversed(self._111l111lll_opy_):
            bstack111l11llll_opy_ = bstack111l1111l1_opy_
            data = self._111l111lll_opy_[bstack111l1111l1_opy_][bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫး")]
            if isinstance(data, bstack111l1lll1l_opy_):
                if not bstack1ll11ll_opy_ (u"ࠩࡈࡅࡈࡎ္ࠧ") in data.bstack111l111l1l_opy_():
                    return bstack111l11llll_opy_
            else:
                return bstack111l11llll_opy_
    def _111l1ll1l1_opy_(self, messages):
        try:
            bstack1111ll1l11_opy_ = BuiltIn().get_variable_value(bstack1ll11ll_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ်")) in (bstack1111ll1ll1_opy_.DEBUG, bstack1111ll1ll1_opy_.TRACE)
            for message, bstack111l1111ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬျ"))
                level = message.get(bstack1ll11ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫြ"))
                if level == bstack1111ll1ll1_opy_.FAIL:
                    self._111l11l1l1_opy_ = name or self._111l11l1l1_opy_
                    self._111l11l1ll_opy_ = bstack111l1111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢွ")) if bstack1111ll1l11_opy_ and bstack111l1111ll_opy_ else self._111l11l1ll_opy_
        except:
            pass
    @classmethod
    def bstack111ll1ll11_opy_(self, event: str, bstack111l11ll11_opy_: bstack1111l1lll1_opy_, bstack111l111111_opy_=False):
        if event == bstack1ll11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩှ"):
            bstack111l11ll11_opy_.set(hooks=self.store[bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬဿ")])
        if event == bstack1ll11ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ၀"):
            event = bstack1ll11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ၁")
        if bstack111l111111_opy_:
            bstack1111ll1111_opy_ = {
                bstack1ll11ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ၂"): event,
                bstack111l11ll11_opy_.bstack1111ll11ll_opy_(): bstack111l11ll11_opy_.bstack111l111l11_opy_(event)
            }
            with self._lock:
                self.bstack1111llll1l_opy_.append(bstack1111ll1111_opy_)
        else:
            bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(event, bstack111l11ll11_opy_)
class bstack1111l1llll_opy_:
    def __init__(self):
        self._111l1ll11l_opy_ = []
    def bstack111l1l1l1l_opy_(self):
        self._111l1ll11l_opy_.append([])
    def bstack1111l1ll1l_opy_(self):
        return self._111l1ll11l_opy_.pop() if self._111l1ll11l_opy_ else list()
    def push(self, message):
        self._111l1ll11l_opy_[-1].append(message) if self._111l1ll11l_opy_ else self._111l1ll11l_opy_.append([message])
class bstack1111ll1ll1_opy_:
    FAIL = bstack1ll11ll_opy_ (u"ࠬࡌࡁࡊࡎࠪ၃")
    ERROR = bstack1ll11ll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ၄")
    WARNING = bstack1ll11ll_opy_ (u"ࠧࡘࡃࡕࡒࠬ၅")
    bstack1111llll11_opy_ = bstack1ll11ll_opy_ (u"ࠨࡋࡑࡊࡔ࠭၆")
    DEBUG = bstack1ll11ll_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨ၇")
    TRACE = bstack1ll11ll_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ၈")
    bstack111l1l111l_opy_ = [FAIL, ERROR]
def bstack111l1l1l11_opy_(bstack111l1l1ll1_opy_):
    if not bstack111l1l1ll1_opy_:
        return None
    if bstack111l1l1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ၉"), None):
        return getattr(bstack111l1l1ll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ၊")], bstack1ll11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ။"), None)
    return bstack111l1l1ll1_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ၌"), None)
def bstack111l11l111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ၍"), bstack1ll11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ၎")]:
        return
    if hook_type.lower() == bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ၏"):
        if current_test_uuid is None:
            return bstack1ll11ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨၐ")
        else:
            return bstack1ll11ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪၑ")
    elif hook_type.lower() == bstack1ll11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨၒ"):
        if current_test_uuid is None:
            return bstack1ll11ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪၓ")
        else:
            return bstack1ll11ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬၔ")