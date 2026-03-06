# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11111ll11l1_opy_
from browserstack_sdk.bstack1l1l111l_opy_ import bstack1l11l11111_opy_
def _111111lll11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111111ll11l_opy_:
    def __init__(self, handler):
        self._111111ll1l1_opy_ = {}
        self._111111ll111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l11l11111_opy_.version()
        if bstack11111ll11l1_opy_(pytest_version, bstack1111_opy_ (u"ࠣ࠺࠱࠵࠳࠷⃦ࠢ")) >= 0:
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⃧")] = Module._register_setup_function_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨ⃨ࠫ")] = Module._register_setup_module_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⃩")] = Class._register_setup_class_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ⃪࠭")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦ⃫ࠩ"))
            Module._register_setup_module_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃬"))
            Class._register_setup_class_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃭"))
            Class._register_setup_method_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ⃮ࠪ"))
        else:
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ⃯࠭")] = Module._inject_setup_function_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⃰")] = Module._inject_setup_module_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⃱")] = Class._inject_setup_class_fixture
            self._111111ll1l1_opy_[bstack1111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⃲")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⃳"))
            Module._inject_setup_module_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃴"))
            Class._inject_setup_class_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃵"))
            Class._inject_setup_method_fixture = self.bstack11111l11l1l_opy_(bstack1111_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⃶"))
    def bstack111111ll1ll_opy_(self, bstack111111l1lll_opy_, hook_type):
        bstack111111llll1_opy_ = id(bstack111111l1lll_opy_.__class__)
        if (bstack111111llll1_opy_, hook_type) in self._111111ll111_opy_:
            return
        meth = getattr(bstack111111l1lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111111ll111_opy_[(bstack111111llll1_opy_, hook_type)] = meth
            setattr(bstack111111l1lll_opy_, hook_type, self.bstack11111l11l11_opy_(hook_type, bstack111111llll1_opy_))
    def bstack111111lll1l_opy_(self, instance, bstack11111l1111l_opy_):
        if bstack11111l1111l_opy_ == bstack1111_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ⃷"):
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ⃸"))
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ⃹"))
        if bstack11111l1111l_opy_ == bstack1111_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ⃺"):
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢ⃻"))
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦ⃼"))
        if bstack11111l1111l_opy_ == bstack1111_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ⃽"):
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ⃾"))
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ⃿"))
        if bstack11111l1111l_opy_ == bstack1111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ℀"):
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨ℁"))
            self.bstack111111ll1ll_opy_(instance.obj, bstack1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥℂ"))
    @staticmethod
    def bstack11111l111l1_opy_(hook_type, func, args):
        if hook_type in [bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ℃"), bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ℄")]:
            _111111lll11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111l11l11_opy_(self, hook_type, bstack111111llll1_opy_):
        def bstack111111l1ll1_opy_(arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ℅"))
            result = None
            try:
                bstack1ll1l1l111l_opy_ = self._111111ll111_opy_[(bstack111111llll1_opy_, hook_type)]
                self.bstack11111l111l1_opy_(hook_type, bstack1ll1l1l111l_opy_, (arg,))
                result = Result(result=bstack1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ℆"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ℇ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭℈"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ℉"), result)
        def bstack111111lllll_opy_(this, arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩℊ"))
            result = None
            exception = None
            try:
                self.bstack11111l111l1_opy_(hook_type, self._111111ll111_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪℋ"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫℌ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫℍ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬℎ"), result)
        if hook_type in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ℏ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪℐ")]:
            return bstack111111lllll_opy_
        return bstack111111l1ll1_opy_
    def bstack11111l11l1l_opy_(self, bstack11111l1111l_opy_):
        def bstack11111l111ll_opy_(this, *args, **kwargs):
            self.bstack111111lll1l_opy_(this, bstack11111l1111l_opy_)
            self._111111ll1l1_opy_[bstack11111l1111l_opy_](this, *args, **kwargs)
        return bstack11111l111ll_opy_