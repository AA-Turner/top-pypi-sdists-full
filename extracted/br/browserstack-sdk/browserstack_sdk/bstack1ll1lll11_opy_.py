# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l111ll111_opy_
from browserstack_sdk.bstack11l1lll1ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11ll1ll_opy_, bstack1lll1llll1l_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from bstack_utils.constants import bstack1llll1lll1l_opy_
from bstack_utils.bstack1llll1l1ll_opy_ import bstack1lllll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll11ll1l_opy_ import bstack1llll1ll1ll_opy_
class bstack11111111_opy_:
    def __init__(self, args, logger, bstack1llll1lll11_opy_, bstack1llll1111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
        self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111ll11111_opy_ = []
        self.bstack1llll111111_opy_ = []
        self.bstack1l111l1l11_opy_ = []
        self.bstack1llll1l111l_opy_ = self.bstack1l11lll11l_opy_()
        self.bstack1ll1ll1111_opy_ = -1
    @measure(event_name=EVENTS.bstack1llll11111l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1lllll1l11_opy_(self, bstack1llll1ll111_opy_):
        self.parse_args()
        self.bstack1llll11ll11_opy_()
        self.bstack1llll111lll_opy_(bstack1llll1ll111_opy_)
        self.bstack1llll111l1l_opy_()
    @measure(event_name=EVENTS.bstack1llll1l11ll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1ll111ll1l_opy_(self):
        bstack1llll1l1ll_opy_ = bstack1lllll1l1l_opy_.get_instance(self.bstack1llll1lll11_opy_, self.logger)
        if bstack1llll1l1ll_opy_ is None:
            self.logger.warn(bstack11l1l11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡨࡢࡰࡧࡰࡪࡸࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᅇ"))
            return
        bstack1llll1l1lll_opy_ = False
        bstack1llll1l1ll_opy_.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠢࡦࡰࡤࡦࡱ࡫ࡤࠣᅈ"), bstack1llll1l1ll_opy_.bstack1l1ll111ll_opy_())
        start_time = time.time()
        if bstack1llll1l1ll_opy_.bstack1l1ll111ll_opy_():
            test_files = self.bstack1lll1lllll1_opy_()
            bstack1llll1l1lll_opy_ = True
            bstack1lll1lll1ll_opy_ = bstack1llll1l1ll_opy_.bstack1llll1l11l1_opy_(test_files)
            if bstack1lll1lll1ll_opy_:
                self.bstack111ll11111_opy_ = [os.path.normpath(item) for item in bstack1lll1lll1ll_opy_]
                self.__1lll1lll1l1_opy_()
                bstack1llll1l1ll_opy_.bstack1llll11l111_opy_(bstack1llll1l1lll_opy_)
                self.logger.info(bstack11l1l11_opy_ (u"ࠣࡖࡨࡷࡹࡹࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡹࡸ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᅉ").format(self.bstack111ll11111_opy_))
            else:
                self.logger.info(bstack11l1l11_opy_ (u"ࠤࡑࡳࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺࡩࡷ࡫ࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡦࡾࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᅊ"))
        bstack1llll1l1ll_opy_.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠥࡸ࡮ࡳࡥࡕࡣ࡮ࡩࡳ࡚࡯ࡂࡲࡳࡰࡾࠨᅋ"), int((time.time() - start_time) * 1000)) # bstack1lll1llll11_opy_ to bstack1llll11l11l_opy_
    def __1lll1lll1l1_opy_(self):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡴࡱࡧࡣࡦࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࡶࠤ࡮ࡴࠠࡄࡎࡌࠤ࡫ࡲࡡࡨࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸࡪࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡦࡴࡹࡩࡷࠦࡲࡦࡶࡸࡶࡳࡹࠠࡳࡧࡲࡶࡩ࡫ࡲࡦࡦࠣࡪ࡮ࡲࡥࠡࡰࡤࡱࡪࡹࠬࠡࡣࡱࡨࠥࡽࡥࠡࡵ࡬ࡱࡵࡲࡹࠡࡷࡳࡨࡦࡺࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬ࡪࠦࡃࡍࡋࠣࡥࡷ࡭ࡳࠡࡶࡲࠤࡺࡹࡥࠡࡶ࡫ࡳࡸ࡫ࠠࡧ࡫࡯ࡩࡸ࠴ࠠࡖࡵࡨࡶࠬࡹࠠࡧ࡫࡯ࡸࡪࡸࡩ࡯ࡩࠣࡪࡱࡧࡧࡴࠢࠫ࠱ࡲ࠲ࠠ࠮࡭ࠬࠤࡷ࡫࡭ࡢ࡫ࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵࡣࡦࡸࠥࡧ࡮ࡥࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡥࡵࡶ࡬ࡪࡧࡧࠤࡳࡧࡴࡶࡴࡤࡰࡱࡿࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᅌ")
        try:
            if not self.bstack111ll11111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡰࡢࡶ࡫ࠤࡹࡵࠠࡴࡧࡷࠦᅍ"))
                return
            bstack1llll1ll1l1_opy_ = []
            for flag in self.bstack1llll111111_opy_:
                if flag.startswith(bstack11l1l11_opy_ (u"࠭࠭ࠨᅎ")):
                    bstack1llll1ll1l1_opy_.append(flag)
                    continue
                bstack1llll11l1l1_opy_ = False
                if bstack11l1l11_opy_ (u"ࠧ࠻࠼ࠪᅏ") in flag:
                    bstack1llll1l1111_opy_ = flag.split(bstack11l1l11_opy_ (u"ࠨ࠼࠽ࠫᅐ"), 1)[0]
                    if os.path.exists(bstack1llll1l1111_opy_):
                        bstack1llll11l1l1_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡾ࠭ᅑ"))):
                        bstack1llll11l1l1_opy_ = True
                if not bstack1llll11l1l1_opy_:
                    bstack1llll1ll1l1_opy_.append(flag)
            bstack1llll1ll1l1_opy_.extend(self.bstack111ll11111_opy_)
            self.bstack1llll111111_opy_ = bstack1llll1ll1l1_opy_
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥࡹࡥ࡭ࡧࡦࡸࡴࡸࡳ࠻ࠢࡾࢁࠧᅒ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llll11llll_opy_():
        return bstack1llll1ll1ll_opy_(bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᅓ"))
    def bstack1llll1111ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1ll1111_opy_ = -1
        if self.bstack1llll1111l1_opy_ and bstack11l1l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᅔ") in self.bstack1llll1lll11_opy_:
            self.bstack1ll1ll1111_opy_ = int(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᅕ")])
        try:
            bstack1llll111ll1_opy_ = [bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩᅖ"), bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫᅗ"), bstack11l1l11_opy_ (u"ࠩ࠰ࡴࠬᅘ")]
            if self.bstack1ll1ll1111_opy_ >= 0:
                bstack1llll111ll1_opy_.extend([bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫᅙ"), bstack11l1l11_opy_ (u"ࠫ࠲ࡴࠧᅚ")])
            for arg in bstack1llll111ll1_opy_:
                self.bstack1llll1111ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll11ll11_opy_(self):
        bstack1llll111111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1llll111111_opy_ = bstack1llll111111_opy_
        return self.bstack1llll111111_opy_
    def bstack111l111l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llll11llll_opy_():
                self.logger.warning(bstack1lll1llll1l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧᅛ"), bstack11l11ll1ll_opy_, str(e))
    def bstack1llll111lll_opy_(self, bstack1llll1ll111_opy_):
        global_config = Config.get_instance()
        if bstack1llll1ll111_opy_:
            self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᅜ"))
            self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠧࡕࡴࡸࡩࠬᅝ"))
        if global_config.should_skip_session_status():
            self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᅞ"))
            self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠩࡗࡶࡺ࡫ࠧᅟ"))
        self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠪ࠱ࡵ࠭ᅠ"))
        self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩᅡ"))
        self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧᅢ"))
        self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᅣ"))
        if self.bstack1ll1ll1111_opy_ > 1:
            self.bstack1llll111111_opy_.append(bstack11l1l11_opy_ (u"ࠧ࠮ࡰࠪᅤ"))
            self.bstack1llll111111_opy_.append(str(self.bstack1ll1ll1111_opy_))
    def bstack1llll111l1l_opy_(self):
        if bstack1l1l11l11l_opy_.bstack111lll1l11_opy_(self.bstack1llll1lll11_opy_):
             self.bstack1llll111111_opy_ += [
                bstack1llll1lll1l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࠧᅥ")), str(bstack1l1l11l11l_opy_.bstack111lll1ll1_opy_(self.bstack1llll1lll11_opy_)),
                bstack1llll1lll1l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡧࡩࡱࡧࡹࠨᅦ")), str(bstack1llll1lll1l_opy_.get(bstack11l1l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨᅧ")))
            ]
    def bstack1llll1llll1_opy_(self):
        bstack1l111l1l11_opy_ = []
        for spec in self.bstack111ll11111_opy_:
            bstack11l1l1111l_opy_ = [spec]
            bstack11l1l1111l_opy_ += self.bstack1llll111111_opy_
            bstack1l111l1l11_opy_.append(bstack11l1l1111l_opy_)
        self.bstack1l111l1l11_opy_ = bstack1l111l1l11_opy_
        return bstack1l111l1l11_opy_
    def bstack1l11lll11l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llll1l111l_opy_ = True
            return True
        except Exception as e:
            self.bstack1llll1l111l_opy_ = False
        return self.bstack1llll1l111l_opy_
    @measure(event_name=EVENTS.bstack1lll1llllll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1ll111lll_opy_(self):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡉࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦ࡯ࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᅨ")
        try:
            from browserstack_sdk.bstack1lllll1l111_opy_ import bstack1lllll11111_opy_
            bstack1llll1l1l11_opy_ = bstack1lllll11111_opy_(bstack1lllll11ll1_opy_=self.bstack1llll111111_opy_)
            if not bstack1llll1l1l11_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᅩ"), False):
                self.logger.error(bstack11l1l11_opy_ (u"ࠨࡔࡦࡵࡷࠤࡨࡵࡵ࡯ࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᅪ").format(bstack1llll1l1l11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᅫ"), bstack11l1l11_opy_ (u"ࠨࡗࡱ࡯ࡳࡵࡷ࡯ࠢࡨࡶࡷࡵࡲࠨᅬ"))))
                return 0
            count = bstack1llll1l1l11_opy_.get(bstack11l1l11_opy_ (u"ࠩࡦࡳࡺࡴࡴࠨᅭ"), 0)
            self.logger.info(bstack11l1l11_opy_ (u"ࠥࡘࡴࡺࡡ࡭ࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠾ࠥࢁࡽࠣᅮ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣᅯ").format(e))
            return 0
    def bstack1lllll111_opy_(self, bstack1llll11l1ll_opy_, bstack1lllll1l11_opy_):
        bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬᅰ")] = self.bstack1llll1lll11_opy_
        multiprocessing.set_start_method(bstack11l1l11_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬᅱ"))
        bstack11ll11111_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll11lll1_opy_ = manager.list()
        if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅲ") in self.bstack1llll1lll11_opy_:
            for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᅳ")]):
                bstack11ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll11l1ll_opy_,
                                                            args=(self.bstack1llll111111_opy_, bstack1lllll1l11_opy_, bstack1llll11lll1_opy_)))
            bstack1llll111l11_opy_ = len(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅴ")])
        else:
            bstack11ll11111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll11l1ll_opy_,
                                                        args=(self.bstack1llll111111_opy_, bstack1lllll1l11_opy_, bstack1llll11lll1_opy_)))
            bstack1llll111l11_opy_ = 1
        i = 0
        for t in bstack11ll11111_opy_:
            os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᅵ")] = str(i)
            if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅶ") in self.bstack1llll1lll11_opy_:
                os.environ[bstack11l1l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ᅷ")] = json.dumps(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅸ")][i % bstack1llll111l11_opy_])
            i += 1
            t.start()
        for t in bstack11ll11111_opy_:
            t.join()
        return list(bstack1llll11lll1_opy_)
    @staticmethod
    def bstack1ll1l1l1_opy_(driver, bstack1llll1lllll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᅹ"), None)
        if item and getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪᅺ"), None) and not getattr(item, bstack11l1l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫᅻ"), False):
            logger.info(
                bstack11l1l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤᅼ"))
            bstack1llll1l1ll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l111ll111_opy_.bstack1l111ll1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll1lllll1_opy_(self):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡹࡵࠠࡣࡧࠣࡩࡽ࡫ࡣࡶࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᅽ")
        try:
            from browserstack_sdk.bstack1lllll1l111_opy_ import bstack1lllll11111_opy_
            bstack1llll1ll11l_opy_ = bstack1lllll11111_opy_(bstack1lllll11ll1_opy_=self.bstack1llll111111_opy_)
            if not bstack1llll1ll11l_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᅾ"), False):
                self.logger.error(bstack11l1l11_opy_ (u"ࠨࡔࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥᅿ").format(bstack1llll1ll11l_opy_.get(bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᆀ"), bstack11l1l11_opy_ (u"ࠨࡗࡱ࡯ࡳࡵࡷ࡯ࠢࡨࡶࡷࡵࡲࠨᆁ"))))
                return []
            test_files = bstack1llll1ll11l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸ࠭ᆂ"), [])
            count = bstack1llll1ll11l_opy_.get(bstack11l1l11_opy_ (u"ࠪࡧࡴࡻ࡮ࡵࠩᆃ"), 0)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡈࡵ࡬࡭ࡧࡦࡸࡪࡪࠠࡼࡿࠣࡸࡪࡹࡴࡴࠢ࡬ࡲࠥࢁࡽࠡࡨ࡬ࡰࡪࡹࠢᆄ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᆅ").format(e))
            return []