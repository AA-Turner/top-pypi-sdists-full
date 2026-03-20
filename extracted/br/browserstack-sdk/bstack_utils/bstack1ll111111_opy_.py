# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111ll111111_opy_ import bstack111l1llll11_opy_
from bstack_utils.constants import bstack111l11l1l1l_opy_, bstack1lll1l111l_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack11lllllll_opy_
from bstack_utils import logger_utils
bstack1111lll1ll1_opy_ = 10
class bstack1l11ll111_opy_:
    def __init__(self, bstack11llll1l11_opy_, config, bstack1111lll1lll_opy_=0):
        self.bstack111l111111l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l1111l11_opy_ = bstack11lll1_opy_ (u"ࠤࡾࢁ࠴ࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣἮ").format(bstack111l11l1l1l_opy_)
        self.bstack111l11111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦἯ").format(os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩἰ"))))
        self.bstack1111lll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦἱ").format(os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫἲ"))))
        self.bstack1111llll111_opy_ = 2
        self.bstack11llll1l11_opy_ = bstack11llll1l11_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1lll1l111l_opy_)
        self.bstack1111lll1lll_opy_ = bstack1111lll1lll_opy_
        self.bstack1111lll11ll_opy_ = False
        self.bstack1111lllllll_opy_ = not (
                            os.environ.get(bstack11lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨἳ")) and
                            os.environ.get(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦἴ")) and
                            os.environ.get(bstack11lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦἵ"))
                        )
        if bstack11lllllll_opy_.bstack1111lll1l1l_opy_(config):
            self.bstack1111llll111_opy_ = bstack11lllllll_opy_.bstack1111llllll1_opy_(config, self.bstack1111lll1lll_opy_)
            self.bstack111l1111ll1_opy_()
    def bstack1111lllll11_opy_(self):
        return bstack11lll1_opy_ (u"ࠥࡿࢂࡥࡻࡾࠤἶ").format(self.config.get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧἷ")), os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫἸ")))
    def bstack111l1111111_opy_(self):
        try:
            if self.bstack1111lllllll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111lll11l1_opy_, bstack11lll1_opy_ (u"ࠨࡲࠣἹ")) as f:
                        bstack1111lll111l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111lll111l_opy_ = set()
                bstack1111lll1l11_opy_ = bstack1111lll111l_opy_ - self.bstack111l111111l_opy_
                if not bstack1111lll1l11_opy_:
                    return
                self.bstack111l111111l_opy_.update(bstack1111lll1l11_opy_)
                data = {bstack11lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࠧἺ"): list(self.bstack111l111111l_opy_), bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦἻ"): self.config.get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬἼ")), bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣἽ"): os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪἾ")), bstack11lll1_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥἿ"): self.config.get(bstack11lll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫὀ"))}
            response = bstack111l1llll11_opy_.bstack1111lllll1l_opy_(self.bstack111l1111l11_opy_, data)
            if response.get(bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢὁ")) == 200:
                self.logger.debug(bstack11lll1_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡴࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣὂ").format(data))
            else:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨὃ").format(response))
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥὄ").format(e))
    def bstack1111llll1ll_opy_(self):
        if self.bstack1111lllllll_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111lll11l1_opy_, bstack11lll1_opy_ (u"ࠦࡷࠨὅ")) as f:
                        bstack1111llll1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111llll1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠣ὆").format(failed_count))
                if failed_count >= self.bstack1111llll111_opy_:
                    self.logger.info(bstack11lll1_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ὇").format(failed_count, self.bstack1111llll111_opy_))
                    self.bstack1111llll11l_opy_(failed_count)
                    self.bstack1111lll11ll_opy_ = True
            return
        try:
            response = bstack111l1llll11_opy_.bstack1111llll1ll_opy_(bstack11lll1_opy_ (u"ࠢࡼࡿࡂࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࡃࡻࡾࠨࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠽ࡼࡿࠩࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥ࠾ࡽࢀࠦὈ").format(self.bstack111l1111l11_opy_, self.config.get(bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫὉ")), os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨὊ")), self.config.get(bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨὋ"))))
            if response.get(bstack11lll1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦὌ")) == 200:
                failed_count = response.get(bstack11lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࡆࡳࡺࡴࡴࠣὍ"), 0)
                self.logger.debug(bstack11lll1_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣ὎").format(failed_count))
                if failed_count >= self.bstack1111llll111_opy_:
                    self.logger.info(bstack11lll1_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ὏").format(failed_count, self.bstack1111llll111_opy_))
                    self.bstack1111llll11l_opy_(failed_count)
                    self.bstack1111lll11ll_opy_ = True
            else:
                self.logger.error(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵ࡬࡭ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧὐ").format(response))
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶ࡯࡭࡮࡬ࡲ࡬ࡀࠠࡼࡿࠥὑ").format(e))
    def bstack1111llll11l_opy_(self, failed_count):
        with open(self.bstack111l11111ll_opy_, bstack11lll1_opy_ (u"ࠥࡻࠧὒ")) as f:
            f.write(bstack11lll1_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࡣࡷࠤࢀࢃ࡜࡯ࠤὓ").format(datetime.now()))
            f.write(bstack11lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃ࡜࡯ࠤὔ").format(failed_count))
        self.logger.debug(bstack11lll1_opy_ (u"ࠨࡁࡣࡱࡵࡸࠥࡈࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࢃࠢὕ").format(self.bstack111l11111ll_opy_))
    def bstack111l1111ll1_opy_(self):
        def bstack111l1111l1l_opy_():
            while not self.bstack1111lll11ll_opy_:
                time.sleep(bstack1111lll1ll1_opy_)
                self.bstack111l1111111_opy_()
                self.bstack1111llll1ll_opy_()
        bstack111l11111l1_opy_ = threading.Thread(target=bstack111l1111l1l_opy_, daemon=True)
        bstack111l11111l1_opy_.start()