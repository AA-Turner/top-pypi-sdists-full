# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11ll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack111l1l1111_opy_, bstack111ll1l1ll_opy_, bstack111llllll1_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack11111ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11l1l1l_opy_, bstack1llllllll1_opy_, Result, \
    bstack111l1ll1l1_opy_, bstack111l1lll11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩཀ"): [],
        bstack111lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཁ"): [],
        bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫག"): []
    }
    bstack111ll11lll_opy_ = []
    bstack111l11l1ll_opy_ = []
    @staticmethod
    def bstack11l1111111_opy_(log):
        if not ((isinstance(log[bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩགྷ")], list) or (isinstance(log[bstack111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪང")], dict)) and len(log[bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཅ")])>0) or (isinstance(log[bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཆ")], str) and log[bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཇ")].strip())):
            return
        active = bstack11l1ll111_opy_.bstack111ll1ll1l_opy_()
        log = {
            bstack111lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ཈"): log[bstack111lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ཉ")],
            bstack111lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫཊ"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠩ࡝ࠫཋ"),
            bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཌ"): log[bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཌྷ")],
        }
        if active:
            if active[bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪཎ")] == bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫཏ"):
                log[bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧཐ")] = active[bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨད")]
            elif active[bstack111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧདྷ")] == bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࠨན"):
                log[bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫཔ")] = active[bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཕ")]
        bstack11111ll1l_opy_.bstack11l1111ll_opy_([log])
    def __init__(self):
        self.messages = bstack1111lll1ll_opy_()
        self._111l1l11ll_opy_ = None
        self._111l1l1ll1_opy_ = None
        self._111l11lll1_opy_ = OrderedDict()
        self.bstack111lll11ll_opy_ = bstack111ll1lll1_opy_(self.bstack11l1111111_opy_)
    @bstack111l1ll1l1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l111l1l_opy_()
        if not self._111l11lll1_opy_.get(attrs.get(bstack111lll_opy_ (u"࠭ࡩࡥࠩབ")), None):
            self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"ࠧࡪࡦࠪབྷ"))] = {}
        bstack111l1ll111_opy_ = bstack111llllll1_opy_(
                bstack111l11l111_opy_=attrs.get(bstack111lll_opy_ (u"ࠨ࡫ࡧࠫམ")),
                name=name,
                started_at=bstack1llllllll1_opy_(),
                file_path=os.path.relpath(attrs[bstack111lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩཙ")], start=os.getcwd()) if attrs.get(bstack111lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཚ")) != bstack111lll_opy_ (u"ࠫࠬཛ") else bstack111lll_opy_ (u"ࠬ࠭ཛྷ"),
                framework=bstack111lll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཝ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111lll_opy_ (u"ࠧࡪࡦࠪཞ"), None)
        self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"ࠨ࡫ࡧࠫཟ"))][bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬའ")] = bstack111l1ll111_opy_
    @bstack111l1ll1l1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll11ll1_opy_()
        self._111l1l1l11_opy_(messages)
        for bstack111ll111l1_opy_ in self.bstack111ll11lll_opy_:
            bstack111ll111l1_opy_[bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬཡ")][bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪར")].extend(self.store[bstack111lll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫལ")])
            bstack11111ll1l_opy_.bstack11111111l_opy_(bstack111ll111l1_opy_)
        self.bstack111ll11lll_opy_ = []
        self.store[bstack111lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཤ")] = []
    @bstack111l1ll1l1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll11ll_opy_.start()
        if not self._111l11lll1_opy_.get(attrs.get(bstack111lll_opy_ (u"ࠧࡪࡦࠪཥ")), None):
            self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"ࠨ࡫ࡧࠫས"))] = {}
        driver = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨཧ"), None)
        bstack11l111111l_opy_ = bstack111llllll1_opy_(
            bstack111l11l111_opy_=attrs.get(bstack111lll_opy_ (u"ࠪ࡭ࡩ࠭ཨ")),
            name=name,
            started_at=bstack1llllllll1_opy_(),
            file_path=os.path.relpath(attrs[bstack111lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཀྵ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack111lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཪ"), None)),
            framework=bstack111lll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཫ"),
            tags=attrs[bstack111lll_opy_ (u"ࠧࡵࡣࡪࡷࠬཬ")],
            hooks=self.store[bstack111lll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ཭")],
            bstack111lll1l11_opy_=bstack11111ll1l_opy_.bstack111lll1lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111lll_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦ཮").format(bstack111lll_opy_ (u"ࠥࠤࠧ཯").join(attrs[bstack111lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ཰")]), name) if attrs[bstack111lll_opy_ (u"ࠬࡺࡡࡨࡵཱࠪ")] else name
        )
        self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"࠭ࡩࡥིࠩ"))][bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣཱིࠪ")] = bstack11l111111l_opy_
        threading.current_thread().current_test_uuid = bstack11l111111l_opy_.bstack111l1111ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111lll_opy_ (u"ࠨ࡫ࡧུࠫ"), None)
        self.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦཱུࠪ"), bstack11l111111l_opy_)
    @bstack111l1ll1l1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll11ll_opy_.reset()
        bstack111l1l11l1_opy_ = bstack111ll1l11l_opy_.get(attrs.get(bstack111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪྲྀ")), bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཷ"))
        self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"ࠬ࡯ࡤࠨླྀ"))][bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཹ")].stop(time=bstack1llllllll1_opy_(), duration=int(attrs.get(bstack111lll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩེࠬ"), bstack111lll_opy_ (u"ࠨ࠲ཻࠪ"))), result=Result(result=bstack111l1l11l1_opy_, exception=attrs.get(bstack111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧོࠪ")), bstack111lll111l_opy_=[attrs.get(bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨཽࠫ"))]))
        self.bstack111lllllll_opy_(bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ཾ"), self._111l11lll1_opy_[attrs.get(bstack111lll_opy_ (u"ࠬ࡯ࡤࠨཿ"))][bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢྀࠩ")], True)
        self.store[bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶཱྀࠫ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1ll1l1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l111l1l_opy_()
        current_test_id = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪྂ"), None)
        bstack1111lll1l1_opy_ = current_test_id if bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫྃ"), None) else bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ྄࠭"), None)
        if attrs.get(bstack111lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ྅"), bstack111lll_opy_ (u"ࠬ࠭྆")).lower() in [bstack111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ྇"), bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩྈ")]:
            hook_type = bstack111l1ll1ll_opy_(attrs.get(bstack111lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྉ")), bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ྊ"), None))
            hook_name = bstack111lll_opy_ (u"ࠪࡿࢂ࠭ྋ").format(attrs.get(bstack111lll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫྌ"), bstack111lll_opy_ (u"ࠬ࠭ྍ")))
            if hook_type in [bstack111lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪྎ"), bstack111lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪྏ")]:
                hook_name = bstack111lll_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩྐ").format(bstack111l111111_opy_.get(hook_type), attrs.get(bstack111lll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྑ"), bstack111lll_opy_ (u"ࠪࠫྒ")))
            bstack111l11l1l1_opy_ = bstack111ll1l1ll_opy_(
                bstack111l11l111_opy_=bstack1111lll1l1_opy_ + bstack111lll_opy_ (u"ࠫ࠲࠭ྒྷ") + attrs.get(bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪྔ"), bstack111lll_opy_ (u"࠭ࠧྕ")).lower(),
                name=hook_name,
                started_at=bstack1llllllll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྖ")), start=os.getcwd()),
                framework=bstack111lll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧྗ"),
                tags=attrs[bstack111lll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ྘")],
                scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack111lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྙ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l11l1l1_opy_.bstack111l1111ll_opy_()
            threading.current_thread().current_hook_id = bstack1111lll1l1_opy_ + bstack111lll_opy_ (u"ࠫ࠲࠭ྚ") + attrs.get(bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪྛ"), bstack111lll_opy_ (u"࠭ࠧྜ")).lower()
            self.store[bstack111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫྜྷ")] = [bstack111l11l1l1_opy_.bstack111l1111ll_opy_()]
            if bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬྞ"), None):
                self.store[bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྟ")].append(bstack111l11l1l1_opy_.bstack111l1111ll_opy_())
            else:
                self.store[bstack111lll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྠ")].append(bstack111l11l1l1_opy_.bstack111l1111ll_opy_())
            if bstack1111lll1l1_opy_:
                self._111l11lll1_opy_[bstack1111lll1l1_opy_ + bstack111lll_opy_ (u"ࠫ࠲࠭ྡ") + attrs.get(bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪྡྷ"), bstack111lll_opy_ (u"࠭ࠧྣ")).lower()] = { bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྤ"): bstack111l11l1l1_opy_ }
            bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩྥ"), bstack111l11l1l1_opy_)
        else:
            bstack111llll111_opy_ = {
                bstack111lll_opy_ (u"ࠩ࡬ࡨࠬྦ"): uuid4().__str__(),
                bstack111lll_opy_ (u"ࠪࡸࡪࡾࡴࠨྦྷ"): bstack111lll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪྨ").format(attrs.get(bstack111lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬྩ")), attrs.get(bstack111lll_opy_ (u"࠭ࡡࡳࡩࡶࠫྪ"), bstack111lll_opy_ (u"ࠧࠨྫ"))) if attrs.get(bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྫྷ"), []) else attrs.get(bstack111lll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྭ")),
                bstack111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪྮ"): attrs.get(bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩྯ"), []),
                bstack111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩྰ"): bstack1llllllll1_opy_(),
                bstack111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ྱ"): bstack111lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨྲ"),
                bstack111lll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ླ"): attrs.get(bstack111lll_opy_ (u"ࠩࡧࡳࡨ࠭ྴ"), bstack111lll_opy_ (u"ࠪࠫྵ"))
            }
            if attrs.get(bstack111lll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬྶ"), bstack111lll_opy_ (u"ࠬ࠭ྷ")) != bstack111lll_opy_ (u"࠭ࠧྸ"):
                bstack111llll111_opy_[bstack111lll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨྐྵ")] = attrs.get(bstack111lll_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩྺ"))
            if not self.bstack111l11l1ll_opy_:
                self._111l11lll1_opy_[self._111l1l111l_opy_()][bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྻ")].add_step(bstack111llll111_opy_)
                threading.current_thread().current_step_uuid = bstack111llll111_opy_[bstack111lll_opy_ (u"ࠪ࡭ࡩ࠭ྼ")]
            self.bstack111l11l1ll_opy_.append(bstack111llll111_opy_)
    @bstack111l1ll1l1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll11ll1_opy_()
        self._111l1l1l11_opy_(messages)
        current_test_id = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭྽"), None)
        bstack1111lll1l1_opy_ = current_test_id if current_test_id else bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ྾"), None)
        bstack111ll11l1l_opy_ = bstack111ll1l11l_opy_.get(attrs.get(bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭྿")), bstack111lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ࿀"))
        bstack111ll1111l_opy_ = attrs.get(bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿁"))
        if bstack111ll11l1l_opy_ != bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ࿂") and not attrs.get(bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃")) and self._111l1l11ll_opy_:
            bstack111ll1111l_opy_ = self._111l1l11ll_opy_
        bstack111llll1ll_opy_ = Result(result=bstack111ll11l1l_opy_, exception=bstack111ll1111l_opy_, bstack111lll111l_opy_=[bstack111ll1111l_opy_])
        if attrs.get(bstack111lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿄"), bstack111lll_opy_ (u"ࠬ࠭࿅")).lower() in [bstack111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࿆ࠬ"), bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿇")]:
            bstack1111lll1l1_opy_ = current_test_id if current_test_id else bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ࿈"), None)
            if bstack1111lll1l1_opy_:
                bstack111llll11l_opy_ = bstack1111lll1l1_opy_ + bstack111lll_opy_ (u"ࠤ࠰ࠦ࿉") + attrs.get(bstack111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ࿊"), bstack111lll_opy_ (u"ࠫࠬ࿋")).lower()
                self._111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿌")].stop(time=bstack1llllllll1_opy_(), duration=int(attrs.get(bstack111lll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ࿍"), bstack111lll_opy_ (u"ࠧ࠱ࠩ࿎"))), result=bstack111llll1ll_opy_)
                bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿏"), self._111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿐")])
        else:
            bstack1111lll1l1_opy_ = current_test_id if current_test_id else bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬ࿑"), None)
            if bstack1111lll1l1_opy_ and len(self.bstack111l11l1ll_opy_) == 1:
                current_step_uuid = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨ࿒"), None)
                self._111l11lll1_opy_[bstack1111lll1l1_opy_][bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿓")].bstack111ll1l1l1_opy_(current_step_uuid, duration=int(attrs.get(bstack111lll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ࿔"), bstack111lll_opy_ (u"ࠧ࠱ࠩ࿕"))), result=bstack111llll1ll_opy_)
            else:
                self.bstack111ll111ll_opy_(attrs)
            self.bstack111l11l1ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111lll_opy_ (u"ࠨࡪࡷࡱࡱ࠭࿖"), bstack111lll_opy_ (u"ࠩࡱࡳࠬ࿗")) == bstack111lll_opy_ (u"ࠪࡽࡪࡹࠧ࿘"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1ll111_opy_.bstack111ll1ll1l_opy_():
                logs.append({
                    bstack111lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ࿙"): bstack1llllllll1_opy_(),
                    bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿚"): message.get(bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿛")),
                    bstack111lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿜"): message.get(bstack111lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿝")),
                    **bstack11l1ll111_opy_.bstack111ll1ll1l_opy_()
                })
                if len(logs) > 0:
                    bstack11111ll1l_opy_.bstack11l1111ll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11111ll1l_opy_.bstack111ll11l11_opy_()
    def bstack111ll111ll_opy_(self, bstack111l1l1l1l_opy_):
        if not bstack11l1ll111_opy_.bstack111ll1ll1l_opy_():
            return
        kwname = bstack111lll_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ࿞").format(bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿟")), bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿠"), bstack111lll_opy_ (u"ࠬ࠭࿡"))) if bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"࠭ࡡࡳࡩࡶࠫ࿢"), []) else bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ࿣"))
        error_message = bstack111lll_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢ࿤").format(kwname, bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ࿥")), str(bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿦"))))
        bstack111l111lll_opy_ = bstack111lll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥ࿧").format(kwname, bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿨")))
        bstack111l11111l_opy_ = error_message if bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿩")) else bstack111l111lll_opy_
        bstack111ll1l111_opy_ = {
            bstack111lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ࿪"): self.bstack111l11l1ll_opy_[-1].get(bstack111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿫"), bstack1llllllll1_opy_()),
            bstack111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿬"): bstack111l11111l_opy_,
            bstack111lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿭"): bstack111lll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿮") if bstack111l1l1l1l_opy_.get(bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿯")) == bstack111lll_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿰") else bstack111lll_opy_ (u"ࠧࡊࡐࡉࡓࠬ࿱"),
            **bstack11l1ll111_opy_.bstack111ll1ll1l_opy_()
        }
        bstack11111ll1l_opy_.bstack11l1111ll_opy_([bstack111ll1l111_opy_])
    def _111l1l111l_opy_(self):
        for bstack111l11l111_opy_ in reversed(self._111l11lll1_opy_):
            bstack111l1l1lll_opy_ = bstack111l11l111_opy_
            data = self._111l11lll1_opy_[bstack111l11l111_opy_][bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿲")]
            if isinstance(data, bstack111ll1l1ll_opy_):
                if not bstack111lll_opy_ (u"ࠩࡈࡅࡈࡎࠧ࿳") in data.bstack1111llll1l_opy_():
                    return bstack111l1l1lll_opy_
            else:
                return bstack111l1l1lll_opy_
    def _111l1l1l11_opy_(self, messages):
        try:
            bstack111l111ll1_opy_ = BuiltIn().get_variable_value(bstack111lll_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ࿴")) in (bstack111l11l11l_opy_.DEBUG, bstack111l11l11l_opy_.TRACE)
            for message, bstack111l1lll1l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿵"))
                level = message.get(bstack111lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿶"))
                if level == bstack111l11l11l_opy_.FAIL:
                    self._111l1l11ll_opy_ = name or self._111l1l11ll_opy_
                    self._111l1l1ll1_opy_ = bstack111l1lll1l_opy_.get(bstack111lll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ࿷")) if bstack111l111ll1_opy_ and bstack111l1lll1l_opy_ else self._111l1l1ll1_opy_
        except:
            pass
    @classmethod
    def bstack111lllllll_opy_(self, event: str, bstack111l11ll11_opy_: bstack111l1l1111_opy_, bstack111ll11111_opy_=False):
        if event == bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿸"):
            bstack111l11ll11_opy_.set(hooks=self.store[bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿹")])
        if event == bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ࿺"):
            event = bstack111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ࿻")
        if bstack111ll11111_opy_:
            bstack111l11llll_opy_ = {
                bstack111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ࿼"): event,
                bstack111l11ll11_opy_.bstack1111llll11_opy_(): bstack111l11ll11_opy_.bstack111l111l11_opy_(event)
            }
            self.bstack111ll11lll_opy_.append(bstack111l11llll_opy_)
        else:
            bstack11111ll1l_opy_.bstack111lllllll_opy_(event, bstack111l11ll11_opy_)
class bstack1111lll1ll_opy_:
    def __init__(self):
        self._111l1lllll_opy_ = []
    def bstack111l111l1l_opy_(self):
        self._111l1lllll_opy_.append([])
    def bstack111ll11ll1_opy_(self):
        return self._111l1lllll_opy_.pop() if self._111l1lllll_opy_ else list()
    def push(self, message):
        self._111l1lllll_opy_[-1].append(message) if self._111l1lllll_opy_ else self._111l1lllll_opy_.append([message])
class bstack111l11l11l_opy_:
    FAIL = bstack111lll_opy_ (u"ࠬࡌࡁࡊࡎࠪ࿽")
    ERROR = bstack111lll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ࿾")
    WARNING = bstack111lll_opy_ (u"ࠧࡘࡃࡕࡒࠬ࿿")
    bstack111l1111l1_opy_ = bstack111lll_opy_ (u"ࠨࡋࡑࡊࡔ࠭က")
    DEBUG = bstack111lll_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨခ")
    TRACE = bstack111lll_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩဂ")
    bstack1111llllll_opy_ = [FAIL, ERROR]
def bstack111l1llll1_opy_(bstack111l1ll11l_opy_):
    if not bstack111l1ll11l_opy_:
        return None
    if bstack111l1ll11l_opy_.get(bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧဃ"), None):
        return getattr(bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨင")], bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫစ"), None)
    return bstack111l1ll11l_opy_.get(bstack111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬဆ"), None)
def bstack111l1ll1ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧဇ"), bstack111lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫဈ")]:
        return
    if hook_type.lower() == bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩဉ"):
        if current_test_uuid is None:
            return bstack111lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨည")
        else:
            return bstack111lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪဋ")
    elif hook_type.lower() == bstack111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨဌ"):
        if current_test_uuid is None:
            return bstack111lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪဍ")
        else:
            return bstack111lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬဎ")