# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1ll1111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11llllll1l_opy_, bstack1lll11111l1_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll1lll1l_opy_
from bstack_utils.constants import bstack1lll111l111_opy_
from bstack_utils.bstack1l1111ll1l_opy_ import bstack11ll11l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1111111_opy_ import bstack1lll11l1111_opy_
class bstack111l1lll1l_opy_:
    def __init__(self, args, logger, bstack1lll11ll1l1_opy_, bstack1lll1111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
        self.bstack1lll1111l11_opy_ = bstack1lll1111l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l11lll1_opy_ = []
        self.bstack1lll111lll1_opy_ = []
        self.bstack1111l111l1_opy_ = []
        self.bstack1lll111ll1l_opy_ = self.bstack111lll1lll_opy_()
        self.bstack111ll1111_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l11ll1ll_opy_(self, bstack1lll11l11ll_opy_):
        self.parse_args()
        self.bstack1lll1111l1l_opy_()
        self.bstack1lll111111l_opy_(bstack1lll11l11ll_opy_)
        self.bstack1lll111ll11_opy_()
    @measure(event_name=EVENTS.bstack1lll1l111ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1ll1l1l111_opy_(self):
        bstack1l1111ll1l_opy_ = bstack11ll11l111_opy_.get_instance(self.bstack1lll11ll1l1_opy_, self.logger)
        if bstack1l1111ll1l_opy_ is None:
            self.logger.warn(bstack1l1_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧሕ"))
            return
        bstack1lll1l11l11_opy_ = False
        bstack1l1111ll1l_opy_.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦሖ"), bstack1l1111ll1l_opy_.bstack1l1111ll11_opy_())
        start_time = time.time()
        if bstack1l1111ll1l_opy_.bstack1l1111ll11_opy_():
            test_files = self.bstack1lll11ll1ll_opy_()
            bstack1lll1l11l11_opy_ = True
            bstack1lll11llll1_opy_ = bstack1l1111ll1l_opy_.bstack1lll11lll1l_opy_(test_files)
            if bstack1lll11llll1_opy_:
                self.bstack111l11lll1_opy_ = [os.path.normpath(item) for item in bstack1lll11llll1_opy_]
                self.__1lll111l1l1_opy_()
                bstack1l1111ll1l_opy_.bstack1lll11l1ll1_opy_(bstack1lll1l11l11_opy_)
                self.logger.info(bstack1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤሗ").format(self.bstack111l11lll1_opy_))
            else:
                self.logger.info(bstack1l1_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥመ"))
        bstack1l1111ll1l_opy_.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤሙ"), int((time.time() - start_time) * 1000)) # bstack1lll11lll11_opy_ to bstack1lll11l1l11_opy_
    def __1lll111l1l1_opy_(self):
        bstack1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧሚ")
        try:
            if not self.bstack111l11lll1_opy_:
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢማ"))
                return
            bstack1lll1111ll1_opy_ = []
            for flag in self.bstack1lll111lll1_opy_:
                if flag.startswith(bstack1l1_opy_ (u"ࠩ࠰ࠫሜ")):
                    bstack1lll1111ll1_opy_.append(flag)
                    continue
                bstack1lll11111ll_opy_ = False
                if bstack1l1_opy_ (u"ࠪ࠾࠿࠭ም") in flag:
                    bstack1lll1111lll_opy_ = flag.split(bstack1l1_opy_ (u"ࠫ࠿ࡀࠧሞ"), 1)[0]
                    if os.path.exists(bstack1lll1111lll_opy_):
                        bstack1lll11111ll_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l1_opy_ (u"ࠬ࠴ࡰࡺࠩሟ"))):
                        bstack1lll11111ll_opy_ = True
                if not bstack1lll11111ll_opy_:
                    bstack1lll1111ll1_opy_.append(flag)
            bstack1lll1111ll1_opy_.extend(self.bstack111l11lll1_opy_)
            self.bstack1lll111lll1_opy_ = bstack1lll1111ll1_opy_
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣሠ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll11l1lll_opy_():
        return bstack1lll11l1111_opy_(bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩሡ"))
    def bstack1lll111llll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111ll1111_opy_ = -1
        if self.bstack1lll1111l11_opy_ and bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨሢ") in self.bstack1lll11ll1l1_opy_:
            self.bstack111ll1111_opy_ = int(self.bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩሣ")])
        try:
            bstack1lll11ll111_opy_ = [bstack1l1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬሤ"), bstack1l1_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧሥ"), bstack1l1_opy_ (u"ࠬ࠳ࡰࠨሦ")]
            if self.bstack111ll1111_opy_ >= 0:
                bstack1lll11ll111_opy_.extend([bstack1l1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧሧ"), bstack1l1_opy_ (u"ࠧ࠮ࡰࠪረ")])
            for arg in bstack1lll11ll111_opy_:
                self.bstack1lll111llll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll1111l1l_opy_(self):
        bstack1lll111lll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
        return self.bstack1lll111lll1_opy_
    def bstack111l111lll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll11l1lll_opy_():
                self.logger.warning(bstack1lll11111l1_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l1_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣሩ"), bstack11llllll1l_opy_, str(e))
    def bstack1lll111111l_opy_(self, bstack1lll11l11ll_opy_):
        global_config = Config.get_instance()
        if bstack1lll11l11ll_opy_:
            self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ሪ"))
            self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠪࡘࡷࡻࡥࠨራ"))
        if global_config.should_skip_session_status():
            self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪሬ"))
            self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"࡚ࠬࡲࡶࡧࠪር"))
        self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"࠭࠭ࡱࠩሮ"))
        self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬሯ"))
        self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪሰ"))
        self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩሱ"))
        if self.bstack111ll1111_opy_ > 1:
            self.bstack1lll111lll1_opy_.append(bstack1l1_opy_ (u"ࠪ࠱ࡳ࠭ሲ"))
            self.bstack1lll111lll1_opy_.append(str(self.bstack111ll1111_opy_))
    def bstack1lll111ll11_opy_(self):
        if bstack1ll1lll1l_opy_.bstack1l1llllll1_opy_(self.bstack1lll11ll1l1_opy_):
             self.bstack1lll111lll1_opy_ += [
                bstack1lll111l111_opy_.get(bstack1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪሳ")), str(bstack1ll1lll1l_opy_.bstack1llll11l1_opy_(self.bstack1lll11ll1l1_opy_)),
                bstack1lll111l111_opy_.get(bstack1l1_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫሴ")), str(bstack1lll111l111_opy_.get(bstack1l1_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫስ")))
            ]
    def bstack1lll111l1ll_opy_(self):
        bstack1111l111l1_opy_ = []
        for spec in self.bstack111l11lll1_opy_:
            bstack1l1ll1l111_opy_ = [spec]
            bstack1l1ll1l111_opy_ += self.bstack1lll111lll1_opy_
            bstack1111l111l1_opy_.append(bstack1l1ll1l111_opy_)
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        return bstack1111l111l1_opy_
    def bstack111lll1lll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll111ll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll111ll1l_opy_ = False
        return self.bstack1lll111ll1l_opy_
    @measure(event_name=EVENTS.bstack1lll1l1111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11l1lllll_opy_(self):
        bstack1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣሶ")
        try:
            from browserstack_sdk.bstack1lll1l1lll1_opy_ import bstack1lll1l11lll_opy_
            bstack1lll11l11l1_opy_ = bstack1lll1l11lll_opy_(bstack1lll1l1l11l_opy_=self.bstack1lll111lll1_opy_)
            if not bstack1lll11l11l1_opy_.get(bstack1l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩሷ"), False):
                self.logger.error(bstack1l1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢሸ").format(bstack1lll11l11l1_opy_.get(bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩሹ"), bstack1l1_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫሺ"))))
                return 0
            count = bstack1lll11l11l1_opy_.get(bstack1l1_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫሻ"), 0)
            self.logger.info(bstack1l1_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦሼ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦሽ").format(e))
            return 0
    def bstack111l1l1lll_opy_(self, bstack1lll111l11l_opy_, bstack1l11ll1ll_opy_):
        bstack1l11ll1ll_opy_[bstack1l1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨሾ")] = self.bstack1lll11ll1l1_opy_
        multiprocessing.set_start_method(bstack1l1_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨሿ"))
        bstack11lll11l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll11l1l1l_opy_ = manager.list()
        if bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቀ") in self.bstack1lll11ll1l1_opy_:
            for index, platform in enumerate(self.bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቁ")]):
                bstack11lll11l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll111l11l_opy_,
                                                            args=(self.bstack1lll111lll1_opy_, bstack1l11ll1ll_opy_, bstack1lll11l1l1l_opy_)))
            bstack1lll1l11111_opy_ = len(self.bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨቂ")])
        else:
            bstack11lll11l1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll111l11l_opy_,
                                                        args=(self.bstack1lll111lll1_opy_, bstack1l11ll1ll_opy_, bstack1lll11l1l1l_opy_)))
            bstack1lll1l11111_opy_ = 1
        i = 0
        for t in bstack11lll11l1l_opy_:
            os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ቃ")] = str(i)
            if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪቄ") in self.bstack1lll11ll1l1_opy_:
                os.environ[bstack1l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩቅ")] = json.dumps(self.bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቆ")][i % bstack1lll1l11111_opy_])
            i += 1
            t.start()
        for t in bstack11lll11l1l_opy_:
            t.join()
        return list(bstack1lll11l1l1l_opy_)
    @staticmethod
    def bstack1l1ll1111l_opy_(driver, bstack1lll11lllll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧቇ"), None)
        if item and getattr(item, bstack1l1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭ቈ"), None) and not getattr(item, bstack1l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ቉"), False):
            logger.info(
                bstack1l1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧቊ"))
            bstack1lll11ll11l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack11l1lll1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll11ll1ll_opy_(self):
        bstack1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨቋ")
        try:
            from browserstack_sdk.bstack1lll1l1lll1_opy_ import bstack1lll1l11lll_opy_
            bstack1lll11l111l_opy_ = bstack1lll1l11lll_opy_(bstack1lll1l1l11l_opy_=self.bstack1lll111lll1_opy_)
            if not bstack1lll11l111l_opy_.get(bstack1l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩቌ"), False):
                self.logger.error(bstack1l1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨቍ").format(bstack1lll11l111l_opy_.get(bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ቎"), bstack1l1_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫ቏"))))
                return []
            test_files = bstack1lll11l111l_opy_.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠩቐ"), [])
            count = bstack1lll11l111l_opy_.get(bstack1l1_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬቑ"), 0)
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡿࢂࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡽࢀࠤ࡫࡯࡬ࡦࡵࠥቒ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤቓ").format(e))
            return []