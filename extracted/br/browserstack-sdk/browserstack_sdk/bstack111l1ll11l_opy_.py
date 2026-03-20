# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1l1l1l11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l11l_opy_, bstack1lll1111111_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack11lllllll_opy_
from bstack_utils.constants import bstack1lll1111l1l_opy_
from bstack_utils.bstack111ll11lll_opy_ import bstack1l1l1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll11l1ll1_opy_ import bstack1lll11111l1_opy_
class bstack1llll11ll_opy_:
    def __init__(self, args, logger, bstack1lll11l111l_opy_, bstack1lll111l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll11l111l_opy_ = bstack1lll11l111l_opy_
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111lll1ll_opy_ = []
        self.bstack1lll11ll1l1_opy_ = []
        self.bstack1ll111lll_opy_ = []
        self.bstack1lll111lll1_opy_ = self.bstack11ll111111_opy_()
        self.bstack1l111l111_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll11l11l1_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1llll1l11_opy_(self, bstack1lll111111l_opy_):
        self.parse_args()
        self.bstack1lll1l111ll_opy_()
        self.bstack1lll11l11ll_opy_(bstack1lll111111l_opy_)
        self.bstack1lll1l111l1_opy_()
    @measure(event_name=EVENTS.bstack1lll1l11l11_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11l11l11_opy_(self):
        bstack111ll11lll_opy_ = bstack1l1l1ll1ll_opy_.get_instance(self.bstack1lll11l111l_opy_, self.logger)
        if bstack111ll11lll_opy_ is None:
            self.logger.warn(bstack11lll1_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧሕ"))
            return
        bstack1lll11l1l1l_opy_ = False
        bstack111ll11lll_opy_.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦሖ"), bstack111ll11lll_opy_.bstack1l1lllll_opy_())
        start_time = time.time()
        if bstack111ll11lll_opy_.bstack1l1lllll_opy_():
            test_files = self.bstack1lll11lllll_opy_()
            bstack1lll11l1l1l_opy_ = True
            bstack1lll11ll11l_opy_ = bstack111ll11lll_opy_.bstack1lll1l1111l_opy_(test_files)
            if bstack1lll11ll11l_opy_:
                self.bstack111lll1ll_opy_ = [os.path.normpath(item) for item in bstack1lll11ll11l_opy_]
                self.__1lll11lll1l_opy_()
                bstack111ll11lll_opy_.bstack1lll111ll1l_opy_(bstack1lll11l1l1l_opy_)
                self.logger.info(bstack11lll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤሗ").format(self.bstack111lll1ll_opy_))
            else:
                self.logger.info(bstack11lll1_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥመ"))
        bstack111ll11lll_opy_.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤሙ"), int((time.time() - start_time) * 1000)) # bstack1lll111llll_opy_ to bstack1lll11l1lll_opy_
    def __1lll11lll1l_opy_(self):
        bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧሚ")
        try:
            if not self.bstack111lll1ll_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢማ"))
                return
            bstack1lll1111l11_opy_ = []
            for flag in self.bstack1lll11ll1l1_opy_:
                if flag.startswith(bstack11lll1_opy_ (u"ࠩ࠰ࠫሜ")):
                    bstack1lll1111l11_opy_.append(flag)
                    continue
                bstack1lll11l1111_opy_ = False
                if bstack11lll1_opy_ (u"ࠪ࠾࠿࠭ም") in flag:
                    bstack1lll1111ll1_opy_ = flag.split(bstack11lll1_opy_ (u"ࠫ࠿ࡀࠧሞ"), 1)[0]
                    if os.path.exists(bstack1lll1111ll1_opy_):
                        bstack1lll11l1111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11lll1_opy_ (u"ࠬ࠴ࡰࡺࠩሟ"))):
                        bstack1lll11l1111_opy_ = True
                if not bstack1lll11l1111_opy_:
                    bstack1lll1111l11_opy_.append(flag)
            bstack1lll1111l11_opy_.extend(self.bstack111lll1ll_opy_)
            self.bstack1lll11ll1l1_opy_ = bstack1lll1111l11_opy_
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣሠ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll11ll111_opy_():
        return bstack1lll11111l1_opy_(bstack11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩሡ"))
    def bstack1lll11lll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l111l111_opy_ = -1
        if self.bstack1lll111l111_opy_ and bstack11lll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨሢ") in self.bstack1lll11l111l_opy_:
            self.bstack1l111l111_opy_ = int(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩሣ")])
        try:
            bstack1lll11l1l11_opy_ = [bstack11lll1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬሤ"), bstack11lll1_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧሥ"), bstack11lll1_opy_ (u"ࠬ࠳ࡰࠨሦ")]
            if self.bstack1l111l111_opy_ >= 0:
                bstack1lll11l1l11_opy_.extend([bstack11lll1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧሧ"), bstack11lll1_opy_ (u"ࠧ࠮ࡰࠪረ")])
            for arg in bstack1lll11l1l11_opy_:
                self.bstack1lll11lll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll1l111ll_opy_(self):
        bstack1lll11ll1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
        return self.bstack1lll11ll1l1_opy_
    def bstack11lll1ll11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll11ll111_opy_():
                self.logger.warning(bstack1lll1111111_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11lll1_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣሩ"), bstack1111l11l_opy_, str(e))
    def bstack1lll11l11ll_opy_(self, bstack1lll111111l_opy_):
        global_config = Config.get_instance()
        if bstack1lll111111l_opy_:
            self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ሪ"))
            self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠪࡘࡷࡻࡥࠨራ"))
        if global_config.should_skip_session_status():
            self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪሬ"))
            self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"࡚ࠬࡲࡶࡧࠪር"))
        self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"࠭࠭ࡱࠩሮ"))
        self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬሯ"))
        self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪሰ"))
        self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩሱ"))
        if self.bstack1l111l111_opy_ > 1:
            self.bstack1lll11ll1l1_opy_.append(bstack11lll1_opy_ (u"ࠪ࠱ࡳ࠭ሲ"))
            self.bstack1lll11ll1l1_opy_.append(str(self.bstack1l111l111_opy_))
    def bstack1lll1l111l1_opy_(self):
        if bstack11lllllll_opy_.bstack1l11ll111l_opy_(self.bstack1lll11l111l_opy_):
             self.bstack1lll11ll1l1_opy_ += [
                bstack1lll1111l1l_opy_.get(bstack11lll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪሳ")), str(bstack11lllllll_opy_.bstack1l1l1l11_opy_(self.bstack1lll11l111l_opy_)),
                bstack1lll1111l1l_opy_.get(bstack11lll1_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫሴ")), str(bstack1lll1111l1l_opy_.get(bstack11lll1_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫስ")))
            ]
    def bstack1lll111l11l_opy_(self):
        bstack1ll111lll_opy_ = []
        for spec in self.bstack111lll1ll_opy_:
            bstack1111l1ll1_opy_ = [spec]
            bstack1111l1ll1_opy_ += self.bstack1lll11ll1l1_opy_
            bstack1ll111lll_opy_.append(bstack1111l1ll1_opy_)
        self.bstack1ll111lll_opy_ = bstack1ll111lll_opy_
        return bstack1ll111lll_opy_
    def bstack11ll111111_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll111lll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll111lll1_opy_ = False
        return self.bstack1lll111lll1_opy_
    @measure(event_name=EVENTS.bstack1lll1111lll_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11lll11ll1_opy_(self):
        bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣሶ")
        try:
            from browserstack_sdk.bstack1lll1l1l1ll_opy_ import bstack1lll1l1l1l1_opy_
            bstack1lll11ll1ll_opy_ = bstack1lll1l1l1l1_opy_(bstack1lll1l1ll11_opy_=self.bstack1lll11ll1l1_opy_)
            if not bstack1lll11ll1ll_opy_.get(bstack11lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩሷ"), False):
                self.logger.error(bstack11lll1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢሸ").format(bstack1lll11ll1ll_opy_.get(bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩሹ"), bstack11lll1_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫሺ"))))
                return 0
            count = bstack1lll11ll1ll_opy_.get(bstack11lll1_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫሻ"), 0)
            self.logger.info(bstack11lll1_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦሼ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦሽ").format(e))
            return 0
    def bstack1l1ll111l_opy_(self, bstack1lll11111ll_opy_, bstack1llll1l11_opy_):
        bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨሾ")] = self.bstack1lll11l111l_opy_
        multiprocessing.set_start_method(bstack11lll1_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨሿ"))
        bstack1ll1l111ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll111ll11_opy_ = manager.list()
        if bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቀ") in self.bstack1lll11l111l_opy_:
            for index, platform in enumerate(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቁ")]):
                bstack1ll1l111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll11111ll_opy_,
                                                            args=(self.bstack1lll11ll1l1_opy_, bstack1llll1l11_opy_, bstack1lll111ll11_opy_)))
            bstack1lll1l11111_opy_ = len(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨቂ")])
        else:
            bstack1ll1l111ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll11111ll_opy_,
                                                        args=(self.bstack1lll11ll1l1_opy_, bstack1llll1l11_opy_, bstack1lll111ll11_opy_)))
            bstack1lll1l11111_opy_ = 1
        i = 0
        for t in bstack1ll1l111ll_opy_:
            os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ቃ")] = str(i)
            if bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪቄ") in self.bstack1lll11l111l_opy_:
                os.environ[bstack11lll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩቅ")] = json.dumps(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቆ")][i % bstack1lll1l11111_opy_])
            i += 1
            t.start()
        for t in bstack1ll1l111ll_opy_:
            t.join()
        return list(bstack1lll111ll11_opy_)
    @staticmethod
    def bstack1ll11ll11_opy_(driver, bstack1lll111l1ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧቇ"), None)
        if item and getattr(item, bstack11lll1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭ቈ"), None) and not getattr(item, bstack11lll1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ቉"), False):
            logger.info(
                bstack11lll1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧቊ"))
            bstack1ll1lllllll_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack111lll1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll11lllll_opy_(self):
        bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨቋ")
        try:
            from browserstack_sdk.bstack1lll1l1l1ll_opy_ import bstack1lll1l1l1l1_opy_
            bstack1lll111l1l1_opy_ = bstack1lll1l1l1l1_opy_(bstack1lll1l1ll11_opy_=self.bstack1lll11ll1l1_opy_)
            if not bstack1lll111l1l1_opy_.get(bstack11lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩቌ"), False):
                self.logger.error(bstack11lll1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨቍ").format(bstack1lll111l1l1_opy_.get(bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ቎"), bstack11lll1_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫ቏"))))
                return []
            test_files = bstack1lll111l1l1_opy_.get(bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠩቐ"), [])
            count = bstack1lll111l1l1_opy_.get(bstack11lll1_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬቑ"), 0)
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡿࢂࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡽࢀࠤ࡫࡯࡬ࡦࡵࠥቒ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤቓ").format(e))
            return []