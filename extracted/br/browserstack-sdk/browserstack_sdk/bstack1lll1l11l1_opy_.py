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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1lll11l1_opy_
import subprocess
from browserstack_sdk.bstack1ll11lll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1l11l_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1ll1lll1_opy_
from bstack_utils.constants import bstack1111l11111_opy_
from bstack_utils.bstack11l1ll111l_opy_ import bstack1ll111ll1_opy_
class bstack1l1lllllll_opy_:
    def __init__(self, args, logger, bstack1111l1l1l1_opy_, bstack1111l1ll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lllll1ll1_opy_ = []
        self.bstack11111ll11l_opy_ = None
        self.bstack11l11ll11_opy_ = []
        self.bstack11111ll1ll_opy_ = self.bstack111111ll_opy_()
        self.bstack11l1l1l1_opy_ = -1
    def bstack1lll1ll1_opy_(self, bstack1111ll11ll_opy_):
        self.parse_args()
        self.bstack1111l1l1ll_opy_()
        self.bstack11111lll1l_opy_(bstack1111ll11ll_opy_)
        self.bstack11111ll111_opy_()
    def bstack1lll111l1_opy_(self):
        bstack11l1ll111l_opy_ = bstack1ll111ll1_opy_.bstack1lllll111l_opy_(self.bstack1111l1l1l1_opy_, self.logger)
        if bstack11l1ll111l_opy_ is None:
            self.logger.warn(bstack11ll1l1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢထ"))
            return
        bstack1111l1llll_opy_ = False
        bstack11l1ll111l_opy_.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠧ࡫࡮ࡢࡤ࡯ࡩࡩࠨဒ"), bstack11l1ll111l_opy_.bstack1ll1lll11_opy_())
        start_time = time.time()
        if bstack11l1ll111l_opy_.bstack1ll1lll11_opy_():
            test_files = self.bstack11111lllll_opy_()
            bstack1111l1llll_opy_ = True
            bstack1111l1l11l_opy_ = bstack11l1ll111l_opy_.bstack1111ll1111_opy_(test_files)
            if bstack1111l1l11l_opy_:
                self.bstack1lllll1ll1_opy_ = [os.path.normpath(item).replace(bstack11ll1l1_opy_ (u"࠭࡜࡝ࠩဓ"), bstack11ll1l1_opy_ (u"ࠧ࠰ࠩန")) for item in bstack1111l1l11l_opy_]
                self.__11111l1ll1_opy_()
                bstack11l1ll111l_opy_.bstack11111llll1_opy_(bstack1111l1llll_opy_)
                self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡖࡨࡷࡹࡹࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡹࡸ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨပ").format(self.bstack1lllll1ll1_opy_))
            else:
                self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡑࡳࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺࡩࡷ࡫ࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡦࡾࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢဖ"))
        bstack11l1ll111l_opy_.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠥࡸ࡮ࡳࡥࡕࡣ࡮ࡩࡳ࡚࡯ࡂࡲࡳࡰࡾࠨဗ"), int((time.time() - start_time) * 1000)) # bstack1111l1lll1_opy_ to bstack1111l111l1_opy_
    def __11111l1ll1_opy_(self):
        bstack11ll1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡴࡱࡧࡣࡦࠢࡤࡰࡱࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࠡࡵࡨࡰ࡫࠴ࡡࡳࡩࡶࠤࡼ࡯ࡴࡩࠢࡶࡩࡱ࡬࠮ࡴࡲࡨࡧࡤ࡬ࡩ࡭ࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡏ࡯࡮ࡼࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡺࡴ࠻ࠡࡣ࡯ࡰࠥࡵࡴࡩࡧࡵࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡢࡴࡨࠤࡵࡸࡥࡴࡧࡵࡺࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧဘ")
        bstack1111l1ll1l_opy_ = [arg for arg in self.args if not (arg.endswith(bstack11ll1l1_opy_ (u"ࠬ࠴ࡰࡺࠩမ")) and os.path.exists(arg))]
        self.args = self.bstack1lllll1ll1_opy_ + bstack1111l1ll1l_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l111ll_opy_():
        import importlib
        if getattr(importlib, bstack11ll1l1_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫယ"), False):
            bstack1111l11ll1_opy_ = importlib.find_loader(bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩရ"))
        else:
            bstack1111l11ll1_opy_ = importlib.util.find_spec(bstack11ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪလ"))
    def bstack1111ll11l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1l1l1_opy_ = -1
        if self.bstack1111l1ll11_opy_ and bstack11ll1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩဝ") in self.bstack1111l1l1l1_opy_:
            self.bstack11l1l1l1_opy_ = int(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪသ")])
        try:
            bstack1111ll111l_opy_ = [bstack11ll1l1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ဟ"), bstack11ll1l1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨဠ"), bstack11ll1l1_opy_ (u"࠭࠭ࡱࠩအ")]
            if self.bstack11l1l1l1_opy_ >= 0:
                bstack1111ll111l_opy_.extend([bstack11ll1l1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨဢ"), bstack11ll1l1_opy_ (u"ࠨ࠯ࡱࠫဣ")])
            for arg in bstack1111ll111l_opy_:
                self.bstack1111ll11l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l1l1ll_opy_(self):
        bstack11111ll11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
        return bstack11111ll11l_opy_
    def bstack11l11ll111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l111ll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1l11l_opy_)
    def bstack11111lll1l_opy_(self, bstack1111ll11ll_opy_):
        bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
        if bstack1111ll11ll_opy_:
            self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ဤ"))
            self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠪࡘࡷࡻࡥࠨဥ"))
        if bstack1111ll111_opy_.bstack1111l1111l_opy_():
            self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪဦ"))
            self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"࡚ࠬࡲࡶࡧࠪဧ"))
        self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"࠭࠭ࡱࠩဨ"))
        self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬဩ"))
        self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪဪ"))
        self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩါ"))
        if self.bstack11l1l1l1_opy_ > 1:
            self.bstack11111ll11l_opy_.append(bstack11ll1l1_opy_ (u"ࠪ࠱ࡳ࠭ာ"))
            self.bstack11111ll11l_opy_.append(str(self.bstack11l1l1l1_opy_))
    def bstack11111ll111_opy_(self):
        if bstack1ll1lll1_opy_.bstack1lll1l1l11_opy_(self.bstack1111l1l1l1_opy_):
             self.bstack11111ll11l_opy_ += [
                bstack1111l11111_opy_.get(bstack11ll1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪိ")), str(bstack1ll1lll1_opy_.bstack1ll11l1111_opy_(self.bstack1111l1l1l1_opy_)),
                bstack1111l11111_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫီ")), str(bstack1111l11111_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫု")))
            ]
    def bstack1111ll1l11_opy_(self):
        bstack11l11ll11_opy_ = []
        for spec in self.bstack1lllll1ll1_opy_:
            bstack11llll11_opy_ = [spec]
            bstack11llll11_opy_ += self.bstack11111ll11l_opy_
            bstack11l11ll11_opy_.append(bstack11llll11_opy_)
        self.bstack11l11ll11_opy_ = bstack11l11ll11_opy_
        return bstack11l11ll11_opy_
    def bstack111111ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111ll1ll_opy_ = True
            return True
        except Exception as e:
            self.bstack11111ll1ll_opy_ = False
        return self.bstack11111ll1ll_opy_
    def bstack11l1llll_opy_(self):
        bstack11ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡉࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦ࡯ࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠩࡶࠤ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠥ࡬࡬ࡢࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥူ")
        try:
            self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࡶࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦေ"))
            bstack1111l11lll_opy_ = [bstack11ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤဲ"), *self.bstack11111ll11l_opy_, bstack11ll1l1_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦဳ")]
            result = subprocess.run(bstack1111l11lll_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤဴ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack11ll1l1_opy_ (u"ࠧࡂࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠤဵ"))
            self.logger.info(bstack11ll1l1_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦံ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀ့ࠦ").format(e))
            return 0
    def bstack1111111l_opy_(self, bstack11111l1lll_opy_, bstack1lll1ll1_opy_):
        bstack1lll1ll1_opy_[bstack11ll1l1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨး")] = self.bstack1111l1l1l1_opy_
        multiprocessing.set_start_method(bstack11ll1l1_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨ္"))
        bstack1ll111ll1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111lll11_opy_ = manager.list()
        if bstack11ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ်࠭") in self.bstack1111l1l1l1_opy_:
            for index, platform in enumerate(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧျ")]):
                bstack1ll111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111l1lll_opy_,
                                                            args=(self.bstack11111ll11l_opy_, bstack1lll1ll1_opy_, bstack11111lll11_opy_)))
            bstack1111l11l11_opy_ = len(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨြ")])
        else:
            bstack1ll111ll1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111l1lll_opy_,
                                                        args=(self.bstack11111ll11l_opy_, bstack1lll1ll1_opy_, bstack11111lll11_opy_)))
            bstack1111l11l11_opy_ = 1
        i = 0
        for t in bstack1ll111ll1l_opy_:
            os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ွ")] = str(i)
            if bstack11ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪှ") in self.bstack1111l1l1l1_opy_:
                os.environ[bstack11ll1l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩဿ")] = json.dumps(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၀")][i % bstack1111l11l11_opy_])
            i += 1
            t.start()
        for t in bstack1ll111ll1l_opy_:
            t.join()
        return list(bstack11111lll11_opy_)
    @staticmethod
    def bstack1l1lllll11_opy_(driver, bstack1111l1l111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ၁"), None)
        if item and getattr(item, bstack11ll1l1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭၂"), None) and not getattr(item, bstack11ll1l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ၃"), False):
            logger.info(
                bstack11ll1l1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧ၄"))
            bstack11111ll1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll11l1_opy_.bstack11l1l1l1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11111lllll_opy_(self):
        bstack11ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ၅")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack11ll1l1_opy_ (u"ࠨ࠰ࡳࡽࠬ၆")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files