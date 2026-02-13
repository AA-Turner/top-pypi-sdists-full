# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1111111111l_opy_ import bstack11111111l11_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.helper import bstack1ll1l11lll_opy_
import json
class bstack1l1lll11l_opy_:
    _1ll11111lll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111111111l1_opy_ = bstack11111111l11_opy_(self.config, logger)
        self.bstack1l11ll1l_opy_ = bstack1l11l1l1ll_opy_.bstack111l1lll_opy_(config=self.config)
        self.bstack1lllllll1ll1_opy_ = {}
        self.bstack1lll1lll1ll_opy_ = False
        self.bstack1lllllll1l1l_opy_ = (
            self.__1lllllllllll_opy_()
            and self.bstack1l11ll1l_opy_ is not None
            and self.bstack1l11ll1l_opy_.bstack1l11lllll_opy_()
            and config.get(bstack11l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⁿ"), None) is not None
            and config.get(bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ₀"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack111l1lll_opy_(cls, config, logger):
        if cls._1ll11111lll_opy_ is None and config is not None:
            cls._1ll11111lll_opy_ = bstack1l1lll11l_opy_(config, logger)
        return cls._1ll11111lll_opy_
    def bstack1l11lllll_opy_(self):
        bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡇࡳࠥࡴ࡯ࡵࠢࡤࡴࡵࡲࡹࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡹ࡫ࡩࡳࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕ࠱࠲ࡻࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒࡶࡩ࡫ࡲࡪࡰࡪࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ₁")
        return self.bstack1lllllll1l1l_opy_ and self.bstack1llllllllll1_opy_()
    def bstack1llllllllll1_opy_(self):
        bstack111111111ll_opy_ = os.getenv(bstack11l11_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ₂"), self.config.get(bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ₃"), None))
        return bstack111111111ll_opy_ in bstack111ll111l1l_opy_
    def __1lllllllllll_opy_(self):
        bstack111llll1111_opy_ = False
        for fw in bstack111ll1lllll_opy_:
            if fw in self.config.get(bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₄"), bstack11l11_opy_ (u"ࠩࠪ₅")):
                bstack111llll1111_opy_ = True
        return bstack1ll1l11lll_opy_(self.config.get(bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ₆"), bstack111llll1111_opy_))
    def bstack1llllllll1ll_opy_(self):
        return (not self.bstack1l11lllll_opy_() and
                self.bstack1l11ll1l_opy_ is not None and self.bstack1l11ll1l_opy_.bstack1l11lllll_opy_())
    def bstack1llllllll1l1_opy_(self):
        if not self.bstack1llllllll1ll_opy_():
            return
        if self.config.get(bstack11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ₇"), None) is None or self.config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ₈"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11l11_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠤࡴࡸࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡰࡸࡰࡱ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡴࡧࡷࠤࡦࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫࠮ࠣ₉"))
        if not self.__1lllllllllll_opy_():
            self.logger.info(bstack11l11_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡪࡩࡴࡣࡥࡰࡪࡪ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡧࡱࡥࡧࡲࡥࠡ࡫ࡷࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱ࠦ₊"))
    def bstack1llllllll11l_opy_(self):
        return self.bstack1lll1lll1ll_opy_
    def bstack1lll1lll11l_opy_(self, bstack1lllllllll1l_opy_):
        self.bstack1lll1lll1ll_opy_ = bstack1lllllllll1l_opy_
        self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡥࡥࠤ₋"), bstack1lllllllll1l_opy_)
    def bstack1lll1l1ll11_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11l11_opy_ (u"ࠤ࡞ࡶࡪࡵࡲࡥࡧࡵࡣࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳ࡞ࠢࡑࡳࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤ࡫ࡵࡲࠡࡱࡵࡨࡪࡸࡩ࡯ࡩ࠱ࠦ₌"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1l11ll1l_opy_.bstack1lllllllll11_opy_()
            if self.bstack1l11ll1l_opy_ is not None:
                orchestration_strategy = self.bstack1l11ll1l_opy_.bstack11llllll1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11l11_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡹࡸࡡࡵࡧࡪࡽࠥ࡯ࡳࠡࡐࡲࡲࡪ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡴࡲࡧࡪ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠳ࠨ₍"))
                return None
            self.logger.info(bstack11l11_opy_ (u"ࠦࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡩࡵࡪࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡻࡾࠤ₎").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11l11_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡈࡒࡉࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ₏"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡹࡤ࡬ࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤₐ"))
                self.bstack111111111l1_opy_.bstack1lllllll1lll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack111111111l1_opy_.bstack1llllllll111_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤₑ"), len(test_files))
            self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦₒ"), int(os.environ.get(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧₓ")) or bstack11l11_opy_ (u"ࠥ࠴ࠧₔ")))
            self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣₕ"), int(os.environ.get(bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣₖ")) or bstack11l11_opy_ (u"ࠨ࠱ࠣₗ")))
            self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡉ࡯ࡶࡰࡷࠦₘ"), len(ordered_test_files))
            self.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠣࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡆࡖࡉࡄࡣ࡯ࡰࡈࡵࡵ࡯ࡶࠥₙ"), self.bstack111111111l1_opy_.bstack11111111111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠤ࡞ࡶࡪࡵࡲࡥࡧࡵࡣࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳ࡞ࠢࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡲࡡࡴࡵࡨࡷ࠿ࠦࡻࡾࠤₚ").format(e))
        return None
    def bstack1llll111lll_opy_(self, key, value):
        self.bstack1lllllll1ll1_opy_[key] = value
    def bstack1l1l1111l_opy_(self):
        return self.bstack1lllllll1ll1_opy_