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
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111111l111l_opy_ import bstack111111l11ll_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from bstack_utils.helper import bstack1lll1l111_opy_
import json
class bstack1lllll1l1l_opy_:
    _1ll1l11l111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111111l11l1_opy_ = bstack111111l11ll_opy_(self.config, logger)
        self.bstack11ll11l1l_opy_ = bstack1l1l11l11l_opy_.get_instance(config=self.config)
        self.bstack1111111ll11_opy_ = {}
        self.bstack1llll1l1lll_opy_ = False
        self.bstack1111111l1l1_opy_ = (
            self.__1111111lll1_opy_()
            and self.bstack11ll11l1l_opy_ is not None
            and self.bstack11ll11l1l_opy_.bstack1l1ll111ll_opy_()
            and config.get(bstack11l1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ₊"), None) is not None
            and config.get(bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ₋"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll1l11l111_opy_ is None and config is not None:
            cls._1ll1l11l111_opy_ = bstack1lllll1l1l_opy_(config, logger)
        return cls._1ll1l11l111_opy_
    def bstack1l1ll111ll_opy_(self):
        bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡰࠢࡱࡳࡹࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡽࡨࡦࡰ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒ࠵࠶ࡿࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏࡳࡦࡨࡶ࡮ࡴࡧࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ₌")
        return self.bstack1111111l1l1_opy_ and self.bstack1111111l111_opy_()
    def bstack1111111l111_opy_(self):
        bstack111111l1l1l_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ₍"), self.config.get(bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ₎"), None))
        return bstack111111l1l1l_opy_ in bstack111ll1ll1l1_opy_
    def __1111111lll1_opy_(self):
        bstack11l11111111_opy_ = False
        for fw in bstack111llll1111_opy_:
            if fw in self.config.get(bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ₏"), bstack11l1l11_opy_ (u"࠭ࠧₐ")):
                bstack11l11111111_opy_ = True
        return bstack1lll1l111_opy_(self.config.get(bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫₑ"), bstack11l11111111_opy_))
    def bstack1111111l11l_opy_(self):
        return (not self.bstack1l1ll111ll_opy_() and
                self.bstack11ll11l1l_opy_ is not None and self.bstack11ll11l1l_opy_.bstack1l1ll111ll_opy_())
    def bstack11111111lll_opy_(self):
        if not self.bstack1111111l11l_opy_():
            return
        if self.config.get(bstack11l1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ₒ"), None) is None or self.config.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬₓ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11l1l11_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧₔ"))
        if not self.__1111111lll1_opy_():
            self.logger.info(bstack11l1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡫࡮ࡢࡤ࡯ࡩࠥ࡯ࡴࠡࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮ࠣₕ"))
    def bstack1111111ll1l_opy_(self):
        return self.bstack1llll1l1lll_opy_
    def bstack1llll11l111_opy_(self, bstack111111l1l11_opy_):
        self.bstack1llll1l1lll_opy_ = bstack111111l1l11_opy_
        self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨₖ"), bstack111111l1l11_opy_)
    def bstack1llll1l11l1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣₗ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack11ll11l1l_opy_.bstack1111111llll_opy_()
            if self.bstack11ll11l1l_opy_ is not None:
                orchestration_strategy = self.bstack11ll11l1l_opy_.bstack1ll11llll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11l1l11_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥₘ"))
                return None
            self.logger.info(bstack11l1l11_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨₙ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧₚ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11l1l11_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨₛ"))
                self.bstack111111l11l1_opy_.bstack11111111ll1_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack111111l11l1_opy_.bstack111111l1111_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨₜ"), len(test_files))
            self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ₝"), int(os.environ.get(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ₞")) or bstack11l1l11_opy_ (u"ࠢ࠱ࠤ₟")))
            self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ₠"), int(os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ₡")) or bstack11l1l11_opy_ (u"ࠥ࠵ࠧ₢")))
            self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣ₣"), len(ordered_test_files))
            self.bstack1llll1l1l1l_opy_(bstack11l1l11_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢ₤"), self.bstack111111l11l1_opy_.bstack1111111l1ll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨ₥").format(e))
        return None
    def bstack1llll1l1l1l_opy_(self, key, value):
        self.bstack1111111ll11_opy_[key] = value
    def bstack111llll111_opy_(self):
        return self.bstack1111111ll11_opy_