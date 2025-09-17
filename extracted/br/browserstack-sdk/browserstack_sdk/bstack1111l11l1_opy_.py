# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11lll1ll1l_opy_
import subprocess
from browserstack_sdk.bstack1ll1l1lll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11ll11ll_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11llll1111_opy_
from bstack_utils.constants import bstack1111l1l11l_opy_
from bstack_utils.bstack1lllllllll_opy_ import bstack1lll111lll_opy_
class bstack1ll11l1l11_opy_:
    def __init__(self, args, logger, bstack11111l11ll_opy_, bstack11111l111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1ll1lll1_opy_ = []
        self.bstack1111l1l1l1_opy_ = None
        self.bstack11ll1lll11_opy_ = []
        self.bstack11111l1lll_opy_ = self.bstack11ll1111_opy_()
        self.bstack1lllll1lll_opy_ = -1
    def bstack111lllllll_opy_(self, bstack11111lll11_opy_):
        self.parse_args()
        self.bstack11111l1ll1_opy_()
        self.bstack1111l1111l_opy_(bstack11111lll11_opy_)
        self.bstack1111l11l1l_opy_()
    def bstack1l11lllll_opy_(self):
        bstack1lllllllll_opy_ = bstack1lll111lll_opy_.bstack1lll111l1l_opy_(self.bstack11111l11ll_opy_, self.logger)
        if bstack1lllllllll_opy_ is None:
            self.logger.warn(bstack1l11ll1_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦၔ"))
            return
        bstack11111ll11l_opy_ = False
        bstack1lllllllll_opy_.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥၕ"), bstack1lllllllll_opy_.bstack1l1lll1lll_opy_())
        start_time = time.time()
        if bstack1lllllllll_opy_.bstack1l1lll1lll_opy_():
            test_files = self.bstack1111l1l1ll_opy_()
            bstack11111ll11l_opy_ = True
            bstack1111l1l111_opy_ = bstack1lllllllll_opy_.bstack1111l11ll1_opy_(test_files)
            if bstack1111l1l111_opy_:
                self.bstack1l1ll1lll1_opy_ = [os.path.normpath(item).replace(bstack1l11ll1_opy_ (u"ࠪࡠࡡ࠭ၖ"), bstack1l11ll1_opy_ (u"ࠫ࠴࠭ၗ")) for item in bstack1111l1l111_opy_]
                self.__1111l11l11_opy_()
                bstack1lllllllll_opy_.bstack111111lll1_opy_(bstack11111ll11l_opy_)
                self.logger.info(bstack1l11ll1_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥၘ").format(self.bstack1l1ll1lll1_opy_))
            else:
                self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦၙ"))
        bstack1lllllllll_opy_.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥၚ"), int((time.time() - start_time) * 1000)) # bstack11111ll1ll_opy_ to bstack11111lll1l_opy_
    def __1111l11l11_opy_(self):
        bstack1l11ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡱ࡮ࡤࡧࡪࠦࡡ࡭࡮ࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢ࡬ࡲࠥࡹࡥ࡭ࡨ࠱ࡥࡷ࡭ࡳࠡࡹ࡬ࡸ࡭ࠦࡳࡦ࡮ࡩ࠲ࡸࡶࡥࡤࡡࡩ࡭ࡱ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡓࡳࡲࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡷࡱ࠿ࠥࡧ࡬࡭ࠢࡲࡸ࡭࡫ࡲࠡࡅࡏࡍࠥ࡬࡬ࡢࡩࡶࠤࡦࡸࡥࠡࡲࡵࡩࡸ࡫ࡲࡷࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤၛ")
        bstack1111l11lll_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1l11ll1_opy_ (u"ࠩ࠱ࡴࡾ࠭ၜ")) and os.path.exists(arg))]
        self.args = self.bstack1l1ll1lll1_opy_ + bstack1111l11lll_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111ll1l1_opy_():
        import importlib
        if getattr(importlib, bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨၝ"), False):
            bstack11111llll1_opy_ = importlib.find_loader(bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ၞ"))
        else:
            bstack11111llll1_opy_ = importlib.util.find_spec(bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧၟ"))
    def bstack11111l1111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lllll1lll_opy_ = -1
        if self.bstack11111l111l_opy_ and bstack1l11ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ၠ") in self.bstack11111l11ll_opy_:
            self.bstack1lllll1lll_opy_ = int(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၡ")])
        try:
            bstack111111llll_opy_ = [bstack1l11ll1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪၢ"), bstack1l11ll1_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬၣ"), bstack1l11ll1_opy_ (u"ࠪ࠱ࡵ࠭ၤ")]
            if self.bstack1lllll1lll_opy_ >= 0:
                bstack111111llll_opy_.extend([bstack1l11ll1_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬၥ"), bstack1l11ll1_opy_ (u"ࠬ࠳࡮ࠨၦ")])
            for arg in bstack111111llll_opy_:
                self.bstack11111l1111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11111l1ll1_opy_(self):
        bstack1111l1l1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        return bstack1111l1l1l1_opy_
    def bstack11lll1llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111ll1l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11ll11ll_opy_)
    def bstack1111l1111l_opy_(self, bstack11111lll11_opy_):
        bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
        if bstack11111lll11_opy_:
            self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪၧ"))
            self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠧࡕࡴࡸࡩࠬၨ"))
        if bstack111lllll11_opy_.bstack11111l1l1l_opy_():
            self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧၩ"))
            self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠩࡗࡶࡺ࡫ࠧၪ"))
        self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠪ࠱ࡵ࠭ၫ"))
        self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩၬ"))
        self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧၭ"))
        self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ၮ"))
        if self.bstack1lllll1lll_opy_ > 1:
            self.bstack1111l1l1l1_opy_.append(bstack1l11ll1_opy_ (u"ࠧ࠮ࡰࠪၯ"))
            self.bstack1111l1l1l1_opy_.append(str(self.bstack1lllll1lll_opy_))
    def bstack1111l11l1l_opy_(self):
        if bstack11llll1111_opy_.bstack1ll1l111l_opy_(self.bstack11111l11ll_opy_):
             self.bstack1111l1l1l1_opy_ += [
                bstack1111l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࠧၰ")), str(bstack11llll1111_opy_.bstack11l1l1l1ll_opy_(self.bstack11111l11ll_opy_)),
                bstack1111l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡧࡩࡱࡧࡹࠨၱ")), str(bstack1111l1l11l_opy_.get(bstack1l11ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨၲ")))
            ]
    def bstack11111l1l11_opy_(self):
        bstack11ll1lll11_opy_ = []
        for spec in self.bstack1l1ll1lll1_opy_:
            bstack1lll11l111_opy_ = [spec]
            bstack1lll11l111_opy_ += self.bstack1111l1l1l1_opy_
            bstack11ll1lll11_opy_.append(bstack1lll11l111_opy_)
        self.bstack11ll1lll11_opy_ = bstack11ll1lll11_opy_
        return bstack11ll1lll11_opy_
    def bstack11ll1111_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111l1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack11111l1lll_opy_ = False
        return self.bstack11111l1lll_opy_
    def bstack1l111ll1l_opy_(self):
        bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࡳࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹ࠭ࡳࠡ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠢࡩࡰࡦ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺ࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢၳ")
        try:
            self.logger.info(bstack1l11ll1_opy_ (u"ࠧࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠠ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣၴ"))
            bstack1111l11111_opy_ = [bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨၵ"), *self.bstack1111l1l1l1_opy_, bstack1l11ll1_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣၶ")]
            result = subprocess.run(bstack1111l11111_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨၷ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1l11ll1_opy_ (u"ࠤ࠿ࡊࡺࡴࡣࡵ࡫ࡲࡲࠥࠨၸ"))
            self.logger.info(bstack1l11ll1_opy_ (u"ࠥࡘࡴࡺࡡ࡭ࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠾ࠥࢁࡽࠣၹ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣၺ").format(e))
            return 0
    def bstack11l11l11ll_opy_(self, bstack1111l111ll_opy_, bstack111lllllll_opy_):
        bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬၻ")] = self.bstack11111l11ll_opy_
        multiprocessing.set_start_method(bstack1l11ll1_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬၼ"))
        bstack11111llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111l11l1_opy_ = manager.list()
        if bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪၽ") in self.bstack11111l11ll_opy_:
            for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ")]):
                bstack11111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l111ll_opy_,
                                                            args=(self.bstack1111l1l1l1_opy_, bstack111lllllll_opy_, bstack11111l11l1_opy_)))
            bstack11111ll111_opy_ = len(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၿ")])
        else:
            bstack11111llll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l111ll_opy_,
                                                        args=(self.bstack1111l1l1l1_opy_, bstack111lllllll_opy_, bstack11111l11l1_opy_)))
            bstack11111ll111_opy_ = 1
        i = 0
        for t in bstack11111llll_opy_:
            os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪႀ")] = str(i)
            if bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ") in self.bstack11111l11ll_opy_:
                os.environ[bstack1l11ll1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ႂ")] = json.dumps(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")][i % bstack11111ll111_opy_])
            i += 1
            t.start()
        for t in bstack11111llll_opy_:
            t.join()
        return list(bstack11111l11l1_opy_)
    @staticmethod
    def bstack111l111l_opy_(driver, bstack1111l111l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫႄ"), None)
        if item and getattr(item, bstack1l11ll1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪႅ"), None) and not getattr(item, bstack1l11ll1_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫႆ"), False):
            logger.info(
                bstack1l11ll1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤႇ"))
            bstack111111ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11lll1ll1l_opy_.bstack1l1ll1111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111l1l1ll_opy_(self):
        bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡹࡵࠠࡣࡧࠣࡩࡽ࡫ࡣࡶࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥႈ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1l11ll1_opy_ (u"ࠬ࠴ࡰࡺࠩႉ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files