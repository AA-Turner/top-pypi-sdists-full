# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll11lll1ll_opy_ import bstack1lll1l111lll_opy_
from bstack_utils.bstack1111l11l_opy_ import bstack1l1l111111_opy_
from bstack_utils.helper import bstack111111lll1_opy_
import json
class bstack11l1111ll1_opy_:
    _1l1lll1l1ll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll1l1111ll_opy_ = bstack1lll1l111lll_opy_(self.config, logger)
        self.bstack1111l11l_opy_ = bstack1l1l111111_opy_.bstack1ll11ll111_opy_(config=self.config)
        self.bstack1lll11lllll1_opy_ = {}
        self.bstack1llll1ll1ll_opy_ = False
        self.bstack1lll11llllll_opy_ = (
            self.__1lll1l111l1l_opy_()
            and self.bstack1111l11l_opy_ is not None
            and self.bstack1111l11l_opy_.bstack1lll1lll1_opy_()
            and config.get(bstack1l111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ⓤ"), None) is not None
            and config.get(bstack1l111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬⓥ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1ll11ll111_opy_(cls, config, logger):
        if cls._1l1lll1l1ll_opy_ is None and config is not None:
            cls._1l1lll1l1ll_opy_ = bstack11l1111ll1_opy_(config, logger)
        return cls._1l1lll1l1ll_opy_
    def bstack1lll1lll1_opy_(self):
        bstack1l111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨⓦ")
        return self.bstack1lll11llllll_opy_ and self.bstack1lll1l11l11l_opy_()
    def bstack1lll1l11l11l_opy_(self):
        bstack1lll11llll11_opy_ = os.getenv(bstack1l111l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬⓧ"), self.config.get(bstack1l111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨⓨ"), None))
        return bstack1lll11llll11_opy_ in bstack11111l1111l_opy_
    def __1lll1l111l1l_opy_(self):
        bstack11111ll1l11_opy_ = False
        for fw in bstack11111l1l11l_opy_:
            if fw in self.config.get(bstack1l111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩⓩ"), bstack1l111l_opy_ (u"ࠧࠨ⓪")):
                bstack11111ll1l11_opy_ = True
        return bstack111111lll1_opy_(self.config.get(bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⓫"), bstack11111ll1l11_opy_))
    def bstack1lll11lll1l1_opy_(self):
        return (not self.bstack1lll1lll1_opy_() and
                self.bstack1111l11l_opy_ is not None and self.bstack1111l11l_opy_.bstack1lll1lll1_opy_())
    def bstack1lll11llll1l_opy_(self):
        if not self.bstack1lll11lll1l1_opy_():
            return
        if self.config.get(bstack1l111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⓬"), None) is None or self.config.get(bstack1l111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⓭"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l111l_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢࡲࡶࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦ࡮ࡶ࡮࡯࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠳ࠨ⓮"))
        if not self.__1lll1l111l1l_opy_():
            self.logger.info(bstack1l111l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤ⓯"))
    def bstack1lll1l11l111_opy_(self):
        return self.bstack1llll1ll1ll_opy_
    def bstack1llll1lll1l_opy_(self, bstack1lll1l111ll1_opy_):
        self.bstack1llll1ll1ll_opy_ = bstack1lll1l111ll1_opy_
        self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠢ⓰"), bstack1lll1l111ll1_opy_)
    def bstack1lllll1111l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l111l_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧ࠯ࠤ⓱"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1111l11l_opy_.bstack1lll1l1111l1_opy_()
            if self.bstack1111l11l_opy_ is not None:
                orchestration_strategy = self.bstack1111l11l_opy_.bstack1111ll1l_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l111l_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣ࡭ࡸࠦࡎࡰࡰࡨ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡲࡰࡥࡨࡩࡩࠦࡷࡪࡶ࡫ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠱ࠦ⓲"))
                return None
            self.logger.info(bstack1l111l_opy_ (u"ࠤࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢ⓳").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l111l_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡆࡐࡎࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ⓴"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l111l_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡷࡩࡱࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢ⓵"))
                self.bstack1lll1l1111ll_opy_.bstack1lll1l111l11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll1l1111ll_opy_.bstack1lll1l11111l_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢ⓶"), len(test_files))
            self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⓷"), int(os.environ.get(bstack1l111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⓸")) or bstack1l111l_opy_ (u"ࠣ࠲ࠥ⓹")))
            self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⓺"), int(os.environ.get(bstack1l111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ⓻")) or bstack1l111l_opy_ (u"ࠦ࠶ࠨ⓼")))
            self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤ⓽"), len(ordered_test_files))
            self.bstack1llll1lllll_opy_(bstack1l111l_opy_ (u"ࠨࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡄࡔࡎࡉࡡ࡭࡮ࡆࡳࡺࡴࡴࠣ⓾"), self.bstack1lll1l1111ll_opy_.bstack1lll1l111111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l111l_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡰࡦࡹࡳࡦࡵ࠽ࠤࢀࢃࠢ⓿").format(e))
        return None
    def bstack1llll1lllll_opy_(self, key, value):
        self.bstack1lll11lllll1_opy_[key] = value
    def bstack1lllll1l1l_opy_(self):
        return self.bstack1lll11lllll1_opy_