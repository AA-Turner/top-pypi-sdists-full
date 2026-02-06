# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack11111l1l1l1_opy_ import bstack11111ll1l11_opy_
from bstack_utils.bstack1lll1111l1_opy_ import bstack11l1lll11_opy_
from bstack_utils.helper import bstack1ll1ll111_opy_
import json
class bstack11ll1l11l1_opy_:
    _1ll11llll1l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack11111ll1l1l_opy_ = bstack11111ll1l11_opy_(self.config, logger)
        self.bstack1lll1111l1_opy_ = bstack11l1lll11_opy_.bstack1llll1l111_opy_(config=self.config)
        self.bstack11111ll11ll_opy_ = {}
        self.bstack1llll1l111l_opy_ = False
        self.bstack11111l1l1ll_opy_ = (
            self.__11111l1lll1_opy_()
            and self.bstack1lll1111l1_opy_ is not None
            and self.bstack1lll1111l1_opy_.bstack1l1ll11ll1_opy_()
            and config.get(bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᾳ"), None) is not None
            and config.get(bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᾴ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1llll1l111_opy_(cls, config, logger):
        if cls._1ll11llll1l_opy_ is None and config is not None:
            cls._1ll11llll1l_opy_ = bstack11ll1l11l1_opy_(config, logger)
        return cls._1ll11llll1l_opy_
    def bstack1l1ll11ll1_opy_(self):
        bstack11lllll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡲࠤࡳࡵࡴࠡࡣࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔ࠷࠱ࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑࡵࡨࡪࡸࡩ࡯ࡩࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᾵")
        return self.bstack11111l1l1ll_opy_ and self.bstack11111l1ll1l_opy_()
    def bstack11111l1ll1l_opy_(self):
        bstack11111ll1111_opy_ = os.getenv(bstack11lllll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ᾶ"), self.config.get(bstack11lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᾷ"), None))
        return bstack11111ll1111_opy_ in bstack111lllll1l1_opy_
    def __11111l1lll1_opy_(self):
        bstack11l11l11l1l_opy_ = False
        for fw in bstack11l111lll11_opy_:
            if fw in self.config.get(bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᾸ"), bstack11lllll_opy_ (u"ࠨࠩᾹ")):
                bstack11l11l11l1l_opy_ = True
        return bstack1ll1ll111_opy_(self.config.get(bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ὰ"), bstack11l11l11l1l_opy_))
    def bstack11111lll111_opy_(self):
        return (not self.bstack1l1ll11ll1_opy_() and
                self.bstack1lll1111l1_opy_ is not None and self.bstack1lll1111l1_opy_.bstack1l1ll11ll1_opy_())
    def bstack11111l1llll_opy_(self):
        if not self.bstack11111lll111_opy_():
            return
        if self.config.get(bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨΆ"), None) is None or self.config.get(bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᾼ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11lllll_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣࡳࡷࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠ࡯ࡷ࡯ࡰ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠴ࠢ᾽"))
        if not self.__11111l1lll1_opy_():
            self.logger.info(bstack11lllll_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥι"))
    def bstack11111l1l11l_opy_(self):
        return self.bstack1llll1l111l_opy_
    def bstack1llll1l11l1_opy_(self, bstack11111ll11l1_opy_):
        self.bstack1llll1l111l_opy_ = bstack11111ll11l1_opy_
        self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠣ᾿"), bstack11111ll11l1_opy_)
    def bstack1llll1l1l1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡰࡴࡧࡩࡷ࡯࡮ࡨ࠰ࠥ῀"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1lll1111l1_opy_.bstack11111l1ll11_opy_()
            if self.bstack1lll1111l1_opy_ is not None:
                orchestration_strategy = self.bstack1lll1111l1_opy_.bstack1l111l11l1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11lllll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤ࡮ࡹࠠࡏࡱࡱࡩ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡳࡱࡦࡩࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠲ࠧ῁"))
                return None
            self.logger.info(bstack11lllll_opy_ (u"ࠥࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣῂ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11lllll_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡇࡑࡏࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢῃ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11lllll_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡸࡪ࡫ࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣῄ"))
                self.bstack11111ll1l1l_opy_.bstack11111ll1ll1_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack11111ll1l1l_opy_.bstack11111ll1lll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣ῅"), len(test_files))
            self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥῆ"), int(os.environ.get(bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦῇ")) or bstack11lllll_opy_ (u"ࠤ࠳ࠦῈ")))
            self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢΈ"), int(os.environ.get(bstack11lllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢῊ")) or bstack11lllll_opy_ (u"ࠧ࠷ࠢΉ")))
            self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥῌ"), len(ordered_test_files))
            self.bstack1lllll111ll_opy_(bstack11lllll_opy_ (u"ࠢࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡅࡕࡏࡃࡢ࡮࡯ࡇࡴࡻ࡮ࡵࠤ῍"), self.bstack11111ll1l1l_opy_.bstack11111ll111l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡱࡧࡳࡴࡧࡶ࠾ࠥࢁࡽࠣ῎").format(e))
        return None
    def bstack1lllll111ll_opy_(self, key, value):
        self.bstack11111ll11ll_opy_[key] = value
    def bstack11l1l1ll1_opy_(self):
        return self.bstack11111ll11ll_opy_