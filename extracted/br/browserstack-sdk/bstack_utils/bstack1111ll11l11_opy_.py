# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111ll1l11l1_opy_
from browserstack_sdk.bstack1l1lll11l_opy_ import bstack1l1ll111_opy_
def _1111l1lll1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111ll111ll_opy_:
    def __init__(self, handler):
        self._1111ll111l1_opy_ = {}
        self._1111l1lll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1ll111_opy_.version()
        if bstack111ll1l11l1_opy_(pytest_version, bstack11lllll_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣỨ")) >= 0:
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ứ")] = Module._register_setup_function_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỪ")] = Module._register_setup_module_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬừ")] = Class._register_setup_class_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧỬ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪử"))
            Module._register_setup_module_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỮ"))
            Class._register_setup_class_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩữ"))
            Class._register_setup_method_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỰ"))
        else:
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧự")] = Module._inject_setup_function_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ỳ")] = Module._inject_setup_module_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ỳ")] = Class._inject_setup_class_fixture
            self._1111ll111l1_opy_[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỴ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỵ"))
            Module._inject_setup_module_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪỶ"))
            Class._inject_setup_class_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪỷ"))
            Class._inject_setup_method_fixture = self.bstack1111ll1l11l_opy_(bstack11lllll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỸ"))
    def bstack1111ll11ll1_opy_(self, bstack1111ll1l1l1_opy_, hook_type):
        bstack1111l1lllll_opy_ = id(bstack1111ll1l1l1_opy_.__class__)
        if (bstack1111l1lllll_opy_, hook_type) in self._1111l1lll11_opy_:
            return
        meth = getattr(bstack1111ll1l1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111l1lll11_opy_[(bstack1111l1lllll_opy_, hook_type)] = meth
            setattr(bstack1111ll1l1l1_opy_, hook_type, self.bstack1111l1llll1_opy_(hook_type, bstack1111l1lllll_opy_))
    def bstack1111ll1111l_opy_(self, instance, bstack1111ll1l111_opy_):
        if bstack1111ll1l111_opy_ == bstack11lllll_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣỹ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢỺ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦỻ"))
        if bstack1111ll1l111_opy_ == bstack11lllll_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤỼ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣỽ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧỾ"))
        if bstack1111ll1l111_opy_ == bstack11lllll_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦỿ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥἀ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢἁ"))
        if bstack1111ll1l111_opy_ == bstack11lllll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣἂ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢἃ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11lllll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦἄ"))
    @staticmethod
    def bstack1111ll11l1l_opy_(hook_type, func, args):
        if hook_type in [bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩἅ"), bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ἆ")]:
            _1111l1lll1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111l1llll1_opy_(self, hook_type, bstack1111l1lllll_opy_):
        def bstack1111ll11111_opy_(arg=None):
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬἇ"))
            result = None
            try:
                bstack1lll111lll1_opy_ = self._1111l1lll11_opy_[(bstack1111l1lllll_opy_, hook_type)]
                self.bstack1111ll11l1l_opy_(hook_type, bstack1lll111lll1_opy_, (arg,))
                result = Result(result=bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ἀ"))
            except Exception as e:
                result = Result(result=bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἉ"), exception=e)
                self.handler(hook_type, bstack11lllll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧἊ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨἋ"), result)
        def bstack1111ll11lll_opy_(this, arg=None):
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪἌ"))
            result = None
            exception = None
            try:
                self.bstack1111ll11l1l_opy_(hook_type, self._1111l1lll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫἍ"))
            except Exception as e:
                result = Result(result=bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬἎ"), exception=e)
                self.handler(hook_type, bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬἏ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ἐ"), result)
        if hook_type in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧἑ"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫἒ")]:
            return bstack1111ll11lll_opy_
        return bstack1111ll11111_opy_
    def bstack1111ll1l11l_opy_(self, bstack1111ll1l111_opy_):
        def bstack1111ll1l1ll_opy_(this, *args, **kwargs):
            self.bstack1111ll1111l_opy_(this, bstack1111ll1l111_opy_)
            self._1111ll111l1_opy_[bstack1111ll1l111_opy_](this, *args, **kwargs)
        return bstack1111ll1l1ll_opy_