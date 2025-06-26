# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1lll1l1_opy_ import bstack111l1lll11l_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1ll1lll1_opy_
from bstack_utils.helper import bstack11l1l111ll_opy_
class bstack1ll111ll1_opy_:
    _1llll11l1l1_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1ll111l_opy_ = bstack111l1lll11l_opy_(self.config, logger)
        self.bstack1l111l1ll_opy_ = bstack1ll1lll1_opy_.bstack1lllll111l_opy_(config=self.config)
        self.bstack111l1l1ll1l_opy_ = {}
        self.bstack1111l1llll_opy_ = False
        self.bstack111l1ll1l1l_opy_ = (
            self.__111l1ll1ll1_opy_()
            and self.bstack1l111l1ll_opy_ is not None
            and self.bstack1l111l1ll_opy_.bstack1ll1lll11_opy_()
            and config.get(bstack11ll1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᶢ"), None) is not None
            and config.get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᶣ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lllll111l_opy_(cls, config, logger):
        if cls._1llll11l1l1_opy_ is None and config is not None:
            cls._1llll11l1l1_opy_ = bstack1ll111ll1_opy_(config, logger)
        return cls._1llll11l1l1_opy_
    def bstack1ll1lll11_opy_(self):
        bstack11ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉࡵࠠ࡯ࡱࡷࠤࡦࡶࡰ࡭ࡻࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡻ࡭࡫࡮࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐ࠳࠴ࡽࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᶤ")
        return self.bstack111l1ll1l1l_opy_ and self.bstack111l1l1llll_opy_()
    def bstack111l1l1llll_opy_(self):
        return self.config.get(bstack11ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᶥ"), None) in bstack11ll1111l1l_opy_
    def __111l1ll1ll1_opy_(self):
        bstack11ll111l1ll_opy_ = False
        for fw in bstack11l1lll1l11_opy_:
            if fw in self.config.get(bstack11ll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᶦ"), bstack11ll1l1_opy_ (u"ࠪࠫᶧ")):
                bstack11ll111l1ll_opy_ = True
        return bstack11l1l111ll_opy_(self.config.get(bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᶨ"), bstack11ll111l1ll_opy_))
    def bstack111l1ll11l1_opy_(self):
        return (not self.bstack1ll1lll11_opy_() and
                self.bstack1l111l1ll_opy_ is not None and self.bstack1l111l1ll_opy_.bstack1ll1lll11_opy_())
    def bstack111l1ll1lll_opy_(self):
        if not self.bstack111l1ll11l1_opy_():
            return
        if self.config.get(bstack11ll1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᶩ"), None) is None or self.config.get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᶪ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤᶫ"))
        if not self.__111l1ll1ll1_opy_():
            self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤᶬ"))
    def bstack111l1ll1111_opy_(self):
        return self.bstack1111l1llll_opy_
    def bstack11111llll1_opy_(self, bstack111l1ll11ll_opy_):
        self.bstack1111l1llll_opy_ = bstack111l1ll11ll_opy_
        self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥᶭ"), bstack111l1ll11ll_opy_)
    def bstack1111ll1111_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧᶮ"))
                return None
            orchestration_strategy = None
            if self.bstack1l111l1ll_opy_ is not None:
                orchestration_strategy = self.bstack1l111l1ll_opy_.bstack1ll1lllll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢᶯ"))
                return None
            self.logger.info(bstack11ll1l1_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥᶰ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᶱ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᶲ"))
                self.bstack111l1ll111l_opy_.bstack111l1l1lll1_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack111l1ll111l_opy_.bstack111l1ll1l11_opy_()
            if not ordered_test_files:
                return None
            self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥᶳ"), len(test_files))
            self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧᶴ"), int(os.environ.get(bstack11ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨᶵ")) or bstack11ll1l1_opy_ (u"ࠦ࠵ࠨᶶ")))
            self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤᶷ"), int(os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᶸ")) or bstack11ll1l1_opy_ (u"ࠢ࠲ࠤᶹ")))
            self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧᶺ"), len(ordered_test_files))
            self.bstack1111l11l1l_opy_(bstack11ll1l1_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦᶻ"), self.bstack111l1ll111l_opy_.bstack111l1lll111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥᶼ").format(e))
        return None
    def bstack1111l11l1l_opy_(self, key, value):
        self.bstack111l1l1ll1l_opy_[key] = value
    def bstack1lll11ll1_opy_(self):
        return self.bstack111l1l1ll1l_opy_