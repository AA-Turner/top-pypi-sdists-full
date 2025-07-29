# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11ll1ll11_opy_
import subprocess
from browserstack_sdk.bstack1l1l111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l11ll11_opy_
from bstack_utils.bstack1l11ll11_opy_ import bstack1ll11l11l1_opy_
from bstack_utils.constants import bstack11111l11ll_opy_
from bstack_utils.bstack11ll111ll_opy_ import bstack11l1ll11ll_opy_
class bstack11lll111l_opy_:
    def __init__(self, args, logger, bstack1111l1111l_opy_, bstack1111ll1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
        self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll11l11l_opy_ = []
        self.bstack1111l111l1_opy_ = None
        self.bstack111111ll_opy_ = []
        self.bstack11111l11l1_opy_ = self.bstack1l11111l11_opy_()
        self.bstack11llll1ll1_opy_ = -1
    def bstack11l11111l_opy_(self, bstack1111l11ll1_opy_):
        self.parse_args()
        self.bstack11111l1lll_opy_()
        self.bstack11111ll1ll_opy_(bstack1111l11ll1_opy_)
        self.bstack11111ll11l_opy_()
    def bstack1l1111l1_opy_(self):
        bstack11ll111ll_opy_ = bstack11l1ll11ll_opy_.bstack1l1l11ll_opy_(self.bstack1111l1111l_opy_, self.logger)
        if bstack11ll111ll_opy_ is None:
            self.logger.warn(bstackl_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡨࡢࡰࡧࡰࡪࡸࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ။"))
            return
        bstack11111l1l11_opy_ = False
        bstack11ll111ll_opy_.bstack1111l11111_opy_(bstackl_opy_ (u"ࠢࡦࡰࡤࡦࡱ࡫ࡤࠣ၌"), bstack11ll111ll_opy_.bstack11l1ll1lll_opy_())
        start_time = time.time()
        if bstack11ll111ll_opy_.bstack11l1ll1lll_opy_():
            test_files = self.bstack1111l11l1l_opy_()
            bstack11111l1l11_opy_ = True
            bstack1111l111ll_opy_ = bstack11ll111ll_opy_.bstack1111l1l111_opy_(test_files)
            if bstack1111l111ll_opy_:
                self.bstack11ll11l11l_opy_ = [os.path.normpath(item).replace(bstackl_opy_ (u"ࠨ࡞࡟ࠫ၍"), bstackl_opy_ (u"ࠩ࠲ࠫ၎")) for item in bstack1111l111ll_opy_]
                self.__11111l1l1l_opy_()
                bstack11ll111ll_opy_.bstack11111l1ll1_opy_(bstack11111l1l11_opy_)
                self.logger.info(bstackl_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ၏").format(self.bstack11ll11l11l_opy_))
            else:
                self.logger.info(bstackl_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤၐ"))
        bstack11ll111ll_opy_.bstack1111l11111_opy_(bstackl_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣၑ"), int((time.time() - start_time) * 1000)) # bstack11111ll1l1_opy_ to bstack1111l11lll_opy_
    def __11111l1l1l_opy_(self):
        bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡶ࡬ࡢࡥࡨࠤࡦࡲ࡬ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡪࡰࠣࡷࡪࡲࡦ࠯ࡣࡵ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡸ࡫࡬ࡧ࠰ࡶࡴࡪࡩ࡟ࡧ࡫࡯ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡑࡱࡰࡾࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡵ࡯࠽ࠣࡥࡱࡲࠠࡰࡶ࡫ࡩࡷࠦࡃࡍࡋࠣࡪࡱࡧࡧࡴࠢࡤࡶࡪࠦࡰࡳࡧࡶࡩࡷࡼࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢၒ")
        bstack11111lll1l_opy_ = [arg for arg in self.args if not (arg.endswith(bstackl_opy_ (u"ࠧ࠯ࡲࡼࠫၓ")) and os.path.exists(arg))]
        self.args = self.bstack11ll11l11l_opy_ + bstack11111lll1l_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1l1ll_opy_():
        import importlib
        if getattr(importlib, bstackl_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭ၔ"), False):
            bstack11111ll111_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫၕ"))
        else:
            bstack11111ll111_opy_ = importlib.util.find_spec(bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬၖ"))
    def bstack11111llll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11llll1ll1_opy_ = -1
        if self.bstack1111ll1111_opy_ and bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫၗ") in self.bstack1111l1111l_opy_:
            self.bstack11llll1ll1_opy_ = int(self.bstack1111l1111l_opy_[bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬၘ")])
        try:
            bstack1111l1lll1_opy_ = [bstackl_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨၙ"), bstackl_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪၚ"), bstackl_opy_ (u"ࠨ࠯ࡳࠫၛ")]
            if self.bstack11llll1ll1_opy_ >= 0:
                bstack1111l1lll1_opy_.extend([bstackl_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪၜ"), bstackl_opy_ (u"ࠪ࠱ࡳ࠭ၝ")])
            for arg in bstack1111l1lll1_opy_:
                self.bstack11111llll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11111l1lll_opy_(self):
        bstack1111l111l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        return bstack1111l111l1_opy_
    def bstack1l11l11l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1l1ll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l11ll11_opy_)
    def bstack11111ll1ll_opy_(self, bstack1111l11ll1_opy_):
        bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
        if bstack1111l11ll1_opy_:
            self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨၞ"))
            self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"࡚ࠬࡲࡶࡧࠪၟ"))
        if bstack1l1llll1l1_opy_.bstack11111lllll_opy_():
            self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬၠ"))
            self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠧࡕࡴࡸࡩࠬၡ"))
        self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠨ࠯ࡳࠫၢ"))
        self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧၣ"))
        self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬၤ"))
        self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫၥ"))
        if self.bstack11llll1ll1_opy_ > 1:
            self.bstack1111l111l1_opy_.append(bstackl_opy_ (u"ࠬ࠳࡮ࠨၦ"))
            self.bstack1111l111l1_opy_.append(str(self.bstack11llll1ll1_opy_))
    def bstack11111ll11l_opy_(self):
        if bstack1ll11l11l1_opy_.bstack1ll11ll1l_opy_(self.bstack1111l1111l_opy_):
             self.bstack1111l111l1_opy_ += [
                bstack11111l11ll_opy_.get(bstackl_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬၧ")), str(bstack1ll11l11l1_opy_.bstack1ll11l1111_opy_(self.bstack1111l1111l_opy_)),
                bstack11111l11ll_opy_.get(bstackl_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ၨ")), str(bstack11111l11ll_opy_.get(bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭ၩ")))
            ]
    def bstack1111l1l1l1_opy_(self):
        bstack111111ll_opy_ = []
        for spec in self.bstack11ll11l11l_opy_:
            bstack1ll1lll11l_opy_ = [spec]
            bstack1ll1lll11l_opy_ += self.bstack1111l111l1_opy_
            bstack111111ll_opy_.append(bstack1ll1lll11l_opy_)
        self.bstack111111ll_opy_ = bstack111111ll_opy_
        return bstack111111ll_opy_
    def bstack1l11111l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111l11l1_opy_ = True
            return True
        except Exception as e:
            self.bstack11111l11l1_opy_ = False
        return self.bstack11111l11l1_opy_
    def bstack11lll11l1_opy_(self):
        bstackl_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࡱࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠠࡧ࡮ࡤ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧၪ")
        try:
            self.logger.info(bstackl_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨၫ"))
            bstack1111l1ll11_opy_ = [bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦၬ"), *self.bstack1111l111l1_opy_, bstackl_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨၭ")]
            result = subprocess.run(bstack1111l1ll11_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦၮ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstackl_opy_ (u"ࠢ࠽ࡈࡸࡲࡨࡺࡩࡰࡰࠣࠦၯ"))
            self.logger.info(bstackl_opy_ (u"ࠣࡖࡲࡸࡦࡲࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠼ࠣࡿࢂࠨၰ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨၱ").format(e))
            return 0
    def bstack1lllllll11_opy_(self, bstack11111lll11_opy_, bstack11l11111l_opy_):
        bstack11l11111l_opy_[bstackl_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪၲ")] = self.bstack1111l1111l_opy_
        multiprocessing.set_start_method(bstackl_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪၳ"))
        bstack11l1111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l1l11l_opy_ = manager.list()
        if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨၴ") in self.bstack1111l1111l_opy_:
            for index, platform in enumerate(self.bstack1111l1111l_opy_[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩၵ")]):
                bstack11l1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111lll11_opy_,
                                                            args=(self.bstack1111l111l1_opy_, bstack11l11111l_opy_, bstack1111l1l11l_opy_)))
            bstack1111l11l11_opy_ = len(self.bstack1111l1111l_opy_[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪၶ")])
        else:
            bstack11l1111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111lll11_opy_,
                                                        args=(self.bstack1111l111l1_opy_, bstack11l11111l_opy_, bstack1111l1l11l_opy_)))
            bstack1111l11l11_opy_ = 1
        i = 0
        for t in bstack11l1111l_opy_:
            os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨၷ")] = str(i)
            if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬၸ") in self.bstack1111l1111l_opy_:
                os.environ[bstackl_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫၹ")] = json.dumps(self.bstack1111l1111l_opy_[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၺ")][i % bstack1111l11l11_opy_])
            i += 1
            t.start()
        for t in bstack11l1111l_opy_:
            t.join()
        return list(bstack1111l1l11l_opy_)
    @staticmethod
    def bstack11l1ll1l_opy_(driver, bstack1111l1llll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩၻ"), None)
        if item and getattr(item, bstackl_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨၼ"), None) and not getattr(item, bstackl_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩၽ"), False):
            logger.info(
                bstackl_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢၾ"))
            bstack1111l1ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11ll1ll11_opy_.bstack11ll11111l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111l11l1l_opy_(self):
        bstackl_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣၿ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstackl_opy_ (u"ࠪ࠲ࡵࡿࠧႀ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files