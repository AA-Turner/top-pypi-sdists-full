# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11l111l11_opy_
import subprocess
from browserstack_sdk.bstack1l11l1lll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11l1l1_opy_
from bstack_utils.bstack11ll11111_opy_ import bstack1l1111111l_opy_
from bstack_utils.constants import bstack11111l11l1_opy_
from bstack_utils.bstack11l1llllll_opy_ import bstack1ll1lll11_opy_
class bstack11l11ll111_opy_:
    def __init__(self, args, logger, bstack1111l1lll1_opy_, bstack1111l111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
        self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1l11lll_opy_ = []
        self.bstack1111l1l11l_opy_ = None
        self.bstack1l1l1ll11_opy_ = []
        self.bstack11111lll11_opy_ = self.bstack1l1lllll_opy_()
        self.bstack111llll1l_opy_ = -1
    def bstack1l11l1l1_opy_(self, bstack11111ll1l1_opy_):
        self.parse_args()
        self.bstack1111l111l1_opy_()
        self.bstack1111l1l111_opy_(bstack11111ll1l1_opy_)
        self.bstack11111lllll_opy_()
    def bstack11l11l1ll_opy_(self):
        bstack11l1llllll_opy_ = bstack1ll1lll11_opy_.bstack1l1l111l1l_opy_(self.bstack1111l1lll1_opy_, self.logger)
        if bstack11l1llllll_opy_ is None:
            self.logger.warn(bstack1l1_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ၈"))
            return
        bstack1111l11111_opy_ = False
        bstack11l1llllll_opy_.bstack11111l1lll_opy_(bstack1l1_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧ၉"), bstack11l1llllll_opy_.bstack1l1ll11l1_opy_())
        start_time = time.time()
        if bstack11l1llllll_opy_.bstack1l1ll11l1_opy_():
            test_files = self.bstack11111lll1l_opy_()
            bstack1111l11111_opy_ = True
            bstack1111l1ll1l_opy_ = bstack11l1llllll_opy_.bstack1111l1l1l1_opy_(test_files)
            if bstack1111l1ll1l_opy_:
                self.bstack1l1l11lll_opy_ = [os.path.normpath(item).replace(bstack1l1_opy_ (u"ࠬࡢ࡜ࠨ၊"), bstack1l1_opy_ (u"࠭࠯ࠨ။")) for item in bstack1111l1ll1l_opy_]
                self.__11111l11ll_opy_()
                bstack11l1llllll_opy_.bstack11111l1ll1_opy_(bstack1111l11111_opy_)
                self.logger.info(bstack1l1_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ၌").format(self.bstack1l1l11lll_opy_))
            else:
                self.logger.info(bstack1l1_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ၍"))
        bstack11l1llllll_opy_.bstack11111l1lll_opy_(bstack1l1_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧ၎"), int((time.time() - start_time) * 1000)) # bstack1111l1111l_opy_ to bstack1111l1ll11_opy_
    def __11111l11ll_opy_(self):
        bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡣ࡯ࡰࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࠠࡴࡧ࡯ࡪ࠳ࡧࡲࡨࡵࠣࡻ࡮ࡺࡨࠡࡵࡨࡰ࡫࠴ࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕ࡮࡭ࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡹࡳࡁࠠࡢ࡮࡯ࠤࡴࡺࡨࡦࡴࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡡࡳࡧࠣࡴࡷ࡫ࡳࡦࡴࡹࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ၏")
        bstack11111llll1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1l1_opy_ (u"ࠫ࠳ࡶࡹࠨၐ")) and os.path.exists(arg))]
        self.args = self.bstack1l1l11lll_opy_ + bstack11111llll1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111l1l11_opy_():
        import importlib
        if getattr(importlib, bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪၑ"), False):
            bstack1111l1l1ll_opy_ = importlib.find_loader(bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨၒ"))
        else:
            bstack1111l1l1ll_opy_ = importlib.util.find_spec(bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩၓ"))
    def bstack1111ll1111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111llll1l_opy_ = -1
        if self.bstack1111l111ll_opy_ and bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨၔ") in self.bstack1111l1lll1_opy_:
            self.bstack111llll1l_opy_ = int(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩၕ")])
        try:
            bstack1111l11l11_opy_ = [bstack1l1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬၖ"), bstack1l1_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧၗ"), bstack1l1_opy_ (u"ࠬ࠳ࡰࠨၘ")]
            if self.bstack111llll1l_opy_ >= 0:
                bstack1111l11l11_opy_.extend([bstack1l1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧၙ"), bstack1l1_opy_ (u"ࠧ࠮ࡰࠪၚ")])
            for arg in bstack1111l11l11_opy_:
                self.bstack1111ll1111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l111l1_opy_(self):
        bstack1111l1l11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l1l11l_opy_ = bstack1111l1l11l_opy_
        return bstack1111l1l11l_opy_
    def bstack1l1l1111l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111l1l11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l11l1l1_opy_)
    def bstack1111l1l111_opy_(self, bstack11111ll1l1_opy_):
        bstack11ll1l1l1_opy_ = Config.bstack1l1l111l1l_opy_()
        if bstack11111ll1l1_opy_:
            self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬၛ"))
            self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠩࡗࡶࡺ࡫ࠧၜ"))
        if bstack11ll1l1l1_opy_.bstack11111ll11l_opy_():
            self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩၝ"))
            self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"࡙ࠫࡸࡵࡦࠩၞ"))
        self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠬ࠳ࡰࠨၟ"))
        self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫၠ"))
        self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩၡ"))
        self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨၢ"))
        if self.bstack111llll1l_opy_ > 1:
            self.bstack1111l1l11l_opy_.append(bstack1l1_opy_ (u"ࠩ࠰ࡲࠬၣ"))
            self.bstack1111l1l11l_opy_.append(str(self.bstack111llll1l_opy_))
    def bstack11111lllll_opy_(self):
        if bstack1l1111111l_opy_.bstack1111l1l1l_opy_(self.bstack1111l1lll1_opy_):
             self.bstack1111l1l11l_opy_ += [
                bstack11111l11l1_opy_.get(bstack1l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩၤ")), str(bstack1l1111111l_opy_.bstack11ll11lll_opy_(self.bstack1111l1lll1_opy_)),
                bstack11111l11l1_opy_.get(bstack1l1_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪၥ")), str(bstack11111l11l1_opy_.get(bstack1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪၦ")))
            ]
    def bstack1111l11l1l_opy_(self):
        bstack1l1l1ll11_opy_ = []
        for spec in self.bstack1l1l11lll_opy_:
            bstack1lll1ll1_opy_ = [spec]
            bstack1lll1ll1_opy_ += self.bstack1111l1l11l_opy_
            bstack1l1l1ll11_opy_.append(bstack1lll1ll1_opy_)
        self.bstack1l1l1ll11_opy_ = bstack1l1l1ll11_opy_
        return bstack1l1l1ll11_opy_
    def bstack1l1lllll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111lll11_opy_ = True
            return True
        except Exception as e:
            self.bstack11111lll11_opy_ = False
        return self.bstack11111lll11_opy_
    def bstack11l11l1ll1_opy_(self):
        bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠨࡵࠣ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠤ࡫ࡲࡡࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤၧ")
        try:
            self.logger.info(bstack1l1_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࡵࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥၨ"))
            bstack11111ll111_opy_ = [bstack1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣၩ"), *self.bstack1111l1l11l_opy_, bstack1l1_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥၪ")]
            result = subprocess.run(bstack11111ll111_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣၫ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1l1_opy_ (u"ࠦࡁࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠣၬ"))
            self.logger.info(bstack1l1_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥၭ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥၮ").format(e))
            return 0
    def bstack1lll11lll_opy_(self, bstack1111l11ll1_opy_, bstack1l11l1l1_opy_):
        bstack1l11l1l1_opy_[bstack1l1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧၯ")] = self.bstack1111l1lll1_opy_
        multiprocessing.set_start_method(bstack1l1_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧၰ"))
        bstack1lll1lll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l1llll_opy_ = manager.list()
        if bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၱ") in self.bstack1111l1lll1_opy_:
            for index, platform in enumerate(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ၲ")]):
                bstack1lll1lll1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l11ll1_opy_,
                                                            args=(self.bstack1111l1l11l_opy_, bstack1l11l1l1_opy_, bstack1111l1llll_opy_)))
            bstack11111l1l1l_opy_ = len(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၳ")])
        else:
            bstack1lll1lll1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l11ll1_opy_,
                                                        args=(self.bstack1111l1l11l_opy_, bstack1l11l1l1_opy_, bstack1111l1llll_opy_)))
            bstack11111l1l1l_opy_ = 1
        i = 0
        for t in bstack1lll1lll1_opy_:
            os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬၴ")] = str(i)
            if bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩၵ") in self.bstack1111l1lll1_opy_:
                os.environ[bstack1l1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨၶ")] = json.dumps(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၷ")][i % bstack11111l1l1l_opy_])
            i += 1
            t.start()
        for t in bstack1lll1lll1_opy_:
            t.join()
        return list(bstack1111l1llll_opy_)
    @staticmethod
    def bstack1lll1ll111_opy_(driver, bstack11111ll1ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ၸ"), None)
        if item and getattr(item, bstack1l1_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬၹ"), None) and not getattr(item, bstack1l1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ၺ"), False):
            logger.info(
                bstack1l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦၻ"))
            bstack1111l11lll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l111l11_opy_.bstack11lll1111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11111lll1l_opy_(self):
        bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧၼ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1l1_opy_ (u"ࠧ࠯ࡲࡼࠫၽ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files