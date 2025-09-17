# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11ll1l1_opy_ import bstack111l11l111l_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11llll1111_opy_
from bstack_utils.helper import bstack11l1ll11l1_opy_
class bstack1lll111lll_opy_:
    _1ll1llllll1_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l11ll11l_opy_ = bstack111l11l111l_opy_(self.config, logger)
        self.bstack11ll1lll1_opy_ = bstack11llll1111_opy_.bstack1lll111l1l_opy_(config=self.config)
        self.bstack111l11l1l11_opy_ = {}
        self.bstack11111ll11l_opy_ = False
        self.bstack111l11l11ll_opy_ = (
            self.__111l11lll1l_opy_()
            and self.bstack11ll1lll1_opy_ is not None
            and self.bstack11ll1lll1_opy_.bstack1l1lll1lll_opy_()
            and config.get(bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ḱ"), None) is not None
            and config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬḲ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lll111l1l_opy_(cls, config, logger):
        if cls._1ll1llllll1_opy_ is None and config is not None:
            cls._1ll1llllll1_opy_ = bstack1lll111lll_opy_(config, logger)
        return cls._1ll1llllll1_opy_
    def bstack1l1lll1lll_opy_(self):
        bstack1l11ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨḳ")
        return self.bstack111l11l11ll_opy_ and self.bstack111l111llll_opy_()
    def bstack111l111llll_opy_(self):
        return self.config.get(bstack1l11ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧḴ"), None) in bstack11l1l1ll11l_opy_
    def __111l11lll1l_opy_(self):
        bstack11l1lllllll_opy_ = False
        for fw in bstack11l1lllll1l_opy_:
            if fw in self.config.get(bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨḵ"), bstack1l11ll1_opy_ (u"࠭ࠧḶ")):
                bstack11l1lllllll_opy_ = True
        return bstack11l1ll11l1_opy_(self.config.get(bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḷ"), bstack11l1lllllll_opy_))
    def bstack111l11l1l1l_opy_(self):
        return (not self.bstack1l1lll1lll_opy_() and
                self.bstack11ll1lll1_opy_ is not None and self.bstack11ll1lll1_opy_.bstack1l1lll1lll_opy_())
    def bstack111l11l11l1_opy_(self):
        if not self.bstack111l11l1l1l_opy_():
            return
        if self.config.get(bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ḹ"), None) is None or self.config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬḹ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l11ll1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧḺ"))
        if not self.__111l11lll1l_opy_():
            self.logger.info(bstack1l11ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡫࡮ࡢࡤ࡯ࡩࠥ࡯ࡴࠡࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮ࠣḻ"))
    def bstack111l11l1lll_opy_(self):
        return self.bstack11111ll11l_opy_
    def bstack111111lll1_opy_(self, bstack111l11ll111_opy_):
        self.bstack11111ll11l_opy_ = bstack111l11ll111_opy_
        self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨḼ"), bstack111l11ll111_opy_)
    def bstack1111l11ll1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣḽ"))
                return None
            orchestration_strategy = None
            bstack111l11l1111_opy_ = self.bstack11ll1lll1_opy_.bstack111l11lll11_opy_()
            if self.bstack11ll1lll1_opy_ is not None:
                orchestration_strategy = self.bstack11ll1lll1_opy_.bstack111l1llll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥḾ"))
                return None
            self.logger.info(bstack1l11ll1_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨḿ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧṀ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1l11ll1_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨṁ"))
                self.bstack111l11ll11l_opy_.bstack111l11l1ll1_opy_(test_files, orchestration_strategy, bstack111l11l1111_opy_)
                ordered_test_files = self.bstack111l11ll11l_opy_.bstack111l11ll1ll_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨṂ"), len(test_files))
            self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣṃ"), int(os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤṄ")) or bstack1l11ll1_opy_ (u"ࠢ࠱ࠤṅ")))
            self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧṆ"), int(os.environ.get(bstack1l11ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧṇ")) or bstack1l11ll1_opy_ (u"ࠥ࠵ࠧṈ")))
            self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣṉ"), len(ordered_test_files))
            self.bstack11111lllll_opy_(bstack1l11ll1_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢṊ"), self.bstack111l11ll11l_opy_.bstack111l11llll1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨṋ").format(e))
        return None
    def bstack11111lllll_opy_(self, key, value):
        self.bstack111l11l1l11_opy_[key] = value
    def bstack1l1ll1l1l1_opy_(self):
        return self.bstack111l11l1l11_opy_