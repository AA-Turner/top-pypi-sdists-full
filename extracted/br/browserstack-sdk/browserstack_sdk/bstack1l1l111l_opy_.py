# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11l1111111_opy_
from browserstack_sdk.bstack1l11llll11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11llll_opy_, bstack1llll111lll_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack11l111lll1_opy_
from bstack_utils.constants import bstack1lll1lll111_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack1l1l111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1ll11ll_opy_ import bstack1llll1111ll_opy_
class bstack1l11l11111_opy_:
    def __init__(self, args, logger, bstack1llll1ll111_opy_, bstack1llll111ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1ll111_opy_ = bstack1llll1ll111_opy_
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11llllll11_opy_ = []
        self.bstack1lll1ll1lll_opy_ = []
        self.bstack1l1ll11ll1_opy_ = []
        self.bstack1llll11l111_opy_ = self.bstack1ll1lllll1_opy_()
        self.bstack1111ll1ll_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll1ll1ll1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l1lll111l_opy_(self, bstack1lll1llll11_opy_):
        self.parse_args()
        self.bstack1lll1lll1l1_opy_()
        self.bstack1llll11l1l1_opy_(bstack1lll1llll11_opy_)
        self.bstack1llll1l1ll1_opy_()
    @measure(event_name=EVENTS.bstack1lll1lll11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l11111l_opy_(self):
        bstack111l1l1l_opy_ = bstack1l1l111l1l_opy_.get_instance(self.bstack1llll1ll111_opy_, self.logger)
        if bstack111l1l1l_opy_ is None:
            self.logger.warn(bstack1111_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᅌ"))
            return
        bstack1llll11lll1_opy_ = False
        bstack111l1l1l_opy_.bstack1llll11l1ll_opy_(bstack1111_opy_ (u"ࠧ࡫࡮ࡢࡤ࡯ࡩࡩࠨᅍ"), bstack111l1l1l_opy_.bstack1lll111111_opy_())
        start_time = time.time()
        if bstack111l1l1l_opy_.bstack1lll111111_opy_():
            test_files = self.bstack1llll111l1l_opy_()
            bstack1llll11lll1_opy_ = True
            bstack1llll1l1l11_opy_ = bstack111l1l1l_opy_.bstack1lll1lll1ll_opy_(test_files)
            if bstack1llll1l1l11_opy_:
                self.bstack11llllll11_opy_ = [os.path.normpath(item) for item in bstack1llll1l1l11_opy_]
                self.__1lll1lllll1_opy_()
                bstack111l1l1l_opy_.bstack1llll1l1l1l_opy_(bstack1llll11lll1_opy_)
                self.logger.info(bstack1111_opy_ (u"ࠨࡔࡦࡵࡷࡷࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᅎ").format(self.bstack11llllll11_opy_))
            else:
                self.logger.info(bstack1111_opy_ (u"ࠢࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸࡧࡵࡩࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡤࡼࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᅏ"))
        bstack111l1l1l_opy_.bstack1llll11l1ll_opy_(bstack1111_opy_ (u"ࠣࡶ࡬ࡱࡪ࡚ࡡ࡬ࡧࡱࡘࡴࡇࡰࡱ࡮ࡼࠦᅐ"), int((time.time() - start_time) * 1000)) # bstack1llll11llll_opy_ to bstack1llll1111l1_opy_
    def __1lll1lllll1_opy_(self):
        bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡲ࡯ࡥࡨ࡫ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢ࡬ࡲࠥࡉࡌࡊࠢࡩࡰࡦ࡭ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡴࡶࡴࡱࡷࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡨ࡬ࡰࡪࠦ࡮ࡢ࡯ࡨࡷ࠱ࠦࡡ࡯ࡦࠣࡻࡪࠦࡳࡪ࡯ࡳࡰࡾࠦࡵࡱࡦࡤࡸࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡈࡒࡉࠡࡣࡵ࡫ࡸࠦࡴࡰࠢࡸࡷࡪࠦࡴࡩࡱࡶࡩࠥ࡬ࡩ࡭ࡧࡶ࠲࡛ࠥࡳࡦࡴࠪࡷࠥ࡬ࡩ࡭ࡶࡨࡶ࡮ࡴࡧࠡࡨ࡯ࡥ࡬ࡹࠠࠩ࠯ࡰ࠰ࠥ࠳࡫ࠪࠢࡵࡩࡲࡧࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺࡡࡤࡶࠣࡥࡳࡪࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡣࡳࡴࡱ࡯ࡥࡥࠢࡱࡥࡹࡻࡲࡢ࡮࡯ࡽࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᅑ")
        try:
            if not self.bstack11llllll11_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡒࡴࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡵࡧࡴࡩࠢࡷࡳࠥࡹࡥࡵࠤᅒ"))
                return
            bstack1llll11ll11_opy_ = []
            for flag in self.bstack1lll1ll1lll_opy_:
                if flag.startswith(bstack1111_opy_ (u"ࠫ࠲࠭ᅓ")):
                    bstack1llll11ll11_opy_.append(flag)
                    continue
                bstack1llll1l1lll_opy_ = False
                if bstack1111_opy_ (u"ࠬࡀ࠺ࠨᅔ") in flag:
                    bstack1lll1llllll_opy_ = flag.split(bstack1111_opy_ (u"࠭࠺࠻ࠩᅕ"), 1)[0]
                    if os.path.exists(bstack1lll1llllll_opy_):
                        bstack1llll1l1lll_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1111_opy_ (u"ࠧ࠯ࡲࡼࠫᅖ"))):
                        bstack1llll1l1lll_opy_ = True
                if not bstack1llll1l1lll_opy_:
                    bstack1llll11ll11_opy_.append(flag)
            bstack1llll11ll11_opy_.extend(self.bstack11llllll11_opy_)
            self.bstack1lll1ll1lll_opy_ = bstack1llll11ll11_opy_
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡷࡪࡲࡥࡤࡶࡲࡶࡸࡀࠠࡼࡿࠥᅗ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll1ll1l1l_opy_():
        return bstack1llll1111ll_opy_(bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᅘ"))
    def bstack1llll11111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1111ll1ll_opy_ = -1
        if self.bstack1llll111ll1_opy_ and bstack1111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᅙ") in self.bstack1llll1ll111_opy_:
            self.bstack1111ll1ll_opy_ = int(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᅚ")])
        try:
            bstack1llll1l11l1_opy_ = [bstack1111_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧᅛ"), bstack1111_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩᅜ"), bstack1111_opy_ (u"ࠧ࠮ࡲࠪᅝ")]
            if self.bstack1111ll1ll_opy_ >= 0:
                bstack1llll1l11l1_opy_.extend([bstack1111_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩᅞ"), bstack1111_opy_ (u"ࠩ࠰ࡲࠬᅟ")])
            for arg in bstack1llll1l11l1_opy_:
                self.bstack1llll11111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll1lll1l1_opy_(self):
        bstack1lll1ll1lll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll1ll1lll_opy_ = bstack1lll1ll1lll_opy_
        return self.bstack1lll1ll1lll_opy_
    def bstack1ll11l1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll1ll1l1l_opy_():
                self.logger.warning(bstack1llll111lll_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1111_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥᅠ"), bstack1l11llll_opy_, str(e))
    def bstack1llll11l1l1_opy_(self, bstack1lll1llll11_opy_):
        global_config = Config.get_instance()
        if bstack1lll1llll11_opy_:
            self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᅡ"))
            self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"࡚ࠬࡲࡶࡧࠪᅢ"))
        if global_config.should_skip_session_status():
            self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᅣ"))
            self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠧࡕࡴࡸࡩࠬᅤ"))
        self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠨ࠯ࡳࠫᅥ"))
        self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧᅦ"))
        self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬᅧ"))
        self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᅨ"))
        if self.bstack1111ll1ll_opy_ > 1:
            self.bstack1lll1ll1lll_opy_.append(bstack1111_opy_ (u"ࠬ࠳࡮ࠨᅩ"))
            self.bstack1lll1ll1lll_opy_.append(str(self.bstack1111ll1ll_opy_))
    def bstack1llll1l1ll1_opy_(self):
        if bstack11l111lll1_opy_.bstack11111l11_opy_(self.bstack1llll1ll111_opy_):
             self.bstack1lll1ll1lll_opy_ += [
                bstack1lll1lll111_opy_.get(bstack1111_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬᅪ")), str(bstack11l111lll1_opy_.bstack1ll11111ll_opy_(self.bstack1llll1ll111_opy_)),
                bstack1lll1lll111_opy_.get(bstack1111_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ᅫ")), str(bstack1lll1lll111_opy_.get(bstack1111_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭ᅬ")))
            ]
    def bstack1llll1l111l_opy_(self):
        bstack1l1ll11ll1_opy_ = []
        for spec in self.bstack11llllll11_opy_:
            bstack111ll1ll11_opy_ = [spec]
            bstack111ll1ll11_opy_ += self.bstack1lll1ll1lll_opy_
            bstack1l1ll11ll1_opy_.append(bstack111ll1ll11_opy_)
        self.bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_
        return bstack1l1ll11ll1_opy_
    def bstack1ll1lllll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llll11l111_opy_ = True
            return True
        except Exception as e:
            self.bstack1llll11l111_opy_ = False
        return self.bstack1llll11l111_opy_
    @measure(event_name=EVENTS.bstack1llll111l11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l1ll1l11_opy_(self):
        bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡇࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫࡭ࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᅭ")
        try:
            from browserstack_sdk.bstack1lllll11l11_opy_ import bstack1llll1ll1l1_opy_
            bstack1lll1ll1l11_opy_ = bstack1llll1ll1l1_opy_(bstack1llll1ll1ll_opy_=self.bstack1lll1ll1lll_opy_)
            if not bstack1lll1ll1l11_opy_.get(bstack1111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᅮ"), False):
                self.logger.error(bstack1111_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡦࡳࡺࡴࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᅯ").format(bstack1lll1ll1l11_opy_.get(bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᅰ"), bstack1111_opy_ (u"࠭ࡕ࡯࡭ࡱࡳࡼࡴࠠࡦࡴࡵࡳࡷ࠭ᅱ"))))
                return 0
            count = bstack1lll1ll1l11_opy_.get(bstack1111_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᅲ"), 0)
            self.logger.info(bstack1111_opy_ (u"ࠣࡖࡲࡸࡦࡲࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠼ࠣࡿࢂࠨᅳ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨᅴ").format(e))
            return 0
    def bstack11lll1l1ll_opy_(self, bstack1llll111111_opy_, bstack1l1lll111l_opy_):
        bstack1l1lll111l_opy_[bstack1111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪᅵ")] = self.bstack1llll1ll111_opy_
        multiprocessing.set_start_method(bstack1111_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪᅶ"))
        bstack11ll111lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll11ll1l_opy_ = manager.list()
        if bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᅷ") in self.bstack1llll1ll111_opy_:
            for index, platform in enumerate(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅸ")]):
                bstack11ll111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll111111_opy_,
                                                            args=(self.bstack1lll1ll1lll_opy_, bstack1l1lll111l_opy_, bstack1llll11ll1l_opy_)))
            bstack1lll1llll1l_opy_ = len(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅹ")])
        else:
            bstack11ll111lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll111111_opy_,
                                                        args=(self.bstack1lll1ll1lll_opy_, bstack1l1lll111l_opy_, bstack1llll11ll1l_opy_)))
            bstack1lll1llll1l_opy_ = 1
        i = 0
        for t in bstack11ll111lll_opy_:
            os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᅺ")] = str(i)
            if bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅻ") in self.bstack1llll1ll111_opy_:
                os.environ[bstack1111_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫᅼ")] = json.dumps(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅽ")][i % bstack1lll1llll1l_opy_])
            i += 1
            t.start()
        for t in bstack11ll111lll_opy_:
            t.join()
        return list(bstack1llll11ll1l_opy_)
    @staticmethod
    def bstack111lllll1_opy_(driver, bstack1llll1l1111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᅾ"), None)
        if item and getattr(item, bstack1111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨᅿ"), None) and not getattr(item, bstack1111_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩᆀ"), False):
            logger.info(
                bstack1111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢᆁ"))
            bstack1llll1l11ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l1111111_opy_.bstack1ll1ll1l11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llll111l1l_opy_(self):
        bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᆂ")
        try:
            from browserstack_sdk.bstack1lllll11l11_opy_ import bstack1llll1ll1l1_opy_
            bstack1llll11l11l_opy_ = bstack1llll1ll1l1_opy_(bstack1llll1ll1ll_opy_=self.bstack1lll1ll1lll_opy_)
            if not bstack1llll11l11l_opy_.get(bstack1111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᆃ"), False):
                self.logger.error(bstack1111_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᆄ").format(bstack1llll11l11l_opy_.get(bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᆅ"), bstack1111_opy_ (u"࠭ࡕ࡯࡭ࡱࡳࡼࡴࠠࡦࡴࡵࡳࡷ࠭ᆆ"))))
                return []
            test_files = bstack1llll11l11l_opy_.get(bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠫᆇ"), [])
            count = bstack1llll11l11l_opy_.get(bstack1111_opy_ (u"ࠨࡥࡲࡹࡳࡺࠧᆈ"), 0)
            self.logger.debug(bstack1111_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶࡨࡨࠥࢁࡽࠡࡶࡨࡷࡹࡹࠠࡪࡰࠣࡿࢂࠦࡦࡪ࡮ࡨࡷࠧᆉ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᆊ").format(e))
            return []