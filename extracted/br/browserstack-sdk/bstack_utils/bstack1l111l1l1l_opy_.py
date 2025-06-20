# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1llll11_opy_ import bstack111l1llll1l_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack111l11l1l_opy_
from bstack_utils.helper import bstack1l111ll1l_opy_
class bstack1lll1lll1_opy_:
    _1lll11l1111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1ll1l1l_opy_ = bstack111l1llll1l_opy_(self.config, logger)
        self.bstack1lll111l_opy_ = bstack111l11l1l_opy_.bstack1lll11ll_opy_(config=self.config)
        self.bstack111l1lll11l_opy_ = {}
        self.bstack11111l1ll1_opy_ = False
        self.bstack111ll11111l_opy_ = (
            self.__111l1lll1ll_opy_()
            and self.bstack1lll111l_opy_ is not None
            and self.bstack1lll111l_opy_.bstack1111111l1_opy_()
            and config.get(bstack11ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᶁ"), None) is not None
            and config.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᶂ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lll11ll_opy_(cls, config, logger):
        if cls._1lll11l1111_opy_ is None and config is not None:
            cls._1lll11l1111_opy_ = bstack1lll1lll1_opy_(config, logger)
        return cls._1lll11l1111_opy_
    def bstack1111111l1_opy_(self):
        bstack11ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡰࠢࡱࡳࡹࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡽࡨࡦࡰ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒ࠵࠶ࡿࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏࡳࡦࡨࡶ࡮ࡴࡧࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᶃ")
        return self.bstack111ll11111l_opy_ and self.bstack111l1lll1l1_opy_()
    def bstack111l1lll1l1_opy_(self):
        return self.config.get(bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᶄ"), None) in bstack11l1ll1l1ll_opy_
    def __111l1lll1ll_opy_(self):
        bstack11ll11l11ll_opy_ = False
        for fw in bstack11ll1111111_opy_:
            if fw in self.config.get(bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᶅ"), bstack11ll11_opy_ (u"ࠬ࠭ᶆ")):
                bstack11ll11l11ll_opy_ = True
        return bstack1l111ll1l_opy_(self.config.get(bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᶇ"), bstack11ll11l11ll_opy_))
    def bstack111ll111111_opy_(self):
        return (not self.bstack1111111l1_opy_() and
                self.bstack1lll111l_opy_ is not None and self.bstack1lll111l_opy_.bstack1111111l1_opy_())
    def bstack111l1ll1l11_opy_(self):
        if not self.bstack111ll111111_opy_():
            return
        if self.config.get(bstack11ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᶈ"), None) is None or self.config.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᶉ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11ll11_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡰࡴࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡳࡻ࡬࡭࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡻࡧ࡬ࡶࡧ࠱ࠦᶊ"))
        if not self.__111l1lll1ll_opy_():
            self.logger.info(bstack11ll11_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢ࡬ࡷࠥࡪࡩࡴࡣࡥࡰࡪࡪ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡧࡱࡥࡧࡲࡥࠡ࡫ࡷࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱ࠦᶋ"))
    def bstack111l1ll1ll1_opy_(self):
        return self.bstack11111l1ll1_opy_
    def bstack1111ll111l_opy_(self, bstack111l1lllll1_opy_):
        self.bstack11111l1ll1_opy_ = bstack111l1lllll1_opy_
        self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠧᶌ"), bstack111l1lllll1_opy_)
    def bstack1111l1ll1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬࠴ࠢᶍ"))
                return None
            orchestration_strategy = None
            if self.bstack1lll111l_opy_ is not None:
                orchestration_strategy = self.bstack1lll111l_opy_.bstack1l1ll1l11_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11ll11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡ࡫ࡶࠤࡓࡵ࡮ࡦ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡷࡵࡣࡦࡧࡧࠤࡼ࡯ࡴࡩࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠯ࠤᶎ"))
                return None
            self.logger.info(bstack11ll11_opy_ (u"ࠢࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧᶏ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡄࡎࡌࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᶐ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡵࡧ࡯ࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᶑ"))
                self.bstack111l1ll1l1l_opy_.bstack111l1lll111_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack111l1ll1l1l_opy_.bstack111l1llllll_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧᶒ"), len(test_files))
            self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢᶓ"), int(os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣᶔ")) or bstack11ll11_opy_ (u"ࠨ࠰ࠣᶕ")))
            self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦᶖ"), int(os.environ.get(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦᶗ")) or bstack11ll11_opy_ (u"ࠤ࠴ࠦᶘ")))
            self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢᶙ"), len(ordered_test_files))
            self.bstack11111lll1l_opy_(bstack11ll11_opy_ (u"ࠦࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࡂࡒࡌࡇࡦࡲ࡬ࡄࡱࡸࡲࡹࠨᶚ"), self.bstack111l1ll1l1l_opy_.bstack111l1ll1lll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤ࡮ࡤࡷࡸ࡫ࡳ࠻ࠢࡾࢁࠧᶛ").format(e))
        return None
    def bstack11111lll1l_opy_(self, key, value):
        self.bstack111l1lll11l_opy_[key] = value
    def bstack1llllll1l1_opy_(self):
        return self.bstack111l1lll11l_opy_