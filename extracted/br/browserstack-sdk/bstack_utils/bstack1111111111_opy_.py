# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll1l111111_opy_ import bstack1lll11llllll_opy_
from bstack_utils.bstack111l11lll_opy_ import bstack1l1111ll11_opy_
from bstack_utils.helper import bstack1111l11lll_opy_
import json
class bstack1l11l1ll11_opy_:
    _1l1lllll111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll11ll11ll_opy_ = bstack1lll11llllll_opy_(self.config, logger)
        self.bstack111l11lll_opy_ = bstack1l1111ll11_opy_.bstack1lllll1lll1_opy_(config=self.config)
        self.bstack1lll11ll1l1l_opy_ = {}
        self.bstack1llll1ll1l1_opy_ = False
        self.bstack1lll11lll11l_opy_ = (
            self.__1lll11lll1l1_opy_()
            and self.bstack111l11lll_opy_ is not None
            and self.bstack111l11lll_opy_.bstack1l111l1ll_opy_()
            and config.get(bstack111ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⓱"), None) is not None
            and config.get(bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⓲"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lllll1lll1_opy_(cls, config, logger):
        if cls._1l1lllll111_opy_ is None and config is not None:
            cls._1l1lllll111_opy_ = bstack1l11l1ll11_opy_(config, logger)
        return cls._1l1lllll111_opy_
    def bstack1l111l1ll_opy_(self):
        bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡰࠢࡱࡳࡹࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡽࡨࡦࡰ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒ࠵࠶ࡿࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏࡳࡦࡨࡶ࡮ࡴࡧࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⓳")
        return self.bstack1lll11lll11l_opy_ and self.bstack1lll11lll111_opy_()
    def bstack1lll11lll111_opy_(self):
        bstack1lll11llll1l_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ⓴"), self.config.get(bstack111ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⓵"), None))
        return bstack1lll11llll1l_opy_ in bstack111111l1111_opy_
    def __1lll11lll1l1_opy_(self):
        bstack11111ll1l11_opy_ = False
        for fw in bstack111111ll111_opy_:
            if fw in self.config.get(bstack111ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⓶"), bstack111ll11_opy_ (u"࠭ࠧ⓷")):
                bstack11111ll1l11_opy_ = True
        return bstack1111l11lll_opy_(self.config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⓸"), bstack11111ll1l11_opy_))
    def bstack1lll1l11111l_opy_(self):
        return (not self.bstack1l111l1ll_opy_() and
                self.bstack111l11lll_opy_ is not None and self.bstack111l11lll_opy_.bstack1l111l1ll_opy_())
    def bstack1lll11ll1ll1_opy_(self):
        if not self.bstack1lll1l11111l_opy_():
            return
        if self.config.get(bstack111ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⓹"), None) is None or self.config.get(bstack111ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⓺"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack111ll11_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧ⓻"))
        if not self.__1lll11lll1l1_opy_():
            self.logger.info(bstack111ll11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡫࡮ࡢࡤ࡯ࡩࠥ࡯ࡴࠡࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮ࠣ⓼"))
    def bstack1lll11ll1l11_opy_(self):
        return self.bstack1llll1ll1l1_opy_
    def bstack1llll1lllll_opy_(self, bstack1lll11lllll1_opy_):
        self.bstack1llll1ll1l1_opy_ = bstack1lll11lllll1_opy_
        self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨ⓽"), bstack1lll11lllll1_opy_)
    def bstack1llll1llll1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣ⓾"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111l11lll_opy_.bstack1lll1l1111l1_opy_()
            if self.bstack111l11lll_opy_ is not None:
                orchestration_strategy = self.bstack111l11lll_opy_.bstack1l11l1111l_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack111ll11_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥ⓿"))
                return None
            self.logger.info(bstack111ll11_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨ─").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack111ll11_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ━"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack111ll11_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ│"))
                self.bstack1lll11ll11ll_opy_.bstack1lll11ll1lll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll11ll11ll_opy_.bstack1lll11llll11_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨ┃"), len(test_files))
            self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ┄"), int(os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ┅")) or bstack111ll11_opy_ (u"ࠢ࠱ࠤ┆")))
            self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ┇"), int(os.environ.get(bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ┈")) or bstack111ll11_opy_ (u"ࠥ࠵ࠧ┉")))
            self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣ┊"), len(ordered_test_files))
            self.bstack1lllll11111_opy_(bstack111ll11_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢ┋"), self.bstack1lll11ll11ll_opy_.bstack1lll11lll1ll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨ┌").format(e))
        return None
    def bstack1lllll11111_opy_(self, key, value):
        self.bstack1lll11ll1l1l_opy_[key] = value
    def bstack11l1lll1l1_opy_(self):
        return self.bstack1lll11ll1l1l_opy_