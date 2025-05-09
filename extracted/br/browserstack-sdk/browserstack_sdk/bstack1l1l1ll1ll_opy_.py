# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack11l1lll11_opy_
from browserstack_sdk.bstack1l1lllll11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11lllll1ll_opy_
class bstack1ll11l11_opy_:
    def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111lll111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11llll1l1_opy_ = []
        self.bstack111l111111_opy_ = None
        self.bstack1lll1llll_opy_ = []
        self.bstack1111lllll1_opy_ = self.bstack1ll11ll1_opy_()
        self.bstack1ll1ll11l_opy_ = -1
    def bstack1l1l1llll1_opy_(self, bstack1111llll1l_opy_):
        self.parse_args()
        self.bstack111l111l11_opy_()
        self.bstack1111ll1l11_opy_(bstack1111llll1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l1111ll_opy_():
        import importlib
        if getattr(importlib, bstack11lll_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭࿫"), False):
            bstack111l1111l1_opy_ = importlib.find_loader(bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ࿬"))
        else:
            bstack111l1111l1_opy_ = importlib.util.find_spec(bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿭"))
    def bstack1111ll1l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1ll11l_opy_ = -1
        if self.bstack1111lll111_opy_ and bstack11lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿮") in self.bstack1111ll1ll1_opy_:
            self.bstack1ll1ll11l_opy_ = int(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿯")])
        try:
            bstack1111lll1l1_opy_ = [bstack11lll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ࿰"), bstack11lll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ࿱"), bstack11lll_opy_ (u"ࠨ࠯ࡳࠫ࿲")]
            if self.bstack1ll1ll11l_opy_ >= 0:
                bstack1111lll1l1_opy_.extend([bstack11lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ࿳"), bstack11lll_opy_ (u"ࠪ࠱ࡳ࠭࿴")])
            for arg in bstack1111lll1l1_opy_:
                self.bstack1111ll1l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l111l11_opy_(self):
        bstack111l111111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l111111_opy_ = bstack111l111111_opy_
        return bstack111l111111_opy_
    def bstack1ll11lll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l1111ll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11lllll1ll_opy_)
    def bstack1111ll1l11_opy_(self, bstack1111llll1l_opy_):
        bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
        if bstack1111llll1l_opy_:
            self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࿵"))
            self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"࡚ࠬࡲࡶࡧࠪ࿶"))
        if bstack1llllll11_opy_.bstack1111ll11ll_opy_():
            self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ࿷"))
            self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠧࡕࡴࡸࡩࠬ࿸"))
        self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠨ࠯ࡳࠫ࿹"))
        self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ࿺"))
        self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ࿻"))
        self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ࿼"))
        if self.bstack1ll1ll11l_opy_ > 1:
            self.bstack111l111111_opy_.append(bstack11lll_opy_ (u"ࠬ࠳࡮ࠨ࿽"))
            self.bstack111l111111_opy_.append(str(self.bstack1ll1ll11l_opy_))
    def bstack1111lll1ll_opy_(self):
        bstack1lll1llll_opy_ = []
        for spec in self.bstack11llll1l1_opy_:
            bstack1llll1llll_opy_ = [spec]
            bstack1llll1llll_opy_ += self.bstack111l111111_opy_
            bstack1lll1llll_opy_.append(bstack1llll1llll_opy_)
        self.bstack1lll1llll_opy_ = bstack1lll1llll_opy_
        return bstack1lll1llll_opy_
    def bstack1ll11ll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111lllll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1111lllll1_opy_ = False
        return self.bstack1111lllll1_opy_
    def bstack1111lll1_opy_(self, bstack1111ll1lll_opy_, bstack1l1l1llll1_opy_):
        bstack1l1l1llll1_opy_[bstack11lll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭࿾")] = self.bstack1111ll1ll1_opy_
        multiprocessing.set_start_method(bstack11lll_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭࿿"))
        bstack111l1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l11111l_opy_ = manager.list()
        if bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက") in self.bstack1111ll1ll1_opy_:
            for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬခ")]):
                bstack111l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111ll1lll_opy_,
                                                            args=(self.bstack111l111111_opy_, bstack1l1l1llll1_opy_, bstack111l11111l_opy_)))
            bstack1111llllll_opy_ = len(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဂ")])
        else:
            bstack111l1111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111ll1lll_opy_,
                                                        args=(self.bstack111l111111_opy_, bstack1l1l1llll1_opy_, bstack111l11111l_opy_)))
            bstack1111llllll_opy_ = 1
        i = 0
        for t in bstack111l1111_opy_:
            os.environ[bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫဃ")] = str(i)
            if bstack11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨင") in self.bstack1111ll1ll1_opy_:
                os.environ[bstack11lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧစ")] = json.dumps(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဆ")][i % bstack1111llllll_opy_])
            i += 1
            t.start()
        for t in bstack111l1111_opy_:
            t.join()
        return list(bstack111l11111l_opy_)
    @staticmethod
    def bstack1ll11l11l_opy_(driver, bstack1111lll11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬဇ"), None)
        if item and getattr(item, bstack11lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫဈ"), None) and not getattr(item, bstack11lll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬဉ"), False):
            logger.info(
                bstack11lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥည"))
            bstack1111llll11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l1lll11_opy_.bstack1lll1l1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)