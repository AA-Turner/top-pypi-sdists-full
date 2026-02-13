# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111l11111l_opy_
from browserstack_sdk.bstack1ll1l111ll_opy_ import bstack1ll11l1l11_opy_
def _11111ll1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11111ll1l1l_opy_:
    def __init__(self, handler):
        self._11111l1l1ll_opy_ = {}
        self._11111l1l111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll11l1l11_opy_.version()
        if bstack1111l11111l_opy_(pytest_version, bstack11l11_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᾳ")) >= 0:
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᾴ")] = Module._register_setup_function_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᾵")] = Module._register_setup_module_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᾶ")] = Class._register_setup_class_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᾷ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᾸ"))
            Module._register_setup_module_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᾹ"))
            Class._register_setup_class_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᾺ"))
            Class._register_setup_method_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫΆ"))
        else:
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᾼ")] = Module._inject_setup_function_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᾽")] = Module._inject_setup_module_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ι")] = Class._inject_setup_class_fixture
            self._11111l1l1ll_opy_[bstack11l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᾿")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ῀"))
            Module._inject_setup_module_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ῁"))
            Class._inject_setup_class_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪῂ"))
            Class._inject_setup_method_fixture = self.bstack11111l1l11l_opy_(bstack11l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬῃ"))
    def bstack11111l1llll_opy_(self, bstack11111ll1l11_opy_, hook_type):
        bstack11111l1ll1l_opy_ = id(bstack11111ll1l11_opy_.__class__)
        if (bstack11111l1ll1l_opy_, hook_type) in self._11111l1l111_opy_:
            return
        meth = getattr(bstack11111ll1l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11111l1l111_opy_[(bstack11111l1ll1l_opy_, hook_type)] = meth
            setattr(bstack11111ll1l11_opy_, hook_type, self.bstack11111l1l1l1_opy_(hook_type, bstack11111l1ll1l_opy_))
    def bstack11111l11lll_opy_(self, instance, bstack11111ll111l_opy_):
        if bstack11111ll111l_opy_ == bstack11l11_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣῄ"):
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢ῅"))
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦῆ"))
        if bstack11111ll111l_opy_ == bstack11l11_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤῇ"):
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣῈ"))
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧΈ"))
        if bstack11111ll111l_opy_ == bstack11l11_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦῊ"):
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥΉ"))
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢῌ"))
        if bstack11111ll111l_opy_ == bstack11l11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ῍"):
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢ῎"))
            self.bstack11111l1llll_opy_(instance.obj, bstack11l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦ῏"))
    @staticmethod
    def bstack11111ll1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩῐ"), bstack11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ῑ")]:
            _11111ll1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111l1l1l1_opy_(self, hook_type, bstack11111l1ll1l_opy_):
        def bstack11111l1ll11_opy_(arg=None):
            self.handler(hook_type, bstack11l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬῒ"))
            result = None
            try:
                bstack1ll1ll11l1l_opy_ = self._11111l1l111_opy_[(bstack11111l1ll1l_opy_, hook_type)]
                self.bstack11111ll1ll1_opy_(hook_type, bstack1ll1ll11l1l_opy_, (arg,))
                result = Result(result=bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ΐ"))
            except Exception as e:
                result = Result(result=bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ῔"), exception=e)
                self.handler(hook_type, bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ῕"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨῖ"), result)
        def bstack11111l1lll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪῗ"))
            result = None
            exception = None
            try:
                self.bstack11111ll1ll1_opy_(hook_type, self._11111l1l111_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫῘ"))
            except Exception as e:
                result = Result(result=bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬῙ"), exception=e)
                self.handler(hook_type, bstack11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬῚ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭Ί"), result)
        if hook_type in [bstack11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ῜"), bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ῝")]:
            return bstack11111l1lll1_opy_
        return bstack11111l1ll11_opy_
    def bstack11111l1l11l_opy_(self, bstack11111ll111l_opy_):
        def bstack11111ll11ll_opy_(this, *args, **kwargs):
            self.bstack11111l11lll_opy_(this, bstack11111ll111l_opy_)
            self._11111l1l1ll_opy_[bstack11111ll111l_opy_](this, *args, **kwargs)
        return bstack11111ll11ll_opy_