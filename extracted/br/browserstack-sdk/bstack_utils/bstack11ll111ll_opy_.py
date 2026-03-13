# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lllll1lll11_opy_ import bstack1lllll1l1111_opy_
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from bstack_utils.helper import bstack1ll111llll_opy_
import json
class bstack1l11lll1l1_opy_:
    _1ll11l111ll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lllll1l1l11_opy_ = bstack1lllll1l1111_opy_(self.config, logger)
        self.bstack11llllll1_opy_ = bstack11ll11l11l_opy_.get_instance(config=self.config)
        self.bstack1lllll1ll1ll_opy_ = {}
        self.bstack1lll1l11ll1_opy_ = False
        self.bstack1lllll1l1l1l_opy_ = (
            self.__1lllll1l11l1_opy_()
            and self.bstack11llllll1_opy_ is not None
            and self.bstack11llllll1_opy_.bstack11l111l1ll_opy_()
            and config.get(bstack1111l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ≱"), None) is not None
            and config.get(bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ≲"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll11l111ll_opy_ is None and config is not None:
            cls._1ll11l111ll_opy_ = bstack1l11lll1l1_opy_(config, logger)
        return cls._1ll11l111ll_opy_
    def bstack11l111l1ll_opy_(self):
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡴࠦ࡮ࡰࡶࠣࡥࡵࡶ࡬ࡺࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡺ࡬ࡪࡴ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏ࠲࠳ࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓࡷࡪࡥࡳ࡫ࡱ࡫ࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ≳")
        return self.bstack1lllll1l1l1l_opy_ and self.bstack1lllll1ll111_opy_()
    def bstack1lllll1ll111_opy_(self):
        bstack1lllll1l111l_opy_ = os.getenv(bstack1111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ≴"), self.config.get(bstack1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ≵"), None))
        return bstack1lllll1l111l_opy_ in bstack111l1l1llll_opy_
    def __1lllll1l11l1_opy_(self):
        bstack111ll11l1ll_opy_ = False
        for fw in bstack111ll111lll_opy_:
            if fw in self.config.get(bstack1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ≶"), bstack1111l_opy_ (u"ࠪࠫ≷")):
                bstack111ll11l1ll_opy_ = True
        return bstack1ll111llll_opy_(self.config.get(bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ≸"), bstack111ll11l1ll_opy_))
    def bstack1lllll1llll1_opy_(self):
        return (not self.bstack11l111l1ll_opy_() and
                self.bstack11llllll1_opy_ is not None and self.bstack11llllll1_opy_.bstack11l111l1ll_opy_())
    def bstack1lllll1l1lll_opy_(self):
        if not self.bstack1lllll1llll1_opy_():
            return
        if self.config.get(bstack1111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ≹"), None) is None or self.config.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ≺"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1111l_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤ≻"))
        if not self.__1lllll1l11l1_opy_():
            self.logger.info(bstack1111l_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧ≼"))
    def bstack1lllll1ll1l1_opy_(self):
        return self.bstack1lll1l11ll1_opy_
    def bstack1lll1l1l1l1_opy_(self, bstack1lllll11llll_opy_):
        self.bstack1lll1l11ll1_opy_ = bstack1lllll11llll_opy_
        self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥ≽"), bstack1lllll11llll_opy_)
    def bstack1lll1lllll1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1111l_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧ≾"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack11llllll1_opy_.bstack1lllll1lll1l_opy_()
            if self.bstack11llllll1_opy_ is not None:
                orchestration_strategy = self.bstack11llllll1_opy_.bstack11111l11l_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1111l_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢ≿"))
                return None
            self.logger.info(bstack1111l_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ⊀").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1111l_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ⊁"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥ⊂"))
                self.bstack1lllll1l1l11_opy_.bstack1lllll1l11ll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lllll1l1l11_opy_.bstack1lllll1l1ll1_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥ⊃"), len(test_files))
            self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ⊄"), int(os.environ.get(bstack1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⊅")) or bstack1111l_opy_ (u"ࠦ࠵ࠨ⊆")))
            self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ⊇"), int(os.environ.get(bstack1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ⊈")) or bstack1111l_opy_ (u"ࠢ࠲ࠤ⊉")))
            self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧ⊊"), len(ordered_test_files))
            self.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦ⊋"), self.bstack1lllll1l1l11_opy_.bstack1lllll1ll11l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥ⊌").format(e))
        return None
    def bstack1lll11llll1_opy_(self, key, value):
        self.bstack1lllll1ll1ll_opy_[key] = value
    def bstack1l11l11111_opy_(self):
        return self.bstack1lllll1ll1ll_opy_