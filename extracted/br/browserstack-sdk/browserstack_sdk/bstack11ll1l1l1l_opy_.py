# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l1l11l1l1_opy_
import subprocess
from browserstack_sdk.bstack1ll111ll1l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll1111_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1ll1l111_opy_
from bstack_utils.constants import bstack1111l11lll_opy_
from bstack_utils.bstack1l1l1l11_opy_ import bstack1ll1l1ll1_opy_
class bstack1l11l11l1l_opy_:
    def __init__(self, args, logger, bstack11111l11ll_opy_, bstack1111l111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1l1l11l_opy_ = []
        self.bstack11111ll111_opy_ = None
        self.bstack11l111l1_opy_ = []
        self.bstack11111l1111_opy_ = self.bstack1l11lll1ll_opy_()
        self.bstack1ll111lll_opy_ = -1
    def bstack11lll111ll_opy_(self, bstack11111ll1ll_opy_):
        self.parse_args()
        self.bstack1111l1111l_opy_()
        self.bstack11111l1l11_opy_(bstack11111ll1ll_opy_)
        self.bstack11111lllll_opy_()
    def bstack1l1111l111_opy_(self):
        bstack1l1l1l11_opy_ = bstack1ll1l1ll1_opy_.bstack11l11lllll_opy_(self.bstack11111l11ll_opy_, self.logger)
        if bstack1l1l1l11_opy_ is None:
            self.logger.warn(bstack1ll11ll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧၕ"))
            return
        bstack11111l1ll1_opy_ = False
        bstack1l1l1l11_opy_.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦၖ"), bstack1l1l1l11_opy_.bstack11l11l11ll_opy_())
        start_time = time.time()
        if bstack1l1l1l11_opy_.bstack11l11l11ll_opy_():
            test_files = self.bstack1111l11l1l_opy_()
            bstack11111l1ll1_opy_ = True
            bstack111111lll1_opy_ = bstack1l1l1l11_opy_.bstack11111l1lll_opy_(test_files)
            if bstack111111lll1_opy_:
                self.bstack11l1l1l11l_opy_ = [os.path.normpath(item).replace(bstack1ll11ll_opy_ (u"ࠫࡡࡢࠧၗ"), bstack1ll11ll_opy_ (u"ࠬ࠵ࠧၘ")) for item in bstack111111lll1_opy_]
                self.__1111l1l11l_opy_()
                bstack1l1l1l11_opy_.bstack11111lll11_opy_(bstack11111l1ll1_opy_)
                self.logger.info(bstack1ll11ll_opy_ (u"ࠨࡔࡦࡵࡷࡷࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦၙ").format(self.bstack11l1l1l11l_opy_))
            else:
                self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸࡧࡵࡩࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡤࡼࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧၚ"))
        bstack1l1l1l11_opy_.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠣࡶ࡬ࡱࡪ࡚ࡡ࡬ࡧࡱࡘࡴࡇࡰࡱ࡮ࡼࠦၛ"), int((time.time() - start_time) * 1000)) # bstack1111l1l1l1_opy_ to bstack111111llll_opy_
    def __1111l1l11l_opy_(self):
        bstack1ll11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡲ࡯ࡥࡨ࡫ࠠࡢ࡮࡯ࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࠦࡳࡦ࡮ࡩ࠲ࡦࡸࡧࡴࠢࡺ࡭ࡹ࡮ࠠࡴࡧ࡯ࡪ࠳ࡹࡰࡦࡥࡢࡪ࡮ࡲࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡔࡴ࡬ࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡸࡲࡀࠦࡡ࡭࡮ࠣࡳࡹ࡮ࡥࡳࠢࡆࡐࡎࠦࡦ࡭ࡣࡪࡷࠥࡧࡲࡦࠢࡳࡶࡪࡹࡥࡳࡸࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥၜ")
        bstack1111l111ll_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1ll11ll_opy_ (u"ࠪ࠲ࡵࡿࠧၝ")) and os.path.exists(arg))]
        self.args = self.bstack11l1l1l11l_opy_ + bstack1111l111ll_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111ll1l1_opy_():
        import importlib
        if getattr(importlib, bstack1ll11ll_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩၞ"), False):
            bstack11111ll11l_opy_ = importlib.find_loader(bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧၟ"))
        else:
            bstack11111ll11l_opy_ = importlib.util.find_spec(bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨၠ"))
    def bstack1111l1l111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll111lll_opy_ = -1
        if self.bstack1111l111l1_opy_ and bstack1ll11ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၡ") in self.bstack11111l11ll_opy_:
            self.bstack1ll111lll_opy_ = int(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨၢ")])
        try:
            bstack1111l1l1ll_opy_ = [bstack1ll11ll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫၣ"), bstack1ll11ll_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ၤ"), bstack1ll11ll_opy_ (u"ࠫ࠲ࡶࠧၥ")]
            if self.bstack1ll111lll_opy_ >= 0:
                bstack1111l1l1ll_opy_.extend([bstack1ll11ll_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ၦ"), bstack1ll11ll_opy_ (u"࠭࠭࡯ࠩၧ")])
            for arg in bstack1111l1l1ll_opy_:
                self.bstack1111l1l111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l1111l_opy_(self):
        bstack11111ll111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111ll111_opy_ = bstack11111ll111_opy_
        return bstack11111ll111_opy_
    def bstack1ll11ll1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111ll1l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llll1111_opy_)
    def bstack11111l1l11_opy_(self, bstack11111ll1ll_opy_):
        bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
        if bstack11111ll1ll_opy_:
            self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫၨ"))
            self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠨࡖࡵࡹࡪ࠭ၩ"))
        if bstack1l111111l1_opy_.bstack11111llll1_opy_():
            self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨၪ"))
            self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠪࡘࡷࡻࡥࠨၫ"))
        self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠫ࠲ࡶࠧၬ"))
        self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪၭ"))
        self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨၮ"))
        self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧၯ"))
        if self.bstack1ll111lll_opy_ > 1:
            self.bstack11111ll111_opy_.append(bstack1ll11ll_opy_ (u"ࠨ࠯ࡱࠫၰ"))
            self.bstack11111ll111_opy_.append(str(self.bstack1ll111lll_opy_))
    def bstack11111lllll_opy_(self):
        if bstack1ll1l111_opy_.bstack11l1lll11_opy_(self.bstack11111l11ll_opy_):
             self.bstack11111ll111_opy_ += [
                bstack1111l11lll_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨၱ")), str(bstack1ll1l111_opy_.bstack1ll11ll1l_opy_(self.bstack11111l11ll_opy_)),
                bstack1111l11lll_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡨࡪࡲࡡࡺࠩၲ")), str(bstack1111l11lll_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰ࠰ࡨࡪࡲࡡࡺࠩၳ")))
            ]
    def bstack11111l111l_opy_(self):
        bstack11l111l1_opy_ = []
        for spec in self.bstack11l1l1l11l_opy_:
            bstack1ll1l1l1l_opy_ = [spec]
            bstack1ll1l1l1l_opy_ += self.bstack11111ll111_opy_
            bstack11l111l1_opy_.append(bstack1ll1l1l1l_opy_)
        self.bstack11l111l1_opy_ = bstack11l111l1_opy_
        return bstack11l111l1_opy_
    def bstack1l11lll1ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111l1111_opy_ = True
            return True
        except Exception as e:
            self.bstack11111l1111_opy_ = False
        return self.bstack11111l1111_opy_
    def bstack11ll1ll1ll_opy_(self):
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡇࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫࡭ࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠧࡴࠢ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠣࡪࡱࡧࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣၴ")
        try:
            self.logger.info(bstack1ll11ll_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࡴࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤၵ"))
            bstack11111l11l1_opy_ = [bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢၶ"), *self.bstack11111ll111_opy_, bstack1ll11ll_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤၷ")]
            result = subprocess.run(bstack11111l11l1_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢၸ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1ll11ll_opy_ (u"ࠥࡀࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠢၹ"))
            self.logger.info(bstack1ll11ll_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠿ࠦࡻࡾࠤၺ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤၻ").format(e))
            return 0
    def bstack1l111ll1l1_opy_(self, bstack1111l11ll1_opy_, bstack11lll111ll_opy_):
        bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ၼ")] = self.bstack11111l11ll_opy_
        multiprocessing.set_start_method(bstack1ll11ll_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭ၽ"))
        bstack1l111111_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111l1l1l_opy_ = manager.list()
        if bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ") in self.bstack11111l11ll_opy_:
            for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၿ")]):
                bstack1l111111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l11ll1_opy_,
                                                            args=(self.bstack11111ll111_opy_, bstack11lll111ll_opy_, bstack11111l1l1l_opy_)))
            bstack1111l11l11_opy_ = len(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")])
        else:
            bstack1l111111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l11ll1_opy_,
                                                        args=(self.bstack11111ll111_opy_, bstack11lll111ll_opy_, bstack11111l1l1l_opy_)))
            bstack1111l11l11_opy_ = 1
        i = 0
        for t in bstack1l111111_opy_:
            os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫႁ")] = str(i)
            if bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႂ") in self.bstack11111l11ll_opy_:
                os.environ[bstack1ll11ll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧႃ")] = json.dumps(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪႄ")][i % bstack1111l11l11_opy_])
            i += 1
            t.start()
        for t in bstack1l111111_opy_:
            t.join()
        return list(bstack11111l1l1l_opy_)
    @staticmethod
    def bstack1llll11l_opy_(driver, bstack11111lll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬႅ"), None)
        if item and getattr(item, bstack1ll11ll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫႆ"), None) and not getattr(item, bstack1ll11ll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬႇ"), False):
            logger.info(
                bstack1ll11ll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥႈ"))
            bstack111111ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1l11l1l1_opy_.bstack1l11ll1l11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111l11l1l_opy_(self):
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡺ࡯ࠡࡤࡨࠤࡪࡾࡥࡤࡷࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦႉ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1ll11ll_opy_ (u"࠭࠮ࡱࡻࠪႊ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files