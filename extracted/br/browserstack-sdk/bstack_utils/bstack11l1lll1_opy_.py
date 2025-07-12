# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack11lll111lll_opy_ import bstack11ll1lll1l1_opy_
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lllll111_opy_
from bstack_utils.helper import bstack11l1l1ll_opy_
class bstack1l1l11111l_opy_:
    _1l111l111ll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack11lll111l11_opy_ = bstack11ll1lll1l1_opy_(self.config, logger)
        self.bstack1lll1ll11l_opy_ = bstack1lllll111_opy_.bstack11l1l11l11_opy_(config=self.config)
        self.bstack11lll11l111_opy_ = {}
        self.bstack1111l11111_opy_ = False
        self.bstack11lll111l1l_opy_ = (
            self.__11lll1111l1_opy_()
            and self.bstack1lll1ll11l_opy_ is not None
            and self.bstack1lll1ll11l_opy_.bstack1ll1ll1l_opy_()
            and config.get(bstack11l1111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᘉ"), None) is not None
            and config.get(bstack11l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᘊ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack11l1l11l11_opy_(cls, config, logger):
        if cls._1l111l111ll_opy_ is None and config is not None:
            cls._1l111l111ll_opy_ = bstack1l1l11111l_opy_(config, logger)
        return cls._1l111l111ll_opy_
    def bstack1ll1ll1l_opy_(self):
        bstack11l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊ࡯ࠡࡰࡲࡸࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡼ࡮ࡥ࡯࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑ࠴࠵ࡾࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᘋ")
        return self.bstack11lll111l1l_opy_ and self.bstack11lll11111l_opy_()
    def bstack11lll11111l_opy_(self):
        return self.config.get(bstack11l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᘌ"), None) in bstack11lll11l11l_opy_
    def __11lll1111l1_opy_(self):
        bstack11ll1lllll1_opy_ = False
        for fw in bstack11lll1111ll_opy_:
            if fw in self.config.get(bstack11l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᘍ"), bstack11l1111_opy_ (u"ࠫࠬᘎ")):
                bstack11ll1lllll1_opy_ = True
        return bstack11l1l1ll_opy_(self.config.get(bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᘏ"), bstack11ll1lllll1_opy_))
    def bstack11lll111ll1_opy_(self):
        return (not self.bstack1ll1ll1l_opy_() and
                self.bstack1lll1ll11l_opy_ is not None and self.bstack1lll1ll11l_opy_.bstack1ll1ll1l_opy_())
    def bstack11ll1llll1l_opy_(self):
        if not self.bstack11lll111ll1_opy_():
            return
        if self.config.get(bstack11l1111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᘐ"), None) is None or self.config.get(bstack11l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᘑ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11l1111_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦ࡯ࡳࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡲࡺࡲ࡬࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡶࡩࡹࠦࡡࠡࡰࡲࡲ࠲ࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦ࠰ࠥᘒ"))
        if not self.__11lll1111l1_opy_():
            self.logger.info(bstack11l1111_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥᘓ"))
    def bstack11ll1lll11l_opy_(self):
        return self.bstack1111l11111_opy_
    def bstack1111l1ll11_opy_(self, bstack11ll1llllll_opy_):
        self.bstack1111l11111_opy_ = bstack11ll1llllll_opy_
        self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠦᘔ"), bstack11ll1llllll_opy_)
    def bstack11111lll11_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫࠳ࠨᘕ"))
                return None
            orchestration_strategy = None
            if self.bstack1lll1ll11l_opy_ is not None:
                orchestration_strategy = self.bstack1lll1ll11l_opy_.bstack11l11lll11_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11l1111_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠࡪࡵࠣࡒࡴࡴࡥ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡶࡴࡩࡥࡦࡦࠣࡻ࡮ࡺࡨࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴ࠮ࠣᘖ"))
                return None
            self.logger.info(bstack11l1111_opy_ (u"ࠨࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦᘗ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11l1111_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡃࡍࡋࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᘘ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡴࡦ࡮ࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᘙ"))
                self.bstack11lll111l11_opy_.bstack11lll111111_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack11lll111l11_opy_.bstack11ll1lll1ll_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡉ࡯ࡶࡰࡷࠦᘚ"), len(test_files))
            self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨᘛ"), int(os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢᘜ")) or bstack11l1111_opy_ (u"ࠧ࠶ࠢᘝ")))
            self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥᘞ"), int(os.environ.get(bstack11l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥᘟ")) or bstack11l1111_opy_ (u"ࠣ࠳ࠥᘠ")))
            self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨᘡ"), len(ordered_test_files))
            self.bstack11111lllll_opy_(bstack11l1111_opy_ (u"ࠥࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹࡁࡑࡋࡆࡥࡱࡲࡃࡰࡷࡱࡸࠧᘢ"), self.bstack11lll111l11_opy_.bstack11ll1llll11_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣ࡭ࡣࡶࡷࡪࡹ࠺ࠡࡽࢀࠦᘣ").format(e))
        return None
    def bstack11111lllll_opy_(self, key, value):
        self.bstack11lll11l111_opy_[key] = value
    def bstack11l111l1ll_opy_(self):
        return self.bstack11lll11l111_opy_