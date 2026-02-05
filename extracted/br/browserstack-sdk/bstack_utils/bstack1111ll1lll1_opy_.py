# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111ll11l1l1_opy_
from browserstack_sdk.bstack1l11ll1111_opy_ import bstack11l111l11l_opy_
def _1111ll1llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111ll1l11l_opy_:
    def __init__(self, handler):
        self._1111lll11l1_opy_ = {}
        self._1111ll1l111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l111l11l_opy_.version()
        if bstack111ll11l1l1_opy_(pytest_version, bstack11l1ll1_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦỈ")) >= 0:
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỉ")] = Module._register_setup_function_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỊ")] = Module._register_setup_module_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨị")] = Class._register_setup_class_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪỌ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ọ"))
            Module._register_setup_module_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỎ"))
            Class._register_setup_class_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỏ"))
            Class._register_setup_method_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧỐ"))
        else:
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪố")] = Module._inject_setup_function_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỒ")] = Module._inject_setup_module_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩồ")] = Class._inject_setup_class_fixture
            self._1111lll11l1_opy_[bstack11l1ll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỔ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧổ"))
            Module._inject_setup_module_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ỗ"))
            Class._inject_setup_class_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ỗ"))
            Class._inject_setup_method_fixture = self.bstack1111ll11lll_opy_(bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỘ"))
    def bstack1111lll1111_opy_(self, bstack1111ll1ll1l_opy_, hook_type):
        bstack1111ll111ll_opy_ = id(bstack1111ll1ll1l_opy_.__class__)
        if (bstack1111ll111ll_opy_, hook_type) in self._1111ll1l111_opy_:
            return
        meth = getattr(bstack1111ll1ll1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111ll1l111_opy_[(bstack1111ll111ll_opy_, hook_type)] = meth
            setattr(bstack1111ll1ll1l_opy_, hook_type, self.bstack1111ll11l11_opy_(hook_type, bstack1111ll111ll_opy_))
    def bstack1111ll1l1l1_opy_(self, instance, bstack1111ll1ll11_opy_):
        if bstack1111ll1ll11_opy_ == bstack11l1ll1_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦộ"):
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥỚ"))
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢớ"))
        if bstack1111ll1ll11_opy_ == bstack11l1ll1_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧỜ"):
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦờ"))
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣỞ"))
        if bstack1111ll1ll11_opy_ == bstack11l1ll1_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢở"):
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨỠ"))
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥỡ"))
        if bstack1111ll1ll11_opy_ == bstack11l1ll1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦỢ"):
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥợ"))
            self.bstack1111lll1111_opy_(instance.obj, bstack11l1ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢỤ"))
    @staticmethod
    def bstack1111lll111l_opy_(hook_type, func, args):
        if hook_type in [bstack11l1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬụ"), bstack11l1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩỦ")]:
            _1111ll1llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111ll11l11_opy_(self, hook_type, bstack1111ll111ll_opy_):
        def bstack1111ll11l1l_opy_(arg=None):
            self.handler(hook_type, bstack11l1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨủ"))
            result = None
            try:
                bstack1lll11l1lll_opy_ = self._1111ll1l111_opy_[(bstack1111ll111ll_opy_, hook_type)]
                self.bstack1111lll111l_opy_(hook_type, bstack1lll11l1lll_opy_, (arg,))
                result = Result(result=bstack11l1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩỨ"))
            except Exception as e:
                result = Result(result=bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪứ"), exception=e)
                self.handler(hook_type, bstack11l1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪỪ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫừ"), result)
        def bstack1111ll11ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭Ử"))
            result = None
            exception = None
            try:
                self.bstack1111lll111l_opy_(hook_type, self._1111ll1l111_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧử"))
            except Exception as e:
                result = Result(result=bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨỮ"), exception=e)
                self.handler(hook_type, bstack11l1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨữ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩỰ"), result)
        if hook_type in [bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪự"), bstack11l1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧỲ")]:
            return bstack1111ll11ll1_opy_
        return bstack1111ll11l1l_opy_
    def bstack1111ll11lll_opy_(self, bstack1111ll1ll11_opy_):
        def bstack1111ll1l1ll_opy_(this, *args, **kwargs):
            self.bstack1111ll1l1l1_opy_(this, bstack1111ll1ll11_opy_)
            self._1111lll11l1_opy_[bstack1111ll1ll11_opy_](this, *args, **kwargs)
        return bstack1111ll1l1ll_opy_