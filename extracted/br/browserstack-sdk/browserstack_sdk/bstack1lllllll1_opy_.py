# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1l11ll1l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l111l1_opy_, bstack1ll11l11l1l_opy_
from bstack_utils.bstack111llll111_opy_ import bstack1ll11l1l_opy_
from bstack_utils.constants import bstack1ll111ll11l_opy_
from bstack_utils.bstack1l11l11ll_opy_ import bstack111lll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11ll1l11_opy_ import bstack1ll11l111l1_opy_
class bstack11l11111l_opy_:
    def __init__(self, args, logger, bstack1llll1ll1l1_opy_, bstack1llll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll1l111_opy_ = []
        self.bstack1ll11l1l11l_opy_ = []
        self.bstack1lllllll111_opy_ = []
        self.bstack1ll11l11ll1_opy_ = self.bstack1l11l1l11l_opy_()
        self.bstack1lll11l11l_opy_ = -1
    @measure(event_name=EVENTS.bstack1ll111ll1l1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l1111ll1_opy_(self, bstack1ll11l1111l_opy_):
        self.parse_args()
        self.bstack1ll11l1l111_opy_()
        self.bstack1ll11l1l1l1_opy_(bstack1ll11l1111l_opy_)
        self.bstack1ll111llll1_opy_()
    @measure(event_name=EVENTS.bstack1ll11ll1111_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1l1l1l111l_opy_(self):
        bstack1l11l11ll_opy_ = bstack111lll1l1l_opy_.bstack1l1l11ll1_opy_(self.bstack1llll1ll1l1_opy_, self.logger)
        if bstack1l11l11ll_opy_ is None:
            self.logger.warn(bstack111ll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ፺"))
            return
        bstack1llll1l1lll_opy_ = False
        bstack1l11l11ll_opy_.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦ፻"), bstack1l11l11ll_opy_.bstack11lll11l1_opy_())
        start_time = time.time()
        if bstack1l11l11ll_opy_.bstack11lll11l1_opy_():
            test_files = self.bstack1ll111ll1ll_opy_()
            bstack1llll1l1lll_opy_ = True
            bstack1llll1l1ll1_opy_ = bstack1l11l11ll_opy_.bstack1llll1llll1_opy_(test_files)
            if bstack1llll1l1ll1_opy_:
                self.bstack1lll1l111_opy_ = [os.path.normpath(item) for item in bstack1llll1l1ll1_opy_]
                self.__1ll111lllll_opy_()
                bstack1l11l11ll_opy_.bstack1llll1ll1ll_opy_(bstack1llll1l1lll_opy_)
                self.logger.info(bstack111ll_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ፼").format(self.bstack1lll1l111_opy_))
            else:
                self.logger.info(bstack111ll_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥ፽"))
        bstack1l11l11ll_opy_.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤ፾"), int((time.time() - start_time) * 1000)) # bstack1ll111l1ll1_opy_ to bstack1ll11l1lll1_opy_
    def __1ll111lllll_opy_(self):
        bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ፿")
        try:
            if not self.bstack1lll1l111_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢᎀ"))
                return
            bstack1ll11l1ll1l_opy_ = []
            for flag in self.bstack1ll11l1l11l_opy_:
                if flag.startswith(bstack111ll_opy_ (u"ࠩ࠰ࠫᎁ")):
                    bstack1ll11l1ll1l_opy_.append(flag)
                    continue
                bstack1ll111lll1l_opy_ = False
                if bstack111ll_opy_ (u"ࠪ࠾࠿࠭ᎂ") in flag:
                    bstack1ll111ll111_opy_ = flag.split(bstack111ll_opy_ (u"ࠫ࠿ࡀࠧᎃ"), 1)[0]
                    if os.path.exists(bstack1ll111ll111_opy_):
                        bstack1ll111lll1l_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack111ll_opy_ (u"ࠬ࠴ࡰࡺࠩᎄ"))):
                        bstack1ll111lll1l_opy_ = True
                if not bstack1ll111lll1l_opy_:
                    bstack1ll11l1ll1l_opy_.append(flag)
            bstack1ll11l1ll1l_opy_.extend(self.bstack1lll1l111_opy_)
            self.bstack1ll11l1l11l_opy_ = bstack1ll11l1ll1l_opy_
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣᎅ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1ll111lll11_opy_():
        return bstack1ll11l111l1_opy_(bstack111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᎆ"))
    def bstack1ll11l111ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll11l11l_opy_ = -1
        if self.bstack1llll1lll11_opy_ and bstack111ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᎇ") in self.bstack1llll1ll1l1_opy_:
            self.bstack1lll11l11l_opy_ = int(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᎈ")])
        try:
            bstack1ll11l11111_opy_ = [bstack111ll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬᎉ"), bstack111ll_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧᎊ"), bstack111ll_opy_ (u"ࠬ࠳ࡰࠨᎋ")]
            if self.bstack1lll11l11l_opy_ >= 0:
                bstack1ll11l11111_opy_.extend([bstack111ll_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧᎌ"), bstack111ll_opy_ (u"ࠧ࠮ࡰࠪᎍ")])
            for arg in bstack1ll11l11111_opy_:
                self.bstack1ll11l111ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11l1l111_opy_(self):
        bstack1ll11l1l11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11l1l11l_opy_ = bstack1ll11l1l11l_opy_
        return self.bstack1ll11l1l11l_opy_
    def bstack1ll111l111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1ll111lll11_opy_():
                self.logger.warning(bstack1ll11l11l1l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack111ll_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣᎎ"), bstack1111l111l1_opy_, str(e))
    def bstack1ll11l1l1l1_opy_(self, bstack1ll11l1111l_opy_):
        global_config = Config.bstack1l1l11ll1_opy_()
        if bstack1ll11l1111l_opy_:
            self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᎏ"))
            self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠪࡘࡷࡻࡥࠨ᎐"))
        if global_config.bstack1ll1ll1lll1_opy_():
            self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ᎑"))
            self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"࡚ࠬࡲࡶࡧࠪ᎒"))
        self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"࠭࠭ࡱࠩ᎓"))
        self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬ᎔"))
        self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ᎕"))
        self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᎖"))
        if self.bstack1lll11l11l_opy_ > 1:
            self.bstack1ll11l1l11l_opy_.append(bstack111ll_opy_ (u"ࠪ࠱ࡳ࠭᎗"))
            self.bstack1ll11l1l11l_opy_.append(str(self.bstack1lll11l11l_opy_))
    def bstack1ll111llll1_opy_(self):
        if bstack1ll11l1l_opy_.bstack1111l11ll1_opy_(self.bstack1llll1ll1l1_opy_):
             self.bstack1ll11l1l11l_opy_ += [
                bstack1ll111ll11l_opy_.get(bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪ᎘")), str(bstack1ll11l1l_opy_.bstack111l1l11l_opy_(self.bstack1llll1ll1l1_opy_)),
                bstack1ll111ll11l_opy_.get(bstack111ll_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫ᎙")), str(bstack1ll111ll11l_opy_.get(bstack111ll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫ᎚")))
            ]
    def bstack1ll11ll11l1_opy_(self):
        bstack1lllllll111_opy_ = []
        for spec in self.bstack1lll1l111_opy_:
            bstack1111ll1ll_opy_ = [spec]
            bstack1111ll1ll_opy_ += self.bstack1ll11l1l11l_opy_
            bstack1lllllll111_opy_.append(bstack1111ll1ll_opy_)
        self.bstack1lllllll111_opy_ = bstack1lllllll111_opy_
        return bstack1lllllll111_opy_
    def bstack1l11l1l11l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11l11ll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11l11ll1_opy_ = False
        return self.bstack1ll11l11ll1_opy_
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1lllllllll1_opy_(self):
        bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᎛")
        try:
            from browserstack_sdk.bstack1ll11lll1l1_opy_ import bstack1ll11ll1ll1_opy_
            bstack1ll11l1llll_opy_ = bstack1ll11ll1ll1_opy_(bstack1ll11llll11_opy_=self.bstack1ll11l1l11l_opy_)
            if not bstack1ll11l1llll_opy_.get(bstack111ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᎜"), False):
                self.logger.error(bstack111ll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢ᎝").format(bstack1ll11l1llll_opy_.get(bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᎞"), bstack111ll_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫ᎟"))))
                return 0
            count = bstack1ll11l1llll_opy_.get(bstack111ll_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫᎠ"), 0)
            self.logger.info(bstack111ll_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦᎡ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦᎢ").format(e))
            return 0
    def bstack11ll1111l1_opy_(self, bstack1ll111l1lll_opy_, bstack11l1111ll1_opy_):
        bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨᎣ")] = self.bstack1llll1ll1l1_opy_
        multiprocessing.set_start_method(bstack111ll_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᎤ"))
        bstack111111l11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll11l1l1ll_opy_ = manager.list()
        if bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꭵ") in self.bstack1llll1ll1l1_opy_:
            for index, platform in enumerate(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᎦ")]):
                bstack111111l11l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1ll111l1lll_opy_,
                                                            args=(self.bstack1ll11l1l11l_opy_, bstack11l1111ll1_opy_, bstack1ll11l1l1ll_opy_)))
            bstack1ll11l1ll11_opy_ = len(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎧ")])
        else:
            bstack111111l11l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1ll111l1lll_opy_,
                                                        args=(self.bstack1ll11l1l11l_opy_, bstack11l1111ll1_opy_, bstack1ll11l1l1ll_opy_)))
            bstack1ll11l1ll11_opy_ = 1
        i = 0
        for t in bstack111111l11l_opy_:
            os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꭸ")] = str(i)
            if bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᎩ") in self.bstack1llll1ll1l1_opy_:
                os.environ[bstack111ll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩᎪ")] = json.dumps(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᎫ")][i % bstack1ll11l1ll11_opy_])
            i += 1
            t.start()
        for t in bstack111111l11l_opy_:
            t.join()
        return list(bstack1ll11l1l1ll_opy_)
    @staticmethod
    def bstack111l11l1_opy_(driver, bstack1ll11ll11ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᎬ"), None)
        if item and getattr(item, bstack111ll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭Ꭽ"), None) and not getattr(item, bstack111ll_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧᎮ"), False):
            logger.info(
                bstack111ll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧᎯ"))
            bstack1ll11ll111l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack11l1ll11l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1ll111ll1ll_opy_(self):
        bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᎰ")
        try:
            from browserstack_sdk.bstack1ll11lll1l1_opy_ import bstack1ll11ll1ll1_opy_
            bstack1ll11l11lll_opy_ = bstack1ll11ll1ll1_opy_(bstack1ll11llll11_opy_=self.bstack1ll11l1l11l_opy_)
            if not bstack1ll11l11lll_opy_.get(bstack111ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᎱ"), False):
                self.logger.error(bstack111ll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨᎲ").format(bstack1ll11l11lll_opy_.get(bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᎳ"), bstack111ll_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫᎴ"))))
                return []
            test_files = bstack1ll11l11lll_opy_.get(bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠩᎵ"), [])
            count = bstack1ll11l11lll_opy_.get(bstack111ll_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᎶ"), 0)
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡿࢂࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡽࢀࠤ࡫࡯࡬ࡦࡵࠥᎷ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᎸ").format(e))
            return []