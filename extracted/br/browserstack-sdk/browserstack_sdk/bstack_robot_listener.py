# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111lll1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack111llll1l1_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1111ll1ll1_opy_, bstack111lllll1l_opy_, bstack111ll1lll1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack1l1111l1_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack1l1l11ll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11111ll1l_opy_, bstack1ll1l11l11_opy_, Result, \
    bstack111l1llll1_opy_, bstack111ll111ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫག"): [],
        bstack11ll1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧགྷ"): [],
        bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ང"): []
    }
    bstack111l111111_opy_ = []
    bstack111l1lll11_opy_ = []
    @staticmethod
    def bstack111lll1lll_opy_(log):
        if not ((isinstance(log[bstack11ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཅ")], list) or (isinstance(log[bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཆ")], dict)) and len(log[bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཇ")])>0) or (isinstance(log[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ཈")], str) and log[bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཉ")].strip())):
            return
        active = bstack1l1111l1_opy_.bstack111llll111_opy_()
        log = {
            bstack11ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧཊ"): log[bstack11ll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨཋ")],
            bstack11ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ཌ"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"ࠫ࡟࠭ཌྷ"),
            bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཎ"): log[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཏ")],
        }
        if active:
            if active[bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬཐ")] == bstack11ll1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ད"):
                log[bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩདྷ")] = active[bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪན")]
            elif active[bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩཔ")] == bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪཕ"):
                log[bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭བ")] = active[bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧབྷ")]
        bstack1l1l11ll11_opy_.bstack1ll111l1l1_opy_([log])
    def __init__(self):
        self.messages = bstack111l111l11_opy_()
        self._111l11l111_opy_ = None
        self._111ll11111_opy_ = None
        self._111l11ll11_opy_ = OrderedDict()
        self.bstack111ll1l111_opy_ = bstack111llll1l1_opy_(self.bstack111lll1lll_opy_)
    @bstack111l1llll1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1ll11l_opy_()
        if not self._111l11ll11_opy_.get(attrs.get(bstack11ll1l1_opy_ (u"ࠨ࡫ࡧࠫམ")), None):
            self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠩ࡬ࡨࠬཙ"))] = {}
        bstack1111ll1l1l_opy_ = bstack111ll1lll1_opy_(
                bstack1111lll11l_opy_=attrs.get(bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ཚ")),
                name=name,
                started_at=bstack1ll1l11l11_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཛ")], start=os.getcwd()) if attrs.get(bstack11ll1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཛྷ")) != bstack11ll1l1_opy_ (u"࠭ࠧཝ") else bstack11ll1l1_opy_ (u"ࠧࠨཞ"),
                framework=bstack11ll1l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧཟ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll1l1_opy_ (u"ࠩ࡬ࡨࠬའ"), None)
        self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ཡ"))][bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧར")] = bstack1111ll1l1l_opy_
    @bstack111l1llll1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1lllll_opy_()
        self._1111lll1ll_opy_(messages)
        for bstack111l1lll1l_opy_ in self.bstack111l111111_opy_:
            bstack111l1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧལ")][bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬཤ")].extend(self.store[bstack11ll1l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ཥ")])
            bstack1l1l11ll11_opy_.bstack11ll111ll1_opy_(bstack111l1lll1l_opy_)
        self.bstack111l111111_opy_ = []
        self.store[bstack11ll1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧས")] = []
    @bstack111l1llll1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111ll1l111_opy_.start()
        if not self._111l11ll11_opy_.get(attrs.get(bstack11ll1l1_opy_ (u"ࠩ࡬ࡨࠬཧ")), None):
            self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ཨ"))] = {}
        driver = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪཀྵ"), None)
        bstack111ll1ll11_opy_ = bstack111ll1lll1_opy_(
            bstack1111lll11l_opy_=attrs.get(bstack11ll1l1_opy_ (u"ࠬ࡯ࡤࠨཪ")),
            name=name,
            started_at=bstack1ll1l11l11_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ཫ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack11ll1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧཬ"), None)),
            framework=bstack11ll1l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ཭"),
            tags=attrs[bstack11ll1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ཮")],
            hooks=self.store[bstack11ll1l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ཯")],
            bstack111ll1l1ll_opy_=bstack1l1l11ll11_opy_.bstack111llll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll1l1_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨ཰").format(bstack11ll1l1_opy_ (u"ཱࠧࠦࠢ").join(attrs[bstack11ll1l1_opy_ (u"࠭ࡴࡢࡩࡶིࠫ")]), name) if attrs[bstack11ll1l1_opy_ (u"ࠧࡵࡣࡪࡷཱིࠬ")] else name
        )
        self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠨ࡫ࡧུࠫ"))][bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥཱུࠬ")] = bstack111ll1ll11_opy_
        threading.current_thread().current_test_uuid = bstack111ll1ll11_opy_.bstack111ll1111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ྲྀ"), None)
        self.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬཷ"), bstack111ll1ll11_opy_)
    @bstack111l1llll1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111ll1l111_opy_.reset()
        bstack111l11lll1_opy_ = bstack1111llll1l_opy_.get(attrs.get(bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬླྀ")), bstack11ll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧཹ"))
        self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠧࡪࡦེࠪ"))][bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤཻࠫ")].stop(time=bstack1ll1l11l11_opy_(), duration=int(attrs.get(bstack11ll1l1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ོࠧ"), bstack11ll1l1_opy_ (u"ࠪ࠴ཽࠬ"))), result=Result(result=bstack111l11lll1_opy_, exception=attrs.get(bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཾ")), bstack111lll11l1_opy_=[attrs.get(bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ"))]))
        self.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨྀ"), self._111l11ll11_opy_[attrs.get(bstack11ll1l1_opy_ (u"ࠧࡪࡦཱྀࠪ"))][bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྂ")], True)
        self.store[bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྃ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1llll1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1ll11l_opy_()
        current_test_id = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨ྄ࠬ"), None)
        bstack111l1ll111_opy_ = current_test_id if bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭྅"), None) else bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ྆"), None)
        if attrs.get(bstack11ll1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ྇"), bstack11ll1l1_opy_ (u"ࠧࠨྈ")).lower() in [bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧྉ"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫྊ")]:
            hook_type = bstack111l111l1l_opy_(attrs.get(bstack11ll1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨྋ")), bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨྌ"), None))
            hook_name = bstack11ll1l1_opy_ (u"ࠬࢁࡽࠨྍ").format(attrs.get(bstack11ll1l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ྎ"), bstack11ll1l1_opy_ (u"ࠧࠨྏ")))
            if hook_type in [bstack11ll1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬྐ"), bstack11ll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬྑ")]:
                hook_name = bstack11ll1l1_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫྒ").format(bstack111ll111l1_opy_.get(hook_type), attrs.get(bstack11ll1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫྒྷ"), bstack11ll1l1_opy_ (u"ࠬ࠭ྔ")))
            bstack111l111lll_opy_ = bstack111lllll1l_opy_(
                bstack1111lll11l_opy_=bstack111l1ll111_opy_ + bstack11ll1l1_opy_ (u"࠭࠭ࠨྕ") + attrs.get(bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬྖ"), bstack11ll1l1_opy_ (u"ࠨࠩྗ")).lower(),
                name=hook_name,
                started_at=bstack1ll1l11l11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ྘")), start=os.getcwd()),
                framework=bstack11ll1l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩྙ"),
                tags=attrs[bstack11ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩྚ")],
                scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack11ll1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྛ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l111lll_opy_.bstack111ll1111l_opy_()
            threading.current_thread().current_hook_id = bstack111l1ll111_opy_ + bstack11ll1l1_opy_ (u"࠭࠭ࠨྜ") + attrs.get(bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬྜྷ"), bstack11ll1l1_opy_ (u"ࠨࠩྞ")).lower()
            self.store[bstack11ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ྟ")] = [bstack111l111lll_opy_.bstack111ll1111l_opy_()]
            if bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧྠ"), None):
                self.store[bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨྡ")].append(bstack111l111lll_opy_.bstack111ll1111l_opy_())
            else:
                self.store[bstack11ll1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫྡྷ")].append(bstack111l111lll_opy_.bstack111ll1111l_opy_())
            if bstack111l1ll111_opy_:
                self._111l11ll11_opy_[bstack111l1ll111_opy_ + bstack11ll1l1_opy_ (u"࠭࠭ࠨྣ") + attrs.get(bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬྤ"), bstack11ll1l1_opy_ (u"ࠨࠩྥ")).lower()] = { bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྦ"): bstack111l111lll_opy_ }
            bstack1l1l11ll11_opy_.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫྦྷ"), bstack111l111lll_opy_)
        else:
            bstack111ll1l1l1_opy_ = {
                bstack11ll1l1_opy_ (u"ࠫ࡮ࡪࠧྨ"): uuid4().__str__(),
                bstack11ll1l1_opy_ (u"ࠬࡺࡥࡹࡶࠪྩ"): bstack11ll1l1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬྪ").format(attrs.get(bstack11ll1l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧྫ")), attrs.get(bstack11ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྫྷ"), bstack11ll1l1_opy_ (u"ࠩࠪྭ"))) if attrs.get(bstack11ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨྮ"), []) else attrs.get(bstack11ll1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫྯ")),
                bstack11ll1l1_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬྰ"): attrs.get(bstack11ll1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫྱ"), []),
                bstack11ll1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫྲ"): bstack1ll1l11l11_opy_(),
                bstack11ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨླ"): bstack11ll1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪྴ"),
                bstack11ll1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨྵ"): attrs.get(bstack11ll1l1_opy_ (u"ࠫࡩࡵࡣࠨྶ"), bstack11ll1l1_opy_ (u"ࠬ࠭ྷ"))
            }
            if attrs.get(bstack11ll1l1_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧྸ"), bstack11ll1l1_opy_ (u"ࠧࠨྐྵ")) != bstack11ll1l1_opy_ (u"ࠨࠩྺ"):
                bstack111ll1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪྻ")] = attrs.get(bstack11ll1l1_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫྼ"))
            if not self.bstack111l1lll11_opy_:
                self._111l11ll11_opy_[self._111l1111l1_opy_()][bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ྽")].add_step(bstack111ll1l1l1_opy_)
                threading.current_thread().current_step_uuid = bstack111ll1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠬ࡯ࡤࠨ྾")]
            self.bstack111l1lll11_opy_.append(bstack111ll1l1l1_opy_)
    @bstack111l1llll1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1lllll_opy_()
        self._1111lll1ll_opy_(messages)
        current_test_id = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ྿"), None)
        bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ࿀"), None)
        bstack111l1l11ll_opy_ = bstack1111llll1l_opy_.get(attrs.get(bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ࿁")), bstack11ll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ࿂"))
        bstack111l1ll1l1_opy_ = attrs.get(bstack11ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃"))
        if bstack111l1l11ll_opy_ != bstack11ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ࿄") and not attrs.get(bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿅")) and self._111l11l111_opy_:
            bstack111l1ll1l1_opy_ = self._111l11l111_opy_
        bstack111ll11l1l_opy_ = Result(result=bstack111l1l11ll_opy_, exception=bstack111l1ll1l1_opy_, bstack111lll11l1_opy_=[bstack111l1ll1l1_opy_])
        if attrs.get(bstack11ll1l1_opy_ (u"࠭ࡴࡺࡲࡨ࿆ࠫ"), bstack11ll1l1_opy_ (u"ࠧࠨ࿇")).lower() in [bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿈"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ࿉")]:
            bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭࿊"), None)
            if bstack111l1ll111_opy_:
                bstack111ll11ll1_opy_ = bstack111l1ll111_opy_ + bstack11ll1l1_opy_ (u"ࠦ࠲ࠨ࿋") + attrs.get(bstack11ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿌"), bstack11ll1l1_opy_ (u"࠭ࠧ࿍")).lower()
                self._111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿎")].stop(time=bstack1ll1l11l11_opy_(), duration=int(attrs.get(bstack11ll1l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭࿏"), bstack11ll1l1_opy_ (u"ࠩ࠳ࠫ࿐"))), result=bstack111ll11l1l_opy_)
                bstack1l1l11ll11_opy_.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ࿑"), self._111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿒")])
        else:
            bstack111l1ll111_opy_ = current_test_id if current_test_id else bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧ࿓"), None)
            if bstack111l1ll111_opy_ and len(self.bstack111l1lll11_opy_) == 1:
                current_step_uuid = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪ࿔"), None)
                self._111l11ll11_opy_[bstack111l1ll111_opy_][bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿕")].bstack111lll111l_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll1l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭࿖"), bstack11ll1l1_opy_ (u"ࠩ࠳ࠫ࿗"))), result=bstack111ll11l1l_opy_)
            else:
                self.bstack111l1l1l1l_opy_(attrs)
            self.bstack111l1lll11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll1l1_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨ࿘"), bstack11ll1l1_opy_ (u"ࠫࡳࡵࠧ࿙")) == bstack11ll1l1_opy_ (u"ࠬࡿࡥࡴࠩ࿚"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1111l1_opy_.bstack111llll111_opy_():
                logs.append({
                    bstack11ll1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ࿛"): bstack1ll1l11l11_opy_(),
                    bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿜"): message.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿝")),
                    bstack11ll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿞"): message.get(bstack11ll1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿟")),
                    **bstack1l1111l1_opy_.bstack111llll111_opy_()
                })
                if len(logs) > 0:
                    bstack1l1l11ll11_opy_.bstack1ll111l1l1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l1l11ll11_opy_.bstack1111llll11_opy_()
    def bstack111l1l1l1l_opy_(self, bstack111l11l1ll_opy_):
        if not bstack1l1111l1_opy_.bstack111llll111_opy_():
            return
        kwname = bstack11ll1l1_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ࿠").format(bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿡")), bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ࿢"), bstack11ll1l1_opy_ (u"ࠧࠨ࿣"))) if bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭࿤"), []) else bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿥"))
        error_message = bstack11ll1l1_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤ࿦").format(kwname, bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ࿧")), str(bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿨"))))
        bstack111l1l11l1_opy_ = bstack11ll1l1_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧ࿩").format(kwname, bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿪")))
        bstack111l1111ll_opy_ = error_message if bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿫")) else bstack111l1l11l1_opy_
        bstack1111ll1lll_opy_ = {
            bstack11ll1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ࿬"): self.bstack111l1lll11_opy_[-1].get(bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ࿭"), bstack1ll1l11l11_opy_()),
            bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿮"): bstack111l1111ll_opy_,
            bstack11ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿯"): bstack11ll1l1_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ࿰") if bstack111l11l1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿱")) == bstack11ll1l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭࿲") else bstack11ll1l1_opy_ (u"ࠩࡌࡒࡋࡕࠧ࿳"),
            **bstack1l1111l1_opy_.bstack111llll111_opy_()
        }
        bstack1l1l11ll11_opy_.bstack1ll111l1l1_opy_([bstack1111ll1lll_opy_])
    def _111l1111l1_opy_(self):
        for bstack1111lll11l_opy_ in reversed(self._111l11ll11_opy_):
            bstack1111llllll_opy_ = bstack1111lll11l_opy_
            data = self._111l11ll11_opy_[bstack1111lll11l_opy_][bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿴")]
            if isinstance(data, bstack111lllll1l_opy_):
                if not bstack11ll1l1_opy_ (u"ࠫࡊࡇࡃࡉࠩ࿵") in data.bstack111l1l1111_opy_():
                    return bstack1111llllll_opy_
            else:
                return bstack1111llllll_opy_
    def _1111lll1ll_opy_(self, messages):
        try:
            bstack111l11111l_opy_ = BuiltIn().get_variable_value(bstack11ll1l1_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦ࿶")) in (bstack111l1l1lll_opy_.DEBUG, bstack111l1l1lll_opy_.TRACE)
            for message, bstack111ll11l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿷"))
                level = message.get(bstack11ll1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿸"))
                if level == bstack111l1l1lll_opy_.FAIL:
                    self._111l11l111_opy_ = name or self._111l11l111_opy_
                    self._111ll11111_opy_ = bstack111ll11l11_opy_.get(bstack11ll1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ࿹")) if bstack111l11111l_opy_ and bstack111ll11l11_opy_ else self._111ll11111_opy_
        except:
            pass
    @classmethod
    def bstack111ll11lll_opy_(self, event: str, bstack111l11llll_opy_: bstack1111ll1ll1_opy_, bstack111l1ll1ll_opy_=False):
        if event == bstack11ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ࿺"):
            bstack111l11llll_opy_.set(hooks=self.store[bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿻")])
        if event == bstack11ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ࿼"):
            event = bstack11ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿽")
        if bstack111l1ll1ll_opy_:
            bstack111l1l1l11_opy_ = {
                bstack11ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ࿾"): event,
                bstack111l11llll_opy_.bstack111l11ll1l_opy_(): bstack111l11llll_opy_.bstack111l111ll1_opy_(event)
            }
            self.bstack111l111111_opy_.append(bstack111l1l1l11_opy_)
        else:
            bstack1l1l11ll11_opy_.bstack111ll11lll_opy_(event, bstack111l11llll_opy_)
class bstack111l111l11_opy_:
    def __init__(self):
        self._111l1l1ll1_opy_ = []
    def bstack111l1ll11l_opy_(self):
        self._111l1l1ll1_opy_.append([])
    def bstack111l1lllll_opy_(self):
        return self._111l1l1ll1_opy_.pop() if self._111l1l1ll1_opy_ else list()
    def push(self, message):
        self._111l1l1ll1_opy_[-1].append(message) if self._111l1l1ll1_opy_ else self._111l1l1ll1_opy_.append([message])
class bstack111l1l1lll_opy_:
    FAIL = bstack11ll1l1_opy_ (u"ࠧࡇࡃࡌࡐࠬ࿿")
    ERROR = bstack11ll1l1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧက")
    WARNING = bstack11ll1l1_opy_ (u"࡚ࠩࡅࡗࡔࠧခ")
    bstack111l1l111l_opy_ = bstack11ll1l1_opy_ (u"ࠪࡍࡓࡌࡏࠨဂ")
    DEBUG = bstack11ll1l1_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪဃ")
    TRACE = bstack11ll1l1_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫင")
    bstack1111lll111_opy_ = [FAIL, ERROR]
def bstack111l11l1l1_opy_(bstack111l11l11l_opy_):
    if not bstack111l11l11l_opy_:
        return None
    if bstack111l11l11l_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩစ"), None):
        return getattr(bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪဆ")], bstack11ll1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ဇ"), None)
    return bstack111l11l11l_opy_.get(bstack11ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧဈ"), None)
def bstack111l111l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩဉ"), bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ည")]:
        return
    if hook_type.lower() == bstack11ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫဋ"):
        if current_test_uuid is None:
            return bstack11ll1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪဌ")
        else:
            return bstack11ll1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬဍ")
    elif hook_type.lower() == bstack11ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪဎ"):
        if current_test_uuid is None:
            return bstack11ll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬဏ")
        else:
            return bstack11ll1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧတ")