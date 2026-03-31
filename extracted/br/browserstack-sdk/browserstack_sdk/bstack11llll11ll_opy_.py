# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1111l11111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1ll1111l_opy_, bstack1lll11111ll_opy_
from bstack_utils.bstack1l1l1llll1_opy_ import bstack1l1ll11ll1_opy_
from bstack_utils.constants import bstack1lll1111111_opy_
from bstack_utils.bstack11ll1l1l_opy_ import bstack1ll1ll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll111l1l1_opy_ import bstack1lll111ll1l_opy_
class bstack1lll1l111l_opy_:
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1ll1l1_opy_ = []
        self.bstack1ll1lll1ll1_opy_ = []
        self.bstack1lllllllll_opy_ = []
        self.bstack1lll111l111_opy_ = self.bstack1ll1ll1l_opy_()
        self.bstack1ll1ll1lll_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll111lll1_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l11l111_opy_(self, bstack1ll1lll1lll_opy_):
        self.parse_args()
        self.bstack1lll11l1111_opy_()
        self.bstack1ll1lllllll_opy_(bstack1ll1lll1lll_opy_)
        self.bstack1ll1lll1l1l_opy_()
    @measure(event_name=EVENTS.bstack1ll1llll1ll_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l11111l1l_opy_(self):
        bstack11ll1l1l_opy_ = bstack1ll1ll11l1_opy_.get_instance(self.bstack1lllllll11l_opy_, self.logger)
        if bstack11ll1l1l_opy_ is None:
            self.logger.warn(bstack1ll11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦሾ"))
            return
        bstack1llllll1l1l_opy_ = False
        bstack11ll1l1l_opy_.bstack1llllll1lll_opy_(bstack1ll11_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥሿ"), bstack11ll1l1l_opy_.bstack1ll11ll111_opy_())
        start_time = time.time()
        if bstack11ll1l1l_opy_.bstack1ll11ll111_opy_():
            test_files = self.bstack1lll111llll_opy_()
            bstack1llllll1l1l_opy_ = True
            bstack1llllll11l1_opy_ = bstack11ll1l1l_opy_.bstack1llllll1ll1_opy_(test_files)
            if bstack1llllll11l1_opy_:
                self.bstack1l1ll1l1_opy_ = [os.path.normpath(item) for item in bstack1llllll11l1_opy_]
                self.__1lll11l111l_opy_()
                bstack11ll1l1l_opy_.bstack1llllll1l11_opy_(bstack1llllll1l1l_opy_)
                self.logger.info(bstack1ll11_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣቀ").format(self.bstack1l1ll1l1_opy_))
            else:
                self.logger.info(bstack1ll11_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤቁ"))
        bstack11ll1l1l_opy_.bstack1llllll1lll_opy_(bstack1ll11_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣቂ"), int((time.time() - start_time) * 1000)) # bstack1lll111l11l_opy_ to bstack1lll111111l_opy_
    def __1lll11l111l_opy_(self):
        bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡶ࡬ࡢࡥࡨࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡩ࡯ࠢࡆࡐࡎࠦࡦ࡭ࡣࡪࡷࠥࡽࡩࡵࡪࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡸࡺࡸ࡮ࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡲࡦࡳࡥࡴ࠮ࠣࡥࡳࡪࠠࡸࡧࠣࡷ࡮ࡳࡰ࡭ࡻࠣࡹࡵࡪࡡࡵࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡧࡲࡨࡵࠣࡸࡴࠦࡵࡴࡧࠣࡸ࡭ࡵࡳࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠢࡘࡷࡪࡸࠧࡴࠢࡩ࡭ࡱࡺࡥࡳ࡫ࡱ࡫ࠥ࡬࡬ࡢࡩࡶࠤ࠭࠳࡭࠭ࠢ࠰࡯࠮ࠦࡲࡦ࡯ࡤ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷࡥࡨࡺࠠࡢࡰࡧࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡧࡰࡱ࡮࡬ࡩࡩࠦ࡮ࡢࡶࡸࡶࡦࡲ࡬ࡺࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦቃ")
        try:
            if not self.bstack1l1ll1l1_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡏࡱࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡤࡸ࡭ࠦࡴࡰࠢࡶࡩࡹࠨቄ"))
                return
            bstack1lll1111lll_opy_ = []
            for flag in self.bstack1ll1lll1ll1_opy_:
                if flag.startswith(bstack1ll11_opy_ (u"ࠨ࠯ࠪቅ")):
                    bstack1lll1111lll_opy_.append(flag)
                    continue
                bstack1ll1llllll1_opy_ = False
                if bstack1ll11_opy_ (u"ࠩ࠽࠾ࠬቆ") in flag:
                    bstack1ll1llll1l1_opy_ = flag.split(bstack1ll11_opy_ (u"ࠪ࠾࠿࠭ቇ"), 1)[0]
                    if os.path.exists(bstack1ll1llll1l1_opy_):
                        bstack1ll1llllll1_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1ll11_opy_ (u"ࠫ࠳ࡶࡹࠨቈ"))):
                        bstack1ll1llllll1_opy_ = True
                if not bstack1ll1llllll1_opy_:
                    bstack1lll1111lll_opy_.append(flag)
            bstack1lll1111lll_opy_.extend(self.bstack1l1ll1l1_opy_)
            self.bstack1ll1lll1ll1_opy_ = bstack1lll1111lll_opy_
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸࡪࡪࠠࡴࡧ࡯ࡩࡨࡺ࡯ࡳࡵ࠽ࠤࢀࢃࠢ቉").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll11111l1_opy_():
        return bstack1lll111ll1l_opy_(bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨቊ"))
    def bstack1lll1111ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1ll1lll_opy_ = -1
        if self.bstack1llllll11ll_opy_ and bstack1ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧቋ") in self.bstack1lllllll11l_opy_:
            self.bstack1ll1ll1lll_opy_ = int(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨቌ")])
        try:
            bstack1lll11l11ll_opy_ = [bstack1ll11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫቍ"), bstack1ll11_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭቎"), bstack1ll11_opy_ (u"ࠫ࠲ࡶࠧ቏")]
            if self.bstack1ll1ll1lll_opy_ >= 0:
                bstack1lll11l11ll_opy_.extend([bstack1ll11_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ቐ"), bstack1ll11_opy_ (u"࠭࠭࡯ࠩቑ")])
            for arg in bstack1lll11l11ll_opy_:
                self.bstack1lll1111ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll11l1111_opy_(self):
        bstack1ll1lll1ll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll1lll1ll1_opy_ = bstack1ll1lll1ll1_opy_
        return self.bstack1ll1lll1ll1_opy_
    def bstack11lll1ll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll11111l1_opy_():
                self.logger.warning(bstack1lll11111ll_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1ll11_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢቒ"), bstack1l1ll1111l_opy_, str(e))
    def bstack1ll1lllllll_opy_(self, bstack1ll1lll1lll_opy_):
        global_config = Config.get_instance()
        if bstack1ll1lll1lll_opy_:
            self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬቓ"))
            self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠩࡗࡶࡺ࡫ࠧቔ"))
        if global_config.should_skip_session_status():
            self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩቕ"))
            self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"࡙ࠫࡸࡵࡦࠩቖ"))
        self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠬ࠳ࡰࠨ቗"))
        self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫቘ"))
        self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ቙"))
        self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨቚ"))
        if self.bstack1ll1ll1lll_opy_ > 1:
            self.bstack1ll1lll1ll1_opy_.append(bstack1ll11_opy_ (u"ࠩ࠰ࡲࠬቛ"))
            self.bstack1ll1lll1ll1_opy_.append(str(self.bstack1ll1ll1lll_opy_))
    def bstack1ll1lll1l1l_opy_(self):
        if bstack1l1ll11ll1_opy_.bstack1lll1lllll_opy_(self.bstack1lllllll11l_opy_):
             self.bstack1ll1lll1ll1_opy_ += [
                bstack1lll1111111_opy_.get(bstack1ll11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩቜ")), str(bstack1l1ll11ll1_opy_.bstack1111llll11_opy_(self.bstack1lllllll11l_opy_)),
                bstack1lll1111111_opy_.get(bstack1ll11_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪቝ")), str(bstack1lll1111111_opy_.get(bstack1ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪ቞")))
            ]
    def bstack1ll1llll11l_opy_(self):
        bstack1lllllllll_opy_ = []
        for spec in self.bstack1l1ll1l1_opy_:
            bstack111ll1l1ll_opy_ = [spec]
            bstack111ll1l1ll_opy_ += self.bstack1ll1lll1ll1_opy_
            bstack1lllllllll_opy_.append(bstack111ll1l1ll_opy_)
        self.bstack1lllllllll_opy_ = bstack1lllllllll_opy_
        return bstack1lllllllll_opy_
    def bstack1ll1ll1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll111l111_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll111l111_opy_ = False
        return self.bstack1lll111l111_opy_
    @measure(event_name=EVENTS.bstack1lll111l1ll_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1ll1l1lll1_opy_(self):
        bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࡱࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺ࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ቟")
        try:
            from browserstack_sdk.bstack1lll11lll1l_opy_ import bstack1lll11llll1_opy_
            bstack1ll1lllll1l_opy_ = bstack1lll11llll1_opy_(bstack1lll11ll1ll_opy_=self.bstack1ll1lll1ll1_opy_)
            if not bstack1ll1lllll1l_opy_.get(bstack1ll11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨበ"), False):
                self.logger.error(bstack1ll11_opy_ (u"ࠣࡖࡨࡷࡹࠦࡣࡰࡷࡱࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨቡ").format(bstack1ll1lllll1l_opy_.get(bstack1ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቢ"), bstack1ll11_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪባ"))))
                return 0
            count = bstack1ll1lllll1l_opy_.get(bstack1ll11_opy_ (u"ࠫࡨࡵࡵ࡯ࡶࠪቤ"), 0)
            self.logger.info(bstack1ll11_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥብ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥቦ").format(e))
            return 0
    def bstack11l1ll1ll_opy_(self, bstack1lll11l11l1_opy_, bstack1l11l111_opy_):
        bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧቧ")] = self.bstack1lllllll11l_opy_
        multiprocessing.set_start_method(bstack1ll11_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧቨ"))
        bstack1lll1l11l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1111l11_opy_ = manager.list()
        if bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቩ") in self.bstack1lllllll11l_opy_:
            for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቪ")]):
                bstack1lll1l11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll11l11l1_opy_,
                                                            args=(self.bstack1ll1lll1ll1_opy_, bstack1l11l111_opy_, bstack1lll1111l11_opy_)))
            bstack1lll111ll11_opy_ = len(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቫ")])
        else:
            bstack1lll1l11l1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll11l11l1_opy_,
                                                        args=(self.bstack1ll1lll1ll1_opy_, bstack1l11l111_opy_, bstack1lll1111l11_opy_)))
            bstack1lll111ll11_opy_ = 1
        i = 0
        for t in bstack1lll1l11l1_opy_:
            os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬቬ")] = str(i)
            if bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩቭ") in self.bstack1lllllll11l_opy_:
                os.environ[bstack1ll11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨቮ")] = json.dumps(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫቯ")][i % bstack1lll111ll11_opy_])
            i += 1
            t.start()
        for t in bstack1lll1l11l1_opy_:
            t.join()
        return list(bstack1lll1111l11_opy_)
    @staticmethod
    def bstack1ll111ll_opy_(driver, bstack1ll1lllll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ተ"), None)
        if item and getattr(item, bstack1ll11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬቱ"), None) and not getattr(item, bstack1ll11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ቲ"), False):
            logger.info(
                bstack1ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦታ"))
            bstack1ll1llll111_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack1l1l1ll1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll111llll_opy_(self):
        bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧቴ")
        try:
            from browserstack_sdk.bstack1lll11lll1l_opy_ import bstack1lll11llll1_opy_
            bstack1lll1111l1l_opy_ = bstack1lll11llll1_opy_(bstack1lll11ll1ll_opy_=self.bstack1ll1lll1ll1_opy_)
            if not bstack1lll1111l1l_opy_.get(bstack1ll11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨት"), False):
                self.logger.error(bstack1ll11_opy_ (u"ࠣࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧቶ").format(bstack1lll1111l1l_opy_.get(bstack1ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቷ"), bstack1ll11_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪቸ"))))
                return []
            test_files = bstack1lll1111l1l_opy_.get(bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠨቹ"), [])
            count = bstack1lll1111l1l_opy_.get(bstack1ll11_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫቺ"), 0)
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡺࡥࡴࡶࡶࠤ࡮ࡴࠠࡼࡿࠣࡪ࡮ࡲࡥࡴࠤቻ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣቼ").format(e))
            return []