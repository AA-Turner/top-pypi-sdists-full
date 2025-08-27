# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1llllll1l1_opy_
import subprocess
from browserstack_sdk.bstack1l1llll1l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll1lll111_opy_
from bstack_utils.bstack111l111ll_opy_ import bstack1l11llll1_opy_
from bstack_utils.constants import bstack1111l1l11l_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11l111ll1l_opy_
class bstack1ll1ll1l11_opy_:
    def __init__(self, args, logger, bstack11111lll1l_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111lll1l_opy_ = bstack11111lll1l_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l11ll1l_opy_ = []
        self.bstack11111ll1l1_opy_ = None
        self.bstack1llll1111_opy_ = []
        self.bstack1111l1ll1l_opy_ = self.bstack11l1l1llll_opy_()
        self.bstack1l11ll11l1_opy_ = -1
    def bstack11l1ll1l11_opy_(self, bstack1111l111ll_opy_):
        self.parse_args()
        self.bstack11111ll11l_opy_()
        self.bstack11111l1l11_opy_(bstack1111l111ll_opy_)
        self.bstack1111ll1111_opy_()
    def bstack11ll1l1ll_opy_(self):
        bstack111l11ll_opy_ = bstack11l111ll1l_opy_.bstack1ll1lll1l1_opy_(self.bstack11111lll1l_opy_, self.logger)
        if bstack111l11ll_opy_ is None:
            self.logger.warn(bstack1111lll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣၑ"))
            return
        bstack11111l1lll_opy_ = False
        bstack111l11ll_opy_.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢၒ"), bstack111l11ll_opy_.bstack1lll1111_opy_())
        start_time = time.time()
        if bstack111l11ll_opy_.bstack1lll1111_opy_():
            test_files = self.bstack1111ll111l_opy_()
            bstack11111l1lll_opy_ = True
            bstack1111l11l1l_opy_ = bstack111l11ll_opy_.bstack11111l1l1l_opy_(test_files)
            if bstack1111l11l1l_opy_:
                self.bstack11l11ll1l_opy_ = [os.path.normpath(item).replace(bstack1111lll_opy_ (u"ࠧ࡝࡞ࠪၓ"), bstack1111lll_opy_ (u"ࠨ࠱ࠪၔ")) for item in bstack1111l11l1l_opy_]
                self.__11111llll1_opy_()
                bstack111l11ll_opy_.bstack1111l1111l_opy_(bstack11111l1lll_opy_)
                self.logger.info(bstack1111lll_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢၕ").format(self.bstack11l11ll1l_opy_))
            else:
                self.logger.info(bstack1111lll_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣၖ"))
        bstack111l11ll_opy_.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢၗ"), int((time.time() - start_time) * 1000)) # bstack11111ll111_opy_ to bstack1111l1l1l1_opy_
    def __11111llll1_opy_(self):
        bstack1111lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡵࡲࡡࡤࡧࠣࡥࡱࡲࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࠢࡶࡩࡱ࡬࠮ࡢࡴࡪࡷࠥࡽࡩࡵࡪࠣࡷࡪࡲࡦ࠯ࡵࡳࡩࡨࡥࡦࡪ࡮ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡐࡰ࡯ࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷࡻ࡮࠼ࠢࡤࡰࡱࠦ࡯ࡵࡪࡨࡶࠥࡉࡌࡊࠢࡩࡰࡦ࡭ࡳࠡࡣࡵࡩࠥࡶࡲࡦࡵࡨࡶࡻ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨၘ")
        bstack1111l11ll1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack1111lll_opy_ (u"࠭࠮ࡱࡻࠪၙ")) and os.path.exists(arg))]
        self.args = self.bstack11l11ll1l_opy_ + bstack1111l11ll1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111lllll_opy_():
        import importlib
        if getattr(importlib, bstack1111lll_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬၚ"), False):
            bstack1111l11lll_opy_ = importlib.find_loader(bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪၛ"))
        else:
            bstack1111l11lll_opy_ = importlib.util.find_spec(bstack1111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫၜ"))
    def bstack11111l11ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l11ll11l1_opy_ = -1
        if self.bstack11111ll1ll_opy_ and bstack1111lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪၝ") in self.bstack11111lll1l_opy_:
            self.bstack1l11ll11l1_opy_ = int(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫၞ")])
        try:
            bstack1111l11l11_opy_ = [bstack1111lll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧၟ"), bstack1111lll_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩၠ"), bstack1111lll_opy_ (u"ࠧ࠮ࡲࠪၡ")]
            if self.bstack1l11ll11l1_opy_ >= 0:
                bstack1111l11l11_opy_.extend([bstack1111lll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩၢ"), bstack1111lll_opy_ (u"ࠩ࠰ࡲࠬၣ")])
            for arg in bstack1111l11l11_opy_:
                self.bstack11111l11ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11111ll11l_opy_(self):
        bstack11111ll1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111ll1l1_opy_ = bstack11111ll1l1_opy_
        return bstack11111ll1l1_opy_
    def bstack1l1ll1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111lllll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1ll1lll111_opy_)
    def bstack11111l1l11_opy_(self, bstack1111l111ll_opy_):
        bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
        if bstack1111l111ll_opy_:
            self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧၤ"))
            self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"࡙ࠫࡸࡵࡦࠩၥ"))
        if bstack1ll111ll11_opy_.bstack1111l1l1ll_opy_():
            self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫၦ"))
            self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"࠭ࡔࡳࡷࡨࠫၧ"))
        self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠧ࠮ࡲࠪၨ"))
        self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ၩ"))
        self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫၪ"))
        self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪၫ"))
        if self.bstack1l11ll11l1_opy_ > 1:
            self.bstack11111ll1l1_opy_.append(bstack1111lll_opy_ (u"ࠫ࠲ࡴࠧၬ"))
            self.bstack11111ll1l1_opy_.append(str(self.bstack1l11ll11l1_opy_))
    def bstack1111ll1111_opy_(self):
        if bstack1l11llll1_opy_.bstack1l1llllll1_opy_(self.bstack11111lll1l_opy_):
             self.bstack11111ll1l1_opy_ += [
                bstack1111l1l11l_opy_.get(bstack1111lll_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫၭ")), str(bstack1l11llll1_opy_.bstack11ll1llll_opy_(self.bstack11111lll1l_opy_)),
                bstack1111l1l11l_opy_.get(bstack1111lll_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬၮ")), str(bstack1111l1l11l_opy_.get(bstack1111lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬၯ")))
            ]
    def bstack1111l1l111_opy_(self):
        bstack1llll1111_opy_ = []
        for spec in self.bstack11l11ll1l_opy_:
            bstack11ll1ll11l_opy_ = [spec]
            bstack11ll1ll11l_opy_ += self.bstack11111ll1l1_opy_
            bstack1llll1111_opy_.append(bstack11ll1ll11l_opy_)
        self.bstack1llll1111_opy_ = bstack1llll1111_opy_
        return bstack1llll1111_opy_
    def bstack11l1l1llll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111l1ll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1111l1ll1l_opy_ = False
        return self.bstack1111l1ll1l_opy_
    def bstack11ll11111_opy_(self):
        bstack1111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࡰࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠪࡷࠥ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠦࡦ࡭ࡣࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦၰ")
        try:
            self.logger.info(bstack1111lll_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧၱ"))
            bstack1111l11111_opy_ = [bstack1111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥၲ"), *self.bstack11111ll1l1_opy_, bstack1111lll_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧၳ")]
            result = subprocess.run(bstack1111l11111_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack1111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥၴ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1111lll_opy_ (u"ࠨ࠼ࡇࡷࡱࡧࡹ࡯࡯࡯ࠢࠥၵ"))
            self.logger.info(bstack1111lll_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧၶ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧၷ").format(e))
            return 0
    def bstack11ll111ll1_opy_(self, bstack1111l1llll_opy_, bstack11l1ll1l11_opy_):
        bstack11l1ll1l11_opy_[bstack1111lll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩၸ")] = self.bstack11111lll1l_opy_
        multiprocessing.set_start_method(bstack1111lll_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩၹ"))
        bstack11ll11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l111l1_opy_ = manager.list()
        if bstack1111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၺ") in self.bstack11111lll1l_opy_:
            for index, platform in enumerate(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨၻ")]):
                bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l1llll_opy_,
                                                            args=(self.bstack11111ll1l1_opy_, bstack11l1ll1l11_opy_, bstack1111l111l1_opy_)))
            bstack11111l1ll1_opy_ = len(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩၼ")])
        else:
            bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l1llll_opy_,
                                                        args=(self.bstack11111ll1l1_opy_, bstack11l1ll1l11_opy_, bstack1111l111l1_opy_)))
            bstack11111l1ll1_opy_ = 1
        i = 0
        for t in bstack11ll11l11_opy_:
            os.environ[bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧၽ")] = str(i)
            if bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ") in self.bstack11111lll1l_opy_:
                os.environ[bstack1111lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪၿ")] = json.dumps(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")][i % bstack11111l1ll1_opy_])
            i += 1
            t.start()
        for t in bstack11ll11l11_opy_:
            t.join()
        return list(bstack1111l111l1_opy_)
    @staticmethod
    def bstack11l11l1lll_opy_(driver, bstack1111l1lll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨႁ"), None)
        if item and getattr(item, bstack1111lll_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧႂ"), None) and not getattr(item, bstack1111lll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨႃ"), False):
            logger.info(
                bstack1111lll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨႄ"))
            bstack1111l1ll11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1llllll1l1_opy_.bstack1ll1ll1l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111ll111l_opy_(self):
        bstack1111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢႅ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack1111lll_opy_ (u"ࠩ࠱ࡴࡾ࠭ႆ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files