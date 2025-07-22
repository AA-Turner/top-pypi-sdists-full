# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l1ll11l1l_opy_
import subprocess
from browserstack_sdk.bstack1ll111l111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1ll11_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack11llllll_opy_
from bstack_utils.constants import bstack1111l11l11_opy_
from bstack_utils.bstack1lll11ll_opy_ import bstack1l1l111l11_opy_
class bstack1l1l11l111_opy_:
    def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l111lll11_opy_ = []
        self.bstack11111ll111_opy_ = None
        self.bstack1llll1lll_opy_ = []
        self.bstack11111llll1_opy_ = self.bstack1ll1l111l1_opy_()
        self.bstack11111l1l1_opy_ = -1
    def bstack1l1l1l11ll_opy_(self, bstack11111ll11l_opy_):
        self.parse_args()
        self.bstack1111ll111l_opy_()
        self.bstack11111l1lll_opy_(bstack11111ll11l_opy_)
        self.bstack1111l1111l_opy_()
    def bstack11111111l_opy_(self):
        bstack1lll11ll_opy_ = bstack1l1l111l11_opy_.bstack1ll11ll1_opy_(self.bstack11111l1ll1_opy_, self.logger)
        if bstack1lll11ll_opy_ is None:
            self.logger.warn(bstack111l111_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ၊"))
            return
        bstack1111l111ll_opy_ = False
        bstack1lll11ll_opy_.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢ။"), bstack1lll11ll_opy_.bstack1l111l1l1l_opy_())
        start_time = time.time()
        if bstack1lll11ll_opy_.bstack1l111l1l1l_opy_():
            test_files = self.bstack1111l1l1ll_opy_()
            bstack1111l111ll_opy_ = True
            bstack1111l1l11l_opy_ = bstack1lll11ll_opy_.bstack1111l1llll_opy_(test_files)
            if bstack1111l1l11l_opy_:
                self.bstack1l111lll11_opy_ = [os.path.normpath(item).replace(bstack111l111_opy_ (u"ࠧ࡝࡞ࠪ၌"), bstack111l111_opy_ (u"ࠨ࠱ࠪ၍")) for item in bstack1111l1l11l_opy_]
                self.__1111l11ll1_opy_()
                bstack1lll11ll_opy_.bstack1111l11111_opy_(bstack1111l111ll_opy_)
                self.logger.info(bstack111l111_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ၎").format(self.bstack1l111lll11_opy_))
            else:
                self.logger.info(bstack111l111_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ၏"))
        bstack1lll11ll_opy_.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢၐ"), int((time.time() - start_time) * 1000)) # bstack1111l1ll11_opy_ to bstack11111lll11_opy_
    def __1111l11ll1_opy_(self):
        bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡵࡲࡡࡤࡧࠣࡥࡱࡲࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࠢࡶࡩࡱ࡬࠮ࡢࡴࡪࡷࠥࡽࡩࡵࡪࠣࡷࡪࡲࡦ࠯ࡵࡳࡩࡨࡥࡦࡪ࡮ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡐࡰ࡯ࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷࡻ࡮࠼ࠢࡤࡰࡱࠦ࡯ࡵࡪࡨࡶࠥࡉࡌࡊࠢࡩࡰࡦ࡭ࡳࠡࡣࡵࡩࠥࡶࡲࡦࡵࡨࡶࡻ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨၑ")
        bstack1111l1lll1_opy_ = [arg for arg in self.args if not (arg.endswith(bstack111l111_opy_ (u"࠭࠮ࡱࡻࠪၒ")) and os.path.exists(arg))]
        self.args = self.bstack1l111lll11_opy_ + bstack1111l1lll1_opy_
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111lll1l_opy_():
        import importlib
        if getattr(importlib, bstack111l111_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬၓ"), False):
            bstack11111lllll_opy_ = importlib.find_loader(bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪၔ"))
        else:
            bstack11111lllll_opy_ = importlib.util.find_spec(bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫၕ"))
    def bstack1111l111l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11111l1l1_opy_ = -1
        if self.bstack11111ll1ll_opy_ and bstack111l111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪၖ") in self.bstack11111l1ll1_opy_:
            self.bstack11111l1l1_opy_ = int(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫၗ")])
        try:
            bstack11111l1l11_opy_ = [bstack111l111_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧၘ"), bstack111l111_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩၙ"), bstack111l111_opy_ (u"ࠧ࠮ࡲࠪၚ")]
            if self.bstack11111l1l1_opy_ >= 0:
                bstack11111l1l11_opy_.extend([bstack111l111_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩၛ"), bstack111l111_opy_ (u"ࠩ࠰ࡲࠬၜ")])
            for arg in bstack11111l1l11_opy_:
                self.bstack1111l111l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111ll111l_opy_(self):
        bstack11111ll111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111ll111_opy_ = bstack11111ll111_opy_
        return bstack11111ll111_opy_
    def bstack1llll11l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111lll1l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1ll11_opy_)
    def bstack11111l1lll_opy_(self, bstack11111ll11l_opy_):
        bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
        if bstack11111ll11l_opy_:
            self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧၝ"))
            self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"࡙ࠫࡸࡵࡦࠩၞ"))
        if bstack1ll1ll11_opy_.bstack1111l1l1l1_opy_():
            self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫၟ"))
            self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"࠭ࡔࡳࡷࡨࠫၠ"))
        self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠧ࠮ࡲࠪၡ"))
        self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ၢ"))
        self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫၣ"))
        self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪၤ"))
        if self.bstack11111l1l1_opy_ > 1:
            self.bstack11111ll111_opy_.append(bstack111l111_opy_ (u"ࠫ࠲ࡴࠧၥ"))
            self.bstack11111ll111_opy_.append(str(self.bstack11111l1l1_opy_))
    def bstack1111l1111l_opy_(self):
        if bstack11llllll_opy_.bstack1lll1l1lll_opy_(self.bstack11111l1ll1_opy_):
             self.bstack11111ll111_opy_ += [
                bstack1111l11l11_opy_.get(bstack111l111_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫၦ")), str(bstack11llllll_opy_.bstack1l111ll1l_opy_(self.bstack11111l1ll1_opy_)),
                bstack1111l11l11_opy_.get(bstack111l111_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬၧ")), str(bstack1111l11l11_opy_.get(bstack111l111_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬၨ")))
            ]
    def bstack1111l1l111_opy_(self):
        bstack1llll1lll_opy_ = []
        for spec in self.bstack1l111lll11_opy_:
            bstack1llllll11l_opy_ = [spec]
            bstack1llllll11l_opy_ += self.bstack11111ll111_opy_
            bstack1llll1lll_opy_.append(bstack1llllll11l_opy_)
        self.bstack1llll1lll_opy_ = bstack1llll1lll_opy_
        return bstack1llll1lll_opy_
    def bstack1ll1l111l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111llll1_opy_ = True
            return True
        except Exception as e:
            self.bstack11111llll1_opy_ = False
        return self.bstack11111llll1_opy_
    def bstack1llll111ll_opy_(self):
        bstack111l111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࡰࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠪࡷࠥ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠦࡦ࡭ࡣࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦၩ")
        try:
            self.logger.info(bstack111l111_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧၪ"))
            bstack1111ll1111_opy_ = [bstack111l111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥၫ"), *self.bstack11111ll111_opy_, bstack111l111_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧၬ")]
            result = subprocess.run(bstack1111ll1111_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥၭ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack111l111_opy_ (u"ࠨ࠼ࡇࡷࡱࡧࡹ࡯࡯࡯ࠢࠥၮ"))
            self.logger.info(bstack111l111_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧၯ").format(test_count))
            return test_count
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧၰ").format(e))
            return 0
    def bstack1llll11ll1_opy_(self, bstack1111l1ll1l_opy_, bstack1l1l1l11ll_opy_):
        bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩၱ")] = self.bstack11111l1ll1_opy_
        multiprocessing.set_start_method(bstack111l111_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩၲ"))
        bstack11ll1l111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l11l1l_opy_ = manager.list()
        if bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၳ") in self.bstack11111l1ll1_opy_:
            for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨၴ")]):
                bstack11ll1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111l1ll1l_opy_,
                                                            args=(self.bstack11111ll111_opy_, bstack1l1l1l11ll_opy_, bstack1111l11l1l_opy_)))
            bstack11111ll1l1_opy_ = len(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩၵ")])
        else:
            bstack11ll1l111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111l1ll1l_opy_,
                                                        args=(self.bstack11111ll111_opy_, bstack1l1l1l11ll_opy_, bstack1111l11l1l_opy_)))
            bstack11111ll1l1_opy_ = 1
        i = 0
        for t in bstack11ll1l111l_opy_:
            os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧၶ")] = str(i)
            if bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၷ") in self.bstack11111l1ll1_opy_:
                os.environ[bstack111l111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪၸ")] = json.dumps(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ၹ")][i % bstack11111ll1l1_opy_])
            i += 1
            t.start()
        for t in bstack11ll1l111l_opy_:
            t.join()
        return list(bstack1111l11l1l_opy_)
    @staticmethod
    def bstack1ll1lll11l_opy_(driver, bstack11111l11ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨၺ"), None)
        if item and getattr(item, bstack111l111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧၻ"), None) and not getattr(item, bstack111l111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨၼ"), False):
            logger.info(
                bstack111l111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨၽ"))
            bstack1111l11lll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1ll11l1l_opy_.bstack1llllll11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111l1l1ll_opy_(self):
        bstack111l111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢၾ")
        test_files = []
        for arg in self.args:
            if arg.endswith(bstack111l111_opy_ (u"ࠩ࠱ࡴࡾ࠭ၿ")) and os.path.exists(arg):
                test_files.append(arg)
        return test_files