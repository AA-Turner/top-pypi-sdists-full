# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111ll11l1l1_opy_
from browserstack_sdk.bstack111l1l1ll1_opy_ import bstack111ll1l1ll_opy_
def _1111ll11lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111ll1ll11_opy_:
    def __init__(self, handler):
        self._1111ll1lll1_opy_ = {}
        self._1111lll1l1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack111ll1l1ll_opy_.version()
        if bstack111ll11l1l1_opy_(pytest_version, bstack1l1111_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧỂ")) >= 0:
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪể")] = Module._register_setup_function_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỄ")] = Module._register_setup_module_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩễ")] = Class._register_setup_class_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỆ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧệ"))
            Module._register_setup_module_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ỉ"))
            Class._register_setup_class_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ỉ"))
            Class._register_setup_method_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỊ"))
        else:
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫị")] = Module._inject_setup_function_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪỌ")] = Module._inject_setup_module_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪọ")] = Class._inject_setup_class_fixture
            self._1111ll1lll1_opy_[bstack1l1111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỎ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỏ"))
            Module._inject_setup_module_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧỐ"))
            Class._inject_setup_class_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧố"))
            Class._inject_setup_method_fixture = self.bstack1111ll1llll_opy_(bstack1l1111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỒ"))
    def bstack1111ll1l111_opy_(self, bstack1111lll11ll_opy_, hook_type):
        bstack1111lll111l_opy_ = id(bstack1111lll11ll_opy_.__class__)
        if (bstack1111lll111l_opy_, hook_type) in self._1111lll1l1l_opy_:
            return
        meth = getattr(bstack1111lll11ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111lll1l1l_opy_[(bstack1111lll111l_opy_, hook_type)] = meth
            setattr(bstack1111lll11ll_opy_, hook_type, self.bstack1111lll1l11_opy_(hook_type, bstack1111lll111l_opy_))
    def bstack1111lll11l1_opy_(self, instance, bstack1111ll11ll1_opy_):
        if bstack1111ll11ll1_opy_ == bstack1l1111_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧồ"):
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦỔ"))
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣổ"))
        if bstack1111ll11ll1_opy_ == bstack1l1111_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨỖ"):
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧỗ"))
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤỘ"))
        if bstack1111ll11ll1_opy_ == bstack1l1111_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣộ"):
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢỚ"))
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦớ"))
        if bstack1111ll11ll1_opy_ == bstack1l1111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧỜ"):
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦờ"))
            self.bstack1111ll1l111_opy_(instance.obj, bstack1l1111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣỞ"))
    @staticmethod
    def bstack1111ll1ll1l_opy_(hook_type, func, args):
        if hook_type in [bstack1l1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ở"), bstack1l1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪỠ")]:
            _1111ll11lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111lll1l11_opy_(self, hook_type, bstack1111lll111l_opy_):
        def bstack1111ll1l1ll_opy_(arg=None):
            self.handler(hook_type, bstack1l1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩỡ"))
            result = None
            try:
                bstack1lll111ll1l_opy_ = self._1111lll1l1l_opy_[(bstack1111lll111l_opy_, hook_type)]
                self.bstack1111ll1ll1l_opy_(hook_type, bstack1lll111ll1l_opy_, (arg,))
                result = Result(result=bstack1l1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪỢ"))
            except Exception as e:
                result = Result(result=bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫợ"), exception=e)
                self.handler(hook_type, bstack1l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫỤ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬụ"), result)
        def bstack1111lll1111_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧỦ"))
            result = None
            exception = None
            try:
                self.bstack1111ll1ll1l_opy_(hook_type, self._1111lll1l1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨủ"))
            except Exception as e:
                result = Result(result=bstack1l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩỨ"), exception=e)
                self.handler(hook_type, bstack1l1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩứ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪỪ"), result)
        if hook_type in [bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫừ"), bstack1l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨỬ")]:
            return bstack1111lll1111_opy_
        return bstack1111ll1l1ll_opy_
    def bstack1111ll1llll_opy_(self, bstack1111ll11ll1_opy_):
        def bstack1111ll1l1l1_opy_(this, *args, **kwargs):
            self.bstack1111lll11l1_opy_(this, bstack1111ll11ll1_opy_)
            self._1111ll1lll1_opy_[bstack1111ll11ll1_opy_](this, *args, **kwargs)
        return bstack1111ll1l1l1_opy_