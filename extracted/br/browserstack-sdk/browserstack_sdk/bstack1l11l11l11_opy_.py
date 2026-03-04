# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11l1111111_opy_
from browserstack_sdk.bstack1ll1l11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll11llll1_opy_, bstack1llll11llll_opy_
from bstack_utils.bstack1lll1ll111_opy_ import bstack11l1llll1_opy_
from bstack_utils.constants import bstack1llll111l11_opy_
from bstack_utils.bstack11l1lll11l_opy_ import bstack111lll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1ll1lll_opy_ import bstack1lll1lll1ll_opy_
class bstack11lllll1l_opy_:
    def __init__(self, args, logger, bstack1llll1l1l1l_opy_, bstack1llll1ll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
        self.bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll11l1l_opy_ = []
        self.bstack1llll11ll1l_opy_ = []
        self.bstack111l11l1l1_opy_ = []
        self.bstack1llll11111l_opy_ = self.bstack111l1l1l1l_opy_()
        self.bstack1111l1l11_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll1lllll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack11ll1l1lll_opy_(self, bstack1lll1llll1l_opy_):
        self.parse_args()
        self.bstack1llll111lll_opy_()
        self.bstack1llll111l1l_opy_(bstack1lll1llll1l_opy_)
        self.bstack1llll11l1l1_opy_()
    @measure(event_name=EVENTS.bstack1lll1ll1ll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1lll11l1ll_opy_(self):
        bstack11l1lll11l_opy_ = bstack111lll1ll_opy_.get_instance(self.bstack1llll1l1l1l_opy_, self.logger)
        if bstack11l1lll11l_opy_ is None:
            self.logger.warn(bstack1lll1l_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨᅋ"))
            return
        bstack1llll11l111_opy_ = False
        bstack11l1lll11l_opy_.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧᅌ"), bstack11l1lll11l_opy_.bstack1l1l1l1l11_opy_())
        start_time = time.time()
        if bstack11l1lll11l_opy_.bstack1l1l1l1l11_opy_():
            test_files = self.bstack1llll1l111l_opy_()
            bstack1llll11l111_opy_ = True
            bstack1llll1l1lll_opy_ = bstack11l1lll11l_opy_.bstack1llll1l1111_opy_(test_files)
            if bstack1llll1l1lll_opy_:
                self.bstack1lll11l1l_opy_ = [os.path.normpath(item) for item in bstack1llll1l1lll_opy_]
                self.__1lll1ll1l1l_opy_()
                bstack11l1lll11l_opy_.bstack1lll1llllll_opy_(bstack1llll11l111_opy_)
                self.logger.info(bstack1lll1l_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᅍ").format(self.bstack1lll11l1l_opy_))
            else:
                self.logger.info(bstack1lll1l_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᅎ"))
        bstack11l1lll11l_opy_.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥᅏ"), int((time.time() - start_time) * 1000)) # bstack1llll1l11ll_opy_ to bstack1lll1lll111_opy_
    def __1lll1ll1l1l_opy_(self):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡱ࡮ࡤࡧࡪࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡ࡫ࡱࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡺࡵࡳࡰࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡧ࡫࡯ࡩࠥࡴࡡ࡮ࡧࡶ࠰ࠥࡧ࡮ࡥࠢࡺࡩࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡻࡰࡥࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡇࡑࡏࠠࡢࡴࡪࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡺࡨࡰࡵࡨࠤ࡫࡯࡬ࡦࡵ࠱ࠤ࡚ࡹࡥࡳࠩࡶࠤ࡫࡯࡬ࡵࡧࡵ࡭ࡳ࡭ࠠࡧ࡮ࡤ࡫ࡸࠦࠨ࠮࡯࠯ࠤ࠲ࡱࠩࠡࡴࡨࡱࡦ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡧࡣࡵࠢࡤࡲࡩࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡢࡲࡳࡰ࡮࡫ࡤࠡࡰࡤࡸࡺࡸࡡ࡭࡮ࡼࠤࡩࡻࡲࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᅐ")
        try:
            if not self.bstack1lll11l1l_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡑࡳࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡴࡦࡺࡨࠡࡶࡲࠤࡸ࡫ࡴࠣᅑ"))
                return
            bstack1llll11lll1_opy_ = []
            for flag in self.bstack1llll11ll1l_opy_:
                if flag.startswith(bstack1lll1l_opy_ (u"ࠪ࠱ࠬᅒ")):
                    bstack1llll11lll1_opy_.append(flag)
                    continue
                bstack1llll1ll111_opy_ = False
                if bstack1lll1l_opy_ (u"ࠫ࠿ࡀࠧᅓ") in flag:
                    bstack1llll1ll1l1_opy_ = flag.split(bstack1lll1l_opy_ (u"ࠬࡀ࠺ࠨᅔ"), 1)[0]
                    if os.path.exists(bstack1llll1ll1l1_opy_):
                        bstack1llll1ll111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1lll1l_opy_ (u"࠭࠮ࡱࡻࠪᅕ"))):
                        bstack1llll1ll111_opy_ = True
                if not bstack1llll1ll111_opy_:
                    bstack1llll11lll1_opy_.append(flag)
            bstack1llll11lll1_opy_.extend(self.bstack1lll11l1l_opy_)
            self.bstack1llll11ll1l_opy_ = bstack1llll11lll1_opy_
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡶࡩࡱ࡫ࡣࡵࡱࡵࡷ࠿ࠦࡻࡾࠤᅖ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llll11l1ll_opy_():
        return bstack1lll1lll1ll_opy_(bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᅗ"))
    def bstack1llll1l1l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1111l1l11_opy_ = -1
        if self.bstack1llll1ll11l_opy_ and bstack1lll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᅘ") in self.bstack1llll1l1l1l_opy_:
            self.bstack1111l1l11_opy_ = int(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᅙ")])
        try:
            bstack1llll1l1ll1_opy_ = [bstack1lll1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ᅚ"), bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨᅛ"), bstack1lll1l_opy_ (u"࠭࠭ࡱࠩᅜ")]
            if self.bstack1111l1l11_opy_ >= 0:
                bstack1llll1l1ll1_opy_.extend([bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨᅝ"), bstack1lll1l_opy_ (u"ࠨ࠯ࡱࠫᅞ")])
            for arg in bstack1llll1l1ll1_opy_:
                self.bstack1llll1l1l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll111lll_opy_(self):
        bstack1llll11ll1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
        return self.bstack1llll11ll1l_opy_
    def bstack11l111llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llll11l1ll_opy_():
                self.logger.warning(bstack1llll11llll_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤᅟ"), bstack1ll11llll1_opy_, str(e))
    def bstack1llll111l1l_opy_(self, bstack1lll1llll1l_opy_):
        global_config = Config.get_instance()
        if bstack1lll1llll1l_opy_:
            self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᅠ"))
            self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"࡙ࠫࡸࡵࡦࠩᅡ"))
        if global_config.should_skip_session_status():
            self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᅢ"))
            self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"࠭ࡔࡳࡷࡨࠫᅣ"))
        self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠧ࠮ࡲࠪᅤ"))
        self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ᅥ"))
        self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫᅦ"))
        self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᅧ"))
        if self.bstack1111l1l11_opy_ > 1:
            self.bstack1llll11ll1l_opy_.append(bstack1lll1l_opy_ (u"ࠫ࠲ࡴࠧᅨ"))
            self.bstack1llll11ll1l_opy_.append(str(self.bstack1111l1l11_opy_))
    def bstack1llll11l1l1_opy_(self):
        if bstack11l1llll1_opy_.bstack1l1l1l11l_opy_(self.bstack1llll1l1l1l_opy_):
             self.bstack1llll11ll1l_opy_ += [
                bstack1llll111l11_opy_.get(bstack1lll1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫᅩ")), str(bstack11l1llll1_opy_.bstack11lll1ll1_opy_(self.bstack1llll1l1l1l_opy_)),
                bstack1llll111l11_opy_.get(bstack1lll1l_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬᅪ")), str(bstack1llll111l11_opy_.get(bstack1lll1l_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬᅫ")))
            ]
    def bstack1lll1llll11_opy_(self):
        bstack111l11l1l1_opy_ = []
        for spec in self.bstack1lll11l1l_opy_:
            bstack1lll1l11ll_opy_ = [spec]
            bstack1lll1l11ll_opy_ += self.bstack1llll11ll1l_opy_
            bstack111l11l1l1_opy_.append(bstack1lll1l11ll_opy_)
        self.bstack111l11l1l1_opy_ = bstack111l11l1l1_opy_
        return bstack111l11l1l1_opy_
    def bstack111l1l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llll11111l_opy_ = True
            return True
        except Exception as e:
            self.bstack1llll11111l_opy_ = False
        return self.bstack1llll11111l_opy_
    @measure(event_name=EVENTS.bstack1llll111111_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l1l111111_opy_(self):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࡳࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᅬ")
        try:
            from browserstack_sdk.bstack1llll1lll1l_opy_ import bstack1lllll11l11_opy_
            bstack1lll1lll11l_opy_ = bstack1lllll11l11_opy_(bstack1lllll1111l_opy_=self.bstack1llll11ll1l_opy_)
            if not bstack1lll1lll11l_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᅭ"), False):
                self.logger.error(bstack1lll1l_opy_ (u"ࠥࡘࡪࡹࡴࠡࡥࡲࡹࡳࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᅮ").format(bstack1lll1lll11l_opy_.get(bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᅯ"), bstack1lll1l_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᅰ"))))
                return 0
            count = bstack1lll1lll11l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᅱ"), 0)
            self.logger.info(bstack1lll1l_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧᅲ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᅳ").format(e))
            return 0
    def bstack111ll11lll_opy_(self, bstack1llll11l11l_opy_, bstack11ll1l1lll_opy_):
        bstack11ll1l1lll_opy_[bstack1lll1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩᅴ")] = self.bstack1llll1l1l1l_opy_
        multiprocessing.set_start_method(bstack1lll1l_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩᅵ"))
        bstack111ll1111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll11ll11_opy_ = manager.list()
        if bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅶ") in self.bstack1llll1l1l1l_opy_:
            for index, platform in enumerate(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᅷ")]):
                bstack111ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll11l11l_opy_,
                                                            args=(self.bstack1llll11ll1l_opy_, bstack11ll1l1lll_opy_, bstack1llll11ll11_opy_)))
            bstack1llll1111ll_opy_ = len(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅸ")])
        else:
            bstack111ll1111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll11l11l_opy_,
                                                        args=(self.bstack1llll11ll1l_opy_, bstack11ll1l1lll_opy_, bstack1llll11ll11_opy_)))
            bstack1llll1111ll_opy_ = 1
        i = 0
        for t in bstack111ll1111l_opy_:
            os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᅹ")] = str(i)
            if bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᅺ") in self.bstack1llll1l1l1l_opy_:
                os.environ[bstack1lll1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪᅻ")] = json.dumps(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᅼ")][i % bstack1llll1111ll_opy_])
            i += 1
            t.start()
        for t in bstack111ll1111l_opy_:
            t.join()
        return list(bstack1llll11ll11_opy_)
    @staticmethod
    def bstack111ll11ll_opy_(driver, bstack1lll1lll1l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᅽ"), None)
        if item and getattr(item, bstack1lll1l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧᅾ"), None) and not getattr(item, bstack1lll1l_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨᅿ"), False):
            logger.info(
                bstack1lll1l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨᆀ"))
            bstack1llll1l11l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l1111111_opy_.bstack11111ll11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llll1l111l_opy_(self):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᆁ")
        try:
            from browserstack_sdk.bstack1llll1lll1l_opy_ import bstack1lllll11l11_opy_
            bstack1llll1111l1_opy_ = bstack1lllll11l11_opy_(bstack1lllll1111l_opy_=self.bstack1llll11ll1l_opy_)
            if not bstack1llll1111l1_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᆂ"), False):
                self.logger.error(bstack1lll1l_opy_ (u"ࠥࡘࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢᆃ").format(bstack1llll1111l1_opy_.get(bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᆄ"), bstack1lll1l_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᆅ"))))
                return []
            test_files = bstack1llll1111l1_opy_.get(bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠪᆆ"), [])
            count = bstack1llll1111l1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᆇ"), 0)
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡾࢁࠥ࡬ࡩ࡭ࡧࡶࠦᆈ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᆉ").format(e))
            return []