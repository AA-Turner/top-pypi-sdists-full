# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1l11l11ll1_opy_
import subprocess
from browserstack_sdk.bstack1l11111l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1l1ll1l_opy_
from bstack_utils.bstack1ll1ll1l_opy_ import bstack1lllll1l11_opy_
from bstack_utils.constants import bstack1111ll111l_opy_
class bstack1llll1l111_opy_:
    def __init__(self, args, logger, bstack1111l1l1ll_opy_, bstack1111ll1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
        self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l11l1l_opy_ = []
        self.bstack1111lll111_opy_ = None
        self.bstack1l1lll1l1_opy_ = []
        self.bstack1111l11ll1_opy_ = self.bstack1llllll1l1_opy_()
        self.bstack11ll1ll1l1_opy_ = -1
    def bstack1lll1l11_opy_(self, bstack1111l1l11l_opy_):
        self.parse_args()
        self.bstack1111l1ll11_opy_()
        self.bstack1111ll1ll1_opy_(bstack1111l1l11l_opy_)
        self.bstack1111ll1lll_opy_()
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l1ll1l_opy_():
        import importlib
        if getattr(importlib, bstack111lll_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧဏ"), False):
            bstack1111l1l111_opy_ = importlib.find_loader(bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬတ"))
        else:
            bstack1111l1l111_opy_ = importlib.util.find_spec(bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ထ"))
    def bstack1111ll11ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11ll1ll1l1_opy_ = -1
        if self.bstack1111ll1111_opy_ and bstack111lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬဒ") in self.bstack1111l1l1ll_opy_:
            self.bstack11ll1ll1l1_opy_ = int(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ဓ")])
        try:
            bstack1111l1l1l1_opy_ = [bstack111lll_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩန"), bstack111lll_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫပ"), bstack111lll_opy_ (u"ࠩ࠰ࡴࠬဖ")]
            if self.bstack11ll1ll1l1_opy_ >= 0:
                bstack1111l1l1l1_opy_.extend([bstack111lll_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫဗ"), bstack111lll_opy_ (u"ࠫ࠲ࡴࠧဘ")])
            for arg in bstack1111l1l1l1_opy_:
                self.bstack1111ll11ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111l1ll11_opy_(self):
        bstack1111lll111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
        return bstack1111lll111_opy_
    def bstack11llll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l1ll1l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1l1ll1l_opy_)
    def bstack1111ll1ll1_opy_(self, bstack1111l1l11l_opy_):
        bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
        if bstack1111l1l11l_opy_:
            self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩမ"))
            self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"࠭ࡔࡳࡷࡨࠫယ"))
        if bstack1ll1l11ll_opy_.bstack1111ll1l1l_opy_():
            self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ရ"))
            self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠨࡖࡵࡹࡪ࠭လ"))
        self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠩ࠰ࡴࠬဝ"))
        self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨသ"))
        self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ဟ"))
        self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬဠ"))
        if self.bstack11ll1ll1l1_opy_ > 1:
            self.bstack1111lll111_opy_.append(bstack111lll_opy_ (u"࠭࠭࡯ࠩအ"))
            self.bstack1111lll111_opy_.append(str(self.bstack11ll1ll1l1_opy_))
    def bstack1111ll1lll_opy_(self):
        if bstack1lllll1l11_opy_.bstack1l1111111_opy_(self.bstack1111l1l1ll_opy_):
             self.bstack1111lll111_opy_ += [
                bstack1111ll111l_opy_.get(bstack111lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭ဢ")), str(bstack1lllll1l11_opy_.bstack1l1ll1l1l_opy_(self.bstack1111l1l1ll_opy_)),
                bstack1111ll111l_opy_.get(bstack111lll_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧဣ")), str(bstack1111ll111l_opy_.get(bstack111lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧဤ")))
            ]
    def bstack1111l11l1l_opy_(self):
        bstack1l1lll1l1_opy_ = []
        for spec in self.bstack11l11l1l_opy_:
            bstack11l1ll1111_opy_ = [spec]
            bstack11l1ll1111_opy_ += self.bstack1111lll111_opy_
            bstack1l1lll1l1_opy_.append(bstack11l1ll1111_opy_)
        self.bstack1l1lll1l1_opy_ = bstack1l1lll1l1_opy_
        return bstack1l1lll1l1_opy_
    def bstack1llllll1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111l11ll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1111l11ll1_opy_ = False
        return self.bstack1111l11ll1_opy_
    def bstack11111111_opy_(self, logger):
        bstack111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠡࡨ࡯ࡥ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨဥ")
        try:
            logger.info(bstack111lll_opy_ (u"ࠦࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢဦ"))
            bstack1111lll11l_opy_ = [bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧဧ"), *self.bstack1111lll111_opy_, bstack111lll_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢဨ")]
            result = subprocess.run(bstack1111lll11l_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                logger.error(bstack111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧဩ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack111lll_opy_ (u"ࠣ࠾ࡉࡹࡳࡩࡴࡪࡱࡱࠤࠧဪ"))
            logger.info(bstack111lll_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠽ࠤࢀࢃࠢါ").format(test_count))
            return test_count
        except Exception as e:
            logger.error(bstack111lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢာ").format(e))
            return 0
    def bstack1ll11ll111_opy_(self, bstack1111ll1l11_opy_, bstack1lll1l11_opy_):
        bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫိ")] = self.bstack1111l1l1ll_opy_
        multiprocessing.set_start_method(bstack111lll_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫီ"))
        bstack1l111ll1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l1llll_opy_ = manager.list()
        if bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩု") in self.bstack1111l1l1ll_opy_:
            for index, platform in enumerate(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪူ")]):
                bstack1l111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111ll1l11_opy_,
                                                            args=(self.bstack1111lll111_opy_, bstack1lll1l11_opy_, bstack1111l1llll_opy_)))
            bstack1111l11lll_opy_ = len(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫေ")])
        else:
            bstack1l111ll1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111ll1l11_opy_,
                                                        args=(self.bstack1111lll111_opy_, bstack1lll1l11_opy_, bstack1111l1llll_opy_)))
            bstack1111l11lll_opy_ = 1
        i = 0
        for t in bstack1l111ll1l_opy_:
            os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩဲ")] = str(i)
            if bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဳ") in self.bstack1111l1l1ll_opy_:
                os.environ[bstack111lll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬဴ")] = json.dumps(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဵ")][i % bstack1111l11lll_opy_])
            i += 1
            t.start()
        for t in bstack1l111ll1l_opy_:
            t.join()
        return list(bstack1111l1llll_opy_)
    @staticmethod
    def bstack1ll1ll1ll_opy_(driver, bstack1111l1lll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪံ"), None)
        if item and getattr(item, bstack111lll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦ့ࠩ"), None) and not getattr(item, bstack111lll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪး"), False):
            logger.info(
                bstack111lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮္ࠣ"))
            bstack1111ll11l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11l11ll1_opy_.bstack1ll1ll1l11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)