# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1111llllll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll11l11_opy_, bstack1ll11l1ll11_opy_
from bstack_utils.bstack1l111111l_opy_ import bstack111ll1ll_opy_
from bstack_utils.constants import bstack1ll111lllll_opy_
from bstack_utils.bstack111l1l11l_opy_ import bstack11l1l11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11l1ll1l_opy_ import bstack1ll11l11ll1_opy_
class bstack111l111ll_opy_:
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1111lll11_opy_ = []
        self.bstack1ll11l1111l_opy_ = []
        self.bstack11111111ll_opy_ = []
        self.bstack1ll11ll1l1l_opy_ = self.bstack1ll11llll_opy_()
        self.bstack11l11l1l1_opy_ = -1
    @measure(event_name=EVENTS.bstack1ll11ll111l_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11111lllll_opy_(self, bstack1ll11ll1lll_opy_):
        self.parse_args()
        self.bstack1ll11ll11l1_opy_()
        self.bstack1ll11l1l111_opy_(bstack1ll11ll1lll_opy_)
        self.bstack1ll11l111ll_opy_()
    @measure(event_name=EVENTS.bstack1ll11l1l1l1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack1lll11l1l_opy_(self):
        bstack111l1l11l_opy_ = bstack11l1l11lll_opy_.bstack1lll111ll_opy_(self.bstack1lllll11111_opy_, self.logger)
        if bstack111l1l11l_opy_ is None:
            self.logger.warn(bstack111l_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡩࡣࡱࡨࡱ࡫ࡲࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥፕ"))
            return
        bstack1lllll11l1l_opy_ = False
        bstack111l1l11l_opy_.bstack1llll1lllll_opy_(bstack111l_opy_ (u"ࠣࡧࡱࡥࡧࡲࡥࡥࠤፖ"), bstack111l1l11l_opy_.bstack1l1l1ll1l_opy_())
        start_time = time.time()
        if bstack111l1l11l_opy_.bstack1l1l1ll1l_opy_():
            test_files = self.bstack1ll11l11lll_opy_()
            bstack1lllll11l1l_opy_ = True
            bstack1lllll1111l_opy_ = bstack111l1l11l_opy_.bstack1llll1llll1_opy_(test_files)
            if bstack1lllll1111l_opy_:
                self.bstack1111lll11_opy_ = [os.path.normpath(item) for item in bstack1lllll1111l_opy_]
                self.__1ll111lll11_opy_()
                bstack111l1l11l_opy_.bstack1lllll111l1_opy_(bstack1lllll11l1l_opy_)
                self.logger.info(bstack111l_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢፗ").format(self.bstack1111lll11_opy_))
            else:
                self.logger.info(bstack111l_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣፘ"))
        bstack111l1l11l_opy_.bstack1llll1lllll_opy_(bstack111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢፙ"), int((time.time() - start_time) * 1000)) # bstack1ll11lll111_opy_ to bstack1ll11l1llll_opy_
    def __1ll111lll11_opy_(self):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡵࡲࡡࡤࡧࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷࠥ࡯࡮ࠡࡅࡏࡍࠥ࡬࡬ࡢࡩࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡷࡹࡷࡴࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤ࡫࡯࡬ࡦࠢࡱࡥࡲ࡫ࡳ࠭ࠢࡤࡲࡩࠦࡷࡦࠢࡶ࡭ࡲࡶ࡬ࡺࠢࡸࡴࡩࡧࡴࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡄࡎࡌࠤࡦࡸࡧࡴࠢࡷࡳࠥࡻࡳࡦࠢࡷ࡬ࡴࡹࡥࠡࡨ࡬ࡰࡪࡹ࠮ࠡࡗࡶࡩࡷ࠭ࡳࠡࡨ࡬ࡰࡹ࡫ࡲࡪࡰࡪࠤ࡫ࡲࡡࡨࡵࠣࠬ࠲ࡳࠬࠡ࠯࡮࠭ࠥࡸࡥ࡮ࡣ࡬ࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶࡤࡧࡹࠦࡡ࡯ࡦࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡦࡶࡰ࡭࡫ࡨࡨࠥࡴࡡࡵࡷࡵࡥࡱࡲࡹࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥፚ")
        try:
            if not self.bstack1111lll11_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠨࡎࡰࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡱࡣࡷ࡬ࠥࡺ࡯ࠡࡵࡨࡸࠧ፛"))
                return
            bstack1ll11l1l11l_opy_ = []
            for flag in self.bstack1ll11l1111l_opy_:
                if flag.startswith(bstack111l_opy_ (u"ࠧ࠮ࠩ፜")):
                    bstack1ll11l1l11l_opy_.append(flag)
                    continue
                bstack1ll11l11111_opy_ = False
                if bstack111l_opy_ (u"ࠨ࠼࠽ࠫ፝") in flag:
                    bstack1ll11ll1111_opy_ = flag.split(bstack111l_opy_ (u"ࠩ࠽࠾ࠬ፞"), 1)[0]
                    if os.path.exists(bstack1ll11ll1111_opy_):
                        bstack1ll11l11111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack111l_opy_ (u"ࠪ࠲ࡵࡿࠧ፟"))):
                        bstack1ll11l11111_opy_ = True
                if not bstack1ll11l11111_opy_:
                    bstack1ll11l1l11l_opy_.append(flag)
            bstack1ll11l1l11l_opy_.extend(self.bstack1111lll11_opy_)
            self.bstack1ll11l1111l_opy_ = bstack1ll11l1l11l_opy_
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡳࡦ࡮ࡨࡧࡹࡵࡲࡴ࠼ࠣࡿࢂࠨ፠").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1ll11ll11ll_opy_():
        return bstack1ll11l11ll1_opy_(bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ፡"))
    def bstack1ll111llll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11l1l1_opy_ = -1
        if self.bstack1lllll111ll_opy_ and bstack111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭።") in self.bstack1lllll11111_opy_:
            self.bstack11l11l1l1_opy_ = int(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ፣")])
        try:
            bstack1ll11l1l1ll_opy_ = [bstack111l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ፤"), bstack111l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ፥"), bstack111l_opy_ (u"ࠪ࠱ࡵ࠭፦")]
            if self.bstack11l11l1l1_opy_ >= 0:
                bstack1ll11l1l1ll_opy_.extend([bstack111l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ፧"), bstack111l_opy_ (u"ࠬ࠳࡮ࠨ፨")])
            for arg in bstack1ll11l1l1ll_opy_:
                self.bstack1ll111llll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11ll11l1_opy_(self):
        bstack1ll11l1111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11l1111l_opy_ = bstack1ll11l1111l_opy_
        return self.bstack1ll11l1111l_opy_
    def bstack1111111lll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1ll11ll11ll_opy_():
                self.logger.warning(bstack1ll11l1ll11_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack111l_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ፩"), bstack1lll11l11_opy_, str(e))
    def bstack1ll11l1l111_opy_(self, bstack1ll11ll1lll_opy_):
        global_config = Config.bstack1lll111ll_opy_()
        if bstack1ll11ll1lll_opy_:
            self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ፪"))
            self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠨࡖࡵࡹࡪ࠭፫"))
        if global_config.bstack1ll1l1l1l11_opy_():
            self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ፬"))
            self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠪࡘࡷࡻࡥࠨ፭"))
        self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠫ࠲ࡶࠧ፮"))
        self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ፯"))
        self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ፰"))
        self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ፱"))
        if self.bstack11l11l1l1_opy_ > 1:
            self.bstack1ll11l1111l_opy_.append(bstack111l_opy_ (u"ࠨ࠯ࡱࠫ፲"))
            self.bstack1ll11l1111l_opy_.append(str(self.bstack11l11l1l1_opy_))
    def bstack1ll11l111ll_opy_(self):
        if bstack111ll1ll_opy_.bstack1lllll1l1l_opy_(self.bstack1lllll11111_opy_):
             self.bstack1ll11l1111l_opy_ += [
                bstack1ll111lllll_opy_.get(bstack111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨ፳")), str(bstack111ll1ll_opy_.bstack111l1ll11l_opy_(self.bstack1lllll11111_opy_)),
                bstack1ll111lllll_opy_.get(bstack111l_opy_ (u"ࠪࡨࡪࡲࡡࡺࠩ፴")), str(bstack1ll111lllll_opy_.get(bstack111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰ࠰ࡨࡪࡲࡡࡺࠩ፵")))
            ]
    def bstack1ll11ll1ll1_opy_(self):
        bstack11111111ll_opy_ = []
        for spec in self.bstack1111lll11_opy_:
            bstack1l111ll111_opy_ = [spec]
            bstack1l111ll111_opy_ += self.bstack1ll11l1111l_opy_
            bstack11111111ll_opy_.append(bstack1l111ll111_opy_)
        self.bstack11111111ll_opy_ = bstack11111111ll_opy_
        return bstack11111111ll_opy_
    def bstack1ll11llll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11ll1l1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11ll1l1l_opy_ = False
        return self.bstack1ll11ll1l1l_opy_
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack1lll1ll1l_opy_(self):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࡰࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ፶")
        try:
            from browserstack_sdk.bstack1ll1l11111l_opy_ import bstack1ll1l1111l1_opy_
            bstack1ll11l111l1_opy_ = bstack1ll1l1111l1_opy_(bstack1ll1l111ll1_opy_=self.bstack1ll11l1111l_opy_)
            if not bstack1ll11l111l1_opy_.get(bstack111l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ፷"), False):
                self.logger.error(bstack111l_opy_ (u"ࠢࡕࡧࡶࡸࠥࡩ࡯ࡶࡰࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧ፸").format(bstack1ll11l111l1_opy_.get(bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ፹"), bstack111l_opy_ (u"ࠩࡘࡲࡰࡴ࡯ࡸࡰࠣࡩࡷࡸ࡯ࡳࠩ፺"))))
                return 0
            count = bstack1ll11l111l1_opy_.get(bstack111l_opy_ (u"ࠪࡧࡴࡻ࡮ࡵࠩ፻"), 0)
            self.logger.info(bstack111l_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠿ࠦࡻࡾࠤ፼").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ፽").format(e))
            return 0
    def bstack111111lll_opy_(self, bstack1ll11lll11l_opy_, bstack11111lllll_opy_):
        bstack11111lllll_opy_[bstack111l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭፾")] = self.bstack1lllll11111_opy_
        multiprocessing.set_start_method(bstack111l_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭፿"))
        bstack111l111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll11lll1l1_opy_ = manager.list()
        if bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎀ") in self.bstack1lllll11111_opy_:
            for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᎁ")]):
                bstack111l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1ll11lll11l_opy_,
                                                            args=(self.bstack1ll11l1111l_opy_, bstack11111lllll_opy_, bstack1ll11lll1l1_opy_)))
            bstack1ll11l11l1l_opy_ = len(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᎂ")])
        else:
            bstack111l111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1ll11lll11l_opy_,
                                                        args=(self.bstack1ll11l1111l_opy_, bstack11111lllll_opy_, bstack1ll11lll1l1_opy_)))
            bstack1ll11l11l1l_opy_ = 1
        i = 0
        for t in bstack111l111l_opy_:
            os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᎃ")] = str(i)
            if bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎄ") in self.bstack1lllll11111_opy_:
                os.environ[bstack111l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧᎅ")] = json.dumps(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᎆ")][i % bstack1ll11l11l1l_opy_])
            i += 1
            t.start()
        for t in bstack111l111l_opy_:
            t.join()
        return list(bstack1ll11lll1l1_opy_)
    @staticmethod
    def bstack11111ll11l_opy_(driver, bstack1ll11l1lll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᎇ"), None)
        if item and getattr(item, bstack111l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫᎈ"), None) and not getattr(item, bstack111l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬᎉ"), False):
            logger.info(
                bstack111l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥᎊ"))
            bstack1ll111lll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack111lll111l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1ll11l11lll_opy_(self):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡺ࡯ࠡࡤࡨࠤࡪࡾࡥࡤࡷࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᎋ")
        try:
            from browserstack_sdk.bstack1ll1l11111l_opy_ import bstack1ll1l1111l1_opy_
            bstack1ll11ll1l11_opy_ = bstack1ll1l1111l1_opy_(bstack1ll1l111ll1_opy_=self.bstack1ll11l1111l_opy_)
            if not bstack1ll11ll1l11_opy_.get(bstack111l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᎌ"), False):
                self.logger.error(bstack111l_opy_ (u"ࠢࡕࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᎍ").format(bstack1ll11ll1l11_opy_.get(bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᎎ"), bstack111l_opy_ (u"ࠩࡘࡲࡰࡴ࡯ࡸࡰࠣࡩࡷࡸ࡯ࡳࠩᎏ"))))
                return []
            test_files = bstack1ll11ll1l11_opy_.get(bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠧ᎐"), [])
            count = bstack1ll11ll1l11_opy_.get(bstack111l_opy_ (u"ࠫࡨࡵࡵ࡯ࡶࠪ᎑"), 0)
            self.logger.debug(bstack111l_opy_ (u"ࠧࡉ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠡࡽࢀࠤࡹ࡫ࡳࡵࡵࠣ࡭ࡳࠦࡻࡾࠢࡩ࡭ࡱ࡫ࡳࠣ᎒").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ᎓").format(e))
            return []