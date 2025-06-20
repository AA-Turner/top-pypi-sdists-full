# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11l11lll11_opy_
import subprocess
from browserstack_sdk.bstack1l1ll1l1l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11ll1l1l1l_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack111l11l1l_opy_
from bstack_utils.constants import bstack1111l1ll11_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack1lll1lll1_opy_
class bstack1l111l1l_opy_:
    def __init__(self, args, logger, bstack1111ll1l11_opy_, bstack1111l1l1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll1l11_opy_ = []
        self.bstack11111ll11l_opy_ = None
        self.bstack11l111l1ll_opy_ = []
        self.bstack11111lllll_opy_ = self.bstack11111l1l1_opy_()
        self.bstack11lll1111l_opy_ = -1
    def bstack1ll11ll1l_opy_(self, bstack11111llll1_opy_):
        self.parse_args()
        self.bstack1111ll11ll_opy_()
        self.bstack1111l1llll_opy_(bstack11111llll1_opy_)
        self.bstack1111l111l1_opy_()
    def bstack1l111l1l1_opy_(self):
        bstack1l111l1l1l_opy_ = bstack1lll1lll1_opy_.bstack1lll11ll_opy_(self.bstack1111ll1l11_opy_, self.logger)
        if bstack1l111l1l1l_opy_ is None:
            self.logger.warn(bstack11ll11_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨတ"))
            return
        bstack11111l1ll1_opy_ = False
        bstack1l111l1l1l_opy_.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧထ"), bstack1l111l1l1l_opy_.bstack1111111l1_opy_())
        start_time = time.time()
        if bstack1l111l1l1l_opy_.bstack1111111l1_opy_():
            test_files = self.bstack1111l11l11_opy_()
            bstack11111l1ll1_opy_ = True
            bstack1111l1l111_opy_ = bstack1l111l1l1l_opy_.bstack1111l1ll1l_opy_(test_files)
            if bstack1111l1l111_opy_:
                self.bstack11ll1l11_opy_ = [os.path.normpath(item).replace(bstack11ll11_opy_ (u"ࠬࡢ࡜ࠨဒ"), bstack11ll11_opy_ (u"࠭࠯ࠨဓ")) for item in bstack1111l1l111_opy_]
                self.__1111l111ll_opy_()
                bstack1l111l1l1l_opy_.bstack1111ll111l_opy_(bstack11111l1ll1_opy_)
                self.logger.info(bstack11ll11_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧန").format(self.bstack11ll1l11_opy_))
            else:
                self.logger.info(bstack11ll11_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨပ"))
        bstack1l111l1l1l_opy_.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧဖ"), int((time.time() - start_time) * 1000)) # bstack11111l1lll_opy_ to bstack11111ll111_opy_
    def __1111l111ll_opy_(self):
        bstack11ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡣ࡯ࡰࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࠠࡴࡧ࡯ࡪ࠳ࡧࡲࡨࡵࠣࡻ࡮ࡺࡨࠡࡵࡨࡰ࡫࠴ࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕ࡮࡭ࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡹࡳࡁࠠࡢ࡮࡯ࠤࡴࡺࡨࡦࡴࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡡࡳࡧࠣࡴࡷ࡫ࡳࡦࡴࡹࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦဗ")
        bstack11111ll1l1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack11ll11_opy_ (u"ࠫ࠳ࡶࡹࠨဘ")) and os.path.exists(arg))]
        self.args = self.bstack11ll1l11_opy_ + bstack11111ll1l1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1lll1_opy_():
        import importlib
        if getattr(importlib, bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪမ"), False):
            bstack1111ll1111_opy_ = importlib.find_loader(bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨယ"))
        else:
            bstack1111ll1111_opy_ = importlib.util.find_spec(bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩရ"))
    def bstack1111l1111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11lll1111l_opy_ = -1
        if self.bstack1111l1l1ll_opy_ and bstack11ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨလ") in self.bstack1111ll1l11_opy_:
            self.bstack11lll1111l_opy_ = int(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩဝ")])
        try:
            bstack1111l11lll_opy_ = [bstack11ll11_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬသ"), bstack11ll11_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧဟ"), bstack11ll11_opy_ (u"ࠬ࠳ࡰࠨဠ")]
            if self.bstack11lll1111l_opy_ >= 0:
                bstack1111l11lll_opy_.extend([bstack11ll11_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧအ"), bstack11ll11_opy_ (u"ࠧ࠮ࡰࠪဢ")])
            for arg in bstack1111l11lll_opy_:
                self.bstack1111l1111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111ll11ll_opy_(self):
        bstack11111ll11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
        return bstack11111ll11l_opy_
    def bstack11l11llll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1lll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11ll1l1l1l_opy_)
    def bstack1111l1llll_opy_(self, bstack11111llll1_opy_):
        bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
        if bstack11111llll1_opy_:
            self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬဣ"))
            self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠩࡗࡶࡺ࡫ࠧဤ"))
        if bstack1l1ll1llll_opy_.bstack1111ll11l1_opy_():
            self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩဥ"))
            self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"࡙ࠫࡸࡵࡦࠩဦ"))
        self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠬ࠳ࡰࠨဧ"))
        self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫဨ"))
        self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩဩ"))
        self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨဪ"))
        if self.bstack11lll1111l_opy_ > 1:
            self.bstack11111ll11l_opy_.append(bstack11ll11_opy_ (u"ࠩ࠰ࡲࠬါ"))
            self.bstack11111ll11l_opy_.append(str(self.bstack11lll1111l_opy_))
    def bstack1111l111l1_opy_(self):
        if bstack111l11l1l_opy_.bstack1llll1ll11_opy_(self.bstack1111ll1l11_opy_):
             self.bstack11111ll11l_opy_ += [
                bstack1111l1ll11_opy_.get(bstack11ll11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩာ")), str(bstack111l11l1l_opy_.bstack11ll1llll_opy_(self.bstack1111ll1l11_opy_)),
                bstack1111l1ll11_opy_.get(bstack11ll11_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪိ")), str(bstack1111l1ll11_opy_.get(bstack11ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪီ")))
            ]
    def bstack11111lll11_opy_(self):
        bstack11l111l1ll_opy_ = []
        for spec in self.bstack11ll1l11_opy_:
            bstack11l111l11l_opy_ = [spec]
            bstack11l111l11l_opy_ += self.bstack11111ll11l_opy_
            bstack11l111l1ll_opy_.append(bstack11l111l11l_opy_)
        self.bstack11l111l1ll_opy_ = bstack11l111l1ll_opy_
        return bstack11l111l1ll_opy_
    def bstack11111l1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111lllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11111lllll_opy_ = False
        return self.bstack11111lllll_opy_
    def bstack11lll1l1_opy_(self):
        bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠨࡵࠣ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠤ࡫ࡲࡡࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤု")
        try:
            self.logger.info(bstack11ll11_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࡵࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥူ"))
            bstack1111l11111_opy_ = [bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣေ"), *self.bstack11111ll11l_opy_, bstack11ll11_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥဲ")]
            result = subprocess.run(bstack1111l11111_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣဳ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack11ll11_opy_ (u"ࠦࡁࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠣဴ"))
            self.logger.info(bstack11ll11_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥဵ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥံ").format(e))
            return 0
    def bstack1ll1111ll_opy_(self, bstack11111ll1ll_opy_, bstack1ll11ll1l_opy_):
        bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍ့ࠧ")] = self.bstack1111ll1l11_opy_
        multiprocessing.set_start_method(bstack11ll11_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧး"))
        bstack11ll1l1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l1l11l_opy_ = manager.list()
        if bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ္ࠬ") in self.bstack1111ll1l11_opy_:
            for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ်࠭")]):
                bstack11ll1l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111ll1ll_opy_,
                                                            args=(self.bstack11111ll11l_opy_, bstack1ll11ll1l_opy_, bstack1111l1l11l_opy_)))
            bstack1111l1l1l1_opy_ = len(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧျ")])
        else:
            bstack11ll1l1ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111ll1ll_opy_,
                                                        args=(self.bstack11111ll11l_opy_, bstack1ll11ll1l_opy_, bstack1111l1l11l_opy_)))
            bstack1111l1l1l1_opy_ = 1
        i = 0
        for t in bstack11ll1l1ll_opy_:
            os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬြ")] = str(i)
            if bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩွ") in self.bstack1111ll1l11_opy_:
                os.environ[bstack11ll11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨှ")] = json.dumps(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဿ")][i % bstack1111l1l1l1_opy_])
            i += 1
            t.start()
        for t in bstack11ll1l1ll_opy_:
            t.join()
        return list(bstack1111l1l11l_opy_)
    @staticmethod
    def bstack1l1l1ll11l_opy_(driver, bstack1111l11ll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭၀"), None)
        if item and getattr(item, bstack11ll11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬ၁"), None) and not getattr(item, bstack11ll11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭၂"), False):
            logger.info(
                bstack11ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦ၃"))
            bstack1111l11l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l11lll11_opy_.bstack1ll1l1l111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111l11l11_opy_(self):
        bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ၄")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack11ll11_opy_ (u"ࠧ࠯ࡲࡼࠫ၅")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files