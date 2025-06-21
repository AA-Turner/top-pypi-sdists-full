# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1lll111_opy_ import bstack111l1ll1lll_opy_
from bstack_utils.bstack1llll1llll_opy_ import bstack1ll11111l_opy_
from bstack_utils.helper import bstack1lll1l1lll_opy_
class bstack1l111llll_opy_:
    _1lll1111l1l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1lllll1_opy_ = bstack111l1ll1lll_opy_(self.config, logger)
        self.bstack1llll1llll_opy_ = bstack1ll11111l_opy_.bstack1ll11lll_opy_(config=self.config)
        self.bstack111l1lll1ll_opy_ = {}
        self.bstack1111l1llll_opy_ = False
        self.bstack111l1lll11l_opy_ = (
            self.__111l1llll1l_opy_()
            and self.bstack1llll1llll_opy_ is not None
            and self.bstack1llll1llll_opy_.bstack1ll1111l_opy_()
            and config.get(bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᶂ"), None) is not None
            and config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᶃ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1ll11lll_opy_(cls, config, logger):
        if cls._1lll1111l1l_opy_ is None and config is not None:
            cls._1lll1111l1l_opy_ = bstack1l111llll_opy_(config, logger)
        return cls._1lll1111l1l_opy_
    def bstack1ll1111l_opy_(self):
        bstack1l1l1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᶄ")
        return self.bstack111l1lll11l_opy_ and self.bstack111l1ll1l1l_opy_()
    def bstack111l1ll1l1l_opy_(self):
        return self.config.get(bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᶅ"), None) in bstack11l1lll1111_opy_
    def __111l1llll1l_opy_(self):
        bstack11ll11l11ll_opy_ = False
        for fw in bstack11l1lll1l11_opy_:
            if fw in self.config.get(bstack1l1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᶆ"), bstack1l1l1l1_opy_ (u"࠭ࠧᶇ")):
                bstack11ll11l11ll_opy_ = True
        return bstack1lll1l1lll_opy_(self.config.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᶈ"), bstack11ll11l11ll_opy_))
    def bstack111l1llll11_opy_(self):
        return (not self.bstack1ll1111l_opy_() and
                self.bstack1llll1llll_opy_ is not None and self.bstack1llll1llll_opy_.bstack1ll1111l_opy_())
    def bstack111ll111111_opy_(self):
        if not self.bstack111l1llll11_opy_():
            return
        if self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᶉ"), None) is None or self.config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᶊ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧᶋ"))
        if not self.__111l1llll1l_opy_():
            self.logger.info(bstack1l1l1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧᶌ"))
    def bstack111l1ll1l11_opy_(self):
        return self.bstack1111l1llll_opy_
    def bstack11111ll11l_opy_(self, bstack111l1lll1l1_opy_):
        self.bstack1111l1llll_opy_ = bstack111l1lll1l1_opy_
        self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨᶍ"), bstack111l1lll1l1_opy_)
    def bstack1111ll11l1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣᶎ"))
                return None
            orchestration_strategy = None
            if self.bstack1llll1llll_opy_ is not None:
                orchestration_strategy = self.bstack1llll1llll_opy_.bstack1l1111llll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥᶏ"))
                return None
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨᶐ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᶑ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1l1l1l1_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨᶒ"))
                self.bstack111l1lllll1_opy_.bstack111l1llllll_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack111l1lllll1_opy_.bstack111l1ll1ll1_opy_()
            if not ordered_test_files:
                return None
            self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨᶓ"), len(test_files))
            self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣᶔ"), int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᶕ")) or bstack1l1l1l1_opy_ (u"ࠢ࠱ࠤᶖ")))
            self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧᶗ"), int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧᶘ")) or bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧᶙ")))
            self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣᶚ"), len(ordered_test_files))
            self.bstack1111l1l11l_opy_(bstack1l1l1l1_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢᶛ"), self.bstack111l1lllll1_opy_.bstack111ll11111l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨᶜ").format(e))
        return None
    def bstack1111l1l11l_opy_(self, key, value):
        self.bstack111l1lll1ll_opy_[key] = value
    def bstack111l111ll_opy_(self):
        return self.bstack111l1lll1ll_opy_