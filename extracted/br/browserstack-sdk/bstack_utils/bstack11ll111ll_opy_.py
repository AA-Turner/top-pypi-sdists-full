# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1ll11ll_opy_ import bstack111l1l1l1l1_opy_
from bstack_utils.bstack1l11ll11_opy_ import bstack1ll11l11l1_opy_
from bstack_utils.helper import bstack11l1111ll_opy_
class bstack11l1ll11ll_opy_:
    _1lll1ll111l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1l1lll1_opy_ = bstack111l1l1l1l1_opy_(self.config, logger)
        self.bstack1l11ll11_opy_ = bstack1ll11l11l1_opy_.bstack1l1l11ll_opy_(config=self.config)
        self.bstack111l1ll1111_opy_ = {}
        self.bstack11111l1l11_opy_ = False
        self.bstack111l1l1l1ll_opy_ = (
            self.__111l1l1ll1l_opy_()
            and self.bstack1l11ll11_opy_ is not None
            and self.bstack1l11ll11_opy_.bstack11l1ll1lll_opy_()
            and config.get(bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᷩ"), None) is not None
            and config.get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᷪ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l1l11ll_opy_(cls, config, logger):
        if cls._1lll1ll111l_opy_ is None and config is not None:
            cls._1lll1ll111l_opy_ = bstack11l1ll11ll_opy_(config, logger)
        return cls._1lll1ll111l_opy_
    def bstack11l1ll1lll_opy_(self):
        bstackl_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊ࡯ࠡࡰࡲࡸࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡼ࡮ࡥ࡯࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑ࠴࠵ࡾࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᷫ")
        return self.bstack111l1l1l1ll_opy_ and self.bstack111l1l1llll_opy_()
    def bstack111l1l1llll_opy_(self):
        return self.config.get(bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᷬ"), None) in bstack11l1ll1ll1l_opy_
    def __111l1l1ll1l_opy_(self):
        bstack11ll1111l1l_opy_ = False
        for fw in bstack11l1ll1l11l_opy_:
            if fw in self.config.get(bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᷭ"), bstackl_opy_ (u"ࠫࠬᷮ")):
                bstack11ll1111l1l_opy_ = True
        return bstack11l1111ll_opy_(self.config.get(bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᷯ"), bstack11ll1111l1l_opy_))
    def bstack111l1l11lll_opy_(self):
        return (not self.bstack11l1ll1lll_opy_() and
                self.bstack1l11ll11_opy_ is not None and self.bstack1l11ll11_opy_.bstack11l1ll1lll_opy_())
    def bstack111l1ll11l1_opy_(self):
        if not self.bstack111l1l11lll_opy_():
            return
        if self.config.get(bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᷰ"), None) is None or self.config.get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᷱ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstackl_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦ࡯ࡳࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡲࡺࡲ࡬࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡶࡩࡹࠦࡡࠡࡰࡲࡲ࠲ࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦ࠰ࠥᷲ"))
        if not self.__111l1l1ll1l_opy_():
            self.logger.info(bstackl_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥᷳ"))
    def bstack111l1l1l111_opy_(self):
        return self.bstack11111l1l11_opy_
    def bstack11111l1ll1_opy_(self, bstack111l1l1l11l_opy_):
        self.bstack11111l1l11_opy_ = bstack111l1l1l11l_opy_
        self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠦᷴ"), bstack111l1l1l11l_opy_)
    def bstack1111l1l111_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstackl_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫࠳ࠨ᷵"))
                return None
            orchestration_strategy = None
            if self.bstack1l11ll11_opy_ is not None:
                orchestration_strategy = self.bstack1l11ll11_opy_.bstack1llll1llll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstackl_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠࡪࡵࠣࡒࡴࡴࡥ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡶࡴࡩࡥࡦࡦࠣࡻ࡮ࡺࡨࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴ࠮ࠣ᷶"))
                return None
            self.logger.info(bstackl_opy_ (u"ࠨࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀ᷷ࠦ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstackl_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡃࡍࡋࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰᷸ࠥ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstackl_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡴࡦ࡮ࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱᷹ࠦ"))
                self.bstack111l1l1lll1_opy_.bstack111l1ll111l_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack111l1l1lll1_opy_.bstack111l1l11ll1_opy_()
            if not ordered_test_files:
                return None
            self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡉ࡯ࡶࡰࡷ᷺ࠦ"), len(test_files))
            self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ᷻"), int(os.environ.get(bstackl_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ᷼")) or bstackl_opy_ (u"ࠧ࠶᷽ࠢ")))
            self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ᷾"), int(os.environ.get(bstackl_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖ᷿ࠥ")) or bstackl_opy_ (u"ࠣ࠳ࠥḀ")))
            self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨḁ"), len(ordered_test_files))
            self.bstack1111l11111_opy_(bstackl_opy_ (u"ࠥࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹࡁࡑࡋࡆࡥࡱࡲࡃࡰࡷࡱࡸࠧḂ"), self.bstack111l1l1lll1_opy_.bstack111l1l1ll11_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣ࡭ࡣࡶࡷࡪࡹ࠺ࠡࡽࢀࠦḃ").format(e))
        return None
    def bstack1111l11111_opy_(self, key, value):
        self.bstack111l1ll1111_opy_[key] = value
    def bstack11l11l1ll_opy_(self):
        return self.bstack111l1ll1111_opy_