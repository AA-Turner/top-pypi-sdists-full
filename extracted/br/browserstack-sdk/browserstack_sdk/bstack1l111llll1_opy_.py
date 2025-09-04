# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1lll1111l1_opy_
import subprocess
from browserstack_sdk.bstack1llll11l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11ll1l1l_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from bstack_utils.constants import bstack1111l1ll11_opy_
from bstack_utils.bstack11ll1111ll_opy_ import bstack11l11l111l_opy_
class bstack11l1ll1ll1_opy_:
    def __init__(self, args, logger, bstack1111l11111_opy_, bstack11111l1l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l11111_opy_ = bstack1111l11111_opy_
        self.bstack11111l1l1l_opy_ = bstack11111l1l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11ll1111_opy_ = []
        self.bstack1111l111ll_opy_ = None
        self.bstack1lll1l1l11_opy_ = []
        self.bstack111111llll_opy_ = self.bstack11lll1ll1_opy_()
        self.bstack11l11ll11_opy_ = -1
    def bstack1l111l1l1l_opy_(self, bstack11111ll1l1_opy_):
        self.parse_args()
        self.bstack11111lll1l_opy_()
        self.bstack11111l11ll_opy_(bstack11111ll1l1_opy_)
        self.bstack1111l11lll_opy_()
    def bstack11l1l111l1_opy_(self):
        bstack11ll1111ll_opy_ = bstack11l11l111l_opy_.bstack1l11llll1_opy_(self.bstack1111l11111_opy_, self.logger)
        if bstack11ll1111ll_opy_ is None:
            self.logger.warn(bstack1111l1l_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨၖ"))
            return
        bstack11111ll11l_opy_ = False
        bstack11ll1111ll_opy_.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧၗ"), bstack11ll1111ll_opy_.bstack1ll11llll1_opy_())
        start_time = time.time()
        if bstack11ll1111ll_opy_.bstack1ll11llll1_opy_():
            test_files = self.bstack11111l1lll_opy_()
            bstack11111ll11l_opy_ = True
            bstack11111lllll_opy_ = bstack11ll1111ll_opy_.bstack111111lll1_opy_(test_files)
            if bstack11111lllll_opy_:
                self.bstack1l11ll1111_opy_ = [os.path.normpath(item).replace(bstack1111l1l_opy_ (u"ࠬࡢ࡜ࠨၘ"), bstack1111l1l_opy_ (u"࠭࠯ࠨၙ")) for item in bstack11111lllll_opy_]
                self.__1111l111l1_opy_()
                bstack11ll1111ll_opy_.bstack11111l1ll1_opy_(bstack11111ll11l_opy_)
                self.logger.info(bstack1111l1l_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧၚ").format(self.bstack1l11ll1111_opy_))
            else:
                self.logger.info(bstack1111l1l_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨၛ"))
        bstack11ll1111ll_opy_.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧၜ"), int((time.time() - start_time) * 1000)) # bstack1111l1l11l_opy_ to bstack1111l1l111_opy_
    def __1111l111l1_opy_(self):
        bstack1111l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡣ࡯ࡰࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࠠࡴࡧ࡯ࡪ࠳ࡧࡲࡨࡵࠣࡻ࡮ࡺࡨࠡࡵࡨࡰ࡫࠴ࡳࡱࡧࡦࡣ࡫࡯࡬ࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕ࡮࡭ࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡹࡳࡁࠠࡢ࡮࡯ࠤࡴࡺࡨࡦࡴࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡡࡳࡧࠣࡴࡷ࡫ࡳࡦࡴࡹࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦၝ")
        bstack1111l1l1l1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1111l1l_opy_ (u"ࠫ࠳ࡶࡹࠨၞ")) and os.path.exists(arg))]
        self.args = self.bstack1l11ll1111_opy_ + bstack1111l1l1l1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1l1ll_opy_():
        import importlib
        if getattr(importlib, bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪၟ"), False):
            bstack11111l111l_opy_ = importlib.find_loader(bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨၠ"))
        else:
            bstack11111l111l_opy_ = importlib.util.find_spec(bstack1111l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩၡ"))
    def bstack11111ll1ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11ll11_opy_ = -1
        if self.bstack11111l1l1l_opy_ and bstack1111l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨၢ") in self.bstack1111l11111_opy_:
            self.bstack11l11ll11_opy_ = int(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩၣ")])
        try:
            bstack11111l11l1_opy_ = [bstack1111l1l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬၤ"), bstack1111l1l_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧၥ"), bstack1111l1l_opy_ (u"ࠬ࠳ࡰࠨၦ")]
            if self.bstack11l11ll11_opy_ >= 0:
                bstack11111l11l1_opy_.extend([bstack1111l1l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧၧ"), bstack1111l1l_opy_ (u"ࠧ࠮ࡰࠪၨ")])
            for arg in bstack11111l11l1_opy_:
                self.bstack11111ll1ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11111lll1l_opy_(self):
        bstack1111l111ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
        return bstack1111l111ll_opy_
    def bstack11lll1llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1l1ll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11ll1l1l_opy_)
    def bstack11111l11ll_opy_(self, bstack11111ll1l1_opy_):
        bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
        if bstack11111ll1l1_opy_:
            self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬၩ"))
            self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧၪ"))
        if bstack1l1ll11l1_opy_.bstack11111l1111_opy_():
            self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩၫ"))
            self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"࡙ࠫࡸࡵࡦࠩၬ"))
        self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠬ࠳ࡰࠨၭ"))
        self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫၮ"))
        self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩၯ"))
        self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨၰ"))
        if self.bstack11l11ll11_opy_ > 1:
            self.bstack1111l111ll_opy_.append(bstack1111l1l_opy_ (u"ࠩ࠰ࡲࠬၱ"))
            self.bstack1111l111ll_opy_.append(str(self.bstack11l11ll11_opy_))
    def bstack1111l11lll_opy_(self):
        if bstack111l1llll_opy_.bstack11111ll1l_opy_(self.bstack1111l11111_opy_):
             self.bstack1111l111ll_opy_ += [
                bstack1111l1ll11_opy_.get(bstack1111l1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩၲ")), str(bstack111l1llll_opy_.bstack1l1ll1llll_opy_(self.bstack1111l11111_opy_)),
                bstack1111l1ll11_opy_.get(bstack1111l1l_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪၳ")), str(bstack1111l1ll11_opy_.get(bstack1111l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪၴ")))
            ]
    def bstack1111l11l11_opy_(self):
        bstack1lll1l1l11_opy_ = []
        for spec in self.bstack1l11ll1111_opy_:
            bstack1lll1llll_opy_ = [spec]
            bstack1lll1llll_opy_ += self.bstack1111l111ll_opy_
            bstack1lll1l1l11_opy_.append(bstack1lll1llll_opy_)
        self.bstack1lll1l1l11_opy_ = bstack1lll1l1l11_opy_
        return bstack1lll1l1l11_opy_
    def bstack11lll1ll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111111llll_opy_ = True
            return True
        except Exception as e:
            self.bstack111111llll_opy_ = False
        return self.bstack111111llll_opy_
    def bstack1lll11ll_opy_(self):
        bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠨࡵࠣ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠤ࡫ࡲࡡࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤၵ")
        try:
            self.logger.info(bstack1111l1l_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࡵࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥၶ"))
            bstack1111l11ll1_opy_ = [bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣၷ"), *self.bstack1111l111ll_opy_, bstack1111l1l_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥၸ")]
            result = subprocess.run(bstack1111l11ll1_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1111l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣၹ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1111l1l_opy_ (u"ࠦࡁࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠣၺ"))
            self.logger.info(bstack1111l1l_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥၻ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥၼ").format(e))
            return 0
    def bstack11l1l1ll_opy_(self, bstack1111l11l1l_opy_, bstack1l111l1l1l_opy_):
        bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧၽ")] = self.bstack1111l11111_opy_
        multiprocessing.set_start_method(bstack1111l1l_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧၾ"))
        bstack11l1l1l1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111llll1_opy_ = manager.list()
        if bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၿ") in self.bstack1111l11111_opy_:
            for index, platform in enumerate(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")]):
                bstack11l1l1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l11l1l_opy_,
                                                            args=(self.bstack1111l111ll_opy_, bstack1l111l1l1l_opy_, bstack11111llll1_opy_)))
            bstack11111l1l11_opy_ = len(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ")])
        else:
            bstack11l1l1l1l1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l11l1l_opy_,
                                                        args=(self.bstack1111l111ll_opy_, bstack1l111l1l1l_opy_, bstack11111llll1_opy_)))
            bstack11111l1l11_opy_ = 1
        i = 0
        for t in bstack11l1l1l1l1_opy_:
            os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬႂ")] = str(i)
            if bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ") in self.bstack1111l11111_opy_:
                os.environ[bstack1111l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨႄ")] = json.dumps(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႅ")][i % bstack11111l1l11_opy_])
            i += 1
            t.start()
        for t in bstack11l1l1l1l1_opy_:
            t.join()
        return list(bstack11111llll1_opy_)
    @staticmethod
    def bstack1l1l11llll_opy_(driver, bstack1111l1111l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ႆ"), None)
        if item and getattr(item, bstack1111l1l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬႇ"), None) and not getattr(item, bstack1111l1l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ႈ"), False):
            logger.info(
                bstack1111l1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦႉ"))
            bstack11111ll111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll1111l1_opy_.bstack11ll1l11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11111l1lll_opy_(self):
        bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧႊ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1111l1l_opy_ (u"ࠧ࠯ࡲࡼࠫႋ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files