# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11ll11_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1l1l1_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack111l11ll1l_opy_, bstack111ll1l11l_opy_, bstack111ll11l11_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack11l1l1111_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1lllllllll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11l11ll_opy_, bstack1l1l11lll_opy_, Result, \
    error_handler, bstack111l1ll11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩོ࠭"): [],
        bstack11l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴཽࠩ"): [],
        bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨཾ"): []
    }
    bstack111l1ll1ll_opy_ = []
    bstack1111ll1l11_opy_ = []
    @staticmethod
    def bstack111lll11l1_opy_(log):
        if not ((isinstance(log[bstack11l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ")], list) or (isinstance(log[bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ྀࠧ")], dict)) and len(log[bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱྀ")])>0) or (isinstance(log[bstack11l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྂ")], str) and log[bstack11l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྃ")].strip())):
            return
        active = bstack11l1l1111_opy_.bstack111ll1l1ll_opy_()
        log = {
            bstack11l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭྄ࠩ"): log[bstack11l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ྅")],
            bstack11l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ྆"): bstack111l1ll11l_opy_().isoformat() + bstack11l1_opy_ (u"࡚࠭ࠨ྇"),
            bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྈ"): log[bstack11l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྉ")],
        }
        if active:
            if active[bstack11l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྊ")] == bstack11l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨྋ"):
                log[bstack11l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྌ")] = active[bstack11l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྍ")]
            elif active[bstack11l1_opy_ (u"࠭ࡴࡺࡲࡨࠫྎ")] == bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࠬྏ"):
                log[bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྐ")] = active[bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩྑ")]
        bstack1lllllllll_opy_.bstack11l11l111_opy_([log])
    def __init__(self):
        self.messages = bstack1111lll111_opy_()
        self._111l11l111_opy_ = None
        self._111l111111_opy_ = None
        self._1111lll1l1_opy_ = OrderedDict()
        self.bstack111lll111l_opy_ = bstack111ll1l1l1_opy_(self.bstack111lll11l1_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1ll111_opy_()
        if not self._1111lll1l1_opy_.get(attrs.get(bstack11l1_opy_ (u"ࠪ࡭ࡩ࠭ྒ")), None):
            self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠫ࡮ࡪࠧྒྷ"))] = {}
        bstack111l11llll_opy_ = bstack111ll11l11_opy_(
                bstack111l11l1l1_opy_=attrs.get(bstack11l1_opy_ (u"ࠬ࡯ࡤࠨྔ")),
                name=name,
                started_at=bstack1l1l11lll_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྕ")], start=os.getcwd()) if attrs.get(bstack11l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྖ")) != bstack11l1_opy_ (u"ࠨࠩྗ") else bstack11l1_opy_ (u"ࠩࠪ྘"),
                framework=bstack11l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩྙ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1_opy_ (u"ࠫ࡮ࡪࠧྚ"), None)
        self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠬ࡯ࡤࠨྛ"))][bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྜ")] = bstack111l11llll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1l11l1_opy_()
        self._111l1l111l_opy_(messages)
        with self._lock:
            for bstack111l1111ll_opy_ in self.bstack111l1ll1ll_opy_:
                bstack111l1111ll_opy_[bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩྜྷ")][bstack11l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧྞ")].extend(self.store[bstack11l1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྟ")])
                bstack1lllllllll_opy_.bstack111l1lll_opy_(bstack111l1111ll_opy_)
            self.bstack111l1ll1ll_opy_ = []
            self.store[bstack11l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྠ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll111l_opy_.start()
        if not self._1111lll1l1_opy_.get(attrs.get(bstack11l1_opy_ (u"ࠫ࡮ࡪࠧྡ")), None):
            self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠬ࡯ࡤࠨྡྷ"))] = {}
        driver = bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬྣ"), None)
        bstack111lll11ll_opy_ = bstack111ll11l11_opy_(
            bstack111l11l1l1_opy_=attrs.get(bstack11l1_opy_ (u"ࠧࡪࡦࠪྤ")),
            name=name,
            started_at=bstack1l1l11lll_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྥ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l111l1l_opy_(attrs.get(bstack11l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩྦ"), None)),
            framework=bstack11l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩྦྷ"),
            tags=attrs[bstack11l1_opy_ (u"ࠫࡹࡧࡧࡴࠩྨ")],
            hooks=self.store[bstack11l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫྩ")],
            bstack111ll11l1l_opy_=bstack1lllllllll_opy_.bstack111ll1l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣྪ").format(bstack11l1_opy_ (u"ࠢࠡࠤྫ").join(attrs[bstack11l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ྫྷ")]), name) if attrs[bstack11l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧྭ")] else name
        )
        self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠪ࡭ࡩ࠭ྮ"))][bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྯ")] = bstack111lll11ll_opy_
        threading.current_thread().current_test_uuid = bstack111lll11ll_opy_.bstack111l11111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1_opy_ (u"ࠬ࡯ࡤࠨྰ"), None)
        self.bstack111lll1ll1_opy_(bstack11l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧྱ"), bstack111lll11ll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll111l_opy_.reset()
        bstack111l1l1111_opy_ = bstack111l1l1ll1_opy_.get(attrs.get(bstack11l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྲ")), bstack11l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩླ"))
        self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠩ࡬ࡨࠬྴ"))][bstack11l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྵ")].stop(time=bstack1l1l11lll_opy_(), duration=int(attrs.get(bstack11l1_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྶ"), bstack11l1_opy_ (u"ࠬ࠶ࠧྷ"))), result=Result(result=bstack111l1l1111_opy_, exception=attrs.get(bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྸ")), bstack111ll11ll1_opy_=[attrs.get(bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྐྵ"))]))
        self.bstack111lll1ll1_opy_(bstack11l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪྺ"), self._1111lll1l1_opy_[attrs.get(bstack11l1_opy_ (u"ࠩ࡬ࡨࠬྻ"))][bstack11l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")], True)
        with self._lock:
            self.store[bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ྽")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1ll111_opy_()
        current_test_id = bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ྾"), None)
        bstack1111llll1l_opy_ = current_test_id if bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ྿"), None) else bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ࿀"), None)
        if attrs.get(bstack11l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿁"), bstack11l1_opy_ (u"ࠩࠪ࿂")).lower() in [bstack11l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ࿃"), bstack11l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭࿄")]:
            hook_type = bstack111ll1111l_opy_(attrs.get(bstack11l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿅")), bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦ࿆ࠪ"), None))
            hook_name = bstack11l1_opy_ (u"ࠧࡼࡿࠪ࿇").format(attrs.get(bstack11l1_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿈"), bstack11l1_opy_ (u"ࠩࠪ࿉")))
            if hook_type in [bstack11l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ࿊"), bstack11l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ࿋")]:
                hook_name = bstack11l1_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭࿌").format(bstack1111lll1ll_opy_.get(hook_type), attrs.get(bstack11l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿍"), bstack11l1_opy_ (u"ࠧࠨ࿎")))
            bstack1111llll11_opy_ = bstack111ll1l11l_opy_(
                bstack111l11l1l1_opy_=bstack1111llll1l_opy_ + bstack11l1_opy_ (u"ࠨ࠯ࠪ࿏") + attrs.get(bstack11l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿐"), bstack11l1_opy_ (u"ࠪࠫ࿑")).lower(),
                name=hook_name,
                started_at=bstack1l1l11lll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ࿒")), start=os.getcwd()),
                framework=bstack11l1_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ࿓"),
                tags=attrs[bstack11l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ࿔")],
                scope=RobotHandler.bstack111l111l1l_opy_(attrs.get(bstack11l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿕"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1111llll11_opy_.bstack111l11111l_opy_()
            threading.current_thread().current_hook_id = bstack1111llll1l_opy_ + bstack11l1_opy_ (u"ࠨ࠯ࠪ࿖") + attrs.get(bstack11l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿗"), bstack11l1_opy_ (u"ࠪࠫ࿘")).lower()
            with self._lock:
                self.store[bstack11l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ࿙")] = [bstack1111llll11_opy_.bstack111l11111l_opy_()]
                if bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ࿚"), None):
                    self.store[bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ࿛")].append(bstack1111llll11_opy_.bstack111l11111l_opy_())
                else:
                    self.store[bstack11l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭࿜")].append(bstack1111llll11_opy_.bstack111l11111l_opy_())
            if bstack1111llll1l_opy_:
                self._1111lll1l1_opy_[bstack1111llll1l_opy_ + bstack11l1_opy_ (u"ࠨ࠯ࠪ࿝") + attrs.get(bstack11l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿞"), bstack11l1_opy_ (u"ࠪࠫ࿟")).lower()] = { bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿠"): bstack1111llll11_opy_ }
            bstack1lllllllll_opy_.bstack111lll1ll1_opy_(bstack11l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭࿡"), bstack1111llll11_opy_)
        else:
            bstack111lll1111_opy_ = {
                bstack11l1_opy_ (u"࠭ࡩࡥࠩ࿢"): uuid4().__str__(),
                bstack11l1_opy_ (u"ࠧࡵࡧࡻࡸࠬ࿣"): bstack11l1_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ࿤").format(attrs.get(bstack11l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿥")), attrs.get(bstack11l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ࿦"), bstack11l1_opy_ (u"ࠫࠬ࿧"))) if attrs.get(bstack11l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿨"), []) else attrs.get(bstack11l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿩")),
                bstack11l1_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ࿪"): attrs.get(bstack11l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭࿫"), []),
                bstack11l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿬"): bstack1l1l11lll_opy_(),
                bstack11l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ࿭"): bstack11l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ࿮"),
                bstack11l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ࿯"): attrs.get(bstack11l1_opy_ (u"࠭ࡤࡰࡥࠪ࿰"), bstack11l1_opy_ (u"ࠧࠨ࿱"))
            }
            if attrs.get(bstack11l1_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ࿲"), bstack11l1_opy_ (u"ࠩࠪ࿳")) != bstack11l1_opy_ (u"ࠪࠫ࿴"):
                bstack111lll1111_opy_[bstack11l1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ࿵")] = attrs.get(bstack11l1_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭࿶"))
            if not self.bstack1111ll1l11_opy_:
                self._1111lll1l1_opy_[self._111l1l1l11_opy_()][bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿷")].add_step(bstack111lll1111_opy_)
                threading.current_thread().current_step_uuid = bstack111lll1111_opy_[bstack11l1_opy_ (u"ࠧࡪࡦࠪ࿸")]
            self.bstack1111ll1l11_opy_.append(bstack111lll1111_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1l11l1_opy_()
        self._111l1l111l_opy_(messages)
        current_test_id = bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ࿹"), None)
        bstack1111llll1l_opy_ = current_test_id if current_test_id else bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ࿺"), None)
        bstack111l1lll1l_opy_ = bstack111l1l1ll1_opy_.get(attrs.get(bstack11l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿻")), bstack11l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ࿼"))
        bstack111l111l11_opy_ = attrs.get(bstack11l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿽"))
        if bstack111l1lll1l_opy_ != bstack11l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ࿾") and not attrs.get(bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿿")) and self._111l11l111_opy_:
            bstack111l111l11_opy_ = self._111l11l111_opy_
        bstack111ll11lll_opy_ = Result(result=bstack111l1lll1l_opy_, exception=bstack111l111l11_opy_, bstack111ll11ll1_opy_=[bstack111l111l11_opy_])
        if attrs.get(bstack11l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭က"), bstack11l1_opy_ (u"ࠩࠪခ")).lower() in [bstack11l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩဂ"), bstack11l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ဃ")]:
            bstack1111llll1l_opy_ = current_test_id if current_test_id else bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨင"), None)
            if bstack1111llll1l_opy_:
                bstack111llll11l_opy_ = bstack1111llll1l_opy_ + bstack11l1_opy_ (u"ࠨ࠭ࠣစ") + attrs.get(bstack11l1_opy_ (u"ࠧࡵࡻࡳࡩࠬဆ"), bstack11l1_opy_ (u"ࠨࠩဇ")).lower()
                self._1111lll1l1_opy_[bstack111llll11l_opy_][bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဈ")].stop(time=bstack1l1l11lll_opy_(), duration=int(attrs.get(bstack11l1_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨဉ"), bstack11l1_opy_ (u"ࠫ࠵࠭ည"))), result=bstack111ll11lll_opy_)
                bstack1lllllllll_opy_.bstack111lll1ll1_opy_(bstack11l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧဋ"), self._1111lll1l1_opy_[bstack111llll11l_opy_][bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩဌ")])
        else:
            bstack1111llll1l_opy_ = current_test_id if current_test_id else bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩဍ"), None)
            if bstack1111llll1l_opy_ and len(self.bstack1111ll1l11_opy_) == 1:
                current_step_uuid = bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬဎ"), None)
                self._1111lll1l1_opy_[bstack1111llll1l_opy_][bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဏ")].bstack111ll111ll_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨတ"), bstack11l1_opy_ (u"ࠫ࠵࠭ထ"))), result=bstack111ll11lll_opy_)
            else:
                self.bstack1111llllll_opy_(attrs)
            self.bstack1111ll1l11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪဒ"), bstack11l1_opy_ (u"࠭࡮ࡰࠩဓ")) == bstack11l1_opy_ (u"ࠧࡺࡧࡶࠫန"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1l1111_opy_.bstack111ll1l1ll_opy_():
                logs.append({
                    bstack11l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫပ"): bstack1l1l11lll_opy_(),
                    bstack11l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဖ"): message.get(bstack11l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဗ")),
                    bstack11l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဘ"): message.get(bstack11l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫမ")),
                    **bstack11l1l1111_opy_.bstack111ll1l1ll_opy_()
                })
                if len(logs) > 0:
                    bstack1lllllllll_opy_.bstack11l11l111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1lllllllll_opy_.bstack111l1llll1_opy_()
    def bstack1111llllll_opy_(self, bstack111l1ll1l1_opy_):
        if not bstack11l1l1111_opy_.bstack111ll1l1ll_opy_():
            return
        kwname = bstack11l1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬယ").format(bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧရ")), bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭လ"), bstack11l1_opy_ (u"ࠩࠪဝ"))) if bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨသ"), []) else bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫဟ"))
        error_message = bstack11l1_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦဠ").format(kwname, bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭အ")), str(bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ"))))
        bstack111l1l1lll_opy_ = bstack11l1_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢဣ").format(kwname, bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩဤ")))
        bstack111l1111l1_opy_ = error_message if bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဥ")) else bstack111l1l1lll_opy_
        bstack111ll11111_opy_ = {
            bstack11l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧဦ"): self.bstack1111ll1l11_opy_[-1].get(bstack11l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩဧ"), bstack1l1l11lll_opy_()),
            bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဨ"): bstack111l1111l1_opy_,
            bstack11l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ဩ"): bstack11l1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧဪ") if bstack111l1ll1l1_opy_.get(bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩါ")) == bstack11l1_opy_ (u"ࠪࡊࡆࡏࡌࠨာ") else bstack11l1_opy_ (u"ࠫࡎࡔࡆࡐࠩိ"),
            **bstack11l1l1111_opy_.bstack111ll1l1ll_opy_()
        }
        bstack1lllllllll_opy_.bstack11l11l111_opy_([bstack111ll11111_opy_])
    def _111l1l1l11_opy_(self):
        for bstack111l11l1l1_opy_ in reversed(self._1111lll1l1_opy_):
            bstack1111ll1lll_opy_ = bstack111l11l1l1_opy_
            data = self._1111lll1l1_opy_[bstack111l11l1l1_opy_][bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨီ")]
            if isinstance(data, bstack111ll1l11l_opy_):
                if not bstack11l1_opy_ (u"࠭ࡅࡂࡅࡋࠫု") in data.bstack111l1l1l1l_opy_():
                    return bstack1111ll1lll_opy_
            else:
                return bstack1111ll1lll_opy_
    def _111l1l111l_opy_(self, messages):
        try:
            bstack111l1lllll_opy_ = BuiltIn().get_variable_value(bstack11l1_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨူ")) in (bstack1111lll11l_opy_.DEBUG, bstack1111lll11l_opy_.TRACE)
            for message, bstack111ll111l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩေ"))
                level = message.get(bstack11l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨဲ"))
                if level == bstack1111lll11l_opy_.FAIL:
                    self._111l11l111_opy_ = name or self._111l11l111_opy_
                    self._111l111111_opy_ = bstack111ll111l1_opy_.get(bstack11l1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦဳ")) if bstack111l1lllll_opy_ and bstack111ll111l1_opy_ else self._111l111111_opy_
        except:
            pass
    @classmethod
    def bstack111lll1ll1_opy_(self, event: str, bstack111l11l11l_opy_: bstack111l11ll1l_opy_, bstack111l1lll11_opy_=False):
        if event == bstack11l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ဴ"):
            bstack111l11l11l_opy_.set(hooks=self.store[bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩဵ")])
        if event == bstack11l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧံ"):
            event = bstack11l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥ့ࠩ")
        if bstack111l1lll11_opy_:
            bstack1111ll1l1l_opy_ = {
                bstack11l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬး"): event,
                bstack111l11l11l_opy_.bstack1111ll1ll1_opy_(): bstack111l11l11l_opy_.bstack111l111lll_opy_(event)
            }
            with self._lock:
                self.bstack111l1ll1ll_opy_.append(bstack1111ll1l1l_opy_)
        else:
            bstack1lllllllll_opy_.bstack111lll1ll1_opy_(event, bstack111l11l11l_opy_)
class bstack1111lll111_opy_:
    def __init__(self):
        self._1111lllll1_opy_ = []
    def bstack111l1ll111_opy_(self):
        self._1111lllll1_opy_.append([])
    def bstack111l1l11l1_opy_(self):
        return self._1111lllll1_opy_.pop() if self._1111lllll1_opy_ else list()
    def push(self, message):
        self._1111lllll1_opy_[-1].append(message) if self._1111lllll1_opy_ else self._1111lllll1_opy_.append([message])
class bstack1111lll11l_opy_:
    FAIL = bstack11l1_opy_ (u"ࠩࡉࡅࡎࡒ္ࠧ")
    ERROR = bstack11l1_opy_ (u"ࠪࡉࡗࡘࡏࡓ်ࠩ")
    WARNING = bstack11l1_opy_ (u"ࠫ࡜ࡇࡒࡏࠩျ")
    bstack111l111ll1_opy_ = bstack11l1_opy_ (u"ࠬࡏࡎࡇࡑࠪြ")
    DEBUG = bstack11l1_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬွ")
    TRACE = bstack11l1_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ှ")
    bstack111l11lll1_opy_ = [FAIL, ERROR]
def bstack111l1l11ll_opy_(bstack111l11l1ll_opy_):
    if not bstack111l11l1ll_opy_:
        return None
    if bstack111l11l1ll_opy_.get(bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဿ"), None):
        return getattr(bstack111l11l1ll_opy_[bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ၀")], bstack11l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ၁"), None)
    return bstack111l11l1ll_opy_.get(bstack11l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ၂"), None)
def bstack111ll1111l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ၃"), bstack11l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ၄")]:
        return
    if hook_type.lower() == bstack11l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭၅"):
        if current_test_uuid is None:
            return bstack11l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ၆")
        else:
            return bstack11l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ၇")
    elif hook_type.lower() == bstack11l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ၈"):
        if current_test_uuid is None:
            return bstack11l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ၉")
        else:
            return bstack11l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ၊")