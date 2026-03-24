# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111l1lll11l_opy_ import bstack111l1llll11_opy_
from bstack_utils.constants import bstack111l11ll11l_opy_, bstack1111lll111_opy_
from bstack_utils.bstack1lll11llll_opy_ import bstack1l11ll1ll1_opy_
from bstack_utils import logger_utils
bstack1111ll1lll1_opy_ = 10
class bstack11lll1ll1_opy_:
    def __init__(self, bstack1lll1l111l_opy_, config, bstack111l11111l1_opy_=0):
        self.bstack111l111111l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1111lll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠳ࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡨࡤ࡭ࡱ࡫ࡤ࠮ࡶࡨࡷࡹࡹࠢἴ").format(bstack111l11ll11l_opy_)
        self.bstack1111lll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠤࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡼࡿࠥἵ").format(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἶ"))))
        self.bstack1111llll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥἷ").format(os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪἸ"))))
        self.bstack1111llll1ll_opy_ = 2
        self.bstack1lll1l111l_opy_ = bstack1lll1l111l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1111lll111_opy_)
        self.bstack111l11111l1_opy_ = bstack111l11111l1_opy_
        self.bstack1111lllll11_opy_ = False
        self.bstack111l1111111_opy_ = not (
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧἹ")) and
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥἺ")) and
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥἻ"))
                        )
        if bstack1l11ll1ll1_opy_.bstack1111ll1llll_opy_(config):
            self.bstack1111llll1ll_opy_ = bstack1l11ll1ll1_opy_.bstack1111llllll1_opy_(config, self.bstack111l11111l1_opy_)
            self.bstack1111lllllll_opy_()
    def bstack1111lll1l11_opy_(self):
        return bstack1ll1lll_opy_ (u"ࠤࡾࢁࡤࢁࡽࠣἼ").format(self.config.get(bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ἵ")), os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪἾ")))
    def bstack1111llll11l_opy_(self):
        try:
            if self.bstack111l1111111_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111llll1l1_opy_, bstack1ll1lll_opy_ (u"ࠧࡸࠢἿ")) as f:
                        bstack111l11111ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111l11111ll_opy_ = set()
                bstack1111lllll1l_opy_ = bstack111l11111ll_opy_ - self.bstack111l111111l_opy_
                if not bstack1111lllll1l_opy_:
                    return
                self.bstack111l111111l_opy_.update(bstack1111lllll1l_opy_)
                data = {bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࠦὀ"): list(self.bstack111l111111l_opy_), bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥὁ"): self.config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫὂ")), bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢὃ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩὄ")), bstack1ll1lll_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤὅ"): self.config.get(bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ὆"))}
            response = bstack111l1llll11_opy_.bstack1111lll1l1l_opy_(self.bstack1111lll11l1_opy_, data)
            if response.get(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ὇")) == 200:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡳࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢὈ").format(data))
            else:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧὉ").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤὊ").format(e))
    def bstack1111lll11ll_opy_(self):
        if self.bstack111l1111111_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111llll1l1_opy_, bstack1ll1lll_opy_ (u"ࠥࡶࠧὋ")) as f:
                        bstack1111lll1111_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111lll1111_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠢὌ").format(failed_count))
                if failed_count >= self.bstack1111llll1ll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨὍ").format(failed_count, self.bstack1111llll1ll_opy_))
                    self.bstack1111lll1lll_opy_(failed_count)
                    self.bstack1111lllll11_opy_ = True
            return
        try:
            response = bstack111l1llll11_opy_.bstack1111lll11ll_opy_(bstack1ll1lll_opy_ (u"ࠨࡻࡾࡁࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࡂࢁࡽࠧࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡃࡻࡾࠨࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫࠽ࡼࡿࠥ὎").format(self.bstack1111lll11l1_opy_, self.config.get(bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ὏")), os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧὐ")), self.config.get(bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧὑ"))))
            if response.get(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥὒ")) == 200:
                failed_count = response.get(bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࡅࡲࡹࡳࡺࠢὓ"), 0)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢὔ").format(failed_count))
                if failed_count >= self.bstack1111llll1ll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨὕ").format(failed_count, self.bstack1111llll1ll_opy_))
                    self.bstack1111lll1lll_opy_(failed_count)
                    self.bstack1111lllll11_opy_ = True
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡴࡲ࡬ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦὖ").format(response))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡵࡵ࡬࡭࡫ࡱ࡫࠿ࠦࡻࡾࠤὗ").format(e))
    def bstack1111lll1lll_opy_(self, failed_count):
        with open(self.bstack1111lll1ll1_opy_, bstack1ll1lll_opy_ (u"ࠤࡺࠦ὘")) as f:
            f.write(bstack1ll1lll_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࡢࡶࠣࡿࢂࡢ࡮ࠣὙ").format(datetime.now()))
            f.write(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࡢ࡮ࠣ὚").format(failed_count))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡢࡰࡴࡷࠤࡇࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࢂࠨὛ").format(self.bstack1111lll1ll1_opy_))
    def bstack1111lllllll_opy_(self):
        def bstack1111llll111_opy_():
            while not self.bstack1111lllll11_opy_:
                time.sleep(bstack1111ll1lll1_opy_)
                self.bstack1111llll11l_opy_()
                self.bstack1111lll11ll_opy_()
        bstack1111lll111l_opy_ = threading.Thread(target=bstack1111llll111_opy_, daemon=True)
        bstack1111lll111l_opy_.start()