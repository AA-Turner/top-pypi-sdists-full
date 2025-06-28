# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l11ll1lll_opy_
import subprocess
from browserstack_sdk.bstack1111ll1l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l111l11ll_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11l1ll1l1_opy_
from bstack_utils.constants import bstack11111l1lll_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack11l111lll1_opy_
class bstack1llll111_opy_:
    def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1111lll_opy_ = []
        self.bstack1111l111l1_opy_ = None
        self.bstack11ll1llll_opy_ = []
        self.bstack11111lllll_opy_ = self.bstack1l1llll11_opy_()
        self.bstack111l11l1_opy_ = -1
    def bstack1ll11l1l_opy_(self, bstack1111ll1111_opy_):
        self.parse_args()
        self.bstack1111ll1l11_opy_()
        self.bstack1111l11l11_opy_(bstack1111ll1111_opy_)
        self.bstack1111l1l111_opy_()
    def bstack1llllll11l_opy_(self):
        bstack1l1l111ll_opy_ = bstack11l111lll1_opy_.bstack11ll1l11l_opy_(self.bstack11111llll1_opy_, self.logger)
        if bstack1l1l111ll_opy_ is None:
            self.logger.warn(bstack1l1ll1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢထ"))
            return
        bstack1111l1ll11_opy_ = False
        bstack1l1l111ll_opy_.bstack1111l111ll_opy_(bstack1l1ll1_opy_ (u"ࠧ࡫࡮ࡢࡤ࡯ࡩࡩࠨဒ"), bstack1l1l111ll_opy_.bstack1l1l1ll1_opy_())
        start_time = time.time()
        if bstack1l1l111ll_opy_.bstack1l1l1ll1_opy_():
            test_files = self.bstack11111ll11l_opy_()
            bstack1111l1ll11_opy_ = True
            bstack1111l11l1l_opy_ = bstack1l1l111ll_opy_.bstack1111l1llll_opy_(test_files)
            if bstack1111l11l1l_opy_:
                self.bstack1l1111lll_opy_ = [os.path.normpath(item).replace(bstack1l1ll1_opy_ (u"࠭࡜࡝ࠩဓ"), bstack1l1ll1_opy_ (u"ࠧ࠰ࠩန")) for item in bstack1111l11l1l_opy_]
                self.__1111l1l1l1_opy_()
                bstack1l1l111ll_opy_.bstack1111l1l11l_opy_(bstack1111l1ll11_opy_)
                self.logger.info(bstack1l1ll1_opy_ (u"ࠣࡖࡨࡷࡹࡹࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡹࡸ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨပ").format(self.bstack1l1111lll_opy_))
            else:
                self.logger.info(bstack1l1ll1_opy_ (u"ࠤࡑࡳࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺࡩࡷ࡫ࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡦࡾࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢဖ"))
        bstack1l1l111ll_opy_.bstack1111l111ll_opy_(bstack1l1ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡕࡣ࡮ࡩࡳ࡚࡯ࡂࡲࡳࡰࡾࠨဗ"), int((time.time() - start_time) * 1000)) # bstack11111ll1l1_opy_ to bstack1111l1ll1l_opy_
    def __1111l1l1l1_opy_(self):
        bstack1l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡴࡱࡧࡣࡦࠢࡤࡰࡱࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࠡࡵࡨࡰ࡫࠴ࡡࡳࡩࡶࠤࡼ࡯ࡴࡩࠢࡶࡩࡱ࡬࠮ࡴࡲࡨࡧࡤ࡬ࡩ࡭ࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡏ࡯࡮ࡼࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡺࡴ࠻ࠡࡣ࡯ࡰࠥࡵࡴࡩࡧࡵࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡢࡴࡨࠤࡵࡸࡥࡴࡧࡵࡺࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧဘ")
        bstack1111l11111_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1l1ll1_opy_ (u"ࠬ࠴ࡰࡺࠩမ")) and os.path.exists(arg))]
        self.args = self.bstack1l1111lll_opy_ + bstack1111l11111_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111ll1l1l_opy_():
        import importlib
        if getattr(importlib, bstack1l1ll1_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫယ"), False):
            bstack1111l11lll_opy_ = importlib.find_loader(bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩရ"))
        else:
            bstack1111l11lll_opy_ = importlib.util.find_spec(bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪလ"))
    def bstack1111l1l1ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111l11l1_opy_ = -1
        if self.bstack11111ll1ll_opy_ and bstack1l1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩဝ") in self.bstack11111llll1_opy_:
            self.bstack111l11l1_opy_ = int(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪသ")])
        try:
            bstack11111ll111_opy_ = [bstack1l1ll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ဟ"), bstack1l1ll1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨဠ"), bstack1l1ll1_opy_ (u"࠭࠭ࡱࠩအ")]
            if self.bstack111l11l1_opy_ >= 0:
                bstack11111ll111_opy_.extend([bstack1l1ll1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨဢ"), bstack1l1ll1_opy_ (u"ࠨ࠯ࡱࠫဣ")])
            for arg in bstack11111ll111_opy_:
                self.bstack1111l1l1ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111ll1l11_opy_(self):
        bstack1111l111l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        return bstack1111l111l1_opy_
    def bstack1111l1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111ll1l1l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l111l11ll_opy_)
    def bstack1111l11l11_opy_(self, bstack1111ll1111_opy_):
        bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
        if bstack1111ll1111_opy_:
            self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ဤ"))
            self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠪࡘࡷࡻࡥࠨဥ"))
        if bstack11lll111ll_opy_.bstack1111ll11ll_opy_():
            self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪဦ"))
            self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"࡚ࠬࡲࡶࡧࠪဧ"))
        self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"࠭࠭ࡱࠩဨ"))
        self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬဩ"))
        self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪဪ"))
        self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩါ"))
        if self.bstack111l11l1_opy_ > 1:
            self.bstack1111l111l1_opy_.append(bstack1l1ll1_opy_ (u"ࠪ࠱ࡳ࠭ာ"))
            self.bstack1111l111l1_opy_.append(str(self.bstack111l11l1_opy_))
    def bstack1111l1l111_opy_(self):
        if bstack11l1ll1l1_opy_.bstack1ll1ll1ll1_opy_(self.bstack11111llll1_opy_):
             self.bstack1111l111l1_opy_ += [
                bstack11111l1lll_opy_.get(bstack1l1ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪိ")), str(bstack11l1ll1l1_opy_.bstack1l1111l111_opy_(self.bstack11111llll1_opy_)),
                bstack11111l1lll_opy_.get(bstack1l1ll1_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫီ")), str(bstack11111l1lll_opy_.get(bstack1l1ll1_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫု")))
            ]
    def bstack1111l11ll1_opy_(self):
        bstack11ll1llll_opy_ = []
        for spec in self.bstack1l1111lll_opy_:
            bstack1llll11lll_opy_ = [spec]
            bstack1llll11lll_opy_ += self.bstack1111l111l1_opy_
            bstack11ll1llll_opy_.append(bstack1llll11lll_opy_)
        self.bstack11ll1llll_opy_ = bstack11ll1llll_opy_
        return bstack11ll1llll_opy_
    def bstack1l1llll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111lllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11111lllll_opy_ = False
        return self.bstack11111lllll_opy_
    def bstack1111lll11_opy_(self):
        bstack1l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡉࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦ࡯ࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠩࡶࠤ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠥ࡬࡬ࡢࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥူ")
        try:
            self.logger.info(bstack1l1ll1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࡶࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦေ"))
            bstack1111l1111l_opy_ = [bstack1l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤဲ"), *self.bstack1111l111l1_opy_, bstack1l1ll1_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦဳ")]
            result = subprocess.run(bstack1111l1111l_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1l1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤဴ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1l1ll1_opy_ (u"ࠧࡂࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠤဵ"))
            self.logger.info(bstack1l1ll1_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦံ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀ့ࠦ").format(e))
            return 0
    def bstack1llll1lll1_opy_(self, bstack1111l1lll1_opy_, bstack1ll11l1l_opy_):
        bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨး")] = self.bstack11111llll1_opy_
        multiprocessing.set_start_method(bstack1l1ll1_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨ္"))
        bstack1l1l1l111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111lll11_opy_ = manager.list()
        if bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ်࠭") in self.bstack11111llll1_opy_:
            for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧျ")]):
                bstack1l1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l1lll1_opy_,
                                                            args=(self.bstack1111l111l1_opy_, bstack1ll11l1l_opy_, bstack11111lll11_opy_)))
            bstack11111lll1l_opy_ = len(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨြ")])
        else:
            bstack1l1l1l111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l1lll1_opy_,
                                                        args=(self.bstack1111l111l1_opy_, bstack1ll11l1l_opy_, bstack11111lll11_opy_)))
            bstack11111lll1l_opy_ = 1
        i = 0
        for t in bstack1l1l1l111l_opy_:
            os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ွ")] = str(i)
            if bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪှ") in self.bstack11111llll1_opy_:
                os.environ[bstack1l1ll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩဿ")] = json.dumps(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၀")][i % bstack11111lll1l_opy_])
            i += 1
            t.start()
        for t in bstack1l1l1l111l_opy_:
            t.join()
        return list(bstack11111lll11_opy_)
    @staticmethod
    def bstack1llll1lll_opy_(driver, bstack1111ll11l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ၁"), None)
        if item and getattr(item, bstack1l1ll1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭၂"), None) and not getattr(item, bstack1l1ll1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ၃"), False):
            logger.info(
                bstack1l1ll1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧ၄"))
            bstack1111ll111l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11ll1lll_opy_.bstack11ll11l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11111ll11l_opy_(self):
        bstack1l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ၅")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1l1ll1_opy_ (u"ࠨ࠰ࡳࡽࠬ၆")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files