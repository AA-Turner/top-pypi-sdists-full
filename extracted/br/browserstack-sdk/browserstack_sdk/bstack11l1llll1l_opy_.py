# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1l11l1llll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11l111_opy_, bstack1ll11l1111l_opy_
from bstack_utils.bstack1111l11l_opy_ import bstack1l1l111111_opy_
from bstack_utils.constants import bstack1ll11l1l1l1_opy_
from bstack_utils.bstack1llll1ll_opy_ import bstack11l1111ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11l1ll11_opy_ import bstack1ll11ll1lll_opy_
class bstack1ll11l1lll_opy_:
    def __init__(self, args, logger, bstack1llll1lll11_opy_, bstack1lllll11111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1111lll1_opy_ = []
        self.bstack1ll11ll1ll1_opy_ = []
        self.bstack11ll111ll1_opy_ = []
        self.bstack1ll11l1l111_opy_ = self.bstack11lll1111l_opy_()
        self.bstack11ll11l1_opy_ = -1
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack1l11ll11l1_opy_(self, bstack1ll11l11l1l_opy_):
        self.parse_args()
        self.bstack1ll111lllll_opy_()
        self.bstack1ll11l111ll_opy_(bstack1ll11l11l1l_opy_)
        self.bstack1ll11ll1l11_opy_()
    @measure(event_name=EVENTS.bstack1ll11ll1l1l_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack111ll1lll_opy_(self):
        bstack1llll1ll_opy_ = bstack11l1111ll1_opy_.bstack1ll11ll111_opy_(self.bstack1llll1lll11_opy_, self.logger)
        if bstack1llll1ll_opy_ is None:
            self.logger.warn(bstack1l111l_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ፬"))
            return
        bstack1llll1ll1ll_opy_ = False
        bstack1llll1ll_opy_.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦ፭"), bstack1llll1ll_opy_.bstack1lll1lll1_opy_())
        start_time = time.time()
        if bstack1llll1ll_opy_.bstack1lll1lll1_opy_():
            test_files = self.bstack1ll111llll1_opy_()
            bstack1llll1ll1ll_opy_ = True
            bstack1llll1ll1l1_opy_ = bstack1llll1ll_opy_.bstack1lllll1111l_opy_(test_files)
            if bstack1llll1ll1l1_opy_:
                self.bstack1111lll1_opy_ = [os.path.normpath(item) for item in bstack1llll1ll1l1_opy_]
                self.__1ll11ll11l1_opy_()
                bstack1llll1ll_opy_.bstack1llll1lll1l_opy_(bstack1llll1ll1ll_opy_)
                self.logger.info(bstack1l111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ፮").format(self.bstack1111lll1_opy_))
            else:
                self.logger.info(bstack1l111l_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥ፯"))
        bstack1llll1ll_opy_.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤ፰"), int((time.time() - start_time) * 1000)) # bstack1ll11ll1111_opy_ to bstack1ll111ll1l1_opy_
    def __1ll11ll11l1_opy_(self):
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ፱")
        try:
            if not self.bstack1111lll1_opy_:
                self.logger.debug(bstack1l111l_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢ፲"))
                return
            bstack1ll11l1llll_opy_ = []
            for flag in self.bstack1ll11ll1ll1_opy_:
                if flag.startswith(bstack1l111l_opy_ (u"ࠩ࠰ࠫ፳")):
                    bstack1ll11l1llll_opy_.append(flag)
                    continue
                bstack1ll11ll111l_opy_ = False
                if bstack1l111l_opy_ (u"ࠪ࠾࠿࠭፴") in flag:
                    bstack1ll111lll11_opy_ = flag.split(bstack1l111l_opy_ (u"ࠫ࠿ࡀࠧ፵"), 1)[0]
                    if os.path.exists(bstack1ll111lll11_opy_):
                        bstack1ll11ll111l_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l111l_opy_ (u"ࠬ࠴ࡰࡺࠩ፶"))):
                        bstack1ll11ll111l_opy_ = True
                if not bstack1ll11ll111l_opy_:
                    bstack1ll11l1llll_opy_.append(flag)
            bstack1ll11l1llll_opy_.extend(self.bstack1111lll1_opy_)
            self.bstack1ll11ll1ll1_opy_ = bstack1ll11l1llll_opy_
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣ፷").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1ll11l111l1_opy_():
        return bstack1ll11ll1lll_opy_(bstack1l111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ፸"))
    def bstack1ll111lll1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11ll11l1_opy_ = -1
        if self.bstack1lllll11111_opy_ and bstack1l111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ፹") in self.bstack1llll1lll11_opy_:
            self.bstack11ll11l1_opy_ = int(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ፺")])
        try:
            bstack1ll11l1lll1_opy_ = [bstack1l111l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ፻"), bstack1l111l_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧ፼"), bstack1l111l_opy_ (u"ࠬ࠳ࡰࠨ፽")]
            if self.bstack11ll11l1_opy_ >= 0:
                bstack1ll11l1lll1_opy_.extend([bstack1l111l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ፾"), bstack1l111l_opy_ (u"ࠧ࠮ࡰࠪ፿")])
            for arg in bstack1ll11l1lll1_opy_:
                self.bstack1ll111lll1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll111lllll_opy_(self):
        bstack1ll11ll1ll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11ll1ll1_opy_ = bstack1ll11ll1ll1_opy_
        return self.bstack1ll11ll1ll1_opy_
    def bstack1ll11ll1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1ll11l111l1_opy_():
                self.logger.warning(bstack1ll11l1111l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l111l_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣᎀ"), bstack1l11l111_opy_, str(e))
    def bstack1ll11l111ll_opy_(self, bstack1ll11l11l1l_opy_):
        global_config = Config.bstack1ll11ll111_opy_()
        if bstack1ll11l11l1l_opy_:
            self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᎁ"))
            self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠪࡘࡷࡻࡥࠨᎂ"))
        if global_config.bstack1lll111ll11_opy_():
            self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᎃ"))
            self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"࡚ࠬࡲࡶࡧࠪᎄ"))
        self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"࠭࠭ࡱࠩᎅ"))
        self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬᎆ"))
        self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪᎇ"))
        self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᎈ"))
        if self.bstack11ll11l1_opy_ > 1:
            self.bstack1ll11ll1ll1_opy_.append(bstack1l111l_opy_ (u"ࠪ࠱ࡳ࠭ᎉ"))
            self.bstack1ll11ll1ll1_opy_.append(str(self.bstack11ll11l1_opy_))
    def bstack1ll11ll1l11_opy_(self):
        if bstack1l1l111111_opy_.bstack11l111l11_opy_(self.bstack1llll1lll11_opy_):
             self.bstack1ll11ll1ll1_opy_ += [
                bstack1ll11l1l1l1_opy_.get(bstack1l111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪᎊ")), str(bstack1l1l111111_opy_.bstack1l1l111l_opy_(self.bstack1llll1lll11_opy_)),
                bstack1ll11l1l1l1_opy_.get(bstack1l111l_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫᎋ")), str(bstack1ll11l1l1l1_opy_.get(bstack1l111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫᎌ")))
            ]
    def bstack1ll11l11ll1_opy_(self):
        bstack11ll111ll1_opy_ = []
        for spec in self.bstack1111lll1_opy_:
            bstack1llll1l1ll_opy_ = [spec]
            bstack1llll1l1ll_opy_ += self.bstack1ll11ll1ll1_opy_
            bstack11ll111ll1_opy_.append(bstack1llll1l1ll_opy_)
        self.bstack11ll111ll1_opy_ = bstack11ll111ll1_opy_
        return bstack11ll111ll1_opy_
    def bstack11lll1111l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11l1l111_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11l1l111_opy_ = False
        return self.bstack1ll11l1l111_opy_
    @measure(event_name=EVENTS.bstack1ll11lll111_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack1l1l111l1_opy_(self):
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᎍ")
        try:
            from browserstack_sdk.bstack1ll11lllll1_opy_ import bstack1ll1l111111_opy_
            bstack1ll11l11lll_opy_ = bstack1ll1l111111_opy_(bstack1ll1l111l11_opy_=self.bstack1ll11ll1ll1_opy_)
            if not bstack1ll11l11lll_opy_.get(bstack1l111l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᎎ"), False):
                self.logger.error(bstack1l111l_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢᎏ").format(bstack1ll11l11lll_opy_.get(bstack1l111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᎐"), bstack1l111l_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫ᎑"))))
                return 0
            count = bstack1ll11l11lll_opy_.get(bstack1l111l_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫ᎒"), 0)
            self.logger.info(bstack1l111l_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦ᎓").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦ᎔").format(e))
            return 0
    def bstack11lllll11_opy_(self, bstack1ll11l1l1ll_opy_, bstack1l11ll11l1_opy_):
        bstack1l11ll11l1_opy_[bstack1l111l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ᎕")] = self.bstack1llll1lll11_opy_
        multiprocessing.set_start_method(bstack1l111l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨ᎖"))
        bstack11l1llll11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll11ll11ll_opy_ = manager.list()
        if bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᎗") in self.bstack1llll1lll11_opy_:
            for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᎘")]):
                bstack11l1llll11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1ll11l1l1ll_opy_,
                                                            args=(self.bstack1ll11ll1ll1_opy_, bstack1l11ll11l1_opy_, bstack1ll11ll11ll_opy_)))
            bstack1ll11l11111_opy_ = len(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᎙")])
        else:
            bstack11l1llll11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1ll11l1l1ll_opy_,
                                                        args=(self.bstack1ll11ll1ll1_opy_, bstack1l11ll11l1_opy_, bstack1ll11ll11ll_opy_)))
            bstack1ll11l11111_opy_ = 1
        i = 0
        for t in bstack11l1llll11_opy_:
            os.environ[bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᎚")] = str(i)
            if bstack1l111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᎛") in self.bstack1llll1lll11_opy_:
                os.environ[bstack1l111l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ᎜")] = json.dumps(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᎝")][i % bstack1ll11l11111_opy_])
            i += 1
            t.start()
        for t in bstack11l1llll11_opy_:
            t.join()
        return list(bstack1ll11ll11ll_opy_)
    @staticmethod
    def bstack11ll111111_opy_(driver, bstack1ll111ll1ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᎞"), None)
        if item and getattr(item, bstack1l111l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭᎟"), None) and not getattr(item, bstack1l111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧᎠ"), False):
            logger.info(
                bstack1l111l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧᎡ"))
            bstack1ll11l1ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack1ll111l1ll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1ll111llll1_opy_(self):
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᎢ")
        try:
            from browserstack_sdk.bstack1ll11lllll1_opy_ import bstack1ll1l111111_opy_
            bstack1ll11l1l11l_opy_ = bstack1ll1l111111_opy_(bstack1ll1l111l11_opy_=self.bstack1ll11ll1ll1_opy_)
            if not bstack1ll11l1l11l_opy_.get(bstack1l111l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᎣ"), False):
                self.logger.error(bstack1l111l_opy_ (u"ࠤࡗࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨᎤ").format(bstack1ll11l1l11l_opy_.get(bstack1l111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᎥ"), bstack1l111l_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫᎦ"))))
                return []
            test_files = bstack1ll11l1l11l_opy_.get(bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠩᎧ"), [])
            count = bstack1ll11l1l11l_opy_.get(bstack1l111l_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᎨ"), 0)
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡿࢂࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡽࢀࠤ࡫࡯࡬ࡦࡵࠥᎩ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᎪ").format(e))
            return []