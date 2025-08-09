# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11llll1_opy_ import bstack111l11lll11_opy_
from bstack_utils.bstack111l11l1_opy_ import bstack1l111ll11l_opy_
from bstack_utils.helper import bstack1ll1l11111_opy_
class bstack11ll1111l_opy_:
    _1llll11ll1l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1l11111_opy_ = bstack111l11lll11_opy_(self.config, logger)
        self.bstack111l11l1_opy_ = bstack1l111ll11l_opy_.bstack1l1lll11l_opy_(config=self.config)
        self.bstack111l1l11l11_opy_ = {}
        self.bstack1111l1111l_opy_ = False
        self.bstack111l1l1l11l_opy_ = (
            self.__111l1l1111l_opy_()
            and self.bstack111l11l1_opy_ is not None
            and self.bstack111l11l1_opy_.bstack1ll11llll1_opy_()
            and config.get(bstack11l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧḹ"), None) is not None
            and config.get(bstack11l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ḻ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l1lll11l_opy_(cls, config, logger):
        if cls._1llll11ll1l_opy_ is None and config is not None:
            cls._1llll11ll1l_opy_ = bstack11ll1111l_opy_(config, logger)
        return cls._1llll11ll1l_opy_
    def bstack1ll11llll1_opy_(self):
        bstack11l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡲࠤࡳࡵࡴࠡࡣࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔ࠷࠱ࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑࡵࡨࡪࡸࡩ࡯ࡩࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢḻ")
        return self.bstack111l1l1l11l_opy_ and self.bstack111l1l111l1_opy_()
    def bstack111l1l111l1_opy_(self):
        return self.config.get(bstack11l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨḼ"), None) in bstack11l1ll111ll_opy_
    def __111l1l1111l_opy_(self):
        bstack11ll1111lll_opy_ = False
        for fw in bstack11l1ll1llll_opy_:
            if fw in self.config.get(bstack11l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩḽ"), bstack11l1_opy_ (u"ࠧࠨḾ")):
                bstack11ll1111lll_opy_ = True
        return bstack1ll1l11111_opy_(self.config.get(bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḿ"), bstack11ll1111lll_opy_))
    def bstack111l1l11lll_opy_(self):
        return (not self.bstack1ll11llll1_opy_() and
                self.bstack111l11l1_opy_ is not None and self.bstack111l11l1_opy_.bstack1ll11llll1_opy_())
    def bstack111l11lllll_opy_(self):
        if not self.bstack111l1l11lll_opy_():
            return
        if self.config.get(bstack11l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧṀ"), None) is None or self.config.get(bstack11l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ṁ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11l1_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢࡲࡶࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦ࡮ࡶ࡮࡯࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠳ࠨṂ"))
        if not self.__111l1l1111l_opy_():
            self.logger.info(bstack11l1_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡮ࡹࠠࡥ࡫ࡶࡥࡧࡲࡥࡥ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡩࡳࡧࡢ࡭ࡧࠣ࡭ࡹࠦࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳ࠨṃ"))
    def bstack111l1l111ll_opy_(self):
        return self.bstack1111l1111l_opy_
    def bstack11111l1ll1_opy_(self, bstack111l1l11l1l_opy_):
        self.bstack1111l1111l_opy_ = bstack111l1l11l1l_opy_
        self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠢṄ"), bstack111l1l11l1l_opy_)
    def bstack11111l1l1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11l1_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧ࠯ࠤṅ"))
                return None
            orchestration_strategy = None
            bstack111l1l11ll1_opy_ = self.bstack111l11l1_opy_.bstack111l11lll1l_opy_()
            if self.bstack111l11l1_opy_ is not None:
                orchestration_strategy = self.bstack111l11l1_opy_.bstack111lllllll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11l1_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣ࡭ࡸࠦࡎࡰࡰࡨ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡲࡰࡥࡨࡩࡩࠦࡷࡪࡶ࡫ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠱ࠦṆ"))
                return None
            self.logger.info(bstack11l1_opy_ (u"ࠤࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢṇ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11l1_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡆࡐࡎࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨṈ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack11l1_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡷࡩࡱࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢṉ"))
                self.bstack111l1l11111_opy_.bstack111l11ll1l1_opy_(test_files, orchestration_strategy, bstack111l1l11ll1_opy_)
                ordered_test_files = self.bstack111l1l11111_opy_.bstack111l11ll1ll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢṊ"), len(test_files))
            self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤṋ"), int(os.environ.get(bstack11l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥṌ")) or bstack11l1_opy_ (u"ࠣ࠲ࠥṍ")))
            self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨṎ"), int(os.environ.get(bstack11l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨṏ")) or bstack11l1_opy_ (u"ࠦ࠶ࠨṐ")))
            self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤṑ"), len(ordered_test_files))
            self.bstack1111l111l1_opy_(bstack11l1_opy_ (u"ࠨࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡄࡔࡎࡉࡡ࡭࡮ࡆࡳࡺࡴࡴࠣṒ"), self.bstack111l1l11111_opy_.bstack111l1l1l111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡰࡦࡹࡳࡦࡵ࠽ࠤࢀࢃࠢṓ").format(e))
        return None
    def bstack1111l111l1_opy_(self, key, value):
        self.bstack111l1l11l11_opy_[key] = value
    def bstack111lll111_opy_(self):
        return self.bstack111l1l11l11_opy_