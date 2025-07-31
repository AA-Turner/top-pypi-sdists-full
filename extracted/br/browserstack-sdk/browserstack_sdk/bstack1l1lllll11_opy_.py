# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1ll1ll1l11_opy_
import subprocess
from browserstack_sdk.bstack1llll1l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11lll1ll_opy_
from bstack_utils.bstack1111111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.constants import bstack1111l1l111_opy_
from bstack_utils.bstack1l1l1l11l_opy_ import bstack1ll1lll111_opy_
class bstack1l111l11l1_opy_:
    def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll11lll1l_opy_ = []
        self.bstack11111lllll_opy_ = None
        self.bstack1lll111l_opy_ = []
        self.bstack1111l11lll_opy_ = self.bstack11l11ll11_opy_()
        self.bstack11l111ll_opy_ = -1
    def bstack11ll1l1l_opy_(self, bstack1111l1llll_opy_):
        self.parse_args()
        self.bstack1111l11ll1_opy_()
        self.bstack11111ll1l1_opy_(bstack1111l1llll_opy_)
        self.bstack1111l1l1ll_opy_()
    def bstack11l1ll1l11_opy_(self):
        bstack1l1l1l11l_opy_ = bstack1ll1lll111_opy_.bstack11l111llll_opy_(self.bstack11111llll1_opy_, self.logger)
        if bstack1l1l1l11l_opy_ is None:
            self.logger.warn(bstack1l11l11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡨࡢࡰࡧࡰࡪࡸࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ။"))
            return
        bstack1111l11l1l_opy_ = False
        bstack1l1l1l11l_opy_.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠢࡦࡰࡤࡦࡱ࡫ࡤࠣ၌"), bstack1l1l1l11l_opy_.bstack11l1l1lll1_opy_())
        start_time = time.time()
        if bstack1l1l1l11l_opy_.bstack11l1l1lll1_opy_():
            test_files = self.bstack11111l11l1_opy_()
            bstack1111l11l1l_opy_ = True
            bstack11111lll11_opy_ = bstack1l1l1l11l_opy_.bstack11111l1l11_opy_(test_files)
            if bstack11111lll11_opy_:
                self.bstack1ll11lll1l_opy_ = [os.path.normpath(item).replace(bstack1l11l11_opy_ (u"ࠨ࡞࡟ࠫ၍"), bstack1l11l11_opy_ (u"ࠩ࠲ࠫ၎")) for item in bstack11111lll11_opy_]
                self.__1111l11111_opy_()
                bstack1l1l1l11l_opy_.bstack1111l11l11_opy_(bstack1111l11l1l_opy_)
                self.logger.info(bstack1l11l11_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ၏").format(self.bstack1ll11lll1l_opy_))
            else:
                self.logger.info(bstack1l11l11_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤၐ"))
        bstack1l1l1l11l_opy_.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣၑ"), int((time.time() - start_time) * 1000)) # bstack1111l1ll1l_opy_ to bstack1111l1lll1_opy_
    def __1111l11111_opy_(self):
        bstack1l11l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡶ࡬ࡢࡥࡨࠤࡦࡲ࡬ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡪࡰࠣࡷࡪࡲࡦ࠯ࡣࡵ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡸ࡫࡬ࡧ࠰ࡶࡴࡪࡩ࡟ࡧ࡫࡯ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡑࡱࡰࡾࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡵ࡯࠽ࠣࡥࡱࡲࠠࡰࡶ࡫ࡩࡷࠦࡃࡍࡋࠣࡪࡱࡧࡧࡴࠢࡤࡶࡪࠦࡰࡳࡧࡶࡩࡷࡼࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢၒ")
        bstack1111l111l1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1l11l11_opy_ (u"ࠧ࠯ࡲࡼࠫၓ")) and os.path.exists(arg))]
        self.args = self.bstack1ll11lll1l_opy_ + bstack1111l111l1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1ll11_opy_():
        import importlib
        if getattr(importlib, bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭ၔ"), False):
            bstack1111l1111l_opy_ = importlib.find_loader(bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫၕ"))
        else:
            bstack1111l1111l_opy_ = importlib.util.find_spec(bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬၖ"))
    def bstack1111l111ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l111ll_opy_ = -1
        if self.bstack11111ll11l_opy_ and bstack1l11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫၗ") in self.bstack11111llll1_opy_:
            self.bstack11l111ll_opy_ = int(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬၘ")])
        try:
            bstack1111l1l1l1_opy_ = [bstack1l11l11_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨၙ"), bstack1l11l11_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪၚ"), bstack1l11l11_opy_ (u"ࠨ࠯ࡳࠫၛ")]
            if self.bstack11l111ll_opy_ >= 0:
                bstack1111l1l1l1_opy_.extend([bstack1l11l11_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪၜ"), bstack1l11l11_opy_ (u"ࠪ࠱ࡳ࠭ၝ")])
            for arg in bstack1111l1l1l1_opy_:
                self.bstack1111l111ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l11ll1_opy_(self):
        bstack11111lllll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111lllll_opy_ = bstack11111lllll_opy_
        return bstack11111lllll_opy_
    def bstack1ll1lllll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1ll11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11lll1ll_opy_)
    def bstack11111ll1l1_opy_(self, bstack1111l1llll_opy_):
        bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
        if bstack1111l1llll_opy_:
            self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨၞ"))
            self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"࡚ࠬࡲࡶࡧࠪၟ"))
        if bstack11l11llll_opy_.bstack11111l11ll_opy_():
            self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬၠ"))
            self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠧࡕࡴࡸࡩࠬၡ"))
        self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠨ࠯ࡳࠫၢ"))
        self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧၣ"))
        self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬၤ"))
        self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫၥ"))
        if self.bstack11l111ll_opy_ > 1:
            self.bstack11111lllll_opy_.append(bstack1l11l11_opy_ (u"ࠬ࠳࡮ࠨၦ"))
            self.bstack11111lllll_opy_.append(str(self.bstack11l111ll_opy_))
    def bstack1111l1l1ll_opy_(self):
        if bstack11l11l1lll_opy_.bstack1l11ll1l1l_opy_(self.bstack11111llll1_opy_):
             self.bstack11111lllll_opy_ += [
                bstack1111l1l111_opy_.get(bstack1l11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬၧ")), str(bstack11l11l1lll_opy_.bstack1l1lll11l1_opy_(self.bstack11111llll1_opy_)),
                bstack1111l1l111_opy_.get(bstack1l11l11_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ၨ")), str(bstack1111l1l111_opy_.get(bstack1l11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭ၩ")))
            ]
    def bstack11111l1ll1_opy_(self):
        bstack1lll111l_opy_ = []
        for spec in self.bstack1ll11lll1l_opy_:
            bstack11l1l1l111_opy_ = [spec]
            bstack11l1l1l111_opy_ += self.bstack11111lllll_opy_
            bstack1lll111l_opy_.append(bstack11l1l1l111_opy_)
        self.bstack1lll111l_opy_ = bstack1lll111l_opy_
        return bstack1lll111l_opy_
    def bstack11l11ll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111l11lll_opy_ = True
            return True
        except Exception as e:
            self.bstack1111l11lll_opy_ = False
        return self.bstack1111l11lll_opy_
    def bstack1l1l1l1l_opy_(self):
        bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࡱࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠠࡧ࡮ࡤ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧၪ")
        try:
            self.logger.info(bstack1l11l11_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨၫ"))
            bstack1111l1l11l_opy_ = [bstack1l11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦၬ"), *self.bstack11111lllll_opy_, bstack1l11l11_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨၭ")]
            result = subprocess.run(bstack1111l1l11l_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1l11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦၮ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1l11l11_opy_ (u"ࠢ࠽ࡈࡸࡲࡨࡺࡩࡰࡰࠣࠦၯ"))
            self.logger.info(bstack1l11l11_opy_ (u"ࠣࡖࡲࡸࡦࡲࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠼ࠣࡿࢂࠨၰ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨၱ").format(e))
            return 0
    def bstack11l1l1llll_opy_(self, bstack11111lll1l_opy_, bstack11ll1l1l_opy_):
        bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪၲ")] = self.bstack11111llll1_opy_
        multiprocessing.set_start_method(bstack1l11l11_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪၳ"))
        bstack1l1l1lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11111ll111_opy_ = manager.list()
        if bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨၴ") in self.bstack11111llll1_opy_:
            for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩၵ")]):
                bstack1l1l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111lll1l_opy_,
                                                            args=(self.bstack11111lllll_opy_, bstack11ll1l1l_opy_, bstack11111ll111_opy_)))
            bstack11111l1lll_opy_ = len(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪၶ")])
        else:
            bstack1l1l1lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111lll1l_opy_,
                                                        args=(self.bstack11111lllll_opy_, bstack11ll1l1l_opy_, bstack11111ll111_opy_)))
            bstack11111l1lll_opy_ = 1
        i = 0
        for t in bstack1l1l1lll_opy_:
            os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨၷ")] = str(i)
            if bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၸ") in self.bstack11111llll1_opy_:
                os.environ[bstack1l11l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫၹ")] = json.dumps(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၺ")][i % bstack11111l1lll_opy_])
            i += 1
            t.start()
        for t in bstack1l1l1lll_opy_:
            t.join()
        return list(bstack11111ll111_opy_)
    @staticmethod
    def bstack1ll1l111_opy_(driver, bstack11111l111l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩၻ"), None)
        if item and getattr(item, bstack1l11l11_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨၼ"), None) and not getattr(item, bstack1l11l11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩၽ"), False):
            logger.info(
                bstack1l11l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢၾ"))
            bstack11111l1l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll1ll1l11_opy_.bstack11l1l1lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11111l11l1_opy_(self):
        bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣၿ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1l11l11_opy_ (u"ࠪ࠲ࡵࡿࠧႀ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files