# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111l1lllll_opy_
from browserstack_sdk.bstack1lllllll1_opy_ import bstack11l11111l_opy_
def _1lll1ll11lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lll1ll11l1l_opy_:
    def __init__(self, handler):
        self._1lll1ll1ll11_opy_ = {}
        self._1lll1ll1llll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l11111l_opy_.version()
        if bstack1111l1lllll_opy_(pytest_version, bstack111ll_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦ⑱")) >= 0:
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⑲")] = Module._register_setup_function_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⑳")] = Module._register_setup_module_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⑴")] = Class._register_setup_class_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑵")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⑶"))
            Module._register_setup_module_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⑷"))
            Class._register_setup_class_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⑸"))
            Class._register_setup_method_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑹"))
        else:
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑺")] = Module._inject_setup_function_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⑻")] = Module._inject_setup_module_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⑼")] = Class._inject_setup_class_fixture
            self._1lll1ll1ll11_opy_[bstack111ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⑽")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑾"))
            Module._inject_setup_module_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⑿"))
            Class._inject_setup_class_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⒀"))
            Class._inject_setup_method_fixture = self.bstack1lll1ll11l11_opy_(bstack111ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⒁"))
    def bstack1lll1ll11111_opy_(self, bstack1lll1ll1l1ll_opy_, hook_type):
        bstack1lll1ll1l11l_opy_ = id(bstack1lll1ll1l1ll_opy_.__class__)
        if (bstack1lll1ll1l11l_opy_, hook_type) in self._1lll1ll1llll_opy_:
            return
        meth = getattr(bstack1lll1ll1l1ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lll1ll1llll_opy_[(bstack1lll1ll1l11l_opy_, hook_type)] = meth
            setattr(bstack1lll1ll1l1ll_opy_, hook_type, self.bstack1lll1ll1ll1l_opy_(hook_type, bstack1lll1ll1l11l_opy_))
    def bstack1lll1ll1l111_opy_(self, instance, bstack1lll1ll1l1l1_opy_):
        if bstack1lll1ll1l1l1_opy_ == bstack111ll_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ⒂"):
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ⒃"))
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢ⒄"))
        if bstack1lll1ll1l1l1_opy_ == bstack111ll_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ⒅"):
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦ⒆"))
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣ⒇"))
        if bstack1lll1ll1l1l1_opy_ == bstack111ll_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ⒈"):
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨ⒉"))
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥ⒊"))
        if bstack1lll1ll1l1l1_opy_ == bstack111ll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ⒋"):
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥ⒌"))
            self.bstack1lll1ll11111_opy_(instance.obj, bstack111ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢ⒍"))
    @staticmethod
    def bstack1lll1ll111l1_opy_(hook_type, func, args):
        if hook_type in [bstack111ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⒎"), bstack111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⒏")]:
            _1lll1ll11lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lll1ll1ll1l_opy_(self, hook_type, bstack1lll1ll1l11l_opy_):
        def bstack1lll1ll1lll1_opy_(arg=None):
            self.handler(hook_type, bstack111ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⒐"))
            result = None
            try:
                bstack1l1ll11l1l1_opy_ = self._1lll1ll1llll_opy_[(bstack1lll1ll1l11l_opy_, hook_type)]
                self.bstack1lll1ll111l1_opy_(hook_type, bstack1l1ll11l1l1_opy_, (arg,))
                result = Result(result=bstack111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⒑"))
            except Exception as e:
                result = Result(result=bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⒒"), exception=e)
                self.handler(hook_type, bstack111ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⒓"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⒔"), result)
        def bstack1lll1ll1111l_opy_(this, arg=None):
            self.handler(hook_type, bstack111ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⒕"))
            result = None
            exception = None
            try:
                self.bstack1lll1ll111l1_opy_(hook_type, self._1lll1ll1llll_opy_[hook_type], (this, arg))
                result = Result(result=bstack111ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⒖"))
            except Exception as e:
                result = Result(result=bstack111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⒗"), exception=e)
                self.handler(hook_type, bstack111ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⒘"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⒙"), result)
        if hook_type in [bstack111ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ⒚"), bstack111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⒛")]:
            return bstack1lll1ll1111l_opy_
        return bstack1lll1ll1lll1_opy_
    def bstack1lll1ll11l11_opy_(self, bstack1lll1ll1l1l1_opy_):
        def bstack1lll1ll111ll_opy_(this, *args, **kwargs):
            self.bstack1lll1ll1l111_opy_(this, bstack1lll1ll1l1l1_opy_)
            self._1lll1ll1ll11_opy_[bstack1lll1ll1l1l1_opy_](this, *args, **kwargs)
        return bstack1lll1ll111ll_opy_