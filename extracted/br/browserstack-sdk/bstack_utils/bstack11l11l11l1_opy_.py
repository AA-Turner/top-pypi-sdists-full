# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll11ll1l11_opy_ import bstack1lll11ll1lll_opy_
from bstack_utils.bstack11lll1lll_opy_ import bstack1lll1111ll_opy_
from bstack_utils.helper import bstack1ll111lll_opy_
import json
class bstack1lll111ll1_opy_:
    _1l1llll1l11_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll11ll1l1l_opy_ = bstack1lll11ll1lll_opy_(self.config, logger)
        self.bstack11lll1lll_opy_ = bstack1lll1111ll_opy_.bstack111111l1ll_opy_(config=self.config)
        self.bstack1lll11ll11l1_opy_ = {}
        self.bstack1llll1llll1_opy_ = False
        self.bstack1lll11llllll_opy_ = (
            self.__1lll11ll111l_opy_()
            and self.bstack11lll1lll_opy_ is not None
            and self.bstack11lll1lll_opy_.bstack1ll1lllll_opy_()
            and config.get(bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⓳"), None) is not None
            and config.get(bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⓴"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack111111l1ll_opy_(cls, config, logger):
        if cls._1l1llll1l11_opy_ is None and config is not None:
            cls._1l1llll1l11_opy_ = bstack1lll111ll1_opy_(config, logger)
        return cls._1l1llll1l11_opy_
    def bstack1ll1lllll_opy_(self):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡲࠤࡳࡵࡴࠡࡣࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔ࠷࠱ࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑࡵࡨࡪࡸࡩ࡯ࡩࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⓵")
        return self.bstack1lll11llllll_opy_ and self.bstack1lll11lll111_opy_()
    def bstack1lll11lll111_opy_(self):
        bstack1lll11lll1ll_opy_ = os.getenv(bstack1l1111l_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭⓶"), self.config.get(bstack1l1111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⓷"), None))
        return bstack1lll11lll1ll_opy_ in bstack11111l11lll_opy_
    def __1lll11ll111l_opy_(self):
        bstack11111ll111l_opy_ = False
        for fw in bstack1111111l1ll_opy_:
            if fw in self.config.get(bstack1l1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⓸"), bstack1l1111l_opy_ (u"ࠨࠩ⓹")):
                bstack11111ll111l_opy_ = True
        return bstack1ll111lll_opy_(self.config.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⓺"), bstack11111ll111l_opy_))
    def bstack1lll1l111111_opy_(self):
        return (not self.bstack1ll1lllll_opy_() and
                self.bstack11lll1lll_opy_ is not None and self.bstack11lll1lll_opy_.bstack1ll1lllll_opy_())
    def bstack1lll11ll1ll1_opy_(self):
        if not self.bstack1lll1l111111_opy_():
            return
        if self.config.get(bstack1l1111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⓻"), None) is None or self.config.get(bstack1l1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⓼"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1111l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣࡳࡷࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠ࡯ࡷ࡯ࡰ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠴ࠢ⓽"))
        if not self.__1lll11ll111l_opy_():
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥ⓾"))
    def bstack1lll11lll1l1_opy_(self):
        return self.bstack1llll1llll1_opy_
    def bstack1lllll11111_opy_(self, bstack1lll11llll1l_opy_):
        self.bstack1llll1llll1_opy_ = bstack1lll11llll1l_opy_
        self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠣ⓿"), bstack1lll11llll1l_opy_)
    def bstack1llll1lllll_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡰࡴࡧࡩࡷ࡯࡮ࡨ࠰ࠥ─"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack11lll1lll_opy_.bstack1lll11llll11_opy_()
            if self.bstack11lll1lll_opy_ is not None:
                orchestration_strategy = self.bstack11lll1lll_opy_.bstack11ll1llll1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1111l_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤ࡮ࡹࠠࡏࡱࡱࡩ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡳࡱࡦࡩࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠲ࠧ━"))
                return None
            self.logger.info(bstack1l1111l_opy_ (u"ࠥࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣ│").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1111l_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡇࡑࡏࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢ┃"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l1111l_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡸࡪ࡫ࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ┄"))
                self.bstack1lll11ll1l1l_opy_.bstack1lll11lllll1_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll11ll1l1l_opy_.bstack1lll11lll11l_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣ┅"), len(test_files))
            self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ┆"), int(os.environ.get(bstack1l1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ┇")) or bstack1l1111l_opy_ (u"ࠤ࠳ࠦ┈")))
            self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ┉"), int(os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ┊")) or bstack1l1111l_opy_ (u"ࠧ࠷ࠢ┋")))
            self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥ┌"), len(ordered_test_files))
            self.bstack1llll1ll11l_opy_(bstack1l1111l_opy_ (u"ࠢࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡅࡕࡏࡃࡢ࡮࡯ࡇࡴࡻ࡮ࡵࠤ┍"), self.bstack1lll11ll1l1l_opy_.bstack1lll11ll11ll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡱࡧࡳࡴࡧࡶ࠾ࠥࢁࡽࠣ┎").format(e))
        return None
    def bstack1llll1ll11l_opy_(self, key, value):
        self.bstack1lll11ll11l1_opy_[key] = value
    def bstack1ll111lll1_opy_(self):
        return self.bstack1lll11ll11l1_opy_