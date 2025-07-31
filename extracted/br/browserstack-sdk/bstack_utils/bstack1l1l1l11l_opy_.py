# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11ll1ll_opy_ import bstack111l11llll1_opy_
from bstack_utils.bstack1111111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.helper import bstack11lll11ll1_opy_
class bstack1ll1lll111_opy_:
    _1lll11ll1l1_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l11l1l1l_opy_ = bstack111l11llll1_opy_(self.config, logger)
        self.bstack1111111l_opy_ = bstack11l11l1lll_opy_.bstack11l111llll_opy_(config=self.config)
        self.bstack111l1l111l1_opy_ = {}
        self.bstack1111l11l1l_opy_ = False
        self.bstack111l1l11l11_opy_ = (
            self.__111l11ll1l1_opy_()
            and self.bstack1111111l_opy_ is not None
            and self.bstack1111111l_opy_.bstack11l1l1lll1_opy_()
            and config.get(bstack1l11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ḹ"), None) is not None
            and config.get(bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬḹ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack11l111llll_opy_(cls, config, logger):
        if cls._1lll11ll1l1_opy_ is None and config is not None:
            cls._1lll11ll1l1_opy_ = bstack1ll1lll111_opy_(config, logger)
        return cls._1lll11ll1l1_opy_
    def bstack11l1l1lll1_opy_(self):
        bstack1l11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨḺ")
        return self.bstack111l1l11l11_opy_ and self.bstack111l11ll111_opy_()
    def bstack111l11ll111_opy_(self):
        return self.config.get(bstack1l11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧḻ"), None) in bstack11l1ll1ll1l_opy_
    def __111l11ll1l1_opy_(self):
        bstack11ll11111l1_opy_ = False
        for fw in bstack11l1ll11lll_opy_:
            if fw in self.config.get(bstack1l11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨḼ"), bstack1l11l11_opy_ (u"࠭ࠧḽ")):
                bstack11ll11111l1_opy_ = True
        return bstack11lll11ll1_opy_(self.config.get(bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḾ"), bstack11ll11111l1_opy_))
    def bstack111l1l1111l_opy_(self):
        return (not self.bstack11l1l1lll1_opy_() and
                self.bstack1111111l_opy_ is not None and self.bstack1111111l_opy_.bstack11l1l1lll1_opy_())
    def bstack111l11l1ll1_opy_(self):
        if not self.bstack111l1l1111l_opy_():
            return
        if self.config.get(bstack1l11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ḿ"), None) is None or self.config.get(bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬṀ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l11l11_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧṁ"))
        if not self.__111l11ll1l1_opy_():
            self.logger.info(bstack1l11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧṂ"))
    def bstack111l11lllll_opy_(self):
        return self.bstack1111l11l1l_opy_
    def bstack1111l11l11_opy_(self, bstack111l11lll1l_opy_):
        self.bstack1111l11l1l_opy_ = bstack111l11lll1l_opy_
        self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨṃ"), bstack111l11lll1l_opy_)
    def bstack11111l1l11_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l11l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣṄ"))
                return None
            orchestration_strategy = None
            bstack111l11lll11_opy_ = self.bstack1111111l_opy_.bstack111l11ll11l_opy_()
            if self.bstack1111111l_opy_ is not None:
                orchestration_strategy = self.bstack1111111l_opy_.bstack1ll11111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l11l11_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥṅ"))
                return None
            self.logger.info(bstack1l11l11_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨṆ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧṇ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1l11l11_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨṈ"))
                self.bstack111l11l1l1l_opy_.bstack111l11l1lll_opy_(test_files, orchestration_strategy, bstack111l11lll11_opy_)
                ordered_test_files = self.bstack111l11l1l1l_opy_.bstack111l1l11111_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨṉ"), len(test_files))
            self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣṊ"), int(os.environ.get(bstack1l11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤṋ")) or bstack1l11l11_opy_ (u"ࠢ࠱ࠤṌ")))
            self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧṍ"), int(os.environ.get(bstack1l11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧṎ")) or bstack1l11l11_opy_ (u"ࠥ࠵ࠧṏ")))
            self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣṐ"), len(ordered_test_files))
            self.bstack11111ll1ll_opy_(bstack1l11l11_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢṑ"), self.bstack111l11l1l1l_opy_.bstack111l1l111ll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨṒ").format(e))
        return None
    def bstack11111ll1ll_opy_(self, key, value):
        self.bstack111l1l111l1_opy_[key] = value
    def bstack1ll11l11l_opy_(self):
        return self.bstack111l1l111l1_opy_