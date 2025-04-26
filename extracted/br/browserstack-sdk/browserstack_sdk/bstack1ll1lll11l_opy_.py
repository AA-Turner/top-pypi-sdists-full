# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack11ll1l1ll1_opy_
from browserstack_sdk.bstack1l1llll1l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l1lll1_opy_
class bstack1ll11l11ll_opy_:
    def __init__(self, args, logger, bstack1111ll1lll_opy_, bstack1111lll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1lllll1_opy_ = []
        self.bstack111l111l1l_opy_ = None
        self.bstack1l1l111l_opy_ = []
        self.bstack111l1111ll_opy_ = self.bstack1llll1ll11_opy_()
        self.bstack1ll11ll111_opy_ = -1
    def bstack11lllll1ll_opy_(self, bstack1111llllll_opy_):
        self.parse_args()
        self.bstack111l1111l1_opy_()
        self.bstack1111lll111_opy_(bstack1111llllll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l11111l_opy_():
        import importlib
        if getattr(importlib, bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭࿫"), False):
            bstack111l111111_opy_ = importlib.find_loader(bstack1l11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ࿬"))
        else:
            bstack111l111111_opy_ = importlib.util.find_spec(bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿭"))
    def bstack1111ll1l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll11ll111_opy_ = -1
        if self.bstack1111lll1ll_opy_ and bstack1l11lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿮") in self.bstack1111ll1lll_opy_:
            self.bstack1ll11ll111_opy_ = int(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿯")])
        try:
            bstack1111lllll1_opy_ = [bstack1l11lll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ࿰"), bstack1l11lll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ࿱"), bstack1l11lll_opy_ (u"ࠨ࠯ࡳࠫ࿲")]
            if self.bstack1ll11ll111_opy_ >= 0:
                bstack1111lllll1_opy_.extend([bstack1l11lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ࿳"), bstack1l11lll_opy_ (u"ࠪ࠱ࡳ࠭࿴")])
            for arg in bstack1111lllll1_opy_:
                self.bstack1111ll1l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l1111l1_opy_(self):
        bstack111l111l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l111l1l_opy_ = bstack111l111l1l_opy_
        return bstack111l111l1l_opy_
    def bstack1llll11l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l11111l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l1lll1_opy_)
    def bstack1111lll111_opy_(self, bstack1111llllll_opy_):
        bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
        if bstack1111llllll_opy_:
            self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࿵"))
            self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"࡚ࠬࡲࡶࡧࠪ࿶"))
        if bstack11lll1l1ll_opy_.bstack1111llll11_opy_():
            self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ࿷"))
            self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠧࡕࡴࡸࡩࠬ࿸"))
        self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠨ࠯ࡳࠫ࿹"))
        self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ࿺"))
        self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ࿻"))
        self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ࿼"))
        if self.bstack1ll11ll111_opy_ > 1:
            self.bstack111l111l1l_opy_.append(bstack1l11lll_opy_ (u"ࠬ࠳࡮ࠨ࿽"))
            self.bstack111l111l1l_opy_.append(str(self.bstack1ll11ll111_opy_))
    def bstack111l111l11_opy_(self):
        bstack1l1l111l_opy_ = []
        for spec in self.bstack11l1lllll1_opy_:
            bstack1l1l1l1ll1_opy_ = [spec]
            bstack1l1l1l1ll1_opy_ += self.bstack111l111l1l_opy_
            bstack1l1l111l_opy_.append(bstack1l1l1l1ll1_opy_)
        self.bstack1l1l111l_opy_ = bstack1l1l111l_opy_
        return bstack1l1l111l_opy_
    def bstack1llll1ll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l1111ll_opy_ = True
            return True
        except Exception as e:
            self.bstack111l1111ll_opy_ = False
        return self.bstack111l1111ll_opy_
    def bstack1l11lll1_opy_(self, bstack1111ll1ll1_opy_, bstack11lllll1ll_opy_):
        bstack11lllll1ll_opy_[bstack1l11lll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭࿾")] = self.bstack1111ll1lll_opy_
        multiprocessing.set_start_method(bstack1l11lll_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭࿿"))
        bstack1ll11ll11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111ll1l1l_opy_ = manager.list()
        if bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက") in self.bstack1111ll1lll_opy_:
            for index, platform in enumerate(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬခ")]):
                bstack1ll11ll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111ll1ll1_opy_,
                                                            args=(self.bstack111l111l1l_opy_, bstack11lllll1ll_opy_, bstack1111ll1l1l_opy_)))
            bstack1111lll1l1_opy_ = len(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဂ")])
        else:
            bstack1ll11ll11l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111ll1ll1_opy_,
                                                        args=(self.bstack111l111l1l_opy_, bstack11lllll1ll_opy_, bstack1111ll1l1l_opy_)))
            bstack1111lll1l1_opy_ = 1
        i = 0
        for t in bstack1ll11ll11l_opy_:
            os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫဃ")] = str(i)
            if bstack1l11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨင") in self.bstack1111ll1lll_opy_:
                os.environ[bstack1l11lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧစ")] = json.dumps(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဆ")][i % bstack1111lll1l1_opy_])
            i += 1
            t.start()
        for t in bstack1ll11ll11l_opy_:
            t.join()
        return list(bstack1111ll1l1l_opy_)
    @staticmethod
    def bstack1l1l1ll11l_opy_(driver, bstack1111lll11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬဇ"), None)
        if item and getattr(item, bstack1l11lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫဈ"), None) and not getattr(item, bstack1l11lll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬဉ"), False):
            logger.info(
                bstack1l11lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥည"))
            bstack1111llll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11ll1l1ll1_opy_.bstack1l111l11l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)