# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll11llll1l_opy_ import bstack1lll11l1lll1_opy_
from bstack_utils.bstack111llll111_opy_ import bstack1ll11l1l_opy_
from bstack_utils.helper import bstack1lllll11ll1_opy_
import json
class bstack111lll1l1l_opy_:
    _1l1llllllll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll11lll1ll_opy_ = bstack1lll11l1lll1_opy_(self.config, logger)
        self.bstack111llll111_opy_ = bstack1ll11l1l_opy_.bstack1l1l11ll1_opy_(config=self.config)
        self.bstack1lll11ll11l1_opy_ = {}
        self.bstack1llll1l1lll_opy_ = False
        self.bstack1lll11ll111l_opy_ = (
            self.__1lll11ll1ll1_opy_()
            and self.bstack111llll111_opy_ is not None
            and self.bstack111llll111_opy_.bstack11lll11l1_opy_()
            and config.get(bstack111ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ┽"), None) is not None
            and config.get(bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ┾"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l1l11ll1_opy_(cls, config, logger):
        if cls._1l1llllllll_opy_ is None and config is not None:
            cls._1l1llllllll_opy_ = bstack111lll1l1l_opy_(config, logger)
        return cls._1l1llllllll_opy_
    def bstack11lll11l1_opy_(self):
        bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊ࡯ࠡࡰࡲࡸࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡼ࡮ࡥ࡯࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑ࠴࠵ࡾࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ┿")
        return self.bstack1lll11ll111l_opy_ and self.bstack1lll11lll1l1_opy_()
    def bstack1lll11lll1l1_opy_(self):
        bstack1lll11ll1l1l_opy_ = os.getenv(bstack111ll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ╀"), self.config.get(bstack111ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭╁"), None))
        return bstack1lll11ll1l1l_opy_ in bstack1111111ll11_opy_
    def __1lll11ll1ll1_opy_(self):
        bstack11111l1llll_opy_ = False
        for fw in bstack11111111l11_opy_:
            if fw in self.config.get(bstack111ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ╂"), bstack111ll_opy_ (u"ࠬ࠭╃")):
                bstack11111l1llll_opy_ = True
        return bstack1lllll11ll1_opy_(self.config.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ╄"), bstack11111l1llll_opy_))
    def bstack1lll11lll111_opy_(self):
        return (not self.bstack11lll11l1_opy_() and
                self.bstack111llll111_opy_ is not None and self.bstack111llll111_opy_.bstack11lll11l1_opy_())
    def bstack1lll11llll11_opy_(self):
        if not self.bstack1lll11lll111_opy_():
            return
        if self.config.get(bstack111ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ╅"), None) is None or self.config.get(bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ╆"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack111ll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡰࡴࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡳࡻ࡬࡭࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡻࡧ࡬ࡶࡧ࠱ࠦ╇"))
        if not self.__1lll11ll1ll1_opy_():
            self.logger.info(bstack111ll_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡪࡴࡡࡣ࡮ࡨࠤ࡮ࡺࠠࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴ࠢ╈"))
    def bstack1lll11ll1lll_opy_(self):
        return self.bstack1llll1l1lll_opy_
    def bstack1llll1ll1ll_opy_(self, bstack1lll11ll11ll_opy_):
        self.bstack1llll1l1lll_opy_ = bstack1lll11ll11ll_opy_
        self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠧ╉"), bstack1lll11ll11ll_opy_)
    def bstack1llll1llll1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack111ll_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬࠴ࠢ╊"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111llll111_opy_.bstack1lll11l1llll_opy_()
            if self.bstack111llll111_opy_ is not None:
                orchestration_strategy = self.bstack111llll111_opy_.bstack1lllll111ll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack111ll_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡ࡫ࡶࠤࡓࡵ࡮ࡦ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡷࡵࡣࡦࡧࡧࠤࡼ࡯ࡴࡩࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠯ࠤ╋"))
                return None
            self.logger.info(bstack111ll_opy_ (u"ࠢࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧ╌").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡄࡎࡌࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦ╍"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡵࡧ࡯ࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ╎"))
                self.bstack1lll11lll1ll_opy_.bstack1lll11ll1l11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll11lll1ll_opy_.bstack1lll11ll1111_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧ╏"), len(test_files))
            self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ═"), int(os.environ.get(bstack111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ║")) or bstack111ll_opy_ (u"ࠨ࠰ࠣ╒")))
            self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ╓"), int(os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ╔")) or bstack111ll_opy_ (u"ࠤ࠴ࠦ╕")))
            self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢ╖"), len(ordered_test_files))
            self.bstack1llll1lll1l_opy_(bstack111ll_opy_ (u"ࠦࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࡂࡒࡌࡇࡦࡲ࡬ࡄࡱࡸࡲࡹࠨ╗"), self.bstack1lll11lll1ll_opy_.bstack1lll11lll11l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤ࡮ࡤࡷࡸ࡫ࡳ࠻ࠢࡾࢁࠧ╘").format(e))
        return None
    def bstack1llll1lll1l_opy_(self, key, value):
        self.bstack1lll11ll11l1_opy_[key] = value
    def bstack1lll1111_opy_(self):
        return self.bstack1lll11ll11l1_opy_