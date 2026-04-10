# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l111ll1_opy_ import bstack1111l111l1l_opy_
from bstack_utils.constants import bstack11111ll1111_opy_, bstack11lll1l1l1_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1l111111ll_opy_
from bstack_utils import logger_utils
bstack11111111lll_opy_ = 10
class bstack1ll1ll1l1_opy_:
    def __init__(self, bstack1l1ll11l_opy_, config, bstack1llllllllll1_opy_=0):
        self.bstack1llllllll1ll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1lllllllllll_opy_ = bstack1ll_opy_ (u"ࠤࡾࢁ࠴ࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣ℻").format(bstack11111ll1111_opy_)
        self.bstack1111111111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦℼ").format(os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩℽ"))))
        self.bstack1lllllllll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦℾ").format(os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℿ"))))
        self.bstack1llllllll11l_opy_ = 2
        self.bstack1l1ll11l_opy_ = bstack1l1ll11l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11lll1l1l1_opy_)
        self.bstack1llllllllll1_opy_ = bstack1llllllllll1_opy_
        self.bstack1111111l1l1_opy_ = False
        self.bstack1111111l111_opy_ = not (
                            os.environ.get(bstack1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ⅀")) and
                            os.environ.get(bstack1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ⅁")) and
                            os.environ.get(bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ⅂"))
                        )
        if bstack1l111111ll_opy_.bstack1llllllll111_opy_(config):
            self.bstack1llllllll11l_opy_ = bstack1l111111ll_opy_.bstack11111111l11_opy_(config, self.bstack1llllllllll1_opy_)
            self.bstack11111111ll1_opy_()
    def bstack111111111l1_opy_(self):
        return bstack1ll_opy_ (u"ࠥࡿࢂࡥࡻࡾࠤ⅃").format(self.config.get(bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⅄")), os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫⅅ")))
    def bstack1111111l1ll_opy_(self):
        try:
            if self.bstack1111111l111_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1lllllllll11_opy_, bstack1ll_opy_ (u"ࠨࡲࠣⅆ")) as f:
                        bstack1llllllll1l1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1llllllll1l1_opy_ = set()
                bstack11111111l1l_opy_ = bstack1llllllll1l1_opy_ - self.bstack1llllllll1ll_opy_
                if not bstack11111111l1l_opy_:
                    return
                self.bstack1llllllll1ll_opy_.update(bstack11111111l1l_opy_)
                data = {bstack1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࠧⅇ"): list(self.bstack1llllllll1ll_opy_), bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦⅈ"): self.config.get(bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬⅉ")), bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ⅊"): os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ⅋")), bstack1ll_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ⅌"): self.config.get(bstack1ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⅍"))}
            response = bstack1111l111l1l_opy_.bstack1lllllll1ll1_opy_(self.bstack1lllllllllll_opy_, data)
            if response.get(bstack1ll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢⅎ")) == 200:
                self.logger.debug(bstack1ll_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡴࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ⅏").format(data))
            else:
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ⅐").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ⅑").format(e))
    def bstack1111111l11l_opy_(self):
        if self.bstack1111111l111_opy_:
            with self.lock:
                try:
                    with open(self.bstack1lllllllll11_opy_, bstack1ll_opy_ (u"ࠦࡷࠨ⅒")) as f:
                        bstack1lllllll1lll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1lllllll1lll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠣ⅓").format(failed_count))
                if failed_count >= self.bstack1llllllll11l_opy_:
                    self.logger.info(bstack1ll_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ⅔").format(failed_count, self.bstack1llllllll11l_opy_))
                    self.bstack1lllllllll1l_opy_(failed_count)
                    self.bstack1111111l1l1_opy_ = True
            return
        try:
            response = bstack1111l111l1l_opy_.bstack1111111l11l_opy_(bstack1ll_opy_ (u"ࠢࡼࡿࡂࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࡃࡻࡾࠨࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠽ࡼࡿࠩࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥ࠾ࡽࢀࠦ⅕").format(self.bstack1lllllllllll_opy_, self.config.get(bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⅖")), os.environ.get(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⅗")), self.config.get(bstack1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⅘"))))
            if response.get(bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ⅙")) == 200:
                failed_count = response.get(bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࡆࡳࡺࡴࡴࠣ⅚"), 0)
                self.logger.debug(bstack1ll_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣ⅛").format(failed_count))
                if failed_count >= self.bstack1llllllll11l_opy_:
                    self.logger.info(bstack1ll_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ⅜").format(failed_count, self.bstack1llllllll11l_opy_))
                    self.bstack1lllllllll1l_opy_(failed_count)
                    self.bstack1111111l1l1_opy_ = True
            else:
                self.logger.error(bstack1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵ࡬࡭ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧ⅝").format(response))
        except Exception as e:
            self.logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶ࡯࡭࡮࡬ࡲ࡬ࡀࠠࡼࡿࠥ⅞").format(e))
    def bstack1lllllllll1l_opy_(self, failed_count):
        with open(self.bstack1111111111l_opy_, bstack1ll_opy_ (u"ࠥࡻࠧ⅟")) as f:
            f.write(bstack1ll_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࡣࡷࠤࢀࢃ࡜࡯ࠤⅠ").format(datetime.now()))
            f.write(bstack1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃ࡜࡯ࠤⅡ").format(failed_count))
        self.logger.debug(bstack1ll_opy_ (u"ࠨࡁࡣࡱࡵࡸࠥࡈࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࢃࠢⅢ").format(self.bstack1111111111l_opy_))
    def bstack11111111ll1_opy_(self):
        def bstack111111111ll_opy_():
            while not self.bstack1111111l1l1_opy_:
                time.sleep(bstack11111111lll_opy_)
                self.bstack1111111l1ll_opy_()
                self.bstack1111111l11l_opy_()
        bstack11111111111_opy_ = threading.Thread(target=bstack111111111ll_opy_, daemon=True)
        bstack11111111111_opy_.start()