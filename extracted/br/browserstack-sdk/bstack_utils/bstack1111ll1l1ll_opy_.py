# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111ll1l1ll1_opy_
from browserstack_sdk.bstack1l1llll11_opy_ import bstack11lll111l1_opy_
def _1111ll1llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111ll1l11l_opy_:
    def __init__(self, handler):
        self._1111lll1l1l_opy_ = {}
        self._1111lll1l11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11lll111l1_opy_.version()
        if bstack111ll1l1ll1_opy_(pytest_version, bstack11l1111_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᷦ")) >= 0:
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷧ")] = Module._register_setup_function_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᷨ")] = Module._register_setup_module_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᷩ")] = Class._register_setup_class_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᷪ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷫ"))
            Module._register_setup_module_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᷬ"))
            Class._register_setup_class_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᷭ"))
            Class._register_setup_method_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᷮ"))
        else:
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᷯ")] = Module._inject_setup_function_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷰ")] = Module._inject_setup_module_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᷱ")] = Class._inject_setup_class_fixture
            self._1111lll1l1l_opy_[bstack11l1111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᷲ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᷳ"))
            Module._inject_setup_module_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᷴ"))
            Class._inject_setup_class_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᷵"))
            Class._inject_setup_method_fixture = self.bstack1111lll1111_opy_(bstack11l1111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᷶"))
    def bstack1111ll11ll1_opy_(self, bstack1111ll11lll_opy_, hook_type):
        bstack1111lll11ll_opy_ = id(bstack1111ll11lll_opy_.__class__)
        if (bstack1111lll11ll_opy_, hook_type) in self._1111lll1l11_opy_:
            return
        meth = getattr(bstack1111ll11lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111lll1l11_opy_[(bstack1111lll11ll_opy_, hook_type)] = meth
            setattr(bstack1111ll11lll_opy_, hook_type, self.bstack1111ll1ll1l_opy_(hook_type, bstack1111lll11ll_opy_))
    def bstack1111ll1lll1_opy_(self, instance, bstack1111ll1l111_opy_):
        if bstack1111ll1l111_opy_ == bstack11l1111_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᷷"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮᷸ࠣ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲ᷹ࠧ"))
        if bstack1111ll1l111_opy_ == bstack11l1111_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧ᷺ࠥ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤ᷻"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨ᷼"))
        if bstack1111ll1l111_opy_ == bstack11l1111_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩ᷽ࠧ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦ᷾"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳ᷿ࠣ"))
        if bstack1111ll1l111_opy_ == bstack11l1111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤḀ"):
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣḁ"))
            self.bstack1111ll11ll1_opy_(instance.obj, bstack11l1111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧḂ"))
    @staticmethod
    def bstack1111lll111l_opy_(hook_type, func, args):
        if hook_type in [bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪḃ"), bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧḄ")]:
            _1111ll1llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111ll1ll1l_opy_(self, hook_type, bstack1111lll11ll_opy_):
        def bstack1111lll11l1_opy_(arg=None):
            self.handler(hook_type, bstack11l1111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ḅ"))
            result = None
            try:
                bstack1l11lll1lll_opy_ = self._1111lll1l11_opy_[(bstack1111lll11ll_opy_, hook_type)]
                self.bstack1111lll111l_opy_(hook_type, bstack1l11lll1lll_opy_, (arg,))
                result = Result(result=bstack11l1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧḆ"))
            except Exception as e:
                result = Result(result=bstack11l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨḇ"), exception=e)
                self.handler(hook_type, bstack11l1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨḈ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩḉ"), result)
        def bstack1111ll1l1l1_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫḊ"))
            result = None
            exception = None
            try:
                self.bstack1111lll111l_opy_(hook_type, self._1111lll1l11_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬḋ"))
            except Exception as e:
                result = Result(result=bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ḍ"), exception=e)
                self.handler(hook_type, bstack11l1111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ḍ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧḎ"), result)
        if hook_type in [bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨḏ"), bstack11l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬḐ")]:
            return bstack1111ll1l1l1_opy_
        return bstack1111lll11l1_opy_
    def bstack1111lll1111_opy_(self, bstack1111ll1l111_opy_):
        def bstack1111ll1ll11_opy_(this, *args, **kwargs):
            self.bstack1111ll1lll1_opy_(this, bstack1111ll1l111_opy_)
            self._1111lll1l1l_opy_[bstack1111ll1l111_opy_](this, *args, **kwargs)
        return bstack1111ll1ll11_opy_