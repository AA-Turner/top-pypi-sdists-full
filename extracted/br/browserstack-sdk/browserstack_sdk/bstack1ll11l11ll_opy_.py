# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack111ll11ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11l1ll11_opy_, bstack1ll11ll1l1l_opy_
from bstack_utils.bstack1l1lll1l11_opy_ import bstack1ll11l11l1_opy_
from bstack_utils.constants import bstack1ll111lll11_opy_
from bstack_utils.bstack111ll111_opy_ import bstack111ll1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11l1l1ll_opy_ import bstack1ll11ll1lll_opy_
class bstack11l1l11ll1_opy_:
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l11l111_opy_ = []
        self.bstack1ll11ll1111_opy_ = []
        self.bstack1lll1ll1ll_opy_ = []
        self.bstack1ll11l1l111_opy_ = self.bstack111ll1l1l1_opy_()
        self.bstack111111l1l_opy_ = -1
    @measure(event_name=EVENTS.bstack1ll111llll1_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1l11l1l1l_opy_(self, bstack1ll11lll1l1_opy_):
        self.parse_args()
        self.bstack1ll11l1lll1_opy_()
        self.bstack1ll111lllll_opy_(bstack1ll11lll1l1_opy_)
        self.bstack1ll111lll1l_opy_()
    @measure(event_name=EVENTS.bstack1ll11ll11ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1llllllll1l_opy_(self):
        bstack111ll111_opy_ = bstack111ll1111l_opy_.bstack111llll11_opy_(self.bstack1lllll11111_opy_, self.logger)
        if bstack111ll111_opy_ is None:
            self.logger.warn(bstack11ll11_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡩࡣࡱࡨࡱ࡫ࡲࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥፕ"))
            return
        bstack1llll1llll1_opy_ = False
        bstack111ll111_opy_.bstack1llll1lll1l_opy_(bstack11ll11_opy_ (u"ࠣࡧࡱࡥࡧࡲࡥࡥࠤፖ"), bstack111ll111_opy_.bstack1ll11lll_opy_())
        start_time = time.time()
        if bstack111ll111_opy_.bstack1ll11lll_opy_():
            test_files = self.bstack1ll11l1111l_opy_()
            bstack1llll1llll1_opy_ = True
            bstack1lllll111l1_opy_ = bstack111ll111_opy_.bstack1llll1lllll_opy_(test_files)
            if bstack1lllll111l1_opy_:
                self.bstack111l11l111_opy_ = [os.path.normpath(item) for item in bstack1lllll111l1_opy_]
                self.__1ll11l1ll11_opy_()
                bstack111ll111_opy_.bstack1lllll1111l_opy_(bstack1llll1llll1_opy_)
                self.logger.info(bstack11ll11_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢፗ").format(self.bstack111l11l111_opy_))
            else:
                self.logger.info(bstack11ll11_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣፘ"))
        bstack111ll111_opy_.bstack1llll1lll1l_opy_(bstack11ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢፙ"), int((time.time() - start_time) * 1000)) # bstack1ll11l11lll_opy_ to bstack1ll11l1llll_opy_
    def __1ll11l1ll11_opy_(self):
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡵࡲࡡࡤࡧࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷࠥ࡯࡮ࠡࡅࡏࡍࠥ࡬࡬ࡢࡩࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡷࡹࡷࡴࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤ࡫࡯࡬ࡦࠢࡱࡥࡲ࡫ࡳ࠭ࠢࡤࡲࡩࠦࡷࡦࠢࡶ࡭ࡲࡶ࡬ࡺࠢࡸࡴࡩࡧࡴࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡄࡎࡌࠤࡦࡸࡧࡴࠢࡷࡳࠥࡻࡳࡦࠢࡷ࡬ࡴࡹࡥࠡࡨ࡬ࡰࡪࡹ࠮ࠡࡗࡶࡩࡷ࠭ࡳࠡࡨ࡬ࡰࡹ࡫ࡲࡪࡰࡪࠤ࡫ࡲࡡࡨࡵࠣࠬ࠲ࡳࠬࠡ࠯࡮࠭ࠥࡸࡥ࡮ࡣ࡬ࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶࡤࡧࡹࠦࡡ࡯ࡦࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡦࡶࡰ࡭࡫ࡨࡨࠥࡴࡡࡵࡷࡵࡥࡱࡲࡹࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥፚ")
        try:
            if not self.bstack111l11l111_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡎࡰࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡱࡣࡷ࡬ࠥࡺ࡯ࠡࡵࡨࡸࠧ፛"))
                return
            bstack1ll11l11111_opy_ = []
            for flag in self.bstack1ll11ll1111_opy_:
                if flag.startswith(bstack11ll11_opy_ (u"ࠧ࠮ࠩ፜")):
                    bstack1ll11l11111_opy_.append(flag)
                    continue
                bstack1ll11l111ll_opy_ = False
                if bstack11ll11_opy_ (u"ࠨ࠼࠽ࠫ፝") in flag:
                    bstack1ll11lll11l_opy_ = flag.split(bstack11ll11_opy_ (u"ࠩ࠽࠾ࠬ፞"), 1)[0]
                    if os.path.exists(bstack1ll11lll11l_opy_):
                        bstack1ll11l111ll_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11ll11_opy_ (u"ࠪ࠲ࡵࡿࠧ፟"))):
                        bstack1ll11l111ll_opy_ = True
                if not bstack1ll11l111ll_opy_:
                    bstack1ll11l11111_opy_.append(flag)
            bstack1ll11l11111_opy_.extend(self.bstack111l11l111_opy_)
            self.bstack1ll11ll1111_opy_ = bstack1ll11l11111_opy_
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡳࡦ࡮ࡨࡧࡹࡵࡲࡴ࠼ࠣࡿࢂࠨ፠").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1ll11l1ll1l_opy_():
        return bstack1ll11ll1lll_opy_(bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ፡"))
    def bstack1ll11l11ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111111l1l_opy_ = -1
        if self.bstack1lllll111ll_opy_ and bstack11ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭።") in self.bstack1lllll11111_opy_:
            self.bstack111111l1l_opy_ = int(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ፣")])
        try:
            bstack1ll11ll1ll1_opy_ = [bstack11ll11_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ፤"), bstack11ll11_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ፥"), bstack11ll11_opy_ (u"ࠪ࠱ࡵ࠭፦")]
            if self.bstack111111l1l_opy_ >= 0:
                bstack1ll11ll1ll1_opy_.extend([bstack11ll11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ፧"), bstack11ll11_opy_ (u"ࠬ࠳࡮ࠨ፨")])
            for arg in bstack1ll11ll1ll1_opy_:
                self.bstack1ll11l11ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11l1lll1_opy_(self):
        bstack1ll11ll1111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11ll1111_opy_ = bstack1ll11ll1111_opy_
        return self.bstack1ll11ll1111_opy_
    def bstack11111llll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1ll11l1ll1l_opy_():
                self.logger.warning(bstack1ll11ll1l1l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11ll11_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ፩"), bstack1l11l1ll11_opy_, str(e))
    def bstack1ll111lllll_opy_(self, bstack1ll11lll1l1_opy_):
        global_config = Config.bstack111llll11_opy_()
        if bstack1ll11lll1l1_opy_:
            self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ፪"))
            self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠨࡖࡵࡹࡪ࠭፫"))
        if global_config.bstack1ll1ll1111l_opy_():
            self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ፬"))
            self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠪࡘࡷࡻࡥࠨ፭"))
        self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠫ࠲ࡶࠧ፮"))
        self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ፯"))
        self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ፰"))
        self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ፱"))
        if self.bstack111111l1l_opy_ > 1:
            self.bstack1ll11ll1111_opy_.append(bstack11ll11_opy_ (u"ࠨ࠯ࡱࠫ፲"))
            self.bstack1ll11ll1111_opy_.append(str(self.bstack111111l1l_opy_))
    def bstack1ll111lll1l_opy_(self):
        if bstack1ll11l11l1_opy_.bstack1111l1lll1_opy_(self.bstack1lllll11111_opy_):
             self.bstack1ll11ll1111_opy_ += [
                bstack1ll111lll11_opy_.get(bstack11ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨ፳")), str(bstack1ll11l11l1_opy_.bstack1llll1l11l_opy_(self.bstack1lllll11111_opy_)),
                bstack1ll111lll11_opy_.get(bstack11ll11_opy_ (u"ࠪࡨࡪࡲࡡࡺࠩ፴")), str(bstack1ll111lll11_opy_.get(bstack11ll11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰ࠰ࡨࡪࡲࡡࡺࠩ፵")))
            ]
    def bstack1ll11l1l11l_opy_(self):
        bstack1lll1ll1ll_opy_ = []
        for spec in self.bstack111l11l111_opy_:
            bstack1lll1ll111_opy_ = [spec]
            bstack1lll1ll111_opy_ += self.bstack1ll11ll1111_opy_
            bstack1lll1ll1ll_opy_.append(bstack1lll1ll111_opy_)
        self.bstack1lll1ll1ll_opy_ = bstack1lll1ll1ll_opy_
        return bstack1lll1ll1ll_opy_
    def bstack111ll1l1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11l1l111_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11l1l111_opy_ = False
        return self.bstack1ll11l1l111_opy_
    @measure(event_name=EVENTS.bstack1ll11ll111l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1ll1l1111l_opy_(self):
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࡰࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ፶")
        try:
            from browserstack_sdk.bstack1ll1l1111l1_opy_ import bstack1ll1l111l1l_opy_
            bstack1ll11l11l1l_opy_ = bstack1ll1l111l1l_opy_(bstack1ll11llllll_opy_=self.bstack1ll11ll1111_opy_)
            if not bstack1ll11l11l1l_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ፷"), False):
                self.logger.error(bstack11ll11_opy_ (u"ࠢࡕࡧࡶࡸࠥࡩ࡯ࡶࡰࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧ፸").format(bstack1ll11l11l1l_opy_.get(bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ፹"), bstack11ll11_opy_ (u"ࠩࡘࡲࡰࡴ࡯ࡸࡰࠣࡩࡷࡸ࡯ࡳࠩ፺"))))
                return 0
            count = bstack1ll11l11l1l_opy_.get(bstack11ll11_opy_ (u"ࠪࡧࡴࡻ࡮ࡵࠩ፻"), 0)
            self.logger.info(bstack11ll11_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠿ࠦࡻࡾࠤ፼").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ፽").format(e))
            return 0
    def bstack1l11111l_opy_(self, bstack1ll11lll111_opy_, bstack1l11l1l1l_opy_):
        bstack1l11l1l1l_opy_[bstack11ll11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭፾")] = self.bstack1lllll11111_opy_
        multiprocessing.set_start_method(bstack11ll11_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭፿"))
        bstack1111l11ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll11l1l1l1_opy_ = manager.list()
        if bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎀ") in self.bstack1lllll11111_opy_:
            for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᎁ")]):
                bstack1111l11ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1ll11lll111_opy_,
                                                            args=(self.bstack1ll11ll1111_opy_, bstack1l11l1l1l_opy_, bstack1ll11l1l1l1_opy_)))
            bstack1ll11l111l1_opy_ = len(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᎂ")])
        else:
            bstack1111l11ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1ll11lll111_opy_,
                                                        args=(self.bstack1ll11ll1111_opy_, bstack1l11l1l1l_opy_, bstack1ll11l1l1l1_opy_)))
            bstack1ll11l111l1_opy_ = 1
        i = 0
        for t in bstack1111l11ll_opy_:
            os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᎃ")] = str(i)
            if bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎄ") in self.bstack1lllll11111_opy_:
                os.environ[bstack11ll11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧᎅ")] = json.dumps(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᎆ")][i % bstack1ll11l111l1_opy_])
            i += 1
            t.start()
        for t in bstack1111l11ll_opy_:
            t.join()
        return list(bstack1ll11l1l1l1_opy_)
    @staticmethod
    def bstack1l1111l111_opy_(driver, bstack1ll11l11l11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᎇ"), None)
        if item and getattr(item, bstack11ll11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫᎈ"), None) and not getattr(item, bstack11ll11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬᎉ"), False):
            logger.info(
                bstack11ll11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥᎊ"))
            bstack1ll11ll11l1_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack1111l1l111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1ll11l1111l_opy_(self):
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡺ࡯ࠡࡤࡨࠤࡪࡾࡥࡤࡷࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᎋ")
        try:
            from browserstack_sdk.bstack1ll1l1111l1_opy_ import bstack1ll1l111l1l_opy_
            bstack1ll11ll1l11_opy_ = bstack1ll1l111l1l_opy_(bstack1ll11llllll_opy_=self.bstack1ll11ll1111_opy_)
            if not bstack1ll11ll1l11_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᎌ"), False):
                self.logger.error(bstack11ll11_opy_ (u"ࠢࡕࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᎍ").format(bstack1ll11ll1l11_opy_.get(bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᎎ"), bstack11ll11_opy_ (u"ࠩࡘࡲࡰࡴ࡯ࡸࡰࠣࡩࡷࡸ࡯ࡳࠩᎏ"))))
                return []
            test_files = bstack1ll11ll1l11_opy_.get(bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠧ᎐"), [])
            count = bstack1ll11ll1l11_opy_.get(bstack11ll11_opy_ (u"ࠫࡨࡵࡵ࡯ࡶࠪ᎑"), 0)
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡉ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠡࡽࢀࠤࡹ࡫ࡳࡵࡵࠣ࡭ࡳࠦࡻࡾࠢࡩ࡭ࡱ࡫ࡳࠣ᎒").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ᎓").format(e))
            return []