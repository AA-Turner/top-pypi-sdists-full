# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111111l11ll_opy_ import bstack1111111l1ll_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from bstack_utils.helper import bstack11l1lll1_opy_
import json
class bstack1llll1lll1_opy_:
    _1ll1l1llll1_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111111l111l_opy_ = bstack1111111l1ll_opy_(self.config, logger)
        self.bstack1lllll111l_opy_ = bstack1111lll11_opy_.get_instance(config=self.config)
        self.bstack11111111lll_opy_ = {}
        self.bstack1llll1l1l1l_opy_ = False
        self.bstack111111l11l1_opy_ = (
            self.__1111111ll1l_opy_()
            and self.bstack1lllll111l_opy_ is not None
            and self.bstack1lllll111l_opy_.bstack11l1ll1l_opy_()
            and config.get(bstack11ll111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ₇"), None) is not None
            and config.get(bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ₈"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll1l1llll1_opy_ is None and config is not None:
            cls._1ll1l1llll1_opy_ = bstack1llll1lll1_opy_(config, logger)
        return cls._1ll1l1llll1_opy_
    def bstack11l1ll1l_opy_(self):
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡴࠦ࡮ࡰࡶࠣࡥࡵࡶ࡬ࡺࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡺ࡬ࡪࡴ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏ࠲࠳ࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓࡷࡪࡥࡳ࡫ࡱ࡫ࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ₉")
        return self.bstack111111l11l1_opy_ and self.bstack11111111l1l_opy_()
    def bstack11111111l1l_opy_(self):
        bstack1111111l11l_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ₊"), self.config.get(bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₋"), None))
        return bstack1111111l11l_opy_ in bstack111lll1l1ll_opy_
    def __1111111ll1l_opy_(self):
        bstack111lllllll1_opy_ = False
        for fw in bstack111lll11l11_opy_:
            if fw in self.config.get(bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ₌"), bstack11ll111_opy_ (u"ࠪࠫ₍")):
                bstack111lllllll1_opy_ = True
        return bstack11l1lll1_opy_(self.config.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ₎"), bstack111lllllll1_opy_))
    def bstack111111l1111_opy_(self):
        return (not self.bstack11l1ll1l_opy_() and
                self.bstack1lllll111l_opy_ is not None and self.bstack1lllll111l_opy_.bstack11l1ll1l_opy_())
    def bstack11111111ll1_opy_(self):
        if not self.bstack111111l1111_opy_():
            return
        if self.config.get(bstack11ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ₏"), None) is None or self.config.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩₐ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11ll111_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤₑ"))
        if not self.__1111111ll1l_opy_():
            self.logger.info(bstack11ll111_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧₒ"))
    def bstack1111111ll11_opy_(self):
        return self.bstack1llll1l1l1l_opy_
    def bstack1llll1ll11l_opy_(self, bstack1111111lll1_opy_):
        self.bstack1llll1l1l1l_opy_ = bstack1111111lll1_opy_
        self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥₓ"), bstack1111111lll1_opy_)
    def bstack1llll1lll11_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧₔ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1lllll111l_opy_.bstack1111111l111_opy_()
            if self.bstack1lllll111l_opy_ is not None:
                orchestration_strategy = self.bstack1lllll111l_opy_.bstack1l11111l11_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11ll111_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢₕ"))
                return None
            self.logger.info(bstack11ll111_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥₖ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤₗ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥₘ"))
                self.bstack111111l111l_opy_.bstack111111l1l11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack111111l111l_opy_.bstack1111111llll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥₙ"), len(test_files))
            self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧₚ"), int(os.environ.get(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨₛ")) or bstack11ll111_opy_ (u"ࠦ࠵ࠨₜ")))
            self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ₝"), int(os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ₞")) or bstack11ll111_opy_ (u"ࠢ࠲ࠤ₟")))
            self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧ₠"), len(ordered_test_files))
            self.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦ₡"), self.bstack111111l111l_opy_.bstack1111111l1l1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥ₢").format(e))
        return None
    def bstack1llll111111_opy_(self, key, value):
        self.bstack11111111lll_opy_[key] = value
    def bstack111l11ll1l_opy_(self):
        return self.bstack11111111lll_opy_