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
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111ll1l1ll1_opy_ import bstack111ll1ll1ll_opy_
from bstack_utils.constants import bstack111ll111l1l_opy_, bstack11l1111lll_opy_
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from bstack_utils import logger_utils
bstack111l111ll1l_opy_ = 10
class bstack1l1lllll_opy_:
    def __init__(self, bstack11l11l11ll_opy_, config, bstack111l11ll1l1_opy_=0):
        self.bstack111l11lll11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l111lll1_opy_ = bstack1111l_opy_ (u"ࠦࢀࢃ࠯ࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡫ࡧࡩ࡭ࡧࡧ࠱ࡹ࡫ࡳࡵࡵࠥợ").format(bstack111ll111l1l_opy_)
        self.bstack111l11ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨỤ").format(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫụ"))))
        self.bstack111l11l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨỦ").format(os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ủ"))))
        self.bstack111l11ll1ll_opy_ = 2
        self.bstack11l11l11ll_opy_ = bstack11l11l11ll_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11l1111lll_opy_)
        self.bstack111l11ll1l1_opy_ = bstack111l11ll1l1_opy_
        self.bstack111l11l1ll1_opy_ = False
        self.bstack111l111l1l1_opy_ = not (
                            os.environ.get(bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣỨ")) and
                            os.environ.get(bstack1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨứ")) and
                            os.environ.get(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨỪ"))
                        )
        if bstack11ll11l11l_opy_.bstack111l11l111l_opy_(config):
            self.bstack111l11ll1ll_opy_ = bstack11ll11l11l_opy_.bstack111l11l1lll_opy_(config, self.bstack111l11ll1l1_opy_)
            self.bstack111l11lll1l_opy_()
    def bstack111l11llll1_opy_(self):
        return bstack1111l_opy_ (u"ࠧࢁࡽࡠࡽࢀࠦừ").format(self.config.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩỬ")), os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ử")))
    def bstack111l11l11ll_opy_(self):
        try:
            if self.bstack111l111l1l1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l11l1l11_opy_, bstack1111l_opy_ (u"ࠣࡴࠥỮ")) as f:
                        bstack111l11l1l1l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111l11l1l1l_opy_ = set()
                bstack111l11l11l1_opy_ = bstack111l11l1l1l_opy_ - self.bstack111l11lll11_opy_
                if not bstack111l11l11l1_opy_:
                    return
                self.bstack111l11lll11_opy_.update(bstack111l11l11l1_opy_)
                data = {bstack1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࠢữ"): list(self.bstack111l11lll11_opy_), bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨỰ"): self.config.get(bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧự")), bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥỲ"): os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬỳ")), bstack1111l_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧỴ"): self.config.get(bstack1111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ỵ"))}
            response = bstack111ll1ll1ll_opy_.bstack111l11lllll_opy_(self.bstack111l111lll1_opy_, data)
            if response.get(bstack1111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤỶ")) == 200:
                self.logger.debug(bstack1111l_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡶࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥỷ").format(data))
            else:
                self.logger.debug(bstack1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣỸ").format(response))
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧỹ").format(e))
    def bstack111l11l1111_opy_(self):
        if self.bstack111l111l1l1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l11l1l11_opy_, bstack1111l_opy_ (u"ࠨࡲࠣỺ")) as f:
                        bstack111l11ll111_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111l11ll111_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠥỻ").format(failed_count))
                if failed_count >= self.bstack111l11ll1ll_opy_:
                    self.logger.info(bstack1111l_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤỼ").format(failed_count, self.bstack111l11ll1ll_opy_))
                    self.bstack111l111ll11_opy_(failed_count)
                    self.bstack111l11l1ll1_opy_ = True
            return
        try:
            response = bstack111ll1ll1ll_opy_.bstack111l11l1111_opy_(bstack1111l_opy_ (u"ࠤࡾࢁࡄࡨࡵࡪ࡮ࡧࡒࡦࡳࡥ࠾ࡽࢀࠪࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࠿ࡾࢁࠫࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࡀࡿࢂࠨỽ").format(self.bstack111l111lll1_opy_, self.config.get(bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ỿ")), os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪỿ")), self.config.get(bstack1111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪἀ"))))
            if response.get(bstack1111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨἁ")) == 200:
                failed_count = response.get(bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࡈࡵࡵ࡯ࡶࠥἂ"), 0)
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥἃ").format(failed_count))
                if failed_count >= self.bstack111l11ll1ll_opy_:
                    self.logger.info(bstack1111l_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤἄ").format(failed_count, self.bstack111l11ll1ll_opy_))
                    self.bstack111l111ll11_opy_(failed_count)
                    self.bstack111l11l1ll1_opy_ = True
            else:
                self.logger.error(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡰ࡮࡯ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢἅ").format(response))
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠻ࠢࡾࢁࠧἆ").format(e))
    def bstack111l111ll11_opy_(self, failed_count):
        with open(self.bstack111l11ll11l_opy_, bstack1111l_opy_ (u"ࠧࡽࠢἇ")) as f:
            f.write(bstack1111l_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࡥࡹࠦࡻࡾ࡞ࡱࠦἈ").format(datetime.now()))
            f.write(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾ࡞ࡱࠦἉ").format(failed_count))
        self.logger.debug(bstack1111l_opy_ (u"ࠣࡃࡥࡳࡷࡺࠠࡃࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡾࠤἊ").format(self.bstack111l11ll11l_opy_))
    def bstack111l11lll1l_opy_(self):
        def bstack111l111llll_opy_():
            while not self.bstack111l11l1ll1_opy_:
                time.sleep(bstack111l111ll1l_opy_)
                self.bstack111l11l11ll_opy_()
                self.bstack111l11l1111_opy_()
        bstack111l111l1ll_opy_ = threading.Thread(target=bstack111l111llll_opy_, daemon=True)
        bstack111l111l1ll_opy_.start()