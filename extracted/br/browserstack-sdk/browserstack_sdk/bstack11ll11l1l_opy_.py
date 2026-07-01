# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1l111lll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11llllll1_opy_, bstack11l1lll1l_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from bstack_utils.constants import bstack11l1l11ll_opy_
from bstack_utils.bstack1llll1ll_opy_ import bstack1ll1l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll1l11l_opy_ import bstack11l1llll1_opy_
class bstack11llll11l_opy_:
    def __init__(self, args, logger, bstack1ll1llll_opy_, bstack1ll1l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
        self.bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll1lll_opy_ = []
        self.bstack11llll1l1_opy_ = []
        self.bstack11l1ll11l_opy_ = []
        self.bstack11ll11111_opy_ = self.bstack11ll1llll_opy_()
        self.bstack11l1ll1l1_opy_ = -1
    @measure(event_name=EVENTS.bstack11lll11l1_opy_, stage=STAGE.SINGLE)
    def bstack11l1l11l1_opy_(self, bstack11lllll1l_opy_):
        self.parse_args()
        self.bstack11l1lll11_opy_()
        self.bstack11l1l1lll_opy_(bstack11lllll1l_opy_)
        self.bstack11ll1l111_opy_()
    @measure(event_name=EVENTS.bstack11ll1ll1l_opy_, stage=STAGE.SINGLE)
    def bstack1lll1111_opy_(self):
        bstack1llll1ll_opy_ = bstack1ll1l1ll_opy_.bstack1lll1l11_opy_(self.bstack1ll1llll_opy_, self.logger)
        if bstack1llll1ll_opy_ is None:
            self.logger.warn(bstack1l1llll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ౉"))
            return
        bstack1lll1l1l_opy_ = False
        bstack1llll1ll_opy_.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦొ"), bstack1llll1ll_opy_.bstack1ll1lll1_opy_())
        start_time = time.time()
        if bstack1llll1ll_opy_.bstack1ll1lll1_opy_():
            test_files = self.bstack11l11lll1_opy_()
            bstack1lll1l1l_opy_ = True
            bstack1lll1ll1_opy_ = bstack1llll1ll_opy_.bstack1llll111_opy_(test_files)
            if bstack1lll1ll1_opy_:
                self.bstack1lll1lll_opy_ = [os.path.normpath(item) for item in bstack1lll1ll1_opy_]
                self.__11l1l1ll1_opy_()
                bstack1llll1ll_opy_.bstack1llll1l1_opy_(bstack1lll1l1l_opy_)
                self.logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤో").format(self.bstack1lll1lll_opy_))
            else:
                self.logger.info(bstack1l1llll_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥౌ"))
        bstack1llll1ll_opy_.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤ్"), int((time.time() - start_time) * 1000)) # bstack11l1l1111_opy_ to bstack11ll1ll11_opy_
    def __11l1l1ll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ౎")
        try:
            if not self.bstack1lll1lll_opy_:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢ౏"))
                return
            bstack11ll11l11_opy_ = []
            for flag in self.bstack11llll1l1_opy_:
                if flag.startswith(bstack1l1llll_opy_ (u"ࠩ࠰ࠫ౐")):
                    bstack11ll11l11_opy_.append(flag)
                    continue
                bstack11lll1l11_opy_ = False
                if bstack1l1llll_opy_ (u"ࠪ࠾࠿࠭౑") in flag:
                    bstack11lllll11_opy_ = flag.split(bstack1l1llll_opy_ (u"ࠫ࠿ࡀࠧ౒"), 1)[0]
                    if os.path.exists(bstack11lllll11_opy_):
                        bstack11lll1l11_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l1llll_opy_ (u"ࠬ࠴ࡰࡺࠩ౓"))):
                        bstack11lll1l11_opy_ = True
                if not bstack11lll1l11_opy_:
                    bstack11ll11l11_opy_.append(flag)
            bstack11ll11l11_opy_.extend(self.bstack1lll1lll_opy_)
            self.bstack11llll1l1_opy_ = bstack11ll11l11_opy_
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣ౔").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll111l1_opy_():
        return bstack11l1llll1_opy_(bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ౕࠩ"))
    def bstack11llll1ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1ll1l1_opy_ = -1
        if self.bstack1ll1l11l_opy_ and bstack1l1llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨౖ") in self.bstack1ll1llll_opy_:
            self.bstack11l1ll1l1_opy_ = int(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ౗")])
        try:
            bstack11lll1ll1_opy_ = [bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬౘ"), bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧౙ"), bstack1l1llll_opy_ (u"ࠬ࠳ࡰࠨౚ")]
            if self.bstack11l1ll1l1_opy_ >= 0:
                bstack11lll1ll1_opy_.extend([bstack1l1llll_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౛"), bstack1l1llll_opy_ (u"ࠧ࠮ࡰࠪ౜")])
            for arg in bstack11lll1ll1_opy_:
                self.bstack11llll1ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1lll11_opy_(self):
        bstack11llll1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11llll1l1_opy_ = bstack11llll1l1_opy_
        return self.bstack11llll1l1_opy_
    def bstack11l11llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack11ll111l1_opy_():
                self.logger.warning(bstack11l1lll1l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣౝ"), bstack11llllll1_opy_, str(e))
    def bstack11l1l1lll_opy_(self, bstack11lllll1l_opy_):
        global_config = Config.bstack1lll1l11_opy_()
        if bstack11lllll1l_opy_:
            self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౞"))
            self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠪࡘࡷࡻࡥࠨ౟"))
        if global_config.bstack11l11l1l_opy_():
            self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪౠ"))
            self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"࡚ࠬࡲࡶࡧࠪౡ"))
        self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"࠭࠭ࡱࠩౢ"))
        self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬౣ"))
        self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ౤"))
        self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ౥"))
        if self.bstack11l1ll1l1_opy_ > 1:
            self.bstack11llll1l1_opy_.append(bstack1l1llll_opy_ (u"ࠪ࠱ࡳ࠭౦"))
            self.bstack11llll1l1_opy_.append(str(self.bstack11l1ll1l1_opy_))
    def bstack11ll1l111_opy_(self):
        if bstack11ll1111l_opy_.bstack11lll1l1l_opy_(self.bstack1ll1llll_opy_):
             self.bstack11llll1l1_opy_ += [
                bstack11l1l11ll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪ౧")), str(bstack11ll1111l_opy_.bstack1l1111111_opy_(self.bstack1ll1llll_opy_)),
                bstack11l1l11ll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫ౨")), str(bstack11l1l11ll_opy_.get(bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫ౩")))
            ]
    def bstack11ll1l1ll_opy_(self):
        bstack11l1ll11l_opy_ = []
        for spec in self.bstack1lll1lll_opy_:
            bstack11lll11ll_opy_ = [spec]
            bstack11lll11ll_opy_ += self.bstack11llll1l1_opy_
            bstack11l1ll11l_opy_.append(bstack11lll11ll_opy_)
        self.bstack11l1ll11l_opy_ = bstack11l1ll11l_opy_
        return bstack11l1ll11l_opy_
    def bstack11ll1llll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll11111_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll11111_opy_ = False
        return self.bstack11ll11111_opy_
    @measure(event_name=EVENTS.bstack11llll111_opy_, stage=STAGE.SINGLE)
    def bstack1l111111l_opy_(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ౪")
        try:
            from browserstack_sdk.bstack1l1111l1l_opy_ import bstack1l11111l1_opy_
            bstack11l1lllll_opy_ = bstack1l11111l1_opy_(bstack1l1111l11_opy_=self.bstack11llll1l1_opy_)
            if not bstack11l1lllll_opy_.get(bstack1l1llll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ౫"), False):
                self.logger.error(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢ౬").format(bstack11l1lllll_opy_.get(bstack1l1llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ౭"), bstack1l1llll_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫ౮"))))
                return 0
            count = bstack11l1lllll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫ౯"), 0)
            self.logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦ౰").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦ౱").format(e))
            return 0
    def bstack11l1l1l11_opy_(self, bstack11ll11ll1_opy_, bstack11l1l11l1_opy_):
        bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ౲")] = self.bstack1ll1llll_opy_
        os.environ[bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡉࡈࡊࡎࡇࡣ࡜ࡕࡒࡌࡇࡕࠦ౳")] = bstack1l1llll_opy_ (u"ࠥ࠵ࠧ౴")
        bstack11lllllll_opy_ = multiprocessing.get_context(bstack1l1llll_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪ౵"))
        bstack11l1ll1ll_opy_ = []
        manager = bstack11lllllll_opy_.Manager()
        bstack11lll111l_opy_ = manager.list()
        bstack11ll111ll_opy_ = self.bstack1ll1l11l_opy_
        if not bstack11ll111ll_opy_:
            bstack11l1ll1ll_opy_.append(bstack11lllllll_opy_.Process(name=str(0),
                                                        target=bstack11ll11ll1_opy_,
                                                        args=(self.bstack11llll1l1_opy_, bstack11l1l11l1_opy_, bstack11lll111l_opy_)))
            bstack11ll1l1l1_opy_ = 1
        elif bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౶") in self.bstack1ll1llll_opy_:
            for index, platform in enumerate(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౷")]):
                bstack11l1ll1ll_opy_.append(bstack11lllllll_opy_.Process(name=str(index),
                                                            target=bstack11ll11ll1_opy_,
                                                            args=(self.bstack11llll1l1_opy_, bstack11l1l11l1_opy_, bstack11lll111l_opy_)))
            bstack11ll1l1l1_opy_ = len(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౸")])
        else:
            bstack11l1ll1ll_opy_.append(bstack11lllllll_opy_.Process(name=str(0),
                                                        target=bstack11ll11ll1_opy_,
                                                        args=(self.bstack11llll1l1_opy_, bstack11l1l11l1_opy_, bstack11lll111l_opy_)))
            bstack11ll1l1l1_opy_ = 1
        bstack11lll1lll_opy_ = None
        if not bstack11ll111ll_opy_:
            try:
                bstack11lll1lll_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡖࡄࡗࡐࡥࡉࡅࠩ౹"), bstack1l1llll_opy_ (u"ࠩ࠳ࠫ౺")) or 0)
            except ValueError:
                bstack11lll1lll_opy_ = 0
        i = 0
        for t in bstack11l1ll1ll_opy_:
            if bstack11lll1lll_opy_ is not None:
                os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ౻")] = str(bstack11lll1lll_opy_ % bstack11ll1l1l1_opy_) if bstack11ll1l1l1_opy_ else bstack1l1llll_opy_ (u"ࠫ࠵࠭౼")
            else:
                os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ౽")] = str(i)
            if bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౾") in self.bstack1ll1llll_opy_:
                idx = (bstack11lll1lll_opy_ if bstack11lll1lll_opy_ is not None else i) % bstack11ll1l1l1_opy_
                os.environ[bstack1l1llll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ౿")] = json.dumps(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಀ")][idx])
            i += 1
            t.start()
        for t in bstack11l1ll1ll_opy_:
            t.join()
        return list(bstack11lll111l_opy_)
    @staticmethod
    def bstack11l1ll111_opy_(driver, bstack11lll1111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ಁ"), None)
        if item and getattr(item, bstack1l1llll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬಂ"), None) and not getattr(item, bstack1l1llll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ಃ"), False):
            logger.info(
                bstack1l1llll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦ಄"))
            bstack11l1l1l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack11ll11lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack11l11lll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧಅ")
        try:
            from browserstack_sdk.bstack1l1111l1l_opy_ import bstack1l11111l1_opy_
            bstack11l1l111l_opy_ = bstack1l11111l1_opy_(bstack1l1111l11_opy_=self.bstack11llll1l1_opy_)
            if not bstack11l1l111l_opy_.get(bstack1l1llll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨಆ"), False):
                self.logger.error(bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧಇ").format(bstack11l1l111l_opy_.get(bstack1l1llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨಈ"), bstack1l1llll_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪಉ"))))
                return []
            test_files = bstack11l1l111l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠨಊ"), [])
            count = bstack11l1l111l_opy_.get(bstack1l1llll_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫಋ"), 0)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡺࡥࡴࡶࡶࠤ࡮ࡴࠠࡼࡿࠣࡪ࡮ࡲࡥࡴࠤಌ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ಍").format(e))
            return []