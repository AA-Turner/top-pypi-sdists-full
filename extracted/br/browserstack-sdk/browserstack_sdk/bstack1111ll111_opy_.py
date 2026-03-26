# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1ll11l111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack111llllll_opy_, bstack1lll11l111l_opy_
from bstack_utils.bstack1lll111ll_opy_ import bstack1l111111l1_opy_
from bstack_utils.constants import bstack1ll1lllll1l_opy_
from bstack_utils.bstack111l11l1_opy_ import bstack111lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1111lll_opy_ import bstack1ll1llll1l1_opy_
class bstack1l11111l_opy_:
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll1l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11llll1l11_opy_ = []
        self.bstack1lll1111l1l_opy_ = []
        self.bstack1l11ll11l_opy_ = []
        self.bstack1lll111l1ll_opy_ = self.bstack1l1lll1ll_opy_()
        self.bstack1ll1l1ll_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll11l11ll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11lllllll_opy_(self, bstack1ll1lllllll_opy_):
        self.parse_args()
        self.bstack1ll1llll11l_opy_()
        self.bstack1lll1111l11_opy_(bstack1ll1lllllll_opy_)
        self.bstack1lll111ll1l_opy_()
    @measure(event_name=EVENTS.bstack1lll111l11l_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1ll1111lll_opy_(self):
        bstack111l11l1_opy_ = bstack111lll11_opy_.get_instance(self.bstack1lllllll11l_opy_, self.logger)
        if bstack111l11l1_opy_ is None:
            self.logger.warn(bstack1ll1lll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣር"))
            return
        bstack1lllllll1ll_opy_ = False
        bstack111l11l1_opy_.bstack1llllll1ll1_opy_(bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢሮ"), bstack111l11l1_opy_.bstack1l11llll_opy_())
        start_time = time.time()
        if bstack111l11l1_opy_.bstack1l11llll_opy_():
            test_files = self.bstack1lll11l1l11_opy_()
            bstack1lllllll1ll_opy_ = True
            bstack1llllll1lll_opy_ = bstack111l11l1_opy_.bstack1llllll1l1l_opy_(test_files)
            if bstack1llllll1lll_opy_:
                self.bstack11llll1l11_opy_ = [os.path.normpath(item) for item in bstack1llllll1lll_opy_]
                self.__1lll111l1l1_opy_()
                bstack111l11l1_opy_.bstack1llllll11ll_opy_(bstack1lllllll1ll_opy_)
                self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧሯ").format(self.bstack11llll1l11_opy_))
            else:
                self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨሰ"))
        bstack111l11l1_opy_.bstack1llllll1ll1_opy_(bstack1ll1lll_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧሱ"), int((time.time() - start_time) * 1000)) # bstack1lll1111ll1_opy_ to bstack1lll1111111_opy_
    def __1lll111l1l1_opy_(self):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣ࡭ࡳࠦࡃࡍࡋࠣࡪࡱࡧࡧࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡵࡷࡵࡲࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡩ࡭ࡱ࡫ࠠ࡯ࡣࡰࡩࡸ࠲ࠠࡢࡰࡧࠤࡼ࡫ࠠࡴ࡫ࡰࡴࡱࡿࠠࡶࡲࡧࡥࡹ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡉࡌࡊࠢࡤࡶ࡬ࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡵࡪࡲࡷࡪࠦࡦࡪ࡮ࡨࡷ࠳ࠦࡕࡴࡧࡵࠫࡸࠦࡦࡪ࡮ࡷࡩࡷ࡯࡮ࡨࠢࡩࡰࡦ࡭ࡳࠡࠪ࠰ࡱ࠱ࠦ࠭࡬ࠫࠣࡶࡪࡳࡡࡪࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴࡢࡥࡷࠤࡦࡴࡤࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡤࡴࡵࡲࡩࡦࡦࠣࡲࡦࡺࡵࡳࡣ࡯ࡰࡾࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣሲ")
        try:
            if not self.bstack11llll1l11_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡓࡵࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡶࡡࡵࡪࠣࡸࡴࠦࡳࡦࡶࠥሳ"))
                return
            bstack1ll1llllll1_opy_ = []
            for flag in self.bstack1lll1111l1l_opy_:
                if flag.startswith(bstack1ll1lll_opy_ (u"ࠬ࠳ࠧሴ")):
                    bstack1ll1llllll1_opy_.append(flag)
                    continue
                bstack1lll11l11l1_opy_ = False
                if bstack1ll1lll_opy_ (u"࠭࠺࠻ࠩስ") in flag:
                    bstack1lll111l111_opy_ = flag.split(bstack1ll1lll_opy_ (u"ࠧ࠻࠼ࠪሶ"), 1)[0]
                    if os.path.exists(bstack1lll111l111_opy_):
                        bstack1lll11l11l1_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1ll1lll_opy_ (u"ࠨ࠰ࡳࡽࠬሷ"))):
                        bstack1lll11l11l1_opy_ = True
                if not bstack1lll11l11l1_opy_:
                    bstack1ll1llllll1_opy_.append(flag)
            bstack1ll1llllll1_opy_.extend(self.bstack11llll1l11_opy_)
            self.bstack1lll1111l1l_opy_ = bstack1ll1llllll1_opy_
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤࡸ࡫࡬ࡦࡥࡷࡳࡷࡹ࠺ࠡࡽࢀࠦሸ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1ll1llll1ll_opy_():
        return bstack1ll1llll1l1_opy_(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬሹ"))
    def bstack1lll11111ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1l1ll_opy_ = -1
        if self.bstack1llllll1l11_opy_ and bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫሺ") in self.bstack1lllllll11l_opy_:
            self.bstack1ll1l1ll_opy_ = int(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬሻ")])
        try:
            bstack1lll111lll1_opy_ = [bstack1ll1lll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨሼ"), bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪሽ"), bstack1ll1lll_opy_ (u"ࠨ࠯ࡳࠫሾ")]
            if self.bstack1ll1l1ll_opy_ >= 0:
                bstack1lll111lll1_opy_.extend([bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪሿ"), bstack1ll1lll_opy_ (u"ࠪ࠱ࡳ࠭ቀ")])
            for arg in bstack1lll111lll1_opy_:
                self.bstack1lll11111ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll1llll11l_opy_(self):
        bstack1lll1111l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll1111l1l_opy_ = bstack1lll1111l1l_opy_
        return self.bstack1lll1111l1l_opy_
    def bstack11lll1111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1ll1llll1ll_opy_():
                self.logger.warning(bstack1lll11l111l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦቁ"), bstack111llllll_opy_, str(e))
    def bstack1lll1111l11_opy_(self, bstack1ll1lllllll_opy_):
        global_config = Config.get_instance()
        if bstack1ll1lllllll_opy_:
            self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩቂ"))
            self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"࠭ࡔࡳࡷࡨࠫቃ"))
        if global_config.should_skip_session_status():
            self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ቄ"))
            self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠨࡖࡵࡹࡪ࠭ቅ"))
        self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠩ࠰ࡴࠬቆ"))
        self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨቇ"))
        self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ቈ"))
        self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ቉"))
        if self.bstack1ll1l1ll_opy_ > 1:
            self.bstack1lll1111l1l_opy_.append(bstack1ll1lll_opy_ (u"࠭࠭࡯ࠩቊ"))
            self.bstack1lll1111l1l_opy_.append(str(self.bstack1ll1l1ll_opy_))
    def bstack1lll111ll1l_opy_(self):
        if bstack1l111111l1_opy_.bstack11111l1l1_opy_(self.bstack1lllllll11l_opy_):
             self.bstack1lll1111l1l_opy_ += [
                bstack1ll1lllll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭ቋ")), str(bstack1l111111l1_opy_.bstack1ll111111_opy_(self.bstack1lllllll11l_opy_)),
                bstack1ll1lllll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧቌ")), str(bstack1ll1lllll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧቍ")))
            ]
    def bstack1ll1lllll11_opy_(self):
        bstack1l11ll11l_opy_ = []
        for spec in self.bstack11llll1l11_opy_:
            bstack11l1ll11ll_opy_ = [spec]
            bstack11l1ll11ll_opy_ += self.bstack1lll1111l1l_opy_
            bstack1l11ll11l_opy_.append(bstack11l1ll11ll_opy_)
        self.bstack1l11ll11l_opy_ = bstack1l11ll11l_opy_
        return bstack1l11ll11l_opy_
    def bstack1l1lll1ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll111l1ll_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll111l1ll_opy_ = False
        return self.bstack1lll111l1ll_opy_
    @measure(event_name=EVENTS.bstack1lll111111l_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11l11lllll_opy_(self):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ቎")
        try:
            from browserstack_sdk.bstack1lll11ll1l1_opy_ import bstack1lll11lll1l_opy_
            bstack1lll11l1111_opy_ = bstack1lll11lll1l_opy_(bstack1lll11lll11_opy_=self.bstack1lll1111l1l_opy_)
            if not bstack1lll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ቏"), False):
                self.logger.error(bstack1ll1lll_opy_ (u"࡚ࠧࡥࡴࡶࠣࡧࡴࡻ࡮ࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥቐ").format(bstack1lll11l1111_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬቑ"), bstack1ll1lll_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧቒ"))))
                return 0
            count = bstack1lll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡥࡲࡹࡳࡺࠧቓ"), 0)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠽ࠤࢀࢃࠢቔ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢቕ").format(e))
            return 0
    def bstack11l111ll11_opy_(self, bstack1lll11111l1_opy_, bstack11lllllll_opy_):
        bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫቖ")] = self.bstack1lllllll11l_opy_
        multiprocessing.set_start_method(bstack1ll1lll_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫ቗"))
        bstack11111lllll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll111ll11_opy_ = manager.list()
        if bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩቘ") in self.bstack1lllllll11l_opy_:
            for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ቙")]):
                bstack11111lllll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll11111l1_opy_,
                                                            args=(self.bstack1lll1111l1l_opy_, bstack11lllllll_opy_, bstack1lll111ll11_opy_)))
            bstack1lll111llll_opy_ = len(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫቚ")])
        else:
            bstack11111lllll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll11111l1_opy_,
                                                        args=(self.bstack1lll1111l1l_opy_, bstack11lllllll_opy_, bstack1lll111ll11_opy_)))
            bstack1lll111llll_opy_ = 1
        i = 0
        for t in bstack11111lllll_opy_:
            os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩቛ")] = str(i)
            if bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቜ") in self.bstack1lllllll11l_opy_:
                os.environ[bstack1ll1lll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬቝ")] = json.dumps(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ቞")][i % bstack1lll111llll_opy_])
            i += 1
            t.start()
        for t in bstack11111lllll_opy_:
            t.join()
        return list(bstack1lll111ll11_opy_)
    @staticmethod
    def bstack1lll1l111_opy_(driver, bstack1lll11l1l1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ቟"), None)
        if item and getattr(item, bstack1ll1lll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩበ"), None) and not getattr(item, bstack1ll1lll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪቡ"), False):
            logger.info(
                bstack1ll1lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣቢ"))
            bstack1ll1llll111_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack1111l1ll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll11l1l11_opy_(self):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡢࡦࠢࡨࡼࡪࡩࡵࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤባ")
        try:
            from browserstack_sdk.bstack1lll11ll1l1_opy_ import bstack1lll11lll1l_opy_
            bstack1ll1lll1lll_opy_ = bstack1lll11lll1l_opy_(bstack1lll11lll11_opy_=self.bstack1lll1111l1l_opy_)
            if not bstack1ll1lll1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬቤ"), False):
                self.logger.error(bstack1ll1lll_opy_ (u"࡚ࠧࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤብ").format(bstack1ll1lll1lll_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬቦ"), bstack1ll1lll_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧቧ"))))
                return []
            test_files = bstack1ll1lll1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠬቨ"), [])
            count = bstack1ll1lll1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡦࡳࡺࡴࡴࠨቩ"), 0)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷࡩࡩࠦࡻࡾࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࢀࢃࠠࡧ࡫࡯ࡩࡸࠨቪ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧቫ").format(e))
            return []